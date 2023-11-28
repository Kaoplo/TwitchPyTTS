import json

from PySide6.QtWidgets import QMainWindow

from src.gui.ui.ui_configwindow import Ui_ConfigWindow


class ConfigWindow(QMainWindow, Ui_ConfigWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ConfigWindow()
        self.ui.setupUi(self)
        self.show()

        self.ui.closeButton.clicked.connect(self.save)
        self.ui.cancelButton.clicked.connect(self.cancel)

        with open('config.json', 'r') as f:
            config = json.load(f)

        self.ui.appID.setText(config['AppID'])
        self.ui.appSecret.setText(config['AppSecret'])
        self.ui.targetChannel.setText(config['Channel'])
        f.close()

    def save(self):
        appID = self.ui.appID.text()
        appSecret = self.ui.appSecret.text()
        channel = self.ui.targetChannel.text()
        with open('config.json', 'w') as f:
            f.write('{\n"AppID": "' + appID + '",\n "AppSecret": "' + appSecret + '",\n "Channel": "' + channel + '"\n}')
        f.close()
        self.close()

    def cancel(self):
        self.close()
