# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QLogSideView.ui',
# licensing of 'QLogSideView.ui' applies.
#
# Created: Sun Jan 13 09:32:42 2019
#      by: pyside2-uic  running on PySide2 5.12.1a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_logFrame(object):
    def setupUi(self, logFrame):
        logFrame.setObjectName("logFrame")
        logFrame.resize(462, 300)
        logFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        logFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gridLayout = QtWidgets.QGridLayout(logFrame)
        self.gridLayout.setContentsMargins(12, 12, 12, 12)
        self.gridLayout.setObjectName("gridLayout")
        self.clearButton = QtWidgets.QPushButton(logFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clearButton.sizePolicy().hasHeightForWidth())
        self.clearButton.setSizePolicy(sizePolicy)
        self.clearButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/PNG/black/32/document.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clearButton.setIcon(icon)
        self.clearButton.setObjectName("clearButton")
        self.gridLayout.addWidget(self.clearButton, 1, 2, 1, 1)
        self.levelComboBox = QtWidgets.QComboBox(logFrame)
        self.levelComboBox.setObjectName("levelComboBox")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/PNG/black/32/bug.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.levelComboBox.addItem(icon1, "")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/PNG/green/32/information.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.levelComboBox.addItem(icon2, "")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/PNG/orange/32/warning.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.levelComboBox.addItem(icon3, "")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/PNG/red/32/exclamation_mark.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.levelComboBox.addItem(icon4, "")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/PNG/magenta/32/cross.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.levelComboBox.addItem(icon5, "")
        self.gridLayout.addWidget(self.levelComboBox, 1, 1, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(logFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 434, 210))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 4, 0, 1, 3)
        self.levelLabel = QtWidgets.QLabel(logFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.levelLabel.sizePolicy().hasHeightForWidth())
        self.levelLabel.setSizePolicy(sizePolicy)
        self.levelLabel.setObjectName("levelLabel")
        self.gridLayout.addWidget(self.levelLabel, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(logFrame)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.levelLabel.setBuddy(self.levelComboBox)

        self.retranslateUi(logFrame)
        QtCore.QObject.connect(self.clearButton, QtCore.SIGNAL("clicked()"), self.textEdit.clear)
        QtCore.QMetaObject.connectSlotsByName(logFrame)
        logFrame.setTabOrder(self.textEdit, self.scrollArea)

    def retranslateUi(self, logFrame):
        logFrame.setWindowTitle(QtWidgets.QApplication.translate("logFrame", "Frame", None, -1))
        self.clearButton.setToolTip(QtWidgets.QApplication.translate("logFrame", "Clear", None, -1))
        self.clearButton.setStatusTip(QtWidgets.QApplication.translate("logFrame", "Clear", None, -1))
        self.clearButton.setWhatsThis(QtWidgets.QApplication.translate("logFrame", "Clear Log", None, -1))
        self.levelComboBox.setItemText(0, QtWidgets.QApplication.translate("logFrame", "Debug", None, -1))
        self.levelComboBox.setItemText(1, QtWidgets.QApplication.translate("logFrame", "Info", None, -1))
        self.levelComboBox.setItemText(2, QtWidgets.QApplication.translate("logFrame", "Warning", None, -1))
        self.levelComboBox.setItemText(3, QtWidgets.QApplication.translate("logFrame", "Error", None, -1))
        self.levelComboBox.setItemText(4, QtWidgets.QApplication.translate("logFrame", "Critical", None, -1))
        self.textEdit.setHtml(QtWidgets.QApplication.translate("logFrame", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.SF NS Text\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'.Helvetica Neue DeskInterface\';\"><br /></p></body></html>", None, -1))
        self.levelLabel.setText(QtWidgets.QApplication.translate("logFrame", "Level:", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("logFrame", "Log:", None, -1))

