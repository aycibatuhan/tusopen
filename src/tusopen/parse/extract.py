"""Parse official ÖSYM TUS booklet PDFs into structured JSON + Markdown.

Local-only step (plan §6.2): full question text stays in the cache under
``<cache>/parsed``. The committable metadata stubs written to ``content/``
carry no question text (plan §5.1).

Usage (via the CLI):
  tusopen parse --all
  tusopen parse --files 2021-ilkbahar_TTBT 2019-sonbahar_KTBT
"""
import csv
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import pymupdf
import yaml

DONEM_AD = {"ilkbahar": "İlkbahar", "sonbahar": "Sonbahar"}

LETTER_RE = re.compile(r"^[A-E]\)$")
MARKER_RE = re.compile(r"^(\d{1,3})\.$")
DOGRU_RE = re.compile(r"DOĞRU\s+CEVAP\s*:\s*([A-E])", re.IGNORECASE)
VISUAL_RE = re.compile(
    r"(?:yukarıda|yukarıdaki|yanda|yandaki|aşağıda|aşağıdaki)[^\n]{0,70}?"
    r"(şekilde|şeklindeki|görüntüde|görüntüsünde|grafide|grafikte|endoskopide|mikroskop|radyografide)"
    r"|şekildeki|görüntüdeki|radyografide|ok ile işaretli",
    re.IGNORECASE,
)

NOISE_SUBSTRINGS = (
    "Diğer sayfaya geçiniz",
    "telif hakları ÖSYM",
    "kullanılamaz",
    "Bu testte",
    "TEST BİTTİ",
    "CEVAPLARINIZI KONTROL EDİNİZ",
)

HEADER_Y = 62.0
FOOTER_Y = 735.0
ROW_TOL = 4.5
SUPER_DY = 5.0


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


@dataclass
class Span:
    text: str
    x0: float
    y0: float
    x1: float
    y1: float
    page: int
    col: int
    size: float = 9.0
    sup: bool = False


def collect_spans(doc, page_no, img_rects) -> list:
    """Filtered spans of one page, column-tagged, small-font fragments merged."""
    d = doc[page_no].get_text("dict")
    raw = []
    for b in d["blocks"]:
        if b["type"] != 0:
            continue
        for ln in b["lines"]:
            for s in ln["spans"]:
                t = s["text"]
                if not t.strip():
                    continue
                x0, y0, x1, y1 = s["bbox"]
                if y0 < HEADER_Y or y0 > FOOTER_Y:
                    continue
                ts = t.strip()
                if s.get("size", 9.0) > 30:  # page watermarks (huge display text,
                    continue                 # incl. diagonal Ö/S/Y/M letters)
                if any(sub in t for sub in NOISE_SUBSTRINGS):
                    continue
                cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                structural = bool(
                    LETTER_RE.match(ts) or MARKER_RE.match(ts)
                )
                if not structural and any(
                    rx0 - 2 <= cx <= rx1 + 2 and ry0 - 2 <= cy <= ry1 + 2
                    for rx0, ry0, rx1, ry1 in img_rects.get(page_no, [])
                ):
                    continue
                raw.append(
                    Span(
                        t, x0, y0, x1, y1, page_no,
                        0 if x0 < 290.0 else 1,
                        s.get("size", 9.0),
                        bool(s.get("flags", 0) & 1),
                    )
                )
    return merge_small_fragments(raw)


def merge_small_fragments(spans):
    """Merge superscript/subscript fragments (O2, Ca2+, MgSO4, mm3) into neighbors."""
    spans.sort(key=lambda s: (s.page, s.col, round(s.y0, 1), s.x0))
    out = []
    for s in spans:
        st = s.text.strip()
        if out:
            p = out[-1]
            same_line = (
                s.page == p.page and s.col == p.col and abs(s.y0 - p.y0) < SUPER_DY
            )
            gap = s.x0 - p.x1
            if (
                same_line
                and len(st) <= 4
                and len(p.text.strip()) > 3  # never merge into letter/marker spans
                and -1.0 < gap < 12.0
                and (s.size < 0.82 * p.size or (s.sup and s.size <= p.size))
            ):
                p.text += s.text
                p.x1 = max(p.x1, s.x1)
                p.y1 = max(p.y1, s.y1)
                continue
        # try prepending to the next normal span (e.g., superscript BEFORE base: 32P)
        if len(st) <= 4 and (s.sup or s.size < 7.5) and out:
            p = out[-1]
            if (
                s.page == p.page
                and s.col == p.col
                and abs(p.y0 - s.y0) < SUPER_DY
                and len(p.text.strip()) > 3  # never prepend into letter/marker spans
                and 0 <= p.x0 - s.x1 < 12
                and p.size >= s.size * 1.2
            ):
                p.text = s.text + p.text
                p.x0 = min(p.x0, s.x0)
                continue
        out.append(s)
    return out


def parse_key_pages(doc):
    """Scan pages from the end; collect (number, letter) rows until a page
    stops looking like a key page. Returns (key, key_page_numbers)."""
    key = {}
    key_pages = set()
    for pno in range(doc.page_count - 1, -1, -1):
        rows = {}
        for b in doc[pno].get_text("dict")["blocks"]:
            if b["type"] != 0:
                continue
            for ln in b["lines"]:
                for s in ln["spans"]:
                    t = s["text"].strip()
                    if t:
                        rows.setdefault(round(s["bbox"][1]), []).append((s["bbox"][0], t))
        page_pairs = 0
        for y in sorted(rows):
            items = sorted(rows[y])
            num = None
            for _, t in items:
                m_single = re.fullmatch(r"(\d{1,3})\.?\s+([A-E])\b", t)
                if m_single and int(m_single.group(1)) not in key:
                    key[int(m_single.group(1))] = m_single.group(2)
                    page_pairs += 1
                    continue
                m = re.fullmatch(r"(\d{1,3})\.?", t)
                if m:
                    num = int(m.group(1))
                    continue
                m2 = re.fullmatch(r"([A-E])", t)
                if m2 and num is not None and num not in key:
                    key[num] = m2.group(1)
                    page_pairs += 1
                    num = None
        if page_pairs < 20:
            break
        key_pages.add(pno)
    return key, key_pages


def slot_spans(markers, col_spans_by_page, idx):
    """Spans belonging to marker #idx: from its y (in its page+col) until the
    next marker in the same column, spanning page boundaries if needed."""
    p0, c0, y0, _ = markers[idx][:4]
    if idx + 1 < len(markers):
        p1, _c1, y1, _ = markers[idx + 1][:4]
    else:
        p1, y1 = 10**9, 0.0
    out = []
    for p in sorted(col_spans_by_page):
        spans = [s for s in col_spans_by_page[p] if s.col == c0]
        if p == p0 and p == p1:
            out += [s for s in spans if y0 - 4 <= s.y0 < y1 - 4]
        elif p == p0:
            out += [s for s in spans if s.y0 >= y0 - 4]
        elif p == p1:
            out += [s for s in spans if s.y0 < y1 - 4]
        elif p0 < p < p1:
            out += spans
    return out


def extract_slot(spans):
    """Split slot spans into stem text + options + inline answer + letters.
    Spans are grouped into visual rows (chain dy<=ROW_TOL) so texts rendered a
    fraction of a point above/below their option letter still pair correctly;
    within a row, texts pair to the nearest letter at-or-left of them (grid
    lanes); texts in rows without letters belong to the last letter above
    (wrapped option lines)."""
    ordered = sorted(spans, key=lambda s: (s.page, s.y0, s.x0))
    rows = []
    for s in ordered:
        if rows and s.page == rows[-1][-1].page and abs(s.y0 - rows[-1][-1].y0) <= ROW_TOL:
            rows[-1].append(s)
        else:
            rows.append([s])

    first_letter = next((s for row in rows for s in row if LETTER_RE.match(s.text.strip())), None)
    inline = None
    stem_parts, opt_parts = [], {L: [] for L in "ABCDE"}
    current = None
    for row in rows:
        row_letters = [s for s in row if LETTER_RE.match(s.text.strip())]
        if row_letters:
            current = row_letters[-1]
        for s in row:
            tt = s.text.strip()
            if MARKER_RE.match(tt):
                continue
            m = DOGRU_RE.search(s.text)
            if m:
                inline = m.group(1)
                continue
            if "iptal edilmiştir" in s.text:
                continue
            if LETTER_RE.match(tt):
                continue
            if first_letter is None or s.y0 < first_letter.y0 - 3:
                stem_parts.append(s)
                continue
            lane = [ln for ln in row_letters if ln.x0 <= s.x0 + 2]
            target = max(lane, key=lambda ln: ln.x0) if lane else current
            if target is None:
                stem_parts.append(s)
                continue
            if s.x0 >= target.x0 + 5:
                opt_parts[target.text.strip()[0]].append(s)
            else:
                stem_parts.append(s)

    def join(parts):
        parts = sorted(parts, key=lambda s: (s.page, s.y0, s.x0))
        # cluster into visual lines (superscripts share the base line), then x-order
        lines = []
        for s in parts:
            if lines and s.page == lines[-1][-1].page and abs(s.y0 - lines[-1][-1].y0) < 5:
                lines[-1].append(s)
            else:
                lines.append([s])
        out = []
        prev = None
        for line in lines:
            line.sort(key=lambda s: s.x0)
            for s in line:
                if prev is not None:
                    if prev.page == s.page and abs(prev.y0 - s.y0) < 5:
                        out.append("" if s.x0 - prev.x1 < 2.5 else " ")
                    elif prev.text.rstrip().endswith("-"):
                        pass  # hyphenated line break
                    elif prev.text.rstrip().endswith((".", ":", "?", ")")):
                        out.append("\n")
                    else:
                        out.append(" ")
                out.append(s.text)
                prev = s
        text = re.sub(r"[ \t]+", " ", "".join(out))
        text = re.sub(r" ([,.;:?!])", r"\1", text)
        text = re.sub(r" +\n", "\n", text)
        text = re.sub(r"\n +", "\n", text)
        return nfc(text.strip())

    stem = join(stem_parts)
    options = {L: join(opt_parts[L]) for L in "ABCDE"}
    letters = [s for row in rows for s in row if LETTER_RE.match(s.text.strip())]
    return stem, options, inline, letters


def classify_images(doc):
    """Return (figure_rects_by_page, attachable_images_by_page).
    Background watermark stripes repeat on nearly every page at the same size —
    detected by (width, height) repetition and excluded everywhere."""
    from collections import defaultdict

    per_page = []
    for pno in range(doc.page_count):
        items = []
        for info in doc[pno].get_image_info(xrefs=True):
            x0, y0, x1, y1 = info["bbox"]
            items.append((info["xref"], (x0, y0, x1, y1)))
        per_page.append(items)

    counts = defaultdict(int)
    for items in per_page:
        for _, (x0, y0, x1, y1) in items:
            counts[(round(x1 - x0), round(y1 - y0))] += 1

    n_pages = max(doc.page_count, 1)
    background = {
        key for key, c in counts.items() if c >= max(6, int(0.4 * n_pages))
    }

    figure_rects, attachable = {}, {}
    for pno, items in enumerate(per_page):
        rects, attaches = [], []
        for xref, (x0, y0, x1, y1) in items:
            w, h = round(x1 - x0), round(y1 - y0)
            if (w, h) in background:
                continue
            if w > 550 and h > 750:  # full-page cover art
                continue
            rects.append((x0, y0, x1, y1))
            attaches.append((xref, (x0, y0, x1, y1)))
        figure_rects[pno] = rects
        attachable[pno] = attaches
    return figure_rects, attachable


INSTRUCTION_MARKERS = (
    "geçersiz sayılacaktır",
    "Tutanağına",
    "kayıt altına",
    "Bu kitapçıkta",
    "cevaplama süresi",
    "AÇIKLAMA",
    "uygulamaya ilişkin",
    "İşaretlediğiniz bir cevabı",
)


def page_is_instructions(doc, pno) -> bool:
    text = doc[pno].get_text("text")
    return any(m in text for m in INSTRUCTION_MARKERS)


def extract_pdf(path: Path, exam_id: str, test: str, url: str, sha: str, out_dir: Path):
    doc = pymupdf.open(path)
    year, donem = exam_id.rsplit("-", 1)
    is_sample = int(year) >= 2022

    key, key_pages = ({}, set()) if is_sample else parse_key_pages(doc)

    img_rects, attachable_images = classify_images(doc)

    # front matter (cover + instructions with fake 1.-8. markers) ends where
    # the first page with >=5 option letters begins
    content_start = 0
    for p in range(doc.page_count):
        if p in key_pages:
            continue
        n_letters = sum(
            1
            for b in doc[p].get_text("dict")["blocks"]
            if b["type"] == 0
            for ln in b["lines"]
            for s in ln["spans"]
            if LETTER_RE.match(s["text"].strip())
        )
        if n_letters >= 5:
            content_start = p
            break

    pages_spans = {
        p: collect_spans(doc, p, img_rects)
        for p in range(doc.page_count)
        if p not in key_pages and p >= content_start and not page_is_instructions(doc, p)
    }

    markers_by_col = {0: [], 1: []}
    for p in sorted(pages_spans):
        for col in (0, 1):
            col_spans = [s for s in pages_spans[p] if s.col == col]
            ms = [s for s in col_spans if MARKER_RE.match(s.text.strip())]
            if not ms:
                continue
            min_x = min(s.x0 for s in ms)
            for s in ms:
                if s.x0 <= min_x + 6:
                    markers_by_col[col].append((p, s.y0, int(MARKER_RE.match(s.text.strip()).group(1))))
    for col in markers_by_col:
        markers_by_col[col].sort()

    # typesetting errors: a question number occasionally printed as a duplicate
    # (e.g., 2013-d2_KTBT: q8's marker printed as "9."). Renumber the first of
    # two adjacent equal numbers to the expected sequence value.
    flow = []
    for p in sorted(pages_spans):
        flow += [(p, 0, y, n) for (pp, y, n) in markers_by_col[0] if pp == p]
        flow += [(p, 1, y, n) for (pp, y, n) in markers_by_col[1] if pp == p]
    renumbers = {}
    expected = 1
    for idx, (p, c, y, n) in enumerate(flow):
        nxt = flow[idx + 1][3] if idx + 1 < len(flow) else None
        if n == expected:
            expected += 1
        elif n == expected + 1 and nxt == n:
            renumbers[(p, c, y)] = expected
            expected += 2
        elif n > expected:
            expected = n + 1
    for (p, c, y), new in renumbers.items():
        markers_by_col[c] = [
            (pp, yy, new if (pp, yy) == (p, y) else nn)
            for (pp, yy, nn) in markers_by_col[c]
        ]
        markers_by_col[c].sort()

    slots = {}  # num -> spans
    cancelled_nums = []
    for col, markers in markers_by_col.items():
        csp = {p: [s for s in pages_spans[p] if s.col == col] for p in sorted(pages_spans)}
        flat = [(p, col, y, n, i) for i, (p, y, n) in enumerate(markers)]
        for i in range(len(flat)):
            spans = slot_spans(flat, csp, i)
            slots.setdefault(flat[i][3], []).extend(spans)

    # cancelled questions: "Bu soru iptal edilmiştir." prints just above the
    # cancelled question's own marker (offset varies by year) -> global rule:
    # each iptal span cancels the nearest marker below it in the same column
    for col in (0, 1):
        for p in sorted(pages_spans):
            col_markers = sorted(
                (y, n) for (pp, y, n) in markers_by_col[col] if pp == p
            )
            for s in pages_spans[p]:
                if s.col != col or "iptal edilmiştir" not in s.text:
                    continue
                below = [(y, n) for y, n in col_markers if y >= s.y0 - 1]
                if below:
                    cancelled_nums.append(min(below)[1])

    questions = []
    for num in sorted(slots):
        if num in cancelled_nums:
            continue
        spans = [
            s for s in slots[num]
            if not MARKER_RE.match(s.text.strip()) and "iptal edilmiştir" not in s.text
        ]
        if not spans:
            continue
        stem, options, inline, letters = extract_slot(spans)
        questions.append(
            {
                "number": num,
                "stem": stem,
                "options": options,
                "answer": None,
                "inline": inline,
                "has_image_reference": bool(VISUAL_RE.search(stem)),
                "images": [],
                "option_images": {},
                "_spans": spans,
                "_letters": letters,
            }
        )

    # attach images by page + column + y-overlap with slot spans
    img_dir = out_dir / "images" / exam_id
    slot_by_num = {q["number"]: q["_spans"] for q in questions}
    letters_by_num = {q["number"]: q["_letters"] for q in questions}
    for pno, attaches in attachable_images.items():
        for xref, (ix0, iy0, ix1, iy1) in attaches:
            col = 0 if ix0 < 290.0 else 1
            center = (ix0 + ix1) / 2
            for q in questions:
                seg = [s for s in slot_by_num[q["number"]] if s.page == pno and s.col == col]
                if not seg:
                    continue
                lo = min(s.y0 for s in seg) - 30
                hi = max(s.y1 for s in seg) + 30
                if iy1 >= lo and iy0 <= hi:
                    try:
                        img = doc.extract_image(xref)
                    except Exception:
                        continue
                    img_dir.mkdir(parents=True, exist_ok=True)
                    fname = f"q{q['number']}_{pno}_{xref}.{img['ext']}"
                    (img_dir / fname).write_bytes(img["image"])
                    rel = str((img_dir / fname).relative_to(out_dir))
                    # an image belongs to an option only if it sits below that
                    # option's letter; figures above the options are stem images
                    letters = letters_by_num[q["number"]]
                    best, best_key = None, None
                    for ln in letters:
                        if iy0 < ln.y0 - 5:
                            continue
                        dy = abs(ln.y0 - iy0)
                        dx = abs(ln.x0 - center)
                        k = (dy, dx)
                        if best_key is None or k < best_key:
                            best_key, best = k, ln
                    L = best.text.strip()[0] if best else None
                    if L and not q["options"][L]:
                        lst = q["option_images"].setdefault(L, [])
                        if rel not in lst:
                            lst.append(rel)
                    elif rel not in q["images"]:
                        q["images"].append(rel)
    doc.close()

    for q in questions:
        q.pop("_spans")
        q.pop("_letters")
        if q["number"] in key:
            q["answer"] = key[q["number"]]
        elif q.get("inline"):
            q["answer"] = q.pop("inline")
        else:
            q.pop("inline", None)
        if not q["option_images"]:
            q.pop("option_images")
        if q["images"] or q.get("option_images"):
            q["has_image_reference"] = True

    # validation
    errs = []
    nums = [q["number"] for q in questions]
    n_max = max(slots) if slots else 0
    expected_nums = set(range(1, n_max + 1)) - set(cancelled_nums)
    if not is_sample:
        missing = sorted(expected_nums - set(nums))
        extra = sorted(set(nums) - set(range(1, n_max + 1)))
        if missing or extra:
            errs.append(f"numbering: missing={missing[:12]} extra={extra[:12]}")
        if len(key) < len(expected_nums):
            errs.append(f"answer key incomplete: {len(key)}/{len(expected_nums)}")
        key_missing = sorted(set(range(1, n_max + 1)) - set(key))
        cancel_set = sorted(set(cancelled_nums))
        unexplained = sorted(set(key_missing) - set(cancel_set))
        if unexplained:
            errs.append(f"cancellation mismatch: key missing without iptal: {unexplained[:12]}")
        if cancelled_nums:
            errs.append(f"cancelled questions: {cancel_set}")
    else:
        if not 10 <= len(questions) <= 12:
            errs.append(f"sample: {len(questions)} content questions, expected 10-12")
        if nums != sorted(nums):
            errs.append("sample numbers not sorted")
    for q in questions:
        if len(q["stem"]) < 15:
            errs.append(f"q{q['number']}: stem too short")
        if "ÖSYM" in q["stem"] or any("ÖSYM" in v for v in q["options"].values()):
            errs.append(f"q{q['number']}: watermark token in text")
        for L in "ABCDE":
            if not q["options"][L] and L not in q.get("option_images", {}):
                errs.append(f"q{q['number']}: option {L} empty")
        if q["answer"] not in {"A", "B", "C", "D", "E"}:
            errs.append(f"q{q['number']}: bad/missing answer {q['answer']!r}")
    alltext = "".join(q["stem"] + "".join(q["options"].values()) for q in questions)
    if not any(c in alltext for c in "ğışİüöçŞĞÜÖ"):
        errs.append("no Turkish letters — possible encoding corruption")

    result = {
        "exam_id": exam_id,
        "test": test,
        "year": int(year),
        "donem": donem,
        "is_sample": is_sample,
        "source_url": url,
        "sha256": sha,
        "question_count": len(questions),
        "cancelled": sorted(set(cancelled_nums)),
        "questions": questions,
        "warnings": sorted(set(errs)),
    }
    return result


def write_outputs(res, exam_id, test, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{exam_id}_{test}.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    title = "Temel Tıp Bilimleri" if test == "TTBT" else "Klinik Tıp Bilimleri"
    donem_ad = DONEM_AD.get(res["donem"], res["donem"])
    lines = [
        f"# {res['year']}-TUS {donem_ad} — {title} ({test})",
        "",
        f"Kaynak: {res['source_url']}",
        f"Soru sayısı: {res['question_count']}" + (" (%10 örnek)" if res["is_sample"] else ""),
        "",
    ]
    for q in res["questions"]:
        lines.append(f"## Soru {q['number']}")
        lines.append("")
        lines.append(q["stem"])
        lines.append("")
        for L in "ABCDE":
            opt = q["options"][L]
            lines.append(f"**{L})** {opt if opt else '_(görsel)_'}")
            for im in q.get("option_images", {}).get(L, []):
                lines.append(f"  ![görüntü]({im})")
        lines.append("")
        for im in q["images"]:
            lines.append(f"![görüntü]({im})")
        if q["images"]:
            lines.append("")
        lines.append(f"**Cevap:** {q['answer'] or '?'}")
        lines.append("")
    (out_dir / f"{exam_id}_{test}.md").write_text("\n".join(lines), encoding="utf-8")


def load_meta(cache: Path):
    urls, sha = {}, {}
    src_path = Path(__file__).parents[1] / "fetch" / "sources.yaml"
    src = yaml.safe_load(src_path.read_text(encoding="utf-8"))
    for s in src["sittings"]:
        urls[f"{s['year']}-{s['donem']}_{s['test']}"] = s["url"]
    man = cache / "manifest.csv"
    if man.exists():
        with open(man, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                sha[row["file"].removesuffix(".pdf")] = row["sha256"]
    return urls, sha


def run(cache: Path, targets, with_stubs: bool = True, content_root: Path | None = None):
    raw = cache / "raw"
    out = cache / "parsed"
    out.mkdir(parents=True, exist_ok=True)
    urls, shas = load_meta(cache)
    ok, bad = 0, 0
    for t in targets:
        path = raw / f"{t}.pdf"
        if not path.exists():
            print(f"{t:24} missing PDF")
            bad += 1
            continue
        exam_id, test = t.rsplit("_", 1)
        res = extract_pdf(path, exam_id, test, urls.get(t, ""), shas.get(t, ""), out)
        write_outputs(res, exam_id, test, out)
        if with_stubs and content_root is not None:
            from tusopen.parse.stubs import write_stub

            write_stub(res, content_root)
        if res["warnings"]:
            bad += 1
            print(f"{t:24} {res['question_count']:3} questions — {'; '.join(res['warnings'][:3])}")
        else:
            ok += 1
            print(f"{t:24} {res['question_count']:3} questions — OK")
    print(f"done: {ok} OK, {bad} with warnings/missing")
    return 1 if bad else 0
