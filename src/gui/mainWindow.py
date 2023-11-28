from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QListWidgetItem

from src.gui.configWindow import ConfigWindow
from src.gui.ui.ui_mainwindow import Ui_MainWindow

from src.TTSengine.TTS import UpdateListWorker, TTS
import json
import os

config_file_path = "config.json"


def check_config():
    if not os.path.isfile(config_file_path):
        print("No config file found, creating one...")
        with open(config_file_path, 'w') as f:
            json.dump({"AppID": "", "AppSecret": "", "Channel": ""}, f, indent=4)
            f.close()


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        check_config()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.startButton.clicked.connect(self.start_tts)
        self.ui.configButton.clicked.connect(self.open_config_window)

        self.worker = UpdateListWorker()
        self.tts = TTS(self.worker)
        self.worker.item_added.connect(self.update_list_widget)

        self.tts.ready.connect(self.ready)
        
        self.config_window = None

    @Slot()
    def open_config_window(self):
        if not self.config_window or not self.config_window.isVisible():
            self.config_window = ConfigWindow(self)
            self.config_window.show()

    @Slot()
    def start_tts(self):
        # This is probably not the best solution to this, but it seems to be working perfectly fine.
        if self.tts.isRunning():
            self.ui.startButton.setText("stopping...")
            self.ui.startButton.setEnabled(False)
            self.tts.stop_request.emit()
            self.tts.wait()
            self.ui.startButton.setText("start")
            self.ui.startButton.setEnabled(True)
            self.ui.configButton.setEnabled(True)
        else:
            self.ui.startButton.setText("stop")
            self.ui.startButton.setEnabled(False)
            self.ui.configButton.setEnabled(False)
            self.tts.start()

    def update_list_widget(self, text):
        item = QListWidgetItem(text)
        self.ui.listWidget.addItem(item)

    def ready(self):
        self.ui.startButton.setText("stop")
        self.ui.startButton.setEnabled(True)

