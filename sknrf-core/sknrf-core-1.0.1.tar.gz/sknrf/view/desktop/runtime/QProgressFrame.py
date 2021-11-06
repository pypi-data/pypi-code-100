# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QProgressFrame.ui',
# licensing of 'QProgressFrame.ui' applies.
#
# Created: Mon Jan 14 11:09:23 2019
#      by: pyside2-uic  running on PySide2 5.12.1a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_progressFrame(object):
    def setupUi(self, progressFrame):
        progressFrame.setObjectName("progressFrame")
        progressFrame.resize(517, 827)
        progressFrame.setFrameShape(QtWidgets.QFrame.WinPanel)
        progressFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(progressFrame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.progressLabel = QtWidgets.QLabel(progressFrame)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.progressLabel.setFont(font)
        self.progressLabel.setStyleSheet("")
        self.progressLabel.setObjectName("progressLabel")
        self.verticalLayout_2.addWidget(self.progressLabel)
        self.tabWidget = QtWidgets.QTabWidget(progressFrame)
        self.tabWidget.setObjectName("tabWidget")
        self.sweepTab = QtWidgets.QWidget()
        self.sweepTab.setObjectName("sweepTab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.sweepTab)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.sweepTab)
        self.scrollArea.setStyleSheet("")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 481, 742))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.tabWidget.addTab(self.sweepTab, "")
        self.optimizationTab = QtWidgets.QWidget()
        self.optimizationTab.setObjectName("optimizationTab")
        self.tabWidget.addTab(self.optimizationTab, "")
        self.verticalLayout_2.addWidget(self.tabWidget)

        self.retranslateUi(progressFrame)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(progressFrame)

    def retranslateUi(self, progressFrame):
        progressFrame.setWindowTitle(QtWidgets.QApplication.translate("progressFrame", "Frame", None, -1))
        self.progressLabel.setText(QtWidgets.QApplication.translate("progressFrame", "Progress:", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.sweepTab), QtWidgets.QApplication.translate("progressFrame", "Sweep", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.optimizationTab), QtWidgets.QApplication.translate("progressFrame", "Optimization", None, -1))

