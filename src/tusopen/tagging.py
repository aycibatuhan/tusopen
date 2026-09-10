"""Agent-assisted question tagging (plan §6.2-§6.4).

`tusopen tag --dump <exam>` writes a local worksheet — question text lives
only in the cache and is never committed. Drafters fill taxonomy ids per
question; `tusopen tag --apply <exam>` merges the result into the
content/questions stubs. Human precedence: fields already set by a human
are kept unless --force. Tagged stubs stay `status: draft` — tags are
metadata drafts like every other AI-assisted item and need human review.
"""
import json
from pathlib import Path

import yaml

from tusopen.validate.content import _normalize, _taxonomy_resolve

TAG_FIELDS = ("ders", "konu", "alt_konu", "soru_tipi", "alt_tip", "hastalik", "zorluk")


def _stub_path(content_root: Path, res: dict) -> Path:
    return (content_root / "questions" / str(res["year"]) / res["donem"]
            / f"{res['test'].lower()}.yaml")


def dump(cache: Path, exam: str) -> Path:
    jp = cache / "parsed" / f"{exam}.json"
    if not jp.is_file():
        raise SystemExit(f"no parsed exam in cache: {jp}")
    res = json.loads(jp.read_text(encoding="utf-8"))
    ws = {
        "exam": exam,
        "test": res["test"],
        "questions": [
            {"no": q["number"], "stem": q["stem"], "options": q["options"],
             "answer": q["answer"]}
            for q in res["questions"]
        ],
    }
    out = cache / "tagging" / f"{exam}.worksheet.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(ws, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


def _set(entry: dict, field: str, value, errors: list, rel: str, no: int, force: bool):
    current = entry.get(field)
    empty = current is None or current == "" or current == []
    if not empty and not force and current == value:
        return
    if not empty and not force:
        errors.append(f"{rel}: soru {no}: field {field} already set ({current!r}); "
                      "kept human value, agent value ignored")
        return
    entry[field] = value


def backfill_scripts(content_root: Path) -> int:
    """Collect hastalik links from all question stubs into script tus_gecmisi (§5.2)."""
    links: dict = {}
    for p in sorted((content_root / "questions").rglob("*.yaml")):
        doc = _normalize(yaml.safe_load(p.read_text(encoding="utf-8")))
        for s in doc.get("sorular", []):
            for h in s.get("hastalik") or []:
                links.setdefault(h, set()).add(s["id"])
    changed = 0
    for p in sorted((content_root / "scripts").rglob("*.yaml")):
        d = _normalize(yaml.safe_load(p.read_text(encoding="utf-8")))
        gid = d.get("id")
        if gid not in links:
            continue
        before = list(d.get("tus_gecmisi") or [])
        after = sorted(set(before) | links[gid])
        if after != before:
            d["tus_gecmisi"] = after
            p.write_text(
                yaml.dump(d, allow_unicode=True, sort_keys=False, width=100),
                encoding="utf-8")
            changed += 1
            print(f"{gid}: tus_gecmisi -> {len(after)} question refs")
    return changed


def apply(cache: Path, content_root: Path, taxonomy_path: Path, exam: str,
          tags_file: Path | None = None, force: bool = False) -> int:
    jp = cache / "parsed" / f"{exam}.json"
    if not jp.is_file():
        raise SystemExit(f"no parsed exam in cache: {jp}")
    res = json.loads(jp.read_text(encoding="utf-8"))
    tax = json.loads(taxonomy_path.read_text(encoding="utf-8"))

    tags_path = tags_file or (cache / "tagging" / f"{exam}.tags.json")
    if not tags_path.is_file():
        raise SystemExit(f"no tags file: {tags_path}")
    tags = json.loads(tags_path.read_text(encoding="utf-8")).get("tags", {})

    stub_path = _stub_path(content_root, res)
    stub = _normalize(yaml.safe_load(stub_path.read_text(encoding="utf-8")))
    by_no = {s["no"]: s for s in stub["sorular"]}

    applied, kept, errors = 0, 0, []
    test_lower = res["test"].lower()
    for no_str, tag in tags.items():
        no = int(no_str)
        entry = by_no.get(no)
        if entry is None:
            errors.append(f"soru {no}: not in stub ({stub_path.name})")
            continue
        ders = tag.get("ders")
        konu = tag.get("konu")
        alt = tag.get("alt_konu")
        if ders and not _taxonomy_resolve(tax, test_lower, ders, konu, alt):
            errors.append(f"soru {no}: taxonomy path does not resolve: "
                          f"[{test_lower}, {ders}, {konu}, {alt}] — ders/konu/alt skipped")
        else:
            for f in ("ders", "konu", "alt_konu"):
                if tag.get(f) is not None:
                    before = entry.get(f)
                    _set(entry, f, tag[f], errors, tags_path.name, no, force)
                    if entry.get(f) != before:
                        applied += 1
                    else:
                        kept += 1
        for f in ("soru_tipi", "alt_tip", "zorluk", "hastalik"):
            if f in tag and tag[f] is not None:
                before = entry.get(f)
                _set(entry, f, tag[f], errors, tags_path.name, no, force)
                if entry.get(f) != before:
                    applied += 1
                else:
                    kept += 1

    stub_path.write_text(
        yaml.dump(stub, allow_unicode=True, sort_keys=False, width=100),
        encoding="utf-8")
    print(f"{exam}: applied={applied} kept/unchanged={kept} errors={len(errors)}")
    for e in errors[:20]:
        print(f"  - {e}")
    if len(errors) > 20:
        print(f"  ... and {len(errors) - 20} more")
    return 1 if errors else 0
