#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 10:58:58 2021

@author: grat05
"""

import matplotlib.pyplot as plt
from matplotlib.backend_tools import ToolToggleBase
import numpy as np
from PIL import Image
from scipy import ndimage
from copy import deepcopy

from . import plot_hsv_labels
from ..fibrosis_segmentation import createColorMasks

#covers everything not selected by the mask and plots it
def showMask(im,mask,name):
    plt.title(name)
    plt.axis('off')
    plt.imshow(coverUnMasked(im,mask))

#covers everything not selected by the mask
def coverUnMasked(im,mask):
    blk_base = Image.new('RGB', im.size)
    mask = Image.fromarray(mask.astype('uint8')*255, mode='L')
    masked = Image.composite(im, blk_base, mask)
    return masked

#increases the saturation to 100% for everything selected by the mask
def beautify(colorMask, im):
    HSV = np.asarray(im.convert('HSV')).copy()
    HSV[colorMask,1] = 255
    return Image.fromarray(HSV, mode='HSV').convert('RGB')

# functions to change the display of pixel information for images in matplotlib
def format_cursor_data(data):
    hsv_string =  plot_hsv_labels.format_cursor_data(data[0])
    if data[1] is not None:
        mask_name = data[1]
    else:
        mask_name = ''
    return hsv_string+', Mask = '+mask_name

def get_cursor_data(self, event, masks):
    data = plot_hsv_labels.get_cursor_data(self, event, return_index=True)
    if data is not None:
        hsv, index = data
    else:
        return None
    mask_name = masks.whichMask(*index)
    return hsv, mask_name
    
def plotImage(im, HSV, masks, ax=None, imshow=None):
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
#        imshow.set_alpha(alpha)
    elif ax is not None:
        imshow = ax.imshow(im)
    else:
        imshow = plt.imshow(im)
    imshow.HSV = HSV
    imshow.get_cursor_data = lambda event: get_cursor_data(imshow, event, masks)
    imshow.format_cursor_data = format_cursor_data
    return imshow

class MaskShowTool(ToolToggleBase):
    """Show the area a color mask would cover"""
#    default_keymap = 'S'
    description = "Show a mask's coverage"
    default_toggled = False
    
    def __init__(self, *args, mask_name, masks, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.mask_name = mask_name
        self.masks = masks
        self.mask = None
        self.edge_alpha = None
        self.imshow = None

    def enable(self, *args):
        mask = self.masks[self.mask_name]
        if (mask == self.mask).all():
            if self.imshow is not None:
                self.imshow.set_visible(True)
                self.figure.canvas.draw()
            return
        self.mask = mask
        edge = ndimage.binary_dilation(self.mask, iterations=15) ^ self.mask
        self.edge_alpha = np.zeros((*self.mask.shape, 4), dtype=np.uint8)
        self.edge_alpha[...,3] = edge*255
        self.imshow = plotImage(self.edge_alpha,
                                self.masks.HSV,
                                self.masks,
                                ax=self.figure.get_axes()[0],
                                imshow=self.imshow)
        self.imshow.set_visible(True)
        self.figure.canvas.draw()

    def disable(self, *args):
        if self.mask is not None:
            self.imshow.set_visible(False)
        self.figure.canvas.draw()
        
class ComputeMasks():
    def __init__(self, HSV=None, color_rules=None):
        self.HSV = HSV
        self.color_rules = deepcopy(color_rules)
        self.recompute_masks = not (HSV is None and color_rules is None)
        self.masks = dict(background=None,
                          tissue=None,
                          stain=None,
                          other=None)
    
    def computeMasks(self, force=False):
        if not self.recompute_masks and not force:
            return
        if self.HSV is None or self.color_rules is None:
            return
        
        masks = createColorMasks(self.HSV, self.color_rules)
        (self.masks['background'],
         self.masks['tissue'],
         self.masks['stain'],
         self.masks['other']) = masks
    
        self.recompute_masks = False
        
    def __getitem__(self, key):
        if key not in self.masks:
            return None
        if self.recompute_masks:
            self.computeMasks()
        return self.masks[key]
        
    def setHSV(self, hsv):
        self.HSV = hsv
        self.recompute_masks = True
        
    def setColorRules(self, color_rules):
        if color_rules != self.color_rules:
            self.color_rules = deepcopy(color_rules)
            self.recompute_masks = True
            
    def whichMask(self, x, y):
        if self.recompute_masks:
            self.computeMasks()
        try:
            for mask_name, mask in self.masks.items():
                if mask[x,y]:
                    return mask_name
        except(TypeError):
            pass
        return None
            