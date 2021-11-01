# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 16:36:37 2019

@author: alexj
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from matplotlib.backend_bases import MouseButton
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt

class CalibPoints(QtWidgets.QWidget):
    pointAdded = pyqtSignal(tuple, int, name='pointAdded')

    def __init__(self, title):
        QWidget.__init__(self)
        self.title = title
        self.CalibPts = []
        self.pointScatters = []
        self.circles = []
        self.center = None

    def new(self, imarr):
#        self.fig, self.ax = plt.subplots()
#        if hasattr(self, '_ax'):
#            self._ax.figure.canvas.close()
#
        layout = QtWidgets.QVBoxLayout(self)
        self.canvas = FigureCanvas(Figure(figsize=(10,10)))
        self.navbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.navbar)
        layout.addWidget(self.canvas)
        self.canvas.setFocusPolicy(Qt.ClickFocus)
        self.canvas.setFocus()
        self._ax = self.canvas.figure.subplots()
        self._ax.imshow(imarr)
        self._ax.set_title(self.title)
        self.CalibPts = []
        self.dims = imarr.shape
        self.imarr = imarr
        self._ax.figure.canvas.draw()

        def onclick(event):
            if (event.dblclick or (event.button == MouseButton.LEFT and event.key == 'shift')): 
                if not self.center is None:
                    self.pointScatters[-1].remove()
                    del self.pointScatters[-1]
                self.center = np.array([event.xdata, event.ydata])
                scatter = self._ax.scatter(self.center[0], self.center[1], s = 3 , color = 'r')
                self.pointScatters.append(scatter)
                self._ax.figure.canvas.draw()
            if (event.button == MouseButton.RIGHT):
                if self.center is None:
                    return
                self.perimeter  = np.array([event.xdata, event.ydata])
                self.radius = np.linalg.norm(self.center-self.perimeter)
                circle1 = plt.Circle(self.center, self.radius, edgecolor = 'r', fill = 0)
                self._ax.add_artist(circle1)
                self.circles.append(circle1)
                self._ax.figure.canvas.draw()
                newpt = np.rint([self.center[0], self.center[1], self.radius]).astype(int)
                self.CalibPts.append(newpt)
                self.pointAdded.emit((newpt[0], newpt[1]), newpt[2])
                self.center = None

        self._ax.figure.canvas.mpl_connect('button_press_event', onclick)
        self.show()

    def add(self):
        if hasattr(self, '_ax'):
            self.show()
        else:
            print('Must first create new')

    def calculate(self):
        if len(self.CalibPts) == 0:
            print('Must first define points')
        else:
            self.CalibData = []
            self.index = []
            im_x = self.dims[1]
            im_y = self.dims[0]
            #CalibMask = np.zeros([im_y, im_x],dtype=np.int64)
            CalibPts_a = np.array(self.CalibPts)
            num = 0
            for i in range(len(CalibPts_a)):
                self.index.append(num)
                x,y,r = CalibPts_a[i,:]
                for j in range(max(x-r,0),min(x+r,im_x-1)):
                    for k in range(max(y-r,0),min(y+r,im_y-1)):
                        if r >= np.linalg.norm([j,k]-np.array([x,y])):
                            #CalibMask[k,j] = True
                            self.CalibData.append(self.imarr[k,j,:])
                            num = num + 1
            self.index.append(num)
            CalibData_a = np.array(self.CalibData)
#            print(CalibData_a)
            ratios = np.transpose(np.transpose(CalibData_a)/np.mean(CalibData_a,axis=1))
            self.brightness = np.std(np.mean(CalibData_a,axis=1)) + np.mean(np.mean(CalibData_a,axis=1))
            self.RGB = np.mean(ratios,axis=0)
            self.tol = (np.max(ratios,axis=0)-np.min(ratios,axis=0))/2
#            print(self.brightness)
#            print(max(np.mean(CalibData_a,axis=1)))
#            print(self.RGB)
#            print(self.tol)
#            print(self.index)
#            self.NumPix = []
#            for i in range(len(self.index)):
#                list1 = CalibData_a[self.index[i]:self.index[i+1]]
#                array = np.array(list1)
#                upper = self.RGB + self.RGB*self.tol
#                lower = self.RGB - self.RGB*self.tol
#                avg = np.array(np.mean(array, axis=1))
#                imrat = np.array(array/avg[...,None])
#                magnitude = np.less(avg, self.brightness)
#                colormatch = np.sum(np.logical_and(imrat>lower,imrat<upper),axis=1)
#                regions = 255*np.invert(np.logical_and(magnitude==True,colormatch==3))
#                regions_filter = gaussian_filter(regions, sigma=2)
#                mask = np.less(regions_filter,190)
#                print(mask)
#                erode = binary_erosion(mask, disk(1))
#                print(np.sum(erode))
#                self.NumPix.append(np.sum(erode))

    def redraw(self):
        self._ax.figure.canvas.draw()

    def removePoint(self, pos):
        del self.CalibPts[pos]
        self.pointScatters[pos].remove()
        del self.pointScatters[pos]
        self.circles[pos].remove()
        del self.circles[pos]
        self._ax.figure.canvas.draw()
