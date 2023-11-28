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
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

class Ui_ConfigWindow(object):
    def setupUi(self, ConfigWindow):
        if not ConfigWindow.objectName():
            ConfigWindow.setObjectName(u"ConfigWindow")
        ConfigWindow.resize(471, 269)
        ConfigWindow.setMaximumSize(QSize(471, 289))
        self.centralWidget = QWidget(ConfigWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, -1, -1, 0)
        self.label = QLabel(self.centralWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 5, 0, 1, 1, Qt.AlignBottom)

        self.label_3 = QLabel(self.centralWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1, Qt.AlignBottom)

        self.targetChannel = QLineEdit(self.centralWidget)
        self.targetChannel.setObjectName(u"targetChannel")

        self.gridLayout.addWidget(self.targetChannel, 6, 0, 1, 1)

        self.label_2 = QLabel(self.centralWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1, Qt.AlignBottom)

        self.appSecret = QLineEdit(self.centralWidget)
        self.appSecret.setObjectName(u"appSecret")

        self.gridLayout.addWidget(self.appSecret, 3, 0, 1, 1)

        self.appID = QLineEdit(self.centralWidget)
        self.appID.setObjectName(u"appID")

        self.gridLayout.addWidget(self.appID, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.closeButton = QPushButton(self.centralWidget)
        self.closeButton.setObjectName(u"closeButton")

        self.horizontalLayout.addWidget(self.closeButton)

        self.cancelButton = QPushButton(self.centralWidget)
        self.cancelButton.setObjectName(u"cancelButton")

        self.horizontalLayout.addWidget(self.cancelButton)


        self.gridLayout.addLayout(self.horizontalLayout, 7, 0, 1, 1)

        ConfigWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QStatusBar(ConfigWindow)
        self.statusBar.setObjectName(u"statusBar")
        ConfigWindow.setStatusBar(self.statusBar)
        self.menuBar = QMenuBar(ConfigWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 471, 20))
        self.menuConfigure = QMenu(self.menuBar)
        self.menuConfigure.setObjectName(u"menuConfigure")
        ConfigWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuConfigure.menuAction())

        self.retranslateUi(ConfigWindow)

        QMetaObject.connectSlotsByName(ConfigWindow)
    # setupUi

    def retranslateUi(self, ConfigWindow):
        ConfigWindow.setWindowTitle(QCoreApplication.translate("ConfigWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("ConfigWindow", u"Target Channel", None))
        self.label_3.setText(QCoreApplication.translate("ConfigWindow", u"AppID", None))
#if QT_CONFIG(tooltip)
        self.targetChannel.setToolTip(QCoreApplication.translate("ConfigWindow", u"<html><head/><body><p>This can be any channel you want</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.targetChannel.setText("")
        self.label_2.setText(QCoreApplication.translate("ConfigWindow", u"App Secret", None))
        self.appSecret.setText("")
        self.appID.setText("")
        self.closeButton.setText(QCoreApplication.translate("ConfigWindow", u"Done", None))
        self.cancelButton.setText(QCoreApplication.translate("ConfigWindow", u"Cancel", None))
        self.menuConfigure.setTitle(QCoreApplication.translate("ConfigWindow", u"Configure", None))
    # retranslateUi

