"""Nullable integer array corresponding to Pandas IntegerArray.
However, nulls are stored in bit arrays similar to Arrow's arrays.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, type_callable, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs.str_arr_ext import kBitmask
from bodo.libs import array_ext, hstr_ext
ll.add_symbol('mask_arr_to_bitmap', hstr_ext.mask_arr_to_bitmap)
ll.add_symbol('is_pd_int_array', array_ext.is_pd_int_array)
ll.add_symbol('int_array_from_sequence', array_ext.int_array_from_sequence)
from bodo.hiframes.datetime_timedelta_ext import pd_timedelta_type
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, check_unsupported_args, is_iterable_type, is_list_like_index_type, is_overload_false, is_overload_none, is_overload_true, parse_dtype, raise_bodo_error, to_nullable_type


class IntegerArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        self.dtype = dtype
        super(IntegerArrayType, self).__init__(name='IntegerArrayType({})'.
            format(dtype))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return IntegerArrayType(self.dtype)


@register_model(IntegerArrayType)
class IntegerArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        zhw__niqpw = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, zhw__niqpw)


make_attribute_wrapper(IntegerArrayType, 'data', '_data')
make_attribute_wrapper(IntegerArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.IntegerArray)
def _typeof_pd_int_array(val, c):
    orbpk__ckvc = 8 * val.dtype.itemsize
    sbm__foa = '' if val.dtype.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(sbm__foa, orbpk__ckvc))
    return IntegerArrayType(dtype)


class IntDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Integer)
        self.dtype = dtype
        bnorr__ikjb = '{}Int{}Dtype()'.format('' if dtype.signed else 'U',
            dtype.bitwidth)
        super(IntDtype, self).__init__(bnorr__ikjb)


register_model(IntDtype)(models.OpaqueModel)


@box(IntDtype)
def box_intdtype(typ, val, c):
    jwe__zncv = c.context.insert_const_string(c.builder.module, 'pandas')
    twifl__jkqb = c.pyapi.import_module_noblock(jwe__zncv)
    mlsek__aya = c.pyapi.call_method(twifl__jkqb, str(typ)[:-2], ())
    c.pyapi.decref(twifl__jkqb)
    return mlsek__aya


@unbox(IntDtype)
def unbox_intdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_int_dtype(val, c):
    orbpk__ckvc = 8 * val.itemsize
    sbm__foa = '' if val.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(sbm__foa, orbpk__ckvc))
    return IntDtype(dtype)


def _register_int_dtype(t):
    typeof_impl.register(t)(typeof_pd_int_dtype)
    int_dtype = typeof_pd_int_dtype(t(), None)
    type_callable(t)(lambda c: lambda : int_dtype)
    lower_builtin(t)(lambda c, b, s, a: c.get_dummy_value())


pd_int_dtype_classes = (pd.Int8Dtype, pd.Int16Dtype, pd.Int32Dtype, pd.
    Int64Dtype, pd.UInt8Dtype, pd.UInt16Dtype, pd.UInt32Dtype, pd.UInt64Dtype)
for t in pd_int_dtype_classes:
    _register_int_dtype(t)


@numba.extending.register_jitable
def mask_arr_to_bitmap(mask_arr):
    n = len(mask_arr)
    lpr__xppel = n + 7 >> 3
    hxvw__sqf = np.empty(lpr__xppel, np.uint8)
    for i in range(n):
        bldrw__ocwm = i // 8
        hxvw__sqf[bldrw__ocwm] ^= np.uint8(-np.uint8(not mask_arr[i]) ^
            hxvw__sqf[bldrw__ocwm]) & kBitmask[i % 8]
    return hxvw__sqf


@unbox(IntegerArrayType)
def unbox_int_array(typ, obj, c):
    dmxrl__kss = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(dmxrl__kss)
    c.pyapi.decref(dmxrl__kss)
    cvs__odtss = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    lpr__xppel = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    ewdnr__xlpu = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [lpr__xppel])
    wed__days = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()]
        )
    ctt__ngow = cgutils.get_or_insert_function(c.builder.module, wed__days,
        name='is_pd_int_array')
    mxfb__jsoy = c.builder.call(ctt__ngow, [obj])
    riu__ejlgq = c.builder.icmp_unsigned('!=', mxfb__jsoy, mxfb__jsoy.type(0))
    with c.builder.if_else(riu__ejlgq) as (pd_then, pd_otherwise):
        with pd_then:
            shaer__bme = c.pyapi.object_getattr_string(obj, '_data')
            cvs__odtss.data = c.pyapi.to_native_value(types.Array(typ.dtype,
                1, 'C'), shaer__bme).value
            cek__qrhn = c.pyapi.object_getattr_string(obj, '_mask')
            mask_arr = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), cek__qrhn).value
            c.pyapi.decref(shaer__bme)
            c.pyapi.decref(cek__qrhn)
            onueh__xgx = c.context.make_array(types.Array(types.bool_, 1, 'C')
                )(c.context, c.builder, mask_arr)
            wed__days = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            ctt__ngow = cgutils.get_or_insert_function(c.builder.module,
                wed__days, name='mask_arr_to_bitmap')
            c.builder.call(ctt__ngow, [ewdnr__xlpu.data, onueh__xgx.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), mask_arr)
        with pd_otherwise:
            yya__zcx = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
                types.Array(typ.dtype, 1, 'C'), [n])
            wed__days = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            uzxh__qopu = cgutils.get_or_insert_function(c.builder.module,
                wed__days, name='int_array_from_sequence')
            c.builder.call(uzxh__qopu, [obj, c.builder.bitcast(yya__zcx.
                data, lir.IntType(8).as_pointer()), ewdnr__xlpu.data])
            cvs__odtss.data = yya__zcx._getvalue()
    cvs__odtss.null_bitmap = ewdnr__xlpu._getvalue()
    hpm__kdrf = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cvs__odtss._getvalue(), is_error=hpm__kdrf)


@box(IntegerArrayType)
def box_int_arr(typ, val, c):
    cvs__odtss = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        cvs__odtss.data, c.env_manager)
    dwcae__yldub = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, cvs__odtss.null_bitmap).data
    dmxrl__kss = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(dmxrl__kss)
    jwe__zncv = c.context.insert_const_string(c.builder.module, 'numpy')
    jegq__edu = c.pyapi.import_module_noblock(jwe__zncv)
    ogs__qqdqd = c.pyapi.object_getattr_string(jegq__edu, 'bool_')
    mask_arr = c.pyapi.call_method(jegq__edu, 'empty', (dmxrl__kss, ogs__qqdqd)
        )
    fdchn__hkjzs = c.pyapi.object_getattr_string(mask_arr, 'ctypes')
    woy__cac = c.pyapi.object_getattr_string(fdchn__hkjzs, 'data')
    nih__mnx = c.builder.inttoptr(c.pyapi.long_as_longlong(woy__cac), lir.
        IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as loop:
        i = loop.index
        gdj__dqrz = c.builder.lshr(i, lir.Constant(lir.IntType(64), 3))
        szzaf__oguvp = c.builder.load(cgutils.gep(c.builder, dwcae__yldub,
            gdj__dqrz))
        xmw__dkzs = c.builder.trunc(c.builder.and_(i, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(szzaf__oguvp, xmw__dkzs), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        msey__dnek = cgutils.gep(c.builder, nih__mnx, i)
        c.builder.store(val, msey__dnek)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        cvs__odtss.null_bitmap)
    jwe__zncv = c.context.insert_const_string(c.builder.module, 'pandas')
    twifl__jkqb = c.pyapi.import_module_noblock(jwe__zncv)
    lrt__qdrs = c.pyapi.object_getattr_string(twifl__jkqb, 'arrays')
    mlsek__aya = c.pyapi.call_method(lrt__qdrs, 'IntegerArray', (data,
        mask_arr))
    c.pyapi.decref(twifl__jkqb)
    c.pyapi.decref(dmxrl__kss)
    c.pyapi.decref(jegq__edu)
    c.pyapi.decref(ogs__qqdqd)
    c.pyapi.decref(fdchn__hkjzs)
    c.pyapi.decref(woy__cac)
    c.pyapi.decref(lrt__qdrs)
    c.pyapi.decref(data)
    c.pyapi.decref(mask_arr)
    return mlsek__aya


@intrinsic
def init_integer_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        adfg__xstwd, jnha__cddhj = args
        cvs__odtss = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        cvs__odtss.data = adfg__xstwd
        cvs__odtss.null_bitmap = jnha__cddhj
        context.nrt.incref(builder, signature.args[0], adfg__xstwd)
        context.nrt.incref(builder, signature.args[1], jnha__cddhj)
        return cvs__odtss._getvalue()
    oqm__nysu = IntegerArrayType(data.dtype)
    ftxo__oyvo = oqm__nysu(data, null_bitmap)
    return ftxo__oyvo, codegen


@lower_constant(IntegerArrayType)
def lower_constant_int_arr(context, builder, typ, pyval):
    n = len(pyval)
    tmbve__itms = np.empty(n, pyval.dtype.type)
    wkfmt__ebjek = np.empty(n + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        isgj__vpae = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(wkfmt__ebjek, i, int(not
            isgj__vpae))
        if not isgj__vpae:
            tmbve__itms[i] = s
    zge__qwdlh = context.get_constant_generic(builder, types.Array(typ.
        dtype, 1, 'C'), tmbve__itms)
    zqqo__dvoec = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), wkfmt__ebjek)
    fjtcl__avijp = context.make_helper(builder, typ)
    fjtcl__avijp.data = zge__qwdlh
    fjtcl__avijp.null_bitmap = zqqo__dvoec
    return fjtcl__avijp._getvalue()


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_int_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    stgt__yub = args[0]
    if equiv_set.has_shape(stgt__yub):
        return ArrayAnalysis.AnalyzeResult(shape=stgt__yub, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_get_int_arr_data = (
    get_int_arr_data_equiv)


def init_integer_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    stgt__yub = args[0]
    if equiv_set.has_shape(stgt__yub):
        return ArrayAnalysis.AnalyzeResult(shape=stgt__yub, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_init_integer_array = (
    init_integer_array_equiv)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


def alias_ext_init_integer_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_integer_array',
    'bodo.libs.int_arr_ext'] = alias_ext_init_integer_array
numba.core.ir_utils.alias_func_extensions['get_int_arr_data',
    'bodo.libs.int_arr_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_int_arr_bitmap',
    'bodo.libs.int_arr_ext'] = alias_ext_dummy_func


@numba.njit(no_cpython_wrapper=True)
def alloc_int_array(n, dtype):
    tmbve__itms = np.empty(n, dtype)
    gilk__nxrgd = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_integer_array(tmbve__itms, gilk__nxrgd)


def alloc_int_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_alloc_int_array = (
    alloc_int_array_equiv)


@numba.extending.register_jitable
def set_bit_to_arr(bits, i, bit_is_set):
    bits[i // 8] ^= np.uint8(-np.uint8(bit_is_set) ^ bits[i // 8]) & kBitmask[
        i % 8]


@numba.extending.register_jitable
def get_bit_bitmap_arr(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@overload(operator.getitem, no_unliteral=True)
def int_arr_getitem(A, ind):
    if not isinstance(A, IntegerArrayType):
        return
    if isinstance(ind, types.Integer):
        return lambda A, ind: A._data[ind]
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            yoreq__xpj, vlqf__eahy = array_getitem_bool_index(A, ind)
            return init_integer_array(yoreq__xpj, vlqf__eahy)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            yoreq__xpj, vlqf__eahy = array_getitem_int_index(A, ind)
            return init_integer_array(yoreq__xpj, vlqf__eahy)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            yoreq__xpj, vlqf__eahy = array_getitem_slice_index(A, ind)
            return init_integer_array(yoreq__xpj, vlqf__eahy)
        return impl_slice
    raise BodoError(
        f'getitem for IntegerArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def int_arr_setitem(A, idx, val):
    if not isinstance(A, IntegerArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    nutog__vzu = (
        f"setitem for IntegerArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    dgm__bjgio = isinstance(val, (types.Integer, types.Boolean))
    if isinstance(idx, types.Integer):
        if dgm__bjgio:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(nutog__vzu)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean)) or dgm__bjgio):
        raise BodoError(nutog__vzu)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, types.Integer):

        def impl_arr_ind_mask(A, idx, val):
            array_setitem_int_index(A, idx, val)
        return impl_arr_ind_mask
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:

        def impl_bool_ind_mask(A, idx, val):
            array_setitem_bool_index(A, idx, val)
        return impl_bool_ind_mask
    if isinstance(idx, types.SliceType):

        def impl_slice_mask(A, idx, val):
            array_setitem_slice_index(A, idx, val)
        return impl_slice_mask
    raise BodoError(
        f'setitem for IntegerArray with indexing type {idx} not supported.')


@overload(len, no_unliteral=True)
def overload_int_arr_len(A):
    if isinstance(A, IntegerArrayType):
        return lambda A: len(A._data)


@overload_attribute(IntegerArrayType, 'shape')
def overload_int_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(IntegerArrayType, 'dtype')
def overload_int_arr_dtype(A):
    dtype_class = getattr(pd, '{}Int{}Dtype'.format('' if A.dtype.signed else
        'U', A.dtype.bitwidth))
    return lambda A: dtype_class()


@overload_attribute(IntegerArrayType, 'ndim')
def overload_int_arr_ndim(A):
    return lambda A: 1


@overload_attribute(IntegerArrayType, 'nbytes')
def int_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


@overload_method(IntegerArrayType, 'copy', no_unliteral=True)
def overload_int_arr_copy(A):
    return lambda A: bodo.libs.int_arr_ext.init_integer_array(bodo.libs.
        int_arr_ext.get_int_arr_data(A).copy(), bodo.libs.int_arr_ext.
        get_int_arr_bitmap(A).copy())


@overload_method(IntegerArrayType, 'astype', no_unliteral=True)
def overload_int_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "IntegerArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if isinstance(dtype, types.NumberClass):
        dtype = dtype.dtype
    if isinstance(dtype, IntDtype) and A.dtype == dtype.dtype:
        if is_overload_false(copy):
            return lambda A, dtype, copy=True: A
        elif is_overload_true(copy):
            return lambda A, dtype, copy=True: A.copy()
        else:

            def impl(A, dtype, copy=True):
                if copy:
                    return A.copy()
                else:
                    return A
            return impl
    if isinstance(dtype, IntDtype):
        np_dtype = dtype.dtype
        return (lambda A, dtype, copy=True: bodo.libs.int_arr_ext.
            init_integer_array(bodo.libs.int_arr_ext.get_int_arr_data(A).
            astype(np_dtype), bodo.libs.int_arr_ext.get_int_arr_bitmap(A).
            copy()))
    nb_dtype = parse_dtype(dtype, 'IntegerArray.astype')
    if isinstance(nb_dtype, types.Float):

        def impl_float(A, dtype, copy=True):
            data = bodo.libs.int_arr_ext.get_int_arr_data(A)
            n = len(data)
            orqa__nkg = np.empty(n, nb_dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                orqa__nkg[i] = data[i]
                if bodo.libs.array_kernels.isna(A, i):
                    orqa__nkg[i] = np.nan
            return orqa__nkg
        return impl_float
    return lambda A, dtype, copy=True: bodo.libs.int_arr_ext.get_int_arr_data(A
        ).astype(nb_dtype)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def apply_null_mask(arr, bitmap, mask_fill, inplace):
    assert isinstance(arr, types.Array)
    if isinstance(arr.dtype, types.Integer):
        if is_overload_none(inplace):
            return (lambda arr, bitmap, mask_fill, inplace: bodo.libs.
                int_arr_ext.init_integer_array(arr, bitmap.copy()))
        else:
            return (lambda arr, bitmap, mask_fill, inplace: bodo.libs.
                int_arr_ext.init_integer_array(arr, bitmap))
    if isinstance(arr.dtype, types.Float):

        def impl(arr, bitmap, mask_fill, inplace):
            n = len(arr)
            for i in numba.parfors.parfor.internal_prange(n):
                if not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bitmap, i):
                    arr[i] = np.nan
            return arr
        return impl
    if arr.dtype == types.bool_:

        def impl_bool(arr, bitmap, mask_fill, inplace):
            n = len(arr)
            for i in numba.parfors.parfor.internal_prange(n):
                if not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bitmap, i):
                    arr[i] = mask_fill
            return arr
        return impl_bool
    return lambda arr, bitmap, mask_fill, inplace: arr


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def merge_bitmaps(B1, B2, n, inplace):
    assert B1 == types.Array(types.uint8, 1, 'C')
    assert B2 == types.Array(types.uint8, 1, 'C')
    if not is_overload_none(inplace):

        def impl_inplace(B1, B2, n, inplace):
            for i in numba.parfors.parfor.internal_prange(n):
                brieu__vxh = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
                nzyg__vfhn = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
                mhxjw__vqxy = brieu__vxh & nzyg__vfhn
                bodo.libs.int_arr_ext.set_bit_to_arr(B1, i, mhxjw__vqxy)
            return B1
        return impl_inplace

    def impl(B1, B2, n, inplace):
        numba.parfors.parfor.init_prange()
        lpr__xppel = n + 7 >> 3
        orqa__nkg = np.empty(lpr__xppel, np.uint8)
        for i in numba.parfors.parfor.internal_prange(n):
            brieu__vxh = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
            nzyg__vfhn = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
            mhxjw__vqxy = brieu__vxh & nzyg__vfhn
            bodo.libs.int_arr_ext.set_bit_to_arr(orqa__nkg, i, mhxjw__vqxy)
        return orqa__nkg
    return impl


ufunc_aliases = {'subtract': 'sub', 'multiply': 'mul', 'floor_divide':
    'floordiv', 'true_divide': 'truediv', 'power': 'pow', 'remainder':
    'mod', 'divide': 'div', 'equal': 'eq', 'not_equal': 'ne', 'less': 'lt',
    'less_equal': 'le', 'greater': 'gt', 'greater_equal': 'ge'}


def create_op_overload(op, n_inputs):
    if n_inputs == 1:

        def overload_int_arr_op_nin_1(A):
            if isinstance(A, IntegerArrayType):
                return get_nullable_array_unary_impl(op, A)
        return overload_int_arr_op_nin_1
    elif n_inputs == 2:

        def overload_series_op_nin_2(lhs, rhs):
            if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
                IntegerArrayType):
                return get_nullable_array_binary_impl(op, lhs, rhs)
        return overload_series_op_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for hbx__zupei in numba.np.ufunc_db.get_ufuncs():
        clxj__uig = create_op_overload(hbx__zupei, hbx__zupei.nin)
        overload(hbx__zupei, no_unliteral=True)(clxj__uig)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        clxj__uig = create_op_overload(op, 2)
        overload(op)(clxj__uig)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        clxj__uig = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(clxj__uig)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        clxj__uig = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(clxj__uig)


_install_unary_ops()


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data_tup(arrs):
    axch__bzox = len(arrs.types)
    aoaux__vzk = 'def f(arrs):\n'
    mlsek__aya = ', '.join('arrs[{}]._data'.format(i) for i in range(
        axch__bzox))
    aoaux__vzk += '  return ({}{})\n'.format(mlsek__aya, ',' if axch__bzox ==
        1 else '')
    yith__rvlp = {}
    exec(aoaux__vzk, {}, yith__rvlp)
    impl = yith__rvlp['f']
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def concat_bitmap_tup(arrs):
    axch__bzox = len(arrs.types)
    ejtiy__jdokn = '+'.join('len(arrs[{}]._data)'.format(i) for i in range(
        axch__bzox))
    aoaux__vzk = 'def f(arrs):\n'
    aoaux__vzk += '  n = {}\n'.format(ejtiy__jdokn)
    aoaux__vzk += '  n_bytes = (n + 7) >> 3\n'
    aoaux__vzk += '  new_mask = np.empty(n_bytes, np.uint8)\n'
    aoaux__vzk += '  curr_bit = 0\n'
    for i in range(axch__bzox):
        aoaux__vzk += '  old_mask = arrs[{}]._null_bitmap\n'.format(i)
        aoaux__vzk += '  for j in range(len(arrs[{}])):\n'.format(i)
        aoaux__vzk += (
            '    bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        aoaux__vzk += (
            '    bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        aoaux__vzk += '    curr_bit += 1\n'
    aoaux__vzk += '  return new_mask\n'
    yith__rvlp = {}
    exec(aoaux__vzk, {'np': np, 'bodo': bodo}, yith__rvlp)
    impl = yith__rvlp['f']
    return impl


@overload_method(IntegerArrayType, 'sum', no_unliteral=True)
def overload_int_arr_sum(A, skipna=True, min_count=0):
    pan__utcl = dict(skipna=skipna, min_count=min_count)
    trm__lvbsx = dict(skipna=True, min_count=0)
    check_unsupported_args('IntegerArray.sum', pan__utcl, trm__lvbsx)

    def impl(A, skipna=True, min_count=0):
        numba.parfors.parfor.init_prange()
        s = 0
        for i in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, i):
                val = A[i]
            s += val
        return s
    return impl


@overload_method(IntegerArrayType, 'unique', no_unliteral=True)
def overload_unique(A):
    dtype = A.dtype

    def impl_int_arr(A):
        data = []
        xmw__dkzs = []
        hkbop__vpzb = False
        s = set()
        for i in range(len(A)):
            val = A[i]
            if bodo.libs.array_kernels.isna(A, i):
                if not hkbop__vpzb:
                    data.append(dtype(1))
                    xmw__dkzs.append(False)
                    hkbop__vpzb = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                xmw__dkzs.append(True)
        yoreq__xpj = np.array(data)
        n = len(yoreq__xpj)
        lpr__xppel = n + 7 >> 3
        vlqf__eahy = np.empty(lpr__xppel, np.uint8)
        for iemcq__nvl in range(n):
            set_bit_to_arr(vlqf__eahy, iemcq__nvl, xmw__dkzs[iemcq__nvl])
        return init_integer_array(yoreq__xpj, vlqf__eahy)
    return impl_int_arr


def get_nullable_array_unary_impl(op, A):
    shh__ixapq = numba.core.registry.cpu_target.typing_context
    ouix__dddwc = shh__ixapq.resolve_function_type(op, (types.Array(A.dtype,
        1, 'C'),), {}).return_type
    ouix__dddwc = to_nullable_type(ouix__dddwc)

    def impl(A):
        n = len(A)
        jnzgu__zgt = bodo.utils.utils.alloc_type(n, ouix__dddwc, None)
        for i in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(jnzgu__zgt, i)
                continue
            jnzgu__zgt[i] = op(A[i])
        return jnzgu__zgt
    return impl


def get_nullable_array_binary_impl(op, lhs, rhs):
    inplace = (op in numba.core.typing.npydecl.
        NumpyRulesInplaceArrayOperator._op_map.keys())
    hmlbb__lbmv = isinstance(lhs, (types.Number, types.Boolean))
    igv__lglb = isinstance(rhs, (types.Number, types.Boolean))
    xozef__mbc = types.Array(getattr(lhs, 'dtype', lhs), 1, 'C')
    cbezb__kkpn = types.Array(getattr(rhs, 'dtype', rhs), 1, 'C')
    shh__ixapq = numba.core.registry.cpu_target.typing_context
    ouix__dddwc = shh__ixapq.resolve_function_type(op, (xozef__mbc,
        cbezb__kkpn), {}).return_type
    ouix__dddwc = to_nullable_type(ouix__dddwc)
    if op in (operator.truediv, operator.itruediv):
        op = np.true_divide
    elif op in (operator.floordiv, operator.ifloordiv):
        op = np.floor_divide
    avqj__qrvqs = 'lhs' if hmlbb__lbmv else 'lhs[i]'
    aqcbl__mxgen = 'rhs' if igv__lglb else 'rhs[i]'
    lenb__wloy = ('False' if hmlbb__lbmv else
        'bodo.libs.array_kernels.isna(lhs, i)')
    saf__slmk = ('False' if igv__lglb else
        'bodo.libs.array_kernels.isna(rhs, i)')
    aoaux__vzk = 'def impl(lhs, rhs):\n'
    aoaux__vzk += '  n = len({})\n'.format('lhs' if not hmlbb__lbmv else 'rhs')
    if inplace:
        aoaux__vzk += '  out_arr = {}\n'.format('lhs' if not hmlbb__lbmv else
            'rhs')
    else:
        aoaux__vzk += (
            '  out_arr = bodo.utils.utils.alloc_type(n, ret_dtype, None)\n')
    aoaux__vzk += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    aoaux__vzk += '    if ({}\n'.format(lenb__wloy)
    aoaux__vzk += '        or {}):\n'.format(saf__slmk)
    aoaux__vzk += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    aoaux__vzk += '      continue\n'
    aoaux__vzk += (
        '    out_arr[i] = bodo.utils.conversion.unbox_if_timestamp(op({}, {}))\n'
        .format(avqj__qrvqs, aqcbl__mxgen))
    aoaux__vzk += '  return out_arr\n'
    yith__rvlp = {}
    exec(aoaux__vzk, {'bodo': bodo, 'numba': numba, 'np': np, 'ret_dtype':
        ouix__dddwc, 'op': op}, yith__rvlp)
    impl = yith__rvlp['impl']
    return impl


def get_int_array_op_pd_td(op):

    def impl(lhs, rhs):
        hmlbb__lbmv = lhs in [pd_timedelta_type]
        igv__lglb = rhs in [pd_timedelta_type]
        if hmlbb__lbmv:

            def impl(lhs, rhs):
                n = len(rhs)
                jnzgu__zgt = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(jnzgu__zgt, i)
                        continue
                    jnzgu__zgt[i] = bodo.utils.conversion.unbox_if_timestamp(op
                        (lhs, rhs[i]))
                return jnzgu__zgt
            return impl
        elif igv__lglb:

            def impl(lhs, rhs):
                n = len(lhs)
                jnzgu__zgt = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(jnzgu__zgt, i)
                        continue
                    jnzgu__zgt[i] = bodo.utils.conversion.unbox_if_timestamp(op
                        (lhs[i], rhs))
                return jnzgu__zgt
            return impl
    return impl
