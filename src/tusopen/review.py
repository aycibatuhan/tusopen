"""Human review workflow (plan §8.3): CSV worksheet dump / apply.

`tusopen review --dump [DERS]` writes a worksheet listing every content item
(scripts, facts, cases) with empty reviewer columns. Reviewers fill
`status` (reviewed|published) and `reviewer` (their name), then
`tusopen review --apply sheet.csv` merges those back into the YAML files.
Merges are idempotent: already-set reviewers are kept, never duplicated.
"""
import csv
import sys
from datetime import date
from pathlib import Path

import yaml

WORKSHEET_COLUMNS = ["id", "tip", "dosya", "ders", "ad", "status",
                     "reviewer", "notlar"]


def _load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _ders_of(data) -> str:
    tax = data.get("taksonomi") or []
    if tax and len(tax[0]) >= 2:
        return str(tax[0][1])
    return ""


def _collect(content_root: Path) -> list:
    rows = []
    roots = [("scripts", content_root / "scripts"),
             ("facts", content_root / "facts"),
             ("cases", content_root / "cases")]
    for tip, root in roots:
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.yaml")):
            data = _load(path)
            if data.get("status") == "deprecated":
                continue
            ders = _ders_of(data)
            if tip == "cases" and not ders and data.get("hastalik"):
                link = content_root / "scripts"
                for sp in link.rglob("*.yaml"):
                    sd = _load(sp)
                    if sd.get("id") == data.get("hastalik"):
                        ders = _ders_of(sd)
                        break
            rows.append({
                "id": data.get("id") or path.stem,
                "tip": tip,
                "dosya": str(path.relative_to(content_root)),
                "ders": ders,
                "ad": data.get("ad") or data.get("baslik") or "",
                "status": data.get("status", "draft"),
                "reviewer": "",
                "notlar": "",
            })
    return rows


def dump(content_root: Path, ders: str | None, out_path: Path) -> Path:
    rows = _collect(content_root)
    if ders:
        wanted = ders.lower().replace(" ", "_")
        rows = [r for r in rows
                if wanted in r["ders"].lower() or wanted == r["tip"]]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=WORKSHEET_COLUMNS)
        w.writeheader()
        w.writerows(rows)
    return out_path


VALID_STATUSES = ("draft", "reviewed", "published", "deprecated")


def apply_sheet(content_root: Path, sheet: Path) -> int:
    today = date.today().isoformat()
    updated, skipped = 0, 0
    with sheet.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            reviewer = (row.get("reviewer") or "").strip()
            new_status = (row.get("status") or "").strip()
            rel = (row.get("dosya") or "").strip()
            if not rel or (not reviewer and not new_status):
                continue
            if new_status and new_status not in VALID_STATUSES:
                print(f"SKIP (geçersiz status {new_status!r}): {rel}",
                      file=sys.stderr)
                skipped += 1
                continue
            if new_status in ("reviewed", "published") and not reviewer:
                print(f"SKIP (reviewer zorunlu: {new_status}): {rel}",
                      file=sys.stderr)
                skipped += 1
                continue
            path = (content_root / rel).resolve()
            if (not path.suffix == ".yaml"
                    or not path.is_relative_to(content_root.resolve())
                    or not path.is_file()):
                print(f"SKIP (content dışındaki/olmayan dosya): {rel}",
                      file=sys.stderr)
                skipped += 1
                continue
            data = _load(path)
            changed = False
            if reviewer:
                people = [p.strip() for p in reviewer.split(";") if p.strip()]
                existing = data.get("reviewed_by") or []
                merged = list(existing) + [p for p in people if p not in existing]
                if merged != existing:
                    data["reviewed_by"] = merged
                    changed = True
            if new_status and new_status != data.get("status"):
                data["status"] = new_status
                changed = True
            if changed:
                if reviewer:
                    data["last_reviewed"] = today
                path.write_text(
                    yaml.safe_dump(data, allow_unicode=True, sort_keys=False,
                                   width=100),
                    encoding="utf-8")
                updated += 1
    print(f"review apply: {updated} dosya güncellendi, {skipped} atlandı")
    return 0 if not skipped else 1
