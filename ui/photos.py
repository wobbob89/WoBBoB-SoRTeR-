from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from core.photos import PhotoManager

class PhotosTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.info = QLabel("Photo organiser: facial recognition & NSFW filter.")
        layout.addWidget(self.info)
        btn = QPushButton("Select Photos Folder")
        btn.clicked.connect(self.scan_photos)
        layout.addWidget(btn)
        self.setLayout(layout)

    def scan_photos(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Photos Folder")
        if folder:
            manager = PhotoManager(folder)
            faces, nsfw = manager.analyse_photos()
            self.info.setText(f"Photos scanned. Faces found: {faces}, NSFW images: {nsfw}")