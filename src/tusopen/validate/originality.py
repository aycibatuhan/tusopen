"""Own-words originality check (plan §8.2).

Compares every free-text field in ``content/`` against the locally cached
ÖSYM booklet text (``<cache>/parsed``). Three layers, in increasing
sophistication:

1. shared 6-word window (verbatim copy detection)
2. 5-word shingle containment ≥ 0.30 (paraphrase-resistant: survives
   scattered word substitutions that defeat layers 1 and 3)
3. fuzzy ratio ≥ 0.6 vs *individual* stems/options (not the concatenated
   question, whose length used to dilute short copies below threshold)

Advisory in CI; mandatory in the maintainer's release run. A missing
booklet cache is reported as SKIPPED and run() returns [] — callers must
check the skip condition themselves instead of treating [] as a pass.
"""
import json
import re
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

import yaml

NGRAM = 6
SHINGLE = 5
SHINGLE_CONTAINMENT = 0.40
MIN_FIELD_SHINGLES = 12
FUZZY_RATIO = 0.6
MIN_FUZZY_TOKENS = 12
MAX_FUZZY_CANDIDATES = 40
MAX_HITS_SHOWN = 3
MIN_REF_TOKENS = 4

# Turkish dotted-İ: "İ".lower() yields "i" + combining dot U+0307, which
# \w+ then splits into two tokens and breaks every index. Map the Turkish
# capitals first so normalization is lossless for both sides.
_TR_MAP = str.maketrans({"İ": "i", "I": "ı"})

# Identifier/reference keys — their values are ids, not prose (plan §5).
EXCLUDED_KEYS = {
    "id", "version", "status", "kapsam", "author", "reviewed_by",
    "last_reviewed", "sources", "taksonomi", "soru_ref", "sinav", "benzer",
    "tus_gecmisi", "kart_uret", "cevap", "iptal", "no", "siklik",
    "hastalik", "ders", "konu", "alt_konu", "soru_tipi", "alt_tip", "zorluk",
}

TOKEN_RE = re.compile(r"\w+", re.UNICODE)


def _norm(text: str) -> str:
    text = unicodedata.normalize("NFC", text).translate(_TR_MAP).lower()
    return " ".join(t for t in TOKEN_RE.findall(text) if t)


def _labish(window) -> bool:
    """True for lab-value windows (e.g. 'na 119 meq l k 4').

    Vignettes inevitably share lab panels; those are not prose copying.
    A window with 2+ numeric or single-character tokens is treated as data.
    """
    special = sum(1 for t in window if t.isdigit() or len(t) == 1)
    return special >= 2


def _walk_strings(node, key=None):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from _walk_strings(v, k)
    elif isinstance(node, list):
        for v in node:
            yield from _walk_strings(v, key)
    elif isinstance(node, str):
        if key not in EXCLUDED_KEYS:
            yield key, node


def content_fields(content_root: Path):
    for p in sorted(content_root.rglob("*.yaml")):
        rel = p.relative_to(content_root)
        try:
            d = yaml.safe_load(p.read_text(encoding="utf-8"))
        except Exception:
            print(f"originality: unparseable YAML skipped: {rel}")
            continue
        for key, s in _walk_strings(d):
            yield rel, key, s


def load_reference(cache: Path):
    """Per-text reference: individual stems and options, two inverted indexes.

    Returns (texts, ngram_index, shingle_index):
      texts         label -> normalized text (one stem or one option)
      ngram_index   NGRAM-token tuple -> [labels]
      shingle_index SHINGLE-token tuple -> [labels]
    """
    texts = {}
    for jp in sorted((cache / "parsed").glob("*.json")):
        d = json.loads(jp.read_text(encoding="utf-8"))
        for q in d["questions"]:
            label = f'{d["exam_id"]}_{d["test"]}:q{q["number"]}'
            parts = [("stem", q["stem"])]
            parts += sorted(q["options"].items())
            for kind, txt in parts:
                if not txt:
                    continue
                norm = _norm(txt)
                if len(norm.split()) >= MIN_REF_TOKENS:
                    texts[f"{label}:{kind}"] = norm
    ngram_index, shingle_index = {}, {}
    for label, norm in texts.items():
        toks = norm.split()
        for i in range(len(toks) - NGRAM + 1):
            ngram_index.setdefault(tuple(toks[i:i + NGRAM]), []).append(label)
        for i in range(len(toks) - SHINGLE + 1):
            shingle_index.setdefault(
                tuple(toks[i:i + SHINGLE]), []).append(label)
    return texts, ngram_index, shingle_index


def run(content_root: Path, cache: Path) -> list:
    if not (cache / "parsed").is_dir():
        print(f"originality: SKIPPED — no parsed cache at {cache / 'parsed'} "
              "(local booklet text gerekli; CI'da advisory'dir)")
        return []
    texts, ngram_index, shingle_index = load_reference(cache)
    # document frequency for rare-token fuzzy candidate selection
    df = Counter()
    for label, norm in texts.items():
        df.update(set(norm.split()))
    token_index = {}
    for label, norm in texts.items():
        for t in set(norm.split()):
            token_index.setdefault(t, []).append(label)

    findings = []
    for rel, key, text in content_fields(content_root):
        norm = _norm(text)
        toks = norm.split()
        if len(toks) < NGRAM:
            continue

        # 1. verbatim N-gram window (lab-value windows excluded)
        matched = set()
        for i in range(len(toks) - NGRAM + 1):
            window = tuple(toks[i:i + NGRAM])
            if _labish(window):
                continue
            matched.update(ngram_index.get(window, ()))
        for label in sorted(matched)[:MAX_HITS_SHOWN]:
            findings.append(f"{rel}:{key} — shared {NGRAM}-word window with {label}")

        # 2. shingle containment (paraphrase-resistant; substantial fields only)
        field_shingles = {tuple(toks[i:i + SHINGLE])
                          for i in range(len(toks) - SHINGLE + 1)}
        if len(field_shingles) >= MIN_FIELD_SHINGLES:
            hit_shingles = Counter()
            for sh in field_shingles:
                for label in shingle_index.get(sh, ()):
                    hit_shingles[label] += 1
            for label, n in hit_shingles.most_common(MAX_HITS_SHOWN):
                containment = n / len(field_shingles)
                if containment >= SHINGLE_CONTAINMENT:
                    findings.append(
                        f"{rel}:{key} — shingle containment {containment:.2f} "
                        f"vs {label} (close paraphrase — rewrite in own words)")

        # 3. fuzzy vs individual stems/options (prose-length fields only —
        # short nomenclature like 'hipokalemik hipokloremik metabolik
        # alkaloz' is standard terminology, not copying)
        if len(toks) < MIN_FUZZY_TOKENS:
            continue
        rare = sorted((t for t in set(toks) if df.get(t, 0) < 200),
                      key=lambda t: df.get(t, 0))[:8]
        cand = Counter()
        for t in rare:
            cand.update(token_index.get(t, ()))
        comparisons = 0
        for label, _shared in cand.most_common(MAX_FUZZY_CANDIDATES * 4):
            if comparisons >= MAX_FUZZY_CANDIDATES:
                break
            if len(texts[label].split()) < MIN_FUZZY_TOKENS:
                continue
            sm = SequenceMatcher(None, norm, texts[label])
            if sm.quick_ratio() < FUZZY_RATIO:
                continue
            comparisons += 1
            if sm.ratio() >= FUZZY_RATIO:
                findings.append(
                    f"{rel}:{key} — fuzzy {sm.ratio():.2f} vs {label} (rewrite in own words)")
    return findings
