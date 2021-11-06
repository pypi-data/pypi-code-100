# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/dylanbespalko/repos/sknrf-core-dev/sknrf/view/desktop/runtime/src/QRuntime.ui',
# licensing of '/Users/dylanbespalko/repos/sknrf-core-dev/sknrf/view/desktop/runtime/src/QRuntime.ui' applies.
#
# Created: Thu Jun  6 19:41:00 2019
#      by: pyside2-uic  running on PySide2 5.12.3
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_runtime(object):
    def setupUi(self, runtime):
        runtime.setObjectName("runtime")
        runtime.resize(1647, 765)
        runtime.setStyleSheet("")
        runtime.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QtWidgets.QWidget(runtime)
        self.centralwidget.setObjectName("centralwidget")
        runtime.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(runtime)
        self.statusbar.setObjectName("statusbar")
        runtime.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(runtime)
        self.toolBar.setStyleSheet("")
        self.toolBar.setMovable(True)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        runtime.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionStop = QtWidgets.QAction(runtime)
        self.actionStop.setCheckable(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/PNG/black/32/circled_stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/PNG/red/32/circled_stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionStop.setIcon(icon)
        self.actionStop.setObjectName("actionStop")
        self.actionPause = QtWidgets.QAction(runtime)
        self.actionPause.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/PNG/black/32/circled_pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/PNG/red/32/circled_pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionPause.setIcon(icon1)
        self.actionPause.setObjectName("actionPause")
        self.actionRun = QtWidgets.QAction(runtime)
        self.actionRun.setCheckable(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/PNG/black/32/circled_border_triangle_right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/PNG/green/32/circled_border_triangle_right.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionRun.setIcon(icon2)
        self.actionRun.setObjectName("actionRun")
        self.actionSingle = QtWidgets.QAction(runtime)
        self.actionSingle.setCheckable(True)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/PNG/black/32/circled_next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon3.addPixmap(QtGui.QPixmap(":/PNG/green/32/circled_next.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionSingle.setIcon(icon3)
        self.actionSingle.setObjectName("actionSingle")
        self.toolBar.addAction(self.actionRun)
        self.toolBar.addAction(self.actionSingle)
        self.toolBar.addAction(self.actionPause)
        self.toolBar.addAction(self.actionStop)

        self.retranslateUi(runtime)
        QtCore.QMetaObject.connectSlotsByName(runtime)

    def retranslateUi(self, runtime):
        runtime.setWindowTitle(QtWidgets.QApplication.translate("runtime", "MainWindow", None, -1))
        self.toolBar.setWindowTitle(QtWidgets.QApplication.translate("runtime", "toolBar", None, -1))
        self.actionStop.setText(QtWidgets.QApplication.translate("runtime", "Stop", None, -1))
        self.actionStop.setShortcut(QtWidgets.QApplication.translate("runtime", "Esc", None, -1))
        self.actionPause.setText(QtWidgets.QApplication.translate("runtime", "Pause", None, -1))
        self.actionPause.setShortcut(QtWidgets.QApplication.translate("runtime", "Space", None, -1))
        self.actionRun.setText(QtWidgets.QApplication.translate("runtime", "Run", None, -1))
        self.actionRun.setToolTip(QtWidgets.QApplication.translate("runtime", "Run", None, -1))
        self.actionRun.setShortcut(QtWidgets.QApplication.translate("runtime", "F9", None, -1))
        self.actionSingle.setText(QtWidgets.QApplication.translate("runtime", "Single", None, -1))
        self.actionSingle.setShortcut(QtWidgets.QApplication.translate("runtime", "F8", None, -1))

from sknrf.icons import black_32_rc
