# Form implementation generated from reading ui file 'calculatorform.ui'
#
# Created by: PyQt6 UI code generator 6.1.0.dev2103211315
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_CalculatorForm(object):
    def setupUi(self, CalculatorForm):
        CalculatorForm.setObjectName("CalculatorForm")
        CalculatorForm.resize(400, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy(5), QtWidgets.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CalculatorForm.sizePolicy().hasHeightForWidth())
        CalculatorForm.setSizePolicy(sizePolicy)
        self.gridlayout = QtWidgets.QGridLayout(CalculatorForm)
        self.gridlayout.setContentsMargins(9, 9, 9, 9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridlayout.addItem(spacerItem, 0, 6, 1, 1)
        self.label_3_2 = QtWidgets.QLabel(CalculatorForm)
        self.label_3_2.setGeometry(QtCore.QRect(169, 9, 20, 52))
        self.label_3_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3_2.setObjectName("label_3_2")
        self.gridlayout.addWidget(self.label_3_2, 0, 4, 1, 1)
        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.setContentsMargins(1, 1, 1, 1)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")
        self.label_2_2_2 = QtWidgets.QLabel(CalculatorForm)
        self.label_2_2_2.setGeometry(QtCore.QRect(1, 1, 36, 17))
        self.label_2_2_2.setObjectName("label_2_2_2")
        self.vboxlayout.addWidget(self.label_2_2_2)
        self.outputWidget = QtWidgets.QLabel(CalculatorForm)
        self.outputWidget.setGeometry(QtCore.QRect(1, 24, 36, 27))
        self.outputWidget.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.outputWidget.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.outputWidget.setAlignment(QtCore.Qt.AlignmentFlag.AlignAbsolute|QtCore.Qt.AlignmentFlag.AlignBottom|QtCore.Qt.AlignmentFlag.AlignCenter|QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignHorizontal_Mask|QtCore.Qt.AlignmentFlag.AlignJustify|QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTop|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter|QtCore.Qt.AlignmentFlag.AlignVertical_Mask)
        self.outputWidget.setObjectName("outputWidget")
        self.vboxlayout.addWidget(self.outputWidget)
        self.gridlayout.addLayout(self.vboxlayout, 0, 5, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridlayout.addItem(spacerItem1, 1, 2, 1, 1)
        self.vboxlayout1 = QtWidgets.QVBoxLayout()
        self.vboxlayout1.setContentsMargins(1, 1, 1, 1)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.label_2 = QtWidgets.QLabel(CalculatorForm)
        self.label_2.setGeometry(QtCore.QRect(1, 1, 46, 19))
        self.label_2.setObjectName("label_2")
        self.vboxlayout1.addWidget(self.label_2)
        self.inputSpinBox2 = QtWidgets.QSpinBox(CalculatorForm)
        self.inputSpinBox2.setGeometry(QtCore.QRect(1, 26, 46, 25))
        self.inputSpinBox2.setObjectName("inputSpinBox2")
        self.vboxlayout1.addWidget(self.inputSpinBox2)
        self.gridlayout.addLayout(self.vboxlayout1, 0, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(CalculatorForm)
        self.label_3.setGeometry(QtCore.QRect(63, 9, 20, 52))
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3, 0, 1, 1, 1)
        self.vboxlayout2 = QtWidgets.QVBoxLayout()
        self.vboxlayout2.setContentsMargins(1, 1, 1, 1)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")
        self.label = QtWidgets.QLabel(CalculatorForm)
        self.label.setGeometry(QtCore.QRect(1, 1, 46, 19))
        self.label.setObjectName("label")
        self.vboxlayout2.addWidget(self.label)
        self.inputSpinBox1 = QtWidgets.QSpinBox(CalculatorForm)
        self.inputSpinBox1.setGeometry(QtCore.QRect(1, 26, 46, 25))
        self.inputSpinBox1.setObjectName("inputSpinBox1")
        self.vboxlayout2.addWidget(self.inputSpinBox1)
        self.gridlayout.addLayout(self.vboxlayout2, 0, 0, 1, 1)

        self.retranslateUi(CalculatorForm)
        QtCore.QMetaObject.connectSlotsByName(CalculatorForm)

    def retranslateUi(self, CalculatorForm):
        _translate = QtCore.QCoreApplication.translate
        CalculatorForm.setWindowTitle(_translate("CalculatorForm", "Calculator Form"))
        self.label_3_2.setText(_translate("CalculatorForm", "="))
        self.label_2_2_2.setText(_translate("CalculatorForm", "Output"))
        self.outputWidget.setText(_translate("CalculatorForm", "0"))
        self.label_2.setText(_translate("CalculatorForm", "Input 2"))
        self.label_3.setText(_translate("CalculatorForm", "+"))
        self.label.setText(_translate("CalculatorForm", "Input 1"))
