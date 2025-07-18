from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from core.duplicates import find_duplicates

class DuplicatesTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.info = QLabel("Find duplicate files in a folder.")
        layout.addWidget(self.info)
        btn = QPushButton("Scan for Duplicates")
        btn.clicked.connect(self.scan_dupes)
        layout.addWidget(btn)
        self.setLayout(layout)

    def scan_dupes(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            dups = find_duplicates(folder)
            self.info.setText(f"Found {len(dups)} duplicate files.")