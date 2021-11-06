# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QLauncherSideView.ui',
# licensing of 'QLauncherSideView.ui' applies.
#
# Created: Sun Jan 13 09:32:43 2019
#      by: pyside2-uic  running on PySide2 5.12.1a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_launcherSideViewFrame(object):
    def setupUi(self, launcherSideViewFrame):
        launcherSideViewFrame.setObjectName("launcherSideViewFrame")
        launcherSideViewFrame.resize(516, 670)
        launcherSideViewFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        launcherSideViewFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.verticalLayout = QtWidgets.QVBoxLayout(launcherSideViewFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter_5 = QtWidgets.QSplitter(launcherSideViewFrame)
        self.splitter_5.setOrientation(QtCore.Qt.Vertical)
        self.splitter_5.setObjectName("splitter_5")
        self.actionTabWidget = QtWidgets.QTabWidget(self.splitter_5)
        self.actionTabWidget.setObjectName("actionTabWidget")
        self.infoEdit = QtWidgets.QTextEdit(self.splitter_5)
        self.infoEdit.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.infoEdit.setFont(font)
        self.infoEdit.setReadOnly(True)
        self.infoEdit.setObjectName("infoEdit")
        self.verticalLayout.addWidget(self.splitter_5)

        self.retranslateUi(launcherSideViewFrame)
        self.actionTabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(launcherSideViewFrame)

    def retranslateUi(self, launcherSideViewFrame):
        launcherSideViewFrame.setWindowTitle(QtWidgets.QApplication.translate("launcherSideViewFrame", "Frame", None, -1))

