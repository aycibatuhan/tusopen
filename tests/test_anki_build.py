import re
import shutil
import subprocess
import tempfile

import pytest

from tusopen.export.anki import build as ab
from tusopen.export.simulator import build as sb


def test_split_sentences_abbrevs():
    sents = ab._split_sentences(
        "P. vivax kanıtında görüldü. Bu ikinci cümledir. Dr. Ahim geldi üçe kaldı?")
    assert len(sents) == 3
    assert sents[0].startswith("P. vivax")


def test_prose_html():
    assert ab._prose_html("Bir. İki.") == "Bir.<br>İki."
    assert ab._prose_html("") == ""
    assert ab._prose_html(None) == ""


def test_split_answer_explanation():
    cevap, aciklama = ab._split_answer_explanation(
        "Kısa cevap cümlesi buradadır. Uzun açıklama ikinci cümledir ve "
        "gerekçeyi anlatarak devam eder, yeterince uzundur.")
    assert cevap.startswith("Kısa cevap")
    assert aciklama.startswith("Uzun")


def test_cloze_chunks_short_value_single():
    assert ab._cloze_chunks("Tek cümle.") == ["Tek cümle."]


def test_cloze_chunks_long_value_atomic():
    val = ". ".join(f"Cümle numarası {i} buraya geldi" for i in range(1, 5)) + "."
    chunks = ab._cloze_chunks(val)
    assert 2 <= len(chunks) <= ab.MAX_CLOZE_CHUNKS
    assert all("Cümle numarası" in c for c in chunks)


def test_cloze_chunks_cap():
    val = ". ".join(f"Yeterince uzun cümle numarası {i} burada" for i in range(10)) + "."
    chunks = ab._cloze_chunks(val)
    assert len(chunks) == ab.MAX_CLOZE_CHUNKS


def test_allocator_unique_and_deterministic():
    a1, a2 = ab._make_allocator(), ab._make_allocator()
    key = ("ktbt", "dahiliye", "dah_hepatoloji", "dah_hep_wilson_hemokromatoz")
    assert [a1(key), a1(key), a1(key)] == [1, 2, 3]
    assert a2(key) == 1


def test_gorsel_attribution(tmp_path):
    fact = {"gorsel": {"dosya": "x.jpg", "yazar": "Foto Grek", "lisans": "CC BY-SA 3.0",
                       "kaynak": "Wikimedia", "etiketler": [
                           {"ad": "Yapı", "x": 10, "y": 10, "w": 20, "h": 10}]}}
    html = ab._gorsel_html(fact)
    assert "io-mask" in html and "c1::Yapı" in html
    assert "Foto Grek" in html and "CC BY-SA 3.0" in html
    assert ab._gorsel_html({"gorsel": {}}) is None


def test_siklik_text():
    assert ab._siklik_text(0) == ""
    assert ab._siklik_text(3) == "3 sınavda soruldu"


def test_models_shape():
    models = ab._models()
    assert set(models) == {"bilgi", "vaka", "ayirici", "celdirici", "spot", "gorsel"}
    for m in models.values():
        assert m.sort_field_index == len(ab.COMMON_FIELDS)


def test_script_notes_spot_atomized(tmp_content, repo_root):
    from tusopen.export.anki.build import _load_taxonomy, _load_yaml, _make_allocator, _script_notes
    ads, pos, tree_ids = _load_taxonomy(repo_root / "taxonomy" / "taxonomy.json")
    script = _load_yaml(tmp_content / "scripts" / "dahiliye" / "test_hastalik.yaml")
    notes = _script_notes(script, ab._models(), ads, tree_ids, _make_allocator())
    spots = [n for n in notes if "tus_spot" in n.tags]
    spot = next(n for n in spots if "Tanı birinci" in n.fields[10])
    cloze_nums = set(re.findall(r"\{\{c(\d+)::", spot.fields[10]))
    assert len(cloze_nums) == ab.MAX_CLOZE_CHUNKS
    # short single-sentence fields stay one deletion
    single = next(n for n in spots if "Tek cümlelik tetkik" in n.fields[10])
    assert re.findall(r"\{\{c(\d+)::", single.fields[10]) == ["1"]
    # anahtar_bulgular listesi: madde başına kart, stem görünür
    bulgu = next(n for n in spots if "Birinci bulgu" in n.fields[10])
    assert "anahtar bulgusu (1/2)" in bulgu.fields[10]
    assert "{{c1::Birinci bulgu}}" in bulgu.fields[10]
    guids = [n.guid for n in notes]
    assert len(guids) == len(set(guids))


def test_vurgu_cloze_grouping():
    html = ab._vurgu_html(
        "Ampirik: **seftriakson** veya **vankomisin**; Listeria'da **ampisilin** eklenir.")
    # aynı segmentteki işaretler aynı indeksi paylaşır, yeni segment yeni indeks
    assert "{{c1::<b>seftriakson</b>}}" in html
    assert "{{c1::<b>vankomisin</b>}}" in html
    assert "{{c2::<b>ampisilin</b>}}" in html
    assert html.count("<b>") == 3
    # gövde görünür kalır (ipucu)
    assert html.index("Ampirik: ") < html.index("{{c1::")
    # işaretsiz değer fallback'e düşer
    assert ab._vurgu_html("işaretsiz düz metin") is None


def test_script_notes_vurgu_spot(tmp_content, repo_root):
    from tusopen.export.anki.build import _load_taxonomy, _load_yaml, _make_allocator, _script_notes
    ads, pos, tree_ids = _load_taxonomy(repo_root / "taxonomy" / "taxonomy.json")
    script = _load_yaml(tmp_content / "scripts" / "dahiliye" / "test_hastalik.yaml")
    script["ilk_tedavi"] = ("Kültür sonrası ampirik tedavi: **seftriakson** veya "
                            "**vankomisin**; Listeria riskinde **ampisilin** eklenir.")
    notes = _script_notes(script, ab._models(), ads, tree_ids, _make_allocator())
    spot = next(n for n in notes
                if "tus_spot" in n.tags and "seftriakson" in n.fields[10])
    assert "{{c1::<b>seftriakson</b>}}" in spot.fields[10]
    # tam ifade gizlenmez: gövde metni görünür kalır
    assert "Kültür sonrası ampirik tedavi:" in spot.fields[10]
    assert "ampirik tedavi: <br>" not in spot.fields[10]


def test_simulator_build_smoke(tmp_content, tmp_path):
    out = tmp_path / "sim"
    n = sb.run(tmp_content, out)
    assert n == 1
    html = (out / "index.html").read_text(encoding="utf-8")
    assert 'setAttribute("aria-live", "polite")' in html
    assert "white-space:pre-line" in html
    _js_parse_check(html)


def _js_parse_check(html: str):
    """Round-2 lesson: substring greps cannot catch broken JS. Parse it."""
    m = re.search(r"<script>\n(.*)</script>\s*</body>", html, re.S)
    assert m, "script block not found"
    node = shutil.which("node")
    if not node:
        pytest.skip("node not available for JS syntax check")
    f = tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                    encoding="utf-8")
    f.write(m.group(1))
    f.close()
    r = subprocess.run([node, "--check", f.name], capture_output=True, text=True)
    assert r.returncode == 0, f"simulator JS syntax error:\n{r.stderr}"
