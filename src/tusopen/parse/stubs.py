"""Write committable question-metadata stubs (plan §5.1, §6.2).

Each parsed exam produces ``content/questions/<year>/<donem>/<test>.yaml``
with ids, answer keys and tags only — never question text. Machine fields
(``id``, ``cevap``, ``iptal``) are refreshed on re-run; human fields
(``ders``, ``konu``, ``hastalik``, ...) are preserved so contributors can
tag stubs without losing work. Cancelled questions are kept with
``iptal: true`` (plan §2).
"""
import json
from pathlib import Path

import yaml

HUMAN_FIELDS = ("ders", "konu", "alt_konu", "hastalik", "soru_tipi",
                "alt_tip", "zorluk", "benzer", "notlar")
LEGACY_DONEM = {1: "ilkbahar", 2: "sonbahar"}


def load_exam(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_sorular(res: dict, existing: dict) -> list:
    yil = res["year"]
    donem = res["donem"]
    test = res["test"].lower()
    cancelled = set(res.get("cancelled", []))
    qmap = {q["number"]: q for q in res["questions"]}
    if res["is_sample"]:
        nums = sorted(qmap)
    else:
        nums = list(range(1, max(set(qmap) | cancelled, default=0) + 1))
    sorular = []
    for n in nums:
        q = qmap.get(n)
        old = existing.get(n, {})
        entry = {
            "no": n,
            "id": f"tus-{yil}-{donem}-{test}-{n}",
            "cevap": q["answer"] if q else None,
            "iptal": n in cancelled,
        }
        for f in HUMAN_FIELDS:
            entry[f] = old.get(f, [] if f == "hastalik" or f == "benzer" else
                               ("" if f == "notlar" else None))
        if entry["iptal"] and not old.get("notlar"):
            entry["notlar"] = "İptal (ÖSYM)"
        sorular.append(entry)
    return sorular


def stub_path(res: dict, content_root: Path) -> Path:
    return (content_root / "questions" / str(res["year"]) / res["donem"]
            / f"{res['test'].lower()}.yaml")


def write_stub(res: dict, content_root: Path) -> Path:
    out = stub_path(res, content_root)
    out.parent.mkdir(parents=True, exist_ok=True)
    existing = {}
    if out.exists():
        old = yaml.safe_load(out.read_text(encoding="utf-8")) or {}
        existing = {s["no"]: s for s in old.get("sorular", [])
                    if isinstance(s, dict) and "no" in s}
    doc = {
        "version": 1,
        "status": "draft",
        "kapsam": "sample10" if res["is_sample"] else "full",
        "sources": [res["source_url"]] if res.get("source_url") else [],
        "sinav": {"yil": res["year"], "donem": res["donem"], "test": res["test"]},
        "sorular": build_sorular(res, existing),
    }
    out.write_text(
        yaml.dump(doc, allow_unicode=True, sort_keys=False, width=100),
        encoding="utf-8",
    )
    return out


def run(cache: Path, content_root: Path, targets=None):
    parsed = cache / "parsed"
    if not parsed.is_dir():
        raise SystemExit(f"no parsed cache at {parsed}; run `tusopen parse` first")
    jsons = sorted(parsed.glob("*.json"))
    if targets:
        wanted = set(targets)
        jsons = [p for p in jsons if p.stem in wanted]
    for jp in jsons:
        res = load_exam(jp)
        out = write_stub(res, content_root)
        n_iptal = len(res.get("cancelled", []))
        print(f"{jp.stem:24} {len(res['questions']):3} soru"
              + (f" (+{n_iptal} iptal)" if n_iptal else "") + f" -> {out.relative_to(content_root)}")
