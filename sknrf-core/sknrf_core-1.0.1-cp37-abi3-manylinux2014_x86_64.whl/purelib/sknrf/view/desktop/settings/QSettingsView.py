# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QSettingsView.ui',
# licensing of 'QSettingsView.ui' applies.
#
# Created: Sun Feb 21 18:56:18 2021
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_settingsView(object):
    def setupUi(self, settingsView):
        settingsView.setObjectName("settingsView")
        settingsView.resize(509, 461)
        self.centralwidget = QtWidgets.QWidget(settingsView)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.mainTab = QtWidgets.QWidget()
        self.mainTab.setObjectName("mainTab")
        self.tabWidget.addTab(self.mainTab, "")
        self.generalTab = QtWidgets.QWidget()
        self.generalTab.setObjectName("generalTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.generalTab)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.propertyTable = PropertyScrollArea(self.generalTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.propertyTable.sizePolicy().hasHeightForWidth())
        self.propertyTable.setSizePolicy(sizePolicy)
        self.propertyTable.setObjectName("propertyTable")
        self.verticalLayout_2.addWidget(self.propertyTable)
        self.tabWidget.addTab(self.generalTab, "")
        self.appTab = QtWidgets.QWidget()
        self.appTab.setObjectName("appTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.appTab)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.appPropertyTable = PropertyScrollArea(self.appTab)
        self.appPropertyTable.setObjectName("appPropertyTable")
        self.verticalLayout_3.addWidget(self.appPropertyTable)
        self.tabWidget.addTab(self.appTab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        settingsView.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(settingsView)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 509, 26))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        settingsView.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(settingsView)
        self.toolBar.setObjectName("toolBar")
        settingsView.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionDocumentation = QtWidgets.QAction(settingsView)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/PNG/black/32/question_mark.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDocumentation.setIcon(icon)
        self.actionDocumentation.setObjectName("actionDocumentation")
        self.menuHelp.addAction(self.actionDocumentation)
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionDocumentation)

        self.retranslateUi(settingsView)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(settingsView)

    def retranslateUi(self, settingsView):
        settingsView.setWindowTitle(QtWidgets.QApplication.translate("settingsView", "MainWindow", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.mainTab), QtWidgets.QApplication.translate("settingsView", "Main", None, -1))
        self.propertyTable.setToolTip(QtWidgets.QApplication.translate("settingsView", "Property Browser", None, -1))
        self.propertyTable.setWhatsThis(QtWidgets.QApplication.translate("settingsView", "The Property Browser Controls Table Properties", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.generalTab), QtWidgets.QApplication.translate("settingsView", "General", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.appTab), QtWidgets.QApplication.translate("settingsView", "App", None, -1))
        self.menuHelp.setTitle(QtWidgets.QApplication.translate("settingsView", "Help", None, -1))
        self.toolBar.setWindowTitle(QtWidgets.QApplication.translate("settingsView", "toolBar", None, -1))
        self.actionDocumentation.setText(QtWidgets.QApplication.translate("settingsView", "Documentation", None, -1))

from sknrf.widget.propertybrowser.view.base import PropertyScrollArea
from sknrf.icons import black_32_rc
