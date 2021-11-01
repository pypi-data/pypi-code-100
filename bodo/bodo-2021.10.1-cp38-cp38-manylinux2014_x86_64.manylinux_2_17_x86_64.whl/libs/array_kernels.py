"""
Implements array kernels such as median and quantile.
"""
import hashlib
import inspect
import math
import operator
import re
import warnings
from math import sqrt
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types, typing
from numba.core.imputils import lower_builtin
from numba.core.ir_utils import find_const, guard
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import overload, overload_attribute, register_jitable
from numba.np.arrayobj import make_array
from numba.np.numpy_support import as_dtype
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, init_categorical_array
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.libs import quantile_alg
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_info_decref_array, delete_table, delete_table_decref_arrays, drop_duplicates_table, info_from_table, info_to_array, sample_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, offset_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.distributed_api import Reduce_Type
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import str_arr_set_na, string_array_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.shuffle import getitem_arr_tup_single
from bodo.utils.typing import BodoError, check_unsupported_args, find_common_np_dtype, get_overload_const_list, get_overload_const_str, is_overload_none, raise_bodo_error
from bodo.utils.utils import build_set_seen_na, check_and_propagate_cpp_exception, numba_to_c_type, unliteral_all
ll.add_symbol('quantile_sequential', quantile_alg.quantile_sequential)
ll.add_symbol('quantile_parallel', quantile_alg.quantile_parallel)
MPI_ROOT = 0
sum_op = np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value)


def isna(arr, i):
    return False


@overload(isna)
def overload_isna(arr, i):
    i = types.unliteral(i)
    if arr == string_array_type:
        return lambda arr, i: bodo.libs.str_arr_ext.str_arr_is_na(arr, i)
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type,
        datetime_timedelta_array_type, string_array_split_view_type):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr
            ._null_bitmap, i)
    if isinstance(arr, ArrayItemArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.array_item_arr_ext.get_null_bitmap(arr), i)
    if isinstance(arr, StructArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.struct_arr_ext.get_null_bitmap(arr), i)
    if isinstance(arr, TupleArrayType):
        return lambda arr, i: bodo.libs.array_kernels.isna(arr._data, i)
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        return lambda arr, i: arr.codes[i] == -1
    if arr == bodo.binary_array_type:
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.array_item_arr_ext.get_null_bitmap(arr._data), i)
    if isinstance(arr, types.List):
        if arr.dtype == types.none:
            return lambda arr, i: True
        elif isinstance(arr.dtype, types.optional):
            return lambda arr, i: arr[i] is None
        else:
            return lambda arr, i: False
    assert isinstance(arr, types.Array)
    dtype = arr.dtype
    if isinstance(dtype, types.Float):
        return lambda arr, i: np.isnan(arr[i])
    if isinstance(dtype, (types.NPDatetime, types.NPTimedelta)):
        return lambda arr, i: np.isnat(arr[i])
    return lambda arr, i: False


def setna(arr, ind, int_nan_const=0):
    arr[ind] = np.nan


@overload(setna, no_unliteral=True)
def setna_overload(arr, ind, int_nan_const=0):
    if isinstance(arr.dtype, types.Float):
        return setna
    if isinstance(arr.dtype, (types.NPDatetime, types.NPTimedelta)):
        yjtc__xoiw = arr.dtype('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr[ind] = yjtc__xoiw
        return _setnan_impl
    if arr == string_array_type:

        def impl(arr, ind, int_nan_const=0):
            arr[ind] = ''
            str_arr_set_na(arr, ind)
        return impl
    if arr == boolean_array:

        def impl(arr, ind, int_nan_const=0):
            arr[ind] = False
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)):
        return (lambda arr, ind, int_nan_const=0: bodo.libs.int_arr_ext.
            set_bit_to_arr(arr._null_bitmap, ind, 0))
    if arr == bodo.binary_array_type:

        def impl_binary_arr(arr, ind, int_nan_const=0):
            auxx__gks = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            auxx__gks[ind + 1] = auxx__gks[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_binary_arr
    if isinstance(arr, bodo.libs.array_item_arr_ext.ArrayItemArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            auxx__gks = bodo.libs.array_item_arr_ext.get_offsets(arr)
            auxx__gks[ind + 1] = auxx__gks[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr), ind, 0)
        return impl_arr_item
    if isinstance(arr, bodo.libs.struct_arr_ext.StructArrayType):

        def impl(arr, ind, int_nan_const=0):
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.struct_arr_ext.
                get_null_bitmap(arr), ind, 0)
            data = bodo.libs.struct_arr_ext.get_data(arr)
            setna_tup(data, ind)
        return impl
    if isinstance(arr, TupleArrayType):

        def impl(arr, ind, int_nan_const=0):
            bodo.libs.array_kernels.setna(arr._data, ind)
        return impl
    if arr.dtype == types.bool_:

        def b_set(arr, ind, int_nan_const=0):
            arr[ind] = False
        return b_set
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):

        def setna_cat(arr, ind, int_nan_const=0):
            arr.codes[ind] = -1
        return setna_cat
    if isinstance(arr.dtype, types.Integer):

        def setna_int(arr, ind, int_nan_const=0):
            arr[ind] = int_nan_const
        return setna_int
    if arr == datetime_date_array_type:

        def setna_datetime_date(arr, ind, int_nan_const=0):
            arr._data[ind] = (1970 << 32) + (1 << 16) + 1
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return setna_datetime_date
    if arr == datetime_timedelta_array_type:

        def setna_datetime_timedelta(arr, ind, int_nan_const=0):
            bodo.libs.array_kernels.setna(arr._days_data, ind)
            bodo.libs.array_kernels.setna(arr._seconds_data, ind)
            bodo.libs.array_kernels.setna(arr._microseconds_data, ind)
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return setna_datetime_timedelta
    return lambda arr, ind, int_nan_const=0: None


def setna_tup(arr_tup, ind, int_nan_const=0):
    for arr in arr_tup:
        arr[ind] = np.nan


@overload(setna_tup, no_unliteral=True)
def overload_setna_tup(arr_tup, ind, int_nan_const=0):
    psjt__cloz = arr_tup.count
    swt__ykazt = 'def f(arr_tup, ind, int_nan_const=0):\n'
    for i in range(psjt__cloz):
        swt__ykazt += '  setna(arr_tup[{}], ind, int_nan_const)\n'.format(i)
    swt__ykazt += '  return\n'
    dny__przd = {}
    exec(swt__ykazt, {'setna': setna}, dny__przd)
    impl = dny__przd['f']
    return impl


def setna_slice(arr, s):
    arr[s] = np.nan


@overload(setna_slice, no_unliteral=True)
def overload_setna_slice(arr, s):

    def impl(arr, s):
        fimaj__tqca = numba.cpython.unicode._normalize_slice(s, len(arr))
        for i in range(fimaj__tqca.start, fimaj__tqca.stop, fimaj__tqca.step):
            setna(arr, i)
    return impl


ll.add_symbol('median_series_computation', quantile_alg.
    median_series_computation)
_median_series_computation = types.ExternalFunction('median_series_computation'
    , types.void(types.voidptr, bodo.libs.array.array_info_type, types.
    bool_, types.bool_))


@numba.njit
def median_series_computation(res, arr, is_parallel, skipna):
    xskn__xuwa = array_to_info(arr)
    _median_series_computation(res, xskn__xuwa, is_parallel, skipna)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(xskn__xuwa)


ll.add_symbol('autocorr_series_computation', quantile_alg.
    autocorr_series_computation)
_autocorr_series_computation = types.ExternalFunction(
    'autocorr_series_computation', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def autocorr_series_computation(res, arr, lag, is_parallel):
    xskn__xuwa = array_to_info(arr)
    _autocorr_series_computation(res, xskn__xuwa, lag, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(xskn__xuwa)


@numba.njit
def autocorr(arr, lag=1, parallel=False):
    res = np.empty(1, types.float64)
    autocorr_series_computation(res.ctypes, arr, lag, parallel)
    return res[0]


ll.add_symbol('compute_series_monotonicity', quantile_alg.
    compute_series_monotonicity)
_compute_series_monotonicity = types.ExternalFunction(
    'compute_series_monotonicity', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def series_monotonicity_call(res, arr, inc_dec, is_parallel):
    xskn__xuwa = array_to_info(arr)
    _compute_series_monotonicity(res, xskn__xuwa, inc_dec, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(xskn__xuwa)


@numba.njit
def series_monotonicity(arr, inc_dec, parallel=False):
    res = np.empty(1, types.float64)
    series_monotonicity_call(res.ctypes, arr, inc_dec, parallel)
    lba__tlohn = res[0] > 0.5
    return lba__tlohn


def quantile(A, q):
    return 0


def quantile_parallel(A, q):
    return 0


@infer_global(quantile)
@infer_global(quantile_parallel)
class QuantileType(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) in [2, 3]
        return signature(types.float64, *unliteral_all(args))


@lower_builtin(quantile, types.Array, types.float64)
@lower_builtin(quantile, IntegerArrayType, types.float64)
@lower_builtin(quantile, BooleanArrayType, types.float64)
def lower_dist_quantile_seq(context, builder, sig, args):
    olav__iuj = numba_to_c_type(sig.args[0].dtype)
    pspzp__snd = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), olav__iuj))
    brjrk__bztpx = args[0]
    nygyw__bgbl = sig.args[0]
    if isinstance(nygyw__bgbl, (IntegerArrayType, BooleanArrayType)):
        brjrk__bztpx = cgutils.create_struct_proxy(nygyw__bgbl)(context,
            builder, brjrk__bztpx).data
        nygyw__bgbl = types.Array(nygyw__bgbl.dtype, 1, 'C')
    assert nygyw__bgbl.ndim == 1
    arr = make_array(nygyw__bgbl)(context, builder, brjrk__bztpx)
    tqzbm__bigvo = builder.extract_value(arr.shape, 0)
    eknir__hoaso = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        tqzbm__bigvo, args[1], builder.load(pspzp__snd)]
    zpu__hti = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        DoubleType(), lir.IntType(32)]
    vyb__lble = lir.FunctionType(lir.DoubleType(), zpu__hti)
    zzq__ujdqo = cgutils.get_or_insert_function(builder.module, vyb__lble,
        name='quantile_sequential')
    xui__avb = builder.call(zzq__ujdqo, eknir__hoaso)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return xui__avb


@lower_builtin(quantile_parallel, types.Array, types.float64, types.intp)
@lower_builtin(quantile_parallel, IntegerArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, BooleanArrayType, types.float64, types.intp)
def lower_dist_quantile_parallel(context, builder, sig, args):
    olav__iuj = numba_to_c_type(sig.args[0].dtype)
    pspzp__snd = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), olav__iuj))
    brjrk__bztpx = args[0]
    nygyw__bgbl = sig.args[0]
    if isinstance(nygyw__bgbl, (IntegerArrayType, BooleanArrayType)):
        brjrk__bztpx = cgutils.create_struct_proxy(nygyw__bgbl)(context,
            builder, brjrk__bztpx).data
        nygyw__bgbl = types.Array(nygyw__bgbl.dtype, 1, 'C')
    assert nygyw__bgbl.ndim == 1
    arr = make_array(nygyw__bgbl)(context, builder, brjrk__bztpx)
    tqzbm__bigvo = builder.extract_value(arr.shape, 0)
    if len(args) == 3:
        zzu__hzw = args[2]
    else:
        zzu__hzw = tqzbm__bigvo
    eknir__hoaso = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        tqzbm__bigvo, zzu__hzw, args[1], builder.load(pspzp__snd)]
    zpu__hti = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.IntType(
        64), lir.DoubleType(), lir.IntType(32)]
    vyb__lble = lir.FunctionType(lir.DoubleType(), zpu__hti)
    zzq__ujdqo = cgutils.get_or_insert_function(builder.module, vyb__lble,
        name='quantile_parallel')
    xui__avb = builder.call(zzq__ujdqo, eknir__hoaso)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return xui__avb


@numba.njit
def min_heapify(arr, ind_arr, n, start, cmp_f):
    xje__wjlq = start
    qmsph__kanu = 2 * start + 1
    nsea__zfuq = 2 * start + 2
    if qmsph__kanu < n and not cmp_f(arr[qmsph__kanu], arr[xje__wjlq]):
        xje__wjlq = qmsph__kanu
    if nsea__zfuq < n and not cmp_f(arr[nsea__zfuq], arr[xje__wjlq]):
        xje__wjlq = nsea__zfuq
    if xje__wjlq != start:
        arr[start], arr[xje__wjlq] = arr[xje__wjlq], arr[start]
        ind_arr[start], ind_arr[xje__wjlq] = ind_arr[xje__wjlq], ind_arr[start]
        min_heapify(arr, ind_arr, n, xje__wjlq, cmp_f)


def select_k_nonan(A, index_arr, m, k):
    return A[:k]


@overload(select_k_nonan, no_unliteral=True)
def select_k_nonan_overload(A, index_arr, m, k):
    dtype = A.dtype
    if isinstance(dtype, types.Integer):
        return lambda A, index_arr, m, k: (A[:k].copy(), index_arr[:k].copy
            (), k)

    def select_k_nonan_float(A, index_arr, m, k):
        bboqm__dgu = np.empty(k, A.dtype)
        bjy__nry = np.empty(k, index_arr.dtype)
        i = 0
        ind = 0
        while i < m and ind < k:
            if not bodo.libs.array_kernels.isna(A, i):
                bboqm__dgu[ind] = A[i]
                bjy__nry[ind] = index_arr[i]
                ind += 1
            i += 1
        if ind < k:
            bboqm__dgu = bboqm__dgu[:ind]
            bjy__nry = bjy__nry[:ind]
        return bboqm__dgu, bjy__nry, i
    return select_k_nonan_float


@numba.njit
def nlargest(A, index_arr, k, is_largest, cmp_f):
    m = len(A)
    if k == 0:
        return A[:0], index_arr[:0]
    if k >= m:
        cjmc__lxrzt = np.sort(A)
        mvf__fsgoq = index_arr[np.argsort(A)]
        eoj__rbztt = pd.Series(cjmc__lxrzt).notna().values
        cjmc__lxrzt = cjmc__lxrzt[eoj__rbztt]
        mvf__fsgoq = mvf__fsgoq[eoj__rbztt]
        if is_largest:
            cjmc__lxrzt = cjmc__lxrzt[::-1]
            mvf__fsgoq = mvf__fsgoq[::-1]
        return np.ascontiguousarray(cjmc__lxrzt), np.ascontiguousarray(
            mvf__fsgoq)
    bboqm__dgu, bjy__nry, start = select_k_nonan(A, index_arr, m, k)
    bjy__nry = bjy__nry[bboqm__dgu.argsort()]
    bboqm__dgu.sort()
    if not is_largest:
        bboqm__dgu = np.ascontiguousarray(bboqm__dgu[::-1])
        bjy__nry = np.ascontiguousarray(bjy__nry[::-1])
    for i in range(start, m):
        if cmp_f(A[i], bboqm__dgu[0]):
            bboqm__dgu[0] = A[i]
            bjy__nry[0] = index_arr[i]
            min_heapify(bboqm__dgu, bjy__nry, k, 0, cmp_f)
    bjy__nry = bjy__nry[bboqm__dgu.argsort()]
    bboqm__dgu.sort()
    if is_largest:
        bboqm__dgu = bboqm__dgu[::-1]
        bjy__nry = bjy__nry[::-1]
    return np.ascontiguousarray(bboqm__dgu), np.ascontiguousarray(bjy__nry)


@numba.njit
def nlargest_parallel(A, I, k, is_largest, cmp_f):
    nprft__ztfh = bodo.libs.distributed_api.get_rank()
    vonv__tpcq, vvvzx__elpqi = nlargest(A, I, k, is_largest, cmp_f)
    gti__eqcdd = bodo.libs.distributed_api.gatherv(vonv__tpcq)
    lokyx__bzgw = bodo.libs.distributed_api.gatherv(vvvzx__elpqi)
    if nprft__ztfh == MPI_ROOT:
        res, yhmmr__fvx = nlargest(gti__eqcdd, lokyx__bzgw, k, is_largest,
            cmp_f)
    else:
        res = np.empty(k, A.dtype)
        yhmmr__fvx = np.empty(k, I.dtype)
    bodo.libs.distributed_api.bcast(res)
    bodo.libs.distributed_api.bcast(yhmmr__fvx)
    return res, yhmmr__fvx


@numba.njit(no_cpython_wrapper=True, cache=True)
def nancorr(mat, cov=0, minpv=1, parallel=False):
    tcpi__huw, ptt__hzl = mat.shape
    rvti__lwqtp = np.empty((ptt__hzl, ptt__hzl), dtype=np.float64)
    for psi__vrq in range(ptt__hzl):
        for oown__vaj in range(psi__vrq + 1):
            wxrt__yifjc = 0
            lirmq__bhj = fvief__qsazs = bgaw__cmgqe = bug__goq = 0.0
            for i in range(tcpi__huw):
                if np.isfinite(mat[i, psi__vrq]) and np.isfinite(mat[i,
                    oown__vaj]):
                    pitwz__pogie = mat[i, psi__vrq]
                    opgz__ggb = mat[i, oown__vaj]
                    wxrt__yifjc += 1
                    bgaw__cmgqe += pitwz__pogie
                    bug__goq += opgz__ggb
            if parallel:
                wxrt__yifjc = bodo.libs.distributed_api.dist_reduce(wxrt__yifjc
                    , sum_op)
                bgaw__cmgqe = bodo.libs.distributed_api.dist_reduce(bgaw__cmgqe
                    , sum_op)
                bug__goq = bodo.libs.distributed_api.dist_reduce(bug__goq,
                    sum_op)
            if wxrt__yifjc < minpv:
                rvti__lwqtp[psi__vrq, oown__vaj] = rvti__lwqtp[oown__vaj,
                    psi__vrq] = np.nan
            else:
                ubn__gusoa = bgaw__cmgqe / wxrt__yifjc
                fajl__bclhb = bug__goq / wxrt__yifjc
                bgaw__cmgqe = 0.0
                for i in range(tcpi__huw):
                    if np.isfinite(mat[i, psi__vrq]) and np.isfinite(mat[i,
                        oown__vaj]):
                        pitwz__pogie = mat[i, psi__vrq] - ubn__gusoa
                        opgz__ggb = mat[i, oown__vaj] - fajl__bclhb
                        bgaw__cmgqe += pitwz__pogie * opgz__ggb
                        lirmq__bhj += pitwz__pogie * pitwz__pogie
                        fvief__qsazs += opgz__ggb * opgz__ggb
                if parallel:
                    bgaw__cmgqe = bodo.libs.distributed_api.dist_reduce(
                        bgaw__cmgqe, sum_op)
                    lirmq__bhj = bodo.libs.distributed_api.dist_reduce(
                        lirmq__bhj, sum_op)
                    fvief__qsazs = bodo.libs.distributed_api.dist_reduce(
                        fvief__qsazs, sum_op)
                lkf__jtoy = wxrt__yifjc - 1.0 if cov else sqrt(lirmq__bhj *
                    fvief__qsazs)
                if lkf__jtoy != 0.0:
                    rvti__lwqtp[psi__vrq, oown__vaj] = rvti__lwqtp[
                        oown__vaj, psi__vrq] = bgaw__cmgqe / lkf__jtoy
                else:
                    rvti__lwqtp[psi__vrq, oown__vaj] = rvti__lwqtp[
                        oown__vaj, psi__vrq] = np.nan
    return rvti__lwqtp


@numba.njit(no_cpython_wrapper=True)
def duplicated(data, ind_arr, parallel=False):
    if parallel:
        data, (ind_arr,) = bodo.ir.join.parallel_shuffle(data, (ind_arr,))
    data = bodo.libs.str_arr_ext.to_list_if_immutable_arr(data)
    n = len(data[0])
    out = np.empty(n, np.bool_)
    zcvmq__yhlgj = dict()
    for i in range(n):
        val = getitem_arr_tup_single(data, i)
        if val in zcvmq__yhlgj:
            out[i] = True
        else:
            out[i] = False
            zcvmq__yhlgj[val] = 0
    return out, ind_arr


def sample_table_operation(data, ind_arr, n, frac, replace, parallel=False):
    return data, ind_arr


@overload(sample_table_operation, no_unliteral=True)
def overload_sample_table_operation(data, ind_arr, n, frac, replace,
    parallel=False):
    psjt__cloz = len(data)
    swt__ykazt = 'def impl(data, ind_arr, n, frac, replace, parallel=False):\n'
    swt__ykazt += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        psjt__cloz)))
    swt__ykazt += '  table_total = arr_info_list_to_table(info_list_total)\n'
    swt__ykazt += (
        '  out_table = sample_table(table_total, n, frac, replace, parallel)\n'
        .format(psjt__cloz))
    for utbb__geedv in range(psjt__cloz):
        swt__ykazt += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(utbb__geedv, utbb__geedv, utbb__geedv))
    swt__ykazt += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(psjt__cloz))
    swt__ykazt += '  delete_table(out_table)\n'
    swt__ykazt += '  delete_table(table_total)\n'
    swt__ykazt += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(psjt__cloz)))
    dny__przd = {}
    exec(swt__ykazt, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'sample_table': sample_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, dny__przd)
    impl = dny__przd['impl']
    return impl


def drop_duplicates(data, ind_arr, parallel=False):
    return data, ind_arr


@overload(drop_duplicates, no_unliteral=True)
def overload_drop_duplicates(data, ind_arr, parallel=False):
    psjt__cloz = len(data)
    swt__ykazt = 'def impl(data, ind_arr, parallel=False):\n'
    swt__ykazt += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        psjt__cloz)))
    swt__ykazt += '  table_total = arr_info_list_to_table(info_list_total)\n'
    swt__ykazt += '  keep_i = 0\n'
    swt__ykazt += (
        """  out_table = drop_duplicates_table(table_total, parallel, {}, keep_i, -1, False)
"""
        .format(psjt__cloz))
    for utbb__geedv in range(psjt__cloz):
        swt__ykazt += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(utbb__geedv, utbb__geedv, utbb__geedv))
    swt__ykazt += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(psjt__cloz))
    swt__ykazt += '  delete_table(out_table)\n'
    swt__ykazt += '  delete_table(table_total)\n'
    swt__ykazt += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(psjt__cloz)))
    dny__przd = {}
    exec(swt__ykazt, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'drop_duplicates_table': drop_duplicates_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, dny__przd)
    impl = dny__przd['impl']
    return impl


def dropna(data, how, thresh, subset, parallel=False):
    return data


@overload(dropna, no_unliteral=True)
def overload_dropna(data, how, thresh, subset):
    dqqe__iwx = len(data.types)
    temco__mdzzk = [('out' + str(i)) for i in range(dqqe__iwx)]
    faliz__yfmg = get_overload_const_list(subset)
    how = get_overload_const_str(how)
    uqy__ofxh = ['isna(data[{}], i)'.format(i) for i in faliz__yfmg]
    jxsn__dcci = 'not ({})'.format(' or '.join(uqy__ofxh))
    if not is_overload_none(thresh):
        jxsn__dcci = '(({}) <= ({}) - thresh)'.format(' + '.join(uqy__ofxh),
            dqqe__iwx - 1)
    elif how == 'all':
        jxsn__dcci = 'not ({})'.format(' and '.join(uqy__ofxh))
    swt__ykazt = 'def _dropna_imp(data, how, thresh, subset):\n'
    swt__ykazt += '  old_len = len(data[0])\n'
    swt__ykazt += '  new_len = 0\n'
    swt__ykazt += '  for i in range(old_len):\n'
    swt__ykazt += '    if {}:\n'.format(jxsn__dcci)
    swt__ykazt += '      new_len += 1\n'
    for i, out in enumerate(temco__mdzzk):
        if isinstance(data[i], bodo.CategoricalArrayType):
            swt__ykazt += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, data[{1}], (-1,))\n'
                .format(out, i))
        else:
            swt__ykazt += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, t{1}, (-1,))\n'
                .format(out, i))
    swt__ykazt += '  curr_ind = 0\n'
    swt__ykazt += '  for i in range(old_len):\n'
    swt__ykazt += '    if {}:\n'.format(jxsn__dcci)
    for i in range(dqqe__iwx):
        swt__ykazt += '      if isna(data[{}], i):\n'.format(i)
        swt__ykazt += '        setna({}, curr_ind)\n'.format(temco__mdzzk[i])
        swt__ykazt += '      else:\n'
        swt__ykazt += '        {}[curr_ind] = data[{}][i]\n'.format(
            temco__mdzzk[i], i)
    swt__ykazt += '      curr_ind += 1\n'
    swt__ykazt += '  return {}\n'.format(', '.join(temco__mdzzk))
    dny__przd = {}
    wfl__atrlu = {'t{}'.format(i): xyyte__plixg for i, xyyte__plixg in
        enumerate(data.types)}
    wfl__atrlu.update({'isna': isna, 'setna': setna, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'bodo': bodo})
    exec(swt__ykazt, wfl__atrlu, dny__przd)
    ocr__abjqm = dny__przd['_dropna_imp']
    return ocr__abjqm


def get(arr, ind):
    return pd.Series(arr).str.get(ind)


@overload(get, no_unliteral=True)
def overload_get(arr, ind):
    if isinstance(arr, ArrayItemArrayType):
        nygyw__bgbl = arr.dtype
        soc__hcoh = nygyw__bgbl.dtype

        def get_arr_item(arr, ind):
            n = len(arr)
            pqthg__gzbc = init_nested_counts(soc__hcoh)
            for k in range(n):
                if bodo.libs.array_kernels.isna(arr, k):
                    continue
                val = arr[k]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    continue
                pqthg__gzbc = add_nested_counts(pqthg__gzbc, val[ind])
            xvsot__ofc = bodo.utils.utils.alloc_type(n, nygyw__bgbl,
                pqthg__gzbc)
            for oju__rsw in range(n):
                if bodo.libs.array_kernels.isna(arr, oju__rsw):
                    setna(xvsot__ofc, oju__rsw)
                    continue
                val = arr[oju__rsw]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    setna(xvsot__ofc, oju__rsw)
                    continue
                xvsot__ofc[oju__rsw] = val[ind]
            return xvsot__ofc
        return get_arr_item


def concat(arr_list):
    return pd.concat(arr_list)


@overload(concat, no_unliteral=True)
def concat_overload(arr_list):
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, ArrayItemArrayType):
        vaecl__dnsv = arr_list.dtype.dtype

        def array_item_concat_impl(arr_list):
            ltnj__yiho = 0
            kmh__gcj = []
            for A in arr_list:
                upld__lku = len(A)
                kmh__gcj.append(bodo.libs.array_item_arr_ext.get_data(A))
                ltnj__yiho += upld__lku
            yskjm__wjwf = np.empty(ltnj__yiho + 1, offset_type)
            osifi__vxx = bodo.libs.array_kernels.concat(kmh__gcj)
            tind__hur = np.empty(ltnj__yiho + 7 >> 3, np.uint8)
            ujwg__cqx = 0
            qrrl__ldn = 0
            for A in arr_list:
                qbxx__iae = bodo.libs.array_item_arr_ext.get_offsets(A)
                jbvoq__wgi = bodo.libs.array_item_arr_ext.get_null_bitmap(A)
                upld__lku = len(A)
                lziqr__lwuoy = qbxx__iae[upld__lku]
                for i in range(upld__lku):
                    yskjm__wjwf[i + ujwg__cqx] = qbxx__iae[i] + qrrl__ldn
                    auibm__sbdr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        jbvoq__wgi, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(tind__hur, i +
                        ujwg__cqx, auibm__sbdr)
                ujwg__cqx += upld__lku
                qrrl__ldn += lziqr__lwuoy
            yskjm__wjwf[ujwg__cqx] = qrrl__ldn
            xvsot__ofc = bodo.libs.array_item_arr_ext.init_array_item_array(
                ltnj__yiho, osifi__vxx, yskjm__wjwf, tind__hur)
            return xvsot__ofc
        return array_item_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_date_array_type:

        def datetime_date_array_concat_impl(arr_list):
            wacj__lpd = 0
            for A in arr_list:
                wacj__lpd += len(A)
            hjg__kjq = (bodo.hiframes.datetime_date_ext.
                alloc_datetime_date_array(wacj__lpd))
            jzbsf__hecjs = 0
            for A in arr_list:
                for i in range(len(A)):
                    hjg__kjq._data[i + jzbsf__hecjs] = A._data[i]
                    auibm__sbdr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(hjg__kjq.
                        _null_bitmap, i + jzbsf__hecjs, auibm__sbdr)
                jzbsf__hecjs += len(A)
            return hjg__kjq
        return datetime_date_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_timedelta_array_type:

        def datetime_timedelta_array_concat_impl(arr_list):
            wacj__lpd = 0
            for A in arr_list:
                wacj__lpd += len(A)
            hjg__kjq = (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(wacj__lpd))
            jzbsf__hecjs = 0
            for A in arr_list:
                for i in range(len(A)):
                    hjg__kjq._days_data[i + jzbsf__hecjs] = A._days_data[i]
                    hjg__kjq._seconds_data[i + jzbsf__hecjs] = A._seconds_data[
                        i]
                    hjg__kjq._microseconds_data[i + jzbsf__hecjs
                        ] = A._microseconds_data[i]
                    auibm__sbdr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(hjg__kjq.
                        _null_bitmap, i + jzbsf__hecjs, auibm__sbdr)
                jzbsf__hecjs += len(A)
            return hjg__kjq
        return datetime_timedelta_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, DecimalArrayType):
        oqe__smim = arr_list.dtype.precision
        pbjdw__qheyn = arr_list.dtype.scale

        def decimal_array_concat_impl(arr_list):
            wacj__lpd = 0
            for A in arr_list:
                wacj__lpd += len(A)
            hjg__kjq = bodo.libs.decimal_arr_ext.alloc_decimal_array(wacj__lpd,
                oqe__smim, pbjdw__qheyn)
            jzbsf__hecjs = 0
            for A in arr_list:
                for i in range(len(A)):
                    hjg__kjq._data[i + jzbsf__hecjs] = A._data[i]
                    auibm__sbdr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(hjg__kjq.
                        _null_bitmap, i + jzbsf__hecjs, auibm__sbdr)
                jzbsf__hecjs += len(A)
            return hjg__kjq
        return decimal_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype in [string_array_type, bodo.binary_array_type]:
        if arr_list.dtype == bodo.binary_array_type:
            ocgb__gew = 'bodo.libs.str_arr_ext.pre_alloc_binary_array'
        elif arr_list.dtype == string_array_type:
            ocgb__gew = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        swt__ykazt = 'def impl(arr_list):  # pragma: no cover\n'
        swt__ykazt += '    # preallocate the output\n'
        swt__ykazt += '    num_strs = 0\n'
        swt__ykazt += '    num_chars = 0\n'
        swt__ykazt += '    for A in arr_list:\n'
        swt__ykazt += '        arr = A\n'
        swt__ykazt += '        num_strs += len(arr)\n'
        swt__ykazt += '        # this should work for both binary and string\n'
        swt__ykazt += (
            '        num_chars += bodo.libs.str_arr_ext.num_total_chars(arr)\n'
            )
        swt__ykazt += f'    out_arr = {ocgb__gew}(\n'
        swt__ykazt += '        num_strs, num_chars\n'
        swt__ykazt += '    )\n'
        swt__ykazt += (
            '    bodo.libs.str_arr_ext.set_null_bits_to_value(out_arr, -1)\n')
        swt__ykazt += '    # copy data to output\n'
        swt__ykazt += '    curr_str_ind = 0\n'
        swt__ykazt += '    curr_chars_ind = 0\n'
        swt__ykazt += '    for A in arr_list:\n'
        swt__ykazt += '        arr = A\n'
        swt__ykazt += '        # This will probably need to be extended\n'
        swt__ykazt += '        bodo.libs.str_arr_ext.set_string_array_range(\n'
        swt__ykazt += (
            '            out_arr, arr, curr_str_ind, curr_chars_ind\n')
        swt__ykazt += '        )\n'
        swt__ykazt += '        curr_str_ind += len(arr)\n'
        swt__ykazt += '        # this should work for both binary and string\n'
        swt__ykazt += (
            '        curr_chars_ind += bodo.libs.str_arr_ext.num_total_chars(arr)\n'
            )
        swt__ykazt += '    return out_arr\n'
        qmmqu__orpgt = dict()
        exec(swt__ykazt, {'bodo': bodo}, qmmqu__orpgt)
        szyig__fwyry = qmmqu__orpgt['impl']
        return szyig__fwyry
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, IntegerArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(xyyte__plixg.dtype, types.Integer) for
        xyyte__plixg in arr_list.types) and any(isinstance(xyyte__plixg,
        IntegerArrayType) for xyyte__plixg in arr_list.types):

        def impl_int_arr_list(arr_list):
            dou__jhsv = convert_to_nullable_tup(arr_list)
            pcdi__hclzh = []
            zovn__yej = 0
            for A in dou__jhsv:
                pcdi__hclzh.append(A._data)
                zovn__yej += len(A)
            osifi__vxx = bodo.libs.array_kernels.concat(pcdi__hclzh)
            utn__jzs = zovn__yej + 7 >> 3
            ndeui__cmn = np.empty(utn__jzs, np.uint8)
            bwetd__icpi = 0
            for A in dou__jhsv:
                leci__mubk = A._null_bitmap
                for oju__rsw in range(len(A)):
                    auibm__sbdr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        leci__mubk, oju__rsw)
                    bodo.libs.int_arr_ext.set_bit_to_arr(ndeui__cmn,
                        bwetd__icpi, auibm__sbdr)
                    bwetd__icpi += 1
            return bodo.libs.int_arr_ext.init_integer_array(osifi__vxx,
                ndeui__cmn)
        return impl_int_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == boolean_array or isinstance(arr_list, types
        .BaseTuple) and all(xyyte__plixg.dtype == types.bool_ for
        xyyte__plixg in arr_list.types) and any(xyyte__plixg ==
        boolean_array for xyyte__plixg in arr_list.types):

        def impl_bool_arr_list(arr_list):
            dou__jhsv = convert_to_nullable_tup(arr_list)
            pcdi__hclzh = []
            zovn__yej = 0
            for A in dou__jhsv:
                pcdi__hclzh.append(A._data)
                zovn__yej += len(A)
            osifi__vxx = bodo.libs.array_kernels.concat(pcdi__hclzh)
            utn__jzs = zovn__yej + 7 >> 3
            ndeui__cmn = np.empty(utn__jzs, np.uint8)
            bwetd__icpi = 0
            for A in dou__jhsv:
                leci__mubk = A._null_bitmap
                for oju__rsw in range(len(A)):
                    auibm__sbdr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        leci__mubk, oju__rsw)
                    bodo.libs.int_arr_ext.set_bit_to_arr(ndeui__cmn,
                        bwetd__icpi, auibm__sbdr)
                    bwetd__icpi += 1
            return bodo.libs.bool_arr_ext.init_bool_array(osifi__vxx,
                ndeui__cmn)
        return impl_bool_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, CategoricalArrayType):

        def cat_array_concat_impl(arr_list):
            rqpt__tnn = []
            for A in arr_list:
                rqpt__tnn.append(A.codes)
            return init_categorical_array(bodo.libs.array_kernels.concat(
                rqpt__tnn), arr_list[0].dtype)
        return cat_array_concat_impl
    if isinstance(arr_list, types.List) and isinstance(arr_list.dtype,
        types.Array) and arr_list.dtype.ndim == 1:
        dtype = arr_list.dtype.dtype

        def impl_np_arr_list(arr_list):
            zovn__yej = 0
            for A in arr_list:
                zovn__yej += len(A)
            xvsot__ofc = np.empty(zovn__yej, dtype)
            lssgs__rnjy = 0
            for A in arr_list:
                n = len(A)
                xvsot__ofc[lssgs__rnjy:lssgs__rnjy + n] = A
                lssgs__rnjy += n
            return xvsot__ofc
        return impl_np_arr_list
    if isinstance(arr_list, types.BaseTuple) and any(isinstance(
        xyyte__plixg, (types.Array, IntegerArrayType)) and isinstance(
        xyyte__plixg.dtype, types.Integer) for xyyte__plixg in arr_list.types
        ) and any(isinstance(xyyte__plixg, types.Array) and isinstance(
        xyyte__plixg.dtype, types.Float) for xyyte__plixg in arr_list.types):
        return lambda arr_list: np.concatenate(astype_float_tup(arr_list))
    for xysxk__jogpu in arr_list:
        if not isinstance(xysxk__jogpu, types.Array):
            raise_bodo_error('concat of array types {} not supported'.
                format(arr_list))
    return lambda arr_list: np.concatenate(arr_list)


def astype_float_tup(arr_tup):
    return tuple(xyyte__plixg.astype(np.float64) for xyyte__plixg in arr_tup)


@overload(astype_float_tup, no_unliteral=True)
def overload_astype_float_tup(arr_tup):
    assert isinstance(arr_tup, types.BaseTuple)
    psjt__cloz = len(arr_tup.types)
    swt__ykazt = 'def f(arr_tup):\n'
    swt__ykazt += '  return ({}{})\n'.format(','.join(
        'arr_tup[{}].astype(np.float64)'.format(i) for i in range(
        psjt__cloz)), ',' if psjt__cloz == 1 else '')
    dny__przd = {}
    exec(swt__ykazt, {'np': np}, dny__przd)
    kgmsy__cguv = dny__przd['f']
    return kgmsy__cguv


def convert_to_nullable_tup(arr_tup):
    return arr_tup


@overload(convert_to_nullable_tup, no_unliteral=True)
def overload_convert_to_nullable_tup(arr_tup):
    if isinstance(arr_tup, (types.UniTuple, types.List)) and isinstance(arr_tup
        .dtype, (IntegerArrayType, BooleanArrayType)):
        return lambda arr_tup: arr_tup
    assert isinstance(arr_tup, types.BaseTuple)
    psjt__cloz = len(arr_tup.types)
    hab__mtyai = find_common_np_dtype(arr_tup.types)
    soc__hcoh = None
    uwib__uwum = ''
    if isinstance(hab__mtyai, types.Integer):
        soc__hcoh = bodo.libs.int_arr_ext.IntDtype(hab__mtyai)
        uwib__uwum = '.astype(out_dtype, False)'
    swt__ykazt = 'def f(arr_tup):\n'
    swt__ykazt += '  return ({}{})\n'.format(','.join(
        'bodo.utils.conversion.coerce_to_array(arr_tup[{}], use_nullable_array=True){}'
        .format(i, uwib__uwum) for i in range(psjt__cloz)), ',' if 
        psjt__cloz == 1 else '')
    dny__przd = {}
    exec(swt__ykazt, {'bodo': bodo, 'out_dtype': soc__hcoh}, dny__przd)
    lcfr__hsevo = dny__przd['f']
    return lcfr__hsevo


def nunique(A, dropna):
    return len(set(A))


def nunique_parallel(A, dropna):
    return len(set(A))


@overload(nunique, no_unliteral=True)
def nunique_overload(A, dropna):

    def nunique_seq(A, dropna):
        s, yvs__pony = build_set_seen_na(A)
        return len(s) + int(not dropna and yvs__pony)
    return nunique_seq


@overload(nunique_parallel, no_unliteral=True)
def nunique_overload_parallel(A, dropna):
    sum_op = bodo.libs.distributed_api.Reduce_Type.Sum.value

    def nunique_par(A, dropna):
        fxyg__rwme = bodo.libs.array_kernels.unique(A, dropna, parallel=True)
        hhkrb__idgw = len(fxyg__rwme)
        return bodo.libs.distributed_api.dist_reduce(hhkrb__idgw, np.int32(
            sum_op))
    return nunique_par


def unique(A, dropna=False, parallel=False):
    return np.array([mnp__yparb for mnp__yparb in set(A)]).astype(A.dtype)


def cummin(A):
    return A


@overload(cummin, no_unliteral=True)
def cummin_overload(A):
    if isinstance(A.dtype, types.Float):
        ukfr__fxdiq = np.finfo(A.dtype(1).dtype).max
    else:
        ukfr__fxdiq = np.iinfo(A.dtype(1).dtype).max

    def impl(A):
        n = len(A)
        xvsot__ofc = np.empty(n, A.dtype)
        kyy__vnfr = ukfr__fxdiq
        for i in range(n):
            kyy__vnfr = min(kyy__vnfr, A[i])
            xvsot__ofc[i] = kyy__vnfr
        return xvsot__ofc
    return impl


def cummax(A):
    return A


@overload(cummax, no_unliteral=True)
def cummax_overload(A):
    if isinstance(A.dtype, types.Float):
        ukfr__fxdiq = np.finfo(A.dtype(1).dtype).min
    else:
        ukfr__fxdiq = np.iinfo(A.dtype(1).dtype).min

    def impl(A):
        n = len(A)
        xvsot__ofc = np.empty(n, A.dtype)
        kyy__vnfr = ukfr__fxdiq
        for i in range(n):
            kyy__vnfr = max(kyy__vnfr, A[i])
            xvsot__ofc[i] = kyy__vnfr
        return xvsot__ofc
    return impl


@overload(unique, no_unliteral=True)
def unique_overload(A, dropna=False, parallel=False):

    def unique_impl(A, dropna=False, parallel=False):
        zju__dyndn = arr_info_list_to_table([array_to_info(A)])
        suep__ycnwl = 1
        jtffj__brf = 0
        kqn__aewym = drop_duplicates_table(zju__dyndn, parallel,
            suep__ycnwl, jtffj__brf, -1, dropna)
        xvsot__ofc = info_to_array(info_from_table(kqn__aewym, 0), A)
        delete_table(zju__dyndn)
        delete_table(kqn__aewym)
        return xvsot__ofc
    return unique_impl


def explode(arr, index_arr):
    return pd.Series(arr, index_arr).explode()


@overload(explode, no_unliteral=True)
def overload_explode(arr, index_arr):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    vaecl__dnsv = arr.dtype
    dwrd__mdtyl = index_arr
    wnod__uunyb = dwrd__mdtyl.dtype

    def impl(arr, index_arr):
        n = len(arr)
        pqthg__gzbc = init_nested_counts(vaecl__dnsv)
        cnfx__zhkxd = init_nested_counts(wnod__uunyb)
        for i in range(n):
            wcg__hha = index_arr[i]
            if isna(arr, i):
                pqthg__gzbc = (pqthg__gzbc[0] + 1,) + pqthg__gzbc[1:]
                cnfx__zhkxd = add_nested_counts(cnfx__zhkxd, wcg__hha)
                continue
            pfnz__eopw = arr[i]
            if len(pfnz__eopw) == 0:
                pqthg__gzbc = (pqthg__gzbc[0] + 1,) + pqthg__gzbc[1:]
                cnfx__zhkxd = add_nested_counts(cnfx__zhkxd, wcg__hha)
                continue
            pqthg__gzbc = add_nested_counts(pqthg__gzbc, pfnz__eopw)
            for kupg__tmwiq in range(len(pfnz__eopw)):
                cnfx__zhkxd = add_nested_counts(cnfx__zhkxd, wcg__hha)
        xvsot__ofc = bodo.utils.utils.alloc_type(pqthg__gzbc[0],
            vaecl__dnsv, pqthg__gzbc[1:])
        gaukp__sdnm = bodo.utils.utils.alloc_type(pqthg__gzbc[0],
            dwrd__mdtyl, cnfx__zhkxd)
        qrrl__ldn = 0
        for i in range(n):
            if isna(arr, i):
                setna(xvsot__ofc, qrrl__ldn)
                gaukp__sdnm[qrrl__ldn] = index_arr[i]
                qrrl__ldn += 1
                continue
            pfnz__eopw = arr[i]
            lziqr__lwuoy = len(pfnz__eopw)
            if lziqr__lwuoy == 0:
                setna(xvsot__ofc, qrrl__ldn)
                gaukp__sdnm[qrrl__ldn] = index_arr[i]
                qrrl__ldn += 1
                continue
            xvsot__ofc[qrrl__ldn:qrrl__ldn + lziqr__lwuoy] = pfnz__eopw
            gaukp__sdnm[qrrl__ldn:qrrl__ldn + lziqr__lwuoy] = index_arr[i]
            qrrl__ldn += lziqr__lwuoy
        return xvsot__ofc, gaukp__sdnm
    return impl


def explode_str_split(arr, pat, n, index_arr):
    return pd.Series(arr, index_arr).str.split(pat, n).explode()


@overload(explode_str_split, no_unliteral=True)
def overload_explode_str_split(arr, pat, n, index_arr):
    assert arr == string_array_type
    dwrd__mdtyl = index_arr
    wnod__uunyb = dwrd__mdtyl.dtype

    def impl(arr, pat, n, index_arr):
        hzosq__iqw = pat is not None and len(pat) > 1
        if hzosq__iqw:
            crgy__ftq = re.compile(pat)
            if n == -1:
                n = 0
        elif n == 0:
            n = -1
        rnda__klxlw = len(arr)
        kpy__tfvjm = 0
        afg__qva = 0
        cnfx__zhkxd = init_nested_counts(wnod__uunyb)
        for i in range(rnda__klxlw):
            wcg__hha = index_arr[i]
            if bodo.libs.array_kernels.isna(arr, i):
                kpy__tfvjm += 1
                cnfx__zhkxd = add_nested_counts(cnfx__zhkxd, wcg__hha)
                continue
            if hzosq__iqw:
                nuti__hopvg = crgy__ftq.split(arr[i], maxsplit=n)
            else:
                nuti__hopvg = arr[i].split(pat, n)
            kpy__tfvjm += len(nuti__hopvg)
            for s in nuti__hopvg:
                cnfx__zhkxd = add_nested_counts(cnfx__zhkxd, wcg__hha)
                afg__qva += bodo.libs.str_arr_ext.get_utf8_size(s)
        xvsot__ofc = bodo.libs.str_arr_ext.pre_alloc_string_array(kpy__tfvjm,
            afg__qva)
        gaukp__sdnm = bodo.utils.utils.alloc_type(kpy__tfvjm, dwrd__mdtyl,
            cnfx__zhkxd)
        fvn__krn = 0
        for oju__rsw in range(rnda__klxlw):
            if isna(arr, oju__rsw):
                xvsot__ofc[fvn__krn] = ''
                bodo.libs.array_kernels.setna(xvsot__ofc, fvn__krn)
                gaukp__sdnm[fvn__krn] = index_arr[oju__rsw]
                fvn__krn += 1
                continue
            if hzosq__iqw:
                nuti__hopvg = crgy__ftq.split(arr[oju__rsw], maxsplit=n)
            else:
                nuti__hopvg = arr[oju__rsw].split(pat, n)
            ayg__bkne = len(nuti__hopvg)
            xvsot__ofc[fvn__krn:fvn__krn + ayg__bkne] = nuti__hopvg
            gaukp__sdnm[fvn__krn:fvn__krn + ayg__bkne] = index_arr[oju__rsw]
            fvn__krn += ayg__bkne
        return xvsot__ofc, gaukp__sdnm
    return impl


def gen_na_array(n, arr):
    return np.full(n, np.nan)


@overload(gen_na_array, no_unliteral=True)
def overload_gen_na_array(n, arr):
    if isinstance(arr, types.TypeRef):
        arr = arr.instance_type
    dtype = arr.dtype
    if isinstance(dtype, (types.Integer, types.Float)):
        dtype = dtype if isinstance(dtype, types.Float) else types.float64

        def impl_float(n, arr):
            numba.parfors.parfor.init_prange()
            xvsot__ofc = np.empty(n, dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                xvsot__ofc[i] = np.nan
            return xvsot__ofc
        return impl_float

    def impl(n, arr):
        numba.parfors.parfor.init_prange()
        xvsot__ofc = bodo.utils.utils.alloc_type(n, arr, (0,))
        for i in numba.parfors.parfor.internal_prange(n):
            setna(xvsot__ofc, i)
        return xvsot__ofc
    return impl


def gen_na_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_array_kernels_gen_na_array = (
    gen_na_array_equiv)


def resize_and_copy(A, new_len):
    return A


@overload(resize_and_copy, no_unliteral=True)
def overload_resize_and_copy(A, old_size, new_len):
    ksb__oqts = A
    if A == types.Array(types.uint8, 1, 'C'):

        def impl_char(A, old_size, new_len):
            xvsot__ofc = bodo.utils.utils.alloc_type(new_len, ksb__oqts)
            bodo.libs.str_arr_ext.str_copy_ptr(xvsot__ofc.ctypes, 0, A.
                ctypes, old_size)
            return xvsot__ofc
        return impl_char

    def impl(A, old_size, new_len):
        xvsot__ofc = bodo.utils.utils.alloc_type(new_len, ksb__oqts, (-1,))
        xvsot__ofc[:old_size] = A[:old_size]
        return xvsot__ofc
    return impl


@register_jitable
def calc_nitems(start, stop, step):
    yvixf__viem = math.ceil((stop - start) / step)
    return int(max(yvixf__viem, 0))


def calc_nitems_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    if guard(find_const, self.func_ir, args[0]) == 0 and guard(find_const,
        self.func_ir, args[2]) == 1:
        return ArrayAnalysis.AnalyzeResult(shape=args[1], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_array_kernels_calc_nitems = (
    calc_nitems_equiv)


def arange_parallel_impl(return_type, *args):
    dtype = as_dtype(return_type.dtype)

    def arange_1(stop):
        return np.arange(0, stop, 1, dtype)

    def arange_2(start, stop):
        return np.arange(start, stop, 1, dtype)

    def arange_3(start, stop, step):
        return np.arange(start, stop, step, dtype)
    if any(isinstance(mnp__yparb, types.Complex) for mnp__yparb in args):

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            syn__dsht = (stop - start) / step
            yvixf__viem = math.ceil(syn__dsht.real)
            vpvob__tcyj = math.ceil(syn__dsht.imag)
            jvgz__myas = int(max(min(vpvob__tcyj, yvixf__viem), 0))
            arr = np.empty(jvgz__myas, dtype)
            for i in numba.parfors.parfor.internal_prange(jvgz__myas):
                arr[i] = start + i * step
            return arr
    else:

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            jvgz__myas = bodo.libs.array_kernels.calc_nitems(start, stop, step)
            arr = np.empty(jvgz__myas, dtype)
            for i in numba.parfors.parfor.internal_prange(jvgz__myas):
                arr[i] = start + i * step
            return arr
    if len(args) == 1:
        return arange_1
    elif len(args) == 2:
        return arange_2
    elif len(args) == 3:
        return arange_3
    elif len(args) == 4:
        return arange_4
    else:
        raise BodoError('parallel arange with types {}'.format(args))


if bodo.numba_compat._check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.arange_parallel_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c72b0390b4f3e52dcc5426bd42c6b55ff96bae5a425381900985d36e7527a4bd':
        warnings.warn('numba.parfors.parfor.arange_parallel_impl has changed')
numba.parfors.parfor.swap_functions_map['arange', 'numpy'
    ] = arange_parallel_impl


def sort(arr, ascending, inplace):
    return np.sort(arr)


@overload(sort, no_unliteral=True)
def overload_sort(arr, ascending, inplace):

    def impl(arr, ascending, inplace):
        n = len(arr)
        data = np.arange(n),
        leirt__ohekc = arr,
        if not inplace:
            leirt__ohekc = arr.copy(),
        edmse__axplf = bodo.libs.str_arr_ext.to_list_if_immutable_arr(
            leirt__ohekc)
        nbiv__gzu = bodo.libs.str_arr_ext.to_list_if_immutable_arr(data, True)
        bodo.libs.timsort.sort(edmse__axplf, 0, n, nbiv__gzu)
        if not ascending:
            bodo.libs.timsort.reverseRange(edmse__axplf, 0, n, nbiv__gzu)
        bodo.libs.str_arr_ext.cp_str_list_to_array(leirt__ohekc, edmse__axplf)
        return leirt__ohekc[0]
    return impl


def overload_array_max(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).max()
        return impl


overload(np.max, inline='always', no_unliteral=True)(overload_array_max)
overload(max, inline='always', no_unliteral=True)(overload_array_max)


def overload_array_min(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).min()
        return impl


overload(np.min, inline='always', no_unliteral=True)(overload_array_min)
overload(min, inline='always', no_unliteral=True)(overload_array_min)


def overload_array_sum(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).sum()
    return impl


overload(np.sum, inline='always', no_unliteral=True)(overload_array_sum)
overload(sum, inline='always', no_unliteral=True)(overload_array_sum)


@overload(np.prod, inline='always', no_unliteral=True)
def overload_array_prod(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).prod()
    return impl


def nonzero(arr):
    return arr,


@overload(nonzero, no_unliteral=True)
def nonzero_overload(A, parallel=False):
    if not bodo.utils.utils.is_array_typ(A, False):
        return

    def impl(A, parallel=False):
        n = len(A)
        if parallel:
            htjj__hwi = bodo.libs.distributed_api.dist_exscan(n,
                Reduce_Type.Sum.value)
        else:
            htjj__hwi = 0
        rvti__lwqtp = []
        for i in range(n):
            if A[i]:
                rvti__lwqtp.append(i + htjj__hwi)
        return np.array(rvti__lwqtp, np.int64),
    return impl


@overload(np.sort, inline='always', no_unliteral=True)
def np_sort(A, axis=-1, kind=None, order=None):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    cok__dln = {'axis': axis, 'kind': kind, 'order': order}
    nxx__fdo = {'axis': -1, 'kind': None, 'order': None}
    check_unsupported_args('np.sort', cok__dln, nxx__fdo, 'numpy')

    def impl(A, axis=-1, kind=None, order=None):
        return pd.Series(A).sort_values().values
    return impl


def repeat_kernel(A, repeats):
    return A


@overload(repeat_kernel, no_unliteral=True)
def repeat_kernel_overload(A, repeats):
    ksb__oqts = A
    if isinstance(repeats, types.Integer):

        def impl_int(A, repeats):
            rnda__klxlw = len(A)
            xvsot__ofc = bodo.utils.utils.alloc_type(rnda__klxlw * repeats,
                ksb__oqts, (-1,))
            for i in range(rnda__klxlw):
                fvn__krn = i * repeats
                if bodo.libs.array_kernels.isna(A, i):
                    for oju__rsw in range(repeats):
                        bodo.libs.array_kernels.setna(xvsot__ofc, fvn__krn +
                            oju__rsw)
                else:
                    xvsot__ofc[fvn__krn:fvn__krn + repeats] = A[i]
            return xvsot__ofc
        return impl_int

    def impl_arr(A, repeats):
        rnda__klxlw = len(A)
        xvsot__ofc = bodo.utils.utils.alloc_type(repeats.sum(), ksb__oqts,
            (-1,))
        fvn__krn = 0
        for i in range(rnda__klxlw):
            bjz__qyg = repeats[i]
            if bodo.libs.array_kernels.isna(A, i):
                for oju__rsw in range(bjz__qyg):
                    bodo.libs.array_kernels.setna(xvsot__ofc, fvn__krn +
                        oju__rsw)
            else:
                xvsot__ofc[fvn__krn:fvn__krn + bjz__qyg] = A[i]
            fvn__krn += bjz__qyg
        return xvsot__ofc
    return impl_arr


@overload(np.repeat, inline='always', no_unliteral=True)
def np_repeat(A, repeats):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    if not isinstance(repeats, types.Integer):
        raise BodoError(
            'Only integer type supported for repeats in np.repeat()')

    def impl(A, repeats):
        return bodo.libs.array_kernels.repeat_kernel(A, repeats)
    return impl


@overload(np.unique, inline='always', no_unliteral=True)
def np_unique(A):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return

    def impl(A):
        apxjx__mqt = bodo.libs.array_kernels.unique(A)
        return bodo.allgatherv(apxjx__mqt, False)
    return impl


@overload(np.union1d, inline='always', no_unliteral=True)
def overload_union1d(A1, A2):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.union1d()')

    def impl(A1, A2):
        ixe__vrwm = bodo.libs.array_kernels.concat([A1, A2])
        vyfi__zrxr = bodo.libs.array_kernels.unique(ixe__vrwm)
        return pd.Series(vyfi__zrxr).sort_values().values
    return impl


@overload(np.intersect1d, inline='always', no_unliteral=True)
def overload_intersect1d(A1, A2, assume_unique=False, return_indices=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    cok__dln = {'assume_unique': assume_unique, 'return_indices':
        return_indices}
    nxx__fdo = {'assume_unique': False, 'return_indices': False}
    check_unsupported_args('np.intersect1d', cok__dln, nxx__fdo, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.intersect1d()'
            )
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.intersect1d()')

    def impl(A1, A2, assume_unique=False, return_indices=False):
        tpt__mrqkf = bodo.libs.array_kernels.unique(A1)
        fnzw__upgk = bodo.libs.array_kernels.unique(A2)
        ixe__vrwm = bodo.libs.array_kernels.concat([tpt__mrqkf, fnzw__upgk])
        quoly__opc = pd.Series(ixe__vrwm).sort_values().values
        return slice_array_intersect1d(quoly__opc)
    return impl


@register_jitable
def slice_array_intersect1d(arr):
    eoj__rbztt = arr[1:] == arr[:-1]
    return arr[:-1][eoj__rbztt]


@overload(np.setdiff1d, inline='always', no_unliteral=True)
def overload_setdiff1d(A1, A2, assume_unique=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    cok__dln = {'assume_unique': assume_unique}
    nxx__fdo = {'assume_unique': False}
    check_unsupported_args('np.setdiff1d', cok__dln, nxx__fdo, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.setdiff1d()')
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.setdiff1d()')

    def impl(A1, A2, assume_unique=False):
        tpt__mrqkf = bodo.libs.array_kernels.unique(A1)
        fnzw__upgk = bodo.libs.array_kernels.unique(A2)
        eoj__rbztt = calculate_mask_setdiff1d(tpt__mrqkf, fnzw__upgk)
        return pd.Series(tpt__mrqkf[eoj__rbztt]).sort_values().values
    return impl


@register_jitable
def calculate_mask_setdiff1d(A1, A2):
    eoj__rbztt = np.ones(len(A1), np.bool_)
    for i in range(len(A2)):
        eoj__rbztt &= A1 != A2[i]
    return eoj__rbztt


@overload(np.linspace, inline='always', no_unliteral=True)
def np_linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=
    None, axis=0):
    cok__dln = {'retstep': retstep, 'axis': axis}
    nxx__fdo = {'retstep': False, 'axis': 0}
    check_unsupported_args('np.linspace', cok__dln, nxx__fdo, 'numpy')
    vwzps__zqsz = False
    if is_overload_none(dtype):
        ksb__oqts = np.promote_types(np.promote_types(numba.np.
            numpy_support.as_dtype(start), numba.np.numpy_support.as_dtype(
            stop)), numba.np.numpy_support.as_dtype(types.float64)).type
    else:
        if isinstance(dtype.dtype, types.Integer):
            vwzps__zqsz = True
        ksb__oqts = numba.np.numpy_support.as_dtype(dtype).type
    if vwzps__zqsz:

        def impl_int(start, stop, num=50, endpoint=True, retstep=False,
            dtype=None, axis=0):
            jio__jmgbl = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            xvsot__ofc = np.empty(num, ksb__oqts)
            for i in numba.parfors.parfor.internal_prange(num):
                xvsot__ofc[i] = ksb__oqts(np.floor(start + i * jio__jmgbl))
            return xvsot__ofc
        return impl_int
    else:

        def impl(start, stop, num=50, endpoint=True, retstep=False, dtype=
            None, axis=0):
            jio__jmgbl = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            xvsot__ofc = np.empty(num, ksb__oqts)
            for i in numba.parfors.parfor.internal_prange(num):
                xvsot__ofc[i] = ksb__oqts(start + i * jio__jmgbl)
            return xvsot__ofc
        return impl


def np_linspace_get_stepsize(start, stop, num, endpoint):
    return 0


@overload(np_linspace_get_stepsize, no_unliteral=True)
def overload_np_linspace_get_stepsize(start, stop, num, endpoint):

    def impl(start, stop, num, endpoint):
        if num < 0:
            raise ValueError('np.linspace() Num must be >= 0')
        if endpoint:
            num -= 1
        if num > 1:
            return (stop - start) / num
        return 0
    return impl


@overload(operator.contains, no_unliteral=True)
def arr_contains(A, val):
    if not (bodo.utils.utils.is_array_typ(A, False) and A.dtype == types.
        unliteral(val)):
        return

    def impl(A, val):
        numba.parfors.parfor.init_prange()
        psjt__cloz = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                psjt__cloz += A[i] == val
        return psjt__cloz > 0
    return impl


@overload(np.any, inline='always', no_unliteral=True)
def np_any(A, axis=None, out=None, keepdims=None):
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    cok__dln = {'axis': axis, 'out': out, 'keepdims': keepdims}
    nxx__fdo = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', cok__dln, nxx__fdo, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        psjt__cloz = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                psjt__cloz += int(bool(A[i]))
        return psjt__cloz > 0
    return impl


@overload(np.all, inline='always', no_unliteral=True)
def np_all(A, axis=None, out=None, keepdims=None):
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    cok__dln = {'axis': axis, 'out': out, 'keepdims': keepdims}
    nxx__fdo = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', cok__dln, nxx__fdo, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        psjt__cloz = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                psjt__cloz += int(bool(A[i]))
        return psjt__cloz == n
    return impl


@overload(np.cbrt, inline='always', no_unliteral=True)
def np_cbrt(A, out=None, where=True, casting='same_kind', order='K', dtype=
    None, subok=True):
    if not (isinstance(A, types.Number) or bodo.utils.utils.is_array_typ(A,
        False) and A.ndim == 1 and isinstance(A.dtype, types.Number)):
        return
    cok__dln = {'out': out, 'where': where, 'casting': casting, 'order':
        order, 'dtype': dtype, 'subok': subok}
    nxx__fdo = {'out': None, 'where': True, 'casting': 'same_kind', 'order':
        'K', 'dtype': None, 'subok': True}
    check_unsupported_args('np.cbrt', cok__dln, nxx__fdo, 'numpy')
    if bodo.utils.utils.is_array_typ(A, False):
        kefyb__pul = np.promote_types(numba.np.numpy_support.as_dtype(A.
            dtype), numba.np.numpy_support.as_dtype(types.float32)).type

        def impl_arr(A, out=None, where=True, casting='same_kind', order=
            'K', dtype=None, subok=True):
            numba.parfors.parfor.init_prange()
            n = len(A)
            xvsot__ofc = np.empty(n, kefyb__pul)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(xvsot__ofc, i)
                    continue
                xvsot__ofc[i] = np_cbrt_scalar(A[i], kefyb__pul)
            return xvsot__ofc
        return impl_arr
    kefyb__pul = np.promote_types(numba.np.numpy_support.as_dtype(A), numba
        .np.numpy_support.as_dtype(types.float32)).type

    def impl_scalar(A, out=None, where=True, casting='same_kind', order='K',
        dtype=None, subok=True):
        return np_cbrt_scalar(A, kefyb__pul)
    return impl_scalar


@register_jitable
def np_cbrt_scalar(x, float_dtype):
    if np.isnan(x):
        return np.nan
    bwvi__jvkn = x < 0
    if bwvi__jvkn:
        x = -x
    res = np.power(float_dtype(x), 1.0 / 3.0)
    if bwvi__jvkn:
        return -res
    return res


@overload(np.hstack, no_unliteral=True)
def np_hstack(tup):
    fqvje__ngrgr = isinstance(tup, (types.BaseTuple, types.List))
    lkugq__vjnlk = isinstance(tup, (bodo.SeriesType, bodo.hiframes.
        pd_series_ext.HeterogeneousSeriesType)) and isinstance(tup.data, (
        types.BaseTuple, types.List))
    if isinstance(tup, types.BaseTuple):
        for xysxk__jogpu in tup.types:
            fqvje__ngrgr = fqvje__ngrgr and bodo.utils.utils.is_array_typ(
                xysxk__jogpu, False)
    elif isinstance(tup, types.List):
        fqvje__ngrgr = bodo.utils.utils.is_array_typ(tup.dtype, False)
    elif lkugq__vjnlk:
        for xysxk__jogpu in tup.data.types:
            lkugq__vjnlk = lkugq__vjnlk and bodo.utils.utils.is_array_typ(
                xysxk__jogpu, False)
    if not (fqvje__ngrgr or lkugq__vjnlk):
        return
    if lkugq__vjnlk:

        def impl_series(tup):
            arr_tup = bodo.hiframes.pd_series_ext.get_series_data(tup)
            return bodo.libs.array_kernels.concat(arr_tup)
        return impl_series

    def impl(tup):
        return bodo.libs.array_kernels.concat(tup)
    return impl


@overload(np.random.multivariate_normal, inline='always', no_unliteral=True)
def np_random_multivariate_normal(mean, cov, size=None, check_valid='warn',
    tol=1e-08):
    cok__dln = {'check_valid': check_valid, 'tol': tol}
    nxx__fdo = {'check_valid': 'warn', 'tol': 1e-08}
    check_unsupported_args('np.random.multivariate_normal', cok__dln,
        nxx__fdo, 'numpy')
    if not isinstance(size, types.Integer):
        raise BodoError(
            'np.random.multivariate_normal() size argument is required and must be an integer'
            )
    if not (bodo.utils.utils.is_array_typ(mean, False) and mean.ndim == 1):
        raise BodoError(
            'np.random.multivariate_normal() mean must be a 1 dimensional numpy array'
            )
    if not (bodo.utils.utils.is_array_typ(cov, False) and cov.ndim == 2):
        raise BodoError(
            'np.random.multivariate_normal() cov must be a 2 dimensional square, numpy array'
            )

    def impl(mean, cov, size=None, check_valid='warn', tol=1e-08):
        _validate_multivar_norm(cov)
        tcpi__huw = mean.shape[0]
        wywrs__isjq = size, tcpi__huw
        itp__gmdg = np.random.standard_normal(wywrs__isjq)
        cov = cov.astype(np.float64)
        bch__wrrec, s, enrx__tjjqs = np.linalg.svd(cov)
        res = np.dot(itp__gmdg, np.sqrt(s).reshape(tcpi__huw, 1) * enrx__tjjqs)
        dip__jvgfr = res + mean
        return dip__jvgfr
    return impl


def _validate_multivar_norm(cov):
    return


@overload(_validate_multivar_norm, no_unliteral=True)
def _overload_validate_multivar_norm(cov):

    def impl(cov):
        if cov.shape[0] != cov.shape[1]:
            raise ValueError(
                'np.random.multivariate_normal() cov must be a 2 dimensional square, numpy array'
                )
    return impl


def _nan_argmin(arr):
    return


@overload(_nan_argmin, no_unliteral=True)
def _overload_nan_argmin(arr):
    if isinstance(arr, IntegerArrayType) or arr in [boolean_array,
        datetime_date_array_type] or arr.dtype == bodo.timedelta64ns:

        def impl_bodo_arr(arr):
            numba.parfors.parfor.init_prange()
            vpan__chnx = bodo.hiframes.series_kernels._get_type_max_value(arr)
            bsw__dwmo = typing.builtins.IndexValue(-1, vpan__chnx)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                mefby__bffe = typing.builtins.IndexValue(i, arr[i])
                bsw__dwmo = min(bsw__dwmo, mefby__bffe)
            return bsw__dwmo.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        bot__ale = bodo.hiframes.pd_categorical_ext.get_categories_int_type(arr
            .dtype)

        def impl_cat_arr(arr):
            hlbt__jxju = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            vpan__chnx = bot__ale(len(arr.dtype.categories) + 1)
            bsw__dwmo = typing.builtins.IndexValue(-1, vpan__chnx)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                mefby__bffe = typing.builtins.IndexValue(i, hlbt__jxju[i])
                bsw__dwmo = min(bsw__dwmo, mefby__bffe)
            return bsw__dwmo.index
        return impl_cat_arr
    return lambda arr: arr.argmin()


def _nan_argmax(arr):
    return


@overload(_nan_argmax, no_unliteral=True)
def _overload_nan_argmax(arr):
    if isinstance(arr, IntegerArrayType) or arr in [boolean_array,
        datetime_date_array_type] or arr.dtype == bodo.timedelta64ns:

        def impl_bodo_arr(arr):
            n = len(arr)
            numba.parfors.parfor.init_prange()
            vpan__chnx = bodo.hiframes.series_kernels._get_type_min_value(arr)
            bsw__dwmo = typing.builtins.IndexValue(-1, vpan__chnx)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                mefby__bffe = typing.builtins.IndexValue(i, arr[i])
                bsw__dwmo = max(bsw__dwmo, mefby__bffe)
            return bsw__dwmo.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        bot__ale = bodo.hiframes.pd_categorical_ext.get_categories_int_type(arr
            .dtype)

        def impl_cat_arr(arr):
            n = len(arr)
            hlbt__jxju = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            vpan__chnx = bot__ale(-1)
            bsw__dwmo = typing.builtins.IndexValue(-1, vpan__chnx)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                mefby__bffe = typing.builtins.IndexValue(i, hlbt__jxju[i])
                bsw__dwmo = max(bsw__dwmo, mefby__bffe)
            return bsw__dwmo.index
        return impl_cat_arr
    return lambda arr: arr.argmax()


@overload_attribute(types.Array, 'nbytes', inline='always')
def overload_dataframe_index(A):
    return lambda A: A.size * bodo.io.np_io.get_dtype_size(A.dtype)
