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
    QPushButton, QSizePolicy, QStatusBar, QTabWidget,
    QVBoxLayout, QWidget)

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
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, -1, -1, 0)
        self.tabWidget = QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.widget = QWidget(self.tab)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(-1, -1, 451, 171))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)

        self.verticalLayout.addWidget(self.label_3)

        self.appID = QLineEdit(self.widget)
        self.appID.setObjectName(u"appID")

        self.verticalLayout.addWidget(self.appID)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)

        self.verticalLayout.addWidget(self.label_2)

        self.appSecret = QLineEdit(self.widget)
        self.appSecret.setObjectName(u"appSecret")

        self.verticalLayout.addWidget(self.appSecret)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)

        self.verticalLayout.addWidget(self.label)

        self.targetChannel = QLineEdit(self.widget)
        self.targetChannel.setObjectName(u"targetChannel")

        self.verticalLayout.addWidget(self.targetChannel)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayoutWidget = QWidget(self.tab_2)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 451, 171))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.prounciatioLabel = QLabel(self.verticalLayoutWidget)
        self.prounciatioLabel.setObjectName(u"prounciatioLabel")
        self.prounciatioLabel.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)

        self.verticalLayout_2.addWidget(self.prounciatioLabel)

        self.pronounciation = QLineEdit(self.verticalLayoutWidget)
        self.pronounciation.setObjectName(u"pronounciation")

        self.verticalLayout_2.addWidget(self.pronounciation)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.closeButton = QPushButton(self.centralWidget)
        self.closeButton.setObjectName(u"closeButton")

        self.horizontalLayout.addWidget(self.closeButton)

        self.cancelButton = QPushButton(self.centralWidget)
        self.cancelButton.setObjectName(u"cancelButton")

        self.horizontalLayout.addWidget(self.cancelButton)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

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

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ConfigWindow)
    # setupUi

    def retranslateUi(self, ConfigWindow):
        ConfigWindow.setWindowTitle(QCoreApplication.translate("ConfigWindow", u"MainWindow", None))
        self.actionjkl.setText(QCoreApplication.translate("ConfigWindow", u"jkl;", None))
        self.label_3.setText(QCoreApplication.translate("ConfigWindow", u"AppID", None))
        self.appID.setText("")
        self.label_2.setText(QCoreApplication.translate("ConfigWindow", u"App Secret", None))
        self.appSecret.setText("")
        self.label.setText(QCoreApplication.translate("ConfigWindow", u"Target Channel", None))
#if QT_CONFIG(tooltip)
        self.targetChannel.setToolTip(QCoreApplication.translate("ConfigWindow", u"<html><head/><body><p>This can be any channel you want</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.targetChannel.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("ConfigWindow", u"Tab 1", None))
        self.prounciatioLabel.setText(QCoreApplication.translate("ConfigWindow", u"TextLabel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("ConfigWindow", u"Tab 2", None))
        self.closeButton.setText(QCoreApplication.translate("ConfigWindow", u"Done", None))
        self.cancelButton.setText(QCoreApplication.translate("ConfigWindow", u"Cancel", None))
        self.menuConfigure.setTitle(QCoreApplication.translate("ConfigWindow", u"Configure", None))
    # retranslateUi

