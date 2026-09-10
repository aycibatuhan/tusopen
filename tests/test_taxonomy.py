import json
import re

from tusopen.validate import content as content_mod


def test_taxonomy_ids_unique_and_ascii(repo_root):
    data = json.loads((repo_root / "taxonomy" / "taxonomy.json").read_text())
    ids = []
    for t in data["tests"].values():
        for ders in t["dersler"]:
            ids.append(ders["id"])
            for konu in ders["konular"]:
                ids.append(konu["id"])
                ids.extend(a["id"] for a in konu["alt_konular"])
    assert len(ids) == len(set(ids)), "duplicate taxonomy ids"
    assert all(re.match(r"^[a-z][a-z0-9_]*$", i) for i in ids)


def test_taxonomy_depth_three(repo_root):
    data = json.loads((repo_root / "taxonomy" / "taxonomy.json").read_text())
    for t in data["tests"].values():
        for ders in t["dersler"]:
            assert ders["konular"], f"{ders['id']}: konular boş"
            for konu in ders["konular"]:
                assert konu["alt_konular"], f"{konu['id']}: alt_konular boş"
                for alt in konu["alt_konular"]:
                    assert "alt_konular" not in alt


def test_content_validates_clean(tmp_content, repo_root):
    errors = content_mod.run(tmp_content, repo_root / "taxonomy" / "taxonomy.json")
    assert errors == []
