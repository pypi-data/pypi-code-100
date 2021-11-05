import numpy as np
from numpy.typing import ArrayLike
from .tool import check_two_array
from typing import Callable


def mean_error(a: ArrayLike, b: ArrayLike, *, is_nan_warning=True, nan_warning_criterion=0.3) -> float:
    """
    平均误差
    :param a: ArrayLike
    :param b: ArrayLike
    :param is_nan_warning: nan 值过多时是否提出 warning
    :param nan_warning_criterion: nan 值超过 size 的百分率 warning（仅在 is_nan_warning=True 时生效）
    :return: 平均误差值
    """
    a, b = check_two_array(
        a, b,
        is_same_size=True,
        is_same_shape=True,
        is_clean_same_time=True,
        is_nan_warning=is_nan_warning,
        nan_warning_criterion=nan_warning_criterion
    )

    return (a - b).sum() / a.size


def mean_absolute_error(a: ArrayLike, b: ArrayLike, *, is_nan_warning=True, nan_warning_criterion=0.3):
    """
    平均绝对误差
    :param a: ArrayLike
    :param b: ArrayLike
    :param is_nan_warning: nan 值过多时是否提出 warning
    :param nan_warning_criterion: nan 值超过 size 的百分率 warning（仅在 is_nan_warning=True 时生效）
    :return: 平均绝对误差值
    """
    a, b = check_two_array(
        a, b,
        is_same_size=True,
        is_same_shape=True,
        is_clean_same_time=True,
        is_nan_warning=is_nan_warning,
        nan_warning_criterion=nan_warning_criterion
    )

    return np.abs(a - b).sum() / a.size


def relative_absolute_error(a: ArrayLike, b: ArrayLike, *, is_nan_warning=True, nan_warning_criterion=0.3):
    """
    相对绝对误差
    :param a: ArrayLike
    :param b: ArrayLike
    :param is_nan_warning: nan 值过多时是否提出 warning
    :param nan_warning_criterion: nan 值超过 size 的百分率 warning（仅在 is_nan_warning=True 时生效）
    :return: 相对绝对误差值
    """
    a, b = check_two_array(
        a, b,
        is_same_size=True,
        is_same_shape=True,
        is_clean_same_time=True,
        is_nan_warning=is_nan_warning,
        nan_warning_criterion=nan_warning_criterion
    )

    return np.abs((a - b) / b).sum() / a.size


def root_mean_squared_error(a: ArrayLike, b: ArrayLike, *, is_nan_warning=True, nan_warning_criterion=0.3):
    """
    均方根误差
    :param a: ArrayLike
    :param b: ArrayLike
    :param is_nan_warning: nan 值过多时是否提出 warning
    :param nan_warning_criterion: nan 值超过 size 的百分率 warning（仅在 is_nan_warning=True 时生效）
    :return: 均方根误差值
    """
    a, b = check_two_array(
        a, b,
        is_same_size=True,
        is_same_shape=True,
        is_clean_same_time=True,
        is_nan_warning=is_nan_warning,
        nan_warning_criterion=nan_warning_criterion
    )

    return np.sqrt(np.power(a - b, 2).sum() / (a - b).sum())


def mean_squared_error(a: ArrayLike, b: ArrayLike, *, is_nan_warning=True, nan_warning_criterion=0.3):
    """
    均方误差
    :param a: ArrayLike
    :param b: ArrayLike
    :param is_nan_warning: nan 值过多时是否提出 warning
    :param nan_warning_criterion: nan 值超过 size 的百分率 warning（仅在 is_nan_warning=True 时生效）
    :return: 均方误差差值
    """
    a, b = check_two_array(
        a, b,
        is_same_size=True,
        is_same_shape=True,
        is_clean_same_time=True,
        is_nan_warning=is_nan_warning,
        nan_warning_criterion=nan_warning_criterion
    )

    return np.power(a - b, 2).sum() / (a - b).sum()


# --- 以下为别名 ---
me: Callable = mean_error
mae: Callable = mean_absolute_error
rae: Callable = relative_absolute_error
rmse: Callable = root_mean_squared_error
mse: Callable = mean_squared_error
