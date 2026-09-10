"""Schema + cross-reference validation for content/ and taxonomy (plan §6.3).

Checks per PR/release:
- taxonomy/taxonomy.json against its schema + global id uniqueness
- every content YAML against its type schema
- every taxonomy path (ders/konu/alt_konu, script `taksonomi` tuples) exists
- every `hastalik` id resolves to an illness script
- every `soru_ref` and `benzer` target resolves to a question id
- no duplicate content ids
- every `published` item has >=1 reviewer, distinct from the author
"""
import json
from pathlib import Path

import yaml
from jsonschema import Draft7Validator

SCHEMAS = Path(__file__).resolve().parents[3] / "schemas"
TEST_UPPER = {"ttbt": "TTBT", "ktbt": "KTBT"}
DONEM = ("ilkbahar", "sonbahar")


def _normalize(node):
    """YAML 1.1: unquoted key `no` loads as boolean False; map key bools back."""
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if k is True:
                k = "yes"
            elif k is False:
                k = "no"
            out[k] = _normalize(v)
        return out
    if isinstance(node, list):
        return [_normalize(x) for x in node]
    return node


def _schema_errors(data, schema):
    errors = Draft7Validator(schema).iter_errors(data)
    return sorted(
        ((" / ".join(str(p) for p in e.absolute_path) or "<file>", e.message)
         for e in errors),
        key=str,
    )


def _load_yaml(path: Path, schema_name: str):
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        return None, [f"{path}: YAML parse error: {e}"]
    data = _normalize(data)
    schema = json.loads((SCHEMAS / f"{schema_name}.schema.json").read_text(encoding="utf-8"))
    return data, [f"{path}: {loc}: {msg}" for loc, msg in _schema_errors(data, schema)]


def _load_taxonomy(path: Path):
    if not path.is_file():
        return None, [f"taxonomy missing: {path}"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return None, [f"taxonomy JSON error: {e}"]
    schema = json.loads((SCHEMAS / "taxonomy.schema.json").read_text(encoding="utf-8"))
    errs = [f"taxonomy: {loc}: {msg}" if loc != "<file>" else f"taxonomy: {msg}"
            for loc, msg in _schema_errors(data, schema)]
    seen = set()
    for test in data.get("tests", {}).values():
        for ders in test.get("dersler", []):
            seen.add(ders["id"])
            for konu in ders["konular"]:
                seen.add(konu["id"])
                for alt in konu.get("alt_konular", []):
                    seen.add(alt["id"])
    if len(seen) != sum(
        1
        for test in data.get("tests", {}).values()
        for ders in test.get("dersler", [])
        for node in [ders, *ders["konular"], *[a for k in ders["konular"] for a in k.get("alt_konular", [])]]
    ):
        errs.append("taxonomy: duplicate ids in tree")
    return data, errs


def _taxonomy_resolve(tax, test, ders, konu, alt):
    """Resolve [test, ders, konu, alt_konu]; None means 'not specified'."""
    upper = TEST_UPPER.get(test)
    if upper is None or upper not in tax["tests"]:
        return False
    dersler = {d["id"]: d for d in tax["tests"][upper]["dersler"]}
    if ders is None or ders not in dersler:
        return False
    if konu is None:
        return alt is None
    konular = {k["id"]: k for k in dersler[ders]["konular"]}
    if konu not in konular:
        return False
    if alt is None:
        return True
    alts = {a["id"] for a in konular[konu].get("alt_konular", [])}
    return alt in alts


def run(content_root: Path, taxonomy_path: Path) -> list:
    errors = []

    # sanity-check every schema file, even the ones not yet in use
    for sp in sorted(SCHEMAS.glob("*.schema.json")):
        try:
            Draft7Validator.check_schema(json.loads(sp.read_text(encoding="utf-8")))
        except Exception as e:
            errors.append(f"schema {sp.name}: {e}")

    tax, errs = _load_taxonomy(taxonomy_path)
    errors += errs
    if tax is None:
        return errors

    all_ids = {}
    soru_ids = set()
    script_ids = set()
    benzer_refs = []
    hastalik_refs = []
    ayirici_refs = []
    published_needing_review = []

    # question stubs
    q_files = sorted((content_root / "questions").rglob("*.yaml")) if (content_root / "questions").is_dir() else []

    for path in q_files:
        data, errs = _load_yaml(path, "question")
        errors += errs
        if data is None or errs:
            continue  # schema-invalid: report errors, skip cross-refs (no crash)
        sinav = data["sinav"]
        rel = path.relative_to(content_root)
        parts = rel.parts
        if parts[-1].split(".")[0] != sinav["test"].lower():
            errors.append(f"{rel}: file name does not match sinav.test {sinav['test']}")
        if str(sinav["yil"]) != parts[1]:
            errors.append(f"{rel}: sinav.yil {sinav['yil']} does not match directory")
        if parts[2] != sinav["donem"]:
            errors.append(f"{rel}: sinav.donem {sinav['donem']} does not match directory")
        nos = set()
        for s in data["sorular"]:
            if s["id"] in all_ids:
                errors.append(f"{rel}: duplicate id {s['id']} (also in {all_ids[s['id']]})")
            all_ids[s["id"]] = rel
            soru_ids.add(s["id"])
            expected = f"tus-{sinav['yil']}-{sinav['donem']}-{sinav['test'].lower()}-{s['no']}"
            if s["id"] != expected:
                errors.append(f"{rel}: id {s['id']} does not match sinav/no (expected {expected})")
            if s["no"] in nos:
                errors.append(f"{rel}: duplicate soru no {s['no']}")
            nos.add(s["no"])
            if s["iptal"] and s["cevap"] is not None:
                errors.append(f"{rel}: soru {s['no']}: iptal=true but cevap set")
            if not s["iptal"] and s["cevap"] is None:
                errors.append(f"{rel}: soru {s['no']}: missing cevap")
            for field in ("ders", "konu", "alt_konu"):
                if s[field] is not None and not _taxonomy_resolve(
                    tax, sinav["test"].lower(),
                    s["ders"], s["konu"], s["alt_konu"],
                ):
                    errors.append(
                        f"{rel}: soru {s['no']}: taxonomy path does not resolve: "
                        f"[{sinav['test'].lower()}, {s['ders']}, {s['konu']}, {s['alt_konu']}]"
                    )
                    break
            hastalik_refs += [(s["id"], h) for h in s["hastalik"]]
            benzer_refs += [(s["id"], b) for b in s["benzer"]]
        if data["status"] == "published":
            published_needing_review.append((rel, data))

    # illness scripts
    scripts = []
    for path in sorted((content_root / "scripts").rglob("*.yaml")) if (content_root / "scripts").is_dir() else []:
        data, errs = _load_yaml(path, "illness_script")
        errors += errs
        if data is None or errs:
            continue  # schema-invalid: report, skip cross-refs (no crash)
        rel = path.relative_to(content_root)
        if data["id"] in all_ids:
            errors.append(f"{rel}: duplicate id {data['id']} (also in {all_ids[data['id']]})")
        all_ids[data["id"]] = rel
        script_ids.add(data["id"])
        for tpath in data["taksonomi"]:
            if not _taxonomy_resolve(tax, *tpath):
                errors.append(f"{rel}: taxonomy path does not resolve: {tpath}")
        for entry in data.get("ayirici", []):
            ayirici_refs.append((data["id"], entry["hastalik"]))
        published_needing_review.append((rel, data))
        scripts.append(data)
        for ref in data.get("tus_gecmisi", []):
            benzer_refs.append((data["id"], ref))

    # cases
    cases = []
    for path in sorted((content_root / "cases").rglob("*.yaml")) if (content_root / "cases").is_dir() else []:
        data, errs = _load_yaml(path, "case")
        errors += errs
        if data is None or errs:
            continue  # schema-invalid: report, skip cross-refs (no crash)
        rel = path.relative_to(content_root)
        if data["id"] in all_ids:
            errors.append(f"{rel}: duplicate id {data['id']} (also in {all_ids[data['id']]})")
        all_ids[data["id"]] = rel
        if data.get("hastalik") and data["hastalik"] not in script_ids:
            errors.append(f"{rel}: case.hastalik has no illness script: {data['hastalik']}")
        n_secim = 0
        for adim in data["adimlar"]:
            if adim.get("tip") != "secim":
                continue
            n_secim += 1
            dogru = [s for s in adim.get("secenekler", []) if s["dogru"]]
            if len(dogru) != 1:
                errors.append(f"{rel}: secim step must have exactly one dogru secenek (found {len(dogru)})")
        if n_secim == 0:
            errors.append(f"{rel}: case has no secim step")
        cases.append(data)
        published_needing_review.append((rel, data))

    # walkthroughs
    for path in sorted((content_root / "walkthroughs").rglob("*.yaml")) if (content_root / "walkthroughs").is_dir() else []:
        data, errs = _load_yaml(path, "walkthrough")
        errors += errs
        if data is None or errs:
            continue  # schema-invalid: report, skip cross-refs (no crash)
        rel = path.relative_to(content_root)
        if data["id"] != f"wt-{data['soru_ref']}":
            errors.append(f"{rel}: id must be wt-<soru_ref> (got {data['id']}, ref {data['soru_ref']})")
        benzer_refs.append((data["id"], data["soru_ref"]))
        published_needing_review.append((rel, data))

    # facts
    for path in sorted((content_root / "facts").rglob("*.yaml")) if (content_root / "facts").is_dir() else []:
        data, errs = _load_yaml(path, "fact")
        errors += errs
        if data is None or errs:
            continue  # schema-invalid: report, skip cross-refs (no crash)
        rel = path.relative_to(content_root)
        if data["id"] in all_ids:
            errors.append(f"{rel}: duplicate id {data['id']} (also in {all_ids[data['id']]})")
        all_ids[data["id"]] = rel
        for tpath in data["taksonomi"]:
            if not _taxonomy_resolve(tax, *tpath):
                errors.append(f"{rel}: taxonomy path does not resolve: {tpath}")
        published_needing_review.append((rel, data))
        for ref in data.get("tus_gecmisi", []):
            benzer_refs.append((data["id"], ref))

    # cross-references
    for src, target in benzer_refs:
        if target not in soru_ids:
            errors.append(f"{src}: question reference does not exist: {target}")
    missing_scripts = sorted({h for _, h in hastalik_refs if h not in script_ids})
    if missing_scripts:
        errors.append(f"hastalik ids with no illness script: {missing_scripts[:10]}")
    missing_ayirici = sorted({h for src, h in ayirici_refs if h not in script_ids})
    if missing_ayirici:
        errors.append(f"ayirici targets with no illness script: {missing_ayirici[:10]}")

    # review rules (plan §8.3)
    for rel, data in published_needing_review:
        if data.get("status") != "published":
            continue
        reviewers = data.get("reviewed_by") or []
        author = data.get("author")
        if len(reviewers) < 1:
            errors.append(f"{rel}: published item has no reviewer")
        elif author is not None and author in reviewers:
            errors.append(f"{rel}: reviewer identical to author")

    return errors
