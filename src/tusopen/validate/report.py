"""Aggregate validation stats + report for the parsed local cache."""
import glob
import json
from collections import Counter
from pathlib import Path


def run(cache: Path) -> Path:
    out = cache / "parsed"
    rows, total_q, cancelled_total = [], 0, 0
    letters = Counter()
    img_q = opt_img_q = 0
    for jp in sorted(glob.glob(str(out / "*.json"))):
        d = json.loads(Path(jp).read_text(encoding="utf-8"))
        qs = d["questions"]
        total_q += len(qs)
        cancelled_total += len(d.get("cancelled", []))
        for q in qs:
            letters[q["answer"]] += 1
            if q["images"]:
                img_q += 1
            if q.get("option_images"):
                opt_img_q += 1
        n_imgs = sum(len(q["images"]) for q in qs)
        n_opt = sum(len(v) for q in qs for v in q.get("option_images", {}).values())
        warn = "; ".join(d["warnings"]) if d["warnings"] else "OK"
        rows.append((d["exam_id"], d["test"], d["question_count"],
                     len(d.get("cancelled", [])), n_imgs, n_opt, warn))

    full = [r for r in rows if r[2] > 20]
    samples = [r for r in rows if r[2] <= 20]

    lines = [
        "# TUS Parse Validation Report",
        "",
        f"- **Files:** {len(rows)} ({len(full)} full exams, {len(samples)} %10 samples)",
        f"- **Questions parsed:** {total_q} (full exams: {sum(r[2] for r in full)}, samples: {sum(r[2] for r in samples)})",
        f"- **Cancelled by ÖSYM (kept as `iptal` in stubs):** {cancelled_total}",
        f"- **Questions with attached figures:** {img_q} · **questions with image-options:** {opt_img_q}",
        "- **Answer distribution:** " + " ".join(f"{k}={v}" for k, v in sorted(letters.items())),
        "",
        "## Per-file status",
        "",
        "| File | Questions | Cancelled | Figures | Opt-images | Status |",
        "|---|---|---|---|---|---|",
    ]
    for exam, test, n, canc, ni, no, warn in rows:
        status = "OK" if warn == "OK" else warn
        lines.append(f"| {exam}_{test} | {n} | {canc} | {ni} | {no} | {status} |")

    lines += [
        "",
        "## Known artifact classes (accepted)",
        "",
        "- **Cancelled questions** (`Bu soru iptal edilmiştir.`) are detected, dropped from the",
        "  parsed question list, and cross-checked against the answer-key table (a cancelled",
        "  question has no key entry; 2017 key tables list letters for cancelled questions —",
        "  treated as informational, not error). The stubs keep them as `iptal: true` entries.",
        "- **Image-glyph tokens:** a handful of symbols (e.g., HCO3- in 2016-sonbahar_TTBT q27)",
        "  are rendered as images in the PDF itself; they are attached as figure images,",
        "  leaving a small text gap.",
        "- **`has_image_reference`** is a text heuristic and may be true for text-only questions.",
        "- Superscript/subscript runs are re-joined (O2, Ca2+, MgSO4, mm3, alpha2); wrapping/",
        "  line-break spacing may differ cosmetically from the PDF.",
        "",
        "## Licensing note (plan §9)",
        "",
        "ÖSYM exam questions are copyrighted works (FSEK). Parsed text and images live in the",
        "local cache only — never redistribute, commit, or ship them. The public repo carries",
        "metadata (ids, answer keys, tags) and own-words content only.",
    ]

    report = out / "validation_report.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {report}")
    print(f"total questions: {total_q}, answer dist: {dict(sorted(letters.items()))}")
    print(f"figure questions: {img_q}, image-option questions: {opt_img_q}")
    return report
