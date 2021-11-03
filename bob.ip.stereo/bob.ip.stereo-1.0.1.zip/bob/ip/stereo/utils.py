import numpy as np
import cv2 as cv


def convert_to_uint8(img, normalize=False):
    if img.dtype == np.uint16:
        if normalize:
            img = cv.normalize(img, None, 0, 65535, cv.NORM_MINMAX)
        img = (img / 256).astype("uint8")
    else:
        if normalize:
            img = cv.normalize(img, None, 0, 255, cv.NORM_MINMAX)
    return img
