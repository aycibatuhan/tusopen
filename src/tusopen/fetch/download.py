"""Fetch official ÖSYM TUS PDFs into the local cache (plan §6.1).

Coverage per ``sources.yaml``: full booklet + key for ~2006-2021;
2022+ yields the 10% sample + answer key only — the CLI reports this
instead of silently producing a partial dataset. Cache is never committed.
"""
import hashlib
import shutil
import subprocess
from pathlib import Path

import yaml

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
SOURCES = Path(__file__).with_name("sources.yaml")


def load_sources() -> list:
    return yaml.safe_load(SOURCES.read_text(encoding="utf-8"))["sittings"]


def rewrite_manifest(cache: Path) -> Path:
    raw = cache / "raw"
    rows = ["file,bytes,sha256"]
    for f in sorted(raw.glob("*.pdf")):
        data = f.read_bytes()
        rows.append(f"{f.name},{len(data)},{hashlib.sha256(data).hexdigest()}")
    man = cache / "manifest.csv"
    man.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return man


def _is_pdf(p: Path) -> bool:
    return p.is_file() and p.read_bytes()[:4] == b"%PDF"


def run(cache: Path, args) -> int:
    raw = cache / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    sel = [s for s in load_sources()
           if (args.year is None or s["year"] == args.year)
           and (args.donem is None or s["donem"] == args.donem)
           and (args.test is None or s["test"] == args.test)]
    if not sel:
        print("no matching sittings in sources.yaml")
        return 1
    failed = []
    for s in sel:
        dest = raw / f"{s['year']}-{s['donem']}_{s['test']}.pdf"
        if _is_pdf(dest):
            print(f"SKIP {dest.name} (exists)")
            continue
        print(f"GET  {dest.name} [{s['coverage']}]")
        r = subprocess.run(
            ["curl", "-fsSL", "--retry", "3", "--retry-delay", "2",
             "--max-time", "120", "-A", UA, "-o", str(dest), s["url"]])
        if r.returncode != 0 or not _is_pdf(dest):
            dest.unlink(missing_ok=True)
            print(f"FAIL {s['url']}")
            failed.append(dest.name)
    sample_used = any(s["coverage"] == "sample10" for s in sel)
    man = rewrite_manifest(cache)
    print(f"manifest written: {man}")
    if sample_used:
        print("note: 2022+ public booklets are 10% samples + answer key only; "
              "full AİS copies can be added with `tusopen import`")
    return 1 if failed else 0


def import_booklet(cache: Path, year: int, donem: str, test: str, file: Path) -> Path:
    if donem not in ("ilkbahar", "sonbahar"):
        raise SystemExit(f"unknown donem: {donem}")
    if not _is_pdf(file):
        raise SystemExit(f"not a PDF: {file}")
    raw = cache / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    dest = raw / f"{year}-{donem}_{test.upper()}.pdf"
    if dest.exists():
        print(f"overwriting existing {dest.name}")
    shutil.copyfile(file, dest)
    rewrite_manifest(cache)
    return dest
