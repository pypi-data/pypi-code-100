# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QCodeDialog.ui',
# licensing of 'QCodeDialog.ui' applies.
#
# Created: Mon Jan 14 10:58:45 2019
#      by: pyside2-uic  running on PySide2 5.12.1a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_codeDialog(object):
    def setupUi(self, codeDialog):
        codeDialog.setObjectName("codeDialog")
        codeDialog.resize(567, 560)
        codeDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(codeDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.codePlainTextEdit = CodeEditor(codeDialog)
        self.codePlainTextEdit.setReadOnly(True)
        self.codePlainTextEdit.setObjectName("codePlainTextEdit")
        self.verticalLayout.addWidget(self.codePlainTextEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(codeDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(codeDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), codeDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), codeDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(codeDialog)

    def retranslateUi(self, codeDialog):
        codeDialog.setWindowTitle(QtWidgets.QApplication.translate("codeDialog", "Sequencer Code", None, -1))

from sknrf.view.desktop.sequencer.code import CodeEditor
