#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 11:42:45 2019

@author: alexj, grat05
"""

import numpy as np
from matplotlib.backends.qt_compat import QtWidgets
from PyQt5.QtWidgets import QWidget, QSpinBox, QDoubleSpinBox, QLabel, QMessageBox, QTreeWidget
from PyQt5.QtCore import Qt
from .CalibPoints import CalibPoints

class Calibrator(QtWidgets.QWidget):
    def __init__(self, title):
        QWidget.__init__(self)
        layout = QtWidgets.QGridLayout(self)
        self.title = title
        layout.addWidget(QLabel("Value"),0,1)
        layout.addWidget(QLabel("Tolerance"),0,2)
        layout.addWidget(QLabel("Red Channel"),1,0)
        layout.addWidget(QLabel("Green Channel"),2,0)
        layout.addWidget(QLabel("Blue Channel"),3,0)
        layout.addWidget(QLabel("Brightness"),4,0)
        self.RGB1 = QDoubleSpinBox()
        self.RGB2 = QDoubleSpinBox()
        self.RGB3 = QDoubleSpinBox()
        self.tol1 = QDoubleSpinBox()
        self.tol2 = QDoubleSpinBox()
        self.tol3 = QDoubleSpinBox()
        self.BrightnessSpin = QSpinBox()
        self.RGB1.setMaximum(255)
        self.RGB1.setMinimum(0)
        self.RGB1.setDecimals(6)
        self.RGB2.setMaximum(255)
        self.RGB2.setMinimum(0)
        self.RGB2.setDecimals(6)
        self.RGB3.setMaximum(255)
        self.RGB3.setMinimum(0)
        self.RGB3.setDecimals(6)
        self.tol1.setMaximum(255)
        self.tol1.setMinimum(0)
        self.tol1.setDecimals(6)
        self.tol2.setMaximum(255)
        self.tol2.setMinimum(0)
        self.tol2.setDecimals(6)
        self.tol3.setMaximum(255)
        self.tol3.setMinimum(0)
        self.tol3.setDecimals(6)
        self.BrightnessSpin.setMaximum(255)
        self.BrightnessSpin.setMinimum(0)
        self.RGB1.setValue(0)
        self.RGB2.setValue(0)
        self.RGB3.setValue(0)
        self.tol1.setValue(0)
        self.tol2.setValue(0)
        self.tol3.setValue(0)
        self.BrightnessSpin.setValue(0)
        self.Choosebutton = QtWidgets.QPushButton('Choose New Points', self)
        self.Addbutton = QtWidgets.QPushButton('Add Points', self)
        self.Calcbutton = QtWidgets.QPushButton('Calculate Ratios', self)
        self.PointsList = QtWidgets.QTreeWidget(self)
        layout.addWidget(self.RGB1,1,1)
        layout.addWidget(self.RGB2,2,1)
        layout.addWidget(self.RGB3,3,1)
        layout.addWidget(self.tol1,1,2)
        layout.addWidget(self.tol2,2,2)
        layout.addWidget(self.tol3,3,2)
        layout.addWidget(self.BrightnessSpin,4,1)
        layout.addWidget(self.Choosebutton,5,0)
        layout.addWidget(self.Addbutton,5,1)
        layout.addWidget(self.Calcbutton,5,2)
        layout.addWidget(self.PointsList, 6, 0, 1, 3)
        self.Choosebutton.clicked.connect(self.Choosepushed)
        self.Addbutton.clicked.connect(self.Addpushed)
        self.Calcbutton.clicked.connect(self.Calcpushed)
        self.setWindowTitle(title)
        self.CalData = CalibPoints(self.title)
        self.CalData.pointAdded.connect(self.AddPoint)
        self.CalData.RGB = np.array([0,0,0],dtype=np.float64)
        self.CalData.tol = np.array([0,0,0],dtype=np.float64)
        self.CalData.brightness = 0
        self.pushed = 0
        self.PointsList.setHeaderLabels(['Point','Radius'])
        self.PointsList.setSortingEnabled(False)
        def eventHandler(event):
            if event.key() == Qt.Key_Delete:
                self.RemoveCurrentPoint()
            return QtWidgets.QTreeWidget.keyPressEvent(self.PointsList, event)
        self.PointsList.keyPressEvent = eventHandler

    def Choosepushed(self):
        if self.pushed == 1:
            self.CalData.destroy()
            self.CalData = CalibPoints(self.title)

        self.CalData.new(self.imarr)
        msg = QMessageBox()
        msg.setText('To add calibration data: \n  1) Double Left Click or Shirt + Left Click to define center \n  2) Right Click to define radius \n  3) Close when finished')
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Help')
        msg.exec()
        self.pushed = 1

    def Addpushed(self):
        self.CalData.add()

    def Calcpushed(self):
        self.CalData.calculate()

        self.tol = self.CalData.tol
        self.RGB = self.CalData.RGB
        self.brightness = self.CalData.brightness
        self.RGB1.setValue(self.CalData.RGB[0])
        self.RGB2.setValue(self.CalData.RGB[1])
        self.RGB3.setValue(self.CalData.RGB[2])
        self.tol1.setValue(self.CalData.tol[0])
        self.tol2.setValue(self.CalData.tol[1])
        self.tol3.setValue(self.CalData.tol[2])
        self.BrightnessSpin.setValue(self.CalData.brightness)
        msg = QMessageBox()
        msg.setText('Calibration Finished')
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('')
        msg.exec()

    def Refresh(self):
        self.CalData.RGB[0] = self.RGB1.value()
        self.CalData.RGB[1] = self.RGB2.value()
        self.CalData.RGB[2] = self.RGB3.value()
        self.CalData.tol[0] = self.tol1.value()
        self.CalData.tol[1] = self.tol2.value()
        self.CalData.tol[2] = self.tol3.value()
        self.CalData.brightness = self.BrightnessSpin.value()

    def AddPoint(self, point, radius):
        self.PointsList.addTopLevelItem(QtWidgets.QTreeWidgetItem(self.PointsList, [str(point),str(radius)]))

    def RemoveCurrentPoint(self):
        selectedItems = self.PointsList.selectedItems()
        for selectedItem in selectedItems:
            currPos = self.PointsList.indexOfTopLevelItem(selectedItem)
            self.CalData.removePoint(currPos)
            curr = self.PointsList.takeTopLevelItem(currPos)
            del curr

    def UpdatePointsList(self):
        self.PointsList.clear()
        for calibPoint in self.CalData.CalibPts:
            self.PointsList.addTopLevelItem(QtWidgets.QTreeWidgetItem(self.PointsList, [str((calibPoint[0],calibPoint[1])),str(calibPoint[2])]))
