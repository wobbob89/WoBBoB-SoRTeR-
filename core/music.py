import os
from mutagen import File as MutagenFile

class MusicManager:
    def __init__(self, folder):
        self.folder = folder

    def scan_and_tag(self):
        count = 0
        for root, dirs, files in os.walk(self.folder):
            for name in files:
                path = os.path.join(root, name)
                try:
                    mf = MutagenFile(path)
                    if mf:
                        # Example: print or log tags
                        pass
                    count += 1
                except Exception:
                    pass
        return count