from typing import Callable
from functools import wraps
from toolz import curry
import inspect
import numpy as np
import cupy
import cupyx
from cupyx.scipy import ndimage
from cupyx.scipy import signal
import napari
from napari_tools_menu import register_function

@curry
def plugin_function(
        function: Callable
) -> Callable:
    # copied from https://github.com/clEsperanto/pyclesperanto_prototype/blob/master/pyclesperanto_prototype/_tier0/_plugin_function.py
    @wraps(function)
    def worker_function(*args, **kwargs):
        sig = inspect.signature(function)
        # create mapping from position and keyword arguments to parameters
        # will raise a TypeError if the provided arguments do not match the signature
        # https://docs.python.org/3/library/inspect.html#inspect.Signature.bind
        bound = sig.bind(*args, **kwargs)
        # set default values for missing arguments
        # https://docs.python.org/3/library/inspect.html#inspect.BoundArguments.apply_defaults
        bound.apply_defaults()

        # copy images to GPU, and create output array if necessary
        for key, value in bound.arguments.items():
            if isinstance(value, np.ndarray):
                bound.arguments[key] = cupy.asarray(value)
            elif 'pyclesperanto_prototype._tier0._pycl.OCLArray' in str(type(value)):
                # compatibility with pyclesperanto
                bound.arguments[key] = cupy.asarray(np.asarray(value))

        # call the decorated function
        result = function(*bound.args, **bound.kwargs)

        if isinstance(result, cupy.ndarray):
            return np.asarray(result.get())
        else:
            return result

    return worker_function


@register_function(menu="Filtering > Gaussian (cupy)")
@plugin_function
def gaussian_filter(image: napari.types.ImageData, sigma: float = 2) -> napari.types.ImageData:
    return cupyx.scipy.ndimage.gaussian_filter(image.astype(float), sigma)


@register_function(menu="Filtering > Gaussian Laplace (cupy)")
@plugin_function
def gaussian_laplace(image: napari.types.ImageData, sigma: float = 2) -> napari.types.ImageData:
    return cupyx.scipy.ndimage.gaussian_laplace(image.astype(float), sigma)


@register_function(menu="Filtering > Median (cupy)")
@plugin_function
def median_filter(image: napari.types.ImageData, radius: float = 2) -> napari.types.ImageData:
    return cupyx.scipy.ndimage.median_filter(image.astype(float), size=radius * 2 + 1)


@register_function(menu="Filtering > Percentile (cupy)")
@plugin_function
def percentile_filter(image: napari.types.ImageData, percentile : float = 50, radius: float = 2) -> napari.types.ImageData:
    return cupyx.scipy.ndimage.percentile_filter(image.astype(float), percentile=percentile, size=radius * 2 + 1)


@register_function(menu="Filtering > Top-hat (white, cupy)")
@plugin_function
def white_tophat(image: napari.types.ImageData, radius: float = 2) -> napari.types.ImageData:
    return cupyx.scipy.ndimage.white_tophat(image.astype(float), size=radius * 2 + 1)


@register_function(menu="Filtering > Top-hat (black, cupy)")
@plugin_function
def black_tophat(image: napari.types.ImageData, radius: float = 2) -> napari.types.ImageData:
    return cupyx.scipy.ndimage.black_tophat(image.astype(float), size=radius * 2 + 1)


@register_function(menu="Filtering > Minimum (cupy)")
@plugin_function
def minimum_filter(image: napari.types.ImageData, radius: float = 2) -> napari.types.ImageData:
    return cupyx.scipy.ndimage.minimum_filter(image.astype(float), size=radius * 2 + 1)


@register_function(menu="Filtering > Maximum (cupy)")
@plugin_function
def maximum_filter(image: napari.types.ImageData, radius: float = 2) -> napari.types.ImageData:
    return cupyx.scipy.ndimage.maximum_filter(image.astype(float), size=radius * 2 + 1)


@register_function(menu="Filtering > Morphological Gradient (cupy)")
@plugin_function
def morphological_gradient(image: napari.types.ImageData, radius: float = 2) -> napari.types.ImageData:
    return cupyx.scipy.ndimage.morphological_gradient(image.astype(float), size=radius * 2 + 1)


@register_function(menu="Filtering > Morphological Laplace (cupy)")
@plugin_function
def morphological_laplace(image: napari.types.ImageData, radius: float = 2) -> napari.types.ImageData:
    return cupyx.scipy.ndimage.morphological_laplace(image.astype(float), size=radius * 2 + 1)


@register_function(menu="Filtering > Wiener (cupy)")
@plugin_function
def wiener(image: napari.types.ImageData, radius: float = 2) -> napari.types.ImageData:
    return signal.wiener(image.astype(float), radius * 2 + 1)


@register_function(menu="Segmentation > Threshold (Otsu et al 1979, scikit-image + cupy)")
@plugin_function
def threshold_otsu(image: napari.types.ImageData) -> napari.types.LabelsData:
    # adapted from https://github.com/clEsperanto/pyclesperanto_prototype/blob/master/pyclesperanto_prototype/_tier9/_threshold_otsu.py#L41

    minimum_intensity = image.min()
    maximum_intensity = image.max()

    range = maximum_intensity - minimum_intensity
    bin_centers = cupy.arange(256) * range / (255)

    histogram, _ = cupy.histogram(image, bins=256, range=(minimum_intensity, maximum_intensity))
    from skimage.filters import threshold_otsu

    threshold = threshold_otsu(hist=(histogram, bin_centers))

    return image > threshold


@register_function(menu="Segmentation > Binary fill holes (cupy)")
@plugin_function
def binary_fill_holes(binary_image: napari.types.LabelsData) -> napari.types.LabelsData:
    return cupyx.scipy.ndimage.binary_fill_holes(binary_image)


@register_function(menu="Segmentation > Connected component labeling (cupy)")
@plugin_function
def label(binary_image: napari.types.LabelsData) -> napari.types.LabelsData:
    result, _ = cupyx.scipy.ndimage.label(binary_image)
    return result

