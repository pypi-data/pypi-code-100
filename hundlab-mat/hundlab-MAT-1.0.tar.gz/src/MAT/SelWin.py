# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 14:06:34 2019

@author: alexj
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QDialog, QPushButton, QVBoxLayout, QMessageBox
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

class SelWin(QtWidgets.QWidget):
    def __init__(self):
        QWidget.__init__(self)
#        self.completeButton = QPushButton('Complete')
#        self.completeButton.clicked.connect(self.complete)
#        layout = QVBoxLayout()
#        layout.addWidget(self.completeButton)
        self.done = 0
        
    def new(self, imarr):
#        self.fig, self.ax = plt.subplots()
        layout = QtWidgets.QVBoxLayout(self)
        self.canvas = FigureCanvas(Figure(figsize=(10,10)))
        self.navbar = NavigationToolbar(self.canvas,self)
        layout.addWidget(self.navbar)
        layout.addWidget(self.canvas)
        self._ax = self.canvas.figure.subplots()
        self._ax.imshow(imarr)
        self._ax.set_title('Select Regions for Analysis')
        self.Selected = []
        self.dims = imarr.shape
        self.imarr = imarr
        self._ax.figure.canvas.draw()
                
        def onclick(event):
            if (event.dblclick == 1):
                self.center = np.array([event.xdata, event.ydata])
                self._ax.scatter(self.center[0], self.center[1], s = 3 , color = 'r')
                self._ax.figure.canvas.draw()
                self.radius = 8
                point1 = plt.Circle(self.center,self.radius, edgecolor = 'r', fill = 0)
                self._ax.add_artist(point1)
                self._ax.figure.canvas.draw()
                newpt = np.rint([self.center[0],self.center[1], self.radius])
                self.Selected.append((newpt).astype(int))
#            if (event.button == 3):
#                self.perimeter  = np.array([event.xdata, event.ydata])
#                self.radius = np.linalg.norm(self.center-self.perimeter)
#                circle1 = plt.Circle(self.center, self.radius, edgecolor = 'r', fill = 0)
#                self._ax.add_artist(circle1)
#                self._ax.figure.canvas.draw()
#                newpt = np.rint([self.center[0], self.center[1], self.radius])
#                self.Selected.append((newpt).astype(int))
        self._ax.figure.canvas.mpl_connect('button_press_event', onclick)
        self.show()
        
    def crop(self, radius):
        SelMask = np.zeros_like(self.imarr).astype(bool)
        im_x = self.dims[1]
        im_y = self.dims[0]
        r = radius
        self.imsel = self.imarr.copy()
        Selected_a = np.array(self.Selected)
        self.imgrey3 = np.ones_like(self.imsel)*255
#        self.imgrey3[:,:,0] = np.mean(self.imsel,-1)
#        self.imgrey3[:,:,1] = np.mean(self.imsel,-1)
#        self.imgrey3[:,:,2] = np.mean(self.imsel,-1)
        for i in range(len(Selected_a)):
            x = Selected_a[i,0]
            y = Selected_a[i,1]
            for j in range(max(x-r,0),min(x+r,im_x-1)):
                for k in range(max(y-r,0),min(y+r,im_y-1)): 
                    if r >= np.linalg.norm([j,k]-np.array([x,y])):
                        SelMask[k,j] = True
                        self.imgrey3[k,j,:] = self.imsel[k,j,:]
                                      
        self.imsel[np.logical_not(SelMask)] = 255

        self._ax.imshow(self.imgrey3)
        self._ax.figure.canvas.draw()
        self.show()
#        plt.figure()
#        plt.imshow(self.imgrey3)
        