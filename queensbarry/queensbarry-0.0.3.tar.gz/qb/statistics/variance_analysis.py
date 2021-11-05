import numpy as np
import scipy as sp
import scipy.stats
from numpy.typing import ArrayLike
from .tool import check_two_array, check_single_array, check_int, rolling
from typing import NamedTuple
from collections import namedtuple


def difference_test(a: ArrayLike, b: ArrayLike) -> NamedTuple:
    """
    样本差异性检验，原假设为方差相等
    :param a: 样本 1
    :param b: 样本 2
    :return: VarianceDifference(coefficient, pvalue)
    """
    a, b = check_two_array(a, b, is_clean_each=True, is_flatten=True)

    f = a.var() / b.var()

    return namedtuple(
        'VarianceDifferenceResult',
        ('statistic', 'pvalue')
    )(f, 2 * sp.stats.f.sf(f, a.size - 1, b.size - 1))


def auto_cov(a: ArrayLike, tau: int = 0, bias: bool = False) -> float:
    """
    自协方差
    :param a: ArrayLike
    :param tau: 滞后步长
    :param bias:
        Default normalization (False) is by ``(N - 1)``, where ``N`` is the
        number of observations given (unbiased estimate). If `bias` is True,
        then normalization is by ``N``.
    :return:
    """
    a = check_single_array(a, is_clean=True, is_flatten=True)
    tau = check_int(tau, minimum=0, maximum=a.size - 1, is_lower_closed=True, is_upper_closed=True)
    s = rolling(a, tau + 1)

    return np.sum((s[:, 0] - a.mean()) * (s[:, -1] - a.mean())) / (a.size if bias else a.size - 1)


def cross_cov(a: ArrayLike, b: ArrayLike, tau: int = 0, bias: bool = False) -> float:
    """
    交叉协方差
    :param a: ArrayLike
    :param b: ArrayLike
    :param tau: 滞后步长
    :param bias:
        Default normalization (False) is by ``(N - 1)``, where ``N`` is the
        number of observations given (unbiased estimate). If `bias` is True,
        then normalization is by ``N``.
    :return:
    """
    a, b = check_two_array(
        a, b, is_same_size=True, is_same_shape=True,
        is_clean_same_time=True, is_flatten=True
    )
    tau = check_int(tau, minimum=0, maximum=a.size - 1, is_lower_closed=True, is_upper_closed=True)
    sa = rolling(a, tau + 1)
    sb = rolling(b, tau + 1)

    return np.sum((sa[:, 0] - a.mean()) * (sb[:, -1] - b.mean())) / (a.size if bias else a.size - 1)
