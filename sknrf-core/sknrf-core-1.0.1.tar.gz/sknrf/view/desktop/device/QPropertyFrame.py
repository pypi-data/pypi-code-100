# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/dylanbespalko/repos/sknrf-core-dev/sknrf/view/desktop/device/src/QPropertyFrame.ui',
# licensing of '/Users/dylanbespalko/repos/sknrf-core-dev/sknrf/view/desktop/device/src/QPropertyFrame.ui' applies.
#
# Created: Fri May 24 12:43:36 2019
#      by: pyside2-uic  running on PySide2 5.12.1a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_propertyFrame(object):
    def setupUi(self, propertyFrame):
        propertyFrame.setObjectName("propertyFrame")
        propertyFrame.resize(400, 300)
        propertyFrame.setFrameShape(QtWidgets.QFrame.WinPanel)
        propertyFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.verticalLayout = QtWidgets.QVBoxLayout(propertyFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.propertyTabWidget = QtWidgets.QTabWidget(propertyFrame)
        self.propertyTabWidget.setObjectName("propertyTabWidget")
        self.propertyTab = QtWidgets.QWidget()
        self.propertyTab.setObjectName("propertyTab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.propertyTab)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.propertyTable = PropertyScrollArea(self.propertyTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.propertyTable.sizePolicy().hasHeightForWidth())
        self.propertyTable.setSizePolicy(sizePolicy)
        self.propertyTable.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.propertyTable.setObjectName("propertyTable")
        self.verticalLayout_5.addWidget(self.propertyTable)
        self.propertyTabWidget.addTab(self.propertyTab, "")
        self.limitTab = QtWidgets.QWidget()
        self.limitTab.setObjectName("limitTab")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.limitTab)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        spacerItem = QtWidgets.QSpacerItem(20, 694, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem)
        self.propertyTabWidget.addTab(self.limitTab, "")
        self.optimizationTab = QtWidgets.QWidget()
        self.optimizationTab.setObjectName("optimizationTab")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.optimizationTab)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        spacerItem1 = QtWidgets.QSpacerItem(20, 694, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem1)
        self.propertyTabWidget.addTab(self.optimizationTab, "")
        self.displayTab = QtWidgets.QWidget()
        self.displayTab.setObjectName("displayTab")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.displayTab)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        spacerItem2 = QtWidgets.QSpacerItem(20, 694, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem2)
        self.propertyTabWidget.addTab(self.displayTab, "")
        self.verticalLayout.addWidget(self.propertyTabWidget)

        self.retranslateUi(propertyFrame)
        self.propertyTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(propertyFrame)

    def retranslateUi(self, propertyFrame):
        propertyFrame.setWindowTitle(QtWidgets.QApplication.translate("propertyFrame", "Frame", None, -1))
        self.propertyTable.setToolTip(QtWidgets.QApplication.translate("propertyFrame", "Property Browser", None, -1))
        self.propertyTable.setWhatsThis(QtWidgets.QApplication.translate("propertyFrame", "The Property Browser Controls Table Properties", None, -1))
        self.propertyTabWidget.setTabText(self.propertyTabWidget.indexOf(self.propertyTab), QtWidgets.QApplication.translate("propertyFrame", "Properties", None, -1))
        self.propertyTabWidget.setTabText(self.propertyTabWidget.indexOf(self.limitTab), QtWidgets.QApplication.translate("propertyFrame", "Limits", None, -1))
        self.propertyTabWidget.setTabText(self.propertyTabWidget.indexOf(self.optimizationTab), QtWidgets.QApplication.translate("propertyFrame", "Optimization", None, -1))
        self.propertyTabWidget.setTabText(self.propertyTabWidget.indexOf(self.displayTab), QtWidgets.QApplication.translate("propertyFrame", "Display", None, -1))

from sknrf.widget.propertybrowser.view.base import PropertyScrollArea
