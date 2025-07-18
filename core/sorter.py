import os
from pathlib import Path
import shutil

class Sorter:
    def __init__(self, rules=None):
        self.rules = rules or {}

    def sort(self, directory):
        """Sort files in a directory by extension into folders."""
        count = 0
        for file in Path(directory).iterdir():
            if file.is_file():
                ext = file.suffix.lower().lstrip(".")
                if not ext:
                    ext = "other"
                target_dir = Path(directory) / ext
                target_dir.mkdir(exist_ok=True)
                shutil.move(str(file), str(target_dir / file.name))
                count += 1
        return count