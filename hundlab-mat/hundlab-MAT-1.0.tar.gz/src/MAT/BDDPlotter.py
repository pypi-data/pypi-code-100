#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 09:37:49 2019

@author: alexj, grat05

"""

import numpy as np
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QAction, QWidget

class BDDPlotter(QtWidgets.QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QtWidgets.QVBoxLayout(self)
        self.imarr = None
        self.canvas = FigureCanvas(Figure(figsize=(10,10)))
        self.navbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.navbar) # Add Navigation Toolbar
        layout.addWidget(self.canvas)
        self.toggleNuclei = QAction('Toggle\n Nuclei', self)
        self.toggleBDD = QAction('Toggle\n Macrophages', self)
        self.toggleColoc = QAction('Toggle\n Colocalize', self)
        before = self.navbar.actions()[6]
        self.navbar.insertAction(before, self.toggleNuclei)
        self.navbar.insertAction(before, self.toggleBDD)
        self.navbar.insertAction(before, self.toggleColoc)
        self.scatterN = None
        self.scatterC = None
        self.scatterB = None
        self._ax = self.canvas.figure.subplots()

    def showImg(self, RGB):
        self._ax.imshow(RGB)
        self._ax.figure.canvas.draw()

    def showNuclei(self, centroidsN):
        self.firstN = True
        if self.scatterN is not None:
            self.firstN = False
            self.scatterN.remove()
        self.scatterN = self._ax.scatter(centroidsN[:,1], centroidsN[:,0], label='Nuclei', color='blue')
        self._ax.legend()
        self._ax.figure.canvas.draw()
        if self.firstN:
            self.toggleNuclei.triggered.connect(lambda b: self.toggleScatter(self.scatterN))

    def showColocalize(self, coloc):
        self.firstC = True
        if self.scatterC is not None:
            self.firstC = False
            self.scatterC.remove()
        self.scatterC = self._ax.scatter(coloc[:,1], coloc[:,0], label='Colocalized', color=[0,1,0], marker='+')
        self._ax.legend()
        self._ax.figure.canvas.draw()
        if self.firstC:
            self.toggleColoc.triggered.connect(lambda b: self.toggleScatter(self.scatterC))

    def showBDD2(self, centroidsB):
#        self.centroidsB = centroidsB
        self.firstB = True
        if self.scatterB is not None:
            self.firstB = False
            self.scatterB.remove()
        self.scatterB = self._ax.scatter(centroidsB[:,1], centroidsB[:,0], label='Macrophages', color='brown')
        self._ax.legend()
        self._ax.figure.canvas.draw()
        if self.firstB:
            self.toggleBDD.triggered.connect(lambda b: self.toggleScatter(self.scatterB))

    def toggleScatter(self, origline):
        # on the pick event, find the orig line corresponding to the
        # legend proxy line, and toggle the visibility
        vis = not origline.get_visible()
        origline.set_visible(vis)
        self._ax.figure.canvas.draw()
        # Change the alpha on the line in the legend so we can see what lines
        # have been toggled
         