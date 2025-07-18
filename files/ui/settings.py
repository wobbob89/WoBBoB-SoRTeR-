from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Settings (theme, language, plugins, account, etc.) coming soon!"))
        self.setLayout(layout)