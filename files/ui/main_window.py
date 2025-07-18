from PyQt5.QtWidgets import QMainWindow, QTabWidget
from ui.dashboard import DashboardTab
from ui.organise import OrganiseTab
from ui.restore import RestoreTab
from ui.settings import SettingsTab
from ui.music import MusicTab
from ui.duplicates import DuplicatesTab
from ui.photos import PhotosTab
from ui.documents import DocumentsTab
from ui.analytics import AnalyticsTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WoBBoB WiZArD")
        self.setGeometry(100, 100, 1280, 900)
        self.tabs = QTabWidget()
        self.tabs.addTab(DashboardTab(), "Dashboard")
        self.tabs.addTab(OrganiseTab(), "Organise")
        self.tabs.addTab(DuplicatesTab(), "Duplicates")
        self.tabs.addTab(PhotosTab(), "Photos")
        self.tabs.addTab(MusicTab(), "Music")
        self.tabs.addTab(DocumentsTab(), "Documents")
        self.tabs.addTab(RestoreTab(), "Restore")
        self.tabs.addTab(AnalyticsTab(), "Analytics")
        self.tabs.addTab(SettingsTab(), "Settings")
        self.setCentralWidget(self.tabs)