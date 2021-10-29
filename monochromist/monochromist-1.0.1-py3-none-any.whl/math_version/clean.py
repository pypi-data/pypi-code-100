from copy import copy

import numpy as np
from PIL import Image, ImageFilter

from .classes import ImageInfo, Settings


def erase(img: Image, settings: Settings) -> ImageInfo:
    """Erases pixels and returns numpy array the same shape as image,
    filled with True (save pixel) and False (erase pixel), and settings that were used.
    Parameters will be used if they are defined, otherwise empirical approach will be used."""
    # Convert to grayscale
    converted = img.convert("L")

    # Blur filter is used to average background
    blured = converted.filter(ImageFilter.MedianFilter(settings.thickness))
    values = np.asarray(blured)

    updated_settings = copy(settings)
    if not settings.saving is None:
        threshold = user_percentile(values, settings)
    else:
        saving, threshold = empirical_percentile(values)
        updated_settings.saving = saving

    erased = values < threshold

    return ImageInfo(img, updated_settings, erased)


def user_percentile(arr: np.ndarray, settings: Settings) -> int:
    saving_safe_value = max(min(settings.saving, 100), 0)
    return np.asscalar(np.percentile(arr.flatten(), saving_safe_value, axis=0))


def empirical_percentile(arr: np.ndarray) -> tuple[int, int]:
    percentiles = [np.percentile(arr.flatten(), i, axis=0) for i in range(101)]
    # y = K * x + b
    K = 1.5
    b_values = np.array([y - K * x for (x, y) in enumerate(percentiles)])
    optimal_index = np.asscalar(np.argmax(b_values))
    optimal_percentile = percentiles[optimal_index]

    return optimal_index, optimal_percentile
