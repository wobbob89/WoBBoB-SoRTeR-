from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from core.documents import DocumentManager

class DocumentsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.info = QLabel("Document automation: OCR & sensitive data scan.")
        layout.addWidget(self.info)
        btn = QPushButton("Select Documents Folder")
        btn.clicked.connect(self.scan_docs)
        layout.addWidget(btn)
        self.setLayout(layout)

    def scan_docs(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Documents Folder")
        if folder:
            manager = DocumentManager(folder)
            count, sensitive = manager.scan_documents()
            self.info.setText(f"Documents scanned: {count}, Sensitive found: {sensitive}")