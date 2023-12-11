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

        self.ui.targetChannel.setText(config['Channel'])
        self.ui.pronounciation.setText(config['pronunciation'])
        self.ui.ignorelist.setText(config['ignorelist'])
        f.close()

    def save(self):
        channel = self.ui.targetChannel.text()
        pronunciation = self.ui.pronounciation.text()
        ignorelist = self.ui.ignorelist.text()
        with open('config.json', 'w') as f:
            json.dump({"Channel": channel, "pronunciation": pronunciation, "ignorelist": ignorelist}, f, indent=4)
        f.close()
        self.close()

    def cancel(self):
        self.close()
