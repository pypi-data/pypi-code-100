# UDFT: Unitary Discrete Fourier Transform (and related)
# Copyright (C) 2021 François Orieux <francois.orieux@universite-paris-saclay.fr>

# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

# For more information, please refer to <https://unlicense.org>

"""UDFT
====

Unitary discrete Fourier transform (and related)

This module implements unitary discrete Fourier transforms, which are
orthonormal. It is just a thin wrapper around Numpy or pyFFTW (maybe others in
the future), mainly done for my personal usage. They are useful for convolution
[1]: they respect the Perceval equality, the value of the null frequency is
equal to

 1
-- ∑ₙ xₙ.
√N

The transforms are always applied on the last axes for performances (C-order
array). For more flexible usage, you must use the numpy.fft functions directly.

"""

from typing import Optional, Sequence, Tuple

import numpy as np  # type: ignore
import numpy.fft as npfft  # type: ignore
from numpy import ndarray as array

LIB = "numpy"

try:
    import pyfftw  # type: ignore
    import pyfftw.interfaces.numpy_fft as fftw  # type: ignore

    pyfftw.config.NUM_THREADS = 4
except ImportError:
    pass


__author__ = "François Orieux"
__copyright__ = "2021, François Orieux <francois.orieux@universite-paris-saclay.fr>"
__credits__ = ["François Orieux"]
__license__ = "Public Domain"
__version__ = "3.3.0"
__maintainer__ = "François Orieux"
__email__ = "francois.orieux@universite-paris-saclay.fr"
__status__ = "stable"
__url__ = "https://github.com/forieux/udft"
__keywords__ = "fft, Fourier"


OptStr = Optional[str]
OptInt = Optional[int]

__all__ = [
    "dftn",
    "idftn",
    "dft",
    "idft",
    "dft2",
    "idft2",
    "rdftn",
    "irdftn",
    "rdft",
    "rdft2",
    "norm",
    "crandn",
    "ir2fr",
    "fr2ir",
    "diff_ir",
    "laplacian",
    "LIB",
]


def dftn(inarray: array, ndim: OptInt = None, lib: OptStr = None) -> array:
    """ND unitary discrete Fourier transform.

    Parameters
    ----------
    inarray : array-like
        The array to transform.
    ndim : int, optional
        The `ndim` last axes along which to compute the transform. All
        axes by default.
    lib : str, optional
        Specify the library to compute the Fourier transform. See `LIB` module
        variable for the default.

    Returns
    -------
    outarray : array-like
        The DFT of `inarray` with same shape.

    """
    if ndim is None:
        ndim = inarray.ndim
    if lib is None:
        lib = LIB

    if lib == "fftw":
        return fftw.fftn(inarray, axes=range(-ndim, 0), norm="ortho")
    elif lib == "numpy":
        return npfft.fftn(inarray, axes=range(-ndim, 0), norm="ortho")
    else:
        raise ValueError(f"{lib} is not a valid `lib` value.")


def idftn(inarray: array, ndim: OptInt = None, lib: OptStr = None) -> array:
    """ND unitary inverse discrete Fourier transform.

    Parameters
    ----------
    inarray : array-like
        The array to transform.
    ndim : int, optional
        The `ndim` last axes along wich to compute the transform. All
        axes by default.
    lib : str, optional
        Specify the library to compute the Fourier transform. See `LIB` module
        variable for the default.

    Returns
    -------
    outarray : array-like
        The IDFT of `inarray` with same shape.
    """
    if ndim is None:
        ndim = inarray.ndim
    if lib is None:
        lib = LIB

    if lib == "fftw":
        return fftw.ifftn(inarray, axes=range(-ndim, 0), norm="ortho")
    elif lib == "numpy":
        return npfft.ifftn(inarray, axes=range(-ndim, 0), norm="ortho")
    else:
        raise ValueError(f"{lib} is not a valid `lib` value.")


def dft(inarray: array, lib: OptStr = None) -> array:
    """1D unitary discrete Fourier transform.

    Compute the unitary discrete Fourier transform on the last 2 axes.

    Parameters
    ----------
    inarray : array-like
        The array to transform.
    lib : str, optional
        Specify the library to compute the Fourier transform. See `LIB` module
        variable for the default.

    Returns
    -------
    outarray : array-like
        The DFT of `inarray` with same shape.
    """
    return dftn(inarray, 1, lib=lib)


def idft(inarray: array, lib: OptStr = None) -> array:
    """1D unitary discrete Fourier transform.

    Compute the unitary discrete Fourier transform on the last axis.

    Parameters
    ----------
    inarray : array-like
        The array to transform.
    lib : str, optional
        Specify the library to compute the Fourier transform. See `LIB` module
        variable for the default.

    Returns
    -------
    outarray : array-like
        The DFT of `inarray` with same shape.
    """
    return idftn(inarray, 1, lib=lib)


def dft2(inarray: array, lib: OptStr = None) -> array:
    """2D unitary discrete Fourier transform.

    Compute the unitary discrete Fourier transform on the last 2 axes.

    Parameters
    ----------
    inarray : array-like
        The array to transform.
    lib : str, optional
        Specify the library to compute the Fourier transform. See `LIB` module
        variable for the default.

    Returns
    -------
    outarray : array-like
        The DFT of `inarray` with same shape.
    """
    return dftn(inarray, 2, lib=lib)


def idft2(inarray: array, lib: OptStr = None) -> array:
    """2D unitary inverse discrete Fourier transform.

    Compute the unitary IDFT on the last 2 axes.

    Parameters
    ----------
    inarray : array-like
        The array to transform.
    lib : str, optional
        Specify the library to compute the Fourier transform. See `LIB` module
        variable for the default.

    Returns
    -------
    outarray : array-like
        The IDFT of `inarray` with same shape.
    """
    return idftn(inarray, 2, lib=lib)


# \
def rdftn(inarray: array, ndim: OptInt = None, lib: OptStr = None) -> array:
    """ND real unitary discrete Fourier transform.

    Consider the Hermitian property of output when input has real values.

    Parameters
    ----------
    inarray : array-like
        The array of real values to transform.
    ndim : int, optional
        The `ndim` last axes along which to compute the transform. All
        axes by default.
    lib : str, optional
        Specify the library to compute the Fourier transform. See `LIB` module
        variable for the default.

    Returns
    -------
    outarray : array-like
        The real DFT of `inarray` (the last axe as N // 2 + 1 length).

    """
    if ndim is None:
        ndim = inarray.ndim
    if lib is None:
        lib = LIB

    if lib == "fftw":
        return fftw.rfftn(inarray, axes=range(-ndim, 0), norm="ortho")
    elif lib == "numpy":
        return npfft.rfftn(inarray, axes=range(-ndim, 0), norm="ortho")
    else:
        raise ValueError(f"{lib} is not a valid `lib` value.")


def irdftn(inarray: array, shape: Tuple[int, ...], lib: OptStr = None) -> array:
    """ND real unitary inverse discrete Fourier transform.

    Consider the Hermitian property of input and return real values.

    Parameters
    ----------
    inarray : array-like
        The array of complex values to transform.
    shape : tuple of int
        The output shape of the `len(shape)` last axes.
    lib : str, optional
        Specify the library to compute the Fourier transform. See `LIB` module
        variable for the default.

    Returns
    -------
    outarray : array-like
        The real IDFT of `inarray`.

    """
    if lib is None:
        lib = LIB

    if lib == "fftw":
        return fftw.irfftn(inarray, s=shape, axes=range(-len(shape), 0), norm="ortho")
    elif lib == "numpy":
        return npfft.irfftn(inarray, s=shape, axes=range(-len(shape), 0), norm="ortho")
    else:
        raise ValueError(f"{lib} is not a valid `lib` value.")


def rdft(inarray: array, lib: OptStr = None) -> array:
    """1D real unitary discrete Fourier transform.

    Compute the unitary real DFT on the last axis. Consider the Hermitian
    property of output when input has real values.

    Parameters
    ----------
    inarray : array-like
        The array to transform.
    lib : str, optional
        Specify the library to compute the Fourier transform. See `LIB` module
        variable for the default.

    Returns
    -------
    outarray : array-like
        The real DFT of `inarray`, where the last dim has length N//2+1.

    """
    return rdftn(inarray, 1, lib=lib)


def rdft2(inarray: array, lib: OptStr = None) -> array:
    """2D real unitary discrete Fourier transform.

    Compute the unitary real DFT on the last 2 axes. Consider the Hermitian
    property of output when input has real values.

    Parameters
    ----------
    inarray : array-like
        The array to transform.
    lib : str, optional
        Specify the library to compute the Fourier transform. See `LIB` module
        variable for the default.

    Returns
    -------
    outarray : array-like
        The real DFT of `inarray`, where the last dim has length N//2+1.

    """
    return rdftn(inarray, 2, lib=lib)


# \


def ir2fr(
    imp_resp: array,
    shape: Tuple[int, ...],
    origin: Optional[Sequence[int]] = None,
    real: bool = True,
) -> array:
    """Compute the frequency response from impulse responses.

    This function makes the necessary correct zero-padding, zero convention,
    correct DFT etc.

    The Fourier transform is performed on the last `len(shape)` dimensions for
    efficiency (C-order array). Use numpy implementation.

    Parameters
    ----------
    imp_resp : array-like
        The impulse responses.
    shape : tuple of int
        A tuple of integer corresponding to the target shape of the frequency
        responses, without hermitian property. The DFT is performed on the
        `len(shape)` last axes of ndarray.
    origin : tuple of int, optional
        The index of the origin (0, 0) of the impulse response. The center by
        default (shape[i] // 2).
    real : boolean, optional
        If True, `imp_resp` is supposed real, and read DFT is used.

    Returns
    -------
    out : array-like
      The frequency responses of shape `shape` on the last `len(shape)`
      dimensions.

    Notes
    -----
    - The output is returned as C-contiguous array.
    - For convolution, the result must be used with unitary discrete Fourier
      transform for the signal (udftn or equivalent).
    """
    if len(shape) > imp_resp.ndim:
        raise ValueError(
            "length of `shape` must be inferior or equal to `imp_resp.ndim`"
        )

    if origin is None:
        origin = [length // 2 for length in imp_resp.shape[-len(shape) :]]

    if len(origin) != len(shape):
        raise ValueError("`origin` and `shape` must have the same length")

    # Place the IR at the beginning of irpadded
    # ┌────────┬──────────────┐
    # │        │              │
    # │   IR   │              │
    # │        │              │
    # │        │              │
    # ├────────┘              │
    # │            0          │
    # │                       │
    # │                       │
    # │                       │
    # └───────────────────────┘
    irpadded = np.zeros(imp_resp.shape[: -len(shape)] + shape)  # zeros of target shape
    irpadded[tuple([slice(0, s) for s in imp_resp.shape])] = imp_resp

    # Roll (circshift in Matlab) to move the origin at index 0 (DFT hypothesis)
    # ┌────────┬──────────────┐     ┌────┬─────────────┬────┐
    # │11112222│              │     │4444│             │3333│
    # │11112222│              │     │4444│             │3333│
    # │33334444│              │     ├────┘             └────┤
    # │33334444│              │     │                       │
    # ├────────┘   0          │ ->  │           0           │
    # │                       │     │                       │
    # │                       │     ├────┐             ┌────┤
    # │                       │     │2222│             │1111│
    # │                       │     │2222│             │1111│
    # └───────────────────────┘     └────┴─────────────┴────┘
    for axe, shift in enumerate(origin):
        irpadded = np.roll(irpadded, -shift, imp_resp.ndim - len(shape) + axe)

    # Perform the DFT on the last axes
    if real:
        return np.ascontiguousarray(
            np.fft.rfftn(
                irpadded, axes=list(range(imp_resp.ndim - len(shape), imp_resp.ndim))
            )
        )
    return np.ascontiguousarray(
        np.fft.fftn(
            irpadded, axes=list(range(imp_resp.ndim - len(shape), imp_resp.ndim))
        )
    )


def fr2ir(
    freq_resp: array,
    shape: Tuple[int, ...],
    origin: Optional[Sequence[int]] = None,
    real: bool = True,
) -> array:
    """Return the impulse responses from frequency responses.

    This function makes the necessary correct zero-padding, zero convention,
    correct DFT etc. to compute the impulse responses from frequency responses.

    The IR array is supposed to have the origin in the middle of the array.

    The Fourier transform is performed on the last `len(shape)` dimensions for
    efficiency (C-order array). Use numpy implementation.

    Parameters
    ----------
    freq_resp : array-like
       The frequency responses.
    shape : tuple of int
       Output shape of the impulse responses.
    origin : tuple of int, optional
        The index of the origin (0, 0) of output the impulse response. The center by
        default (shape[i] // 2).
    real : boolean, optional
       If True, imp_resp is supposed real, and real DFT is used.

    Returns
    -------
    out : array-like
       The impulse responses of shape `shape` on the last `len(shape)` axes.

    Notes
    -----
    - The output is returned as C-contiguous array.
    - For convolution, the result has to be used with unitary discrete Fourier
      transform for the signal (udftn or equivalent).
    """
    if len(shape) > freq_resp.ndim:
        raise ValueError(
            "length of `shape` must be inferior or equal to `imp_resp.ndim`"
        )

    if origin is None:
        origin = [int(np.floor(length / 2)) for length in shape]

    if len(origin) != len(shape):
        raise ValueError("`origin` and `shape` must have the same length")

    if real:
        irpadded = np.fft.irfftn(
            freq_resp, axes=list(range(freq_resp.ndim - len(shape), freq_resp.ndim))
        )
    else:
        irpadded = np.fft.ifftn(
            freq_resp, axes=list(range(freq_resp.ndim - len(shape), freq_resp.ndim))
        )

    for axe, shift in enumerate(origin):
        irpadded = np.roll(irpadded, shift, freq_resp.ndim - len(shape) + axe)

    return np.ascontiguousarray(irpadded[tuple([slice(0, s) for s in shape])])


# \


def diff_ir(ndim, axis):
    """Return the impulse response of first order differences.

    Parameters
    ----------
    ndim : int
        The number of dimensions.
    axis : int
        The axis where the diff operates.

    Returns
    -------
    out : array_like
        The impulse response
    """
    assert ndim > 0, "The number of dimensions `ndim` must be strictly positive."
    assert axis < ndim, "The `axe` argument must be inferior to `ndim`."

    return np.reshape(
        np.array([0, -1, 1], ndmin=ndim), [1] * axis + [3] + [1] * (ndim - axis - 1)
    )


def laplacian(ndim: int) -> array:
    """Return the Laplacian impulse response.

    The second-order difference in each axes.

    Parameters
    ----------
    ndim : int
        The dimension of the Laplacian.

    Returns
    -------
    out : array_like
        The impulse response
    """
    imp = np.zeros([3] * ndim)
    for dim in range(ndim):
        idx = tuple(
            [slice(1, 2)] * dim + [slice(None)] + [slice(1, 2)] * (ndim - dim - 1)
        )
        imp[idx] = np.array([-1.0, 0.0, -1.0]).reshape(
            [-1 if i == dim else 1 for i in range(ndim)]
        )
    imp[tuple([slice(1, 2)] * ndim)] = 2.0 * ndim
    return imp


# \


def norm(inarray: array, hermitian: bool = True) -> float:
    """Return l2-norm of array in discrete Fourier space.

    Parameters
    ----------
    inarray : array-like
        The input array.
    hermitian : boolean, optional
        If True, `array` is supposed to contain half of the frequency plane.
    lib : str, optional
        Specify the library to compute the Fourier transform. See `LIB` module
        variable for the default.

    Returns
    -------
    norm : float

    """
    if hermitian:
        return 2 * np.sum(np.abs(inarray) ** 2) - np.sum(np.abs(inarray[..., 0]) ** 2)
    return np.sum(np.abs(inarray) ** 2)


def crandn(shape: Tuple[int, ...]) -> array:
    """Draw from white complex Normal.

    Draw unitary DFT of real white Gaussian field of zero mean and variance
    unity. Does not consider hermitian property, `shape` is supposed to consider
    half of the frequency plane already.
    """
    return np.sqrt(0.5) * (
        np.random.standard_normal(shape) + 1j * np.random.standard_normal(shape)
    )


### Local Variables:
### ispell-local-dictionary: "english"
### End:
