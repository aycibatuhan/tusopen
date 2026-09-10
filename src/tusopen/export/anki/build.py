"""Build the Anki deck from content/ (plan §6.5, §7).

- genanki with stable note GUIDs derived from content ids:
  guid_for("tusopen", <content id>, <card type>, <key>) — never random.
- single deck, navigation via tags; tags are stamped from data.
- note types: Bilgi, Vaka, Ayırıcı (from illness scripts), Çeldirici
  (only from walkthroughs' celdirici_kavramlar, per plan §7).
- siklik badge derived from the number of distinct sittings in tus_gecmisi.
"""
import json
import re
from pathlib import Path

import genanki
import yaml

DECK_ID = 1985217159
DECK_NAME = "TUS Open"
DECK_VERSION = "0.4.0-alpha"
TAG_PREFIX = "TUS_v1"

MODEL_IDS = {
    "bilgi": 1746821301,
    "vaka": 1746821302,
    "ayirici": 1746821303,
    "celdirici": 1746821304,
    "spot": 1746821305,
    "gorsel": 1746821306,
}

COMMON_FIELDS = ["id", "tree_id", "ders", "konu", "alt_konu", "siklik", "kaynak",
                 "hastalik", "versiyon", "notlar"]

CSS = (".card{font-size:17px;line-height:1.5;color:#222;}"
       ".vinyet{background:#f5f5f5;color:#222;padding:8px;border-radius:6px;margin-bottom:8px;}"
       ".badge{display:inline-block;background:#eef;border-radius:4px;"
       "padding:1px 6px;font-size:smaller;margin-bottom:8px;color:#35c;}"
       ".aciklama{color:#666;font-size:smaller;margin-top:8px;}"
       ".cevap-kisa{font-size:18px;font-weight:600;margin:4px 0 8px 0;}"
       ".explanation{margin-top:16px;padding-top:10px;border-top:1px solid #ddd;"
       "font-size:15px;color:#555;}"
       ".kaynak{font-size:12px;color:#999;margin-top:10px;}"
       ".night_mode .kaynak,.nightMode .kaynak{color:#777;}"
       "table{border-collapse:collapse;margin-top:6px;}"
       "td,th{border:1px solid #ccc;padding:4px 8px;text-align:left;}"
       ".night_mode .card,.nightMode .card{color:#e8e8e8;}"
       ".night_mode .vinyet,.nightMode .vinyet{background:#333;color:#e8e8e8;}"
       ".night_mode .badge,.nightMode .badge{background:#25324a;color:#9ec1ff;}"
       ".night_mode .aciklama,.nightMode .aciklama{color:#aaa;}"
       ".night_mode .cevap-kisa,.nightMode .cevap-kisa{color:#fff;}"
       ".night_mode .explanation,.nightMode .explanation{border-top-color:#444;color:#aaa;}"
       ".night_mode td,.night_mode th,.nightMode td,.nightMode th{border-color:#555;}"
       ".io-container{position:relative;display:inline-block;max-width:100%;}"
       ".io-img{max-width:100%;display:block;border-radius:4px;}"
       ".io-mask{position:absolute;background:#333;color:transparent;"
       "border-radius:2px;font-size:11px;padding:2px;overflow:hidden;"
       "display:flex;align-items:center;justify-content:center;text-align:center;}"
       ".io-mask .cloze{color:#fff;}"
       ".night_mode .io-mask,.nightMode .io-mask{background:#555;}")

MODELS = {
    "bilgi": (
        ["soru", "cevap", "aciklama"],
        '<div class="vinyet">{{soru}}</div>{{#siklik}}<div class="badge">{{siklik}}</div>{{/siklik}}',
        '{{FrontSide}}<hr id=answer><div class="cevap-kisa">{{cevap}}</div>'
        '{{#aciklama}}<div class="explanation">{{aciklama}}</div>{{/aciklama}}'
        '{{#kaynak}}<div class="kaynak">TUS: {{kaynak}}</div>{{/kaynak}}',
    ),
    "vaka": (
        ["vinyet", "soru_tipi", "cevap", "anahtar_bulgular", "aciklama"],
        '<div class="vinyet">{{vinyet}}</div><div>{{soru_tipi}} nedir?</div>'
        '{{#siklik}}<div class="badge">{{siklik}}</div>{{/siklik}}',
        '{{FrontSide}}<hr id=answer><div class="cevap-kisa">{{cevap}}</div>'
        '{{#aciklama}}<div class="explanation">{{aciklama}}</div>{{/aciklama}}'
        '{{#kaynak}}<div class="kaynak">TUS: {{kaynak}}</div>{{/kaynak}}',
    ),
    "ayirici": (
        ["tablo"],
        '<div class="vinyet">Bu hastalıklar nasıl ayrılır?</div>'
        '{{#siklik}}<div class="badge">{{siklik}}</div>{{/siklik}}',
        "{{FrontSide}}<hr id=answer>{{tablo}}",
    ),
    "celdirici": (
        ["vinyet", "yanlis_secenek", "neden_yanlis", "hangi_durumda_dogru"],
        '<div class="vinyet">{{vinyet}}</div>'
        '<div>Yanlış seçeneğin kavramı: {{yanlis_secenek}}</div>',
        '{{FrontSide}}<hr id=answer><div class="cevap-kisa">{{neden_yanlis}}</div>'
        '{{#hangi_durumda_dogru}}<div class="explanation">Doğru olduğu durum: '
        '{{hangi_durumda_dogru}}</div>{{/hangi_durumda_dogru}}',
    ),
    "spot": (
        ["metin", "ekstra"],
        '{{cloze:metin}}{{#siklik}}<div class="badge">{{siklik}}</div>{{/siklik}}',
        '{{cloze:metin}}<hr id=answer>{{#siklik}}<div class="badge">{{siklik}}</div>{{/siklik}}'
        '{{#ekstra}}<div class="explanation"><b>Ekstra</b> — {{ekstra}}</div>{{/ekstra}}'
        '{{#kaynak}}<div class="kaynak">TUS: {{kaynak}}</div>{{/kaynak}}',
    ),
    "gorsel": (
        ["metin", "etiketler"],
        '{{cloze:metin}}{{#siklik}}<div class="badge">{{siklik}}</div>{{/siklik}}',
        '{{cloze:metin}}<hr id=answer>{{#etiketler}}<div class="explanation">{{etiketler}}</div>{{/etiketler}}',
    ),
}

BILGI_PROMPTS = {
    "patognomonik": "patognomonik bulgusu",
    "ilk_tetkik": "ilk tetkiki",
    "kesin_tani": "kesin tanısı",
    "ilk_tedavi": "ilk tedavisi",
    "klasik_komplikasyon": "klasik komplikasyonu",
}

# Sentence-level line breaking for card prose (readability).
_ABBREVS = {"dr", "prof", "doç", "vs", "vb", "bkz", "md", "bk", "çev",
            "ing", "fr", "alm", "lat", "yun"}
_SENT_BOUNDARY = re.compile(r"(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ\"“«(0-9])")


def _split_sentences(text: str) -> list:
    parts, prev = [], 0
    for m in _SENT_BOUNDARY.finditer(text):
        tail = re.search(r"(\S+)$", text[:m.start()])
        word = tail.group(1).lower().rstrip(".") if tail else ""
        if re.fullmatch(r"[a-zçğıöşü]", word) or word in _ABBREVS:
            continue  # genus abbrevs (P. vivax) and common abbrevs
        parts.append(text[prev:m.end()].rstrip())
        prev = m.end()
    parts.append(text[prev:])
    return [p for p in parts if p]


def _prose_html(text) -> str:
    """Sentences joined with <br> for Anki field rendering."""
    if not text:
        return ""
    return "<br>".join(_split_sentences(str(text)))


def _bullets(items) -> str:
    return "<br>• ".join(items)


MAX_CLOZE_CHUNKS = 5
MIN_SENTENCE_CHARS = 45


def _cloze_chunks(value) -> list:
    """Split a long fact value into atomic cloze chunks.

    Sentence boundaries (.!?) AND semicolon clause boundaries split the
    value — round-2 review measured 76% of script values as semicolon-
    chained with <2 periods, so ';' is where most atomization gains live.
    Short chunks merge into the previous one; count capped at MAX_CLOZE_CHUNKS.
    """
    pieces = []
    for part in re.split(r";\s+", str(value)):
        pieces.extend(_split_sentences(part))
    if len(pieces) <= 1:
        return pieces
    merged = []
    for s in pieces:
        if merged and len(merged[-1]) < MIN_SENTENCE_CHARS:
            merged[-1] += " " + s
        else:
            merged.append(s)
    if len(merged) > MAX_CLOZE_CHUNKS:
        head, tail = merged[:MAX_CLOZE_CHUNKS - 1], merged[MAX_CLOZE_CHUNKS - 1:]
        merged = head + [" ".join(tail)]
    return merged


CLOZE_KINDS = {"spot", "gorsel"}
CLOZE_MODEL_TYPE = 1  # Anki model type: 0 = standard, 1 = cloze


def _models():
    out = {}
    for kind, (extra, qfmt, afmt) in MODELS.items():
        names = COMMON_FIELDS + extra
        kwargs = {}
        if kind in CLOZE_KINDS:
            kwargs["model_type"] = CLOZE_MODEL_TYPE
        out[kind] = genanki.Model(
            model_id=MODEL_IDS[kind],
            name=f"TUS {kind.capitalize()}",
            fields=[{"name": n} for n in names],
            templates=[{"name": "Kart", "qfmt": qfmt, "afmt": afmt}],
            css=CSS,
            sort_field_index=len(COMMON_FIELDS),
            **kwargs,
        )
    return out


def _load_taxonomy(path: Path):
    """Return (ads, pos, tree_ids).

    ads:      (test, ders, konu, alt) -> (ders_ad, konu_ad, alt_ad)
    pos:      (test, ders, konu, alt) -> (test_num, ders_num, konu_num, alt_num)
    tree_ids: (test, ders, konu, alt) -> "1010101" (7-digit taxonomy position)
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    ads, pos, tree_ids = {}, {}, {}
    test_num = {"TTBT": 1, "KTBT": 2}
    for test_name, t in data["tests"].items():
        tn = test_num.get(test_name, 0)
        for di, ders in enumerate(t["dersler"], 1):
            for ki, konu in enumerate(ders["konular"], 1):
                for ai, alt in enumerate(konu.get("alt_konular", []), 1):
                    key = (test_name.lower(), ders["id"], konu["id"], alt["id"])
                    ads[key] = (ders["ad"], konu["ad"], alt["ad"])
                    pos[key] = (tn, di, ki, ai)
                    tree_ids[key] = f"{tn}{di:02d}{ki:02d}{ai:02d}"
    return ads, pos, tree_ids


def _slug(text: str) -> str:
    return text.replace(" ", "")


def _sittings(tus_gecmisi):
    return len({tuple(ref.split("-")[1:3]) for ref in tus_gecmisi})


def _siklik_text(n: int) -> str:
    return f"{n} sınavda soruldu" if n else ""


def _siklik_tag(n: int) -> str:
    bucket = "0" if n == 0 else ("1" if n == 1 else ("2-4" if n <= 4 else "5+"))
    return f"{TAG_PREFIX}::Sıklık::{bucket}"


def _nav_tags(script, ads, tree_ids=None, card_seq=0):
    """Generate all tags: full path + parent prefixes + numeric tree ID.

    Returns (tags, primary_tree_id, topic) where topic is the primary
    path's readable (test, ders_ad, konu_ad, alt_ad) or None.
    Only the primary path gets an ID tag — it is unique per card; topic
    navigation lives in the Ders:: hierarchy (all paths tagged there).
    """
    tags = set()
    primary_tree_id = None
    topic = None
    for i, (test, ders, konu, alt) in enumerate(script["taksonomi"]):
        key = (test, ders, konu, alt)
        if key not in ads:
            continue
        d_ad, k_ad, a_ad = ads[key]
        base = [TAG_PREFIX, "Ders", test.upper()]
        # full path
        tags.add(_slug("::".join(base + [d_ad, k_ad, a_ad])))
        # parent prefix tags (all ancestors)
        tags.add(_slug("::".join(base)))
        tags.add(_slug("::".join(base + [d_ad])))
        tags.add(_slug("::".join(base + [d_ad, k_ad])))
        # numeric tree ID: primary path only, unique per card
        if tree_ids and key in tree_ids:
            tid = tree_ids[key]
            if i == 0:
                primary_tree_id = f"{tid}{card_seq:03d}" if card_seq else tid
                tags.add(f"{TAG_PREFIX}::ID::{primary_tree_id}")
                topic = (test.upper(), d_ad, k_ad, a_ad)
    tags.add(_slug("::".join([TAG_PREFIX, "Hastalik", script["ad"]])))
    return sorted(tags), primary_tree_id, topic


def _load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _make_note(models, script, kind, extra_fields, guid_key, ads,
               tree_ids=None, card_seq=0):
    n = _sittings(script.get("tus_gecmisi", []))
    tags, primary_tree_id, topic = _nav_tags(script, ads, tree_ids, card_seq)
    tags = list(tags) + [
        _siklik_tag(n), f"{TAG_PREFIX}::KartTipi::{kind.capitalize()}",
        f"tus_{kind}"]
    # combined id: numeric tree position + readable slug (unique per card)
    note_id = (f"{primary_tree_id}-{script['id']}"
               if primary_tree_id else script["id"])
    ders_ad, konu_ad, alt_ad = ("", "", "")
    if topic:
        ders_ad, konu_ad, alt_ad = topic[1], topic[2], topic[3]
    common = {
        "id": note_id,
        "tree_id": primary_tree_id or "",
        "ders": f"{topic[0]} · {ders_ad}" if topic else "",
        "konu": konu_ad,
        "alt_konu": alt_ad,
        "siklik": _siklik_text(n),
        "kaynak": " ".join(script.get("tus_gecmisi", [])),
        "hastalik": script["ad"],
        "versiyon": str(script["version"]),
        "notlar": "",
    }
    fields = {**common, **extra_fields}
    values = [fields.get(name, "") for name in COMMON_FIELDS + MODELS[kind][0]]
    return genanki.Note(
        model=models[kind],
        fields=values,
        tags=tags,
        guid=genanki.guid_for("tusopen", script["id"], kind, guid_key),
    )


def _make_allocator():
    """Global card-sequence allocator keyed by primary taxonomy path.

    Keeps 10-digit tree_ids unique across scripts that share an alt_konu
    (previously each script restarted its own counter, producing collisions).
    Deterministic: build order is sorted, so output is reproducible.
    """
    used = {}

    def alloc(key) -> int:
        used[key] = used.get(key, 0) + 1
        return used[key]

    return alloc


def _script_notes(script, models, ads, tree_ids, alloc, with_spots=True,
                  with_bilgi=False):
    """Generate cards for one script.

    Deduplicated strategy (plan §7 + competitive analysis):
    - Vaka: 1 card only (vignette → tanı) — tests case recognition
    - Spot: 1 cloze per fact field — primary fact tester (replaces Bilgi)
    - Bilgi: opt-in (redundant with Spot; for facts only by default)
    - Ayırıcı: as authored
    """
    notes = []

    def next_seq():
        return alloc(tuple(script["taksonomi"][0]))

    if with_bilgi and script.get("kart_uret", {}).get("bilgi"):
        for field, prompt in BILGI_PROMPTS.items():
            value = script.get(field)
            if not value:
                continue
            notes.append(_make_note(
                models, script, "bilgi",
                {"soru": f"{script['ad']}: {prompt}?",
                 "cevap": _prose_html(value), "aciklama": ""},
                guid_key=f"bilgi:{field}", ads=ads, tree_ids=tree_ids,
                card_seq=next_seq()))
    if with_spots and script.get("kart_uret", {}).get("spot", True):
        pato_sents = _split_sentences(str(script.get("patofizyoloji") or ""))
        ekstra = _prose_html(" ".join(pato_sents[:2])) if pato_sents else ""
        for field, prompt in BILGI_PROMPTS.items():
            value = script.get(field)
            if not value:
                continue
            chunks = _cloze_chunks(value)
            if len(chunks) == 1:
                metin = f"{script['ad']} — {prompt}: {{{{c1::{_prose_html(value)}}}}}"
            else:
                lines = "<br>".join(
                    f"{{{{c{i}::{_prose_html(ch)}}}}}"
                    for i, ch in enumerate(chunks, 1))
                metin = f"{script['ad']} — {prompt}:<br>{lines}"
            notes.append(_make_note(
                models, script, "spot", {"metin": metin, "ekstra": ekstra},
                guid_key=f"spot:{field}", ads=ads, tree_ids=tree_ids,
                card_seq=next_seq()))
    if script.get("kart_uret", {}).get("vaka"):
        vinyet = (_prose_html(script["tipik_hasta"])
                  + "<br><br><b>Anahtar bulgular</b><br>• "
                  + _bullets(script["anahtar_bulgular"]))
        notes.append(_make_note(
            models, script, "vaka",
            {"vinyet": vinyet, "soru_tipi": "tanı", "cevap": script["ad"],
             "anahtar_bulgular": "• " + _bullets(script["anahtar_bulgular"]),
             "aciklama": _prose_html(script.get("patofizyoloji", ""))},
            guid_key="vaka:tani", ads=ads, tree_ids=tree_ids,
            card_seq=next_seq()))
    for entry in script.get("ayirici", []):
        self_row = "<tr><td>{}</td><td>{}</td></tr>".format(
            script["ad"], _prose_html(
                script.get("patognomonik") or script["ilk_tetkik"]))
        other_row = "<tr><td>{}</td><td>{}</td></tr>".format(
            entry["hastalik"], _prose_html(entry["ayirt_edici"]))
        tablo = ("<table><tr><th>Hastalık</th><th>Ayırt edici özellik</th></tr>"
                 + self_row + other_row + "</table>")
        notes.append(_make_note(
            models, script, "ayirici", {"tablo": tablo},
            guid_key=f"ayirici:{entry['hastalik']}", ads=ads, tree_ids=tree_ids,
            card_seq=next_seq()))
    return notes


def _walkthrough_notes(models, walkthroughs_dir: Path):
    if not walkthroughs_dir.is_dir():
        return []
    notes = []
    for path in sorted(walkthroughs_dir.rglob("*.yaml")):
        data = _load_yaml(path)
        ref = data["soru_ref"]
        for entry in data.get("celdirici_kavramlar", []):
            extra = {
                "vinyet": f"Gerçek TUS sorusu: {ref}",
                "yanlis_secenek": entry["kavram"],
                "neden_yanlis": entry["neden_yanlis"],
                "hangi_durumda_dogru": entry["dogru_oldugu_durum"],
            }
            common = {name: "" for name in COMMON_FIELDS}
            common.update({
                "id": data.get("id") or ref,
                "kaynak": ref,
                "hastalik": data.get("hastalik", ""),
                "versiyon": str(data.get("version", 1)),
            })
            values = [common.get(n, "") for n in COMMON_FIELDS] + [
                extra.get(f, "") for f in MODELS["celdirici"][0]]
            notes.append(genanki.Note(
                model=models["celdirici"],
                fields=values,
                tags=[f"{TAG_PREFIX}::Soru::{ref}",
                      f"{TAG_PREFIX}::KartTipi::Çeldirici", "tus_celdirici"],
                guid=genanki.guid_for("tusopen", ref, "celdirici", entry["kavram"]),
            ))
    return notes


def _split_answer_explanation(text: str):
    """First sentence = the short answer; the rest = the explanation layer."""
    m = re.search(r"(?<=\.)\s+(?=[A-ZÇĞİÖŞÜ0-9\"““(])", text)
    if m:
        first, rest = text[:m.start()].strip(), text[m.start():].strip()
        if len(first) >= 25 and len(rest) >= 30:
            return first, rest
    return text.strip(), ""


def _gorsel_html(fact: dict) -> str | None:
    """Build the image-occlusion HTML from a fact's `gorsel` object."""
    g = fact.get("gorsel")
    if not g or not g.get("dosya"):
        return None
    masks = []
    for i, e in enumerate(g.get("etiketler", []), 1):
        masks.append(
            f'<div class="io-mask" style="left:{e["x"]}%;top:{e["y"]}%;'
            f'width:{e["w"]}%;height:{e["h"]}%;">'
            f'{{{{c{i}::{e["ad"]}}}}}</div>')
    img = f'<img src="{g["dosya"]}" class="io-img">'
    body = img + "".join(masks)
    credit = " · ".join(str(g.get(k, "")) for k in ("yazar", "lisans", "kaynak")
                        if g.get(k)).strip(" ·")
    if credit:
        body += f'<div class="aciklama">{credit}</div>'
    return f'<div class="io-container">{body}</div>'


def _fact_notes(models, facts_dir: Path, ads, tree_ids, alloc):
    if not facts_dir.is_dir():
        return []
    notes = []
    for path in sorted(facts_dir.rglob("*.yaml")):
        fact = _load_yaml(path)
        if fact.get("status") == "deprecated":
            continue

        def next_seq():
            return alloc(tuple(fact["taksonomi"][0]))

        cevap, aciklama = _split_answer_explanation(fact["metin"])
        notes.append(_make_note(
            models, fact, "bilgi",
            {"soru": fact["ad"], "cevap": _prose_html(cevap),
             "aciklama": _prose_html(aciklama)},
            guid_key="fact", ads=ads, tree_ids=tree_ids, card_seq=next_seq()))
        gorsel_html = _gorsel_html(fact)
        if gorsel_html:
            g = fact["gorsel"]
            etiketler = "; ".join(e["ad"] for e in g.get("etiketler", []))
            notes.append(_make_note(
                models, fact, "gorsel",
                {"metin": gorsel_html, "etiketler": etiketler},
                guid_key="gorsel", ads=ads, tree_ids=tree_ids,
                card_seq=next_seq()))
    return notes


def _collect_media(content_root: Path, models_used: set) -> list:
    """Find all media files referenced in gorsel fields across facts."""
    media = []
    facts_dir = content_root / "facts"
    if not facts_dir.is_dir():
        return media
    for path in sorted(facts_dir.rglob("*.yaml")):
        fact = _load_yaml(path)
        g = fact.get("gorsel")
        if g and g.get("dosya"):
            fp = facts_dir / "media" / g["dosya"]
            if fp.is_file():
                media.append(str(fp))
            else:
                print(f"WARNING: gorsel media not found: {fp}")
    return media


DECK_DESCRIPTION = (
    f"TUS Open — açık kaynak TUS çalışma destesi (sürüm {DECK_VERSION}). "
    "© 2026 Batuhan Ayci ve katkıcılar. İçerik CC BY-SA 4.0, kod Apache-2.0 "
    "(github'daki depoya bakın). "
    "Tıbbi bilgi tazelik ve doğruluk garantisi yoktur; tek başına çalışma "
    "kaynağı değildir; ÖSYM ile hiçbir bağı yoktur. "
    "Görseller Wikimedia Commons'tan serbest lisanslıdır; görsel ayrıntıları "
    "deponun content/facts/media/LICENSE-MANIFEST.md dosyasındadır.")


def run(content_root: Path, out_path: Path, taxonomy_path: Path,
        with_spots: bool = True, with_bilgi: bool = False) -> int:
    ads, pos, tree_ids = _load_taxonomy(taxonomy_path)
    models = _models()
    deck = genanki.Deck(deck_id=DECK_ID, name=DECK_NAME,
                        description=DECK_DESCRIPTION)
    alloc = _make_allocator()
    count = 0
    spoilers = []
    scripts_dir = content_root / "scripts"
    if scripts_dir.is_dir():
        for path in sorted(scripts_dir.rglob("*.yaml")):
            script = _load_yaml(path)
            if script.get("status") == "deprecated":
                continue
            if script.get("kart_uret", {}).get("vaka"):
                th = (script.get("tipik_hasta") or "").lower()
                ad = (script.get("ad") or "").lower()
                if ad and len(ad) > 5 and ad in th:
                    spoilers.append(script["id"])
            for note in _script_notes(script, models, ads, tree_ids, alloc,
                                      with_spots=with_spots,
                                      with_bilgi=with_bilgi):
                deck.add_note(note)
                count += 1
    for note in _walkthrough_notes(models, content_root / "walkthroughs"):
        deck.add_note(note)
        count += 1
    for note in _fact_notes(models, content_root / "facts", ads, tree_ids, alloc):
        deck.add_note(note)
        count += 1
    seen = {}
    for note in deck.notes:
        tid = note.fields[1]
        if tid:
            if tid in seen:
                print(f"WARNING: duplicate tree_id {tid} "
                      f"({seen[tid]} vs {note.fields[0]})")
            seen[tid] = note.fields[0]
    if spoilers:
        print(f"WARNING: {len(spoilers)} vaka vinyeti hastalık adını geçiyor "
              f"(tanıyı ele verir — gözden geçirin): "
              f"{', '.join(sorted(spoilers)[:10])}"
              + (" ..." if len(spoilers) > 10 else ""))
    media_files = _collect_media(content_root, set())
    out_path.parent.mkdir(parents=True, exist_ok=True)
    genanki.Package(deck, media_files=media_files).write_to_file(out_path)
    return count
