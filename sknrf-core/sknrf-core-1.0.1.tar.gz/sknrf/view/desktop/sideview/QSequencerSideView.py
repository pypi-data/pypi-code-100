# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QSequencerSideView.ui',
# licensing of 'QSequencerSideView.ui' applies.
#
# Created: Sun Jan 13 09:32:43 2019
#      by: pyside2-uic  running on PySide2 5.12.1a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_sequencerSideViewFrame(object):
    def setupUi(self, sequencerSideViewFrame):
        sequencerSideViewFrame.setObjectName("sequencerSideViewFrame")
        sequencerSideViewFrame.resize(516, 670)
        sequencerSideViewFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        sequencerSideViewFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.verticalLayout = QtWidgets.QVBoxLayout(sequencerSideViewFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter_5 = QtWidgets.QSplitter(sequencerSideViewFrame)
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

        self.retranslateUi(sequencerSideViewFrame)
        self.actionTabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(sequencerSideViewFrame)

    def retranslateUi(self, sequencerSideViewFrame):
        sequencerSideViewFrame.setWindowTitle(QtWidgets.QApplication.translate("sequencerSideViewFrame", "Frame", None, -1))

