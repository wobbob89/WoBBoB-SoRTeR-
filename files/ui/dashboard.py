from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class DashboardTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel(
            "<h1>Welcome to WoBBoB WiZArD!</h1>"
            "<p>Your AI-powered desktop organiser.<br>"
            "Use the tabs above to explore all features.</p>"
        )
        layout.addWidget(label)
        self.setLayout(layout)