from dataclasses import dataclass
from typing import Optional

import numpy as np
from colour import Color
from PIL import Image


@dataclass
class Settings:
    """Tools settings"""

    saving: Optional[int] = None
    """Defines what part of the pixels will be saved (not erased).
    From 0 (erase everything) to 100 (save everything)"""

    thickness: int = 3
    """Thickness of the line, used in algorithm to set blur radius"""

    color: Color = Color("black")
    """Color of the contour"""

    crop: bool = True
    """Crop empty pixels after converting"""


@dataclass
class ImageInfo:
    """Describes image with additional information"""

    original: Image
    """Original images"""

    settings: Settings
    """Settings that were used to process image"""

    bool_array: np.ndarray
    """2D array that represents used and unused pixels"""
