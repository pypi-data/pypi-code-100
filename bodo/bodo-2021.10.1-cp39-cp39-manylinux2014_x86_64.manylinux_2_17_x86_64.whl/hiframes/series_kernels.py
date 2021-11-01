"""Some kernels for Series related functions. This is a legacy file that needs to be
refactored.
"""
import datetime
import numba
import numpy as np
from numba.core import types
from numba.extending import overload, register_jitable
import bodo
from bodo.libs.int_arr_ext import IntDtype


def _column_filter_impl(B, ind):
    A = bodo.hiframes.rolling.alloc_shift(len(B), B, (-1,))
    for mqu__avk in numba.parfors.parfor.internal_prange(len(A)):
        if ind[mqu__avk]:
            A[mqu__avk] = B[mqu__avk]
        else:
            bodo.libs.array_kernels.setna(A, mqu__avk)
    return A


def _column_count_impl(A):
    numba.parfors.parfor.init_prange()
    count = 0
    for mqu__avk in numba.parfors.parfor.internal_prange(len(A)):
        if not bodo.libs.array_kernels.isna(A, mqu__avk):
            count += 1
    aseta__clfbu = count
    return aseta__clfbu


def _column_fillna_impl(A, B, fill):
    for mqu__avk in numba.parfors.parfor.internal_prange(len(A)):
        s = B[mqu__avk]
        if bodo.libs.array_kernels.isna(B, mqu__avk):
            s = fill
        A[mqu__avk] = s


@numba.njit(no_cpython_wrapper=True)
def _series_dropna_str_alloc_impl_inner(B):
    eia__los = len(B)
    fpw__dtg = 0
    for mqu__avk in range(len(B)):
        if bodo.libs.str_arr_ext.str_arr_is_na(B, mqu__avk):
            fpw__dtg += 1
    rdo__kebz = eia__los - fpw__dtg
    gxgl__xorj = bodo.libs.str_arr_ext.num_total_chars(B)
    A = bodo.libs.str_arr_ext.pre_alloc_string_array(rdo__kebz, gxgl__xorj)
    bodo.libs.str_arr_ext.copy_non_null_offsets(A, B)
    bodo.libs.str_arr_ext.copy_data(A, B)
    bodo.libs.str_arr_ext.set_null_bits_to_value(A, -1)
    return A


def _get_nan(val):
    return np.nan


@overload(_get_nan, no_unliteral=True)
def _get_nan_overload(val):
    if isinstance(val, (types.NPDatetime, types.NPTimedelta)):
        nat = val('NaT')
        return lambda val: nat
    if isinstance(val, types.Float):
        return lambda val: np.nan
    return lambda val: val


def _get_type_max_value(dtype):
    return 0


@overload(_get_type_max_value, inline='always', no_unliteral=True)
def _get_type_max_value_overload(dtype):
    if isinstance(dtype, (bodo.IntegerArrayType, IntDtype)):
        _dtype = dtype.dtype
        return lambda dtype: numba.cpython.builtins.get_type_max_value(_dtype)
    if dtype == bodo.datetime_date_array_type:
        return lambda dtype: _get_date_max_value()
    if isinstance(dtype.dtype, types.NPDatetime):
        return lambda dtype: bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
            numba.cpython.builtins.get_type_max_value(numba.core.types.int64))
    if isinstance(dtype.dtype, types.NPTimedelta):
        return (lambda dtype: bodo.hiframes.pd_timestamp_ext.
            integer_to_timedelta64(numba.cpython.builtins.
            get_type_max_value(numba.core.types.int64)))
    if dtype.dtype == types.bool_:
        return lambda dtype: True
    return lambda dtype: numba.cpython.builtins.get_type_max_value(dtype)


@register_jitable
def _get_date_max_value():
    return datetime.date(datetime.MAXYEAR, 12, 31)


def _get_type_min_value(dtype):
    return 0


@overload(_get_type_min_value, inline='always', no_unliteral=True)
def _get_type_min_value_overload(dtype):
    if isinstance(dtype, (bodo.IntegerArrayType, IntDtype)):
        _dtype = dtype.dtype
        return lambda dtype: numba.cpython.builtins.get_type_min_value(_dtype)
    if dtype == bodo.datetime_date_array_type:
        return lambda dtype: _get_date_min_value()
    if isinstance(dtype.dtype, types.NPDatetime):
        return lambda dtype: bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
            numba.cpython.builtins.get_type_min_value(numba.core.types.int64))
    if isinstance(dtype.dtype, types.NPTimedelta):
        return (lambda dtype: bodo.hiframes.pd_timestamp_ext.
            integer_to_timedelta64(numba.cpython.builtins.
            get_type_min_value(numba.core.types.uint64)))
    if dtype.dtype == types.bool_:
        return lambda dtype: False
    return lambda dtype: numba.cpython.builtins.get_type_min_value(dtype)


@register_jitable
def _get_date_min_value():
    return datetime.date(datetime.MINYEAR, 1, 1)


@overload(min)
def indval_min(a1, a2):
    if a1 == types.bool_ and a2 == types.bool_:

        def min_impl(a1, a2):
            if a1 > a2:
                return a2
            return a1
        return min_impl


@overload(max)
def indval_max(a1, a2):
    if a1 == types.bool_ and a2 == types.bool_:

        def max_impl(a1, a2):
            if a2 > a1:
                return a2
            return a1
        return max_impl


@numba.njit
def _sum_handle_nan(s, count):
    if not count:
        s = bodo.hiframes.series_kernels._get_nan(s)
    return s


@numba.njit
def _box_cat_val(s, cat_dtype, count):
    if s == -1 or count == 0:
        return bodo.hiframes.series_kernels._get_nan(cat_dtype.categories[0])
    return cat_dtype.categories[s]


@numba.generated_jit
def get_float_nan(s):
    nan = np.nan
    if s == types.float32:
        nan = np.float32('nan')
    return lambda s: nan


@numba.njit
def _mean_handle_nan(s, count):
    if not count:
        s = get_float_nan(s)
    else:
        s = s / count
    return s


@numba.njit
def _handle_nan_count(s, count):
    if count <= 1:
        s = np.nan
    else:
        s = s / (count - 1)
    return s


@numba.njit
def _var_handle_mincount(s, count, min_count):
    if count < min_count:
        aseta__clfbu = np.nan
    else:
        aseta__clfbu = s
    return aseta__clfbu


@numba.njit
def _handle_nan_count_ddof(s, count, ddof):
    if count <= ddof:
        s = np.nan
    else:
        s = s / (count - ddof)
    return s


@numba.njit
def lt_f(a, b):
    return a < b


@numba.njit
def gt_f(a, b):
    return a > b


@numba.njit
def compute_skew(first_moment, second_moment, third_moment, count):
    if count < 3:
        return np.nan
    hxz__rlzyv = first_moment / count
    pwmt__vspo = (third_moment - 3 * second_moment * hxz__rlzyv + 2 * count *
        hxz__rlzyv ** 3)
    bqyf__yyhh = second_moment - hxz__rlzyv * first_moment
    s = count * (count - 1) ** 1.5 / (count - 2
        ) * pwmt__vspo / bqyf__yyhh ** 1.5
    s = s / (count - 1)
    return s


@numba.njit
def compute_kurt(first_moment, second_moment, third_moment, fourth_moment,
    count):
    if count < 4:
        return np.nan
    hxz__rlzyv = first_moment / count
    ugmhq__zca = (fourth_moment - 4 * third_moment * hxz__rlzyv + 6 *
        second_moment * hxz__rlzyv ** 2 - 3 * count * hxz__rlzyv ** 4)
    idi__xbz = second_moment - hxz__rlzyv * first_moment
    qrhf__hroo = 3 * (count - 1) ** 2 / ((count - 2) * (count - 3))
    brwfg__lwwrd = count * (count + 1) * (count - 1) * ugmhq__zca
    nofn__kavu = (count - 2) * (count - 3) * idi__xbz ** 2
    s = (count - 1) * (brwfg__lwwrd / nofn__kavu - qrhf__hroo)
    s = s / (count - 1)
    return s
