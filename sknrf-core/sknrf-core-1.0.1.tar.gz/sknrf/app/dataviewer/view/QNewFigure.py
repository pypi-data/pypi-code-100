# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QNewFigure.ui',
# licensing of 'QNewFigure.ui' applies.
#
# Created: Sat Jan 19 23:21:32 2019
#      by: pyside2-uic  running on PySide2 5.12.1a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_QNewFigureDialog(object):
    def setupUi(self, QNewFigureDialog):
        QNewFigureDialog.setObjectName("QNewFigureDialog")
        QNewFigureDialog.resize(400, 155)
        self.formLayout = QtWidgets.QFormLayout(QNewFigureDialog)
        self.formLayout.setObjectName("formLayout")
        self.nameLabel = QtWidgets.QLabel(QNewFigureDialog)
        self.nameLabel.setObjectName("nameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.nameLabel)
        self.nameLineEdit = QtWidgets.QLineEdit(QNewFigureDialog)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.nameLineEdit)
        self.gridGroupBox = QtWidgets.QGroupBox(QNewFigureDialog)
        self.gridGroupBox.setObjectName("gridGroupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.gridGroupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.widthLabel = QtWidgets.QLabel(self.gridGroupBox)
        self.widthLabel.setObjectName("widthLabel")
        self.gridLayout.addWidget(self.widthLabel, 0, 0, 1, 1)
        self.widthGridSpinBox = QtWidgets.QSpinBox(self.gridGroupBox)
        self.widthGridSpinBox.setMinimum(1)
        self.widthGridSpinBox.setObjectName("widthGridSpinBox")
        self.gridLayout.addWidget(self.widthGridSpinBox, 0, 1, 1, 1)
        self.heightGridLabel = QtWidgets.QLabel(self.gridGroupBox)
        self.heightGridLabel.setObjectName("heightGridLabel")
        self.gridLayout.addWidget(self.heightGridLabel, 0, 2, 1, 1)
        self.heightGridSpinBox = QtWidgets.QSpinBox(self.gridGroupBox)
        self.heightGridSpinBox.setMinimum(1)
        self.heightGridSpinBox.setObjectName("heightGridSpinBox")
        self.gridLayout.addWidget(self.heightGridSpinBox, 0, 3, 1, 1)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.gridGroupBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(QNewFigureDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.buttonBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(2, QtWidgets.QFormLayout.LabelRole, spacerItem)

        self.retranslateUi(QNewFigureDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), QNewFigureDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), QNewFigureDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(QNewFigureDialog)

    def retranslateUi(self, QNewFigureDialog):
        QNewFigureDialog.setWindowTitle(QtWidgets.QApplication.translate("QNewFigureDialog", "Dialog", None, -1))
        self.nameLabel.setText(QtWidgets.QApplication.translate("QNewFigureDialog", "Name:", None, -1))
        self.gridGroupBox.setTitle(QtWidgets.QApplication.translate("QNewFigureDialog", "Grid", None, -1))
        self.widthLabel.setText(QtWidgets.QApplication.translate("QNewFigureDialog", "Width:", None, -1))
        self.heightGridLabel.setText(QtWidgets.QApplication.translate("QNewFigureDialog", "Height:", None, -1))

