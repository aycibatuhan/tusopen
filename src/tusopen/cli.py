"""TUS Open CLI (plan §6).

  tusopen fetch [--year Y] [--donem ilkbahar|sonbahar] [--test TTBT|KTBT]
  tusopen import --year Y --donem D --test T --file booklet.pdf
  tusopen parse [--all | --files id_TEST ...] [--no-stubs]
  tusopen stubs [--all | --files id_TEST ...]
  tusopen validate [--originality]

The cache (raw PDFs + parsed question text) defaults to ~/.tusopen/cache
and is never committed. Only content/ metadata stubs and code are public.
"""
import argparse
import sys
from pathlib import Path

from tusopen.fetch import download as fetch_mod
from tusopen.parse import extract as parse_mod
from tusopen.parse import stubs as stubs_mod
from tusopen.paths import default_cache, repo_root
from tusopen.validate import content as content_mod
from tusopen.validate import originality as originality_mod
from tusopen.validate import report as report_mod

DONEMLER = ("ilkbahar", "sonbahar")
TESTLER = ("TTBT", "KTBT")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="tusopen", description="TUS Open local content pipeline")
    ap.add_argument("--cache-dir", type=Path, default=default_cache(),
                    help="local cache root (default: ~/.tusopen/cache)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("fetch", help="download official ÖSYM PDFs into the cache")
    f.add_argument("--year", type=int)
    f.add_argument("--donem", choices=DONEMLER)
    f.add_argument("--test", choices=TESTLER)

    i = sub.add_parser("import", help="add a candidate-held AİS booklet copy")
    i.add_argument("--year", type=int, required=True)
    i.add_argument("--donem", choices=DONEMLER, required=True)
    i.add_argument("--test", choices=TESTLER, required=True)
    i.add_argument("--file", type=Path, required=True)

    p = sub.add_parser("parse", help="parse cached PDFs into structured JSON + stubs")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true")
    g.add_argument("--files", nargs="+")
    p.add_argument("--no-stubs", action="store_true",
                   help="skip writing content/ metadata stubs")

    s = sub.add_parser("stubs", help="(re)generate content/ stubs from parsed JSON")
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true")
    g.add_argument("--files", nargs="+")

    v = sub.add_parser("validate",
                       help="schemas + cross-refs + parse report (+ own-words check)")
    v.add_argument("--originality", action="store_true",
                   help="check content/ for ÖSYM text overlap (plan §8.2)")

    t = sub.add_parser("tag",
                       help="agent-assisted question tagging (dump worksheet / apply tags)")
    t.add_argument("--dump", metavar="EXAM",
                   help="write local worksheet for an exam (e.g. 2021-ilkbahar_TTBT)")
    t.add_argument("--apply", metavar="EXAM",
                   help="merge a tags JSON into content/questions stubs")
    t.add_argument("--tags", type=Path,
                   help="tags JSON path (default: cache/tagging/<exam>.tags.json)")
    t.add_argument("--force", action="store_true",
                   help="overwrite fields a human already set")
    t.add_argument("--backfill-scripts", action="store_true",
                   help="copy hastalik links from stubs into script tus_gecmisi")
    _build_export_parser(sub)
    r = sub.add_parser("review",
                       help="human review workflow: dump CSV worksheet / apply back")
    r.add_argument("--dump", metavar="DERS", nargs="?", const="all",
                   help="write review worksheet (optionally filter by ders id)")
    r.add_argument("--apply", type=Path, metavar="SHEET",
                   help="merge a filled worksheet CSV back into content/")
    r.add_argument("--out", type=Path,
                   default=Path("local") / "review" / "worksheet.csv",
                   help="worksheet output path (default: local/review/worksheet.csv)")
    return ap


def _build_export_parser(sub):
    e = sub.add_parser("export", help="generate study outputs from content/")
    e2 = e.add_subparsers(dest="what", required=True)
    a = e2.add_parser("anki", help="build the Anki deck (.apkg) (plan §6.5)")
    a.add_argument("--out", type=Path,
                   default=Path("site") / "anki" / "tusopen.apkg")
    a.add_argument("--no-spots", action="store_true",
                   help="skip auto-generated cloze spot cards from scripts")
    a.add_argument("--with-bilgi", action="store_true",
                   help="also generate Bilgi cards from scripts (default: off, "
                        "Spot replaces them to avoid duplication)")
    s = e2.add_parser("simulator", help="build the static case simulator (plan §6.6)")
    s.add_argument("--out", type=Path, default=Path("site") / "simulator",
                   metavar="DIR", help="output directory (default: site/simulator)")
    return e


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    cache: Path = args.cache_dir
    content_root = repo_root() / "content"

    if args.cmd == "fetch":
        return fetch_mod.run(cache, args)

    if args.cmd == "import":
        if not args.file.is_file():
            print(f"file not found: {args.file}")
            return 1
        dest = fetch_mod.import_booklet(cache, args.year, args.donem, args.test, args.file)
        print(f"imported: {dest}")
        return 0

    if args.cmd == "parse":
        if args.all:
            targets = sorted(x.stem for x in (cache / "raw").glob("*.pdf"))
        else:
            targets = args.files
        return parse_mod.run(cache, targets,
                             with_stubs=not args.no_stubs, content_root=content_root)

    if args.cmd == "stubs":
        targets = args.files if not args.all else None
        stubs_mod.run(cache, content_root, targets)
        return 0

    if args.cmd == "validate":
        if (cache / "parsed").is_dir():
            report_mod.run(cache)
        else:
            print(f"parse report skipped (no parsed cache at {cache})")
        errors = content_mod.run(content_root, repo_root() / "taxonomy" / "taxonomy.json")
        if errors:
            print(f"\ncontent validation: FAIL ({len(errors)})")
            for x in errors[:40]:
                print(f"  - {x}")
            if len(errors) > 40:
                print(f"  ... and {len(errors) - 40} more")
            return 1
        print("content validation: OK (schema + cross-refs)")
        if not args.originality:
            return 0
        if not (cache / "parsed").is_dir():
            print("originality: SKIPPED — no parsed cache at "
                  f"{cache / 'parsed'} (CI'da advisory; yerel makinede koşun)")
            return 0
        findings = originality_mod.run(content_root, cache)
        if findings:
            print("\noriginality: FAIL — rewrite the following in own words (plan §8):")
            for x in findings:
                print(f"  - {x}")
            return 1
        print("originality: OK — no ÖSYM text overlap found in content/")
        return 0

    if args.cmd == "tag":
        from tusopen import tagging

        if args.backfill_scripts:
            n = tagging.backfill_scripts(content_root)
            print(f"scripts updated: {n}")
            return 0
        if args.dump and args.apply:
            print("--dump and --apply are exclusive")
            return 2
        if args.dump:
            out = tagging.dump(cache, args.dump)
            print(f"worksheet: {out}")
            return 0
        if args.apply:
            return tagging.apply(cache, content_root,
                                 repo_root() / "taxonomy" / "taxonomy.json",
                                 args.apply, args.tags, args.force)
        print("tag needs --dump <exam> or --apply <exam>")
        return 2

    if args.cmd == "review":
        from tusopen import review as review_mod

        if args.apply:
            return review_mod.apply_sheet(content_root, args.apply)
        if args.dump:
            out = review_mod.dump(
                content_root, None if args.dump == "all" else args.dump,
                args.out)
            print(f"review worksheet ({out}):"
                  f" fill 'reviewer' + 'status', then: tusopen review --apply {out}")
            return 0
        print("review needs --dump [DERS] or --apply SHEET")
        return 2

    if args.cmd == "export" and args.what == "anki":
        from tusopen.export.anki import build as anki_build

        n = anki_build.run(content_root, args.out,
                           repo_root() / "taxonomy" / "taxonomy.json",
                           with_spots=not args.no_spots,
                           with_bilgi=args.with_bilgi)
        print(f"anki deck: {n} notes -> {args.out}")
        return 0

    if args.cmd == "export" and args.what == "simulator":
        from tusopen.export.simulator import build as simulator_build

        n = simulator_build.run(content_root, args.out)
        print(f"simulator: {n} cases -> {args.out}")
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
