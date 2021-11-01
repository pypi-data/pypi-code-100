#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 10:31:11 2019

@author: grat05
"""
from PyQt5 import QtCore
import numpy as np

class Runner(QtCore.QRunnable):
    def __init__(self, func, args):
        QtCore.QRunnable.__init__(self)
        self.signals = RunnerSignals()
        self.func = func
        self.args = args

    def run(self):
        data = self.func(*self.args)
        self.signals.finished.emit(data)
        del self.signals

class RunnerSignals(QtCore.QObject):
    finished = QtCore.pyqtSignal(np.ndarray)
    def __init__(self):
        QtCore.QObject.__init__(self)