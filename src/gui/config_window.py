from __future__ import annotations

from PySide6.QtWidgets import QMainWindow

from src.app_config import AppConfig
from src.gui.ui.ui_configwindow import Ui_ConfigWindow


class ConfigWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ConfigWindow()
        self.ui.setupUi(self)

        self.ui.closeButton.clicked.connect(self.save)
        self.ui.cancelButton.clicked.connect(self.close)

        self.config = AppConfig.load()
        self.ui.targetChannel.setText(self.config.channel)
        self.ui.pronounciation.setText(self.config.pronunciation)
        self.ui.ignorelist.setText(", ".join(self.config.ignore_list))
        self.ui.voiceModel.setText(self.config.voice_model)
        self.ui.skipCommand.setText(self.config.skip_command)
        self.ui.modOnlySkip.setChecked(self.config.mod_only_skip)

    def save(self):
        self.config.channel = self.ui.targetChannel.text().strip()
        self.config.pronunciation = self.ui.pronounciation.text() or self.config.pronunciation
        self.config.ignore_list = [
            name.strip() for name in self.ui.ignorelist.text().split(",") if name.strip()
        ]
        self.config.voice_model = self.ui.voiceModel.text().strip() or self.config.voice_model
        self.config.skip_command = self.ui.skipCommand.text().strip() or self.config.skip_command
        self.config.mod_only_skip = self.ui.modOnlySkip.isChecked()
        self.config.save()
        self.close()
