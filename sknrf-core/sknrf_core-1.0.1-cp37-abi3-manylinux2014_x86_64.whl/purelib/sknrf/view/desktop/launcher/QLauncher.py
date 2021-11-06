# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QLauncher.ui',
# licensing of 'QLauncher.ui' applies.
#
# Created: Mon Jan 14 10:47:42 2019
#      by: pyside2-uic  running on PySide2 5.12.1a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_launcherFrame(object):
    def setupUi(self, launcherFrame):
        launcherFrame.setObjectName("launcherFrame")
        launcherFrame.resize(803, 551)
        launcherFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        launcherFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.verticalLayout = QtWidgets.QVBoxLayout(launcherFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.iconGridLayout = QtWidgets.QGridLayout()
        self.iconGridLayout.setObjectName("iconGridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.iconGridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.iconGridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(launcherFrame)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Open)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(launcherFrame)
        QtCore.QMetaObject.connectSlotsByName(launcherFrame)

    def retranslateUi(self, launcherFrame):
        launcherFrame.setWindowTitle(QtWidgets.QApplication.translate("launcherFrame", "Frame", None, -1))

