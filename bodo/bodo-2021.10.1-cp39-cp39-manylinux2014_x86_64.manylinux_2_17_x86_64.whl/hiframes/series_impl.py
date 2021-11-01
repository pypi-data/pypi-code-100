"""
Implementation of Series attributes and methods using overload.
"""
import operator
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_builtin, overload, overload_attribute, overload_method, register_jitable
import bodo
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.hiframes.datetime_timedelta_ext import PDTimeDeltaType, datetime_timedelta_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.pd_offsets_ext import is_offsets_type
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType, if_series_to_array_type
from bodo.hiframes.pd_timestamp_ext import PandasTimestampType, pd_timestamp_type
from bodo.hiframes.rolling import is_supported_shift_array_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import BinaryArrayType, binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, string_array_type
from bodo.libs.str_ext import string_type
from bodo.utils.transform import gen_const_tup, is_var_size_item_array_type
from bodo.utils.typing import BodoError, can_replace, check_unsupported_args, dtype_to_array_type, element_type, get_literal_value, get_overload_const_bytes, get_overload_const_int, get_overload_const_str, is_common_scalar_dtype, is_iterable_type, is_literal_type, is_overload_bool, is_overload_constant_bool, is_overload_constant_bytes, is_overload_constant_int, is_overload_constant_nan, is_overload_constant_str, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_overload_zero, is_scalar_type, raise_bodo_error


@overload_attribute(HeterogeneousSeriesType, 'index', inline='always')
@overload_attribute(SeriesType, 'index', inline='always')
def overload_series_index(s):
    return lambda s: bodo.hiframes.pd_series_ext.get_series_index(s)


@overload_attribute(HeterogeneousSeriesType, 'values', inline='always')
@overload_attribute(SeriesType, 'values', inline='always')
def overload_series_values(s):
    return lambda s: bodo.hiframes.pd_series_ext.get_series_data(s)


@overload_attribute(SeriesType, 'dtype', inline='always')
def overload_series_dtype(s):
    if s.dtype == bodo.string_type:
        raise BodoError('Series.dtype not supported for string Series yet')
    return lambda s: bodo.hiframes.pd_series_ext.get_series_data(s).dtype


@overload_attribute(HeterogeneousSeriesType, 'shape')
@overload_attribute(SeriesType, 'shape')
def overload_series_shape(s):
    return lambda s: (len(bodo.hiframes.pd_series_ext.get_series_data(s)),)


@overload_attribute(HeterogeneousSeriesType, 'ndim', inline='always')
@overload_attribute(SeriesType, 'ndim', inline='always')
def overload_series_ndim(s):
    return lambda s: 1


@overload_attribute(HeterogeneousSeriesType, 'size')
@overload_attribute(SeriesType, 'size')
def overload_series_size(s):
    return lambda s: len(bodo.hiframes.pd_series_ext.get_series_data(s))


@overload_attribute(HeterogeneousSeriesType, 'T', inline='always')
@overload_attribute(SeriesType, 'T', inline='always')
def overload_series_T(s):
    return lambda s: s


@overload_attribute(SeriesType, 'hasnans', inline='always')
def overload_series_hasnans(s):
    return lambda s: s.isna().sum() != 0


@overload_attribute(HeterogeneousSeriesType, 'empty')
@overload_attribute(SeriesType, 'empty')
def overload_series_empty(s):
    return lambda s: len(bodo.hiframes.pd_series_ext.get_series_data(s)) == 0


@overload_attribute(SeriesType, 'dtypes', inline='always')
def overload_series_dtypes(s):
    return lambda s: s.dtype


@overload_attribute(HeterogeneousSeriesType, 'name', inline='always')
@overload_attribute(SeriesType, 'name', inline='always')
def overload_series_name(s):
    return lambda s: bodo.hiframes.pd_series_ext.get_series_name(s)


@overload(len, no_unliteral=True)
def overload_series_len(S):
    if isinstance(S, (SeriesType, HeterogeneousSeriesType)):
        return lambda S: len(bodo.hiframes.pd_series_ext.get_series_data(S))


@overload_method(SeriesType, 'copy', inline='always', no_unliteral=True)
def overload_series_copy(S, deep=True):
    if is_overload_true(deep):

        def impl1(S, deep=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr.copy(),
                index, name)
        return impl1
    if is_overload_false(deep):

        def impl2(S, deep=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
        return impl2

    def impl(S, deep=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        if deep:
            arr = arr.copy()
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
    return impl


@overload_method(SeriesType, 'to_list', no_unliteral=True)
@overload_method(SeriesType, 'tolist', no_unliteral=True)
def overload_series_to_list(S):
    if isinstance(S.dtype, types.Float):

        def impl_float(S):
            joc__xrmj = list()
            for yccp__hnzd in range(len(S)):
                joc__xrmj.append(S.iat[yccp__hnzd])
            return joc__xrmj
        return impl_float

    def impl(S):
        joc__xrmj = list()
        for yccp__hnzd in range(len(S)):
            if bodo.libs.array_kernels.isna(S.values, yccp__hnzd):
                raise ValueError(
                    'Series.to_list(): Not supported for NA values with non-float dtypes'
                    )
            joc__xrmj.append(S.iat[yccp__hnzd])
        return joc__xrmj
    return impl


@overload_method(SeriesType, 'to_numpy', inline='always', no_unliteral=True)
def overload_series_to_numpy(S, dtype=None, copy=False, na_value=None):
    hvuw__yveso = dict(dtype=dtype, copy=copy, na_value=na_value)
    ltyv__lube = dict(dtype=None, copy=False, na_value=None)
    check_unsupported_args('Series.to_numpy', hvuw__yveso, ltyv__lube)

    def impl(S, dtype=None, copy=False, na_value=None):
        return S.values
    return impl


@overload_method(SeriesType, 'reset_index', inline='always', no_unliteral=True)
def overload_series_reset_index(S, level=None, drop=False, name=None,
    inplace=False):
    hvuw__yveso = dict(name=name, inplace=inplace)
    ltyv__lube = dict(name=None, inplace=False)
    check_unsupported_args('Series.reset_index', hvuw__yveso, ltyv__lube)
    if not bodo.hiframes.dataframe_impl._is_all_levels(S, level):
        raise_bodo_error(
            'Series.reset_index(): only dropping all index levels supported')
    if not is_overload_constant_bool(drop):
        raise_bodo_error(
            "Series.reset_index(): 'drop' parameter should be a constant boolean value"
            )
    if is_overload_true(drop):

        def impl_drop(S, level=None, drop=False, name=None, inplace=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_index_ext.init_range_index(0, len(arr),
                1, None)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
        return impl_drop

    def get_name_literal(name_typ, is_index=False, series_name=None):
        if is_overload_none(name_typ):
            if is_index:
                return 'index' if series_name != 'index' else 'level_0'
            return 0
        if is_literal_type(name_typ):
            return get_literal_value(name_typ)
        else:
            raise BodoError(
                'Series.reset_index() not supported for non-literal series names'
                )
    series_name = get_name_literal(S.name_typ)
    vqpy__laljf = get_name_literal(S.index.name_typ, True, series_name)
    ykcxf__rtwav = [vqpy__laljf, series_name]
    igzyi__qds = (
        'def _impl(S, level=None, drop=False, name=None, inplace=False):\n')
    igzyi__qds += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    igzyi__qds += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    igzyi__qds += """    df_index = bodo.hiframes.pd_index_ext.init_range_index(0, len(S), 1, None)
"""
    igzyi__qds += '    col_var = {}\n'.format(gen_const_tup(ykcxf__rtwav))
    igzyi__qds += """    return bodo.hiframes.pd_dataframe_ext.init_dataframe((index, arr), df_index, col_var)
"""
    pfwwr__zazwk = {}
    exec(igzyi__qds, {'bodo': bodo}, pfwwr__zazwk)
    gnv__htgo = pfwwr__zazwk['_impl']
    return gnv__htgo


@overload_method(SeriesType, 'isna', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'isnull', inline='always', no_unliteral=True)
def overload_series_isna(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        nvo__rzq = bodo.libs.array_ops.array_op_isna(arr)
        return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, index, name)
    return impl


@overload_method(SeriesType, 'round', inline='always', no_unliteral=True)
def overload_series_round(S, decimals=0):

    def impl(S, decimals=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(arr)
        nvo__rzq = bodo.utils.utils.alloc_type(n, arr, (-1,))
        for yccp__hnzd in numba.parfors.parfor.internal_prange(n):
            if pd.isna(arr[yccp__hnzd]):
                bodo.libs.array_kernels.setna(nvo__rzq, yccp__hnzd)
            else:
                nvo__rzq[yccp__hnzd] = np.round(arr[yccp__hnzd], decimals)
        return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, index, name)
    return impl


@overload_method(SeriesType, 'sum', inline='always', no_unliteral=True)
def overload_series_sum(S, axis=None, skipna=True, level=None, numeric_only
    =None, min_count=0):
    hvuw__yveso = dict(level=level, numeric_only=numeric_only)
    ltyv__lube = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sum', hvuw__yveso, ltyv__lube)
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError('Series.sum(): axis argument not supported')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None,
        min_count=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_sum(arr, skipna, min_count)
    return impl


@overload_method(SeriesType, 'prod', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'product', inline='always', no_unliteral=True)
def overload_series_prod(S, axis=None, skipna=True, level=None,
    numeric_only=None, min_count=0):
    hvuw__yveso = dict(level=level, numeric_only=numeric_only)
    ltyv__lube = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.product', hvuw__yveso, ltyv__lube)
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError('Series.product(): axis argument not supported')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None,
        min_count=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_prod(arr, skipna, min_count)
    return impl


@overload_method(SeriesType, 'any', inline='always', no_unliteral=True)
def overload_series_any(S, axis=0, bool_only=None, skipna=True, level=None):
    hvuw__yveso = dict(axis=axis, bool_only=bool_only, skipna=skipna, level
        =level)
    ltyv__lube = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.any', hvuw__yveso, ltyv__lube)

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        dicfb__pbbx = 0
        for yccp__hnzd in numba.parfors.parfor.internal_prange(len(A)):
            zfkb__iuv = 0
            if not bodo.libs.array_kernels.isna(A, yccp__hnzd):
                zfkb__iuv = int(A[yccp__hnzd])
            dicfb__pbbx += zfkb__iuv
        return dicfb__pbbx != 0
    return impl


@overload_method(SeriesType, 'equals', inline='always', no_unliteral=True)
def overload_series_equals(S, other):
    if not isinstance(other, SeriesType):
        raise BodoError("Series.equals() 'other' must be a Series")
    if isinstance(S.data, bodo.ArrayItemArrayType):
        raise BodoError(
            'Series.equals() not supported for Series where each element is an array or list'
            )
    if S.data != other.data:
        return lambda S, other: False

    def impl(S, other):
        vhfhn__xkiv = bodo.hiframes.pd_series_ext.get_series_data(S)
        oxma__pqnf = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        dicfb__pbbx = 0
        for yccp__hnzd in numba.parfors.parfor.internal_prange(len(vhfhn__xkiv)
            ):
            zfkb__iuv = 0
            thah__tvlzd = bodo.libs.array_kernels.isna(vhfhn__xkiv, yccp__hnzd)
            pilz__hpdrb = bodo.libs.array_kernels.isna(oxma__pqnf, yccp__hnzd)
            if (thah__tvlzd and not pilz__hpdrb or not thah__tvlzd and
                pilz__hpdrb):
                zfkb__iuv = 1
            elif not thah__tvlzd:
                if vhfhn__xkiv[yccp__hnzd] != oxma__pqnf[yccp__hnzd]:
                    zfkb__iuv = 1
            dicfb__pbbx += zfkb__iuv
        return dicfb__pbbx == 0
    return impl


@overload_method(SeriesType, 'all', inline='always', no_unliteral=True)
def overload_series_all(S, axis=0, bool_only=None, skipna=True, level=None):
    hvuw__yveso = dict(axis=axis, bool_only=bool_only, skipna=skipna, level
        =level)
    ltyv__lube = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.all', hvuw__yveso, ltyv__lube)

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        dicfb__pbbx = 0
        for yccp__hnzd in numba.parfors.parfor.internal_prange(len(A)):
            zfkb__iuv = 0
            if not bodo.libs.array_kernels.isna(A, yccp__hnzd):
                zfkb__iuv = int(not A[yccp__hnzd])
            dicfb__pbbx += zfkb__iuv
        return dicfb__pbbx == 0
    return impl


@overload_method(SeriesType, 'mad', inline='always', no_unliteral=True)
def overload_series_mad(S, axis=None, skipna=True, level=None):
    hvuw__yveso = dict(axis=axis, level=level)
    ltyv__lube = dict(axis=None, level=None)
    check_unsupported_args('Series.mad', hvuw__yveso, ltyv__lube)
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError('Series.mad(): axis argument not supported')
    zzuxv__zbulp = types.float64
    dmvh__qkdl = types.float64
    if S.dtype == types.float32:
        zzuxv__zbulp = types.float32
        dmvh__qkdl = types.float32
    nwnz__bnx = zzuxv__zbulp(0)
    uvj__cesz = dmvh__qkdl(0)
    wczk__hkztv = dmvh__qkdl(1)

    def impl(S, axis=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        zwdr__oon = nwnz__bnx
        dicfb__pbbx = uvj__cesz
        for yccp__hnzd in numba.parfors.parfor.internal_prange(len(A)):
            zfkb__iuv = nwnz__bnx
            doyn__rpy = uvj__cesz
            if not bodo.libs.array_kernels.isna(A, yccp__hnzd) or not skipna:
                zfkb__iuv = A[yccp__hnzd]
                doyn__rpy = wczk__hkztv
            zwdr__oon += zfkb__iuv
            dicfb__pbbx += doyn__rpy
        khio__zxgl = bodo.hiframes.series_kernels._mean_handle_nan(zwdr__oon,
            dicfb__pbbx)
        fior__zsv = nwnz__bnx
        for yccp__hnzd in numba.parfors.parfor.internal_prange(len(A)):
            zfkb__iuv = nwnz__bnx
            if not bodo.libs.array_kernels.isna(A, yccp__hnzd) or not skipna:
                zfkb__iuv = abs(A[yccp__hnzd] - khio__zxgl)
            fior__zsv += zfkb__iuv
        jcaf__otw = bodo.hiframes.series_kernels._mean_handle_nan(fior__zsv,
            dicfb__pbbx)
        return jcaf__otw
    return impl


@overload_method(SeriesType, 'mean', inline='always', no_unliteral=True)
def overload_series_mean(S, axis=None, skipna=None, level=None,
    numeric_only=None):
    if not isinstance(S.dtype, types.Number) and S.dtype not in [bodo.
        datetime64ns, types.bool_]:
        raise BodoError(f"Series.mean(): Series with type '{S}' not supported")
    hvuw__yveso = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    ltyv__lube = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.mean', hvuw__yveso, ltyv__lube)
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError('Series.mean(): axis argument not supported')

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_mean(arr)
    return impl


@overload_method(SeriesType, 'sem', inline='always', no_unliteral=True)
def overload_series_sem(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    hvuw__yveso = dict(level=level, numeric_only=numeric_only)
    ltyv__lube = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sem', hvuw__yveso, ltyv__lube)
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError('Series.sem(): axis argument not supported')

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        csx__fczx = 0
        vlj__ykxpm = 0
        dicfb__pbbx = 0
        for yccp__hnzd in numba.parfors.parfor.internal_prange(len(A)):
            zfkb__iuv = 0
            doyn__rpy = 0
            if not bodo.libs.array_kernels.isna(A, yccp__hnzd) or not skipna:
                zfkb__iuv = A[yccp__hnzd]
                doyn__rpy = 1
            csx__fczx += zfkb__iuv
            vlj__ykxpm += zfkb__iuv * zfkb__iuv
            dicfb__pbbx += doyn__rpy
        s = vlj__ykxpm - csx__fczx * csx__fczx / dicfb__pbbx
        vhoy__ryuyp = bodo.hiframes.series_kernels._handle_nan_count_ddof(s,
            dicfb__pbbx, ddof)
        jhro__sdbsr = (vhoy__ryuyp / dicfb__pbbx) ** 0.5
        return jhro__sdbsr
    return impl


@overload_method(SeriesType, 'kurt', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'kurtosis', inline='always', no_unliteral=True)
def overload_series_kurt(S, axis=0, skipna=True, level=None, numeric_only=None
    ):
    hvuw__yveso = dict(axis=axis, level=level, numeric_only=numeric_only)
    ltyv__lube = dict(axis=0, level=None, numeric_only=None)
    check_unsupported_args('Series.kurtosis', hvuw__yveso, ltyv__lube)

    def impl(S, axis=0, skipna=True, level=None, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        csx__fczx = 0.0
        vlj__ykxpm = 0.0
        bgz__vfv = 0.0
        hefb__dtq = 0.0
        dicfb__pbbx = 0
        for yccp__hnzd in numba.parfors.parfor.internal_prange(len(A)):
            zfkb__iuv = 0.0
            doyn__rpy = 0
            if not bodo.libs.array_kernels.isna(A, yccp__hnzd) or not skipna:
                zfkb__iuv = np.float64(A[yccp__hnzd])
                doyn__rpy = 1
            csx__fczx += zfkb__iuv
            vlj__ykxpm += zfkb__iuv ** 2
            bgz__vfv += zfkb__iuv ** 3
            hefb__dtq += zfkb__iuv ** 4
            dicfb__pbbx += doyn__rpy
        vhoy__ryuyp = bodo.hiframes.series_kernels.compute_kurt(csx__fczx,
            vlj__ykxpm, bgz__vfv, hefb__dtq, dicfb__pbbx)
        return vhoy__ryuyp
    return impl


@overload_method(SeriesType, 'skew', inline='always', no_unliteral=True)
def overload_series_skew(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    hvuw__yveso = dict(level=level, numeric_only=numeric_only)
    ltyv__lube = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.skew', hvuw__yveso, ltyv__lube)
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError('Series.skew(): axis argument not supported')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        csx__fczx = 0.0
        vlj__ykxpm = 0.0
        bgz__vfv = 0.0
        dicfb__pbbx = 0
        for yccp__hnzd in numba.parfors.parfor.internal_prange(len(A)):
            zfkb__iuv = 0.0
            doyn__rpy = 0
            if not bodo.libs.array_kernels.isna(A, yccp__hnzd) or not skipna:
                zfkb__iuv = np.float64(A[yccp__hnzd])
                doyn__rpy = 1
            csx__fczx += zfkb__iuv
            vlj__ykxpm += zfkb__iuv ** 2
            bgz__vfv += zfkb__iuv ** 3
            dicfb__pbbx += doyn__rpy
        vhoy__ryuyp = bodo.hiframes.series_kernels.compute_skew(csx__fczx,
            vlj__ykxpm, bgz__vfv, dicfb__pbbx)
        return vhoy__ryuyp
    return impl


@overload_method(SeriesType, 'var', inline='always', no_unliteral=True)
def overload_series_var(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    hvuw__yveso = dict(level=level, numeric_only=numeric_only)
    ltyv__lube = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.var', hvuw__yveso, ltyv__lube)
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError('Series.var(): axis argument not supported')

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_var(arr, skipna, ddof)
    return impl


@overload_method(SeriesType, 'std', inline='always', no_unliteral=True)
def overload_series_std(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    hvuw__yveso = dict(level=level, numeric_only=numeric_only)
    ltyv__lube = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.std', hvuw__yveso, ltyv__lube)
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError('Series.std(): axis argument not supported')

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_std(arr, skipna, ddof)
    return impl


@overload_method(SeriesType, 'dot', inline='always', no_unliteral=True)
def overload_series_dot(S, other):

    def impl(S, other):
        vhfhn__xkiv = bodo.hiframes.pd_series_ext.get_series_data(S)
        oxma__pqnf = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        zet__cyg = 0
        for yccp__hnzd in numba.parfors.parfor.internal_prange(len(vhfhn__xkiv)
            ):
            hxqh__scsx = vhfhn__xkiv[yccp__hnzd]
            viy__pql = oxma__pqnf[yccp__hnzd]
            zet__cyg += hxqh__scsx * viy__pql
        return zet__cyg
    return impl


@overload_method(SeriesType, 'cumsum', inline='always', no_unliteral=True)
def overload_series_cumsum(S, axis=0, skipna=True):
    hvuw__yveso = dict(axis=axis, skipna=skipna)
    ltyv__lube = dict(axis=0, skipna=True)
    check_unsupported_args('Series.cumsum', hvuw__yveso, ltyv__lube)

    def impl(S, axis=0, skipna=True):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(A.cumsum(), index, name)
    return impl


@overload_method(SeriesType, 'cumprod', inline='always', no_unliteral=True)
def overload_series_cumprod(S, axis=0, skipna=True):
    hvuw__yveso = dict(axis=axis, skipna=skipna)
    ltyv__lube = dict(axis=0, skipna=True)
    check_unsupported_args('Series.cumprod', hvuw__yveso, ltyv__lube)

    def impl(S, axis=0, skipna=True):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(A.cumprod(), index, name
            )
    return impl


@overload_method(SeriesType, 'cummin', inline='always', no_unliteral=True)
def overload_series_cummin(S, axis=0, skipna=True):
    hvuw__yveso = dict(axis=axis, skipna=skipna)
    ltyv__lube = dict(axis=0, skipna=True)
    check_unsupported_args('Series.cummax', hvuw__yveso, ltyv__lube)

    def impl(S, axis=0, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.cummin(arr), index, name)
    return impl


@overload_method(SeriesType, 'cummax', inline='always', no_unliteral=True)
def overload_series_cummax(S, axis=0, skipna=True):
    hvuw__yveso = dict(axis=axis, skipna=skipna)
    ltyv__lube = dict(axis=0, skipna=True)
    check_unsupported_args('Series.cummax', hvuw__yveso, ltyv__lube)

    def impl(S, axis=0, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.cummax(arr), index, name)
    return impl


@overload_method(SeriesType, 'rename', inline='always', no_unliteral=True)
def overload_series_rename(S, index=None, axis=None, copy=True, inplace=
    False, level=None, errors='ignore'):
    if not (index == bodo.string_type or isinstance(index, types.StringLiteral)
        ):
        raise BodoError("Series.rename() 'index' can only be a string")
    hvuw__yveso = dict(copy=copy, inplace=inplace, level=level, errors=errors)
    ltyv__lube = dict(copy=True, inplace=False, level=None, errors='ignore')
    check_unsupported_args('Series.rename', hvuw__yveso, ltyv__lube)

    def impl(S, index=None, axis=None, copy=True, inplace=False, level=None,
        errors='ignore'):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        nuzqn__fwad = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_series_ext.init_series(A, nuzqn__fwad, index)
    return impl


@overload_method(SeriesType, 'abs', inline='always', no_unliteral=True)
def overload_series_abs(S):

    def impl(S):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(np.abs(A), index, name)
    return impl


@overload_method(SeriesType, 'count', no_unliteral=True)
def overload_series_count(S, level=None):
    hvuw__yveso = dict(level=level)
    ltyv__lube = dict(level=None)
    check_unsupported_args('Series.count', hvuw__yveso, ltyv__lube)

    def impl(S, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_count(A)
    return impl


@overload_method(SeriesType, 'corr', inline='always', no_unliteral=True)
def overload_series_corr(S, other, method='pearson', min_periods=None):
    hvuw__yveso = dict(method=method, min_periods=min_periods)
    ltyv__lube = dict(method='pearson', min_periods=None)
    check_unsupported_args('Series.corr', hvuw__yveso, ltyv__lube)

    def impl(S, other, method='pearson', min_periods=None):
        n = S.count()
        rkcnv__dxm = S.sum()
        iyoco__lxjs = other.sum()
        a = n * (S * other).sum() - rkcnv__dxm * iyoco__lxjs
        wbdu__jyv = n * (S ** 2).sum() - rkcnv__dxm ** 2
        otrq__hhluz = n * (other ** 2).sum() - iyoco__lxjs ** 2
        return a / np.sqrt(wbdu__jyv * otrq__hhluz)
    return impl


@overload_method(SeriesType, 'cov', inline='always', no_unliteral=True)
def overload_series_cov(S, other, min_periods=None, ddof=1):
    hvuw__yveso = dict(min_periods=min_periods)
    ltyv__lube = dict(min_periods=None)
    check_unsupported_args('Series.cov', hvuw__yveso, ltyv__lube)

    def impl(S, other, min_periods=None, ddof=1):
        rkcnv__dxm = S.mean()
        iyoco__lxjs = other.mean()
        yve__rsx = ((S - rkcnv__dxm) * (other - iyoco__lxjs)).sum()
        N = np.float64(S.count() - ddof)
        nonzero_len = S.count() * other.count()
        return _series_cov_helper(yve__rsx, N, nonzero_len)
    return impl


def _series_cov_helper(sum_val, N, nonzero_len):
    return


@overload(_series_cov_helper, no_unliteral=True)
def _overload_series_cov_helper(sum_val, N, nonzero_len):

    def impl(sum_val, N, nonzero_len):
        if not nonzero_len:
            return np.nan
        if N <= 0.0:
            xksmd__ajxr = np.sign(sum_val)
            return np.inf * xksmd__ajxr
        return sum_val / N
    return impl


@overload_method(SeriesType, 'min', inline='always', no_unliteral=True)
def overload_series_min(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    hvuw__yveso = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    ltyv__lube = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.min', hvuw__yveso, ltyv__lube)
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError('Series.min(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.min(): only ordered categoricals are possible')

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_min(arr)
    return impl


@overload(max, no_unliteral=True)
def overload_series_builtins_max(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.max()
        return impl


@overload(min, no_unliteral=True)
def overload_series_builtins_min(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.min()
        return impl


@overload(sum, no_unliteral=True)
def overload_series_builtins_sum(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.sum()
        return impl


@overload(np.prod, inline='always', no_unliteral=True)
def overload_series_np_prod(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.prod()
        return impl


@overload_method(SeriesType, 'max', inline='always', no_unliteral=True)
def overload_series_max(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    hvuw__yveso = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    ltyv__lube = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.max', hvuw__yveso, ltyv__lube)
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError('Series.max(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.max(): only ordered categoricals are possible')

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_max(arr)
    return impl


@overload_method(SeriesType, 'idxmin', inline='always', no_unliteral=True)
def overload_series_idxmin(S, axis=0, skipna=True):
    hvuw__yveso = dict(axis=axis, skipna=skipna)
    ltyv__lube = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmin', hvuw__yveso, ltyv__lube)
    if not (S.dtype == types.none or bodo.utils.utils.is_np_array_typ(S.
        data) and (S.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
        isinstance(S.dtype, (types.Number, types.Boolean))) or isinstance(S
        .data, (bodo.IntegerArrayType, bodo.CategoricalArrayType)) or S.
        data in [bodo.boolean_array, bodo.datetime_date_array_type]):
        raise BodoError(
            f'Series.idxmin() only supported for numeric array types. Array type: {S.data} not supported.'
            )
    if isinstance(S.data, bodo.CategoricalArrayType) and not S.dtype.ordered:
        raise BodoError(
            'Series.idxmin(): only ordered categoricals are possible')

    def impl(S, axis=0, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.libs.array_ops.array_op_idxmin(arr, index)
    return impl


@overload_method(SeriesType, 'idxmax', inline='always', no_unliteral=True)
def overload_series_idxmax(S, axis=0, skipna=True):
    hvuw__yveso = dict(axis=axis, skipna=skipna)
    ltyv__lube = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmax', hvuw__yveso, ltyv__lube)
    if not (S.dtype == types.none or bodo.utils.utils.is_np_array_typ(S.
        data) and (S.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
        isinstance(S.dtype, (types.Number, types.Boolean))) or isinstance(S
        .data, (bodo.IntegerArrayType, bodo.CategoricalArrayType)) or S.
        data in [bodo.boolean_array, bodo.datetime_date_array_type]):
        raise BodoError(
            f'Series.idxmax() only supported for numeric array types. Array type: {S.data} not supported.'
            )
    if isinstance(S.data, bodo.CategoricalArrayType) and not S.dtype.ordered:
        raise BodoError(
            'Series.idxmax(): only ordered categoricals are possible')

    def impl(S, axis=0, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.libs.array_ops.array_op_idxmax(arr, index)
    return impl


@overload_attribute(SeriesType, 'is_monotonic', inline='always')
@overload_attribute(SeriesType, 'is_monotonic_increasing', inline='always')
def overload_series_is_monotonic_increasing(S):
    return lambda S: bodo.libs.array_kernels.series_monotonicity(bodo.
        hiframes.pd_series_ext.get_series_data(S), 1)


@overload_attribute(SeriesType, 'is_monotonic_decreasing', inline='always')
def overload_series_is_monotonic_decreasing(S):
    return lambda S: bodo.libs.array_kernels.series_monotonicity(bodo.
        hiframes.pd_series_ext.get_series_data(S), 2)


@overload_attribute(SeriesType, 'nbytes', inline='always')
def overload_series_nbytes(S):
    return lambda S: bodo.hiframes.pd_series_ext.get_series_data(S).nbytes


@overload_method(SeriesType, 'autocorr', inline='always', no_unliteral=True)
def overload_series_autocorr(S, lag=1):
    return lambda S, lag=1: bodo.libs.array_kernels.autocorr(bodo.hiframes.
        pd_series_ext.get_series_data(S), lag)


@overload_method(SeriesType, 'median', inline='always', no_unliteral=True)
def overload_series_median(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    hvuw__yveso = dict(level=level, numeric_only=numeric_only)
    ltyv__lube = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.median', hvuw__yveso, ltyv__lube)
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError('Series.median(): axis argument not supported')
    return (lambda S, axis=None, skipna=True, level=None, numeric_only=None:
        bodo.libs.array_ops.array_op_median(bodo.hiframes.pd_series_ext.
        get_series_data(S), skipna))


def overload_series_head(S, n=5):

    def impl(S, n=5):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mpq__tqjr = arr[:n]
        kbcy__zaxuu = index[:n]
        return bodo.hiframes.pd_series_ext.init_series(mpq__tqjr,
            kbcy__zaxuu, name)
    return impl


@lower_builtin('series.head', SeriesType, types.Integer)
@lower_builtin('series.head', SeriesType, types.Omitted)
def series_head_lower(context, builder, sig, args):
    impl = overload_series_head(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@numba.extending.register_jitable
def tail_slice(k, n):
    if n == 0:
        return k
    return -n


@overload_method(SeriesType, 'tail', inline='always', no_unliteral=True)
def overload_series_tail(S, n=5):
    if not is_overload_int(n):
        raise BodoError("Series.tail(): 'n' must be an Integer")

    def impl(S, n=5):
        mrp__iasy = tail_slice(len(S), n)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mpq__tqjr = arr[mrp__iasy:]
        kbcy__zaxuu = index[mrp__iasy:]
        return bodo.hiframes.pd_series_ext.init_series(mpq__tqjr,
            kbcy__zaxuu, name)
    return impl


@overload_method(SeriesType, 'nlargest', inline='always', no_unliteral=True)
def overload_series_nlargest(S, n=5, keep='first'):
    hvuw__yveso = dict(keep=keep)
    ltyv__lube = dict(keep='first')
    check_unsupported_args('Series.nlargest', hvuw__yveso, ltyv__lube)

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        chv__twj = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        nvo__rzq, ktl__xpvb = bodo.libs.array_kernels.nlargest(arr,
            chv__twj, n, True, bodo.hiframes.series_kernels.gt_f)
        uwzni__tzd = bodo.utils.conversion.convert_to_index(ktl__xpvb)
        return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, uwzni__tzd,
            name)
    return impl


@overload_method(SeriesType, 'nsmallest', inline='always', no_unliteral=True)
def overload_series_nsmallest(S, n=5, keep='first'):
    hvuw__yveso = dict(keep=keep)
    ltyv__lube = dict(keep='first')
    check_unsupported_args('Series.nsmallest', hvuw__yveso, ltyv__lube)

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        chv__twj = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        nvo__rzq, ktl__xpvb = bodo.libs.array_kernels.nlargest(arr,
            chv__twj, n, False, bodo.hiframes.series_kernels.lt_f)
        uwzni__tzd = bodo.utils.conversion.convert_to_index(ktl__xpvb)
        return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, uwzni__tzd,
            name)
    return impl


@overload_method(SeriesType, 'notnull', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'notna', inline='always', no_unliteral=True)
def overload_series_notna(S):
    return lambda S: S.isna() == False


@overload_method(SeriesType, 'astype', inline='always', no_unliteral=True)
def overload_series_astype(S, dtype, copy=True, errors='raise',
    _bodo_nan_to_str=True):
    hvuw__yveso = dict(errors=errors)
    ltyv__lube = dict(errors='raise')
    check_unsupported_args('Series.astype', hvuw__yveso, ltyv__lube)
    if dtype == types.unicode_type:
        raise_bodo_error(
            "Series.astype(): 'dtype' when passed as string must be a constant value"
            )

    def impl(S, dtype, copy=True, errors='raise', _bodo_nan_to_str=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        nvo__rzq = bodo.utils.conversion.fix_arr_dtype(arr, dtype, copy,
            nan_to_str=_bodo_nan_to_str, from_series=True)
        return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, index, name)
    return impl


@overload_method(SeriesType, 'take', inline='always', no_unliteral=True)
def overload_series_take(S, indices, axis=0, is_copy=True):
    hvuw__yveso = dict(axis=axis, is_copy=is_copy)
    ltyv__lube = dict(axis=0, is_copy=True)
    check_unsupported_args('Series.take', hvuw__yveso, ltyv__lube)
    if not (is_iterable_type(indices) and isinstance(indices.dtype, types.
        Integer)):
        raise BodoError(
            f"Series.take() 'indices' must be an array-like and contain integers. Found type {indices}."
            )

    def impl(S, indices, axis=0, is_copy=True):
        kzeii__fbvv = bodo.utils.conversion.coerce_to_ndarray(indices)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr[kzeii__fbvv],
            index[kzeii__fbvv], name)
    return impl


@overload_method(SeriesType, 'argsort', inline='always', no_unliteral=True)
def overload_series_argsort(S, axis=0, kind='quicksort', order=None):
    hvuw__yveso = dict(axis=axis, kind=kind, order=order)
    ltyv__lube = dict(axis=0, kind='quicksort', order=None)
    check_unsupported_args('Series.argsort', hvuw__yveso, ltyv__lube)

    def impl(S, axis=0, kind='quicksort', order=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        n = len(arr)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        qqj__vuus = S.notna().values
        if not qqj__vuus.all():
            nvo__rzq = np.full(n, -1, np.int64)
            nvo__rzq[qqj__vuus] = argsort(arr[qqj__vuus])
        else:
            nvo__rzq = argsort(arr)
        return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, index, name)
    return impl


@overload_method(SeriesType, 'sort_index', inline='always', no_unliteral=True)
def overload_series_sort_index(S, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    hvuw__yveso = dict(axis=axis, level=level, inplace=inplace, kind=kind,
        sort_remaining=sort_remaining, ignore_index=ignore_index, key=key)
    ltyv__lube = dict(axis=0, level=None, inplace=False, kind='quicksort',
        sort_remaining=True, ignore_index=False, key=None)
    check_unsupported_args('Series.sort_index', hvuw__yveso, ltyv__lube)

    def impl(S, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        kty__joua = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col3_',))
        vuh__hde = kty__joua.sort_index(ascending=ascending, inplace=
            inplace, na_position=na_position)
        nvo__rzq = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(vuh__hde,
            0)
        uwzni__tzd = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            vuh__hde)
        return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, uwzni__tzd,
            name)
    return impl


@overload_method(SeriesType, 'sort_values', inline='always', no_unliteral=True)
def overload_series_sort_values(S, axis=0, ascending=True, inplace=False,
    kind='quicksort', na_position='last', ignore_index=False, key=None):
    hvuw__yveso = dict(axis=axis, inplace=inplace, kind=kind, ignore_index=
        ignore_index, key=key)
    ltyv__lube = dict(axis=0, inplace=False, kind='quicksort', ignore_index
        =False, key=None)
    check_unsupported_args('Series.sort_values', hvuw__yveso, ltyv__lube)

    def impl(S, axis=0, ascending=True, inplace=False, kind='quicksort',
        na_position='last', ignore_index=False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        kty__joua = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col_',))
        vuh__hde = kty__joua.sort_values(['$_bodo_col_'], ascending=
            ascending, inplace=inplace, na_position=na_position)
        nvo__rzq = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(vuh__hde,
            0)
        uwzni__tzd = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            vuh__hde)
        return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, uwzni__tzd,
            name)
    return impl


def get_bin_inds(bins, arr):
    return arr


@overload(get_bin_inds, inline='always', no_unliteral=True)
def overload_get_bin_inds(bins, arr, is_nullable=True, include_lowest=True):
    assert is_overload_constant_bool(is_nullable)
    sdk__bgfg = is_overload_true(is_nullable)
    igzyi__qds = (
        'def impl(bins, arr, is_nullable=True, include_lowest=True):\n')
    igzyi__qds += '  numba.parfors.parfor.init_prange()\n'
    igzyi__qds += '  n = len(arr)\n'
    if sdk__bgfg:
        igzyi__qds += (
            '  out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
    else:
        igzyi__qds += '  out_arr = np.empty(n, np.int64)\n'
    igzyi__qds += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    igzyi__qds += '    if bodo.libs.array_kernels.isna(arr, i):\n'
    if sdk__bgfg:
        igzyi__qds += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        igzyi__qds += '      out_arr[i] = -1\n'
    igzyi__qds += '      continue\n'
    igzyi__qds += '    val = arr[i]\n'
    igzyi__qds += '    if include_lowest and val == bins[0]:\n'
    igzyi__qds += '      ind = 1\n'
    igzyi__qds += '    else:\n'
    igzyi__qds += '      ind = np.searchsorted(bins, val)\n'
    igzyi__qds += '    if ind == 0 or ind == len(bins):\n'
    if sdk__bgfg:
        igzyi__qds += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        igzyi__qds += '      out_arr[i] = -1\n'
    igzyi__qds += '    else:\n'
    igzyi__qds += '      out_arr[i] = ind - 1\n'
    igzyi__qds += '  return out_arr\n'
    pfwwr__zazwk = {}
    exec(igzyi__qds, {'bodo': bodo, 'np': np, 'numba': numba}, pfwwr__zazwk)
    impl = pfwwr__zazwk['impl']
    return impl


@register_jitable
def _round_frac(x, precision: int):
    if not np.isfinite(x) or x == 0:
        return x
    else:
        uyh__iawa, doib__pxj = np.divmod(x, 1)
        if uyh__iawa == 0:
            yznwx__rpsut = -int(np.floor(np.log10(abs(doib__pxj)))
                ) - 1 + precision
        else:
            yznwx__rpsut = precision
        return np.around(x, yznwx__rpsut)


@register_jitable
def _infer_precision(base_precision: int, bins) ->int:
    for precision in range(base_precision, 20):
        hjaem__ekh = np.array([_round_frac(b, precision) for b in bins])
        if len(np.unique(hjaem__ekh)) == len(bins):
            return precision
    return base_precision


def get_bin_labels(bins):
    pass


@overload(get_bin_labels, no_unliteral=True)
def overload_get_bin_labels(bins, right=True, include_lowest=True):
    dtype = np.float64 if isinstance(bins.dtype, types.Integer) else bins.dtype
    if dtype == bodo.datetime64ns:
        ozptb__fuy = bodo.timedelta64ns(1)

        def impl_dt64(bins, right=True, include_lowest=True):
            nkla__jzhoh = bins.copy()
            if right and include_lowest:
                nkla__jzhoh[0] = nkla__jzhoh[0] - ozptb__fuy
            yrk__qbm = bodo.libs.interval_arr_ext.init_interval_array(
                nkla__jzhoh[:-1], nkla__jzhoh[1:])
            return bodo.hiframes.pd_index_ext.init_interval_index(yrk__qbm,
                None)
        return impl_dt64

    def impl(bins, right=True, include_lowest=True):
        base_precision = 3
        precision = _infer_precision(base_precision, bins)
        nkla__jzhoh = np.array([_round_frac(b, precision) for b in bins],
            dtype=dtype)
        if right and include_lowest:
            nkla__jzhoh[0] = nkla__jzhoh[0] - 10.0 ** -precision
        yrk__qbm = bodo.libs.interval_arr_ext.init_interval_array(nkla__jzhoh
            [:-1], nkla__jzhoh[1:])
        return bodo.hiframes.pd_index_ext.init_interval_index(yrk__qbm, None)
    return impl


def get_output_bin_counts(count_series, nbins):
    pass


@overload(get_output_bin_counts, no_unliteral=True)
def overload_get_output_bin_counts(count_series, nbins):

    def impl(count_series, nbins):
        sjvhu__xtms = bodo.hiframes.pd_series_ext.get_series_data(count_series)
        igder__whqq = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(count_series))
        nvo__rzq = np.zeros(nbins, np.int64)
        for yccp__hnzd in range(len(sjvhu__xtms)):
            nvo__rzq[igder__whqq[yccp__hnzd]] = sjvhu__xtms[yccp__hnzd]
        return nvo__rzq
    return impl


def compute_bins(nbins, min_val, max_val):
    pass


@overload(compute_bins, no_unliteral=True)
def overload_compute_bins(nbins, min_val, max_val, right=True):

    def impl(nbins, min_val, max_val, right=True):
        if nbins < 1:
            raise ValueError('`bins` should be a positive integer.')
        min_val = min_val + 0.0
        max_val = max_val + 0.0
        if np.isinf(min_val) or np.isinf(max_val):
            raise ValueError(
                'cannot specify integer `bins` when input data contains infinity'
                )
        elif min_val == max_val:
            min_val -= 0.001 * abs(min_val) if min_val != 0 else 0.001
            max_val += 0.001 * abs(max_val) if max_val != 0 else 0.001
            bins = np.linspace(min_val, max_val, nbins + 1, endpoint=True)
        else:
            bins = np.linspace(min_val, max_val, nbins + 1, endpoint=True)
            zlt__jxn = (max_val - min_val) * 0.001
            if right:
                bins[0] -= zlt__jxn
            else:
                bins[-1] += zlt__jxn
        return bins
    return impl


@overload_method(SeriesType, 'value_counts', inline='always', no_unliteral=True
    )
def overload_series_value_counts(S, normalize=False, sort=True, ascending=
    False, bins=None, dropna=True, _index_name=None):
    hvuw__yveso = dict(dropna=dropna)
    ltyv__lube = dict(dropna=True)
    check_unsupported_args('Series.value_counts', hvuw__yveso, ltyv__lube)
    epvc__nqjvu = not is_overload_none(bins)
    igzyi__qds = 'def impl(\n'
    igzyi__qds += '    S,\n'
    igzyi__qds += '    normalize=False,\n'
    igzyi__qds += '    sort=True,\n'
    igzyi__qds += '    ascending=False,\n'
    igzyi__qds += '    bins=None,\n'
    igzyi__qds += '    dropna=True,\n'
    igzyi__qds += (
        '    _index_name=None,  # bodo argument. See groupby.value_counts\n')
    igzyi__qds += '):\n'
    igzyi__qds += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    igzyi__qds += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    igzyi__qds += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    if epvc__nqjvu:
        igzyi__qds += '    right = True\n'
        igzyi__qds += _gen_bins_handling(bins, S.dtype)
        igzyi__qds += '    arr = get_bin_inds(bins, arr)\n'
    igzyi__qds += (
        '    in_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
    igzyi__qds += "        (arr,), index, ('$_bodo_col2_',)\n"
    igzyi__qds += '    )\n'
    igzyi__qds += "    count_series = in_df.groupby('$_bodo_col2_').size()\n"
    if epvc__nqjvu:
        igzyi__qds += """    count_series = bodo.gatherv(count_series, allgather=True, warn_if_rep=False)
"""
        igzyi__qds += (
            '    count_arr = get_output_bin_counts(count_series, len(bins) - 1)\n'
            )
        igzyi__qds += '    index = get_bin_labels(bins)\n'
    else:
        igzyi__qds += (
            '    count_arr = bodo.hiframes.pd_series_ext.get_series_data(count_series)\n'
            )
        igzyi__qds += '    ind_arr = bodo.utils.conversion.coerce_to_array(\n'
        igzyi__qds += (
            '        bodo.hiframes.pd_series_ext.get_series_index(count_series)\n'
            )
        igzyi__qds += '    )\n'
        igzyi__qds += """    index = bodo.utils.conversion.index_from_array(ind_arr, name=_index_name)
"""
    igzyi__qds += (
        '    res = bodo.hiframes.pd_series_ext.init_series(count_arr, index, name)\n'
        )
    if is_overload_true(sort):
        igzyi__qds += '    res = res.sort_values(ascending=ascending)\n'
    if is_overload_true(normalize):
        psnp__snjl = 'len(S)' if epvc__nqjvu else 'count_arr.sum()'
        igzyi__qds += f'    res = res / float({psnp__snjl})\n'
    igzyi__qds += '    return res\n'
    pfwwr__zazwk = {}
    exec(igzyi__qds, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, pfwwr__zazwk)
    impl = pfwwr__zazwk['impl']
    return impl


def _gen_bins_handling(bins, dtype):
    igzyi__qds = ''
    if isinstance(bins, types.Integer):
        igzyi__qds += '    min_val = bodo.libs.array_ops.array_op_min(arr)\n'
        igzyi__qds += '    max_val = bodo.libs.array_ops.array_op_max(arr)\n'
        if dtype == bodo.datetime64ns:
            igzyi__qds += '    min_val = min_val.value\n'
            igzyi__qds += '    max_val = max_val.value\n'
        igzyi__qds += (
            '    bins = compute_bins(bins, min_val, max_val, right)\n')
        if dtype == bodo.datetime64ns:
            igzyi__qds += (
                "    bins = bins.astype(np.int64).view(np.dtype('datetime64[ns]'))\n"
                )
    else:
        igzyi__qds += (
            '    bins = bodo.utils.conversion.coerce_to_ndarray(bins)\n')
    return igzyi__qds


@overload(pd.cut, inline='always', no_unliteral=True)
def overload_cut(x, bins, right=True, labels=None, retbins=False, precision
    =3, include_lowest=False, duplicates='raise', ordered=True):
    hvuw__yveso = dict(right=right, labels=labels, retbins=retbins,
        precision=precision, duplicates=duplicates, ordered=ordered)
    ltyv__lube = dict(right=True, labels=None, retbins=False, precision=3,
        duplicates='raise', ordered=True)
    check_unsupported_args('pd.cut', hvuw__yveso, ltyv__lube)
    igzyi__qds = 'def impl(\n'
    igzyi__qds += '    x,\n'
    igzyi__qds += '    bins,\n'
    igzyi__qds += '    right=True,\n'
    igzyi__qds += '    labels=None,\n'
    igzyi__qds += '    retbins=False,\n'
    igzyi__qds += '    precision=3,\n'
    igzyi__qds += '    include_lowest=False,\n'
    igzyi__qds += "    duplicates='raise',\n"
    igzyi__qds += '    ordered=True\n'
    igzyi__qds += '):\n'
    if isinstance(x, SeriesType):
        igzyi__qds += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(x)\n')
        igzyi__qds += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(x)\n')
        igzyi__qds += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(x)\n')
    else:
        igzyi__qds += '    arr = bodo.utils.conversion.coerce_to_array(x)\n'
    igzyi__qds += _gen_bins_handling(bins, x.dtype)
    igzyi__qds += '    arr = get_bin_inds(bins, arr, False, include_lowest)\n'
    igzyi__qds += (
        '    label_index = get_bin_labels(bins, right, include_lowest)\n')
    igzyi__qds += """    cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(label_index, ordered, None)
"""
    igzyi__qds += """    out_arr = bodo.hiframes.pd_categorical_ext.init_categorical_array(arr, cat_dtype)
"""
    if isinstance(x, SeriesType):
        igzyi__qds += (
            '    res = bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        igzyi__qds += '    return res\n'
    else:
        igzyi__qds += '    return out_arr\n'
    pfwwr__zazwk = {}
    exec(igzyi__qds, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, pfwwr__zazwk)
    impl = pfwwr__zazwk['impl']
    return impl


def _get_q_list(q):
    return q


@overload(_get_q_list, no_unliteral=True)
def get_q_list_overload(q):
    if is_overload_int(q):
        return lambda q: np.linspace(0, 1, q + 1)
    return lambda q: q


@overload(pd.qcut, inline='always', no_unliteral=True)
def overload_qcut(x, q, labels=None, retbins=False, precision=3, duplicates
    ='raise'):
    hvuw__yveso = dict(labels=labels, retbins=retbins, precision=precision,
        duplicates=duplicates)
    ltyv__lube = dict(labels=None, retbins=False, precision=3, duplicates=
        'raise')
    check_unsupported_args('pd.qcut', hvuw__yveso, ltyv__lube)
    if not (is_overload_int(q) or is_iterable_type(q)):
        raise BodoError(
            "pd.qcut(): 'q' should be an integer or a list of quantiles")

    def impl(x, q, labels=None, retbins=False, precision=3, duplicates='raise'
        ):
        grlfb__gazq = _get_q_list(q)
        arr = bodo.utils.conversion.coerce_to_array(x)
        bins = bodo.libs.array_ops.array_op_quantile(arr, grlfb__gazq)
        return pd.cut(x, bins, include_lowest=True)
    return impl


@overload_method(SeriesType, 'groupby', inline='always', no_unliteral=True)
def overload_series_groupby(S, by=None, axis=0, level=None, as_index=True,
    sort=True, group_keys=True, squeeze=False, observed=True, dropna=True):
    hvuw__yveso = dict(axis=axis, group_keys=group_keys, squeeze=squeeze,
        observed=observed, dropna=dropna)
    ltyv__lube = dict(axis=0, group_keys=True, squeeze=False, observed=True,
        dropna=True)
    check_unsupported_args('Series.groupby', hvuw__yveso, ltyv__lube)
    if not is_overload_true(as_index):
        raise BodoError('as_index=False only valid with DataFrame')
    if is_overload_none(by) and is_overload_none(level):
        raise BodoError("You have to supply one of 'by' and 'level'")
    if not is_overload_none(by) and not is_overload_none(level):
        raise BodoError(
            "Series.groupby(): 'level' argument should be None if 'by' is not None"
            )
    if not is_overload_none(level):
        if not (is_overload_constant_int(level) and get_overload_const_int(
            level) == 0) or isinstance(S.index, bodo.hiframes.
            pd_multi_index_ext.MultiIndexType):
            raise BodoError(
                "Series.groupby(): MultiIndex case or 'level' other than 0 not supported yet"
                )

        def impl_index(S, by=None, axis=0, level=None, as_index=True, sort=
            True, group_keys=True, squeeze=False, observed=True, dropna=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            eqn__wgif = bodo.utils.conversion.coerce_to_array(index)
            kty__joua = bodo.hiframes.pd_dataframe_ext.init_dataframe((
                eqn__wgif, arr), index, (' ', ''))
            return kty__joua.groupby(' ')['']
        return impl_index
    nll__zwjst = by
    if isinstance(by, SeriesType):
        nll__zwjst = by.data
    if isinstance(nll__zwjst, DecimalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with decimal type is not supported yet.'
            )
    if isinstance(by, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with categorical type is not supported yet.'
            )

    def impl(S, by=None, axis=0, level=None, as_index=True, sort=True,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        eqn__wgif = bodo.utils.conversion.coerce_to_array(by)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        kty__joua = bodo.hiframes.pd_dataframe_ext.init_dataframe((
            eqn__wgif, arr), index, (' ', ''))
        return kty__joua.groupby(' ')['']
    return impl


@overload_method(SeriesType, 'append', inline='always', no_unliteral=True)
def overload_series_append(S, to_append, ignore_index=False,
    verify_integrity=False):
    hvuw__yveso = dict(verify_integrity=verify_integrity)
    ltyv__lube = dict(verify_integrity=False)
    check_unsupported_args('Series.append', hvuw__yveso, ltyv__lube)
    if isinstance(to_append, SeriesType):
        return (lambda S, to_append, ignore_index=False, verify_integrity=
            False: pd.concat((S, to_append), ignore_index=ignore_index,
            verify_integrity=verify_integrity))
    if isinstance(to_append, types.BaseTuple):
        return (lambda S, to_append, ignore_index=False, verify_integrity=
            False: pd.concat((S,) + to_append, ignore_index=ignore_index,
            verify_integrity=verify_integrity))
    return (lambda S, to_append, ignore_index=False, verify_integrity=False:
        pd.concat([S] + to_append, ignore_index=ignore_index,
        verify_integrity=verify_integrity))


@overload_method(SeriesType, 'isin', inline='always', no_unliteral=True)
def overload_series_isin(S, values):
    if bodo.utils.utils.is_array_typ(values):

        def impl_arr(S, values):
            vsgw__gqycv = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(A)
            nvo__rzq = np.empty(n, np.bool_)
            bodo.libs.array.array_isin(nvo__rzq, A, vsgw__gqycv, False)
            return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, index,
                name)
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(S, values):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        nvo__rzq = bodo.libs.array_ops.array_op_isin(A, values)
        return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, index, name)
    return impl


@overload_method(SeriesType, 'quantile', inline='always', no_unliteral=True)
def overload_series_quantile(S, q=0.5, interpolation='linear'):
    hvuw__yveso = dict(interpolation=interpolation)
    ltyv__lube = dict(interpolation='linear')
    check_unsupported_args('Series.quantile', hvuw__yveso, ltyv__lube)
    if is_iterable_type(q) and isinstance(q.dtype, types.Number):

        def impl_list(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            nvo__rzq = bodo.libs.array_ops.array_op_quantile(arr, q)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            index = bodo.hiframes.pd_index_ext.init_numeric_index(bodo.
                utils.conversion.coerce_to_array(q), None)
            return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, index,
                name)
        return impl_list
    elif isinstance(q, (float, types.Number)) or is_overload_constant_int(q):

        def impl(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            return bodo.libs.array_ops.array_op_quantile(arr, q)
        return impl
    else:
        raise BodoError(
            f'Series.quantile() q type must be float or iterable of floats only.'
            )


@overload_method(SeriesType, 'nunique', inline='always', no_unliteral=True)
def overload_series_nunique(S, dropna=True):
    if not is_overload_bool(dropna):
        raise BodoError('Series.nunique: dropna must be a boolean value')

    def impl(S, dropna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_kernels.nunique(arr, dropna)
    return impl


@overload_method(SeriesType, 'unique', inline='always', no_unliteral=True)
def overload_series_unique(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        ujmy__llym = bodo.libs.array_kernels.unique(arr)
        return bodo.allgatherv(ujmy__llym, False)
    return impl


@overload_method(SeriesType, 'describe', inline='always', no_unliteral=True)
def overload_series_describe(S, percentiles=None, include=None, exclude=
    None, datetime_is_numeric=True):
    hvuw__yveso = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    ltyv__lube = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('Series.describe', hvuw__yveso, ltyv__lube)
    if not (isinstance(S.data, types.Array) and (isinstance(S.data.dtype,
        types.Number) or S.data.dtype == bodo.datetime64ns)
        ) and not isinstance(S.data, IntegerArrayType):
        raise BodoError(f'describe() column input type {S.data} not supported.'
            )
    if S.data.dtype == bodo.datetime64ns:

        def impl_dt(S, percentiles=None, include=None, exclude=None,
            datetime_is_numeric=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
                array_ops.array_op_describe(arr), bodo.utils.conversion.
                convert_to_index(['count', 'mean', 'min', '25%', '50%',
                '75%', 'max']), name)
        return impl_dt

    def impl(S, percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.array_ops.
            array_op_describe(arr), bodo.utils.conversion.convert_to_index(
            ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']), name)
    return impl


@overload_method(SeriesType, 'memory_usage', inline='always', no_unliteral=True
    )
def overload_series_memory_usage(S, index=True, deep=False):
    if is_overload_true(index):

        def impl(S, index=True, deep=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            return arr.nbytes + index.nbytes
        return impl
    else:

        def impl(S, index=True, deep=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            return arr.nbytes
        return impl


def binary_str_fillna_inplace_series_impl(is_binary=False):
    if is_binary:
        yukpp__yvwge = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        yukpp__yvwge = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    igzyi__qds = 'def impl(\n'
    igzyi__qds += '    S,\n'
    igzyi__qds += '    value=None,\n'
    igzyi__qds += '    method=None,\n'
    igzyi__qds += '    axis=None,\n'
    igzyi__qds += '    inplace=False,\n'
    igzyi__qds += '    limit=None,\n'
    igzyi__qds += '    downcast=None,\n'
    igzyi__qds += '):  # pragma: no cover\n'
    igzyi__qds += (
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    igzyi__qds += (
        '    fill_arr = bodo.hiframes.pd_series_ext.get_series_data(value)\n')
    igzyi__qds += '    n = len(in_arr)\n'
    igzyi__qds += f'    out_arr = {yukpp__yvwge}(n, -1)\n'
    igzyi__qds += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    igzyi__qds += '        s = in_arr[j]\n'
    igzyi__qds += """        if bodo.libs.array_kernels.isna(in_arr, j) and not bodo.libs.array_kernels.isna(
"""
    igzyi__qds += '            fill_arr, j\n'
    igzyi__qds += '        ):\n'
    igzyi__qds += '            s = fill_arr[j]\n'
    igzyi__qds += '        out_arr[j] = s\n'
    igzyi__qds += (
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)\n'
        )
    ypnu__euz = dict()
    exec(igzyi__qds, {'bodo': bodo, 'numba': numba}, ypnu__euz)
    bdrw__xoszr = ypnu__euz['impl']
    return bdrw__xoszr


def binary_str_fillna_inplace_impl(is_binary=False):
    if is_binary:
        yukpp__yvwge = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        yukpp__yvwge = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    igzyi__qds = 'def impl(S,\n'
    igzyi__qds += '     value=None,\n'
    igzyi__qds += '    method=None,\n'
    igzyi__qds += '    axis=None,\n'
    igzyi__qds += '    inplace=False,\n'
    igzyi__qds += '    limit=None,\n'
    igzyi__qds += '   downcast=None,\n'
    igzyi__qds += '):\n'
    igzyi__qds += (
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    igzyi__qds += '    n = len(in_arr)\n'
    igzyi__qds += f'    out_arr = {yukpp__yvwge}(n, -1)\n'
    igzyi__qds += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    igzyi__qds += '        s = in_arr[j]\n'
    igzyi__qds += '        if bodo.libs.array_kernels.isna(in_arr, j):\n'
    igzyi__qds += '            s = value\n'
    igzyi__qds += '        out_arr[j] = s\n'
    igzyi__qds += (
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)\n'
        )
    ypnu__euz = dict()
    exec(igzyi__qds, {'bodo': bodo, 'numba': numba}, ypnu__euz)
    bdrw__xoszr = ypnu__euz['impl']
    return bdrw__xoszr


def fillna_inplace_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    tjgnk__pjd = bodo.hiframes.pd_series_ext.get_series_data(S)
    vjwro__avt = bodo.hiframes.pd_series_ext.get_series_data(value)
    for yccp__hnzd in numba.parfors.parfor.internal_prange(len(tjgnk__pjd)):
        s = tjgnk__pjd[yccp__hnzd]
        if bodo.libs.array_kernels.isna(tjgnk__pjd, yccp__hnzd
            ) and not bodo.libs.array_kernels.isna(vjwro__avt, yccp__hnzd):
            s = vjwro__avt[yccp__hnzd]
        tjgnk__pjd[yccp__hnzd] = s


def fillna_inplace_impl(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    tjgnk__pjd = bodo.hiframes.pd_series_ext.get_series_data(S)
    for yccp__hnzd in numba.parfors.parfor.internal_prange(len(tjgnk__pjd)):
        s = tjgnk__pjd[yccp__hnzd]
        if bodo.libs.array_kernels.isna(tjgnk__pjd, yccp__hnzd):
            s = value
        tjgnk__pjd[yccp__hnzd] = s


def str_fillna_alloc_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    tjgnk__pjd = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    vjwro__avt = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(tjgnk__pjd)
    nvo__rzq = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
    for woftx__ytqh in numba.parfors.parfor.internal_prange(n):
        s = tjgnk__pjd[woftx__ytqh]
        if bodo.libs.array_kernels.isna(tjgnk__pjd, woftx__ytqh
            ) and not bodo.libs.array_kernels.isna(vjwro__avt, woftx__ytqh):
            s = vjwro__avt[woftx__ytqh]
        nvo__rzq[woftx__ytqh] = s
        if bodo.libs.array_kernels.isna(tjgnk__pjd, woftx__ytqh
            ) and bodo.libs.array_kernels.isna(vjwro__avt, woftx__ytqh):
            bodo.libs.array_kernels.setna(nvo__rzq, woftx__ytqh)
    return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, index, name)


def fillna_series_impl(S, value=None, method=None, axis=None, inplace=False,
    limit=None, downcast=None):
    tjgnk__pjd = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    vjwro__avt = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(tjgnk__pjd)
    nvo__rzq = bodo.utils.utils.alloc_type(n, tjgnk__pjd.dtype, (-1,))
    for yccp__hnzd in numba.parfors.parfor.internal_prange(n):
        s = tjgnk__pjd[yccp__hnzd]
        if bodo.libs.array_kernels.isna(tjgnk__pjd, yccp__hnzd
            ) and not bodo.libs.array_kernels.isna(vjwro__avt, yccp__hnzd):
            s = vjwro__avt[yccp__hnzd]
        nvo__rzq[yccp__hnzd] = s
    return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, index, name)


@overload_method(SeriesType, 'fillna', no_unliteral=True)
def overload_series_fillna(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    hvuw__yveso = dict(method=method, limit=limit, downcast=downcast)
    ltyv__lube = dict(method=None, limit=None, downcast=None)
    check_unsupported_args('Series.series_fillna', hvuw__yveso, ltyv__lube)
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError('Series.min(): axis argument not supported')
    elif is_iterable_type(value) and not isinstance(value, SeriesType):
        raise BodoError('Series.fillna(): "value" parameter cannot be a list')
    elif is_var_size_item_array_type(S.data
        ) and not S.dtype == bodo.string_type:
        raise BodoError(
            f'Series.fillna() with inplace=True not supported for {S.dtype} values yet'
            )
    xrkx__bcy = element_type(S.data)
    qwajt__xradu = element_type(types.unliteral(value))
    if not can_replace(xrkx__bcy, qwajt__xradu):
        raise BodoError(
            f'Series.fillna(): Cannot use value type {qwajt__xradu} with series type {xrkx__bcy}'
            )
    if is_overload_true(inplace):
        if S.dtype == bodo.string_type:
            if is_overload_constant_str(value) and get_overload_const_str(value
                ) == '':
                return (lambda S, value=None, method=None, axis=None,
                    inplace=False, limit=None, downcast=None: bodo.libs.
                    str_arr_ext.set_null_bits_to_value(bodo.hiframes.
                    pd_series_ext.get_series_data(S), -1))
            if isinstance(value, SeriesType):
                return binary_str_fillna_inplace_series_impl(is_binary=False)
            return binary_str_fillna_inplace_impl(is_binary=False)
        if S.dtype == bodo.bytes_type:
            if is_overload_constant_bytes(value) and get_overload_const_bytes(
                value) == b'':
                return (lambda S, value=None, method=None, axis=None,
                    inplace=False, limit=None, downcast=None: bodo.libs.
                    str_arr_ext.set_null_bits_to_value(bodo.hiframes.
                    pd_series_ext.get_series_data(S), -1))
            if isinstance(value, SeriesType):
                return binary_str_fillna_inplace_series_impl(is_binary=True)
            return binary_str_fillna_inplace_impl(is_binary=True)
        else:
            if isinstance(value, SeriesType):
                return fillna_inplace_series_impl
            return fillna_inplace_impl
    else:
        vkpzf__vub = S.data
        if isinstance(value, SeriesType):

            def fillna_series_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                tjgnk__pjd = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                vjwro__avt = bodo.hiframes.pd_series_ext.get_series_data(value)
                n = len(tjgnk__pjd)
                nvo__rzq = bodo.utils.utils.alloc_type(n, vkpzf__vub, (-1,))
                for yccp__hnzd in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(tjgnk__pjd, yccp__hnzd
                        ) and bodo.libs.array_kernels.isna(vjwro__avt,
                        yccp__hnzd):
                        bodo.libs.array_kernels.setna(nvo__rzq, yccp__hnzd)
                        continue
                    if bodo.libs.array_kernels.isna(tjgnk__pjd, yccp__hnzd):
                        nvo__rzq[yccp__hnzd
                            ] = bodo.utils.conversion.unbox_if_timestamp(
                            vjwro__avt[yccp__hnzd])
                        continue
                    nvo__rzq[yccp__hnzd
                        ] = bodo.utils.conversion.unbox_if_timestamp(tjgnk__pjd
                        [yccp__hnzd])
                return bodo.hiframes.pd_series_ext.init_series(nvo__rzq,
                    index, name)
            return fillna_series_impl

        def fillna_impl(S, value=None, method=None, axis=None, inplace=
            False, limit=None, downcast=None):
            value = bodo.utils.conversion.unbox_if_timestamp(value)
            tjgnk__pjd = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(tjgnk__pjd)
            nvo__rzq = bodo.utils.utils.alloc_type(n, vkpzf__vub, (-1,))
            for yccp__hnzd in numba.parfors.parfor.internal_prange(n):
                s = bodo.utils.conversion.unbox_if_timestamp(tjgnk__pjd[
                    yccp__hnzd])
                if bodo.libs.array_kernels.isna(tjgnk__pjd, yccp__hnzd):
                    s = value
                nvo__rzq[yccp__hnzd] = s
            return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, index,
                name)
        return fillna_impl


def check_unsupported_types(S, to_replace, value):
    if any(bodo.utils.utils.is_array_typ(x, True) for x in [S.dtype,
        to_replace, value]):
        kovi__djtot = (
            'Series.replace(): only support with Scalar, List, or Dictionary')
        raise BodoError(kovi__djtot)
    elif isinstance(to_replace, types.DictType) and not is_overload_none(value
        ):
        kovi__djtot = (
            "Series.replace(): 'value' must be None when 'to_replace' is a dictionary"
            )
        raise BodoError(kovi__djtot)
    elif any(isinstance(x, (PandasTimestampType, PDTimeDeltaType)) for x in
        [to_replace, value]):
        kovi__djtot = (
            f'Series.replace(): Not supported for types {to_replace} and {value}'
            )
        raise BodoError(kovi__djtot)


def series_replace_error_checking(S, to_replace, value, inplace, limit,
    regex, method):
    hvuw__yveso = dict(inplace=inplace, limit=limit, regex=regex, method=method
        )
    njeg__lvp = dict(inplace=False, limit=None, regex=False, method='pad')
    check_unsupported_args('Series.replace', hvuw__yveso, njeg__lvp)
    check_unsupported_types(S, to_replace, value)


@overload_method(SeriesType, 'replace', inline='always', no_unliteral=True)
def overload_series_replace(S, to_replace=None, value=None, inplace=False,
    limit=None, regex=False, method='pad'):
    series_replace_error_checking(S, to_replace, value, inplace, limit,
        regex, method)
    xrkx__bcy = element_type(S.data)
    if isinstance(to_replace, types.DictType):
        icnf__njbef = element_type(to_replace.key_type)
        qwajt__xradu = element_type(to_replace.value_type)
    else:
        icnf__njbef = element_type(to_replace)
        qwajt__xradu = element_type(value)
    qqvhz__jrptf = None
    if xrkx__bcy != types.unliteral(icnf__njbef):
        if bodo.utils.typing.equality_always_false(xrkx__bcy, types.
            unliteral(icnf__njbef)
            ) or not bodo.utils.typing.types_equality_exists(xrkx__bcy,
            icnf__njbef):

            def impl(S, to_replace=None, value=None, inplace=False, limit=
                None, regex=False, method='pad'):
                return S.copy()
            return impl
        if isinstance(xrkx__bcy, (types.Float, types.Integer)
            ) or xrkx__bcy == np.bool_:
            qqvhz__jrptf = xrkx__bcy
    if not can_replace(xrkx__bcy, types.unliteral(qwajt__xradu)):

        def impl(S, to_replace=None, value=None, inplace=False, limit=None,
            regex=False, method='pad'):
            return S.copy()
        return impl
    ioic__wio = S.data
    if isinstance(ioic__wio, CategoricalArrayType):

        def cat_impl(S, to_replace=None, value=None, inplace=False, limit=
            None, regex=False, method='pad'):
            tjgnk__pjd = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(tjgnk__pjd.
                replace(to_replace, value), index, name)
        return cat_impl

    def impl(S, to_replace=None, value=None, inplace=False, limit=None,
        regex=False, method='pad'):
        tjgnk__pjd = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        n = len(tjgnk__pjd)
        nvo__rzq = bodo.utils.utils.alloc_type(n, ioic__wio, (-1,))
        hcq__jbmm = build_replace_dict(to_replace, value, qqvhz__jrptf)
        for yccp__hnzd in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(tjgnk__pjd, yccp__hnzd):
                bodo.libs.array_kernels.setna(nvo__rzq, yccp__hnzd)
                continue
            s = tjgnk__pjd[yccp__hnzd]
            if s in hcq__jbmm:
                s = hcq__jbmm[s]
            nvo__rzq[yccp__hnzd] = s
        return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, index, name)
    return impl


def build_replace_dict(to_replace, value, key_dtype_conv):
    pass


@overload(build_replace_dict)
def _build_replace_dict(to_replace, value, key_dtype_conv):
    tycck__upnf = isinstance(to_replace, (types.Number, Decimal128Type)
        ) or to_replace in [bodo.string_type, types.boolean, bodo.bytes_type]
    amctn__fhyj = is_iterable_type(to_replace)
    wto__qrdsu = isinstance(value, (types.Number, Decimal128Type)
        ) or value in [bodo.string_type, bodo.bytes_type, types.boolean]
    zbc__lyzi = is_iterable_type(value)
    if tycck__upnf and wto__qrdsu:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                hcq__jbmm = {}
                hcq__jbmm[key_dtype_conv(to_replace)] = value
                return hcq__jbmm
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            hcq__jbmm = {}
            hcq__jbmm[to_replace] = value
            return hcq__jbmm
        return impl
    if amctn__fhyj and wto__qrdsu:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                hcq__jbmm = {}
                for qjr__ockkj in to_replace:
                    hcq__jbmm[key_dtype_conv(qjr__ockkj)] = value
                return hcq__jbmm
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            hcq__jbmm = {}
            for qjr__ockkj in to_replace:
                hcq__jbmm[qjr__ockkj] = value
            return hcq__jbmm
        return impl
    if amctn__fhyj and zbc__lyzi:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                hcq__jbmm = {}
                assert len(to_replace) == len(value
                    ), 'To_replace and value lengths must be the same'
                for yccp__hnzd in range(len(to_replace)):
                    hcq__jbmm[key_dtype_conv(to_replace[yccp__hnzd])] = value[
                        yccp__hnzd]
                return hcq__jbmm
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            hcq__jbmm = {}
            assert len(to_replace) == len(value
                ), 'To_replace and value lengths must be the same'
            for yccp__hnzd in range(len(to_replace)):
                hcq__jbmm[to_replace[yccp__hnzd]] = value[yccp__hnzd]
            return hcq__jbmm
        return impl
    if isinstance(to_replace, numba.types.DictType) and is_overload_none(value
        ):
        return lambda to_replace, value, key_dtype_conv: to_replace
    raise BodoError(
        'Series.replace(): Not supported for types to_replace={} and value={}'
        .format(to_replace, value))


@overload_method(SeriesType, 'diff', inline='always', no_unliteral=True)
def overload_series_diff(S, periods=1):
    if not (isinstance(S.data, types.Array) and (isinstance(S.data.dtype,
        types.Number) or S.data.dtype == bodo.datetime64ns)):
        raise BodoError(
            f'Series.diff() column input type {S.data} not supported.')
    if not is_overload_int(periods):
        raise BodoError("Series.diff(): 'periods' input must be an integer.")
    if S.data == types.Array(bodo.datetime64ns, 1, 'C'):

        def impl_datetime(S, periods=1):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            nvo__rzq = bodo.hiframes.series_impl.dt64_arr_sub(arr, bodo.
                hiframes.rolling.shift(arr, periods, False))
            return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, index,
                name)
        return impl_datetime

    def impl(S, periods=1):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        nvo__rzq = arr - bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, index, name)
    return impl


@overload_method(SeriesType, 'explode', inline='always', no_unliteral=True)
def overload_series_explode(S, ignore_index=False):
    from bodo.hiframes.split_impl import string_array_split_view_type
    hvuw__yveso = dict(ignore_index=ignore_index)
    ubx__doxai = dict(ignore_index=False)
    check_unsupported_args('Series.explode', hvuw__yveso, ubx__doxai)
    if not (isinstance(S.data, ArrayItemArrayType) or S.data ==
        string_array_split_view_type):
        return lambda S, ignore_index=False: S.copy()

    def impl(S, ignore_index=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        chv__twj = bodo.utils.conversion.index_to_array(index)
        nvo__rzq, pfwr__xvs = bodo.libs.array_kernels.explode(arr, chv__twj)
        uwzni__tzd = bodo.utils.conversion.index_from_array(pfwr__xvs)
        return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, uwzni__tzd,
            name)
    return impl


@overload(np.digitize, inline='always', no_unliteral=True)
def overload_series_np_digitize(x, bins, right=False):
    if isinstance(x, SeriesType):

        def impl(x, bins, right=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(x)
            return np.digitize(arr, bins, right)
        return impl


@overload(np.argmax, inline='always', no_unliteral=True)
def argmax_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            nmofi__qjrtg = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for yccp__hnzd in numba.parfors.parfor.internal_prange(n):
                nmofi__qjrtg[yccp__hnzd] = np.argmax(a[yccp__hnzd])
            return nmofi__qjrtg
        return impl


@overload(np.argmin, inline='always', no_unliteral=True)
def argmin_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            rcjg__phwv = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for yccp__hnzd in numba.parfors.parfor.internal_prange(n):
                rcjg__phwv[yccp__hnzd] = np.argmin(a[yccp__hnzd])
            return rcjg__phwv
        return impl


def overload_series_np_dot(a, b, out=None):
    if (isinstance(a, SeriesType) or isinstance(b, SeriesType)
        ) and not is_overload_none(out):
        raise BodoError("np.dot(): 'out' parameter not supported yet")
    if isinstance(a, SeriesType):

        def impl(a, b, out=None):
            arr = bodo.hiframes.pd_series_ext.get_series_data(a)
            return np.dot(arr, b)
        return impl
    if isinstance(b, SeriesType):

        def impl(a, b, out=None):
            arr = bodo.hiframes.pd_series_ext.get_series_data(b)
            return np.dot(a, arr)
        return impl


overload(np.dot, inline='always', no_unliteral=True)(overload_series_np_dot)
overload(operator.matmul, inline='always', no_unliteral=True)(
    overload_series_np_dot)


@overload_method(SeriesType, 'dropna', inline='always', no_unliteral=True)
def overload_series_dropna(S, axis=0, inplace=False):
    hvuw__yveso = dict(axis=axis, inplace=inplace)
    ubx__doxai = dict(axis=0, inplace=False)
    check_unsupported_args('Series.dropna', hvuw__yveso, ubx__doxai)
    if S.dtype == bodo.string_type:

        def dropna_str_impl(S, axis=0, inplace=False):
            tjgnk__pjd = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            qqj__vuus = S.notna().values
            chv__twj = bodo.utils.conversion.extract_index_array(S)
            uwzni__tzd = bodo.utils.conversion.convert_to_index(chv__twj[
                qqj__vuus])
            nvo__rzq = (bodo.hiframes.series_kernels.
                _series_dropna_str_alloc_impl_inner(tjgnk__pjd))
            return bodo.hiframes.pd_series_ext.init_series(nvo__rzq,
                uwzni__tzd, name)
        return dropna_str_impl
    else:

        def dropna_impl(S, axis=0, inplace=False):
            tjgnk__pjd = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            chv__twj = bodo.utils.conversion.extract_index_array(S)
            qqj__vuus = S.notna().values
            uwzni__tzd = bodo.utils.conversion.convert_to_index(chv__twj[
                qqj__vuus])
            nvo__rzq = tjgnk__pjd[qqj__vuus]
            return bodo.hiframes.pd_series_ext.init_series(nvo__rzq,
                uwzni__tzd, name)
        return dropna_impl


@overload_method(SeriesType, 'shift', inline='always', no_unliteral=True)
def overload_series_shift(S, periods=1, freq=None, axis=0, fill_value=None):
    hvuw__yveso = dict(freq=freq, axis=axis, fill_value=fill_value)
    ltyv__lube = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('Series.shift', hvuw__yveso, ltyv__lube)
    if not is_supported_shift_array_type(S.data):
        raise BodoError(
            f"Series.shift(): Series input type '{S.data.dtype}' not supported yet."
            )
    if not is_overload_int(periods):
        raise BodoError("Series.shift(): 'periods' input must be an integer.")

    def impl(S, periods=1, freq=None, axis=0, fill_value=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        nvo__rzq = bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, index, name)
    return impl


@overload_method(SeriesType, 'pct_change', inline='always', no_unliteral=True)
def overload_series_pct_change(S, periods=1, fill_method='pad', limit=None,
    freq=None):
    hvuw__yveso = dict(fill_method=fill_method, limit=limit, freq=freq)
    ltyv__lube = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('Series.pct_change', hvuw__yveso, ltyv__lube)

    def impl(S, periods=1, fill_method='pad', limit=None, freq=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        nvo__rzq = bodo.hiframes.rolling.pct_change(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, index, name)
    return impl


@overload_method(SeriesType, 'where', inline='always', no_unliteral=True)
def overload_series_where(S, cond, other=np.nan, inplace=False, axis=None,
    level=None, errors='raise', try_cast=False):
    _validate_arguments_mask_where('Series.where', S, cond, other, inplace,
        axis, level, errors, try_cast)

    def impl(S, cond, other=np.nan, inplace=False, axis=None, level=None,
        errors='raise', try_cast=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        nvo__rzq = bodo.hiframes.series_impl.where_impl(cond, arr, other)
        return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, index, name)
    return impl


@overload_method(SeriesType, 'mask', inline='always', no_unliteral=True)
def overload_series_mask(S, cond, other=np.nan, inplace=False, axis=None,
    level=None, errors='raise', try_cast=False):
    _validate_arguments_mask_where('Series.mask', S, cond, other, inplace,
        axis, level, errors, try_cast)

    def impl(S, cond, other=np.nan, inplace=False, axis=None, level=None,
        errors='raise', try_cast=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        nvo__rzq = bodo.hiframes.series_impl.where_impl(~cond, arr, other)
        return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, index, name)
    return impl


def _validate_arguments_mask_where(func_name, S, cond, other, inplace, axis,
    level, errors, try_cast):
    hvuw__yveso = dict(inplace=inplace, level=level, errors=errors,
        try_cast=try_cast)
    ltyv__lube = dict(inplace=False, level=None, errors='raise', try_cast=False
        )
    check_unsupported_args(f'{func_name}', hvuw__yveso, ltyv__lube)
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError(f'{func_name}(): axis argument not supported')
    if not (isinstance(S.data, types.Array) or isinstance(S.data,
        BooleanArrayType) or isinstance(S.data, IntegerArrayType) or bodo.
        utils.utils.is_array_typ(S.data, False) and S.dtype in [bodo.
        string_type, bodo.bytes_type] or isinstance(S.data, bodo.
        CategoricalArrayType) and S.dtype.elem_type not in [bodo.
        datetime64ns, bodo.timedelta64ns, bodo.pd_timestamp_type, bodo.
        pd_timedelta_type]):
        raise BodoError(
            f'{func_name}() Series data with type {S.data} not yet supported')
    if not (isinstance(cond, (SeriesType, types.Array, BooleanArrayType)) and
        cond.ndim == 1 and cond.dtype == types.bool_):
        raise BodoError(
            f"{func_name}() 'cond' argument must be a Series or 1-dim array of booleans"
            )
    wvl__tqwzo = is_overload_constant_nan(other)
    if not (wvl__tqwzo or is_scalar_type(other) or isinstance(other, types.
        Array) and other.ndim == 1 or isinstance(other, SeriesType) and (
        isinstance(S.data, types.Array) or S.dtype in [bodo.string_type,
        bodo.bytes_type]) or isinstance(other, StringArrayType) and S.dtype ==
        bodo.string_type or isinstance(other, BinaryArrayType) and S.dtype ==
        bodo.bytes_type or (not isinstance(other, (StringArrayType,
        BinaryArrayType)) and (isinstance(S.data.dtype, types.Integer) and
        isinstance(other.data.dtype, types.Integer)) or S.data.dtype ==
        other.data.dtype) and (isinstance(S.data, BooleanArrayType) or
        isinstance(S.data, IntegerArrayType))):
        raise BodoError(
            f"{func_name}() 'other' must be a scalar, series, 1-dim numpy array or StringArray with a matching type for Series."
            )
    if isinstance(S.dtype, bodo.PDCategoricalDtype):
        cvfa__iwv = S.dtype.elem_type
    else:
        cvfa__iwv = S.dtype
    if is_iterable_type(other):
        kfwhn__oooj = other.dtype
    elif wvl__tqwzo:
        kfwhn__oooj = types.float64
    else:
        kfwhn__oooj = types.unliteral(other)
    if not is_common_scalar_dtype([cvfa__iwv, kfwhn__oooj]):
        raise BodoError(
            f"{func_name}() series and 'other' must share a common type.")


def create_explicit_binary_op_overload(op):

    def overload_series_explicit_binary_op(S, other, level=None, fill_value
        =None, axis=0):
        hvuw__yveso = dict(level=level, axis=axis)
        ltyv__lube = dict(level=None, axis=0)
        check_unsupported_args('series.{}'.format(op.__name__), hvuw__yveso,
            ltyv__lube)
        koyjt__grd = other == string_type or is_overload_constant_str(other)
        ogi__qqxbg = is_iterable_type(other) and other.dtype == string_type
        qfypd__pfxd = S.dtype == string_type and (op == operator.add and (
            koyjt__grd or ogi__qqxbg) or op == operator.mul and isinstance(
            other, types.Integer))
        piirn__rayi = S.dtype == bodo.timedelta64ns
        adv__wwtrw = S.dtype == bodo.datetime64ns
        isj__htjos = is_iterable_type(other) and (other.dtype ==
            datetime_timedelta_type or other.dtype == bodo.timedelta64ns)
        qclm__zvns = is_iterable_type(other) and (other.dtype ==
            datetime_datetime_type or other.dtype == pd_timestamp_type or 
            other.dtype == bodo.datetime64ns)
        ewsf__xhxw = piirn__rayi and (isj__htjos or qclm__zvns
            ) or adv__wwtrw and isj__htjos
        ewsf__xhxw = ewsf__xhxw and op == operator.add
        if not (isinstance(S.dtype, types.Number) or qfypd__pfxd or ewsf__xhxw
            ):
            raise BodoError(f'Unsupported types for Series.{op.__name__}')
        ntb__tivi = numba.core.registry.cpu_target.typing_context
        if is_scalar_type(other):
            args = S.data, other
            ioic__wio = ntb__tivi.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and ioic__wio == types.Array(types.bool_, 1, 'C'):
                ioic__wio = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                other = bodo.utils.conversion.unbox_if_timestamp(other)
                n = len(arr)
                nvo__rzq = bodo.utils.utils.alloc_type(n, ioic__wio, (-1,))
                for yccp__hnzd in numba.parfors.parfor.internal_prange(n):
                    edly__hezv = bodo.libs.array_kernels.isna(arr, yccp__hnzd)
                    if edly__hezv:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(nvo__rzq, yccp__hnzd)
                        else:
                            nvo__rzq[yccp__hnzd] = op(fill_value, other)
                    else:
                        nvo__rzq[yccp__hnzd] = op(arr[yccp__hnzd], other)
                return bodo.hiframes.pd_series_ext.init_series(nvo__rzq,
                    index, name)
            return impl_scalar
        args = S.data, types.Array(other.dtype, 1, 'C')
        ioic__wio = ntb__tivi.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, IntegerArrayType) and ioic__wio == types.Array(
            types.bool_, 1, 'C'):
            ioic__wio = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            gnb__yach = bodo.utils.conversion.coerce_to_array(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            nvo__rzq = bodo.utils.utils.alloc_type(n, ioic__wio, (-1,))
            for yccp__hnzd in numba.parfors.parfor.internal_prange(n):
                edly__hezv = bodo.libs.array_kernels.isna(arr, yccp__hnzd)
                utwe__qwzh = bodo.libs.array_kernels.isna(gnb__yach, yccp__hnzd
                    )
                if edly__hezv and utwe__qwzh:
                    bodo.libs.array_kernels.setna(nvo__rzq, yccp__hnzd)
                elif edly__hezv:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(nvo__rzq, yccp__hnzd)
                    else:
                        nvo__rzq[yccp__hnzd] = op(fill_value, gnb__yach[
                            yccp__hnzd])
                elif utwe__qwzh:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(nvo__rzq, yccp__hnzd)
                    else:
                        nvo__rzq[yccp__hnzd] = op(arr[yccp__hnzd], fill_value)
                else:
                    nvo__rzq[yccp__hnzd] = op(arr[yccp__hnzd], gnb__yach[
                        yccp__hnzd])
            return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, index,
                name)
        return impl
    return overload_series_explicit_binary_op


def create_explicit_binary_reverse_op_overload(op):

    def overload_series_explicit_binary_reverse_op(S, other, level=None,
        fill_value=None, axis=0):
        if not is_overload_none(level):
            raise BodoError('level argument not supported')
        if not is_overload_zero(axis):
            raise BodoError('axis argument not supported')
        if not isinstance(S.dtype, types.Number):
            raise BodoError('only numeric values supported')
        ntb__tivi = numba.core.registry.cpu_target.typing_context
        if isinstance(other, types.Number):
            args = other, S.data
            ioic__wio = ntb__tivi.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and ioic__wio == types.Array(types.bool_, 1, 'C'):
                ioic__wio = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                n = len(arr)
                nvo__rzq = bodo.utils.utils.alloc_type(n, ioic__wio, None)
                for yccp__hnzd in numba.parfors.parfor.internal_prange(n):
                    edly__hezv = bodo.libs.array_kernels.isna(arr, yccp__hnzd)
                    if edly__hezv:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(nvo__rzq, yccp__hnzd)
                        else:
                            nvo__rzq[yccp__hnzd] = op(other, fill_value)
                    else:
                        nvo__rzq[yccp__hnzd] = op(other, arr[yccp__hnzd])
                return bodo.hiframes.pd_series_ext.init_series(nvo__rzq,
                    index, name)
            return impl_scalar
        args = types.Array(other.dtype, 1, 'C'), S.data
        ioic__wio = ntb__tivi.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, IntegerArrayType) and ioic__wio == types.Array(
            types.bool_, 1, 'C'):
            ioic__wio = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            gnb__yach = bodo.hiframes.pd_series_ext.get_series_data(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            nvo__rzq = bodo.utils.utils.alloc_type(n, ioic__wio, None)
            for yccp__hnzd in numba.parfors.parfor.internal_prange(n):
                edly__hezv = bodo.libs.array_kernels.isna(arr, yccp__hnzd)
                utwe__qwzh = bodo.libs.array_kernels.isna(gnb__yach, yccp__hnzd
                    )
                nvo__rzq[yccp__hnzd] = op(gnb__yach[yccp__hnzd], arr[
                    yccp__hnzd])
                if edly__hezv and utwe__qwzh:
                    bodo.libs.array_kernels.setna(nvo__rzq, yccp__hnzd)
                elif edly__hezv:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(nvo__rzq, yccp__hnzd)
                    else:
                        nvo__rzq[yccp__hnzd] = op(gnb__yach[yccp__hnzd],
                            fill_value)
                elif utwe__qwzh:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(nvo__rzq, yccp__hnzd)
                    else:
                        nvo__rzq[yccp__hnzd] = op(fill_value, arr[yccp__hnzd])
                else:
                    nvo__rzq[yccp__hnzd] = op(gnb__yach[yccp__hnzd], arr[
                        yccp__hnzd])
            return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, index,
                name)
        return impl
    return overload_series_explicit_binary_reverse_op


explicit_binop_funcs_two_ways = {operator.add: {'add'}, operator.sub: {
    'sub'}, operator.mul: {'mul'}, operator.truediv: {'div', 'truediv'},
    operator.floordiv: {'floordiv'}, operator.mod: {'mod'}, operator.pow: {
    'pow'}}
explicit_binop_funcs_single = {operator.lt: 'lt', operator.gt: 'gt',
    operator.le: 'le', operator.ge: 'ge', operator.ne: 'ne', operator.eq: 'eq'}
explicit_binop_funcs = set()
split_logical_binops_funcs = [operator.or_, operator.and_]


def _install_explicit_binary_ops():
    for op, nsh__zad in explicit_binop_funcs_two_ways.items():
        for name in nsh__zad:
            ytfi__ytyi = create_explicit_binary_op_overload(op)
            vbu__gnve = create_explicit_binary_reverse_op_overload(op)
            auryo__kfcih = 'r' + name
            overload_method(SeriesType, name, no_unliteral=True)(ytfi__ytyi)
            overload_method(SeriesType, auryo__kfcih, no_unliteral=True)(
                vbu__gnve)
            explicit_binop_funcs.add(name)
    for op, name in explicit_binop_funcs_single.items():
        ytfi__ytyi = create_explicit_binary_op_overload(op)
        overload_method(SeriesType, name, no_unliteral=True)(ytfi__ytyi)
        explicit_binop_funcs.add(name)


_install_explicit_binary_ops()


def create_binary_op_overload(op):

    def overload_series_binary_op(lhs, rhs):
        if (isinstance(lhs, SeriesType) and isinstance(rhs, SeriesType) and
            lhs.dtype == bodo.datetime64ns and rhs.dtype == bodo.
            datetime64ns and op == operator.sub):

            def impl_dt64(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                cgfva__shety = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                nvo__rzq = dt64_arr_sub(arr, cgfva__shety)
                return bodo.hiframes.pd_series_ext.init_series(nvo__rzq,
                    index, name)
            return impl_dt64
        if op in [operator.add, operator.sub] and isinstance(lhs, SeriesType
            ) and lhs.dtype == bodo.datetime64ns and is_offsets_type(rhs):

            def impl_offsets(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                nvo__rzq = np.empty(n, np.dtype('datetime64[ns]'))
                for yccp__hnzd in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(arr, yccp__hnzd):
                        bodo.libs.array_kernels.setna(nvo__rzq, yccp__hnzd)
                        continue
                    exvcq__vrp = (bodo.hiframes.pd_timestamp_ext.
                        convert_datetime64_to_timestamp(arr[yccp__hnzd]))
                    nip__iooc = op(exvcq__vrp, rhs)
                    nvo__rzq[yccp__hnzd
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        nip__iooc.value)
                return bodo.hiframes.pd_series_ext.init_series(nvo__rzq,
                    index, name)
            return impl_offsets
        if op == operator.add and is_offsets_type(lhs) and isinstance(rhs,
            SeriesType) and rhs.dtype == bodo.datetime64ns:

            def impl(lhs, rhs):
                return op(rhs, lhs)
            return impl
        if isinstance(lhs, SeriesType):
            if lhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                    cgfva__shety = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    nvo__rzq = op(arr, bodo.utils.conversion.
                        unbox_if_timestamp(cgfva__shety))
                    return bodo.hiframes.pd_series_ext.init_series(nvo__rzq,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                cgfva__shety = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                nvo__rzq = op(arr, cgfva__shety)
                return bodo.hiframes.pd_series_ext.init_series(nvo__rzq,
                    index, name)
            return impl
        if isinstance(rhs, SeriesType):
            if rhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                    tyn__kodm = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    nvo__rzq = op(bodo.utils.conversion.unbox_if_timestamp(
                        tyn__kodm), arr)
                    return bodo.hiframes.pd_series_ext.init_series(nvo__rzq,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                tyn__kodm = bodo.utils.conversion.get_array_if_series_or_index(
                    lhs)
                nvo__rzq = op(tyn__kodm, arr)
                return bodo.hiframes.pd_series_ext.init_series(nvo__rzq,
                    index, name)
            return impl
    return overload_series_binary_op


skips = list(explicit_binop_funcs_two_ways.keys()) + list(
    explicit_binop_funcs_single.keys()) + split_logical_binops_funcs


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        ytfi__ytyi = create_binary_op_overload(op)
        overload(op)(ytfi__ytyi)


_install_binary_ops()


def dt64_arr_sub(arg1, arg2):
    return arg1 - arg2


@overload(dt64_arr_sub, no_unliteral=True)
def overload_dt64_arr_sub(arg1, arg2):
    assert arg1 == types.Array(bodo.datetime64ns, 1, 'C'
        ) and arg2 == types.Array(bodo.datetime64ns, 1, 'C')
    lcex__akglp = np.dtype('timedelta64[ns]')

    def impl(arg1, arg2):
        numba.parfors.parfor.init_prange()
        n = len(arg1)
        S = np.empty(n, lcex__akglp)
        for yccp__hnzd in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg1, yccp__hnzd
                ) or bodo.libs.array_kernels.isna(arg2, yccp__hnzd):
                bodo.libs.array_kernels.setna(S, yccp__hnzd)
                continue
            S[yccp__hnzd
                ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg1[
                yccp__hnzd]) - bodo.hiframes.pd_timestamp_ext.
                dt64_to_integer(arg2[yccp__hnzd]))
        return S
    return impl


def create_inplace_binary_op_overload(op):

    def overload_series_inplace_binary_op(S, other):
        if isinstance(S, SeriesType) or isinstance(other, SeriesType):

            def impl(S, other):
                arr = bodo.utils.conversion.get_array_if_series_or_index(S)
                gnb__yach = bodo.utils.conversion.get_array_if_series_or_index(
                    other)
                op(arr, gnb__yach)
                return S
            return impl
    return overload_series_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        ytfi__ytyi = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(ytfi__ytyi)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_series_unary_op(S):
        if isinstance(S, SeriesType):

            def impl(S):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                nvo__rzq = op(arr)
                return bodo.hiframes.pd_series_ext.init_series(nvo__rzq,
                    index, name)
            return impl
    return overload_series_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        ytfi__ytyi = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(ytfi__ytyi)


_install_unary_ops()


def create_ufunc_overload(ufunc):
    if ufunc.nin == 1:

        def overload_series_ufunc_nin_1(S):
            if isinstance(S, SeriesType):

                def impl(S):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S)
                    nvo__rzq = ufunc(arr)
                    return bodo.hiframes.pd_series_ext.init_series(nvo__rzq,
                        index, name)
                return impl
        return overload_series_ufunc_nin_1
    elif ufunc.nin == 2:

        def overload_series_ufunc_nin_2(S1, S2):
            if isinstance(S1, SeriesType):

                def impl(S1, S2):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S1)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S1)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S1)
                    gnb__yach = (bodo.utils.conversion.
                        get_array_if_series_or_index(S2))
                    nvo__rzq = ufunc(arr, gnb__yach)
                    return bodo.hiframes.pd_series_ext.init_series(nvo__rzq,
                        index, name)
                return impl
            elif isinstance(S2, SeriesType):

                def impl(S1, S2):
                    arr = bodo.utils.conversion.get_array_if_series_or_index(S1
                        )
                    gnb__yach = bodo.hiframes.pd_series_ext.get_series_data(S2)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S2)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S2)
                    nvo__rzq = ufunc(arr, gnb__yach)
                    return bodo.hiframes.pd_series_ext.init_series(nvo__rzq,
                        index, name)
                return impl
        return overload_series_ufunc_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for ufunc in numba.np.ufunc_db.get_ufuncs():
        ytfi__ytyi = create_ufunc_overload(ufunc)
        overload(ufunc, no_unliteral=True)(ytfi__ytyi)


_install_np_ufuncs()


def argsort(A):
    return np.argsort(A)


@overload(argsort, no_unliteral=True)
def overload_argsort(A):

    def impl(A):
        n = len(A)
        qytt__tsi = bodo.libs.str_arr_ext.to_list_if_immutable_arr((A.copy(),))
        nassr__yaob = np.arange(n),
        bodo.libs.timsort.sort(qytt__tsi, 0, n, nassr__yaob)
        return nassr__yaob[0]
    return impl


@overload(pd.to_numeric, inline='always', no_unliteral=True)
def overload_to_numeric(arg_a, errors='raise', downcast=None):
    if not is_overload_none(downcast) and not (is_overload_constant_str(
        downcast) and get_overload_const_str(downcast) in ('integer',
        'signed', 'unsigned', 'float')):
        raise BodoError(
            'pd.to_numeric(): invalid downcasting method provided {}'.
            format(downcast))
    out_dtype = types.float64
    if not is_overload_none(downcast):
        drb__jjjp = get_overload_const_str(downcast)
        if drb__jjjp in ('integer', 'signed'):
            out_dtype = types.int64
        elif drb__jjjp == 'unsigned':
            out_dtype = types.uint64
        else:
            assert drb__jjjp == 'float'
    if isinstance(arg_a, (types.Array, IntegerArrayType)):
        return lambda arg_a, errors='raise', downcast=None: arg_a.astype(
            out_dtype)
    if isinstance(arg_a, SeriesType):

        def impl_series(arg_a, errors='raise', downcast=None):
            tjgnk__pjd = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            index = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            name = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            nvo__rzq = pd.to_numeric(tjgnk__pjd, errors, downcast)
            return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, index,
                name)
        return impl_series
    if arg_a != string_array_type:
        raise BodoError('pd.to_numeric(): invalid argument type {}'.format(
            arg_a))
    if out_dtype == types.float64:

        def to_numeric_float_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            nvteh__jyesk = np.empty(n, np.float64)
            for yccp__hnzd in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, yccp__hnzd):
                    bodo.libs.array_kernels.setna(nvteh__jyesk, yccp__hnzd)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(nvteh__jyesk,
                        yccp__hnzd, arg_a, yccp__hnzd)
            return nvteh__jyesk
        return to_numeric_float_impl
    else:

        def to_numeric_int_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            nvteh__jyesk = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)
            for yccp__hnzd in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, yccp__hnzd):
                    bodo.libs.array_kernels.setna(nvteh__jyesk, yccp__hnzd)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(nvteh__jyesk,
                        yccp__hnzd, arg_a, yccp__hnzd)
            return nvteh__jyesk
        return to_numeric_int_impl


def series_filter_bool(arr, bool_arr):
    return arr[bool_arr]


@infer_global(series_filter_bool)
class SeriesFilterBoolInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        yqwmi__cjeg = if_series_to_array_type(args[0])
        if isinstance(yqwmi__cjeg, types.Array) and isinstance(yqwmi__cjeg.
            dtype, types.Integer):
            yqwmi__cjeg = types.Array(types.float64, 1, 'C')
        return yqwmi__cjeg(*args)


def where_impl_one_arg(c):
    return np.where(c)


@overload(where_impl_one_arg, no_unliteral=True)
def overload_where_unsupported_one_arg(condition):
    if isinstance(condition, SeriesType) or bodo.utils.utils.is_array_typ(
        condition, False):
        return lambda condition: np.where(condition)


def overload_np_where_one_arg(condition):
    if isinstance(condition, SeriesType):

        def impl_series(condition):
            condition = bodo.hiframes.pd_series_ext.get_series_data(condition)
            return bodo.libs.array_kernels.nonzero(condition)
        return impl_series
    elif bodo.utils.utils.is_array_typ(condition, False):

        def impl(condition):
            return bodo.libs.array_kernels.nonzero(condition)
        return impl


overload(np.where, inline='always', no_unliteral=True)(
    overload_np_where_one_arg)
overload(where_impl_one_arg, inline='always', no_unliteral=True)(
    overload_np_where_one_arg)


def where_impl(c, x, y):
    return np.where(c, x, y)


@overload(where_impl, no_unliteral=True)
def overload_where_unsupported(condition, x, y):
    if not isinstance(condition, (SeriesType, types.Array, BooleanArrayType)
        ) or condition.ndim != 1:
        return lambda condition, x, y: np.where(condition, x, y)


@overload(where_impl, no_unliteral=True)
@overload(np.where, no_unliteral=True)
def overload_np_where(condition, x, y):
    if not isinstance(condition, (SeriesType, types.Array, BooleanArrayType)
        ) or condition.ndim != 1:
        return
    assert condition.dtype == types.bool_, 'invalid condition dtype'
    yuy__dpxqe = bodo.utils.utils.is_array_typ(x, True)
    akkfj__yvl = bodo.utils.utils.is_array_typ(y, True)
    igzyi__qds = 'def _impl(condition, x, y):\n'
    if isinstance(condition, SeriesType):
        igzyi__qds += (
            '  condition = bodo.hiframes.pd_series_ext.get_series_data(condition)\n'
            )
    if yuy__dpxqe and not bodo.utils.utils.is_array_typ(x, False):
        igzyi__qds += '  x = bodo.utils.conversion.coerce_to_array(x)\n'
    if akkfj__yvl and not bodo.utils.utils.is_array_typ(y, False):
        igzyi__qds += '  y = bodo.utils.conversion.coerce_to_array(y)\n'
    igzyi__qds += '  n = len(condition)\n'
    bgxl__xfm = x.dtype if yuy__dpxqe else types.unliteral(x)
    tvpdz__vuqz = y.dtype if akkfj__yvl else types.unliteral(y)
    if not isinstance(x, CategoricalArrayType):
        bgxl__xfm = element_type(x)
    if not isinstance(y, CategoricalArrayType):
        tvpdz__vuqz = element_type(y)

    def get_data(x):
        if isinstance(x, SeriesType):
            return x.data
        elif isinstance(x, types.Array):
            return x
        return types.unliteral(x)
    inx__szfq = get_data(x)
    cpk__rvqt = get_data(y)
    is_nullable = any(bodo.utils.typing.is_nullable(nassr__yaob) for
        nassr__yaob in [inx__szfq, cpk__rvqt])
    if inx__szfq == cpk__rvqt and not is_nullable:
        out_dtype = dtype_to_array_type(bgxl__xfm)
    elif bgxl__xfm == string_type or tvpdz__vuqz == string_type:
        out_dtype = bodo.string_array_type
    elif inx__szfq == bytes_type or (yuy__dpxqe and bgxl__xfm == bytes_type
        ) and (cpk__rvqt == bytes_type or akkfj__yvl and tvpdz__vuqz ==
        bytes_type):
        out_dtype = binary_array_type
    elif isinstance(bgxl__xfm, bodo.PDCategoricalDtype):
        out_dtype = None
    elif bgxl__xfm in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(bgxl__xfm, 1, 'C')
    elif tvpdz__vuqz in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(tvpdz__vuqz, 1, 'C')
    else:
        out_dtype = numba.from_dtype(np.promote_types(numba.np.
            numpy_support.as_dtype(bgxl__xfm), numba.np.numpy_support.
            as_dtype(tvpdz__vuqz)))
        out_dtype = types.Array(out_dtype, 1, 'C')
        if is_nullable:
            out_dtype = bodo.utils.typing.to_nullable_type(out_dtype)
    if isinstance(bgxl__xfm, bodo.PDCategoricalDtype):
        mlceb__ccfo = 'x'
    else:
        mlceb__ccfo = 'out_dtype'
    igzyi__qds += (
        f'  out_arr = bodo.utils.utils.alloc_type(n, {mlceb__ccfo}, (-1,))\n')
    if isinstance(bgxl__xfm, bodo.PDCategoricalDtype):
        igzyi__qds += """  out_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(out_arr)
"""
        igzyi__qds += (
            '  x_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(x)\n'
            )
    igzyi__qds += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    igzyi__qds += (
        '    if not bodo.libs.array_kernels.isna(condition, j) and condition[j]:\n'
        )
    if yuy__dpxqe:
        igzyi__qds += '      if bodo.libs.array_kernels.isna(x, j):\n'
        igzyi__qds += '        setna(out_arr, j)\n'
        igzyi__qds += '        continue\n'
    if isinstance(bgxl__xfm, bodo.PDCategoricalDtype):
        igzyi__qds += '      out_codes[j] = x_codes[j]\n'
    else:
        igzyi__qds += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('x[j]' if yuy__dpxqe else 'x'))
    igzyi__qds += '    else:\n'
    if akkfj__yvl:
        igzyi__qds += '      if bodo.libs.array_kernels.isna(y, j):\n'
        igzyi__qds += '        setna(out_arr, j)\n'
        igzyi__qds += '        continue\n'
    igzyi__qds += (
        '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
        .format('y[j]' if akkfj__yvl else 'y'))
    igzyi__qds += '  return out_arr\n'
    pfwwr__zazwk = {}
    exec(igzyi__qds, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'out_dtype': out_dtype}, pfwwr__zazwk)
    gnv__htgo = pfwwr__zazwk['_impl']
    return gnv__htgo


@overload_method(SeriesType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_series_drop_duplicates(S, subset=None, keep='first', inplace=False
    ):
    if not is_overload_none(subset):
        raise BodoError('drop_duplicates() subset argument not supported yet')
    if not is_overload_false(inplace):
        raise BodoError('drop_duplicates() inplace argument not supported yet')

    def impl(S, subset=None, keep='first', inplace=False):
        sywfv__prq = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        (sywfv__prq,), chv__twj = bodo.libs.array_kernels.drop_duplicates((
            sywfv__prq,), index)
        index = bodo.utils.conversion.index_from_array(chv__twj)
        return bodo.hiframes.pd_series_ext.init_series(sywfv__prq, index, name)
    return impl


@overload_method(SeriesType, 'between', inline='always', no_unliteral=True)
def overload_series_between(S, left, right, inclusive=True):

    def impl(S, left, right, inclusive=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(arr)
        nvo__rzq = np.empty(n, np.bool_)
        for yccp__hnzd in numba.parfors.parfor.internal_prange(n):
            zfkb__iuv = bodo.utils.conversion.box_if_dt64(arr[yccp__hnzd])
            if inclusive:
                nvo__rzq[yccp__hnzd] = zfkb__iuv <= right and zfkb__iuv >= left
            else:
                nvo__rzq[yccp__hnzd] = zfkb__iuv < right and zfkb__iuv > left
        return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, index, name)
    return impl


@overload_method(SeriesType, 'repeat', inline='always', no_unliteral=True)
def overload_series_repeat(S, repeats, axis=None):
    hvuw__yveso = dict(axis=axis)
    ltyv__lube = dict(axis=None)
    check_unsupported_args('Series.repeat', hvuw__yveso, ltyv__lube)
    if not (isinstance(repeats, types.Integer) or is_iterable_type(repeats) and
        isinstance(repeats.dtype, types.Integer)):
        raise BodoError(
            "Series.repeat(): 'repeats' should be an integer or array of integers"
            )
    if isinstance(repeats, types.Integer):

        def impl_int(S, repeats, axis=None):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            chv__twj = bodo.utils.conversion.index_to_array(index)
            nvo__rzq = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
            pfwr__xvs = bodo.libs.array_kernels.repeat_kernel(chv__twj, repeats
                )
            uwzni__tzd = bodo.utils.conversion.index_from_array(pfwr__xvs)
            return bodo.hiframes.pd_series_ext.init_series(nvo__rzq,
                uwzni__tzd, name)
        return impl_int

    def impl_arr(S, repeats, axis=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        chv__twj = bodo.utils.conversion.index_to_array(index)
        repeats = bodo.utils.conversion.coerce_to_array(repeats)
        nvo__rzq = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
        pfwr__xvs = bodo.libs.array_kernels.repeat_kernel(chv__twj, repeats)
        uwzni__tzd = bodo.utils.conversion.index_from_array(pfwr__xvs)
        return bodo.hiframes.pd_series_ext.init_series(nvo__rzq, uwzni__tzd,
            name)
    return impl_arr


@overload_method(SeriesType, 'to_dict', no_unliteral=True)
def overload_to_dict(S, into=None):

    def impl(S, into=None):
        nassr__yaob = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        n = len(nassr__yaob)
        jiki__axmlf = {}
        for yccp__hnzd in range(n):
            zfkb__iuv = bodo.utils.conversion.box_if_dt64(nassr__yaob[
                yccp__hnzd])
            jiki__axmlf[index[yccp__hnzd]] = zfkb__iuv
        return jiki__axmlf
    return impl


@overload_method(SeriesType, 'to_frame', inline='always', no_unliteral=True)
def overload_series_to_frame(S, name=None):
    oiwr__dyjo = (
        "Series.to_frame(): output column name should be known at compile time. Set 'name' to a constant value."
        )
    if is_overload_none(name):
        if is_literal_type(S.name_typ):
            bht__ssbow = get_literal_value(S.name_typ)
        else:
            raise_bodo_error(oiwr__dyjo)
    elif is_literal_type(name):
        bht__ssbow = get_literal_value(name)
    else:
        raise_bodo_error(oiwr__dyjo)
    bht__ssbow = 0 if bht__ssbow is None else bht__ssbow

    def impl(S, name=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,), index,
            (bht__ssbow,))
    return impl
