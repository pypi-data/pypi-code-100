# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QEquationDialog.ui',
# licensing of 'QEquationDialog.ui' applies.
#
# Created: Mon Jan 14 23:53:17 2019
#      by: pyside2-uic  running on PySide2 5.12.1a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_equationDialog(object):
    def setupUi(self, equationDialog):
        equationDialog.setObjectName("equationDialog")
        equationDialog.resize(362, 159)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(equationDialog.sizePolicy().hasHeightForWidth())
        equationDialog.setSizePolicy(sizePolicy)
        equationDialog.setSizeGripEnabled(True)
        equationDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(equationDialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.equationFrame = QtWidgets.QFrame(equationDialog)
        self.equationFrame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.equationFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.equationFrame.setObjectName("equationFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.equationFrame)
        self.gridLayout.setObjectName("gridLayout")
        self.nameLabel = QtWidgets.QLabel(self.equationFrame)
        self.nameLabel.setObjectName("nameLabel")
        self.gridLayout.addWidget(self.nameLabel, 0, 0, 1, 1)
        self.unitLabel = QtWidgets.QLabel(self.equationFrame)
        self.unitLabel.setObjectName("unitLabel")
        self.gridLayout.addWidget(self.unitLabel, 2, 0, 1, 1)
        self.unitLineEdit = QtWidgets.QLineEdit(self.equationFrame)
        self.unitLineEdit.setObjectName("unitLineEdit")
        self.gridLayout.addWidget(self.unitLineEdit, 2, 1, 1, 1)
        self.nameLineEdit = QtWidgets.QLineEdit(self.equationFrame)
        self.nameLineEdit.setEnabled(True)
        self.nameLineEdit.setText("")
        self.nameLineEdit.setReadOnly(False)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.gridLayout.addWidget(self.nameLineEdit, 0, 1, 1, 1)
        self.equationLineEdit = QtWidgets.QLineEdit(self.equationFrame)
        self.equationLineEdit.setObjectName("equationLineEdit")
        self.gridLayout.addWidget(self.equationLineEdit, 1, 1, 1, 1)
        self.equationLabel = QtWidgets.QLabel(self.equationFrame)
        self.equationLabel.setObjectName("equationLabel")
        self.gridLayout.addWidget(self.equationLabel, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.equationFrame)
        self.buttonBox = QtWidgets.QDialogButtonBox(equationDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.nameLabel.setBuddy(self.nameLineEdit)
        self.unitLabel.setBuddy(self.unitLineEdit)
        self.equationLabel.setBuddy(self.equationLineEdit)

        self.retranslateUi(equationDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), equationDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), equationDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(equationDialog)
        equationDialog.setTabOrder(self.nameLineEdit, self.equationLineEdit)
        equationDialog.setTabOrder(self.equationLineEdit, self.unitLineEdit)
        equationDialog.setTabOrder(self.unitLineEdit, self.buttonBox)

    def retranslateUi(self, equationDialog):
        equationDialog.setWindowTitle(QtWidgets.QApplication.translate("equationDialog", "Dialog", None, -1))
        self.nameLabel.setText(QtWidgets.QApplication.translate("equationDialog", "Name:", None, -1))
        self.unitLabel.setText(QtWidgets.QApplication.translate("equationDialog", "Unit:", None, -1))
        self.equationLabel.setText(QtWidgets.QApplication.translate("equationDialog", "Equation:", None, -1))

