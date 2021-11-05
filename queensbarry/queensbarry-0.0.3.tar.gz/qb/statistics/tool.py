import sys
import numpy as np
from numpy.typing import ArrayLike, NDArray
from typing import Union


def check_single_array(
        a: ArrayLike,
        *,
        is_clean: bool = False,
        is_flatten: bool = False,
        is_nan_warning: bool = False,
        nan_warning_criterion: float = 0.3
) -> NDArray:
    """
        检查并转换两个数组
        :param a: ArrayLike
        :param is_clean: 是否去除 nan 值
        :param is_flatten: 是否展平
        :param is_nan_warning: nan 值过多时是否提出 warning
        :param nan_warning_criterion: nan 值超过 size 的百分率 warning（仅在 is_nan_warning=True 时生效）
        :return:
        """
    a = np.asarray(a)

    if is_clean:
        a = a[~np.isnan(a)]

    if is_flatten:
        a = a.flatten()

    if is_nan_warning:
        _nan_warning(a, nan_warning_criterion=nan_warning_criterion)

    return a


def check_two_array(
        a: ArrayLike, b: ArrayLike,
        *,
        is_same_size: bool = False,
        is_same_shape: bool = False,
        is_clean_each: bool = False,
        is_clean_same_time: bool = False,
        is_flatten: bool = False,
        is_nan_warning: bool = False,
        nan_warning_criterion: float = 0.3
) -> (NDArray, NDArray):
    """
    检查并转换两个数组
    :param a: ArrayLike
    :param b: ArrayLike
    :param is_same_size: 是否检查相同 size
    :param is_same_shape: 是否检查相同 shape
    :param is_clean_each: 是否分别清理 nan 值
    :param is_clean_same_time: 是否由两个数组的 nan 值共同决定清洗
    :param is_flatten: 是否展平
    :param is_nan_warning: nan 值过多时是否提出 warning
    :param nan_warning_criterion: nan 值超过 size 的百分率 warning（仅在 is_nan_warning=True 时生效）
    :return:
    """
    a = np.asarray(a)
    b = np.asarray(b)

    if is_same_size:
        if a.size != b.size:
            raise ValueError(f'Expect two array have then same size, but got {a.size} and {b.size}')

    if is_same_shape:
        if a.shape != b.shape:
            raise ValueError(f'Expect two array have then same shape, but got {a.shape} and {b.shape}')

    if is_clean_each:
        a = a[~np.isnan(a)]
        b = b[~np.isnan(b)]
    if is_clean_same_time:
        not_nan = np.logical_not(np.logical_or(np.isnan(a), np.isnan(b)))
        a = a[not_nan]
        b = b[not_nan]

    if is_flatten:
        a = a.flatten()
        b = b.flatten()

    if is_nan_warning:
        _nan_warning(a, b, nan_warning_criterion=nan_warning_criterion)

    return a, b


def check_three_array(
        a: ArrayLike, b: ArrayLike, c: ArrayLike,
        *,
        is_same_size: bool = False,
        is_same_shape: bool = False,
        is_clean_each: bool = False,
        is_clean_same_time: bool = False,
        is_flatten: bool = False,
        is_nan_warning: bool = False,
        nan_warning_criterion: float = 0.3
):
    """
    检查并转换三个数组
    :param a: ArrayLike
    :param b: ArrayLike
    :param c: ArrayLike
    :param is_same_size: 是否检查相同 size
    :param is_same_shape: 是否检查相同 shape
    :param is_clean_each: 是否分别清理 nan 值
    :param is_clean_same_time: 是否由两个数组的 nan 值共同决定清洗
    :param is_flatten: 是否展平
    :param is_nan_warning: nan 值过多时是否提出 warning
    :param nan_warning_criterion: nan 值超过 size 的百分率 warning（仅在 is_nan_warning=True 时生效）
    :return:
    """
    a = np.asarray(a)
    b = np.asarray(b)
    c = np.asarray(c)

    if is_same_size:
        if a.size != b.size != b.size:
            raise ValueError(f'Expect two array have then same size, but got {a.size} and {b.size}')

    if is_same_shape:
        if a.shape != b.shape != c.shape:
            raise ValueError(f'Expect two array have then same shape, but got {a.shape} and {b.shape}')

    if is_clean_each:
        a = a[~np.isnan(a)]
        b = b[~np.isnan(b)]
        c = c[~np.isnan(c)]
    if is_clean_same_time:
        _t = np.logical_or(np.isnan(a), np.isnan(b))
        not_nan = np.logical_not(np.logical_or(_t, np.isnan(c)))
        a = a[not_nan]
        b = b[not_nan]
        c = c[not_nan]

    if is_flatten:
        a = a.flatten()
        b = b.flatten()
        c = c.flatten()

    if is_nan_warning:
        _nan_warning(a, b, c, nan_warning_criterion=nan_warning_criterion)

    return a, b, c


def _nan_warning(*arrays: ArrayLike, nan_warning_criterion: float):
    """
    （内部方法）封装 nan 值校验
    :param arrays:
    :param nan_warning_criterion:
    :return:
    """
    nan_warning_criterion = check_float(
        nan_warning_criterion,
        is_lower_closed=True,
        is_upper_closed=True,
        minimum=0, maximum=1
    )
    for array in arrays:
        if np.count_nonzero(np.isnan(array)) / array.size >= array.size * nan_warning_criterion:
            raise RuntimeWarning('Input array nan value have too much')


def check_int(
        a: Union[int, float],
        *,
        is_upper_closed: bool = False,
        is_lower_closed: bool = False,
        minimum: int = -sys.maxsize,
        maximum: int = sys.maxsize
) -> int:
    """
    检查整数是否在范围中
    :param a: 整数
    :param is_upper_closed: 上限是否为闭区间
    :param is_lower_closed: 下限是否为闭区间
    :param minimum: 区间最小值
    :param maximum: 区间最大值
    :return:
    """
    a = int(a)
    if not minimum <= a <= maximum:
        raise ValueError
    if not is_lower_closed and a == minimum:
        raise ValueError
    if not is_upper_closed and a == maximum:
        raise ValueError

    return a


def check_float(
        a: Union[int, float],
        *,
        is_upper_closed: bool = False,
        is_lower_closed: bool = False,
        minimum: int = -sys.maxsize,
        maximum: int = sys.maxsize
) -> float:
    """
    检查整数是否在范围中
    :param a: 整数
    :param is_upper_closed: 上限是否为闭区间
    :param is_lower_closed: 下限是否为闭区间
    :param minimum: 区间最小值
    :param maximum: 区间最大值
    :return:
    """
    a = float(a)
    if not minimum <= a <= maximum:
        raise ValueError
    if not is_lower_closed and a == minimum:
        raise ValueError
    if not is_upper_closed and a == maximum:
        raise ValueError

    return a


def rolling(a: ArrayLike, win: int):
    """
    滑动窗口
    :param a:
    :param win:
    :return:
    """
    a = np.asarray(a)
    win = check_int(win, minimum=1, maximum=np.min(a.shape), is_lower_closed=True, is_upper_closed=True)
    shape = (a.size - win + 1, win)
    strides = (a.itemsize, a.itemsize)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)
