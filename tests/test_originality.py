import json

from tusopen.validate import originality as orig

REF_STEM = ("Yetmiş yaşında erkek hastada progresif dizi ağrısı, sabah tutukluğu ve "
            "yürüme mesafesinde kısalma saptanıyor; radyografide medial kompartman "
            "darlığı belirgin ve klinik tablo gonartroz ile uyumludur. Hastanın vücut "
            "ağırlığı 92 kilogramdır ve altı aydır semptomları ilerlemektedir. "
            "Aşağıdaki tedavi seçeneklerinden hangisi bu hastada ilk basamak olarak "
            "önerilir bu soruda yer alan ifadeyle devam etmektedir?")


def _make_cache(tmp_path, stem):
    cache = tmp_path / "cache"
    (cache / "parsed").mkdir(parents=True)
    (cache / "parsed" / "2099-ilkbahar_TTBT.json").write_text(json.dumps({
        "exam_id": "2099-ilkbahar", "test": "TTBT",
        "questions": [{"number": 1, "stem": stem,
                       "options": {"A": "Primer total diz protezi hemen yapılmalıdır",
                                   "B": "Kilo verme ve quadriseps güçlendirme önerilir",
                                   "C": "Sistemik steroid başlanması uygundur",
                                   "D": "İntraartiküler radyoaktif sinovektomi yapılmalıdır",
                                   "E": "Hemen artroskopik debridman yapılmalıdır"},
                       "answer": "B", "iptal": False}]}, ensure_ascii=False),
        encoding="utf-8")
    return cache


def _make_content(tmp_path, **fields):
    root = tmp_path / "content"
    root.mkdir(exist_ok=True)
    lines = ["id: test_kopya", "version: 1", "status: draft", "author: t",
             "sources: ['kaynak']", "ad: Test", "taksonomi:",
             "  - [ttbt, anatomi, anat_genel, anat_genel_terminoloji]"]
    for k, v in fields.items():
        lines.append(f"{k}: \"{v}\"")
    (root / "k.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return root


def test_missing_cache_is_graceful(tmp_path):
    assert orig.run(tmp_path / "content", tmp_path / "cache") == []


def test_verbatim_caught_by_all_layers(tmp_path):
    cache = _make_cache(tmp_path, REF_STEM)
    root = _make_content(tmp_path, metin=REF_STEM)
    findings = orig.run(root, cache)
    assert findings
    assert any("metin" in f and "window" in f for f in findings)
    assert any("shingle" in f for f in findings)


def test_close_paraphrase_caught(tmp_path):
    cache = _make_cache(tmp_path, REF_STEM)
    words = REF_STEM.split()
    swaps = {"progresif": "ilerleyici", "tutukluğu": "katılığı",
             "radyografide": "grafide", "kompartman": "bölümde",
             "gonartroz": "artroz", "kilogramdır": "kg'dır",
             "ilerlemektedir": "artmaktadır", "seçeneklerinden": "önerilerinden"}
    swapped = " ".join(swaps.get(w, w) for w in words)
    assert swapped != REF_STEM
    root = _make_content(tmp_path, metin=swapped)
    findings = orig.run(root, cache)
    assert findings, "one-word-substituted copy must still be flagged"


def test_lab_values_and_original_text_pass(tmp_path):
    cache = _make_cache(tmp_path, REF_STEM)
    root = _make_content(
        tmp_path,
        metin1="Kan biyokimyasında Na 118 mEq/L, K 4.1 mEq/L ve Cl 92 mEq/L saptandı.",
        metin2="Bu tamamen özgün bir cümledir ve hiçbir kaynakla örtüşmez, kelimeleri farklıdır.")
    assert orig.run(root, cache) == []


def test_short_nomenclature_not_flagged(tmp_path):
    cache = _make_cache(tmp_path, REF_STEM)
    root = _make_content(tmp_path, ad="Hipokalemik hipokloremik metabolik alkaloz")
    assert orig.run(root, cache) == []


def test_labish_helper():
    assert orig._labish(("na", "119", "meq", "l", "k", "4"))
    assert not orig._labish(("hastada", "ani", "başlayan", "şiddetli", "ağrı", "vardır"))
