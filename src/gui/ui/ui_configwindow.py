# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize)
from PySide6.QtWidgets import (QCheckBox, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy, QStatusBar, QVBoxLayout,
    QWidget)


class Ui_ConfigWindow(object):
    def setupUi(self, ConfigWindow):
        if not ConfigWindow.objectName():
            ConfigWindow.setObjectName(u"ConfigWindow")
        ConfigWindow.resize(471, 430)
        ConfigWindow.setMinimumSize(QSize(471, 430))
        self.centralWidget = QWidget(ConfigWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.ChannelText = QLabel(self.centralWidget)
        self.ChannelText.setObjectName(u"ChannelText")
        self.verticalLayout.addWidget(self.ChannelText)

        self.targetChannel = QLineEdit(self.centralWidget)
        self.targetChannel.setObjectName(u"targetChannel")
        self.verticalLayout.addWidget(self.targetChannel)

        self.pronounciationText = QLabel(self.centralWidget)
        self.pronounciationText.setObjectName(u"pronounciationText")
        self.verticalLayout.addWidget(self.pronounciationText)

        self.pronounciation = QLineEdit(self.centralWidget)
        self.pronounciation.setObjectName(u"pronounciation")
        self.verticalLayout.addWidget(self.pronounciation)

        self.IgnorelistText = QLabel(self.centralWidget)
        self.IgnorelistText.setObjectName(u"IgnorelistText")
        self.verticalLayout.addWidget(self.IgnorelistText)

        self.ignorelist = QLineEdit(self.centralWidget)
        self.ignorelist.setObjectName(u"ignorelist")
        self.verticalLayout.addWidget(self.ignorelist)

        self.voiceModelText = QLabel(self.centralWidget)
        self.voiceModelText.setObjectName(u"voiceModelText")
        self.verticalLayout.addWidget(self.voiceModelText)

        self.voiceModel = QLineEdit(self.centralWidget)
        self.voiceModel.setObjectName(u"voiceModel")
        self.verticalLayout.addWidget(self.voiceModel)

        self.skipCommandText = QLabel(self.centralWidget)
        self.skipCommandText.setObjectName(u"skipCommandText")
        self.verticalLayout.addWidget(self.skipCommandText)

        self.skipCommand = QLineEdit(self.centralWidget)
        self.skipCommand.setObjectName(u"skipCommand")
        self.verticalLayout.addWidget(self.skipCommand)

        self.modOnlySkip = QCheckBox(self.centralWidget)
        self.modOnlySkip.setObjectName(u"modOnlySkip")
        self.modOnlySkip.setChecked(True)
        self.verticalLayout.addWidget(self.modOnlySkip)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 20, -1, -1)

        self.closeButton = QPushButton(self.centralWidget)
        self.closeButton.setObjectName(u"closeButton")
        self.horizontalLayout.addWidget(self.closeButton)

        self.cancelButton = QPushButton(self.centralWidget)
        self.cancelButton.setObjectName(u"cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        ConfigWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QStatusBar(ConfigWindow)
        self.statusBar.setObjectName(u"statusBar")
        ConfigWindow.setStatusBar(self.statusBar)

        self.retranslateUi(ConfigWindow)

        QMetaObject.connectSlotsByName(ConfigWindow)
    # setupUi

    def retranslateUi(self, ConfigWindow):
        ConfigWindow.setWindowTitle(QCoreApplication.translate("ConfigWindow", u"Configure", None))
        self.ChannelText.setText(QCoreApplication.translate("ConfigWindow", u"Channel", None))
        self.pronounciationText.setText(QCoreApplication.translate("ConfigWindow", u"Pronounciation (use {username} and {message})", None))
        self.IgnorelistText.setText(QCoreApplication.translate("ConfigWindow", u"Ignorelist (comma separated usernames)", None))
        self.voiceModelText.setText(QCoreApplication.translate("ConfigWindow", u"Voice model (Piper voice name)", None))
        self.skipCommandText.setText(QCoreApplication.translate("ConfigWindow", u"Mod skip command (without the ! prefix)", None))
        self.modOnlySkip.setText(QCoreApplication.translate("ConfigWindow", u"Only allow moderators/broadcaster to use the skip command", None))
        self.closeButton.setText(QCoreApplication.translate("ConfigWindow", u"Done", None))
        self.cancelButton.setText(QCoreApplication.translate("ConfigWindow", u"Cancel", None))
    # retranslateUi
