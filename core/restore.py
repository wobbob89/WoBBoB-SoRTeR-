import shutil
from pathlib import Path

class RestorePoint:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.restore_dir = self.base_dir / ".restore_points"
        self.restore_dir.mkdir(exist_ok=True)

    def create(self):
        snapshots = list(self.restore_dir.glob("snap_*"))
        snap_id = len(snapshots) + 1
        snapshot = self.restore_dir / f"snap_{snap_id}"
        shutil.copytree(self.base_dir, snapshot, dirs_exist_ok=True, ignore=shutil.ignore_patterns('.restore_points'))

    def last_snapshot(self):
        snaps = sorted(self.restore_dir.glob("snap_*"), key=lambda p: p.stat().st_mtime, reverse=True)
        return snaps[0].name if snaps else None

    def restore(self, snap_name):
        snapshot = self.restore_dir / snap_name
        if snapshot.exists():
            for item in self.base_dir.iterdir():
                if item.name != ".restore_points":
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
            shutil.copytree(snapshot, self.base_dir, dirs_exist_ok=True, ignore=shutil.ignore_patterns('.restore_points'))