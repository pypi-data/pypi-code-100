import cv2
import numpy as np

from .classes import Settings


def find_mask(img: np.ndarray, settings: Settings) -> np.ndarray:
    """Find contour and return mask image with black background and white contour"""
    blured = cv2.blur(img, (3, 3))
    edges = cv2.Canny(blured, settings.lower, settings.upper)

    return edges
