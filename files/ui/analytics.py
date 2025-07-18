from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class AnalyticsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Analytics and logs coming soon!"))
        self.setLayout(layout)