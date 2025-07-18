from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from core.music import MusicManager

class MusicTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.info = QLabel("Music organiser: scan and tag your music library.")
        layout.addWidget(self.info)
        btn = QPushButton("Select Music Folder")
        btn.clicked.connect(self.scan_music)
        layout.addWidget(btn)
        self.setLayout(layout)

    def scan_music(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Music Folder")
        if folder:
            manager = MusicManager(folder)
            count = manager.scan_and_tag()
            self.info.setText(f"Scanned and tagged {count} music files.")