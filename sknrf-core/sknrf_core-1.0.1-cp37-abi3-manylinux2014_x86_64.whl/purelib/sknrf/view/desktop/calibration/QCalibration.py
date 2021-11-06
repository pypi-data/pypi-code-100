# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QCalibration.ui',
# licensing of 'QCalibration.ui' applies.
#
# Created: Mon Jan 14 16:01:40 2019
#      by: pyside2-uic  running on PySide2 5.12.1a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_calibrationWizard(object):
    def setupUi(self, calibrationWizard):
        calibrationWizard.setObjectName("calibrationWizard")
        calibrationWizard.resize(501, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(calibrationWizard.sizePolicy().hasHeightForWidth())
        calibrationWizard.setSizePolicy(sizePolicy)
        calibrationWizard.setMaximumSize(QtCore.QSize(600, 300))
        calibrationWizard.setModal(False)
        calibrationWizard.setWizardStyle(QtWidgets.QWizard.ModernStyle)
        calibrationWizard.setOptions(QtWidgets.QWizard.HaveCustomButton1|QtWidgets.QWizard.HaveHelpButton|QtWidgets.QWizard.IndependentPages|QtWidgets.QWizard.NoBackButtonOnStartPage)
        calibrationWizard.setSubTitleFormat(QtCore.Qt.RichText)

        self.retranslateUi(calibrationWizard)
        QtCore.QMetaObject.connectSlotsByName(calibrationWizard)

    def retranslateUi(self, calibrationWizard):
        calibrationWizard.setWindowTitle(QtWidgets.QApplication.translate("calibrationWizard", "Calibration", None, -1))

