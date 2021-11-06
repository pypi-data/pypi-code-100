# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QLauncherMenu.ui',
# licensing of 'QLauncherMenu.ui' applies.
#
# Created: Mon Jan 14 10:47:42 2019
#      by: pyside2-uic  running on PySide2 5.12.1a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_launcherMenu(object):
    def setupUi(self, launcherMenu):
        launcherMenu.setObjectName("launcherMenu")
        launcherMenu.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(launcherMenu)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        launcherMenu.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        launcherMenu.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(launcherMenu)
        self.statusbar.setObjectName("statusbar")
        launcherMenu.setStatusBar(self.statusbar)

        self.retranslateUi(launcherMenu)
        QtCore.QMetaObject.connectSlotsByName(launcherMenu)

    def retranslateUi(self, launcherMenu):
        launcherMenu.setWindowTitle(QtWidgets.QApplication.translate("launcherMenu", "MainWindow", None, -1))

