#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 17:03:58 2019

@author: grat05
"""
from PIL import Image
from glob import glob
import numpy as np

basedir = input('Please enter the directory with .tiff files to process:\n')#'R:/Hund/DanielGratz/Fibrosis/validation/dan gratz_validation - Copy'
files = glob(basedir+'/*.tif')

for file in files:
    im = Image.open(file)
    imarr = np.array(im)
    bdr = imarr[...,2]/imarr[...,0]
    rdb = imarr[...,0]/imarr[...,2]
    blue_count = np.sum((bdr -1.2)>0)
    red_count = np.sum((rdb -1.2)>0)
    filename = file.replace('\\','/').split('/')[-1]
    print(filename, blue_count, red_count)

input('Press Enter to continue ...')

