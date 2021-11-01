#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 10:48:19 2021

@author: grat05
"""


import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox, BboxTransform
from numbers import Number
import numpy as np

# functions to change the display of pixel information for images in matplotlib
def format_cursor_data(data):
    data_str = ', '.join('{:0.3g}'.format(item) for item in data
                          if isinstance(item, Number))
    return "[H,S,V]=[" + data_str + "] "

def get_cursor_data(self, event, return_index=False):
    xmin, xmax, ymin, ymax = self.get_extent()
    if self.origin == 'upper':
        ymin, ymax = ymax, ymin
    arr = self.get_array()
    data_extent = Bbox([[ymin, xmin], [ymax, xmax]])
    array_extent = Bbox([[0, 0], arr.shape[:2]])
    trans = BboxTransform(boxin=data_extent, boxout=array_extent)
    y, x = event.ydata, event.xdata
    point = trans.transform_point([y, x])
    if any(np.isnan(point)):
        return None
    i, j = point.astype(int)
    # Clip the coordinates at array bounds
    if not (0 <= i < arr.shape[0]) or not (0 <= j < arr.shape[1]):
        return None
    else:
        ret = self.HSV[i, j]
        if return_index:
            return ret, (i,j)
        else:
            return ret
    
def plotImage(im, HSV, ax=None, imshow=None):
    '''
    Plot an image, modifying the mouseover data to display the HSV values
    insteada of the RGB values
    Parameters
    ----------
    im : RGB array or image object
    HSV : HSV array

    Returns
    -------
    imshow : pyplot imshow object
    '''
    if imshow is not None:
        imshow.set_data(im)
    elif ax is not None:
        imshow = ax.imshow(im)
    else:
        imshow = plt.imshow(im)
    imshow.HSV = HSV
    imshow.get_cursor_data = lambda event: get_cursor_data(imshow, event)
    imshow.format_cursor_data = format_cursor_data
    return imshow
