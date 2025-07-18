import os
from core.sorter import Sorter

def test_sorter(tmp_path):
    test_dir = tmp_path / "test"
    test_dir.mkdir()
    (test_dir / "a.txt").write_text("hello")
    (test_dir / "b.jpg").write_text("image")
    s = Sorter()
    count = s.sort(str(test_dir))
    assert count == 2
    assert (test_dir / "txt" / "a.txt").exists()
    assert (test_dir / "jpg" / "b.jpg").exists()