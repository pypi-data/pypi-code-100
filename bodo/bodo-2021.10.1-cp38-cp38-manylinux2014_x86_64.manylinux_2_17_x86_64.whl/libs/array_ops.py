"""
Implements array operations for usage by DataFrames and Series
such as count and max.
"""
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.extending import overload
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.utils.typing import element_type, is_hashable_type, is_iterable_type, is_overload_true, is_overload_zero


@numba.njit
def array_op_median(arr, skipna=True, parallel=False):
    ygq__vbs = np.empty(1, types.float64)
    bodo.libs.array_kernels.median_series_computation(ygq__vbs.ctypes, arr,
        parallel, skipna)
    return ygq__vbs[0]


def array_op_isna(arr):
    pass


@overload(array_op_isna)
def overload_array_op_isna(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        nbnq__tays = len(arr)
        tnksw__qxg = np.empty(nbnq__tays, np.bool_)
        for lffc__qdemc in numba.parfors.parfor.internal_prange(nbnq__tays):
            tnksw__qxg[lffc__qdemc] = bodo.libs.array_kernels.isna(arr,
                lffc__qdemc)
        return tnksw__qxg
    return impl


def array_op_count(arr):
    pass


@overload(array_op_count)
def overload_array_op_count(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        nbci__ijagy = 0
        for lffc__qdemc in numba.parfors.parfor.internal_prange(len(arr)):
            qkb__qdbt = 0
            if not bodo.libs.array_kernels.isna(arr, lffc__qdemc):
                qkb__qdbt = 1
            nbci__ijagy += qkb__qdbt
        ygq__vbs = nbci__ijagy
        return ygq__vbs
    return impl


def array_op_describe(arr):
    pass


def array_op_describe_impl(arr):
    gaq__irva = array_op_count(arr)
    lqi__umnf = array_op_min(arr)
    bys__rblw = array_op_max(arr)
    iml__ptpo = array_op_mean(arr)
    wzl__kwd = array_op_std(arr)
    kju__cngjf = array_op_quantile(arr, 0.25)
    cukz__vhw = array_op_quantile(arr, 0.5)
    hnw__nulb = array_op_quantile(arr, 0.75)
    return (gaq__irva, iml__ptpo, wzl__kwd, lqi__umnf, kju__cngjf,
        cukz__vhw, hnw__nulb, bys__rblw)


def array_op_describe_dt_impl(arr):
    gaq__irva = array_op_count(arr)
    lqi__umnf = array_op_min(arr)
    bys__rblw = array_op_max(arr)
    iml__ptpo = array_op_mean(arr)
    kju__cngjf = array_op_quantile(arr, 0.25)
    cukz__vhw = array_op_quantile(arr, 0.5)
    hnw__nulb = array_op_quantile(arr, 0.75)
    return (gaq__irva, iml__ptpo, lqi__umnf, kju__cngjf, cukz__vhw,
        hnw__nulb, bys__rblw)


@overload(array_op_describe)
def overload_array_op_describe(arr):
    if arr.dtype == bodo.datetime64ns:
        return array_op_describe_dt_impl
    return array_op_describe_impl


def array_op_min(arr):
    pass


@overload(array_op_min)
def overload_array_op_min(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            lxcg__uem = numba.cpython.builtins.get_type_max_value(np.int64)
            nbci__ijagy = 0
            for lffc__qdemc in numba.parfors.parfor.internal_prange(len(arr)):
                itofp__lvxsl = lxcg__uem
                qkb__qdbt = 0
                if not bodo.libs.array_kernels.isna(arr, lffc__qdemc):
                    itofp__lvxsl = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[lffc__qdemc]))
                    qkb__qdbt = 1
                lxcg__uem = min(lxcg__uem, itofp__lvxsl)
                nbci__ijagy += qkb__qdbt
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(lxcg__uem,
                nbci__ijagy)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            lxcg__uem = numba.cpython.builtins.get_type_max_value(np.int64)
            nbci__ijagy = 0
            for lffc__qdemc in numba.parfors.parfor.internal_prange(len(arr)):
                itofp__lvxsl = lxcg__uem
                qkb__qdbt = 0
                if not bodo.libs.array_kernels.isna(arr, lffc__qdemc):
                    itofp__lvxsl = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[lffc__qdemc]))
                    qkb__qdbt = 1
                lxcg__uem = min(lxcg__uem, itofp__lvxsl)
                nbci__ijagy += qkb__qdbt
            return bodo.hiframes.pd_index_ext._dti_val_finalize(lxcg__uem,
                nbci__ijagy)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            qjrz__gohve = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            lxcg__uem = numba.cpython.builtins.get_type_max_value(np.int64)
            nbci__ijagy = 0
            for lffc__qdemc in numba.parfors.parfor.internal_prange(len(
                qjrz__gohve)):
                cpwhq__dbg = qjrz__gohve[lffc__qdemc]
                if cpwhq__dbg == -1:
                    continue
                lxcg__uem = min(lxcg__uem, cpwhq__dbg)
                nbci__ijagy += 1
            ygq__vbs = bodo.hiframes.series_kernels._box_cat_val(lxcg__uem,
                arr.dtype, nbci__ijagy)
            return ygq__vbs
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            lxcg__uem = bodo.hiframes.series_kernels._get_date_max_value()
            nbci__ijagy = 0
            for lffc__qdemc in numba.parfors.parfor.internal_prange(len(arr)):
                itofp__lvxsl = lxcg__uem
                qkb__qdbt = 0
                if not bodo.libs.array_kernels.isna(arr, lffc__qdemc):
                    itofp__lvxsl = arr[lffc__qdemc]
                    qkb__qdbt = 1
                lxcg__uem = min(lxcg__uem, itofp__lvxsl)
                nbci__ijagy += qkb__qdbt
            ygq__vbs = bodo.hiframes.series_kernels._sum_handle_nan(lxcg__uem,
                nbci__ijagy)
            return ygq__vbs
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        lxcg__uem = bodo.hiframes.series_kernels._get_type_max_value(arr.dtype)
        nbci__ijagy = 0
        for lffc__qdemc in numba.parfors.parfor.internal_prange(len(arr)):
            itofp__lvxsl = lxcg__uem
            qkb__qdbt = 0
            if not bodo.libs.array_kernels.isna(arr, lffc__qdemc):
                itofp__lvxsl = arr[lffc__qdemc]
                qkb__qdbt = 1
            lxcg__uem = min(lxcg__uem, itofp__lvxsl)
            nbci__ijagy += qkb__qdbt
        ygq__vbs = bodo.hiframes.series_kernels._sum_handle_nan(lxcg__uem,
            nbci__ijagy)
        return ygq__vbs
    return impl


def array_op_max(arr):
    pass


@overload(array_op_max)
def overload_array_op_max(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            lxcg__uem = numba.cpython.builtins.get_type_min_value(np.int64)
            nbci__ijagy = 0
            for lffc__qdemc in numba.parfors.parfor.internal_prange(len(arr)):
                itofp__lvxsl = lxcg__uem
                qkb__qdbt = 0
                if not bodo.libs.array_kernels.isna(arr, lffc__qdemc):
                    itofp__lvxsl = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[lffc__qdemc]))
                    qkb__qdbt = 1
                lxcg__uem = max(lxcg__uem, itofp__lvxsl)
                nbci__ijagy += qkb__qdbt
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(lxcg__uem,
                nbci__ijagy)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            lxcg__uem = numba.cpython.builtins.get_type_min_value(np.int64)
            nbci__ijagy = 0
            for lffc__qdemc in numba.parfors.parfor.internal_prange(len(arr)):
                itofp__lvxsl = lxcg__uem
                qkb__qdbt = 0
                if not bodo.libs.array_kernels.isna(arr, lffc__qdemc):
                    itofp__lvxsl = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[lffc__qdemc]))
                    qkb__qdbt = 1
                lxcg__uem = max(lxcg__uem, itofp__lvxsl)
                nbci__ijagy += qkb__qdbt
            return bodo.hiframes.pd_index_ext._dti_val_finalize(lxcg__uem,
                nbci__ijagy)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            qjrz__gohve = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            lxcg__uem = -1
            for lffc__qdemc in numba.parfors.parfor.internal_prange(len(
                qjrz__gohve)):
                lxcg__uem = max(lxcg__uem, qjrz__gohve[lffc__qdemc])
            ygq__vbs = bodo.hiframes.series_kernels._box_cat_val(lxcg__uem,
                arr.dtype, 1)
            return ygq__vbs
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            lxcg__uem = bodo.hiframes.series_kernels._get_date_min_value()
            nbci__ijagy = 0
            for lffc__qdemc in numba.parfors.parfor.internal_prange(len(arr)):
                itofp__lvxsl = lxcg__uem
                qkb__qdbt = 0
                if not bodo.libs.array_kernels.isna(arr, lffc__qdemc):
                    itofp__lvxsl = arr[lffc__qdemc]
                    qkb__qdbt = 1
                lxcg__uem = max(lxcg__uem, itofp__lvxsl)
                nbci__ijagy += qkb__qdbt
            ygq__vbs = bodo.hiframes.series_kernels._sum_handle_nan(lxcg__uem,
                nbci__ijagy)
            return ygq__vbs
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        lxcg__uem = bodo.hiframes.series_kernels._get_type_min_value(arr.dtype)
        nbci__ijagy = 0
        for lffc__qdemc in numba.parfors.parfor.internal_prange(len(arr)):
            itofp__lvxsl = lxcg__uem
            qkb__qdbt = 0
            if not bodo.libs.array_kernels.isna(arr, lffc__qdemc):
                itofp__lvxsl = arr[lffc__qdemc]
                qkb__qdbt = 1
            lxcg__uem = max(lxcg__uem, itofp__lvxsl)
            nbci__ijagy += qkb__qdbt
        ygq__vbs = bodo.hiframes.series_kernels._sum_handle_nan(lxcg__uem,
            nbci__ijagy)
        return ygq__vbs
    return impl


def array_op_mean(arr):
    pass


@overload(array_op_mean)
def overload_array_op_mean(arr):
    if arr.dtype == bodo.datetime64ns:

        def impl(arr):
            return pd.Timestamp(types.int64(bodo.libs.array_ops.
                array_op_mean(arr.view(np.int64))))
        return impl
    odl__edhk = types.float64
    lbt__rmd = types.float64
    if isinstance(arr, types.Array) and arr.dtype == types.float32:
        odl__edhk = types.float32
        lbt__rmd = types.float32
    ycx__bvdpp = odl__edhk(0)
    mcu__xrvlh = lbt__rmd(0)
    orq__avbr = lbt__rmd(1)

    def impl(arr):
        numba.parfors.parfor.init_prange()
        lxcg__uem = ycx__bvdpp
        nbci__ijagy = mcu__xrvlh
        for lffc__qdemc in numba.parfors.parfor.internal_prange(len(arr)):
            itofp__lvxsl = ycx__bvdpp
            qkb__qdbt = mcu__xrvlh
            if not bodo.libs.array_kernels.isna(arr, lffc__qdemc):
                itofp__lvxsl = arr[lffc__qdemc]
                qkb__qdbt = orq__avbr
            lxcg__uem += itofp__lvxsl
            nbci__ijagy += qkb__qdbt
        ygq__vbs = bodo.hiframes.series_kernels._mean_handle_nan(lxcg__uem,
            nbci__ijagy)
        return ygq__vbs
    return impl


def array_op_var(arr, skipna, ddof):
    pass


@overload(array_op_var)
def overload_array_op_var(arr, skipna, ddof):

    def impl(arr, skipna, ddof):
        numba.parfors.parfor.init_prange()
        ipcxd__tlbr = 0.0
        fvle__grf = 0.0
        nbci__ijagy = 0
        for lffc__qdemc in numba.parfors.parfor.internal_prange(len(arr)):
            itofp__lvxsl = 0.0
            qkb__qdbt = 0
            if not bodo.libs.array_kernels.isna(arr, lffc__qdemc
                ) or not skipna:
                itofp__lvxsl = arr[lffc__qdemc]
                qkb__qdbt = 1
            ipcxd__tlbr += itofp__lvxsl
            fvle__grf += itofp__lvxsl * itofp__lvxsl
            nbci__ijagy += qkb__qdbt
        lxcg__uem = fvle__grf - ipcxd__tlbr * ipcxd__tlbr / nbci__ijagy
        ygq__vbs = bodo.hiframes.series_kernels._handle_nan_count_ddof(
            lxcg__uem, nbci__ijagy, ddof)
        return ygq__vbs
    return impl


def array_op_std(arr, skipna=True, ddof=1):
    pass


@overload(array_op_std)
def overload_array_op_std(arr, skipna=True, ddof=1):
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr, skipna=True, ddof=1):
            return pd.Timedelta(types.int64(array_op_var(arr.view(np.int64),
                skipna, ddof) ** 0.5))
        return impl_dt64
    return lambda arr, skipna=True, ddof=1: array_op_var(arr, skipna, ddof
        ) ** 0.5


def array_op_quantile(arr, q):
    pass


@overload(array_op_quantile)
def overload_array_op_quantile(arr, q):
    if is_iterable_type(q):
        if arr.dtype == bodo.datetime64ns:

            def _impl_list_dt(arr, q):
                tnksw__qxg = np.empty(len(q), np.int64)
                for lffc__qdemc in range(len(q)):
                    oksm__xqld = np.float64(q[lffc__qdemc])
                    tnksw__qxg[lffc__qdemc] = bodo.libs.array_kernels.quantile(
                        arr.view(np.int64), oksm__xqld)
                return tnksw__qxg.view(np.dtype('datetime64[ns]'))
            return _impl_list_dt

        def impl_list(arr, q):
            tnksw__qxg = np.empty(len(q), np.float64)
            for lffc__qdemc in range(len(q)):
                oksm__xqld = np.float64(q[lffc__qdemc])
                tnksw__qxg[lffc__qdemc] = bodo.libs.array_kernels.quantile(arr,
                    oksm__xqld)
            return tnksw__qxg
        return impl_list
    if arr.dtype == bodo.datetime64ns:

        def _impl_dt(arr, q):
            return pd.Timestamp(bodo.libs.array_kernels.quantile(arr.view(
                np.int64), np.float64(q)))
        return _impl_dt

    def impl(arr, q):
        return bodo.libs.array_kernels.quantile(arr, np.float64(q))
    return impl


def array_op_sum(arr, skipna, min_count):
    pass


@overload(array_op_sum, no_unliteral=True)
def overload_array_op_sum(arr, skipna, min_count):
    if isinstance(arr.dtype, types.Integer):
        xtv__gyo = types.intp
    elif arr.dtype == types.bool_:
        xtv__gyo = np.int64
    else:
        xtv__gyo = arr.dtype
    qepoy__thp = xtv__gyo(0)
    if isinstance(arr.dtype, types.Float) and (not is_overload_true(skipna) or
        not is_overload_zero(min_count)):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            lxcg__uem = qepoy__thp
            nbnq__tays = len(arr)
            nbci__ijagy = 0
            for lffc__qdemc in numba.parfors.parfor.internal_prange(nbnq__tays
                ):
                itofp__lvxsl = qepoy__thp
                qkb__qdbt = 0
                if not bodo.libs.array_kernels.isna(arr, lffc__qdemc
                    ) or not skipna:
                    itofp__lvxsl = arr[lffc__qdemc]
                    qkb__qdbt = 1
                lxcg__uem += itofp__lvxsl
                nbci__ijagy += qkb__qdbt
            ygq__vbs = bodo.hiframes.series_kernels._var_handle_mincount(
                lxcg__uem, nbci__ijagy, min_count)
            return ygq__vbs
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            lxcg__uem = qepoy__thp
            nbnq__tays = len(arr)
            for lffc__qdemc in numba.parfors.parfor.internal_prange(nbnq__tays
                ):
                itofp__lvxsl = qepoy__thp
                if not bodo.libs.array_kernels.isna(arr, lffc__qdemc):
                    itofp__lvxsl = arr[lffc__qdemc]
                lxcg__uem += itofp__lvxsl
            return lxcg__uem
    return impl


def array_op_prod(arr, skipna, min_count):
    pass


@overload(array_op_prod)
def overload_array_op_prod(arr, skipna, min_count):
    fojl__znb = arr.dtype(1)
    if arr.dtype == types.bool_:
        fojl__znb = 1
    if isinstance(arr.dtype, types.Float):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            lxcg__uem = fojl__znb
            nbci__ijagy = 0
            for lffc__qdemc in numba.parfors.parfor.internal_prange(len(arr)):
                itofp__lvxsl = fojl__znb
                qkb__qdbt = 0
                if not bodo.libs.array_kernels.isna(arr, lffc__qdemc
                    ) or not skipna:
                    itofp__lvxsl = arr[lffc__qdemc]
                    qkb__qdbt = 1
                nbci__ijagy += qkb__qdbt
                lxcg__uem *= itofp__lvxsl
            ygq__vbs = bodo.hiframes.series_kernels._var_handle_mincount(
                lxcg__uem, nbci__ijagy, min_count)
            return ygq__vbs
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            lxcg__uem = fojl__znb
            for lffc__qdemc in numba.parfors.parfor.internal_prange(len(arr)):
                itofp__lvxsl = fojl__znb
                if not bodo.libs.array_kernels.isna(arr, lffc__qdemc):
                    itofp__lvxsl = arr[lffc__qdemc]
                lxcg__uem *= itofp__lvxsl
            return lxcg__uem
    return impl


def array_op_idxmax(arr, index):
    pass


@overload(array_op_idxmax, inline='always')
def overload_array_op_idxmax(arr, index):

    def impl(arr, index):
        lffc__qdemc = bodo.libs.array_kernels._nan_argmax(arr)
        return index[lffc__qdemc]
    return impl


def array_op_idxmin(arr, index):
    pass


@overload(array_op_idxmin, inline='always')
def overload_array_op_idxmin(arr, index):

    def impl(arr, index):
        lffc__qdemc = bodo.libs.array_kernels._nan_argmin(arr)
        return index[lffc__qdemc]
    return impl


def _convert_isin_values(values, use_hash_impl):
    pass


@overload(_convert_isin_values, no_unliteral=True)
def overload_convert_isin_values(values, use_hash_impl):
    if is_overload_true(use_hash_impl):

        def impl(values, use_hash_impl):
            nryza__ajf = {}
            for agxu__npj in values:
                nryza__ajf[bodo.utils.conversion.box_if_dt64(agxu__npj)] = 0
            return nryza__ajf
        return impl
    else:

        def impl(values, use_hash_impl):
            return values
        return impl


def array_op_isin(arr, values):
    pass


@overload(array_op_isin, inline='always')
def overload_array_op_isin(arr, values):
    use_hash_impl = element_type(values) == element_type(arr
        ) and is_hashable_type(element_type(values))

    def impl(arr, values):
        values = bodo.libs.array_ops._convert_isin_values(values, use_hash_impl
            )
        numba.parfors.parfor.init_prange()
        nbnq__tays = len(arr)
        tnksw__qxg = np.empty(nbnq__tays, np.bool_)
        for lffc__qdemc in numba.parfors.parfor.internal_prange(nbnq__tays):
            tnksw__qxg[lffc__qdemc] = bodo.utils.conversion.box_if_dt64(arr
                [lffc__qdemc]) in values
        return tnksw__qxg
    return impl
