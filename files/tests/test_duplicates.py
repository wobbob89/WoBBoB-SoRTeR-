import os
from core.duplicates import find_duplicates

def test_find_duplicates(tmp_path):
    test_dir = tmp_path / "d"
    test_dir.mkdir()
    f1 = test_dir / "a.txt"
    f2 = test_dir / "b.txt"
    f1.write_text("same")
    f2.write_text("same")
    dups = find_duplicates(str(test_dir))
    assert dups, "Should find duplicates"