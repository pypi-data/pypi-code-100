# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/dylanbespalko/repos/sknrf-core-dev/sknrf/view/desktop/runtime/src/QBusyFrame.ui',
# licensing of '/Users/dylanbespalko/repos/sknrf-core-dev/sknrf/view/desktop/runtime/src/QBusyFrame.ui' applies.
#
# Created: Fri May 31 10:02:43 2019
#      by: pyside2-uic  running on PySide2 5.12.1a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_busyFrame(object):
    def setupUi(self, busyFrame):
        busyFrame.setObjectName("busyFrame")
        busyFrame.resize(400, 300)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        busyFrame.setFont(font)
        busyFrame.setAutoFillBackground(False)
        busyFrame.setStyleSheet("")
        busyFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        busyFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.verticalLayout = QtWidgets.QVBoxLayout(busyFrame)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.busyIndicator = QProgressIndicator(busyFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.busyIndicator.sizePolicy().hasHeightForWidth())
        self.busyIndicator.setSizePolicy(sizePolicy)
        self.busyIndicator.setMaximumSize(QtCore.QSize(250, 250))
        self.busyIndicator.setProperty("displayedWhenStopped", True)
        self.busyIndicator.setObjectName("busyIndicator")
        self.horizontalLayout_2.addWidget(self.busyIndicator)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.label = QtWidgets.QLabel(busyFrame)
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem5 = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)

        self.retranslateUi(busyFrame)
        QtCore.QMetaObject.connectSlotsByName(busyFrame)

    def retranslateUi(self, busyFrame):
        busyFrame.setWindowTitle(QtWidgets.QApplication.translate("busyFrame", "Frame", None, -1))
        self.busyIndicator.setToolTip(QtWidgets.QApplication.translate("busyFrame", "Progress Indicator", None, -1))
        self.busyIndicator.setWhatsThis(QtWidgets.QApplication.translate("busyFrame", "The Progress Indicator indicates the system is busy", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("busyFrame", "Loading...", None, -1))

from sknrf.widget.progressindicator.view import QProgressIndicator
