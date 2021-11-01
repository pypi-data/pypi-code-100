import atexit
import datetime
import operator
import sys
import time
from collections import defaultdict
from decimal import Decimal
from enum import Enum
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from mpi4py import MPI
from numba.core import cgutils, ir_utils, types
from numba.core.typing import signature
from numba.core.typing.builtins import IndexValueType
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, models, overload, register_jitable, register_model
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.libs import hdist
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, np_offset_type, offset_type
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.libs.int_arr_ext import IntegerArrayType, set_bit_to_arr
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import convert_len_arr_to_offset, get_bit_bitmap, get_data_ptr, get_null_bitmap_ptr, get_offset_ptr, num_total_chars, pre_alloc_string_array, set_bit_to, string_array_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoError, is_overload_false, is_overload_none
from bodo.utils.utils import CTypeEnum, check_and_propagate_cpp_exception, empty_like_type, numba_to_c_type, tuple_to_scalar
ll.add_symbol('dist_get_time', hdist.dist_get_time)
ll.add_symbol('get_time', hdist.get_time)
ll.add_symbol('dist_reduce', hdist.dist_reduce)
ll.add_symbol('dist_arr_reduce', hdist.dist_arr_reduce)
ll.add_symbol('dist_exscan', hdist.dist_exscan)
ll.add_symbol('dist_irecv', hdist.dist_irecv)
ll.add_symbol('dist_isend', hdist.dist_isend)
ll.add_symbol('dist_wait', hdist.dist_wait)
ll.add_symbol('dist_get_item_pointer', hdist.dist_get_item_pointer)
ll.add_symbol('get_dummy_ptr', hdist.get_dummy_ptr)
ll.add_symbol('allgather', hdist.allgather)
ll.add_symbol('comm_req_alloc', hdist.comm_req_alloc)
ll.add_symbol('comm_req_dealloc', hdist.comm_req_dealloc)
ll.add_symbol('req_array_setitem', hdist.req_array_setitem)
ll.add_symbol('dist_waitall', hdist.dist_waitall)
ll.add_symbol('oneD_reshape_shuffle', hdist.oneD_reshape_shuffle)
ll.add_symbol('permutation_int', hdist.permutation_int)
ll.add_symbol('permutation_array_index', hdist.permutation_array_index)
ll.add_symbol('c_get_rank', hdist.dist_get_rank)
ll.add_symbol('c_get_size', hdist.dist_get_size)
ll.add_symbol('c_barrier', hdist.barrier)
ll.add_symbol('c_alltoall', hdist.c_alltoall)
ll.add_symbol('c_gather_scalar', hdist.c_gather_scalar)
ll.add_symbol('c_gatherv', hdist.c_gatherv)
ll.add_symbol('c_scatterv', hdist.c_scatterv)
ll.add_symbol('c_allgatherv', hdist.c_allgatherv)
ll.add_symbol('c_bcast', hdist.c_bcast)
ll.add_symbol('c_recv', hdist.dist_recv)
ll.add_symbol('c_send', hdist.dist_send)
mpi_req_numba_type = getattr(types, 'int' + str(8 * hdist.mpi_req_num_bytes))
MPI_ROOT = 0
ANY_SOURCE = np.int32(hdist.ANY_SOURCE)


class Reduce_Type(Enum):
    Sum = 0
    Prod = 1
    Min = 2
    Max = 3
    Argmin = 4
    Argmax = 5
    Or = 6
    Concat = 7
    No_Op = 8


_get_rank = types.ExternalFunction('c_get_rank', types.int32())
_get_size = types.ExternalFunction('c_get_size', types.int32())
_barrier = types.ExternalFunction('c_barrier', types.int32())


@numba.njit
def get_rank():
    return _get_rank()


@numba.njit
def get_size():
    return _get_size()


@numba.njit
def barrier():
    _barrier()


_get_time = types.ExternalFunction('get_time', types.float64())
dist_time = types.ExternalFunction('dist_get_time', types.float64())


@overload(time.time, no_unliteral=True)
def overload_time_time():
    return lambda : _get_time()


@numba.generated_jit(nopython=True)
def get_type_enum(arr):
    arr = arr.instance_type if isinstance(arr, types.TypeRef) else arr
    dtype = arr.dtype
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):
        dtype = bodo.hiframes.pd_categorical_ext.get_categories_int_type(dtype)
    typ_val = numba_to_c_type(dtype)
    return lambda arr: np.int32(typ_val)


INT_MAX = np.iinfo(np.int32).max
_send = types.ExternalFunction('c_send', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def send(val, rank, tag):
    send_arr = np.full(1, val)
    xjsa__umzw = get_type_enum(send_arr)
    _send(send_arr.ctypes, 1, xjsa__umzw, rank, tag)


_recv = types.ExternalFunction('c_recv', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def recv(dtype, rank, tag):
    recv_arr = np.empty(1, dtype)
    xjsa__umzw = get_type_enum(recv_arr)
    _recv(recv_arr.ctypes, 1, xjsa__umzw, rank, tag)
    return recv_arr[0]


_isend = types.ExternalFunction('dist_isend', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def isend(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            xjsa__umzw = get_type_enum(arr)
            return _isend(arr.ctypes, size, xjsa__umzw, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        xjsa__umzw = np.int32(numba_to_c_type(arr.dtype))
        orh__hirro = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            lviwl__wnsdp = size + 7 >> 3
            kdm__gopx = _isend(arr._data.ctypes, size, xjsa__umzw, pe, tag,
                cond)
            rssg__geeh = _isend(arr._null_bitmap.ctypes, lviwl__wnsdp,
                orh__hirro, pe, tag, cond)
            return kdm__gopx, rssg__geeh
        return impl_nullable
    if arr in [binary_array_type, string_array_type]:
        ijv__rdl = np.int32(numba_to_c_type(offset_type))
        orh__hirro = np.int32(numba_to_c_type(types.uint8))

        def impl_str_arr(arr, size, pe, tag, cond=True):
            jypuo__gagy = np.int64(bodo.libs.str_arr_ext.num_total_chars(arr))
            send(jypuo__gagy, pe, tag - 1)
            lviwl__wnsdp = size + 7 >> 3
            _send(bodo.libs.str_arr_ext.get_offset_ptr(arr), size + 1,
                ijv__rdl, pe, tag)
            _send(bodo.libs.str_arr_ext.get_data_ptr(arr), jypuo__gagy,
                orh__hirro, pe, tag)
            _send(bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr),
                lviwl__wnsdp, orh__hirro, pe, tag)
            return None
        return impl_str_arr
    typ_enum = numba_to_c_type(types.uint8)

    def impl_voidptr(arr, size, pe, tag, cond=True):
        return _isend(arr, size, typ_enum, pe, tag, cond)
    return impl_voidptr


_irecv = types.ExternalFunction('dist_irecv', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def irecv(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            xjsa__umzw = get_type_enum(arr)
            return _irecv(arr.ctypes, size, xjsa__umzw, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        xjsa__umzw = np.int32(numba_to_c_type(arr.dtype))
        orh__hirro = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            lviwl__wnsdp = size + 7 >> 3
            kdm__gopx = _irecv(arr._data.ctypes, size, xjsa__umzw, pe, tag,
                cond)
            rssg__geeh = _irecv(arr._null_bitmap.ctypes, lviwl__wnsdp,
                orh__hirro, pe, tag, cond)
            return kdm__gopx, rssg__geeh
        return impl_nullable
    if arr in [binary_array_type, string_array_type]:
        ijv__rdl = np.int32(numba_to_c_type(offset_type))
        orh__hirro = np.int32(numba_to_c_type(types.uint8))
        if arr == binary_array_type:
            vdwy__avhj = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            vdwy__avhj = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        laee__nljh = f"""def impl(arr, size, pe, tag, cond=True):
            # recv the number of string characters and resize buffer to proper size
            n_chars = bodo.libs.distributed_api.recv(np.int64, pe, tag - 1)
            new_arr = {vdwy__avhj}(size, n_chars)
            bodo.libs.str_arr_ext.move_str_binary_arr_payload(arr, new_arr)

            n_bytes = (size + 7) >> 3
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_offset_ptr(arr),
                size + 1,
                offset_typ_enum,
                pe,
                tag,
            )
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_data_ptr(arr), n_chars, char_typ_enum, pe, tag
            )
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr),
                n_bytes,
                char_typ_enum,
                pe,
                tag,
            )
            return None"""
        mysn__otrqi = dict()
        exec(laee__nljh, {'bodo': bodo, 'np': np, 'offset_typ_enum':
            ijv__rdl, 'char_typ_enum': orh__hirro}, mysn__otrqi)
        impl = mysn__otrqi['impl']
        return impl
    raise BodoError(f'irecv(): array type {arr} not supported yet')


_alltoall = types.ExternalFunction('c_alltoall', types.void(types.voidptr,
    types.voidptr, types.int32, types.int32))


@numba.njit
def alltoall(send_arr, recv_arr, count):
    assert count < INT_MAX
    xjsa__umzw = get_type_enum(send_arr)
    _alltoall(send_arr.ctypes, recv_arr.ctypes, np.int32(count), xjsa__umzw)


@numba.generated_jit(nopython=True)
def gather_scalar(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    data = types.unliteral(data)
    typ_val = numba_to_c_type(data)
    dtype = data

    def gather_scalar_impl(data, allgather=False, warn_if_rep=True, root=
        MPI_ROOT):
        n_pes = bodo.libs.distributed_api.get_size()
        rank = bodo.libs.distributed_api.get_rank()
        send = np.full(1, data, dtype)
        iyxjn__wbp = n_pes if rank == root or allgather else 0
        hyzpk__cefr = np.empty(iyxjn__wbp, dtype)
        c_gather_scalar(send.ctypes, hyzpk__cefr.ctypes, np.int32(typ_val),
            allgather, np.int32(root))
        return hyzpk__cefr
    return gather_scalar_impl


c_gather_scalar = types.ExternalFunction('c_gather_scalar', types.void(
    types.voidptr, types.voidptr, types.int32, types.bool_, types.int32))
c_gatherv = types.ExternalFunction('c_gatherv', types.void(types.voidptr,
    types.int32, types.voidptr, types.voidptr, types.voidptr, types.int32,
    types.bool_, types.int32))
c_scatterv = types.ExternalFunction('c_scatterv', types.void(types.voidptr,
    types.voidptr, types.voidptr, types.voidptr, types.int32, types.int32))


@intrinsic
def value_to_ptr(typingctx, val_tp=None):

    def codegen(context, builder, sig, args):
        nvsx__lpdtz = cgutils.alloca_once(builder, args[0].type)
        builder.store(args[0], nvsx__lpdtz)
        return builder.bitcast(nvsx__lpdtz, lir.IntType(8).as_pointer())
    return types.voidptr(val_tp), codegen


@intrinsic
def load_val_ptr(typingctx, ptr_tp, val_tp=None):

    def codegen(context, builder, sig, args):
        nvsx__lpdtz = builder.bitcast(args[0], args[1].type.as_pointer())
        return builder.load(nvsx__lpdtz)
    return val_tp(ptr_tp, val_tp), codegen


_dist_reduce = types.ExternalFunction('dist_reduce', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))
_dist_arr_reduce = types.ExternalFunction('dist_arr_reduce', types.void(
    types.voidptr, types.int64, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_reduce(value, reduce_op):
    if isinstance(value, types.Array):
        typ_enum = np.int32(numba_to_c_type(value.dtype))

        def impl_arr(value, reduce_op):
            A = np.ascontiguousarray(value)
            _dist_arr_reduce(A.ctypes, A.size, reduce_op, typ_enum)
            return A
        return impl_arr
    khmd__tgrs = types.unliteral(value)
    if isinstance(khmd__tgrs, IndexValueType):
        khmd__tgrs = khmd__tgrs.val_typ
        ncwi__dlt = [types.bool_, types.uint8, types.int8, types.uint16,
            types.int16, types.uint32, types.int32, types.float32, types.
            float64]
        if not sys.platform.startswith('win'):
            ncwi__dlt.append(types.int64)
            ncwi__dlt.append(bodo.datetime64ns)
            ncwi__dlt.append(bodo.timedelta64ns)
            ncwi__dlt.append(bodo.datetime_date_type)
        if khmd__tgrs not in ncwi__dlt:
            raise BodoError('argmin/argmax not supported for type {}'.
                format(khmd__tgrs))
    typ_enum = np.int32(numba_to_c_type(khmd__tgrs))

    def impl(value, reduce_op):
        xayw__fbr = value_to_ptr(value)
        ipit__upc = value_to_ptr(value)
        _dist_reduce(xayw__fbr, ipit__upc, reduce_op, typ_enum)
        return load_val_ptr(ipit__upc, value)
    return impl


_dist_exscan = types.ExternalFunction('dist_exscan', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_exscan(value, reduce_op):
    khmd__tgrs = types.unliteral(value)
    typ_enum = np.int32(numba_to_c_type(khmd__tgrs))
    lkj__bekj = khmd__tgrs(0)

    def impl(value, reduce_op):
        xayw__fbr = value_to_ptr(value)
        ipit__upc = value_to_ptr(lkj__bekj)
        _dist_exscan(xayw__fbr, ipit__upc, reduce_op, typ_enum)
        return load_val_ptr(ipit__upc, value)
    return impl


@numba.njit
def get_bit(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@numba.njit
def copy_gathered_null_bytes(null_bitmap_ptr, tmp_null_bytes,
    recv_counts_nulls, recv_counts):
    uzgs__wwbl = 0
    kuqqv__edh = 0
    for i in range(len(recv_counts)):
        rttb__rmcs = recv_counts[i]
        lviwl__wnsdp = recv_counts_nulls[i]
        zxul__gme = tmp_null_bytes[uzgs__wwbl:uzgs__wwbl + lviwl__wnsdp]
        for hgzlp__tpyjb in range(rttb__rmcs):
            set_bit_to(null_bitmap_ptr, kuqqv__edh, get_bit(zxul__gme,
                hgzlp__tpyjb))
            kuqqv__edh += 1
        uzgs__wwbl += lviwl__wnsdp


@numba.generated_jit(nopython=True)
def gatherv(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    from bodo.libs.csr_matrix_ext import CSRMatrixType
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            tthd__glwtr = bodo.gatherv(data.codes, allgather, root=root)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                tthd__glwtr, data.dtype)
        return impl_cat
    if isinstance(data, types.Array):
        typ_val = numba_to_c_type(data.dtype)

        def gatherv_impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            data = np.ascontiguousarray(data)
            rank = bodo.libs.distributed_api.get_rank()
            hjkv__ijfdm = data.size
            recv_counts = gather_scalar(np.int32(hjkv__ijfdm), allgather,
                root=root)
            zhzso__lxl = recv_counts.sum()
            shqh__sow = empty_like_type(zhzso__lxl, data)
            tsknr__msdpw = np.empty(1, np.int32)
            if rank == root or allgather:
                tsknr__msdpw = bodo.ir.join.calc_disp(recv_counts)
            c_gatherv(data.ctypes, np.int32(hjkv__ijfdm), shqh__sow.ctypes,
                recv_counts.ctypes, tsknr__msdpw.ctypes, np.int32(typ_val),
                allgather, np.int32(root))
            return shqh__sow.reshape((-1,) + data.shape[1:])
        return gatherv_impl
    if data == string_array_type:

        def gatherv_str_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            shqh__sow = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.str_arr_ext.init_str_arr(shqh__sow)
        return gatherv_str_arr_impl
    if data == binary_array_type:

        def gatherv_binary_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            shqh__sow = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(shqh__sow)
        return gatherv_binary_arr_impl
    if data == datetime_timedelta_array_type:
        typ_val = numba_to_c_type(types.int64)
        orh__hirro = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            hjkv__ijfdm = len(data)
            lviwl__wnsdp = hjkv__ijfdm + 7 >> 3
            recv_counts = gather_scalar(np.int32(hjkv__ijfdm), allgather,
                root=root)
            zhzso__lxl = recv_counts.sum()
            shqh__sow = empty_like_type(zhzso__lxl, data)
            tsknr__msdpw = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            sqc__jor = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                tsknr__msdpw = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                sqc__jor = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._days_data.ctypes, np.int32(hjkv__ijfdm),
                shqh__sow._days_data.ctypes, recv_counts.ctypes,
                tsknr__msdpw.ctypes, np.int32(typ_val), allgather, np.int32
                (root))
            c_gatherv(data._seconds_data.ctypes, np.int32(hjkv__ijfdm),
                shqh__sow._seconds_data.ctypes, recv_counts.ctypes,
                tsknr__msdpw.ctypes, np.int32(typ_val), allgather, np.int32
                (root))
            c_gatherv(data._microseconds_data.ctypes, np.int32(hjkv__ijfdm),
                shqh__sow._microseconds_data.ctypes, recv_counts.ctypes,
                tsknr__msdpw.ctypes, np.int32(typ_val), allgather, np.int32
                (root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(lviwl__wnsdp),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, sqc__jor.
                ctypes, orh__hirro, allgather, np.int32(root))
            copy_gathered_null_bytes(shqh__sow._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return shqh__sow
        return gatherv_impl_int_arr
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        typ_val = numba_to_c_type(data.dtype)
        orh__hirro = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            hjkv__ijfdm = len(data)
            lviwl__wnsdp = hjkv__ijfdm + 7 >> 3
            recv_counts = gather_scalar(np.int32(hjkv__ijfdm), allgather,
                root=root)
            zhzso__lxl = recv_counts.sum()
            shqh__sow = empty_like_type(zhzso__lxl, data)
            tsknr__msdpw = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            sqc__jor = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                tsknr__msdpw = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                sqc__jor = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._data.ctypes, np.int32(hjkv__ijfdm), shqh__sow.
                _data.ctypes, recv_counts.ctypes, tsknr__msdpw.ctypes, np.
                int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(lviwl__wnsdp),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, sqc__jor.
                ctypes, orh__hirro, allgather, np.int32(root))
            copy_gathered_null_bytes(shqh__sow._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return shqh__sow
        return gatherv_impl_int_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, allgather=False, warn_if_rep=True, root
            =MPI_ROOT):
            oulkn__xeo = bodo.gatherv(data._left, allgather, warn_if_rep, root)
            meb__sjxm = bodo.gatherv(data._right, allgather, warn_if_rep, root)
            return bodo.libs.interval_arr_ext.init_interval_array(oulkn__xeo,
                meb__sjxm)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            uri__cnm = bodo.hiframes.pd_series_ext.get_series_name(data)
            out_arr = bodo.libs.distributed_api.gatherv(arr, allgather,
                warn_if_rep, root)
            rso__mqbf = bodo.gatherv(index, allgather, warn_if_rep, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rso__mqbf, uri__cnm)
        return impl
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):
        qlp__ozbl = np.iinfo(np.int64).max
        vbg__tmvxu = np.iinfo(np.int64).min

        def impl_range_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            start = data._start
            stop = data._stop
            if len(data) == 0:
                start = qlp__ozbl
                stop = vbg__tmvxu
            start = bodo.libs.distributed_api.dist_reduce(start, np.int32(
                Reduce_Type.Min.value))
            stop = bodo.libs.distributed_api.dist_reduce(stop, np.int32(
                Reduce_Type.Max.value))
            total_len = bodo.libs.distributed_api.dist_reduce(len(data), np
                .int32(Reduce_Type.Sum.value))
            if start == qlp__ozbl and stop == vbg__tmvxu:
                start = 0
                stop = 0
            aehx__buqxv = max(0, -(-(stop - start) // data._step))
            if aehx__buqxv < total_len:
                stop = start + data._step * total_len
            if bodo.get_rank() != root and not allgather:
                start = 0
                stop = 0
            return bodo.hiframes.pd_index_ext.init_range_index(start, stop,
                data._step, data._name)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):
        from bodo.hiframes.pd_index_ext import PeriodIndexType
        if isinstance(data, PeriodIndexType):
            jpkkl__lcw = data.freq

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.hiframes.pd_index_ext.init_period_index(arr,
                    data._name, jpkkl__lcw)
        else:

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.utils.conversion.index_from_array(arr, data._name)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            shqh__sow = bodo.gatherv(data._data, allgather, root=root)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(shqh__sow,
                data._names, data._name)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        rzwqk__thwwu = len(data.columns)
        if rzwqk__thwwu == 0:
            return (lambda data, allgather=False, warn_if_rep=True, root=
                MPI_ROOT: bodo.hiframes.pd_dataframe_ext.init_dataframe((),
                bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data), ()))
        eeq__lrqez = ', '.join(f'g_data_{i}' for i in range(rzwqk__thwwu))
        wzyl__gatv = bodo.utils.transform.gen_const_tup(data.columns)
        laee__nljh = (
            'def impl_df(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        for i in range(rzwqk__thwwu):
            laee__nljh += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            laee__nljh += (
                '  g_data_{} = bodo.gatherv(data_{}, allgather, warn_if_rep, root)\n'
                .format(i, i))
        laee__nljh += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        laee__nljh += (
            '  g_index = bodo.gatherv(index, allgather, warn_if_rep, root)\n')
        laee__nljh += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})
"""
            .format(eeq__lrqez, wzyl__gatv))
        mysn__otrqi = {}
        exec(laee__nljh, {'bodo': bodo}, mysn__otrqi)
        tbex__zep = mysn__otrqi['impl_df']
        return tbex__zep
    if isinstance(data, ArrayItemArrayType):
        eclj__fqw = np.int32(numba_to_c_type(types.int32))
        orh__hirro = np.int32(numba_to_c_type(types.uint8))

        def gatherv_array_item_arr_impl(data, allgather=False, warn_if_rep=
            True, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            oah__ipoe = bodo.libs.array_item_arr_ext.get_offsets(data)
            thm__qnq = bodo.libs.array_item_arr_ext.get_data(data)
            myoyq__fyyww = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            hjkv__ijfdm = len(data)
            lnovb__xjeri = np.empty(hjkv__ijfdm, np.uint32)
            lviwl__wnsdp = hjkv__ijfdm + 7 >> 3
            for i in range(hjkv__ijfdm):
                lnovb__xjeri[i] = oah__ipoe[i + 1] - oah__ipoe[i]
            recv_counts = gather_scalar(np.int32(hjkv__ijfdm), allgather,
                root=root)
            zhzso__lxl = recv_counts.sum()
            tsknr__msdpw = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            sqc__jor = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                tsknr__msdpw = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for tjkuw__lmr in range(len(recv_counts)):
                    recv_counts_nulls[tjkuw__lmr] = recv_counts[tjkuw__lmr
                        ] + 7 >> 3
                sqc__jor = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            yyd__yiqgy = np.empty(zhzso__lxl + 1, np.uint32)
            jkijn__llbfv = bodo.gatherv(thm__qnq, allgather, warn_if_rep, root)
            gaq__vwi = np.empty(zhzso__lxl + 7 >> 3, np.uint8)
            c_gatherv(lnovb__xjeri.ctypes, np.int32(hjkv__ijfdm),
                yyd__yiqgy.ctypes, recv_counts.ctypes, tsknr__msdpw.ctypes,
                eclj__fqw, allgather, np.int32(root))
            c_gatherv(myoyq__fyyww.ctypes, np.int32(lviwl__wnsdp),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, sqc__jor.
                ctypes, orh__hirro, allgather, np.int32(root))
            dummy_use(data)
            lmkl__muww = np.empty(zhzso__lxl + 1, np.uint64)
            convert_len_arr_to_offset(yyd__yiqgy.ctypes, lmkl__muww.ctypes,
                zhzso__lxl)
            copy_gathered_null_bytes(gaq__vwi.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                zhzso__lxl, jkijn__llbfv, lmkl__muww, gaq__vwi)
            return out_arr
        return gatherv_array_item_arr_impl
    if isinstance(data, StructArrayType):
        oau__ezaro = data.names
        orh__hirro = np.int32(numba_to_c_type(types.uint8))

        def impl_struct_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            kkt__pcb = bodo.libs.struct_arr_ext.get_data(data)
            irqx__rsllj = bodo.libs.struct_arr_ext.get_null_bitmap(data)
            cyyi__clxp = bodo.gatherv(kkt__pcb, allgather=allgather, root=root)
            rank = bodo.libs.distributed_api.get_rank()
            hjkv__ijfdm = len(data)
            lviwl__wnsdp = hjkv__ijfdm + 7 >> 3
            recv_counts = gather_scalar(np.int32(hjkv__ijfdm), allgather,
                root=root)
            zhzso__lxl = recv_counts.sum()
            crks__irz = np.empty(zhzso__lxl + 7 >> 3, np.uint8)
            recv_counts_nulls = np.empty(1, np.int32)
            sqc__jor = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                sqc__jor = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(irqx__rsllj.ctypes, np.int32(lviwl__wnsdp),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, sqc__jor.
                ctypes, orh__hirro, allgather, np.int32(root))
            copy_gathered_null_bytes(crks__irz.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            return bodo.libs.struct_arr_ext.init_struct_arr(cyyi__clxp,
                crks__irz, oau__ezaro)
        return impl_struct_arr
    if data == binary_array_type:

        def impl_bin_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            shqh__sow = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(shqh__sow)
        return impl_bin_arr
    if isinstance(data, TupleArrayType):

        def impl_tuple_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            shqh__sow = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.tuple_arr_ext.init_tuple_arr(shqh__sow)
        return impl_tuple_arr
    if isinstance(data, MapArrayType):

        def impl_map_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            shqh__sow = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.map_arr_ext.init_map_arr(shqh__sow)
        return impl_map_arr
    if isinstance(data, CSRMatrixType):

        def impl_csr_matrix(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            shqh__sow = bodo.gatherv(data.data, allgather, warn_if_rep, root)
            zpqn__pkz = bodo.gatherv(data.indices, allgather, warn_if_rep, root
                )
            gxdf__urnnt = bodo.gatherv(data.indptr, allgather, warn_if_rep,
                root)
            irum__ffrq = gather_scalar(data.shape[0], allgather, root=root)
            amo__rzbyw = irum__ffrq.sum()
            rzwqk__thwwu = bodo.libs.distributed_api.dist_reduce(data.shape
                [1], np.int32(Reduce_Type.Max.value))
            gwjt__rni = np.empty(amo__rzbyw + 1, np.int64)
            zpqn__pkz = zpqn__pkz.astype(np.int64)
            gwjt__rni[0] = 0
            cqb__lope = 1
            glhjg__gbgue = 0
            for srv__imzvq in irum__ffrq:
                for lsdla__yif in range(srv__imzvq):
                    xuldc__pafm = gxdf__urnnt[glhjg__gbgue + 1] - gxdf__urnnt[
                        glhjg__gbgue]
                    gwjt__rni[cqb__lope] = gwjt__rni[cqb__lope - 1
                        ] + xuldc__pafm
                    cqb__lope += 1
                    glhjg__gbgue += 1
                glhjg__gbgue += 1
            return bodo.libs.csr_matrix_ext.init_csr_matrix(shqh__sow,
                zpqn__pkz, gwjt__rni, (amo__rzbyw, rzwqk__thwwu))
        return impl_csr_matrix
    if isinstance(data, types.BaseTuple):
        laee__nljh = (
            'def impl_tuple(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        laee__nljh += '  return ({}{})\n'.format(', '.join(
            'bodo.gatherv(data[{}], allgather, warn_if_rep, root)'.format(i
            ) for i in range(len(data))), ',' if len(data) > 0 else '')
        mysn__otrqi = {}
        exec(laee__nljh, {'bodo': bodo}, mysn__otrqi)
        hkca__gwsp = mysn__otrqi['impl_tuple']
        return hkca__gwsp
    if data is types.none:
        return (lambda data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT: None)
    raise BodoError('gatherv() not available for {}'.format(data))


@numba.generated_jit(nopython=True)
def rebalance(data, dests=None, random=False, random_seed=None, parallel=False
    ):
    laee__nljh = (
        'def impl(data, dests=None, random=False, random_seed=None, parallel=False):\n'
        )
    laee__nljh += '    if random:\n'
    laee__nljh += '        if random_seed is None:\n'
    laee__nljh += '            random = 1\n'
    laee__nljh += '        else:\n'
    laee__nljh += '            random = 2\n'
    laee__nljh += '    if random_seed is None:\n'
    laee__nljh += '        random_seed = -1\n'
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        ovicz__aedo = data
        rzwqk__thwwu = len(ovicz__aedo.columns)
        for i in range(rzwqk__thwwu):
            laee__nljh += f"""    data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
        laee__nljh += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data))
"""
        eeq__lrqez = ', '.join(f'data_{i}' for i in range(rzwqk__thwwu))
        laee__nljh += ('    info_list_total = [{}, array_to_info(ind_arr)]\n'
            .format(', '.join('array_to_info(data_{})'.format(hfh__tnjl) for
            hfh__tnjl in range(rzwqk__thwwu))))
        laee__nljh += (
            '    table_total = arr_info_list_to_table(info_list_total)\n')
        laee__nljh += '    if dests is None:\n'
        laee__nljh += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        laee__nljh += '    else:\n'
        laee__nljh += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        for yrzu__ztxb in range(rzwqk__thwwu):
            laee__nljh += (
                """    out_arr_{0} = info_to_array(info_from_table(out_table, {0}), data_{0})
"""
                .format(yrzu__ztxb))
        laee__nljh += (
            """    out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)
"""
            .format(rzwqk__thwwu))
        laee__nljh += '    delete_table(out_table)\n'
        laee__nljh += '    if parallel:\n'
        laee__nljh += '        delete_table(table_total)\n'
        eeq__lrqez = ', '.join('out_arr_{}'.format(i) for i in range(
            rzwqk__thwwu))
        wzyl__gatv = bodo.utils.transform.gen_const_tup(ovicz__aedo.columns)
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        laee__nljh += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), {}, {})\n'
            .format(eeq__lrqez, index, wzyl__gatv))
    elif isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):
        laee__nljh += (
            '    data_0 = bodo.hiframes.pd_series_ext.get_series_data(data)\n')
        laee__nljh += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(data))
"""
        laee__nljh += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(data)\n')
        laee__nljh += """    table_total = arr_info_list_to_table([array_to_info(data_0), array_to_info(ind_arr)])
"""
        laee__nljh += '    if dests is None:\n'
        laee__nljh += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        laee__nljh += '    else:\n'
        laee__nljh += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        laee__nljh += (
            '    out_arr_0 = info_to_array(info_from_table(out_table, 0), data_0)\n'
            )
        laee__nljh += (
            '    out_arr_index = info_to_array(info_from_table(out_table, 1), ind_arr)\n'
            )
        laee__nljh += '    delete_table(out_table)\n'
        laee__nljh += '    if parallel:\n'
        laee__nljh += '        delete_table(table_total)\n'
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        laee__nljh += f"""    return bodo.hiframes.pd_series_ext.init_series(out_arr_0, {index}, name)
"""
    elif isinstance(data, types.Array):
        assert is_overload_false(random
            ), 'Call random_shuffle instead of rebalance'
        laee__nljh += '    if not parallel:\n'
        laee__nljh += '        return data\n'
        laee__nljh += """    dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        laee__nljh += '    if dests is None:\n'
        laee__nljh += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        laee__nljh += '    elif bodo.get_rank() not in dests:\n'
        laee__nljh += '        dim0_local_size = 0\n'
        laee__nljh += '    else:\n'
        laee__nljh += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, len(dests), dests.index(bodo.get_rank()))
"""
        laee__nljh += """    out = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        laee__nljh += """    bodo.libs.distributed_api.dist_oneD_reshape_shuffle(out, data, dim0_global_size, dests)
"""
        laee__nljh += '    return out\n'
    elif bodo.utils.utils.is_array_typ(data, False):
        laee__nljh += (
            '    table_total = arr_info_list_to_table([array_to_info(data)])\n'
            )
        laee__nljh += '    if dests is None:\n'
        laee__nljh += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        laee__nljh += '    else:\n'
        laee__nljh += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        laee__nljh += (
            '    out_arr = info_to_array(info_from_table(out_table, 0), data)\n'
            )
        laee__nljh += '    delete_table(out_table)\n'
        laee__nljh += '    if parallel:\n'
        laee__nljh += '        delete_table(table_total)\n'
        laee__nljh += '    return out_arr\n'
    else:
        raise BodoError(f'Type {data} not supported for bodo.rebalance')
    mysn__otrqi = {}
    exec(laee__nljh, {'np': np, 'bodo': bodo, 'array_to_info': bodo.libs.
        array.array_to_info, 'shuffle_renormalization': bodo.libs.array.
        shuffle_renormalization, 'shuffle_renormalization_group': bodo.libs
        .array.shuffle_renormalization_group, 'arr_info_list_to_table':
        bodo.libs.array.arr_info_list_to_table, 'info_from_table': bodo.
        libs.array.info_from_table, 'info_to_array': bodo.libs.array.
        info_to_array, 'delete_table': bodo.libs.array.delete_table},
        mysn__otrqi)
    impl = mysn__otrqi['impl']
    return impl


@numba.generated_jit(nopython=True)
def random_shuffle(data, seed=None, dests=None, parallel=False):
    laee__nljh = 'def impl(data, seed=None, dests=None, parallel=False):\n'
    if isinstance(data, types.Array):
        if not is_overload_none(dests):
            raise BodoError('not supported')
        laee__nljh += '    if seed is None:\n'
        laee__nljh += """        seed = bodo.libs.distributed_api.bcast_scalar(np.random.randint(0, 2**31))
"""
        laee__nljh += '    np.random.seed(seed)\n'
        laee__nljh += '    if not parallel:\n'
        laee__nljh += '        data = data.copy()\n'
        laee__nljh += '        np.random.shuffle(data)\n'
        laee__nljh += '        return data\n'
        laee__nljh += '    else:\n'
        laee__nljh += """        dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        laee__nljh += '        permutation = np.arange(dim0_global_size)\n'
        laee__nljh += '        np.random.shuffle(permutation)\n'
        laee__nljh += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        laee__nljh += """        output = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        laee__nljh += (
            '        dtype_size = bodo.io.np_io.get_dtype_size(data.dtype)\n')
        laee__nljh += """        bodo.libs.distributed_api.dist_permutation_array_index(output, dim0_global_size, dtype_size, data, permutation, len(permutation))
"""
        laee__nljh += '        return output\n'
    else:
        laee__nljh += """    return bodo.libs.distributed_api.rebalance(data, dests=dests, random=True, random_seed=seed, parallel=parallel)
"""
    mysn__otrqi = {}
    exec(laee__nljh, {'np': np, 'bodo': bodo}, mysn__otrqi)
    impl = mysn__otrqi['impl']
    return impl


@numba.generated_jit(nopython=True)
def allgatherv(data, warn_if_rep=True, root=MPI_ROOT):
    return lambda data, warn_if_rep=True, root=MPI_ROOT: gatherv(data, True,
        warn_if_rep, root)


@numba.njit
def get_scatter_null_bytes_buff(null_bitmap_ptr, sendcounts, sendcounts_nulls):
    if bodo.get_rank() != MPI_ROOT:
        return np.empty(1, np.uint8)
    zvevk__sdoi = np.empty(sendcounts_nulls.sum(), np.uint8)
    uzgs__wwbl = 0
    kuqqv__edh = 0
    for nvdu__eik in range(len(sendcounts)):
        rttb__rmcs = sendcounts[nvdu__eik]
        lviwl__wnsdp = sendcounts_nulls[nvdu__eik]
        zxul__gme = zvevk__sdoi[uzgs__wwbl:uzgs__wwbl + lviwl__wnsdp]
        for hgzlp__tpyjb in range(rttb__rmcs):
            set_bit_to_arr(zxul__gme, hgzlp__tpyjb, get_bit_bitmap(
                null_bitmap_ptr, kuqqv__edh))
            kuqqv__edh += 1
        uzgs__wwbl += lviwl__wnsdp
    return zvevk__sdoi


def _bcast_dtype(data):
    try:
        from mpi4py import MPI
    except:
        raise BodoError('mpi4py is required for scatterv')
    zdno__wpl = MPI.COMM_WORLD
    data = zdno__wpl.bcast(data)
    return data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_scatterv_send_counts(send_counts, n_pes, n):
    if not is_overload_none(send_counts):
        return lambda send_counts, n_pes, n: send_counts

    def impl(send_counts, n_pes, n):
        send_counts = np.empty(n_pes, np.int32)
        for i in range(n_pes):
            send_counts[i] = get_node_portion(n, n_pes, i)
        return send_counts
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _scatterv_np(data, send_counts=None, warn_if_dist=True):
    typ_val = numba_to_c_type(data.dtype)
    ccl__zlmeb = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    uvjce__qgmhy = (0,) * ccl__zlmeb

    def scatterv_arr_impl(data, send_counts=None, warn_if_dist=True):
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        caxeu__sbebh = np.ascontiguousarray(data)
        nun__nzv = data.ctypes
        msf__exj = uvjce__qgmhy
        if rank == MPI_ROOT:
            msf__exj = caxeu__sbebh.shape
        msf__exj = bcast_tuple(msf__exj)
        avdss__ylsju = get_tuple_prod(msf__exj[1:])
        send_counts = _get_scatterv_send_counts(send_counts, n_pes, msf__exj[0]
            )
        send_counts *= avdss__ylsju
        hjkv__ijfdm = send_counts[rank]
        yhiv__izlx = np.empty(hjkv__ijfdm, dtype)
        tsknr__msdpw = bodo.ir.join.calc_disp(send_counts)
        c_scatterv(nun__nzv, send_counts.ctypes, tsknr__msdpw.ctypes,
            yhiv__izlx.ctypes, np.int32(hjkv__ijfdm), np.int32(typ_val))
        return yhiv__izlx.reshape((-1,) + msf__exj[1:])
    return scatterv_arr_impl


def _get_name_value_for_type(name_typ):
    assert isinstance(name_typ, (types.UnicodeType, types.StringLiteral)
        ) or name_typ == types.none
    return None if name_typ == types.none else '_' + str(ir_utils.next_label())


def get_value_for_type(dtype):
    if isinstance(dtype, types.Array):
        return np.zeros((1,) * dtype.ndim, numba.np.numpy_support.as_dtype(
            dtype.dtype))
    if dtype == string_array_type:
        return pd.array(['A'], 'string')
    if dtype == binary_array_type:
        return np.array([b'A'], dtype=object)
    if isinstance(dtype, IntegerArrayType):
        fivf__xhox = '{}Int{}'.format('' if dtype.dtype.signed else 'U',
            dtype.dtype.bitwidth)
        return pd.array([3], fivf__xhox)
    if dtype == boolean_array:
        return pd.array([True], 'boolean')
    if isinstance(dtype, DecimalArrayType):
        return np.array([Decimal('32.1')])
    if dtype == datetime_date_array_type:
        return np.array([datetime.date(2011, 8, 9)])
    if dtype == datetime_timedelta_array_type:
        return np.array([datetime.timedelta(33)])
    if bodo.hiframes.pd_index_ext.is_pd_index_type(dtype):
        uri__cnm = _get_name_value_for_type(dtype.name_typ)
        if isinstance(dtype, bodo.hiframes.pd_index_ext.RangeIndexType):
            return pd.RangeIndex(1, name=uri__cnm)
        zfsy__czog = bodo.utils.typing.get_index_data_arr_types(dtype)[0]
        arr = get_value_for_type(zfsy__czog)
        return pd.Index(arr, name=uri__cnm)
    if isinstance(dtype, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        uri__cnm = _get_name_value_for_type(dtype.name_typ)
        oau__ezaro = tuple(_get_name_value_for_type(t) for t in dtype.names_typ
            )
        czggj__mvwty = tuple(get_value_for_type(t) for t in dtype.array_types)
        val = pd.MultiIndex.from_arrays(czggj__mvwty, names=oau__ezaro)
        val.name = uri__cnm
        return val
    if isinstance(dtype, bodo.hiframes.pd_series_ext.SeriesType):
        uri__cnm = _get_name_value_for_type(dtype.name_typ)
        arr = get_value_for_type(dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.Series(arr, index, name=uri__cnm)
    if isinstance(dtype, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        czggj__mvwty = tuple(get_value_for_type(t) for t in dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.DataFrame({uri__cnm: arr for uri__cnm, arr in zip(dtype.
            columns, czggj__mvwty)}, index)
    if isinstance(dtype, CategoricalArrayType):
        return pd.Categorical.from_codes([0], dtype.dtype.categories)
    if isinstance(dtype, types.BaseTuple):
        return tuple(get_value_for_type(t) for t in dtype.types)
    if isinstance(dtype, ArrayItemArrayType):
        return pd.Series([get_value_for_type(dtype.dtype),
            get_value_for_type(dtype.dtype)]).values
    raise BodoError('get_value_for_type(dtype): Missing data type')


def scatterv(data, send_counts=None, warn_if_dist=True):
    rank = bodo.libs.distributed_api.get_rank()
    if rank != MPI_ROOT and data is not None:
        raise BodoError(
            "bodo.scatterv() requires 'data' argument to be None on all ranks except rank 0."
            )
    dtype = bodo.typeof(data)
    dtype = _bcast_dtype(dtype)
    if rank != MPI_ROOT:
        data = get_value_for_type(dtype)
    return scatterv_impl(data, send_counts)


@overload(scatterv)
def scatterv_overload(data, send_counts=None, warn_if_dist=True):
    return lambda data, send_counts=None, warn_if_dist=True: scatterv_impl(data
        , send_counts)


@numba.generated_jit(nopython=True)
def scatterv_impl(data, send_counts=None, warn_if_dist=True):
    if isinstance(data, types.Array):
        return lambda data, send_counts=None, warn_if_dist=True: _scatterv_np(
            data, send_counts)
    if data in [binary_array_type, string_array_type]:
        eclj__fqw = np.int32(numba_to_c_type(types.int32))
        orh__hirro = np.int32(numba_to_c_type(types.uint8))
        if data == binary_array_type:
            vdwy__avhj = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            vdwy__avhj = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        laee__nljh = f"""def impl(
            data, send_counts=None, warn_if_dist=True
        ):  # pragma: no cover
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            n_all = bodo.libs.distributed_api.bcast_scalar(len(data))

            # convert offsets to lengths of strings
            send_arr_lens = np.empty(
                len(data), np.uint32
            )  # XXX offset type is offset_type, lengths for comm are uint32
            for i in range(len(data)):
                send_arr_lens[i] = bodo.libs.str_arr_ext.get_str_arr_item_length(
                    data, i
                )

            # ------- calculate buffer counts -------

            send_counts = bodo.libs.distributed_api._get_scatterv_send_counts(send_counts, n_pes, n_all)

            # displacements
            displs = bodo.ir.join.calc_disp(send_counts)

            # compute send counts for characters
            send_counts_char = np.empty(n_pes, np.int32)
            if rank == 0:
                curr_str = 0
                for i in range(n_pes):
                    c = 0
                    for _ in range(send_counts[i]):
                        c += send_arr_lens[curr_str]
                        curr_str += 1
                    send_counts_char[i] = c

            bodo.libs.distributed_api.bcast(send_counts_char)

            # displacements for characters
            displs_char = bodo.ir.join.calc_disp(send_counts_char)

            # compute send counts for nulls
            send_counts_nulls = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                send_counts_nulls[i] = (send_counts[i] + 7) >> 3

            # displacements for nulls
            displs_nulls = bodo.ir.join.calc_disp(send_counts_nulls)

            # alloc output array
            n_loc = send_counts[rank]  # total number of elements on this PE
            n_loc_char = send_counts_char[rank]
            recv_arr = {vdwy__avhj}(n_loc, n_loc_char)

            # ----- string lengths -----------

            recv_lens = np.empty(n_loc, np.uint32)
            bodo.libs.distributed_api.c_scatterv(
                send_arr_lens.ctypes,
                send_counts.ctypes,
                displs.ctypes,
                recv_lens.ctypes,
                np.int32(n_loc),
                int32_typ_enum,
            )

            # TODO: don't hardcode offset type. Also, if offset is 32 bit we can
            # use the same buffer
            bodo.libs.str_arr_ext.convert_len_arr_to_offset(recv_lens.ctypes, bodo.libs.str_arr_ext.get_offset_ptr(recv_arr), n_loc)

            # ----- string characters -----------

            bodo.libs.distributed_api.c_scatterv(
                bodo.libs.str_arr_ext.get_data_ptr(data),
                send_counts_char.ctypes,
                displs_char.ctypes,
                bodo.libs.str_arr_ext.get_data_ptr(recv_arr),
                np.int32(n_loc_char),
                char_typ_enum,
            )

            # ----------- null bitmap -------------

            n_recv_bytes = (n_loc + 7) >> 3

            send_null_bitmap = bodo.libs.distributed_api.get_scatter_null_bytes_buff(
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(data), send_counts, send_counts_nulls
            )

            bodo.libs.distributed_api.c_scatterv(
                send_null_bitmap.ctypes,
                send_counts_nulls.ctypes,
                displs_nulls.ctypes,
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(recv_arr),
                np.int32(n_recv_bytes),
                char_typ_enum,
            )

            return recv_arr"""
        mysn__otrqi = dict()
        exec(laee__nljh, {'bodo': bodo, 'np': np, 'int32_typ_enum':
            eclj__fqw, 'char_typ_enum': orh__hirro}, mysn__otrqi)
        impl = mysn__otrqi['impl']
        return impl
    if isinstance(data, ArrayItemArrayType):
        eclj__fqw = np.int32(numba_to_c_type(types.int32))
        orh__hirro = np.int32(numba_to_c_type(types.uint8))

        def scatterv_array_item_impl(data, send_counts=None, warn_if_dist=True
            ):
            pxpy__fcg = bodo.libs.array_item_arr_ext.get_offsets(data)
            sgwzs__skbxx = bodo.libs.array_item_arr_ext.get_data(data)
            zgzgt__upvst = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            kpouu__nbrxj = bcast_scalar(len(data))
            znyq__oiwof = np.empty(len(data), np.uint32)
            for i in range(len(data)):
                znyq__oiwof[i] = pxpy__fcg[i + 1] - pxpy__fcg[i]
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                kpouu__nbrxj)
            tsknr__msdpw = bodo.ir.join.calc_disp(send_counts)
            yyea__xrwe = np.empty(n_pes, np.int32)
            if rank == 0:
                zgr__mqix = 0
                for i in range(n_pes):
                    uzbef__ocgmf = 0
                    for lsdla__yif in range(send_counts[i]):
                        uzbef__ocgmf += znyq__oiwof[zgr__mqix]
                        zgr__mqix += 1
                    yyea__xrwe[i] = uzbef__ocgmf
            bcast(yyea__xrwe)
            wwcjm__wwvyz = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                wwcjm__wwvyz[i] = send_counts[i] + 7 >> 3
            sqc__jor = bodo.ir.join.calc_disp(wwcjm__wwvyz)
            hjkv__ijfdm = send_counts[rank]
            bbu__ano = np.empty(hjkv__ijfdm + 1, np_offset_type)
            vvwc__xbrm = bodo.libs.distributed_api.scatterv_impl(sgwzs__skbxx,
                yyea__xrwe)
            gok__wup = hjkv__ijfdm + 7 >> 3
            fgzk__hiey = np.empty(gok__wup, np.uint8)
            ulzd__xvrae = np.empty(hjkv__ijfdm, np.uint32)
            c_scatterv(znyq__oiwof.ctypes, send_counts.ctypes, tsknr__msdpw
                .ctypes, ulzd__xvrae.ctypes, np.int32(hjkv__ijfdm), eclj__fqw)
            convert_len_arr_to_offset(ulzd__xvrae.ctypes, bbu__ano.ctypes,
                hjkv__ijfdm)
            muqk__vmkd = get_scatter_null_bytes_buff(zgzgt__upvst.ctypes,
                send_counts, wwcjm__wwvyz)
            c_scatterv(muqk__vmkd.ctypes, wwcjm__wwvyz.ctypes, sqc__jor.
                ctypes, fgzk__hiey.ctypes, np.int32(gok__wup), orh__hirro)
            return bodo.libs.array_item_arr_ext.init_array_item_array(
                hjkv__ijfdm, vvwc__xbrm, bbu__ano, fgzk__hiey)
        return scatterv_array_item_impl
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        orh__hirro = np.int32(numba_to_c_type(types.uint8))
        if isinstance(data, IntegerArrayType):
            uovem__urxon = bodo.libs.int_arr_ext.init_integer_array
        if isinstance(data, DecimalArrayType):
            precision = data.precision
            scale = data.scale
            uovem__urxon = numba.njit(no_cpython_wrapper=True)(lambda d, b:
                bodo.libs.decimal_arr_ext.init_decimal_array(d, b,
                precision, scale))
        if data == boolean_array:
            uovem__urxon = bodo.libs.bool_arr_ext.init_bool_array
        if data == datetime_date_array_type:
            uovem__urxon = (bodo.hiframes.datetime_date_ext.
                init_datetime_date_array)

        def scatterv_impl_int_arr(data, send_counts=None, warn_if_dist=True):
            n_pes = bodo.libs.distributed_api.get_size()
            caxeu__sbebh = data._data
            irqx__rsllj = data._null_bitmap
            wbots__lnzz = len(caxeu__sbebh)
            judzc__igjdv = _scatterv_np(caxeu__sbebh, send_counts)
            kpouu__nbrxj = bcast_scalar(wbots__lnzz)
            qqk__rmn = len(judzc__igjdv) + 7 >> 3
            aswo__lwi = np.empty(qqk__rmn, np.uint8)
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                kpouu__nbrxj)
            wwcjm__wwvyz = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                wwcjm__wwvyz[i] = send_counts[i] + 7 >> 3
            sqc__jor = bodo.ir.join.calc_disp(wwcjm__wwvyz)
            muqk__vmkd = get_scatter_null_bytes_buff(irqx__rsllj.ctypes,
                send_counts, wwcjm__wwvyz)
            c_scatterv(muqk__vmkd.ctypes, wwcjm__wwvyz.ctypes, sqc__jor.
                ctypes, aswo__lwi.ctypes, np.int32(qqk__rmn), orh__hirro)
            return uovem__urxon(judzc__igjdv, aswo__lwi)
        return scatterv_impl_int_arr
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, send_counts=None, warn_if_dist=True):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            start = data._start
            stop = data._stop
            qjjwh__ogqwo = data._step
            uri__cnm = data._name
            uri__cnm = bcast_scalar(uri__cnm)
            start = bcast_scalar(start)
            stop = bcast_scalar(stop)
            qjjwh__ogqwo = bcast_scalar(qjjwh__ogqwo)
            yafj__wpbje = bodo.libs.array_kernels.calc_nitems(start, stop,
                qjjwh__ogqwo)
            chunk_start = bodo.libs.distributed_api.get_start(yafj__wpbje,
                n_pes, rank)
            chunk_count = bodo.libs.distributed_api.get_node_portion(
                yafj__wpbje, n_pes, rank)
            tyro__abu = start + qjjwh__ogqwo * chunk_start
            trb__lufq = start + qjjwh__ogqwo * (chunk_start + chunk_count)
            trb__lufq = min(trb__lufq, stop)
            return bodo.hiframes.pd_index_ext.init_range_index(tyro__abu,
                trb__lufq, qjjwh__ogqwo, uri__cnm)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, send_counts=None, warn_if_dist=True):
            caxeu__sbebh = data._data
            uri__cnm = data._name
            uri__cnm = bcast_scalar(uri__cnm)
            arr = bodo.libs.distributed_api.scatterv_impl(caxeu__sbebh,
                send_counts)
            return bodo.utils.conversion.index_from_array(arr, uri__cnm)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, send_counts=None, warn_if_dist=True):
            shqh__sow = bodo.libs.distributed_api.scatterv_impl(data._data,
                send_counts)
            uri__cnm = bcast_scalar(data._name)
            oau__ezaro = bcast_tuple(data._names)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(shqh__sow,
                oau__ezaro, uri__cnm)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, send_counts=None, warn_if_dist=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            uri__cnm = bodo.hiframes.pd_series_ext.get_series_name(data)
            obbo__vynj = bcast_scalar(uri__cnm)
            out_arr = bodo.libs.distributed_api.scatterv_impl(arr, send_counts)
            rso__mqbf = bodo.libs.distributed_api.scatterv_impl(index,
                send_counts)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rso__mqbf, obbo__vynj)
        return impl_series
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        rzwqk__thwwu = len(data.columns)
        eeq__lrqez = ', '.join('g_data_{}'.format(i) for i in range(
            rzwqk__thwwu))
        wzyl__gatv = bodo.utils.transform.gen_const_tup(data.columns)
        laee__nljh = (
            'def impl_df(data, send_counts=None, warn_if_dist=True):\n')
        for i in range(rzwqk__thwwu):
            laee__nljh += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            laee__nljh += (
                """  g_data_{} = bodo.libs.distributed_api.scatterv_impl(data_{}, send_counts)
"""
                .format(i, i))
        laee__nljh += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        laee__nljh += (
            '  g_index = bodo.libs.distributed_api.scatterv_impl(index, send_counts)\n'
            )
        laee__nljh += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})
"""
            .format(eeq__lrqez, wzyl__gatv))
        mysn__otrqi = {}
        exec(laee__nljh, {'bodo': bodo}, mysn__otrqi)
        tbex__zep = mysn__otrqi['impl_df']
        return tbex__zep
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, send_counts=None, warn_if_dist=True):
            tthd__glwtr = bodo.libs.distributed_api.scatterv_impl(data.
                codes, send_counts)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                tthd__glwtr, data.dtype)
        return impl_cat
    if isinstance(data, types.BaseTuple):
        laee__nljh = (
            'def impl_tuple(data, send_counts=None, warn_if_dist=True):\n')
        laee__nljh += '  return ({}{})\n'.format(', '.join(
            'bodo.libs.distributed_api.scatterv_impl(data[{}], send_counts)'
            .format(i) for i in range(len(data))), ',' if len(data) > 0 else ''
            )
        mysn__otrqi = {}
        exec(laee__nljh, {'bodo': bodo}, mysn__otrqi)
        hkca__gwsp = mysn__otrqi['impl_tuple']
        return hkca__gwsp
    if data is types.none:
        return lambda data, send_counts=None, warn_if_dist=True: None
    raise BodoError('scatterv() not available for {}'.format(data))


@intrinsic
def cptr_to_voidptr(typingctx, cptr_tp=None):

    def codegen(context, builder, sig, args):
        return builder.bitcast(args[0], lir.IntType(8).as_pointer())
    return types.voidptr(cptr_tp), codegen


def bcast(data):
    return


@overload(bcast, no_unliteral=True)
def bcast_overload(data):
    if isinstance(data, types.Array):

        def bcast_impl(data):
            typ_enum = get_type_enum(data)
            count = data.size
            assert count < INT_MAX
            c_bcast(data.ctypes, np.int32(count), typ_enum, np.array([-1]).
                ctypes, 0)
            return
        return bcast_impl
    if isinstance(data, DecimalArrayType):

        def bcast_decimal_arr(data):
            count = data._data.size
            assert count < INT_MAX
            c_bcast(data._data.ctypes, np.int32(count), CTypeEnum.Int128.
                value, np.array([-1]).ctypes, 0)
            bcast(data._null_bitmap)
            return
        return bcast_decimal_arr
    if isinstance(data, IntegerArrayType) or data in (boolean_array,
        datetime_date_array_type):

        def bcast_impl_int_arr(data):
            bcast(data._data)
            bcast(data._null_bitmap)
            return
        return bcast_impl_int_arr
    if data in [binary_array_type, string_array_type]:
        ijv__rdl = np.int32(numba_to_c_type(offset_type))
        orh__hirro = np.int32(numba_to_c_type(types.uint8))

        def bcast_str_impl(data):
            hjkv__ijfdm = len(data)
            ihru__wxhf = num_total_chars(data)
            assert hjkv__ijfdm < INT_MAX
            assert ihru__wxhf < INT_MAX
            cdbq__blrg = get_offset_ptr(data)
            nun__nzv = get_data_ptr(data)
            null_bitmap_ptr = get_null_bitmap_ptr(data)
            lviwl__wnsdp = hjkv__ijfdm + 7 >> 3
            c_bcast(cdbq__blrg, np.int32(hjkv__ijfdm + 1), ijv__rdl, np.
                array([-1]).ctypes, 0)
            c_bcast(nun__nzv, np.int32(ihru__wxhf), orh__hirro, np.array([-
                1]).ctypes, 0)
            c_bcast(null_bitmap_ptr, np.int32(lviwl__wnsdp), orh__hirro, np
                .array([-1]).ctypes, 0)
        return bcast_str_impl


c_bcast = types.ExternalFunction('c_bcast', types.void(types.voidptr, types
    .int32, types.int32, types.voidptr, types.int32))


def bcast_scalar(val):
    return val


@overload(bcast_scalar, no_unliteral=True)
def bcast_scalar_overload(val):
    val = types.unliteral(val)
    assert isinstance(val, (types.Integer, types.Float)) or val in [bodo.
        datetime64ns, bodo.timedelta64ns, bodo.string_type, types.none,
        types.bool_]
    if val == types.none:
        return lambda val: None
    if val == bodo.string_type:
        orh__hirro = np.int32(numba_to_c_type(types.uint8))

        def impl_str(val):
            rank = bodo.libs.distributed_api.get_rank()
            if rank != MPI_ROOT:
                ybq__lqm = 0
                rhmh__jzux = np.empty(0, np.uint8).ctypes
            else:
                rhmh__jzux, ybq__lqm = (bodo.libs.str_ext.
                    unicode_to_utf8_and_len(val))
            ybq__lqm = bodo.libs.distributed_api.bcast_scalar(ybq__lqm)
            if rank != MPI_ROOT:
                pbfs__dwr = np.empty(ybq__lqm + 1, np.uint8)
                pbfs__dwr[ybq__lqm] = 0
                rhmh__jzux = pbfs__dwr.ctypes
            c_bcast(rhmh__jzux, np.int32(ybq__lqm), orh__hirro, np.array([-
                1]).ctypes, 0)
            return bodo.libs.str_arr_ext.decode_utf8(rhmh__jzux, ybq__lqm)
        return impl_str
    typ_val = numba_to_c_type(val)
    laee__nljh = (
        """def bcast_scalar_impl(val):
  send = np.empty(1, dtype)
  send[0] = val
  c_bcast(send.ctypes, np.int32(1), np.int32({}), np.array([-1]).ctypes, 0)
  return send[0]
"""
        .format(typ_val))
    dtype = numba.np.numpy_support.as_dtype(val)
    mysn__otrqi = {}
    exec(laee__nljh, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast, 'dtype':
        dtype}, mysn__otrqi)
    prn__qysuk = mysn__otrqi['bcast_scalar_impl']
    return prn__qysuk


def bcast_tuple(val):
    return val


@overload(bcast_tuple, no_unliteral=True)
def overload_bcast_tuple(val):
    assert isinstance(val, types.BaseTuple)
    zro__eeth = len(val)
    laee__nljh = 'def bcast_tuple_impl(val):\n'
    laee__nljh += '  return ({}{})'.format(','.join('bcast_scalar(val[{}])'
        .format(i) for i in range(zro__eeth)), ',' if zro__eeth else '')
    mysn__otrqi = {}
    exec(laee__nljh, {'bcast_scalar': bcast_scalar}, mysn__otrqi)
    mznj__ridg = mysn__otrqi['bcast_tuple_impl']
    return mznj__ridg


def prealloc_str_for_bcast(arr):
    return arr


@overload(prealloc_str_for_bcast, no_unliteral=True)
def prealloc_str_for_bcast_overload(arr):
    if arr == string_array_type:

        def prealloc_impl(arr):
            rank = bodo.libs.distributed_api.get_rank()
            hjkv__ijfdm = bcast_scalar(len(arr))
            zisbd__jrvkg = bcast_scalar(np.int64(num_total_chars(arr)))
            if rank != MPI_ROOT:
                arr = pre_alloc_string_array(hjkv__ijfdm, zisbd__jrvkg)
            return arr
        return prealloc_impl
    return lambda arr: arr


def get_local_slice(idx, arr_start, total_len):
    return idx


@overload(get_local_slice, no_unliteral=True, jit_options={'cache': True,
    'no_cpython_wrapper': True})
def get_local_slice_overload(idx, arr_start, total_len):

    def impl(idx, arr_start, total_len):
        slice_index = numba.cpython.unicode._normalize_slice(idx, total_len)
        start = slice_index.start
        qjjwh__ogqwo = slice_index.step
        vnim__gwwq = 0 if qjjwh__ogqwo == 1 or start > arr_start else abs(
            qjjwh__ogqwo - arr_start % qjjwh__ogqwo) % qjjwh__ogqwo
        tyro__abu = max(arr_start, slice_index.start) - arr_start + vnim__gwwq
        trb__lufq = max(slice_index.stop - arr_start, 0)
        return slice(tyro__abu, trb__lufq, qjjwh__ogqwo)
    return impl


def slice_getitem(arr, slice_index, arr_start, total_len):
    return arr[slice_index]


@overload(slice_getitem, no_unliteral=True, jit_options={'cache': True})
def slice_getitem_overload(arr, slice_index, arr_start, total_len):

    def getitem_impl(arr, slice_index, arr_start, total_len):
        qgrv__pcyw = get_local_slice(slice_index, arr_start, total_len)
        return bodo.utils.conversion.ensure_contig_if_np(arr[qgrv__pcyw])
    return getitem_impl


def slice_getitem_from_start(arr, slice_index):
    return arr[slice_index]


@overload(slice_getitem_from_start, no_unliteral=True)
def slice_getitem_from_start_overload(arr, slice_index):
    if arr == bodo.hiframes.datetime_date_ext.datetime_date_array_type:

        def getitem_datetime_date_impl(arr, slice_index):
            rank = bodo.libs.distributed_api.get_rank()
            tjkuw__lmr = slice_index.stop
            A = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
                tjkuw__lmr)
            if rank == 0:
                A = arr[:tjkuw__lmr]
            bodo.libs.distributed_api.bcast(A)
            return A
        return getitem_datetime_date_impl
    if (arr == bodo.hiframes.datetime_timedelta_ext.
        datetime_timedelta_array_type):

        def getitem_datetime_timedelta_impl(arr, slice_index):
            rank = bodo.libs.distributed_api.get_rank()
            tjkuw__lmr = slice_index.stop
            A = (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(tjkuw__lmr))
            if rank == 0:
                A = arr[:tjkuw__lmr]
            bodo.libs.distributed_api.bcast(A)
            return A
        return getitem_datetime_timedelta_impl
    if isinstance(arr.dtype, Decimal128Type):
        precision = arr.dtype.precision
        scale = arr.dtype.scale

        def getitem_decimal_impl(arr, slice_index):
            rank = bodo.libs.distributed_api.get_rank()
            tjkuw__lmr = slice_index.stop
            A = bodo.libs.decimal_arr_ext.alloc_decimal_array(tjkuw__lmr,
                precision, scale)
            if rank == 0:
                for i in range(tjkuw__lmr):
                    A._data[i] = arr._data[i]
                    mucgv__xbrmz = bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, i,
                        mucgv__xbrmz)
            bodo.libs.distributed_api.bcast(A)
            return A
        return getitem_decimal_impl
    if arr == string_array_type:

        def getitem_str_impl(arr, slice_index):
            rank = bodo.libs.distributed_api.get_rank()
            tjkuw__lmr = slice_index.stop
            jypuo__gagy = np.uint64(0)
            if rank == 0:
                out_arr = arr[:tjkuw__lmr]
                jypuo__gagy = num_total_chars(out_arr)
            jypuo__gagy = bcast_scalar(jypuo__gagy)
            if rank != 0:
                out_arr = pre_alloc_string_array(tjkuw__lmr, jypuo__gagy)
            bodo.libs.distributed_api.bcast(out_arr)
            return out_arr
        return getitem_str_impl
    zfsy__czog = arr

    def getitem_impl(arr, slice_index):
        rank = bodo.libs.distributed_api.get_rank()
        tjkuw__lmr = slice_index.stop
        out_arr = bodo.utils.utils.alloc_type(tuple_to_scalar((tjkuw__lmr,) +
            arr.shape[1:]), zfsy__czog)
        if rank == 0:
            out_arr = arr[:tjkuw__lmr]
        bodo.libs.distributed_api.bcast(out_arr)
        return out_arr
    return getitem_impl


dummy_use = numba.njit(lambda a: None)


def int_getitem(arr, ind, arr_start, total_len, is_1D):
    return arr[ind]


def transform_str_getitem_output(data, length):
    pass


@overload(transform_str_getitem_output)
def overload_transform_str_getitem_output(data, length):
    if data == bodo.string_type:
        return lambda data, length: bodo.libs.str_arr_ext.decode_utf8(data.
            _data, length)
    if data == types.Array(types.uint8, 1, 'C'):
        return lambda data, length: bodo.libs.binary_arr_ext.init_bytes_type(
            data, length)
    raise BodoError(
        f'Internal Error: Expected String or Uint8 Array, found {data}')


@overload(int_getitem, no_unliteral=True)
def int_getitem_overload(arr, ind, arr_start, total_len, is_1D):
    if arr in [bodo.binary_array_type, string_array_type]:
        ideno__bcbvr = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND
        orh__hirro = np.int32(numba_to_c_type(types.uint8))
        rnd__buyj = arr.dtype

        def str_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            vvh__lybot = np.int32(10)
            tag = np.int32(11)
            bck__igrv = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                ind = ind - arr_start
                thm__qnq = arr._data
                ltjb__emw = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    thm__qnq, ind)
                ctq__lgxwd = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    thm__qnq, ind + 1)
                length = ctq__lgxwd - ltjb__emw
                nvsx__lpdtz = thm__qnq[ind]
                bck__igrv[0] = length
                isend(bck__igrv, np.int32(1), root, vvh__lybot, True)
                isend(nvsx__lpdtz, np.int32(length), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(rnd__buyj,
                ideno__bcbvr, 0, 1)
            aehx__buqxv = 0
            if rank == root:
                aehx__buqxv = recv(np.int64, ANY_SOURCE, vvh__lybot)
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    rnd__buyj, ideno__bcbvr, aehx__buqxv, 1)
                nun__nzv = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
                _recv(nun__nzv, np.int32(aehx__buqxv), orh__hirro,
                    ANY_SOURCE, tag)
            dummy_use(bck__igrv)
            aehx__buqxv = bcast_scalar(aehx__buqxv)
            if rank != root:
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    rnd__buyj, ideno__bcbvr, aehx__buqxv, 1)
            nun__nzv = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
            c_bcast(nun__nzv, np.int32(aehx__buqxv), orh__hirro, np.array([
                -1]).ctypes, 0)
            val = transform_str_getitem_output(val, aehx__buqxv)
            return val
        return str_getitem_impl
    if isinstance(arr, bodo.CategoricalArrayType):
        kem__tpacb = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def cat_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, kem__tpacb)
            if arr_start <= ind < arr_start + len(arr):
                tthd__glwtr = (bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(arr))
                data = tthd__glwtr[ind - arr_start]
                send_arr = np.full(1, data, kem__tpacb)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = kem__tpacb(-1)
            if rank == root:
                val = recv(kem__tpacb, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            uicaa__lpr = arr.dtype.categories[max(val, 0)]
            return uicaa__lpr
        return cat_getitem_impl
    bao__wqnh = arr.dtype

    def getitem_impl(arr, ind, arr_start, total_len, is_1D):
        if ind >= total_len:
            raise IndexError('index out of bounds')
        ind = ind % total_len
        root = np.int32(0)
        tag = np.int32(11)
        send_arr = np.zeros(1, bao__wqnh)
        if arr_start <= ind < arr_start + len(arr):
            data = arr[ind - arr_start]
            send_arr = np.full(1, data)
            isend(send_arr, np.int32(1), root, tag, True)
        rank = bodo.libs.distributed_api.get_rank()
        val = np.zeros(1, bao__wqnh)[0]
        if rank == root:
            val = recv(bao__wqnh, ANY_SOURCE, tag)
        dummy_use(send_arr)
        val = bcast_scalar(val)
        return val
    return getitem_impl


c_alltoallv = types.ExternalFunction('c_alltoallv', types.void(types.
    voidptr, types.voidptr, types.voidptr, types.voidptr, types.voidptr,
    types.voidptr, types.int32))


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def alltoallv(send_data, out_data, send_counts, recv_counts, send_disp,
    recv_disp):
    typ_enum = get_type_enum(send_data)
    bdng__mimzy = get_type_enum(out_data)
    assert typ_enum == bdng__mimzy
    if isinstance(send_data, (IntegerArrayType, DecimalArrayType)
        ) or send_data in (boolean_array, datetime_date_array_type):
        return (lambda send_data, out_data, send_counts, recv_counts,
            send_disp, recv_disp: c_alltoallv(send_data._data.ctypes,
            out_data._data.ctypes, send_counts.ctypes, recv_counts.ctypes,
            send_disp.ctypes, recv_disp.ctypes, typ_enum))
    if isinstance(send_data, bodo.CategoricalArrayType):
        return (lambda send_data, out_data, send_counts, recv_counts,
            send_disp, recv_disp: c_alltoallv(send_data.codes.ctypes,
            out_data.codes.ctypes, send_counts.ctypes, recv_counts.ctypes,
            send_disp.ctypes, recv_disp.ctypes, typ_enum))
    return (lambda send_data, out_data, send_counts, recv_counts, send_disp,
        recv_disp: c_alltoallv(send_data.ctypes, out_data.ctypes,
        send_counts.ctypes, recv_counts.ctypes, send_disp.ctypes, recv_disp
        .ctypes, typ_enum))


def alltoallv_tup(send_data, out_data, send_counts, recv_counts, send_disp,
    recv_disp):
    return


@overload(alltoallv_tup, no_unliteral=True)
def alltoallv_tup_overload(send_data, out_data, send_counts, recv_counts,
    send_disp, recv_disp):
    count = send_data.count
    assert out_data.count == count
    laee__nljh = (
        'def f(send_data, out_data, send_counts, recv_counts, send_disp, recv_disp):\n'
        )
    for i in range(count):
        laee__nljh += (
            """  alltoallv(send_data[{}], out_data[{}], send_counts, recv_counts, send_disp, recv_disp)
"""
            .format(i, i))
    laee__nljh += '  return\n'
    mysn__otrqi = {}
    exec(laee__nljh, {'alltoallv': alltoallv}, mysn__otrqi)
    pgr__bfsl = mysn__otrqi['f']
    return pgr__bfsl


@numba.njit
def get_start_count(n):
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    start = bodo.libs.distributed_api.get_start(n, n_pes, rank)
    count = bodo.libs.distributed_api.get_node_portion(n, n_pes, rank)
    return start, count


@numba.njit
def get_start(total_size, pes, rank):
    hyzpk__cefr = total_size % pes
    zylm__wjri = (total_size - hyzpk__cefr) // pes
    return rank * zylm__wjri + min(rank, hyzpk__cefr)


@numba.njit
def get_end(total_size, pes, rank):
    hyzpk__cefr = total_size % pes
    zylm__wjri = (total_size - hyzpk__cefr) // pes
    return (rank + 1) * zylm__wjri + min(rank + 1, hyzpk__cefr)


@numba.njit
def get_node_portion(total_size, pes, rank):
    hyzpk__cefr = total_size % pes
    zylm__wjri = (total_size - hyzpk__cefr) // pes
    if rank < hyzpk__cefr:
        return zylm__wjri + 1
    else:
        return zylm__wjri


@numba.generated_jit(nopython=True)
def dist_cumsum(in_arr, out_arr):
    lkj__bekj = in_arr.dtype(0)
    zgh__mpu = np.int32(Reduce_Type.Sum.value)

    def cumsum_impl(in_arr, out_arr):
        uzbef__ocgmf = lkj__bekj
        for rxwzb__lri in np.nditer(in_arr):
            uzbef__ocgmf += rxwzb__lri.item()
        ivm__sfq = dist_exscan(uzbef__ocgmf, zgh__mpu)
        for i in range(in_arr.size):
            ivm__sfq += in_arr[i]
            out_arr[i] = ivm__sfq
        return 0
    return cumsum_impl


@numba.generated_jit(nopython=True)
def dist_cumprod(in_arr, out_arr):
    fcyq__fuuq = in_arr.dtype(1)
    zgh__mpu = np.int32(Reduce_Type.Prod.value)

    def cumprod_impl(in_arr, out_arr):
        uzbef__ocgmf = fcyq__fuuq
        for rxwzb__lri in np.nditer(in_arr):
            uzbef__ocgmf *= rxwzb__lri.item()
        ivm__sfq = dist_exscan(uzbef__ocgmf, zgh__mpu)
        if get_rank() == 0:
            ivm__sfq = fcyq__fuuq
        for i in range(in_arr.size):
            ivm__sfq *= in_arr[i]
            out_arr[i] = ivm__sfq
        return 0
    return cumprod_impl


@numba.generated_jit(nopython=True)
def dist_cummin(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        fcyq__fuuq = np.finfo(in_arr.dtype(1).dtype).max
    else:
        fcyq__fuuq = np.iinfo(in_arr.dtype(1).dtype).max
    zgh__mpu = np.int32(Reduce_Type.Min.value)

    def cummin_impl(in_arr, out_arr):
        uzbef__ocgmf = fcyq__fuuq
        for rxwzb__lri in np.nditer(in_arr):
            uzbef__ocgmf = min(uzbef__ocgmf, rxwzb__lri.item())
        ivm__sfq = dist_exscan(uzbef__ocgmf, zgh__mpu)
        if get_rank() == 0:
            ivm__sfq = fcyq__fuuq
        for i in range(in_arr.size):
            ivm__sfq = min(ivm__sfq, in_arr[i])
            out_arr[i] = ivm__sfq
        return 0
    return cummin_impl


@numba.generated_jit(nopython=True)
def dist_cummax(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        fcyq__fuuq = np.finfo(in_arr.dtype(1).dtype).min
    else:
        fcyq__fuuq = np.iinfo(in_arr.dtype(1).dtype).min
    fcyq__fuuq = in_arr.dtype(1)
    zgh__mpu = np.int32(Reduce_Type.Max.value)

    def cummax_impl(in_arr, out_arr):
        uzbef__ocgmf = fcyq__fuuq
        for rxwzb__lri in np.nditer(in_arr):
            uzbef__ocgmf = max(uzbef__ocgmf, rxwzb__lri.item())
        ivm__sfq = dist_exscan(uzbef__ocgmf, zgh__mpu)
        if get_rank() == 0:
            ivm__sfq = fcyq__fuuq
        for i in range(in_arr.size):
            ivm__sfq = max(ivm__sfq, in_arr[i])
            out_arr[i] = ivm__sfq
        return 0
    return cummax_impl


_allgather = types.ExternalFunction('allgather', types.void(types.voidptr,
    types.int32, types.voidptr, types.int32))


@numba.njit
def allgather(arr, val):
    xjsa__umzw = get_type_enum(arr)
    _allgather(arr.ctypes, 1, value_to_ptr(val), xjsa__umzw)


def dist_return(A):
    return A


def dist_return_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    zrze__uno = args[0]
    if equiv_set.has_shape(zrze__uno):
        return ArrayAnalysis.AnalyzeResult(shape=zrze__uno, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_distributed_api_dist_return = (
    dist_return_equiv)


def threaded_return(A):
    return A


@numba.njit
def set_arr_local(arr, ind, val):
    arr[ind] = val


@numba.njit
def local_alloc_size(n, in_arr):
    return n


@infer_global(threaded_return)
@infer_global(dist_return)
class ThreadedRetTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        return signature(args[0], *args)


@numba.njit
def parallel_print(*args):
    print(*args)


@numba.njit
def single_print(*args):
    if bodo.libs.distributed_api.get_rank() == 0:
        print(*args)


@numba.njit(no_cpython_wrapper=True)
def print_if_not_empty(arg):
    if len(arg) != 0 or bodo.get_rank() == 0:
        print(arg)


_wait = types.ExternalFunction('dist_wait', types.void(mpi_req_numba_type,
    types.bool_))


@numba.generated_jit(nopython=True)
def wait(req, cond=True):
    if isinstance(req, types.BaseTuple):
        count = len(req.types)
        tdy__aky = ','.join(f'_wait(req[{i}], cond)' for i in range(count))
        laee__nljh = 'def f(req, cond=True):\n'
        laee__nljh += f'  return {tdy__aky}\n'
        mysn__otrqi = {}
        exec(laee__nljh, {'_wait': _wait}, mysn__otrqi)
        impl = mysn__otrqi['f']
        return impl
    if is_overload_none(req):
        return lambda req, cond=True: None
    return lambda req, cond=True: _wait(req, cond)


class ReqArrayType(types.Type):

    def __init__(self):
        super(ReqArrayType, self).__init__(name='ReqArrayType()')


req_array_type = ReqArrayType()
register_model(ReqArrayType)(models.OpaqueModel)
waitall = types.ExternalFunction('dist_waitall', types.void(types.int32,
    req_array_type))
comm_req_alloc = types.ExternalFunction('comm_req_alloc', req_array_type(
    types.int32))
comm_req_dealloc = types.ExternalFunction('comm_req_dealloc', types.void(
    req_array_type))
req_array_setitem = types.ExternalFunction('req_array_setitem', types.void(
    req_array_type, types.int64, mpi_req_numba_type))


@overload(operator.setitem, no_unliteral=True)
def overload_req_arr_setitem(A, idx, val):
    if A == req_array_type:
        assert val == mpi_req_numba_type
        return lambda A, idx, val: req_array_setitem(A, idx, val)


@numba.njit
def _get_local_range(start, stop, chunk_start, chunk_count):
    assert start >= 0 and stop > 0
    tyro__abu = max(start, chunk_start)
    trb__lufq = min(stop, chunk_start + chunk_count)
    uan__njjt = tyro__abu - chunk_start
    fcmps__clok = trb__lufq - chunk_start
    if uan__njjt < 0 or fcmps__clok < 0:
        uan__njjt = 1
        fcmps__clok = 0
    return uan__njjt, fcmps__clok


@register_jitable
def _set_if_in_range(A, val, index, chunk_start):
    if index >= chunk_start and index < chunk_start + len(A):
        A[index - chunk_start] = val


@register_jitable
def _root_rank_select(old_val, new_val):
    if get_rank() == 0:
        return old_val
    return new_val


def get_tuple_prod(t):
    return np.prod(t)


@overload(get_tuple_prod, no_unliteral=True)
def get_tuple_prod_overload(t):
    if t == numba.core.types.containers.Tuple(()):
        return lambda t: 1

    def get_tuple_prod_impl(t):
        hyzpk__cefr = 1
        for a in t:
            hyzpk__cefr *= a
        return hyzpk__cefr
    return get_tuple_prod_impl


sig = types.void(types.voidptr, types.voidptr, types.intp, types.intp,
    types.intp, types.intp, types.int32, types.voidptr)
oneD_reshape_shuffle = types.ExternalFunction('oneD_reshape_shuffle', sig)


@numba.njit(no_cpython_wrapper=True, cache=True)
def dist_oneD_reshape_shuffle(lhs, in_arr, new_dim0_global_len, dest_ranks=None
    ):
    ccsyz__vcjn = np.ascontiguousarray(in_arr)
    nhv__uekn = get_tuple_prod(ccsyz__vcjn.shape[1:])
    gauot__jzqle = get_tuple_prod(lhs.shape[1:])
    if dest_ranks is not None:
        vpd__eve = np.array(dest_ranks, dtype=np.int32)
    else:
        vpd__eve = np.empty(0, dtype=np.int32)
    dtype_size = bodo.io.np_io.get_dtype_size(in_arr.dtype)
    oneD_reshape_shuffle(lhs.ctypes, ccsyz__vcjn.ctypes,
        new_dim0_global_len, len(in_arr), dtype_size * gauot__jzqle, 
        dtype_size * nhv__uekn, len(vpd__eve), vpd__eve.ctypes)
    check_and_propagate_cpp_exception()


permutation_int = types.ExternalFunction('permutation_int', types.void(
    types.voidptr, types.intp))


@numba.njit
def dist_permutation_int(lhs, n):
    permutation_int(lhs.ctypes, n)


permutation_array_index = types.ExternalFunction('permutation_array_index',
    types.void(types.voidptr, types.intp, types.intp, types.voidptr, types.
    int64, types.voidptr, types.intp))


@numba.njit
def dist_permutation_array_index(lhs, lhs_len, dtype_size, rhs, p, p_len):
    cvahp__ftse = np.ascontiguousarray(rhs)
    cue__plrr = get_tuple_prod(cvahp__ftse.shape[1:])
    blv__uwa = dtype_size * cue__plrr
    permutation_array_index(lhs.ctypes, lhs_len, blv__uwa, cvahp__ftse.
        ctypes, cvahp__ftse.shape[0], p.ctypes, p_len)
    check_and_propagate_cpp_exception()


from bodo.io import fsspec_reader, hdfs_reader, s3_reader
ll.add_symbol('finalize', hdist.finalize)
finalize = types.ExternalFunction('finalize', types.int32())
ll.add_symbol('finalize_s3', s3_reader.finalize_s3)
finalize_s3 = types.ExternalFunction('finalize_s3', types.int32())
ll.add_symbol('finalize_fsspec', fsspec_reader.finalize_fsspec)
finalize_fsspec = types.ExternalFunction('finalize_fsspec', types.int32())
ll.add_symbol('disconnect_hdfs', hdfs_reader.disconnect_hdfs)
disconnect_hdfs = types.ExternalFunction('disconnect_hdfs', types.int32())


def _check_for_cpp_errors():
    pass


@overload(_check_for_cpp_errors)
def overload_check_for_cpp_errors():
    return lambda : check_and_propagate_cpp_exception()


@numba.njit
def call_finalize():
    finalize()
    finalize_s3()
    finalize_fsspec()
    _check_for_cpp_errors()
    disconnect_hdfs()


def flush_stdout():
    if not sys.stdout.closed:
        sys.stdout.flush()


atexit.register(call_finalize)
atexit.register(flush_stdout)


def bcast_comm(data, comm_ranks, nranks):
    rank = bodo.libs.distributed_api.get_rank()
    dtype = bodo.typeof(data)
    dtype = _bcast_dtype(dtype)
    if rank != MPI_ROOT:
        data = get_value_for_type(dtype)
    return bcast_comm_impl(data, comm_ranks, nranks)


@overload(bcast_comm)
def bcast_comm_overload(data, comm_ranks, nranks):
    return lambda data, comm_ranks, nranks: bcast_comm_impl(data,
        comm_ranks, nranks)


@numba.generated_jit(nopython=True)
def bcast_comm_impl(data, comm_ranks, nranks):
    if isinstance(data, (types.Integer, types.Float)):
        typ_val = numba_to_c_type(data)
        laee__nljh = (
            """def bcast_scalar_impl(data, comm_ranks, nranks):
  send = np.empty(1, dtype)
  send[0] = data
  c_bcast(send.ctypes, np.int32(1), np.int32({}), comm_ranks,ctypes, np.int32({}))
  return send[0]
"""
            .format(typ_val, nranks))
        dtype = numba.np.numpy_support.as_dtype(data)
        mysn__otrqi = {}
        exec(laee__nljh, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast,
            'dtype': dtype}, mysn__otrqi)
        prn__qysuk = mysn__otrqi['bcast_scalar_impl']
        return prn__qysuk
    if isinstance(data, types.Array):
        return lambda data, comm_ranks, nranks: _bcast_np(data, comm_ranks,
            nranks)
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        rzwqk__thwwu = len(data.columns)
        eeq__lrqez = ', '.join('g_data_{}'.format(i) for i in range(
            rzwqk__thwwu))
        wzyl__gatv = bodo.utils.transform.gen_const_tup(data.columns)
        laee__nljh = 'def impl_df(data, comm_ranks, nranks):\n'
        for i in range(rzwqk__thwwu):
            laee__nljh += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            laee__nljh += (
                """  g_data_{} = bodo.libs.distributed_api.bcast_comm_impl(data_{}, comm_ranks, nranks)
"""
                .format(i, i))
        laee__nljh += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        laee__nljh += """  g_index = bodo.libs.distributed_api.bcast_comm_impl(index, comm_ranks, nranks)
"""
        laee__nljh += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})
"""
            .format(eeq__lrqez, wzyl__gatv))
        mysn__otrqi = {}
        exec(laee__nljh, {'bodo': bodo}, mysn__otrqi)
        tbex__zep = mysn__otrqi['impl_df']
        return tbex__zep
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, comm_ranks, nranks):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            start = data._start
            stop = data._stop
            qjjwh__ogqwo = data._step
            uri__cnm = data._name
            uri__cnm = bcast_scalar(uri__cnm)
            start = bcast_scalar(start)
            stop = bcast_scalar(stop)
            qjjwh__ogqwo = bcast_scalar(qjjwh__ogqwo)
            yafj__wpbje = bodo.libs.array_kernels.calc_nitems(start, stop,
                qjjwh__ogqwo)
            chunk_start = bodo.libs.distributed_api.get_start(yafj__wpbje,
                n_pes, rank)
            chunk_count = bodo.libs.distributed_api.get_node_portion(
                yafj__wpbje, n_pes, rank)
            tyro__abu = start + qjjwh__ogqwo * chunk_start
            trb__lufq = start + qjjwh__ogqwo * (chunk_start + chunk_count)
            trb__lufq = min(trb__lufq, stop)
            return bodo.hiframes.pd_index_ext.init_range_index(tyro__abu,
                trb__lufq, qjjwh__ogqwo, uri__cnm)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, comm_ranks, nranks):
            caxeu__sbebh = data._data
            uri__cnm = data._name
            arr = bodo.libs.distributed_api.bcast_comm_impl(caxeu__sbebh,
                comm_ranks, nranks)
            return bodo.utils.conversion.index_from_array(arr, uri__cnm)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, comm_ranks, nranks):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            uri__cnm = bodo.hiframes.pd_series_ext.get_series_name(data)
            obbo__vynj = bodo.libs.distributed_api.bcast_comm_impl(uri__cnm,
                comm_ranks, nranks)
            out_arr = bodo.libs.distributed_api.bcast_comm_impl(arr,
                comm_ranks, nranks)
            rso__mqbf = bodo.libs.distributed_api.bcast_comm_impl(index,
                comm_ranks, nranks)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                rso__mqbf, obbo__vynj)
        return impl_series
    if isinstance(data, types.BaseTuple):
        laee__nljh = 'def impl_tuple(data, comm_ranks, nranks):\n'
        laee__nljh += '  return ({}{})\n'.format(', '.join(
            'bcast_comm_impl(data[{}], comm_ranks, nranks)'.format(i) for i in
            range(len(data))), ',' if len(data) > 0 else '')
        mysn__otrqi = {}
        exec(laee__nljh, {'bcast_comm_impl': bcast_comm_impl}, mysn__otrqi)
        hkca__gwsp = mysn__otrqi['impl_tuple']
        return hkca__gwsp
    if data is types.none:
        return lambda data, comm_ranks, nranks: None


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _bcast_np(data, comm_ranks, nranks):
    typ_val = numba_to_c_type(data.dtype)
    ccl__zlmeb = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    uvjce__qgmhy = (0,) * ccl__zlmeb

    def bcast_arr_impl(data, comm_ranks, nranks):
        rank = bodo.libs.distributed_api.get_rank()
        caxeu__sbebh = np.ascontiguousarray(data)
        nun__nzv = data.ctypes
        msf__exj = uvjce__qgmhy
        if rank == MPI_ROOT:
            msf__exj = caxeu__sbebh.shape
        msf__exj = bcast_tuple(msf__exj)
        avdss__ylsju = get_tuple_prod(msf__exj[1:])
        send_counts = msf__exj[0] * avdss__ylsju
        yhiv__izlx = np.empty(send_counts, dtype)
        if rank == MPI_ROOT:
            c_bcast(nun__nzv, np.int32(send_counts), np.int32(typ_val),
                comm_ranks.ctypes, np.int32(nranks))
            return data
        else:
            c_bcast(yhiv__izlx.ctypes, np.int32(send_counts), np.int32(
                typ_val), comm_ranks.ctypes, np.int32(nranks))
            return yhiv__izlx.reshape((-1,) + msf__exj[1:])
    return bcast_arr_impl


node_ranks = None


def get_host_ranks():
    global node_ranks
    if node_ranks is None:
        zdno__wpl = MPI.COMM_WORLD
        pcwi__bwtp = MPI.Get_processor_name()
        waz__hpi = zdno__wpl.allgather(pcwi__bwtp)
        node_ranks = defaultdict(list)
        for i, hcc__vtgu in enumerate(waz__hpi):
            node_ranks[hcc__vtgu].append(i)
    return node_ranks


def create_subcomm_mpi4py(comm_ranks):
    zdno__wpl = MPI.COMM_WORLD
    bvw__otm = zdno__wpl.Get_group()
    efi__gvy = bvw__otm.Incl(comm_ranks)
    gbiwx__rvv = zdno__wpl.Create_group(efi__gvy)
    return gbiwx__rvv


def get_nodes_first_ranks():
    uno__dbf = get_host_ranks()
    return np.array([nor__zbt[0] for nor__zbt in uno__dbf.values()], dtype=
        'int32')


def get_num_nodes():
    return len(get_host_ranks())
