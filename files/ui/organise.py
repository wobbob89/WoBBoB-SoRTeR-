from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from core.sorter import Sorter

class OrganiseTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.info = QLabel("Select a folder to organise your files with AI.")
        layout.addWidget(self.info)
        btn_browse = QPushButton("Choose Folder")
        btn_browse.clicked.connect(self.choose_folder)
        layout.addWidget(btn_browse)
        self.setLayout(layout)

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            sorter = Sorter()
            count = sorter.sort(folder)
            self.info.setText(f"Organised! {count} files sorted.")