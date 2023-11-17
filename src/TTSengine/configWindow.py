from PySide6.QtCore import Slot, QThread, Signal, QObject
from PySide6.QtWidgets import QMainWindow, QListWidgetItem

from src.gui.ui_configwindow import Ui_ConfigWindow


class ConfigWindow(QMainWindow, Ui_ConfigWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ConfigWindow()
        self.ui.setupUi(self)
        self.show()

        self.ui.closeButton.clicked.connect(self.closeEvent)

    def closeEvent(self, event):
        appID = self.ui.appID.text()
        appSecret = self.ui.appSecret.text()
        channel = self.ui.targetChannel.text()
        with open('config.json', 'w') as f:
            f.write('{\n"AppID": "' + appID + '",\n "AppSecret": "' + appSecret + '",\n "Channel": "' + channel + '"\n}')
        print(self.ui.appID.text())
        self.close()
