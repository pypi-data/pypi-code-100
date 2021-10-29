import numpy as np
from colour import Color
from PIL import Image

from monochromist.math_version.classes import ImageInfo


def color_and_crop(image_info: ImageInfo) -> Image:
    """Color non-transparent pixels with selected color, then crop transparent pixels if needed"""

    color_as_tuple = color_to_tuple(image_info.settings.color)
    transparent = [0, 0, 0, 0]

    def color_row(row: np.array) -> np.array:
        return np.array([color_as_tuple if x else transparent for x in row])

    colored = np.apply_along_axis(color_row, 1, image_info.bool_array)
    new_image = Image.fromarray(np.uint8(colored), "RGBA")

    if image_info.settings.crop and image_info.bool_array.any():
        borders = find_borders(image_info.bool_array)
        new_image = new_image.crop(borders)

    return new_image


def color_to_tuple(color: Color) -> list[int]:
    """Convert color to RGBA tuple"""
    r, g, b = [int(255 * x) for x in color.rgb]
    alpha_channel = 255
    return [r, g, b, alpha_channel]


def find_borders(arr: np.array) -> tuple[int, int, int, int]:
    """Find transparent borders"""

    notna_columns = arr.any(axis=0)
    notna_rows = arr.any(axis=1)

    left = np.flatnonzero(notna_columns)[0]
    right = np.flatnonzero(notna_columns)[-1]

    upper = np.flatnonzero(notna_rows)[0]
    lower = np.flatnonzero(notna_rows)[-1]

    return left, upper, right, lower
