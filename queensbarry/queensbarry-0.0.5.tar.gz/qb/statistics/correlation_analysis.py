import numpy as np
import scipy as sp
import scipy.stats
from numpy.typing import ArrayLike
from .tool import check_single_array, check_three_array, check_int, rolling
from typing import NamedTuple
from collections import namedtuple


def partial3var(a: ArrayLike, b: ArrayLike, c: ArrayLike) -> NamedTuple:
    """
    三变量偏相关系数
    :param a:
    :param b:
    :param c:
    :return:
    """
    a, b, c = check_three_array(
        a, b, c,
        is_same_size=True,
        is_same_shape=True,
        is_clean_same_time=True,
        is_flatten=True
    )

    p_ab, _ = sp.stats.pearsonr(a, b)
    p_ac, _ = sp.stats.pearsonr(a, c)
    p_bc, _ = sp.stats.pearsonr(b, c)

    stat = (p_ab - p_ac * p_bc) / np.sqrt((1 - p_ac**2) * (1 - p_bc**2))

    t = stat * np.sqrt(a.size - 5) / np.sqrt(1 - stat**2)

    return namedtuple(
        'PartialThreeVariableResult',
        ('statistic', 'pvalue')
    )(t, sp.stats.t.sf(t, a.size - 5))
