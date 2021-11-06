# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/dylanbespalko/repos/sknrf-core-dev/sknrf/view/desktop/runtime/src/QRuntimePortFrame.ui',
# licensing of '/Users/dylanbespalko/repos/sknrf-core-dev/sknrf/view/desktop/runtime/src/QRuntimePortFrame.ui' applies.
#
# Created: Thu Jun  6 08:41:31 2019
#      by: pyside2-uic  running on PySide2 5.12.3
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_runtimePortFrame(object):
    def setupUi(self, runtimePortFrame):
        runtimePortFrame.setObjectName("runtimePortFrame")
        runtimePortFrame.resize(780, 931)
        runtimePortFrame.setFrameShape(QtWidgets.QFrame.WinPanel)
        runtimePortFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.verticalLayout = QtWidgets.QVBoxLayout(runtimePortFrame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.portLabel = QtWidgets.QLabel(runtimePortFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.portLabel.sizePolicy().hasHeightForWidth())
        self.portLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(32)
        font.setWeight(75)
        font.setItalic(False)
        font.setBold(True)
        self.portLabel.setFont(font)
        self.portLabel.setStyleSheet("")
        self.portLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.portLabel.setObjectName("portLabel")
        self.verticalLayout.addWidget(self.portLabel)
        self.meterFrame = QtWidgets.QFrame(runtimePortFrame)
        self.meterFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.meterFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.meterFrame.setObjectName("meterFrame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.meterFrame)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout.addWidget(self.meterFrame)
        self.previewPlotWidget = ContentFigure(runtimePortFrame)
        self.previewPlotWidget.setObjectName("previewPlotWidget")
        self.verticalLayout.addWidget(self.previewPlotWidget)

        self.retranslateUi(runtimePortFrame)
        QtCore.QMetaObject.connectSlotsByName(runtimePortFrame)

    def retranslateUi(self, runtimePortFrame):
        runtimePortFrame.setWindowTitle(QtWidgets.QApplication.translate("runtimePortFrame", "Frame", None, -1))
        self.portLabel.setText(QtWidgets.QApplication.translate("runtimePortFrame", "Port 1:", None, -1))

from sknrf.app.dataviewer.view.figure import ContentFigure
