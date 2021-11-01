# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 14:06:34 2019

@author: alexj
"""

import sys
import scipy.misc
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QDialog, QPushButton, QVBoxLayout, QMessageBox, QDoubleSpinBox, QLabel, QFileDialog

from .SelWin import SelWin

class RegionSel(QtWidgets.QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QtWidgets.QGridLayout(self)
        self.cropButton = QPushButton('Crop')
        self.cropButton.clicked.connect(self.crop)
        self.saveButton = QPushButton('Save')
        self.saveButton.clicked.connect(self.save)
        self.scaleB = QDoubleSpinBox()
        self.radiusB = QDoubleSpinBox()
        self.scaleB.setRange(0,1e10)
        self.radiusB.setRange(0,1e10)
        layout.addWidget(QLabel('Scale [pix/\u03BCm]'),0,0)
        layout.addWidget(QLabel('Radius [\u03BCm]'),1,0)
        layout.addWidget(self.scaleB,0,1)
        layout.addWidget(self.radiusB,1,1)
        layout.addWidget(self.cropButton,2,0)
        layout.addWidget(self.saveButton,2,1)
        self.regions = SelWin()

        
    def new(self, imarr):
        self.regions.new(imarr)
        msg = QMessageBox()
        msg.setText('To Select Regions: \n  1) double click to define each center \n  2) close when finished')
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Help')
        msg.show()
        
    def crop(self):
        r = self.radiusB.value()
        s = self.scaleB.value()
        radius = int(r*s)
        self.regions.crop(radius)
        
    def save(self):
        file = QFileDialog.getSaveFileName(caption='Save Image As:')
        if len(file[0])==0:
            return
        filename = file[0] + '.jpg'
        Cropped = Image.fromarray(self.regions.imgrey3)
        Cropped.save(filename)      
