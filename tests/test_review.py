import csv

from tusopen.review import apply_sheet, dump


def _rows(path):
    return list(csv.DictReader(path.open(encoding="utf-8")))


def test_review_roundtrip(tmp_content, tmp_path):
    sheet = tmp_path / "sheet.csv"
    dump(tmp_content, None, sheet)
    rows = _rows(sheet)
    assert len(rows) == 3  # 1 script + 1 fact + 1 case
    assert {r["tip"] for r in rows} == {"scripts", "facts", "cases"}

    rows[0]["reviewer"] = "Dr. A; Dr. B"
    rows[0]["status"] = "reviewed"
    filled = tmp_path / "filled.csv"
    with filled.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    assert apply_sheet(tmp_content, filled) == 0
    assert apply_sheet(tmp_content, filled) == 0  # idempotent

    import yaml
    target = tmp_content / rows[0]["dosya"]
    data = yaml.safe_load(target.read_text(encoding="utf-8"))
    assert data["status"] == "reviewed"
    assert data["reviewed_by"] == ["Dr. A", "Dr. B"]
    assert data["last_reviewed"]
    # untouched file keeps draft
    other = next(r for r in rows if r is not rows[0])
    other_data = yaml.safe_load(
        (tmp_content / other["dosya"]).read_text(encoding="utf-8"))
    assert other_data["status"] == "draft"


def test_review_ders_filter(tmp_content, tmp_path):
    sheet = tmp_path / "d.csv"
    dump(tmp_content, "dahiliye", sheet)
    rows = _rows(sheet)
    assert all(r["ders"] == "dahiliye" for r in rows)
    dump(tmp_content, "patoloji", sheet)
    assert _rows(sheet) == []
