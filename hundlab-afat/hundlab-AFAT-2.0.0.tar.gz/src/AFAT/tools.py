#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 11:07:06 2021

@author: grat05
"""

import numpy as np
from PIL import Image

def openImage(image_filepath):
    try:
        im = Image.open(image_filepath)
    except(Image.DecompressionBombError):
        print("Large Image, Retrying")
        Image.MAX_IMAGE_PIXELS = np.inf
        im = Image.open(image_filepath)
    return im.convert('RGB')