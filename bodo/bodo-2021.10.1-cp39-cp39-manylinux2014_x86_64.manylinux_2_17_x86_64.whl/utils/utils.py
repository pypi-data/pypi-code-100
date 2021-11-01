"""
Collection of utility functions. Needs to be refactored in separate files.
"""
import hashlib
import inspect
import keyword
import re
import warnings
from enum import Enum
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir, ir_utils, types
from numba.core.imputils import lower_builtin
from numba.core.ir_utils import find_callname, find_const, get_definition, guard, mk_unique_var, require
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, overload
from numba.np.arrayobj import get_itemsize, make_array, populate_array
import bodo
from bodo.libs.binary_arr_ext import bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import num_total_chars, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import string_type
from bodo.utils.typing import NOT_CONSTANT, BodoError
int128_type = types.Integer('int128', 128)


class CTypeEnum(Enum):
    Int8 = 0
    UInt8 = 1
    Int32 = 2
    UInt32 = 3
    Int64 = 4
    UInt64 = 7
    Float32 = 5
    Float64 = 6
    Int16 = 8
    UInt16 = 9
    STRING = 10
    Bool = 11
    Decimal = 12
    Date = 13
    Datetime = 14
    Timedelta = 15
    Int128 = 16
    LIST = 18
    STRUCT = 19
    BINARY = 20


_numba_to_c_type_map = {types.int8: CTypeEnum.Int8.value, types.uint8:
    CTypeEnum.UInt8.value, types.int32: CTypeEnum.Int32.value, types.uint32:
    CTypeEnum.UInt32.value, types.int64: CTypeEnum.Int64.value, types.
    uint64: CTypeEnum.UInt64.value, types.float32: CTypeEnum.Float32.value,
    types.float64: CTypeEnum.Float64.value, types.NPDatetime('ns'):
    CTypeEnum.Datetime.value, types.NPTimedelta('ns'): CTypeEnum.Timedelta.
    value, types.bool_: CTypeEnum.Bool.value, types.int16: CTypeEnum.Int16.
    value, types.uint16: CTypeEnum.UInt16.value, int128_type: CTypeEnum.
    Int128.value}
numba.core.errors.error_extras = {'unsupported_error': '', 'typing': '',
    'reportable': '', 'interpreter': '', 'constant_inference': ''}
np_alloc_callnames = 'empty', 'zeros', 'ones', 'full'


def unliteral_all(args):
    return tuple(types.unliteral(a) for a in args)


def get_constant(func_ir, var, default=NOT_CONSTANT):
    igra__mwkfg = guard(get_definition, func_ir, var)
    if igra__mwkfg is None:
        return default
    if isinstance(igra__mwkfg, ir.Const):
        return igra__mwkfg.value
    if isinstance(igra__mwkfg, ir.Var):
        return get_constant(func_ir, igra__mwkfg, default)
    return default


def numba_to_c_type(t):
    if isinstance(t, bodo.libs.decimal_arr_ext.Decimal128Type):
        return CTypeEnum.Decimal.value
    if t == bodo.hiframes.datetime_date_ext.datetime_date_type:
        return CTypeEnum.Date.value
    return _numba_to_c_type_map[t]


def is_alloc_callname(func_name, mod_name):
    return isinstance(mod_name, str) and (mod_name == 'numpy' and func_name in
        np_alloc_callnames or func_name == 'empty_inferred' and mod_name in
        ('numba.extending', 'numba.np.unsafe.ndarray') or func_name ==
        'pre_alloc_string_array' and mod_name == 'bodo.libs.str_arr_ext' or
        func_name == 'pre_alloc_binary_array' and mod_name ==
        'bodo.libs.binary_arr_ext' or func_name ==
        'alloc_random_access_string_array' and mod_name ==
        'bodo.libs.str_ext' or func_name == 'pre_alloc_array_item_array' and
        mod_name == 'bodo.libs.array_item_arr_ext' or func_name ==
        'pre_alloc_struct_array' and mod_name == 'bodo.libs.struct_arr_ext' or
        func_name == 'pre_alloc_tuple_array' and mod_name ==
        'bodo.libs.tuple_arr_ext' or func_name == 'alloc_bool_array' and 
        mod_name == 'bodo.libs.bool_arr_ext' or func_name ==
        'alloc_int_array' and mod_name == 'bodo.libs.int_arr_ext' or 
        func_name == 'alloc_datetime_date_array' and mod_name ==
        'bodo.hiframes.datetime_date_ext' or func_name ==
        'alloc_datetime_timedelta_array' and mod_name ==
        'bodo.hiframes.datetime_timedelta_ext' or func_name ==
        'alloc_decimal_array' and mod_name == 'bodo.libs.decimal_arr_ext' or
        func_name == 'alloc_categorical_array' and mod_name ==
        'bodo.hiframes.pd_categorical_ext' or func_name == 'gen_na_array' and
        mod_name == 'bodo.libs.array_kernels')


def find_build_tuple(func_ir, var):
    require(isinstance(var, (ir.Var, str)))
    dnauu__nvyl = get_definition(func_ir, var)
    require(isinstance(dnauu__nvyl, ir.Expr))
    require(dnauu__nvyl.op == 'build_tuple')
    return dnauu__nvyl.items


def cprint(*s):
    print(*s)


@infer_global(cprint)
class CprintInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.none, *unliteral_all(args))


typ_to_format = {types.int32: 'd', types.uint32: 'u', types.int64: 'lld',
    types.uint64: 'llu', types.float32: 'f', types.float64: 'lf', types.
    voidptr: 's'}


@lower_builtin(cprint, types.VarArg(types.Any))
def cprint_lower(context, builder, sig, args):
    for cwkk__jsg, val in enumerate(args):
        zji__idwi = sig.args[cwkk__jsg]
        if isinstance(zji__idwi, types.ArrayCTypes):
            cgutils.printf(builder, '%p ', val)
            continue
        ouza__ogu = typ_to_format[zji__idwi]
        cgutils.printf(builder, '%{} '.format(ouza__ogu), val)
    cgutils.printf(builder, '\n')
    return context.get_dummy_value()


def is_whole_slice(typemap, func_ir, var, accept_stride=False):
    require(typemap[var.name] == types.slice2_type or accept_stride and 
        typemap[var.name] == types.slice3_type)
    neni__jpunj = get_definition(func_ir, var)
    require(isinstance(neni__jpunj, ir.Expr) and neni__jpunj.op == 'call')
    assert len(neni__jpunj.args) == 2 or accept_stride and len(neni__jpunj.args
        ) == 3
    assert find_callname(func_ir, neni__jpunj) == ('slice', 'builtins')
    blqot__mou = get_definition(func_ir, neni__jpunj.args[0])
    nfbk__hdbf = get_definition(func_ir, neni__jpunj.args[1])
    require(isinstance(blqot__mou, ir.Const) and blqot__mou.value == None)
    require(isinstance(nfbk__hdbf, ir.Const) and nfbk__hdbf.value == None)
    return True


def is_slice_equiv_arr(arr_var, index_var, func_ir, equiv_set,
    accept_stride=False):
    sbj__kqt = get_definition(func_ir, index_var)
    require(find_callname(func_ir, sbj__kqt) == ('slice', 'builtins'))
    require(len(sbj__kqt.args) in (2, 3))
    require(find_const(func_ir, sbj__kqt.args[0]) in (0, None))
    require(equiv_set.is_equiv(sbj__kqt.args[1], arr_var.name + '#0'))
    require(accept_stride or len(sbj__kqt.args) == 2 or find_const(func_ir,
        sbj__kqt.args[2]) == 1)
    return True


def get_slice_step(typemap, func_ir, var):
    require(typemap[var.name] == types.slice3_type)
    neni__jpunj = get_definition(func_ir, var)
    require(isinstance(neni__jpunj, ir.Expr) and neni__jpunj.op == 'call')
    assert len(neni__jpunj.args) == 3
    return neni__jpunj.args[2]


def is_array_typ(var_typ, include_index_series=True):
    return is_np_array_typ(var_typ) or var_typ in (string_array_type, bodo.
        binary_array_type, bodo.hiframes.split_impl.
        string_array_split_view_type, bodo.hiframes.datetime_date_ext.
        datetime_date_array_type, bodo.hiframes.datetime_timedelta_ext.
        datetime_timedelta_array_type, boolean_array, bodo.libs.str_ext.
        random_access_string_array) or isinstance(var_typ, (
        IntegerArrayType, bodo.libs.decimal_arr_ext.DecimalArrayType, bodo.
        hiframes.pd_categorical_ext.CategoricalArrayType, bodo.libs.
        array_item_arr_ext.ArrayItemArrayType, bodo.libs.struct_arr_ext.
        StructArrayType, bodo.libs.interval_arr_ext.IntervalArrayType, bodo
        .libs.tuple_arr_ext.TupleArrayType, bodo.libs.map_arr_ext.
        MapArrayType, bodo.libs.csr_matrix_ext.CSRMatrixType)
        ) or include_index_series and (isinstance(var_typ, (bodo.hiframes.
        pd_series_ext.SeriesType, bodo.hiframes.pd_multi_index_ext.
        MultiIndexType)) or bodo.hiframes.pd_index_ext.is_pd_index_type(
        var_typ))


def is_np_array_typ(var_typ):
    return isinstance(var_typ, types.Array)


def is_distributable_typ(var_typ):
    return is_array_typ(var_typ) or isinstance(var_typ, bodo.hiframes.
        pd_dataframe_ext.DataFrameType) or isinstance(var_typ, types.List
        ) and is_distributable_typ(var_typ.dtype) or isinstance(var_typ,
        types.DictType) and is_distributable_typ(var_typ.value_type)


def is_distributable_tuple_typ(var_typ):
    return isinstance(var_typ, types.BaseTuple) and any(
        is_distributable_typ(t) or is_distributable_tuple_typ(t) for t in
        var_typ.types) or isinstance(var_typ, types.List
        ) and is_distributable_tuple_typ(var_typ.dtype) or isinstance(var_typ,
        types.DictType) and is_distributable_tuple_typ(var_typ.value_type
        ) or isinstance(var_typ, types.iterators.EnumerateType) and (
        is_distributable_typ(var_typ.yield_type[1]) or
        is_distributable_tuple_typ(var_typ.yield_type[1]))


@numba.generated_jit(nopython=True, cache=True)
def build_set_seen_na(A):

    def impl(A):
        s = dict()
        hwmfc__yxvn = False
        for cwkk__jsg in range(len(A)):
            if bodo.libs.array_kernels.isna(A, cwkk__jsg):
                hwmfc__yxvn = True
                continue
            s[A[cwkk__jsg]] = 0
        return s, hwmfc__yxvn
    return impl


@numba.generated_jit(nopython=True, cache=True)
def build_set(A):
    if isinstance(A, IntegerArrayType) or A in (string_array_type,
        boolean_array):

        def impl_int_arr(A):
            s = dict()
            for cwkk__jsg in range(len(A)):
                if not bodo.libs.array_kernels.isna(A, cwkk__jsg):
                    s[A[cwkk__jsg]] = 0
            return s
        return impl_int_arr
    else:

        def impl(A):
            s = dict()
            for cwkk__jsg in range(len(A)):
                s[A[cwkk__jsg]] = 0
            return s
        return impl


def to_array(A):
    return np.array(A)


@overload(to_array, no_unliteral=True)
def to_array_overload(A):
    if isinstance(A, types.DictType):
        dtype = A.key_type

        def impl(A):
            n = len(A)
            arr = alloc_type(n, dtype, (-1,))
            cwkk__jsg = 0
            for lhv__ptzer in A.keys():
                arr[cwkk__jsg] = lhv__ptzer
                cwkk__jsg += 1
            return arr
        return impl

    def to_array_impl(A):
        return np.array(A)
    try:
        numba.njit(to_array_impl).get_call_template((A,), {})
        return to_array_impl
    except:
        pass


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def unique(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:
        return lambda A: A.unique()
    return lambda A: to_array(build_set(A))


def empty_like_type(n, arr):
    return np.empty(n, arr.dtype)


@overload(empty_like_type, no_unliteral=True)
def empty_like_type_overload(n, arr):
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        return (lambda n, arr: bodo.hiframes.pd_categorical_ext.
            alloc_categorical_array(n, arr.dtype))
    if isinstance(arr, types.Array):
        return lambda n, arr: np.empty(n, arr.dtype)
    if isinstance(arr, types.List) and arr.dtype == string_type:

        def empty_like_type_str_list(n, arr):
            return [''] * n
        return empty_like_type_str_list
    if isinstance(arr, types.List) and arr.dtype == bytes_type:

        def empty_like_type_binary_list(n, arr):
            return [b''] * n
        return empty_like_type_binary_list
    if isinstance(arr, IntegerArrayType):
        pew__bse = arr.dtype

        def empty_like_type_int_arr(n, arr):
            return bodo.libs.int_arr_ext.alloc_int_array(n, pew__bse)
        return empty_like_type_int_arr
    if arr == boolean_array:

        def empty_like_type_bool_arr(n, arr):
            return bodo.libs.bool_arr_ext.alloc_bool_array(n)
        return empty_like_type_bool_arr
    if arr == bodo.hiframes.datetime_date_ext.datetime_date_array_type:

        def empty_like_type_datetime_date_arr(n, arr):
            return bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(n)
        return empty_like_type_datetime_date_arr
    if (arr == bodo.hiframes.datetime_timedelta_ext.
        datetime_timedelta_array_type):

        def empty_like_type_datetime_timedelta_arr(n, arr):
            return (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(n))
        return empty_like_type_datetime_timedelta_arr
    if isinstance(arr, bodo.libs.decimal_arr_ext.DecimalArrayType):
        precision = arr.precision
        scale = arr.scale

        def empty_like_type_decimal_arr(n, arr):
            return bodo.libs.decimal_arr_ext.alloc_decimal_array(n,
                precision, scale)
        return empty_like_type_decimal_arr
    assert arr == string_array_type

    def empty_like_type_str_arr(n, arr):
        thlxw__veqte = 20
        if len(arr) != 0:
            thlxw__veqte = num_total_chars(arr) // len(arr)
        return pre_alloc_string_array(n, n * thlxw__veqte)
    return empty_like_type_str_arr


def _empty_nd_impl(context, builder, arrtype, shapes):
    zlztq__ybg = make_array(arrtype)
    qkfz__aqf = zlztq__ybg(context, builder)
    omlov__izfmv = context.get_data_type(arrtype.dtype)
    xvk__cfrg = context.get_constant(types.intp, get_itemsize(context, arrtype)
        )
    rwdbu__mcx = context.get_constant(types.intp, 1)
    oqf__dhu = lir.Constant(lir.IntType(1), 0)
    for s in shapes:
        bfqeu__dlbj = builder.smul_with_overflow(rwdbu__mcx, s)
        rwdbu__mcx = builder.extract_value(bfqeu__dlbj, 0)
        oqf__dhu = builder.or_(oqf__dhu, builder.extract_value(bfqeu__dlbj, 1))
    if arrtype.ndim == 0:
        cyxvu__pzi = ()
    elif arrtype.layout == 'C':
        cyxvu__pzi = [xvk__cfrg]
        for kfpp__pii in reversed(shapes[1:]):
            cyxvu__pzi.append(builder.mul(cyxvu__pzi[-1], kfpp__pii))
        cyxvu__pzi = tuple(reversed(cyxvu__pzi))
    elif arrtype.layout == 'F':
        cyxvu__pzi = [xvk__cfrg]
        for kfpp__pii in shapes[:-1]:
            cyxvu__pzi.append(builder.mul(cyxvu__pzi[-1], kfpp__pii))
        cyxvu__pzi = tuple(cyxvu__pzi)
    else:
        raise NotImplementedError(
            "Don't know how to allocate array with layout '{0}'.".format(
            arrtype.layout))
    ost__dghdt = builder.smul_with_overflow(rwdbu__mcx, xvk__cfrg)
    ajt__eag = builder.extract_value(ost__dghdt, 0)
    oqf__dhu = builder.or_(oqf__dhu, builder.extract_value(ost__dghdt, 1))
    with builder.if_then(oqf__dhu, likely=False):
        cgutils.printf(builder,
            'array is too big; `arr.size * arr.dtype.itemsize` is larger than the maximum possible size.'
            )
    dtype = arrtype.dtype
    stbzh__rduz = context.get_preferred_array_alignment(dtype)
    mkxt__uyj = context.get_constant(types.uint32, stbzh__rduz)
    sqkhp__gnby = context.nrt.meminfo_alloc_aligned(builder, size=ajt__eag,
        align=mkxt__uyj)
    data = context.nrt.meminfo_data(builder, sqkhp__gnby)
    ahfa__kgdy = context.get_value_type(types.intp)
    pld__xilk = cgutils.pack_array(builder, shapes, ty=ahfa__kgdy)
    xyc__vjf = cgutils.pack_array(builder, cyxvu__pzi, ty=ahfa__kgdy)
    populate_array(qkfz__aqf, data=builder.bitcast(data, omlov__izfmv.
        as_pointer()), shape=pld__xilk, strides=xyc__vjf, itemsize=
        xvk__cfrg, meminfo=sqkhp__gnby)
    return qkfz__aqf


if bodo.numba_compat._check_numba_change:
    lines = inspect.getsource(numba.np.arrayobj._empty_nd_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b6a998927680caa35917a553c79704e9d813d8f1873d83a5f8513837c159fa29':
        warnings.warn('numba.np.arrayobj._empty_nd_impl has changed')


def alloc_arr_tup(n, arr_tup, init_vals=()):
    esbi__hwsjs = []
    for jurie__modc in arr_tup:
        esbi__hwsjs.append(np.empty(n, jurie__modc.dtype))
    return tuple(esbi__hwsjs)


@overload(alloc_arr_tup, no_unliteral=True)
def alloc_arr_tup_overload(n, data, init_vals=()):
    kihl__pvo = data.count
    selwc__jxfpv = ','.join(['empty_like_type(n, data[{}])'.format(
        cwkk__jsg) for cwkk__jsg in range(kihl__pvo)])
    if init_vals != ():
        selwc__jxfpv = ','.join([
            'np.full(n, init_vals[{}], data[{}].dtype)'.format(cwkk__jsg,
            cwkk__jsg) for cwkk__jsg in range(kihl__pvo)])
    kll__hipm = 'def f(n, data, init_vals=()):\n'
    kll__hipm += '  return ({}{})\n'.format(selwc__jxfpv, ',' if kihl__pvo ==
        1 else '')
    aicct__uvb = {}
    exec(kll__hipm, {'empty_like_type': empty_like_type, 'np': np}, aicct__uvb)
    rwf__zbnw = aicct__uvb['f']
    return rwf__zbnw


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def tuple_to_scalar(n):
    if isinstance(n, types.BaseTuple) and len(n.types) == 1:
        return lambda n: n[0]
    return lambda n: n


def alloc_type(n, t, s=None):
    return np.empty(n, t.dtype)


@overload(alloc_type)
def overload_alloc_type(n, t, s=None):
    zji__idwi = t.instance_type if isinstance(t, types.TypeRef) else t
    if zji__idwi == string_array_type:
        return (lambda n, t, s=None: bodo.libs.str_arr_ext.
            pre_alloc_string_array(n, s[0]))
    if zji__idwi == bodo.binary_array_type:
        return (lambda n, t, s=None: bodo.libs.binary_arr_ext.
            pre_alloc_binary_array(n, s[0]))
    if isinstance(zji__idwi, bodo.libs.array_item_arr_ext.ArrayItemArrayType):
        dtype = zji__idwi.dtype
        return (lambda n, t, s=None: bodo.libs.array_item_arr_ext.
            pre_alloc_array_item_array(n, s, dtype))
    if isinstance(zji__idwi, bodo.libs.struct_arr_ext.StructArrayType):
        dtypes = zji__idwi.data
        names = zji__idwi.names
        return (lambda n, t, s=None: bodo.libs.struct_arr_ext.
            pre_alloc_struct_array(n, s, dtypes, names))
    if isinstance(zji__idwi, bodo.libs.tuple_arr_ext.TupleArrayType):
        dtypes = zji__idwi.data
        return (lambda n, t, s=None: bodo.libs.tuple_arr_ext.
            pre_alloc_tuple_array(n, s, dtypes))
    if isinstance(zji__idwi, bodo.hiframes.pd_categorical_ext.
        CategoricalArrayType):
        if isinstance(t, types.TypeRef):
            if zji__idwi.dtype.categories is None:
                raise BodoError(
                    'UDFs or Groupbys that return Categorical values must have categories known at compile time.'
                    )
            _cat_dtype = pd.CategoricalDtype(zji__idwi.dtype.categories,
                zji__idwi.dtype.ordered)
            return (lambda n, t, s=None: bodo.hiframes.pd_categorical_ext.
                alloc_categorical_array(n, _cat_dtype))
        else:
            return (lambda n, t, s=None: bodo.hiframes.pd_categorical_ext.
                alloc_categorical_array(n, t.dtype))
    if zji__idwi.dtype == bodo.hiframes.datetime_date_ext.datetime_date_type:
        return (lambda n, t, s=None: bodo.hiframes.datetime_date_ext.
            alloc_datetime_date_array(n))
    if (zji__idwi.dtype == bodo.hiframes.datetime_timedelta_ext.
        datetime_timedelta_type):
        return (lambda n, t, s=None: bodo.hiframes.datetime_timedelta_ext.
            alloc_datetime_timedelta_array(n))
    if isinstance(zji__idwi, DecimalArrayType):
        precision = zji__idwi.dtype.precision
        scale = zji__idwi.dtype.scale
        return (lambda n, t, s=None: bodo.libs.decimal_arr_ext.
            alloc_decimal_array(n, precision, scale))
    dtype = numba.np.numpy_support.as_dtype(zji__idwi.dtype)
    if isinstance(zji__idwi, IntegerArrayType):
        return lambda n, t, s=None: bodo.libs.int_arr_ext.alloc_int_array(n,
            dtype)
    if zji__idwi == boolean_array:
        return lambda n, t, s=None: bodo.libs.bool_arr_ext.alloc_bool_array(n)
    return lambda n, t, s=None: np.empty(n, dtype)


def astype(A, t):
    return A.astype(t.dtype)


@overload(astype, no_unliteral=True)
def overload_astype(A, t):
    zji__idwi = t.instance_type if isinstance(t, types.TypeRef) else t
    dtype = zji__idwi.dtype
    if A == zji__idwi:
        return lambda A, t: A
    if isinstance(A, (types.Array, IntegerArrayType)) and isinstance(zji__idwi,
        types.Array):
        return lambda A, t: A.astype(dtype)
    if isinstance(zji__idwi, IntegerArrayType):
        return lambda A, t: bodo.libs.int_arr_ext.init_integer_array(A.
            astype(dtype), np.full(len(A) + 7 >> 3, 255, np.uint8))
    raise BodoError(f'cannot convert array type {A} to {zji__idwi}')


def full_type(n, val, t):
    return np.full(n, val, t.dtype)


@overload(full_type, no_unliteral=True)
def overload_full_type(n, val, t):
    zji__idwi = t.instance_type if isinstance(t, types.TypeRef) else t
    if isinstance(zji__idwi, types.Array):
        dtype = numba.np.numpy_support.as_dtype(zji__idwi.dtype)
        return lambda n, val, t: np.full(n, val, dtype)
    if isinstance(zji__idwi, IntegerArrayType):
        dtype = numba.np.numpy_support.as_dtype(zji__idwi.dtype)
        return lambda n, val, t: bodo.libs.int_arr_ext.init_integer_array(np
            .full(n, val, dtype), np.full(tuple_to_scalar(n) + 7 >> 3, 255,
            np.uint8))
    if zji__idwi == boolean_array:
        return lambda n, val, t: bodo.libs.bool_arr_ext.init_bool_array(np.
            full(n, val, np.bool_), np.full(tuple_to_scalar(n) + 7 >> 3, 
            255, np.uint8))
    if zji__idwi == string_array_type:

        def impl_str(n, val, t):
            ojne__tnhg = n * len(val)
            A = pre_alloc_string_array(n, ojne__tnhg)
            for cwkk__jsg in range(n):
                A[cwkk__jsg] = val
            return A
        return impl_str

    def impl(n, val, t):
        A = alloc_type(n, zji__idwi, (-1,))
        for cwkk__jsg in range(n):
            A[cwkk__jsg] = val
        return A
    return impl


@intrinsic
def get_ctypes_ptr(typingctx, ctypes_typ=None):
    assert isinstance(ctypes_typ, types.ArrayCTypes)

    def codegen(context, builder, sig, args):
        opqz__ymt, = args
        adki__xjo = context.make_helper(builder, sig.args[0], opqz__ymt)
        return adki__xjo.data
    return types.voidptr(ctypes_typ), codegen


@intrinsic
def is_null_pointer(typingctx, ptr_typ=None):

    def codegen(context, builder, signature, args):
        xpca__hln, = args
        sgoy__mzhi = context.get_constant_null(ptr_typ)
        return builder.icmp_unsigned('==', xpca__hln, sgoy__mzhi)
    return types.bool_(ptr_typ), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def tuple_list_to_array(A, data, elem_type):
    elem_type = elem_type.instance_type if isinstance(elem_type, types.TypeRef
        ) else elem_type
    kll__hipm = 'def impl(A, data, elem_type):\n'
    kll__hipm += '  for i, d in enumerate(data):\n'
    if elem_type == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        kll__hipm += '    A[i] = bodo.utils.conversion.unbox_if_timestamp(d)\n'
    else:
        kll__hipm += '    A[i] = d\n'
    aicct__uvb = {}
    exec(kll__hipm, {'bodo': bodo}, aicct__uvb)
    impl = aicct__uvb['impl']
    return impl


def object_length(c, obj):
    npb__qoug = c.context.get_argument_type(types.pyobject)
    ugjj__dxcfu = lir.FunctionType(lir.IntType(64), [npb__qoug])
    ohbrx__mjs = cgutils.get_or_insert_function(c.builder.module,
        ugjj__dxcfu, name='PyObject_Length')
    return c.builder.call(ohbrx__mjs, (obj,))


def sequence_getitem(c, obj, ind):
    npb__qoug = c.context.get_argument_type(types.pyobject)
    ugjj__dxcfu = lir.FunctionType(npb__qoug, [npb__qoug, lir.IntType(64)])
    ohbrx__mjs = cgutils.get_or_insert_function(c.builder.module,
        ugjj__dxcfu, name='PySequence_GetItem')
    return c.builder.call(ohbrx__mjs, (obj, ind))


@intrinsic
def incref(typingctx, data=None):

    def codegen(context, builder, signature, args):
        dwkss__dyo, = args
        context.nrt.incref(builder, signature.args[0], dwkss__dyo)
    return types.void(data), codegen


def gen_getitem(out_var, in_var, ind, calltypes, nodes):
    piexc__fui = out_var.loc
    xcyy__wcxd = ir.Expr.static_getitem(in_var, ind, None, piexc__fui)
    calltypes[xcyy__wcxd] = None
    nodes.append(ir.Assign(xcyy__wcxd, out_var, piexc__fui))


def is_static_getsetitem(node):
    return is_expr(node, 'static_getitem') or isinstance(node, ir.StaticSetItem
        )


def get_getsetitem_index_var(node, typemap, nodes):
    index_var = node.index_var if is_static_getsetitem(node) else node.index
    if index_var is None:
        assert is_static_getsetitem(node)
        try:
            ttek__ushf = types.literal(node.index)
        except:
            ttek__ushf = numba.typeof(node.index)
        index_var = ir.Var(node.value.scope, ir_utils.mk_unique_var(
            'dummy_index'), node.loc)
        typemap[index_var.name] = ttek__ushf
        nodes.append(ir.Assign(ir.Const(node.index, node.loc), index_var,
            node.loc))
    return index_var


import copy
ir.Const.__deepcopy__ = lambda self, memo: ir.Const(self.value, copy.
    deepcopy(self.loc))


def is_call_assign(stmt):
    return isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
        ) and stmt.value.op == 'call'


def is_call(expr):
    return isinstance(expr, ir.Expr) and expr.op == 'call'


def is_var_assign(inst):
    return isinstance(inst, ir.Assign) and isinstance(inst.value, ir.Var)


def is_assign(inst):
    return isinstance(inst, ir.Assign)


def is_expr(val, op):
    return isinstance(val, ir.Expr) and val.op == op


def sanitize_varname(varname):
    if isinstance(varname, (tuple, list)):
        varname = '_'.join(sanitize_varname(lhv__ptzer) for lhv__ptzer in
            varname)
    varname = str(varname)
    oypa__cqxbb = re.sub('\\W+', '_', varname)
    if not oypa__cqxbb or not oypa__cqxbb[0].isalpha():
        oypa__cqxbb = '_' + oypa__cqxbb
    if not oypa__cqxbb.isidentifier() or keyword.iskeyword(oypa__cqxbb):
        oypa__cqxbb = mk_unique_var('new_name').replace('.', '_')
    return oypa__cqxbb


def dump_node_list(node_list):
    for n in node_list:
        print('   ', n)


def debug_prints():
    return numba.core.config.DEBUG_ARRAY_OPT == 1


@overload(reversed)
def list_reverse(A):
    if isinstance(A, types.List):

        def impl_reversed(A):
            cuci__fmkq = len(A)
            for cwkk__jsg in range(cuci__fmkq):
                yield A[cuci__fmkq - 1 - cwkk__jsg]
        return impl_reversed


@numba.njit()
def count_nonnan(a):
    return np.count_nonzero(~np.isnan(a))


@numba.njit()
def nanvar_ddof1(a):
    pgu__prafa = count_nonnan(a)
    if pgu__prafa <= 1:
        return np.nan
    return np.nanvar(a) * (pgu__prafa / (pgu__prafa - 1))


@numba.njit()
def nanstd_ddof1(a):
    return np.sqrt(nanvar_ddof1(a))


def has_supported_h5py():
    try:
        import h5py
        from bodo.io import _hdf5
    except ImportError as usbg__uol:
        jwr__vrcw = False
    else:
        jwr__vrcw = h5py.version.hdf5_version_tuple[1] == 10
    return jwr__vrcw


def check_h5py():
    if not has_supported_h5py():
        raise BodoError("install 'h5py' package to enable hdf5 support")


def has_pyarrow():
    try:
        import pyarrow
    except ImportError as usbg__uol:
        yxks__lfuv = False
    else:
        yxks__lfuv = True
    return yxks__lfuv


def has_scipy():
    try:
        import scipy
    except ImportError as usbg__uol:
        ptjx__hyu = False
    else:
        ptjx__hyu = True
    return ptjx__hyu


@intrinsic
def check_and_propagate_cpp_exception(typingctx):

    def codegen(context, builder, sig, args):
        dab__wrjx = context.get_python_api(builder)
        ytzlt__jpdt = dab__wrjx.err_occurred()
        otid__wsiq = cgutils.is_not_null(builder, ytzlt__jpdt)
        with builder.if_then(otid__wsiq):
            builder.ret(numba.core.callconv.RETCODE_EXC)
    return types.void(), codegen


def inlined_check_and_propagate_cpp_exception(context, builder):
    dab__wrjx = context.get_python_api(builder)
    ytzlt__jpdt = dab__wrjx.err_occurred()
    otid__wsiq = cgutils.is_not_null(builder, ytzlt__jpdt)
    with builder.if_then(otid__wsiq):
        builder.ret(numba.core.callconv.RETCODE_EXC)


@numba.njit
def check_java_installation(fname):
    with numba.objmode():
        check_java_installation_(fname)


def check_java_installation_(fname):
    if not fname.startswith('hdfs://'):
        return
    import shutil
    if not shutil.which('java'):
        dvj__pjl = (
            "Java not found. Make sure openjdk is installed for hdfs. openjdk can be installed by calling 'conda install openjdk=8 -c conda-forge'."
            )
        raise BodoError(dvj__pjl)


dt_err = """
        If you are trying to set NULL values for timedelta64 in regular Python, 

        consider using np.timedelta64('nat') instead of None
        """
