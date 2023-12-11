# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_ConfigWindow(object):
    def setupUi(self, ConfigWindow):
        if not ConfigWindow.objectName():
            ConfigWindow.setObjectName(u"ConfigWindow")
        ConfigWindow.resize(471, 282)
        ConfigWindow.setMinimumSize(QSize(471, 282))
        ConfigWindow.setMaximumSize(QSize(471, 282))
        self.actionjkl = QAction(ConfigWindow)
        self.actionjkl.setObjectName(u"actionjkl")
        self.centralWidget = QWidget(ConfigWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(9, 9, 9, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.ChannelText = QLabel(self.centralWidget)
        self.ChannelText.setObjectName(u"ChannelText")
        self.ChannelText.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)

        self.verticalLayout.addWidget(self.ChannelText)

        self.targetChannel = QLineEdit(self.centralWidget)
        self.targetChannel.setObjectName(u"targetChannel")

        self.verticalLayout.addWidget(self.targetChannel)

        self.pronounciationText = QLabel(self.centralWidget)
        self.pronounciationText.setObjectName(u"pronounciationText")
        self.pronounciationText.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)

        self.verticalLayout.addWidget(self.pronounciationText)

        self.pronounciation = QLineEdit(self.centralWidget)
        self.pronounciation.setObjectName(u"pronounciation")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pronounciation.sizePolicy().hasHeightForWidth())
        self.pronounciation.setSizePolicy(sizePolicy)
        self.pronounciation.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout.addWidget(self.pronounciation)

        self.IgnorelistText = QLabel(self.centralWidget)
        self.IgnorelistText.setObjectName(u"IgnorelistText")
        self.IgnorelistText.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)

        self.verticalLayout.addWidget(self.IgnorelistText)

        self.ignorelist = QLineEdit(self.centralWidget)
        self.ignorelist.setObjectName(u"ignorelist")
        sizePolicy.setHeightForWidth(self.ignorelist.sizePolicy().hasHeightForWidth())
        self.ignorelist.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.ignorelist)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
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
        ConfigWindow.setWindowTitle(QCoreApplication.translate("ConfigWindow", u"MainWindow", None))
        self.actionjkl.setText(QCoreApplication.translate("ConfigWindow", u"jkl;", None))
        self.ChannelText.setText(QCoreApplication.translate("ConfigWindow", u"Channel", None))
        self.pronounciationText.setText(QCoreApplication.translate("ConfigWindow", u"Pronounciation", None))
        self.IgnorelistText.setText(QCoreApplication.translate("ConfigWindow", u"Ignorelist", None))
        self.closeButton.setText(QCoreApplication.translate("ConfigWindow", u"Done", None))
        self.cancelButton.setText(QCoreApplication.translate("ConfigWindow", u"Cancel", None))
    # retranslateUi

