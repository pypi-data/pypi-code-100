from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike
from numpy.typing import DTypeLike

from . import mean  # noqa: F401
from ._version import version  # noqa: F401
from ._version import version_tuple  # noqa: F401


class scalar:
    r"""
    Ensemble average of a scalar.
    Add samples to it using :py:func:`scalar.add_sample`.
    The mean, variance, and standard deviation can be obtained at any time.
    Also the sums of the first and statistical moments, as well as the number of samples can be
    obtained at any time.

    Continue an old average by specifying:

    :param float first: Sum of the first moment.
    :param float second: Sum of the second moment.
    :param int norm: Number of samples.
    """

    def __init__(self, first: float = 0, second: float = 0, norm: float = 0):

        self.m_first = first
        self.m_second = second
        self.m_norm = norm

    def add_sample(self, data: ArrayLike):
        r"""
        Add a sample.
        Internally changes the sums of the first and second statistical moments and normalisation.

        :param data: Sample.
        """

        data = np.array(data)
        self.m_first += np.sum(data)
        self.m_second += np.sum(data ** 2)
        self.m_norm += data.size

    def mean(self):
        r"""
        Current mean.
        Samples can be added afterwards without any problems.

        :rtype: float
        :return: Mean.
        """

        if self.m_norm == 0:
            return np.NaN

        return self.m_first / self.m_norm

    def variance(self):
        r"""
        Current variance.
        Samples can be added afterwards without any problems.

        :rtype: float
        :return: Variance.
        """

        if self.m_norm <= 1:
            return np.NaN

        d = (self.m_second / self.m_norm - (self.m_first / self.m_norm) ** 2) * self.m_norm
        n = self.m_norm - 1

        return d / n

    def std(self):
        r"""
        Current standard deviation.
        Samples can be added afterwards without any problems.

        :rtype: float
        :return: Standard deviation.
        """

        return np.sqrt(self.variance())

    def norm(self):
        r"""
        Current normalisation: the number of samples.
        Samples can be added afterwards without any problems.

        :rtype: float
        :return: Normalisation.
        """

        return self.m_norm

    def first(self):
        r"""
        Current sum of the first statistical moment.
        Samples can be added afterwards without any problems.

        :rtype: float
        :return: First statistical moment.
        """

        return self.m_first

    def second(self):
        r"""
        Current sum of the second statistical moment.
        Samples can be added afterwards without any problems.

        :rtype: float
        :return: Second statistical moment.
        """

        return self.m_second


class static:
    r"""
    Ensemble average of an nd-array (of same size for all samples).
    Add samples to it using :py:func:`static.add_sample`.
    The mean, variance, and standard deviation can be obtained at any time.
    Also the sums of the first and statistical moments, as well as the number of samples can be
    obtained at any time.

    Continue an old average by specifying:

    :param compute_variance:
        If set ``False`` no second moment will be computed.
        In that case, the variance an standard deviation will not be available.

    :param shape, optional:
        The shape of the data.
        If not specified it is determined form the first sample.

    :param dtype, optional:
        The type of the data.
        If not specified it is determined form the first sample.

    :param first: Continued computation: Sum of the first moment.
    :param second: Continued computation: Sum of the second moment.
    :param norm: Continued computation: Number of samples (integer).
    """

    def __init__(
        self,
        compute_variance: bool = True,
        shape: tuple[int] = None,
        dtype: DTypeLike = None,
        first: ArrayLike = None,
        second: ArrayLike = None,
        norm: ArrayLike = None,
    ):

        if isinstance(shape, int):
            shape = (shape,)
        elif shape:
            shape = tuple(shape)

        self.m_compute_variance = compute_variance
        self.m_first = first
        self.m_second = second
        self.m_norm = norm
        self.m_shape = shape
        self.m_dtype = dtype

    def _allocate(self, data):

        if self.m_first is not None:
            assert data.shape == self.m_shape
            return

        self.m_shape = self.m_shape if self.m_shape is not None else data.shape
        self.m_dtype = self.m_dtype if self.m_dtype is not None else data.dtype

        self.m_norm = np.zeros(self.m_shape, np.int64)
        self.m_first = np.zeros(self.m_shape, self.m_dtype)

        if self.m_compute_variance:
            self.m_second = np.zeros(self.m_shape, self.m_dtype)

    def shape(self):
        r"""
        Data's shape.

        :rtype: list
        :return: Shape.
        """
        return self.m_shape

    def size(self):
        r"""
        Data's size.

        :rtype: int
        :return: Shape.
        """
        return np.prod(self.m_shape)

    def ravel(self):
        r"""
        Return as :py:class:`scalar`: all entries are summed.

        :rtype: :py:class:`scalar`
        :return: Ensemble average.
        """

        return scalar(
            first=np.sum(self.m_first),
            second=np.sum(self.m_second),
            norm=np.sum(self.m_norm),
        )

    def add_sample(self, data: ArrayLike, mask: ArrayLike = None):
        r"""
        Add a sample.
        Internally changes the sums of the first and second statistical moments and normalisation.

        :param data: The sample.
        :param mask: Mask entries (boolean array).
        """

        self._allocate(data)

        # masked data
        if mask is not None:
            incl = np.logical_not(mask)
            self.m_norm[incl] += 1
            self.m_first[incl] += data[incl]
            if self.m_compute_variance:
                self.m_second[incl] += data[incl] ** 2
            return

        # unmasked data
        self.m_norm += 1
        self.m_first += data
        if self.m_compute_variance:
            self.m_second += data ** 2

    def mean(self):
        r"""
        Current mean.
        Samples can be added afterwards without any problems.

        :rtype: ArrayLike, shape: :py:func:`static.shape`.
        :return: Mean.
        """

        if self.m_norm is None:
            return None

        n = np.where(self.m_norm > 0, self.m_norm, 1)
        ret = self.m_first / n
        return np.where(self.m_norm > 0, ret, np.NaN)

    def variance(self):
        r"""
        Current variance.
        Samples can be added afterwards without any problems.

        :rtype: ArrayLike, shape: :py:func:`static.shape`.
        :return: Variance.
        """

        if self.m_norm is None:
            return None

        assert self.m_compute_variance
        n = np.where(self.m_norm > 1, self.m_norm, 2)
        ret = (self.m_second / n - (self.m_first / n) ** 2) * n / (n - 1)
        return np.where(self.m_norm > 1, ret, np.NaN)

    def std(self):
        r"""
        Current standard deviation.
        Samples can be added afterwards without any problems.

        :rtype: ArrayLike, shape: :py:func:`static.shape`.
        :return: Standard deviation.
        """

        if self.m_norm is None:
            return None

        return np.sqrt(self.variance())

    def norm(self):
        r"""
        Current normalisation: the number of samples.
        Samples can be added afterwards without any problems.

        :rtype: ArrayLike, shape: :py:func:`static.shape`.
        :return: Normalisation.
        """

        return self.m_norm

    def first(self):
        r"""
        Current sum of the first statistical moment.
        Samples can be added afterwards without any problems.

        :rtype: ArrayLike, shape: :py:func:`static.shape`.
        :return: First statistical moment.
        """

        return self.m_first

    def second(self):
        r"""
        Current sum of the second statistical moment.
        Samples can be added afterwards without any problems.

        :rtype: ArrayLike, shape: :py:func:`static.shape`.
        :return: Second statistical moment.
        """

        assert self.m_compute_variance
        return self.m_second


def _expand_array1d(data, size):

    tmp = np.zeros((size), data.dtype)
    tmp[: data.size] = data
    return tmp


class dynamic1d(static):
    r"""
    Ensemble average of an 1d-array (which grows depending of the size of the samples).
    Add samples to it using :py:func:`dynamic1d.add_sample`.
    The mean, variance, and standard deviation can be obtained at any time.
    Also the sums of the first and statistical moments, as well as the number of samples can be
    obtained at any time.

    Continue an old average by specifying:

    :param compute_variance:
        If set ``False`` no second moment will be computed.
        In that case, the variance an standard deviation will not be available.

    :param size:
        The initial size of the data.
        If not specified it is determined form the first sample.

    :param dtype, optional:
        The type of the data.
        If not specified it is determined form the first sample.

    :param first: Continued computation: Sum of the first moment.
    :param second: Continued computation: Sum of the second moment.
    :param norm: Continued computation: Number of samples (integer).
    """

    def __init__(
        self,
        compute_variance: bool = True,
        size: int = None,
        dtype: DTypeLike = None,
        first: ArrayLike = None,
        second: ArrayLike = None,
        norm: ArrayLike = None,
    ):

        self.m_compute_variance = compute_variance
        self.m_first = first
        self.m_second = second
        self.m_norm = norm
        self.m_size = size
        self.m_shape = (self.m_size,)
        self.m_dtype = dtype

    def _allocate(self, data: ArrayLike):
        r"""
        Allocate data if necessary.
        """

        if self.m_first is not None:
            return

        self.m_size = self.m_size if self.m_size is not None else data.size
        self.m_dtype = self.m_dtype if self.m_dtype is not None else data.dtype
        self.m_shape = (self.m_size,)

        self.m_norm = np.zeros((self.m_size), np.int64)
        self.m_first = np.zeros((self.m_size), self.m_dtype)

        if self.m_compute_variance:
            self.m_second = np.zeros((self.m_size), self.m_dtype)

    def _expand(self, data: ArrayLike):

        if data.size <= self.m_size:
            return

        self.m_size = data.size
        self.m_shape = (self.m_size,)
        self.m_norm = _expand_array1d(self.m_norm, data.size)
        self.m_first = _expand_array1d(self.m_first, data.size)

        if self.m_compute_variance:
            self.m_second = _expand_array1d(self.m_second, data.size)

    def add_sample(self, data: ArrayLike):
        r"""
        Add a sample.
        Internally changes the sums of the first and second statistical moments and normalisation.

        :param data: Sample.
        """

        assert data.ndim == 1

        self._allocate(data)
        self._expand(data)

        self.m_norm[: data.size] += 1
        self.m_first[: data.size] += data

        if self.m_compute_variance:
            self.m_second[: data.size] += data ** 2


if __name__ == "__main__":
    pass
