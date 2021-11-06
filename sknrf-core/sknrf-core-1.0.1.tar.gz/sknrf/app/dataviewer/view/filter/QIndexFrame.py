# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QIndexFrame.ui',
# licensing of 'QIndexFrame.ui' applies.
#
# Created: Sat Jan 19 23:21:31 2019
#      by: pyside2-uic  running on PySide2 5.12.1a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_indexFrame(object):
    def setupUi(self, indexFrame):
        indexFrame.setObjectName("indexFrame")
        indexFrame.resize(389, 789)
        indexFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        indexFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.verticalLayout = QtWidgets.QVBoxLayout(indexFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toolbarFrame = QtWidgets.QFrame(indexFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolbarFrame.sizePolicy().hasHeightForWidth())
        self.toolbarFrame.setSizePolicy(sizePolicy)
        self.toolbarFrame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.toolbarFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.toolbarFrame.setObjectName("toolbarFrame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.toolbarFrame)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.markerToolButton = QtWidgets.QToolButton(self.toolbarFrame)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/PNG/black/32/pin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.markerToolButton.setIcon(icon)
        self.markerToolButton.setIconSize(QtCore.QSize(24, 24))
        self.markerToolButton.setCheckable(True)
        self.markerToolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.markerToolButton.setAutoRaise(True)
        self.markerToolButton.setObjectName("markerToolButton")
        self.horizontalLayout_3.addWidget(self.markerToolButton)
        self.clearToolButton = QtWidgets.QToolButton(self.toolbarFrame)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/PNG/black/32/cancel-circle.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clearToolButton.setIcon(icon1)
        self.clearToolButton.setIconSize(QtCore.QSize(24, 24))
        self.clearToolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.clearToolButton.setAutoRaise(True)
        self.clearToolButton.setObjectName("clearToolButton")
        self.horizontalLayout_3.addWidget(self.clearToolButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addWidget(self.toolbarFrame)
        self.filtersToolbox = QtWidgets.QToolBox(indexFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filtersToolbox.sizePolicy().hasHeightForWidth())
        self.filtersToolbox.setSizePolicy(sizePolicy)
        self.filtersToolbox.setObjectName("filtersToolbox")
        self.filter1 = QtWidgets.QWidget()
        self.filter1.setGeometry(QtCore.QRect(0, 0, 363, 311))
        self.filter1.setObjectName("filter1")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.filter1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.filtersToolbox.addItem(self.filter1, "")
        self.verticalLayout.addWidget(self.filtersToolbox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(indexFrame)
        self.filtersToolbox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(indexFrame)
        indexFrame.setTabOrder(self.markerToolButton, self.clearToolButton)

    def retranslateUi(self, indexFrame):
        indexFrame.setWindowTitle(QtWidgets.QApplication.translate("indexFrame", "Frame", None, -1))
        self.markerToolButton.setToolTip(QtWidgets.QApplication.translate("indexFrame", "Undo", None, -1))
        self.markerToolButton.setText(QtWidgets.QApplication.translate("indexFrame", "Marker", None, -1))
        self.clearToolButton.setToolTip(QtWidgets.QApplication.translate("indexFrame", "Clear", None, -1))
        self.clearToolButton.setText(QtWidgets.QApplication.translate("indexFrame", "Clear", None, -1))
        self.filtersToolbox.setItemText(self.filtersToolbox.indexOf(self.filter1), QtWidgets.QApplication.translate("indexFrame", "No Filters", None, -1))

from sknrf.icons import black_32_rc
