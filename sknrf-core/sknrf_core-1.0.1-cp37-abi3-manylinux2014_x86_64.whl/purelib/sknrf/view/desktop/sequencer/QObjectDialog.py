# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QObjectDialog.ui',
# licensing of 'QObjectDialog.ui' applies.
#
# Created: Mon Jan 14 10:58:45 2019
#      by: pyside2-uic  running on PySide2 5.12.1a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_objectDialog(object):
    def setupUi(self, objectDialog):
        objectDialog.setObjectName("objectDialog")
        objectDialog.resize(362, 362)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(objectDialog.sizePolicy().hasHeightForWidth())
        objectDialog.setSizePolicy(sizePolicy)
        objectDialog.setSizeGripEnabled(True)
        objectDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(objectDialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.moduleFrame = QtWidgets.QFrame(objectDialog)
        self.moduleFrame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.moduleFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.moduleFrame.setObjectName("moduleFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.moduleFrame)
        self.gridLayout.setObjectName("gridLayout")
        self.moduleLabel = QtWidgets.QLabel(self.moduleFrame)
        self.moduleLabel.setObjectName("moduleLabel")
        self.gridLayout.addWidget(self.moduleLabel, 0, 0, 1, 1)
        self.moduleLineEdit = QtWidgets.QLineEdit(self.moduleFrame)
        self.moduleLineEdit.setEnabled(False)
        self.moduleLineEdit.setText("")
        self.moduleLineEdit.setReadOnly(False)
        self.moduleLineEdit.setObjectName("moduleLineEdit")
        self.gridLayout.addWidget(self.moduleLineEdit, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.moduleFrame)
        self.returnFrame = QtWidgets.QFrame(objectDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.returnFrame.sizePolicy().hasHeightForWidth())
        self.returnFrame.setSizePolicy(sizePolicy)
        self.returnFrame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.returnFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.returnFrame.setObjectName("returnFrame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.returnFrame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.returnLabel = QtWidgets.QLabel(self.returnFrame)
        self.returnLabel.setObjectName("returnLabel")
        self.gridLayout_2.addWidget(self.returnLabel, 0, 0, 1, 1)
        self.returnLineEdit = QtWidgets.QLineEdit(self.returnFrame)
        self.returnLineEdit.setObjectName("returnLineEdit")
        self.gridLayout_2.addWidget(self.returnLineEdit, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.returnFrame)
        self.argumentFrame = QtWidgets.QFrame(objectDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.argumentFrame.sizePolicy().hasHeightForWidth())
        self.argumentFrame.setSizePolicy(sizePolicy)
        self.argumentFrame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.argumentFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.argumentFrame.setObjectName("argumentFrame")
        self.verticalLayout.addWidget(self.argumentFrame)
        self.buttonBox = QtWidgets.QDialogButtonBox(objectDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(objectDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), objectDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), objectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(objectDialog)
        objectDialog.setTabOrder(self.moduleLineEdit, self.returnLineEdit)
        objectDialog.setTabOrder(self.returnLineEdit, self.buttonBox)

    def retranslateUi(self, objectDialog):
        objectDialog.setWindowTitle(QtWidgets.QApplication.translate("objectDialog", "Dialog", None, -1))
        self.moduleLabel.setText(QtWidgets.QApplication.translate("objectDialog", "Module: ", None, -1))
        self.returnLabel.setText(QtWidgets.QApplication.translate("objectDialog", "Return: ", None, -1))

