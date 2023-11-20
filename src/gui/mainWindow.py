from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QListWidgetItem

from src.gui.configWindow import ConfigWindow
from src.gui.ui.ui_mainwindow import Ui_MainWindow

from src.TTSengine.TTS import UpdateListWorker, TTS


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.startButton.clicked.connect(self.start_tts)
        self.ui.configButton.clicked.connect(self.open_config_window)

        self.worker = UpdateListWorker()
        self.tts = TTS(self.worker)
        self.worker.item_added.connect(self.update_list_widget)

        self.config_window = None

    @Slot()
    def open_config_window(self):
        if not self.config_window or not self.config_window.isVisible():
            self.config_window = ConfigWindow(self)
            self.config_window.show()

    @Slot()
    def start_tts(self):
        self.tts.finished.connect(self.thread_finished)
        self.tts.start()

    def update_list_widget(self, text):
        item = QListWidgetItem(text)
        self.ui.listWidget.addItem(item)

    def thread_finished(self):
        self.tts.quit()
        self.tts.wait()
