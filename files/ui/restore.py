from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from core.restore import RestorePoint

class RestoreTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.info = QLabel("Create or restore from a restore point.")
        layout.addWidget(self.info)
        btn_create = QPushButton("Create Restore Point")
        btn_create.clicked.connect(self.create_restore)
        layout.addWidget(btn_create)
        btn_restore = QPushButton("Restore Last Point")
        btn_restore.clicked.connect(self.restore_last)
        layout.addWidget(btn_restore)
        self.setLayout(layout)

    def create_restore(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            rp = RestorePoint(folder)
            rp.create()
            self.info.setText("Restore point created.")

    def restore_last(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            rp = RestorePoint(folder)
            snap = rp.last_snapshot()
            if snap:
                rp.restore(snap)
                self.info.setText("Restored from last point.")
            else:
                self.info.setText("No snapshots found.")