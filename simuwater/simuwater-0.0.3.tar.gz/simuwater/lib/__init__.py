# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 10:47:59 2021

@author: mumuz
"""

import ctypes
import os

LIB_PATH = os.path.abspath(os.path.dirname(__file__))

SIMUWATER = ctypes.cdll.LoadLibrary(LIB_PATH + '\\simuwater.dll')
OUTPUT = ctypes.cdll.LoadLibrary(LIB_PATH + '\\simuwater_output.dll')