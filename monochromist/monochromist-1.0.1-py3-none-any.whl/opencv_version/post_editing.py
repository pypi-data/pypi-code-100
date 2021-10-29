from typing import Tuple

import numpy as np
from colour import Color

from monochromist.opencv_version.classes import Settings


def color_image(img: np.ndarray, settings: Settings) -> np.ndarray:
    """Color non-transparent pixels with selected color

    :param img: input image with black (0) background and white contour (255)
    :param settings: user settings

    :return: numpy array with transparent background and colored contour"""

    color_tuple = color2tuple(settings.color)
    transparent = (0, 0, 0, 0)

    colored = np.array([color_tuple if x else transparent for x in img.flatten()])
    height, width = img.shape

    return colored.reshape((height, width, -1))


def crop_borders(img: np.ndarray) -> np.ndarray:
    notna_columns = img.any(axis=0)
    notna_rows = img.any(axis=1)

    left = np.flatnonzero(notna_columns)[0]
    right = np.flatnonzero(notna_columns)[-1]

    upper = np.flatnonzero(notna_rows)[0]
    lower = np.flatnonzero(notna_rows)[-1]

    return img[upper:lower, left:right]


def color2tuple(color: Color) -> Tuple[int, int, int, int]:
    """Convert color to RGBA tuple"""
    r, g, b = [int(255 * x) for x in color.rgb]
    alpha_channel = 255
    # opencv use BGR not RGB model
    return b, g, r, alpha_channel
