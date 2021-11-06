# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QDeviceMenuView.ui',
# licensing of 'QDeviceMenuView.ui' applies.
#
# Created: Sat Jan 12 19:35:02 2019
#      by: pyside2-uic  running on PySide2 5.12.1a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_deviceMenuView(object):
    def setupUi(self, deviceMenuView):
        deviceMenuView.setObjectName("deviceMenuView")
        deviceMenuView.resize(1600, 900)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(deviceMenuView.sizePolicy().hasHeightForWidth())
        deviceMenuView.setSizePolicy(sizePolicy)
        deviceMenuView.setMinimumSize(QtCore.QSize(1600, 900))
        deviceMenuView.setMaximumSize(QtCore.QSize(2880, 1800))
        deviceMenuView.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(deviceMenuView)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMaximumSize(QtCore.QSize(2880, 1800))
        self.centralwidget.setSizeIncrement(QtCore.QSize(0, 0))
        self.centralwidget.setObjectName("centralwidget")
        deviceMenuView.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1600, 22))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuRun = QtWidgets.QMenu(self.menubar)
        self.menuRun.setObjectName("menuRun")
        deviceMenuView.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(deviceMenuView)
        self.statusbar.setObjectName("statusbar")
        deviceMenuView.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(deviceMenuView)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        deviceMenuView.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionDocumentation = QtWidgets.QAction(deviceMenuView)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/PNG/black/32/question_mark.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDocumentation.setIcon(icon)
        self.actionDocumentation.setObjectName("actionDocumentation")
        self.actionSingle = QtWidgets.QAction(deviceMenuView)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/PNG/black/32/circled_border_triangle_right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/PNG/green/32/circled_border_triangle_right.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionSingle.setIcon(icon1)
        self.actionSingle.setObjectName("actionSingle")
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuRun.addAction(self.actionSingle)
        self.menubar.addAction(self.menuRun.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionDocumentation)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSingle)

        self.retranslateUi(deviceMenuView)
        QtCore.QMetaObject.connectSlotsByName(deviceMenuView)

    def retranslateUi(self, deviceMenuView):
        deviceMenuView.setWindowTitle(QtWidgets.QApplication.translate("deviceMenuView", "Device Menu", None, -1))
        self.menuHelp.setTitle(QtWidgets.QApplication.translate("deviceMenuView", "Help", None, -1))
        self.menuRun.setTitle(QtWidgets.QApplication.translate("deviceMenuView", "Run", None, -1))
        self.toolBar.setWindowTitle(QtWidgets.QApplication.translate("deviceMenuView", "toolBar", None, -1))
        self.actionDocumentation.setText(QtWidgets.QApplication.translate("deviceMenuView", "Documentation", None, -1))
        self.actionSingle.setText(QtWidgets.QApplication.translate("deviceMenuView", "Single", None, -1))

from sknrf.icons import black_32_rc
