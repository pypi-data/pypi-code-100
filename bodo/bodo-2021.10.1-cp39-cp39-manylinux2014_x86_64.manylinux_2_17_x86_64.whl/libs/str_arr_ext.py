"""Array implementation for string objects, which are usually immutable.
The characters are stored in a contingous data array, and an offsets array marks the
the individual strings. For example:
value:             ['a', 'bc', '', 'abc', None, 'bb']
data:              [a, b, c, a, b, c, b, b]
offsets:           [0, 1, 3, 3, 6, 6, 8]
"""
import glob
import operator
import llvmlite.llvmpy.core as lc
import numba
import numba.core.typing.typeof
import numpy as np
import pandas as pd
from numba.core import cgutils, types
from numba.core.imputils import RefType, impl_ret_borrowed, iternext_impl, lower_constant
from numba.core.typing.templates import signature
from numba.core.unsafe.bytes import memcpy_region
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, type_callable, typeof_impl, unbox
import bodo
from bodo.libs.array_item_arr_ext import ArrayItemArrayPayloadType, ArrayItemArrayType, _get_array_item_arr_payload, np_offset_type, offset_type
from bodo.libs.binary_arr_ext import BinaryArrayType, binary_array_type, pre_alloc_binary_array
from bodo.libs.str_ext import memcmp, string_type, unicode_to_utf8_and_len
from bodo.utils.typing import BodoError, is_list_like_index_type, is_overload_constant_int, is_overload_none, is_overload_true, parse_dtype, raise_bodo_error
use_pd_string_array = False
char_type = types.uint8
char_arr_type = types.Array(char_type, 1, 'C')
offset_arr_type = types.Array(offset_type, 1, 'C')
null_bitmap_arr_type = types.Array(types.uint8, 1, 'C')
data_ctypes_type = types.ArrayCTypes(char_arr_type)
offset_ctypes_type = types.ArrayCTypes(offset_arr_type)


class StringArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self):
        super(StringArrayType, self).__init__(name='StringArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_type

    @property
    def iterator_type(self):
        return StringArrayIterator()

    def copy(self):
        return StringArrayType()


string_array_type = StringArrayType()


@typeof_impl.register(pd.arrays.StringArray)
def typeof_string_array(val, c):
    return string_array_type


@register_model(BinaryArrayType)
@register_model(StringArrayType)
class StringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ivp__pasz = ArrayItemArrayType(char_arr_type)
        xcbho__ayl = [('data', ivp__pasz)]
        models.StructModel.__init__(self, dmm, fe_type, xcbho__ayl)


make_attribute_wrapper(StringArrayType, 'data', '_data')
make_attribute_wrapper(BinaryArrayType, 'data', '_data')


@intrinsic
def init_str_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(char_type, 1, 'C')

    def codegen(context, builder, sig, args):
        faoem__azgtf, = args
        cvvyt__mqxk = context.make_helper(builder, string_array_type)
        cvvyt__mqxk.data = faoem__azgtf
        context.nrt.incref(builder, data_typ, faoem__azgtf)
        return cvvyt__mqxk._getvalue()
    return string_array_type(data_typ), codegen


class StringDtype(types.Number):

    def __init__(self):
        super(StringDtype, self).__init__('StringDtype')


string_dtype = StringDtype()
register_model(StringDtype)(models.OpaqueModel)


@box(StringDtype)
def box_string_dtype(typ, val, c):
    ctd__vrvr = c.context.insert_const_string(c.builder.module, 'pandas')
    klmqd__ofkz = c.pyapi.import_module_noblock(ctd__vrvr)
    tmgvw__tsgw = c.pyapi.call_method(klmqd__ofkz, 'StringDtype', ())
    c.pyapi.decref(klmqd__ofkz)
    return tmgvw__tsgw


@unbox(StringDtype)
def unbox_string_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.StringDtype)(lambda a, b: string_dtype)
type_callable(pd.StringDtype)(lambda c: lambda : string_dtype)
lower_builtin(pd.StringDtype)(lambda c, b, s, a: c.get_dummy_value())


def create_binary_op_overload(op):

    def overload_string_array_binary_op(lhs, rhs):
        if lhs == string_array_type and rhs == string_array_type:

            def impl_both(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tny__wvp = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(tny__wvp)
                for i in numba.parfors.parfor.internal_prange(tny__wvp):
                    if bodo.libs.array_kernels.isna(lhs, i
                        ) or bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs[i], rhs[i])
                    out_arr[i] = val
                return out_arr
            return impl_both
        if lhs == string_array_type and types.unliteral(rhs) == string_type:

            def impl_left(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tny__wvp = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(tny__wvp)
                for i in numba.parfors.parfor.internal_prange(tny__wvp):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs[i], rhs)
                    out_arr[i] = val
                return out_arr
            return impl_left
        if types.unliteral(lhs) == string_type and rhs == string_array_type:

            def impl_right(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tny__wvp = len(rhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(tny__wvp)
                for i in numba.parfors.parfor.internal_prange(tny__wvp):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs, rhs[i])
                    out_arr[i] = val
                return out_arr
            return impl_right
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_string_array_binary_op


def overload_add_operator_string_array(lhs, rhs):
    hntk__surr = lhs == string_array_type or isinstance(lhs, types.Array
        ) and lhs.dtype == string_type
    dzdsv__xxed = rhs == string_array_type or isinstance(rhs, types.Array
        ) and rhs.dtype == string_type
    if (lhs == string_array_type and dzdsv__xxed or hntk__surr and rhs ==
        string_array_type):

        def impl_both(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for hxmso__ydmoq in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, hxmso__ydmoq
                    ) or bodo.libs.array_kernels.isna(rhs, hxmso__ydmoq):
                    out_arr[hxmso__ydmoq] = ''
                    bodo.libs.array_kernels.setna(out_arr, hxmso__ydmoq)
                else:
                    out_arr[hxmso__ydmoq] = lhs[hxmso__ydmoq] + rhs[
                        hxmso__ydmoq]
            return out_arr
        return impl_both
    if lhs == string_array_type and types.unliteral(rhs) == string_type:

        def impl_left(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for hxmso__ydmoq in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, hxmso__ydmoq):
                    out_arr[hxmso__ydmoq] = ''
                    bodo.libs.array_kernels.setna(out_arr, hxmso__ydmoq)
                else:
                    out_arr[hxmso__ydmoq] = lhs[hxmso__ydmoq] + rhs
            return out_arr
        return impl_left
    if types.unliteral(lhs) == string_type and rhs == string_array_type:

        def impl_right(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(rhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for hxmso__ydmoq in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(rhs, hxmso__ydmoq):
                    out_arr[hxmso__ydmoq] = ''
                    bodo.libs.array_kernels.setna(out_arr, hxmso__ydmoq)
                else:
                    out_arr[hxmso__ydmoq] = lhs + rhs[hxmso__ydmoq]
            return out_arr
        return impl_right


def overload_mul_operator_str_arr(lhs, rhs):
    if lhs == string_array_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for hxmso__ydmoq in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, hxmso__ydmoq):
                    out_arr[hxmso__ydmoq] = ''
                    bodo.libs.array_kernels.setna(out_arr, hxmso__ydmoq)
                else:
                    out_arr[hxmso__ydmoq] = lhs[hxmso__ydmoq] * rhs
            return out_arr
        return impl
    if isinstance(lhs, types.Integer) and rhs == string_array_type:

        def impl(lhs, rhs):
            return rhs * lhs
        return impl


class StringArrayIterator(types.SimpleIteratorType):

    def __init__(self):
        wgqnh__xdcv = 'iter(String)'
        lvpd__otgbu = string_type
        super(StringArrayIterator, self).__init__(wgqnh__xdcv, lvpd__otgbu)


@register_model(StringArrayIterator)
class StrArrayIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        xcbho__ayl = [('index', types.EphemeralPointer(types.uintp)), (
            'array', string_array_type)]
        super(StrArrayIteratorModel, self).__init__(dmm, fe_type, xcbho__ayl)


lower_builtin('getiter', string_array_type)(numba.np.arrayobj.getiter_array)


@lower_builtin('iternext', StringArrayIterator)
@iternext_impl(RefType.NEW)
def iternext_str_array(context, builder, sig, args, result):
    [qyo__gnpt] = sig.args
    [vxbyq__xwjbv] = args
    lpt__zvu = context.make_helper(builder, qyo__gnpt, value=vxbyq__xwjbv)
    fbr__xfqin = signature(types.intp, string_array_type)
    vvhja__mbck = context.compile_internal(builder, lambda a: len(a),
        fbr__xfqin, [lpt__zvu.array])
    acp__cpsk = builder.load(lpt__zvu.index)
    rpcz__gvbyi = builder.icmp(lc.ICMP_SLT, acp__cpsk, vvhja__mbck)
    result.set_valid(rpcz__gvbyi)
    with builder.if_then(rpcz__gvbyi):
        knjn__otihz = signature(string_type, string_array_type, types.intp)
        value = context.compile_internal(builder, lambda a, i: a[i],
            knjn__otihz, [lpt__zvu.array, acp__cpsk])
        result.yield_(value)
        tdsh__pswpo = cgutils.increment_index(builder, acp__cpsk)
        builder.store(tdsh__pswpo, lpt__zvu.index)


def _get_str_binary_arr_payload(context, builder, arr_value, arr_typ):
    assert arr_typ == string_array_type or arr_typ == binary_array_type
    abgh__opgmg = context.make_helper(builder, arr_typ, arr_value)
    ivp__pasz = ArrayItemArrayType(char_arr_type)
    xnshf__ogk = _get_array_item_arr_payload(context, builder, ivp__pasz,
        abgh__opgmg.data)
    return xnshf__ogk


@intrinsic
def num_strings(typingctx, str_arr_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        xnshf__ogk = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        return xnshf__ogk.n_arrays
    return types.int64(string_array_type), codegen


def _get_num_total_chars(builder, offsets, num_strings):
    return builder.zext(builder.load(builder.gep(offsets, [num_strings])),
        lir.IntType(64))


@intrinsic
def num_total_chars(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        xnshf__ogk = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        ejom__uxkj = context.make_helper(builder, offset_arr_type,
            xnshf__ogk.offsets).data
        return _get_num_total_chars(builder, ejom__uxkj, xnshf__ogk.n_arrays)
    return types.uint64(in_arr_typ), codegen


@intrinsic
def get_offset_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        xnshf__ogk = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        rqngv__nogs = context.make_helper(builder, offset_arr_type,
            xnshf__ogk.offsets)
        cbaag__ymn = context.make_helper(builder, offset_ctypes_type)
        cbaag__ymn.data = builder.bitcast(rqngv__nogs.data, lir.IntType(
            offset_type.bitwidth).as_pointer())
        cbaag__ymn.meminfo = rqngv__nogs.meminfo
        tmgvw__tsgw = cbaag__ymn._getvalue()
        return impl_ret_borrowed(context, builder, offset_ctypes_type,
            tmgvw__tsgw)
    return offset_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        xnshf__ogk = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        faoem__azgtf = context.make_helper(builder, char_arr_type,
            xnshf__ogk.data)
        cbaag__ymn = context.make_helper(builder, data_ctypes_type)
        cbaag__ymn.data = faoem__azgtf.data
        cbaag__ymn.meminfo = faoem__azgtf.meminfo
        tmgvw__tsgw = cbaag__ymn._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type,
            tmgvw__tsgw)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr_ind(typingctx, in_arr_typ, int_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        vaym__lamxi, ind = args
        xnshf__ogk = _get_str_binary_arr_payload(context, builder,
            vaym__lamxi, sig.args[0])
        faoem__azgtf = context.make_helper(builder, char_arr_type,
            xnshf__ogk.data)
        cbaag__ymn = context.make_helper(builder, data_ctypes_type)
        cbaag__ymn.data = builder.gep(faoem__azgtf.data, [ind])
        cbaag__ymn.meminfo = faoem__azgtf.meminfo
        tmgvw__tsgw = cbaag__ymn._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type,
            tmgvw__tsgw)
    return data_ctypes_type(in_arr_typ, types.intp), codegen


@intrinsic
def copy_single_char(typingctx, dst_ptr_t, dst_ind_t, src_ptr_t, src_ind_t=None
    ):

    def codegen(context, builder, sig, args):
        nqgrh__trc, shbt__ahpmb, sagfa__qccie, ljax__zsk = args
        ruw__iomz = builder.bitcast(builder.gep(nqgrh__trc, [shbt__ahpmb]),
            lir.IntType(8).as_pointer())
        iuaug__lmaso = builder.bitcast(builder.gep(sagfa__qccie, [ljax__zsk
            ]), lir.IntType(8).as_pointer())
        bgfv__rjitc = builder.load(iuaug__lmaso)
        builder.store(bgfv__rjitc, ruw__iomz)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@intrinsic
def get_null_bitmap_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        xnshf__ogk = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        swng__wkioi = context.make_helper(builder, null_bitmap_arr_type,
            xnshf__ogk.null_bitmap)
        cbaag__ymn = context.make_helper(builder, data_ctypes_type)
        cbaag__ymn.data = swng__wkioi.data
        cbaag__ymn.meminfo = swng__wkioi.meminfo
        tmgvw__tsgw = cbaag__ymn._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type,
            tmgvw__tsgw)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def getitem_str_offset(typingctx, in_arr_typ, ind_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        xnshf__ogk = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        ejom__uxkj = context.make_helper(builder, offset_arr_type,
            xnshf__ogk.offsets).data
        return builder.load(builder.gep(ejom__uxkj, [ind]))
    return offset_type(in_arr_typ, ind_t), codegen


@intrinsic
def setitem_str_offset(typingctx, str_arr_typ, ind_t, val_t=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind, val = args
        xnshf__ogk = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, xnshf__ogk.
            offsets).data
        builder.store(val, builder.gep(offsets, [ind]))
        return context.get_dummy_value()
    return types.void(string_array_type, ind_t, offset_type), codegen


@intrinsic
def getitem_str_bitmap(typingctx, in_bitmap_typ, ind_t=None):

    def codegen(context, builder, sig, args):
        tem__omyrv, ind = args
        if in_bitmap_typ == data_ctypes_type:
            cbaag__ymn = context.make_helper(builder, data_ctypes_type,
                tem__omyrv)
            tem__omyrv = cbaag__ymn.data
        return builder.load(builder.gep(tem__omyrv, [ind]))
    return char_type(in_bitmap_typ, ind_t), codegen


@intrinsic
def setitem_str_bitmap(typingctx, in_bitmap_typ, ind_t, val_t=None):

    def codegen(context, builder, sig, args):
        tem__omyrv, ind, val = args
        if in_bitmap_typ == data_ctypes_type:
            cbaag__ymn = context.make_helper(builder, data_ctypes_type,
                tem__omyrv)
            tem__omyrv = cbaag__ymn.data
        builder.store(val, builder.gep(tem__omyrv, [ind]))
        return context.get_dummy_value()
    return types.void(in_bitmap_typ, ind_t, char_type), codegen


@intrinsic
def copy_str_arr_slice(typingctx, out_str_arr_typ, in_str_arr_typ, ind_t=None):
    assert out_str_arr_typ == string_array_type and in_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr, ind = args
        wgc__mopta = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        clhju__wdwf = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        zrrb__cdcj = context.make_helper(builder, offset_arr_type,
            wgc__mopta.offsets).data
        yox__ozjpm = context.make_helper(builder, offset_arr_type,
            clhju__wdwf.offsets).data
        qutz__whbyr = context.make_helper(builder, char_arr_type,
            wgc__mopta.data).data
        adl__yznih = context.make_helper(builder, char_arr_type,
            clhju__wdwf.data).data
        mqe__nfsft = context.make_helper(builder, null_bitmap_arr_type,
            wgc__mopta.null_bitmap).data
        tuqj__iooum = context.make_helper(builder, null_bitmap_arr_type,
            clhju__wdwf.null_bitmap).data
        jrajy__kqn = builder.add(ind, context.get_constant(types.intp, 1))
        cgutils.memcpy(builder, yox__ozjpm, zrrb__cdcj, jrajy__kqn)
        cgutils.memcpy(builder, adl__yznih, qutz__whbyr, builder.load(
            builder.gep(zrrb__cdcj, [ind])))
        fte__rfmhc = builder.add(ind, lir.Constant(lir.IntType(64), 7))
        cxvg__dhcrd = builder.lshr(fte__rfmhc, lir.Constant(lir.IntType(64), 3)
            )
        cgutils.memcpy(builder, tuqj__iooum, mqe__nfsft, cxvg__dhcrd)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type, ind_t), codegen


@intrinsic
def copy_data(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        wgc__mopta = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        clhju__wdwf = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        zrrb__cdcj = context.make_helper(builder, offset_arr_type,
            wgc__mopta.offsets).data
        qutz__whbyr = context.make_helper(builder, char_arr_type,
            wgc__mopta.data).data
        adl__yznih = context.make_helper(builder, char_arr_type,
            clhju__wdwf.data).data
        num_total_chars = _get_num_total_chars(builder, zrrb__cdcj,
            wgc__mopta.n_arrays)
        cgutils.memcpy(builder, adl__yznih, qutz__whbyr, num_total_chars)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def copy_non_null_offsets(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        wgc__mopta = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        clhju__wdwf = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        zrrb__cdcj = context.make_helper(builder, offset_arr_type,
            wgc__mopta.offsets).data
        yox__ozjpm = context.make_helper(builder, offset_arr_type,
            clhju__wdwf.offsets).data
        mqe__nfsft = context.make_helper(builder, null_bitmap_arr_type,
            wgc__mopta.null_bitmap).data
        tny__wvp = wgc__mopta.n_arrays
        xtss__edvjm = context.get_constant(offset_type, 0)
        brxxv__xnljp = cgutils.alloca_once_value(builder, xtss__edvjm)
        with cgutils.for_range(builder, tny__wvp) as loop:
            slez__nhijr = lower_is_na(context, builder, mqe__nfsft, loop.index)
            with cgutils.if_likely(builder, builder.not_(slez__nhijr)):
                oly__jpyud = builder.load(builder.gep(zrrb__cdcj, [loop.index])
                    )
                qre__awgt = builder.load(brxxv__xnljp)
                builder.store(oly__jpyud, builder.gep(yox__ozjpm, [qre__awgt]))
                builder.store(builder.add(qre__awgt, lir.Constant(context.
                    get_value_type(offset_type), 1)), brxxv__xnljp)
        qre__awgt = builder.load(brxxv__xnljp)
        oly__jpyud = builder.load(builder.gep(zrrb__cdcj, [tny__wvp]))
        builder.store(oly__jpyud, builder.gep(yox__ozjpm, [qre__awgt]))
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def str_copy(typingctx, buff_arr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        qjsql__sva, ind, str, ust__gfmn = args
        qjsql__sva = context.make_array(sig.args[0])(context, builder,
            qjsql__sva)
        ohla__geho = builder.gep(qjsql__sva.data, [ind])
        cgutils.raw_memcpy(builder, ohla__geho, str, ust__gfmn, 1)
        return context.get_dummy_value()
    return types.void(null_bitmap_arr_type, types.intp, types.voidptr,
        types.intp), codegen


@intrinsic
def str_copy_ptr(typingctx, ptr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        ohla__geho, ind, kbivn__qmpjz, ust__gfmn = args
        ohla__geho = builder.gep(ohla__geho, [ind])
        cgutils.raw_memcpy(builder, ohla__geho, kbivn__qmpjz, ust__gfmn, 1)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_length(A, i):
    return np.int64(getitem_str_offset(A, i + 1) - getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_ptr(A, i):
    return get_data_ptr_ind(A, getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_null_bools(str_arr):
    tny__wvp = len(str_arr)
    mssk__esaam = np.empty(tny__wvp, np.bool_)
    for i in range(tny__wvp):
        mssk__esaam[i] = bodo.libs.array_kernels.isna(str_arr, i)
    return mssk__esaam


def to_list_if_immutable_arr(arr, str_null_bools=None):
    return arr


@overload(to_list_if_immutable_arr, no_unliteral=True)
def to_list_if_immutable_arr_overload(data, str_null_bools=None):
    if data in [string_array_type, binary_array_type]:

        def to_list_impl(data, str_null_bools=None):
            tny__wvp = len(data)
            l = []
            for i in range(tny__wvp):
                l.append(data[i])
            return l
        return to_list_impl
    if isinstance(data, types.BaseTuple):
        osp__quicc = data.count
        skvrk__sre = ['to_list_if_immutable_arr(data[{}])'.format(i) for i in
            range(osp__quicc)]
        if is_overload_true(str_null_bools):
            skvrk__sre += ['get_str_null_bools(data[{}])'.format(i) for i in
                range(osp__quicc) if data.types[i] in [string_array_type,
                binary_array_type]]
        ozr__aivmu = 'def f(data, str_null_bools=None):\n'
        ozr__aivmu += '  return ({}{})\n'.format(', '.join(skvrk__sre), ',' if
            osp__quicc == 1 else '')
        pnemf__uhcck = {}
        exec(ozr__aivmu, {'to_list_if_immutable_arr':
            to_list_if_immutable_arr, 'get_str_null_bools':
            get_str_null_bools, 'bodo': bodo}, pnemf__uhcck)
        afbjm__yqxwn = pnemf__uhcck['f']
        return afbjm__yqxwn
    return lambda data, str_null_bools=None: data


def cp_str_list_to_array(str_arr, str_list, str_null_bools=None):
    return


@overload(cp_str_list_to_array, no_unliteral=True)
def cp_str_list_to_array_overload(str_arr, list_data, str_null_bools=None):
    if str_arr == string_array_type:
        if is_overload_none(str_null_bools):

            def cp_str_list_impl(str_arr, list_data, str_null_bools=None):
                tny__wvp = len(list_data)
                for i in range(tny__wvp):
                    kbivn__qmpjz = list_data[i]
                    str_arr[i] = kbivn__qmpjz
            return cp_str_list_impl
        else:

            def cp_str_list_impl_null(str_arr, list_data, str_null_bools=None):
                tny__wvp = len(list_data)
                for i in range(tny__wvp):
                    kbivn__qmpjz = list_data[i]
                    str_arr[i] = kbivn__qmpjz
                    if str_null_bools[i]:
                        str_arr_set_na(str_arr, i)
                    else:
                        str_arr_set_not_na(str_arr, i)
            return cp_str_list_impl_null
    if isinstance(str_arr, types.BaseTuple):
        osp__quicc = str_arr.count
        alame__wzwi = 0
        ozr__aivmu = 'def f(str_arr, list_data, str_null_bools=None):\n'
        for i in range(osp__quicc):
            if is_overload_true(str_null_bools) and str_arr.types[i
                ] == string_array_type:
                ozr__aivmu += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}], list_data[{}])\n'
                    .format(i, i, osp__quicc + alame__wzwi))
                alame__wzwi += 1
            else:
                ozr__aivmu += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}])\n'.
                    format(i, i))
        ozr__aivmu += '  return\n'
        pnemf__uhcck = {}
        exec(ozr__aivmu, {'cp_str_list_to_array': cp_str_list_to_array},
            pnemf__uhcck)
        yds__oiev = pnemf__uhcck['f']
        return yds__oiev
    return lambda str_arr, list_data, str_null_bools=None: None


def str_list_to_array(str_list):
    return str_list


@overload(str_list_to_array, no_unliteral=True)
def str_list_to_array_overload(str_list):
    if isinstance(str_list, types.List) and str_list.dtype == bodo.string_type:

        def str_list_impl(str_list):
            tny__wvp = len(str_list)
            str_arr = pre_alloc_string_array(tny__wvp, -1)
            for i in range(tny__wvp):
                kbivn__qmpjz = str_list[i]
                str_arr[i] = kbivn__qmpjz
            return str_arr
        return str_list_impl
    return lambda str_list: str_list


def get_num_total_chars(A):
    pass


@overload(get_num_total_chars)
def overload_get_num_total_chars(A):
    if isinstance(A, types.List) and A.dtype == string_type:

        def str_list_impl(A):
            tny__wvp = len(A)
            toctx__puvk = 0
            for i in range(tny__wvp):
                kbivn__qmpjz = A[i]
                toctx__puvk += get_utf8_size(kbivn__qmpjz)
            return toctx__puvk
        return str_list_impl
    assert A == string_array_type
    return lambda A: num_total_chars(A)


@overload_method(StringArrayType, 'copy', no_unliteral=True)
def str_arr_copy_overload(arr):

    def copy_impl(arr):
        tny__wvp = len(arr)
        n_chars = num_total_chars(arr)
        jti__fxqd = pre_alloc_string_array(tny__wvp, np.int64(n_chars))
        copy_str_arr_slice(jti__fxqd, arr, tny__wvp)
        return jti__fxqd
    return copy_impl


@overload(len, no_unliteral=True)
def str_arr_len_overload(str_arr):
    if str_arr == string_array_type:

        def str_arr_len(str_arr):
            return str_arr.size
        return str_arr_len


@overload_attribute(StringArrayType, 'size')
def str_arr_size_overload(str_arr):
    return lambda str_arr: len(str_arr._data)


@overload_attribute(StringArrayType, 'shape')
def str_arr_shape_overload(str_arr):
    return lambda str_arr: (str_arr.size,)


@overload_attribute(StringArrayType, 'nbytes')
def str_arr_nbytes_overload(str_arr):
    return lambda str_arr: str_arr._data.nbytes


@overload_method(types.Array, 'tolist', no_unliteral=True)
@overload_method(StringArrayType, 'tolist', no_unliteral=True)
def overload_to_list(arr):
    return lambda arr: list(arr)


import llvmlite.binding as ll
from llvmlite import ir as lir
from bodo.libs import array_ext, hstr_ext
ll.add_symbol('get_str_len', hstr_ext.get_str_len)
ll.add_symbol('setitem_string_array', hstr_ext.setitem_string_array)
ll.add_symbol('is_na', hstr_ext.is_na)
ll.add_symbol('string_array_from_sequence', array_ext.
    string_array_from_sequence)
ll.add_symbol('pd_array_from_string_array', hstr_ext.pd_array_from_string_array
    )
ll.add_symbol('np_array_from_string_array', hstr_ext.np_array_from_string_array
    )
ll.add_symbol('convert_len_arr_to_offset32', hstr_ext.
    convert_len_arr_to_offset32)
ll.add_symbol('convert_len_arr_to_offset', hstr_ext.convert_len_arr_to_offset)
ll.add_symbol('set_string_array_range', hstr_ext.set_string_array_range)
ll.add_symbol('str_arr_to_int64', hstr_ext.str_arr_to_int64)
ll.add_symbol('str_arr_to_float64', hstr_ext.str_arr_to_float64)
ll.add_symbol('get_utf8_size', hstr_ext.get_utf8_size)
ll.add_symbol('print_str_arr', hstr_ext.print_str_arr)
ll.add_symbol('inplace_int64_to_str', hstr_ext.inplace_int64_to_str)
inplace_int64_to_str = types.ExternalFunction('inplace_int64_to_str', types
    .void(types.voidptr, types.int64, types.int64))
convert_len_arr_to_offset32 = types.ExternalFunction(
    'convert_len_arr_to_offset32', types.void(types.voidptr, types.intp))
convert_len_arr_to_offset = types.ExternalFunction('convert_len_arr_to_offset',
    types.void(types.voidptr, types.voidptr, types.intp))
setitem_string_array = types.ExternalFunction('setitem_string_array', types
    .void(types.CPointer(offset_type), types.CPointer(char_type), types.
    uint64, types.voidptr, types.intp, offset_type, offset_type, types.intp))
_get_utf8_size = types.ExternalFunction('get_utf8_size', types.intp(types.
    voidptr, types.intp, offset_type))
_print_str_arr = types.ExternalFunction('print_str_arr', types.void(types.
    uint64, types.uint64, types.CPointer(offset_type), types.CPointer(
    char_type)))


@numba.generated_jit(nopython=True)
def str_arr_from_sequence(in_seq):
    if in_seq.dtype == bodo.bytes_type:
        zbui__cyotg = 'pre_alloc_binary_array'
    else:
        zbui__cyotg = 'pre_alloc_string_array'
    ozr__aivmu = 'def f(in_seq):\n'
    ozr__aivmu += '    n_strs = len(in_seq)\n'
    ozr__aivmu += f'    A = {zbui__cyotg}(n_strs, -1)\n'
    ozr__aivmu += '    for i in range(n_strs):\n'
    ozr__aivmu += '        A[i] = in_seq[i]\n'
    ozr__aivmu += '    return A\n'
    pnemf__uhcck = {}
    exec(ozr__aivmu, {'pre_alloc_string_array': pre_alloc_string_array,
        'pre_alloc_binary_array': pre_alloc_binary_array}, pnemf__uhcck)
    pjfw__qxuf = pnemf__uhcck['f']
    return pjfw__qxuf


@intrinsic
def set_all_offsets_to_0(typingctx, arr_typ=None):
    assert arr_typ in [string_array_type, binary_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        xnshf__ogk = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        ucx__xycok = builder.add(xnshf__ogk.n_arrays, lir.Constant(lir.
            IntType(64), 1))
        shya__dif = builder.lshr(lir.Constant(lir.IntType(64), offset_type.
            bitwidth), lir.Constant(lir.IntType(64), 3))
        cxvg__dhcrd = builder.mul(ucx__xycok, shya__dif)
        yfnkq__rvrxv = context.make_array(offset_arr_type)(context, builder,
            xnshf__ogk.offsets).data
        cgutils.memset(builder, yfnkq__rvrxv, cxvg__dhcrd, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@numba.njit
def pre_alloc_string_array(n_strs, n_chars):
    if n_chars is None:
        n_chars = -1
    str_arr = init_str_arr(bodo.libs.array_item_arr_ext.
        pre_alloc_array_item_array(np.int64(n_strs), (np.int64(n_chars),),
        char_arr_type))
    if n_chars == 0:
        set_all_offsets_to_0(str_arr)
    return str_arr


kBitmask = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)


@numba.njit
def set_bit_to(bits, i, bit_is_set):
    nmfhq__rto = i // 8
    atqb__win = getitem_str_bitmap(bits, nmfhq__rto)
    atqb__win ^= np.uint8(-np.uint8(bit_is_set) ^ atqb__win) & kBitmask[i % 8]
    setitem_str_bitmap(bits, nmfhq__rto, atqb__win)


@numba.njit
def get_bit_bitmap(bits, i):
    return getitem_str_bitmap(bits, i >> 3) >> (i & 7) & 1


@numba.njit
def copy_nulls_range(out_str_arr, in_str_arr, out_start):
    ikx__pede = get_null_bitmap_ptr(out_str_arr)
    ihxr__oxapu = get_null_bitmap_ptr(in_str_arr)
    for hxmso__ydmoq in range(len(in_str_arr)):
        zuvi__xukpx = get_bit_bitmap(ihxr__oxapu, hxmso__ydmoq)
        set_bit_to(ikx__pede, out_start + hxmso__ydmoq, zuvi__xukpx)


@intrinsic
def set_string_array_range(typingctx, out_typ, in_typ, curr_str_typ,
    curr_chars_typ=None):
    assert out_typ == string_array_type and in_typ == string_array_type or out_typ == binary_array_type and in_typ == binary_array_type
    assert curr_str_typ == types.intp and curr_chars_typ == types.intp

    def codegen(context, builder, sig, args):
        out_arr, vaym__lamxi, pyk__wubq, mnm__biorg = args
        wgc__mopta = _get_str_binary_arr_payload(context, builder,
            vaym__lamxi, string_array_type)
        clhju__wdwf = _get_str_binary_arr_payload(context, builder, out_arr,
            string_array_type)
        zrrb__cdcj = context.make_helper(builder, offset_arr_type,
            wgc__mopta.offsets).data
        yox__ozjpm = context.make_helper(builder, offset_arr_type,
            clhju__wdwf.offsets).data
        qutz__whbyr = context.make_helper(builder, char_arr_type,
            wgc__mopta.data).data
        adl__yznih = context.make_helper(builder, char_arr_type,
            clhju__wdwf.data).data
        num_total_chars = _get_num_total_chars(builder, zrrb__cdcj,
            wgc__mopta.n_arrays)
        kan__dfe = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(64), lir.IntType(64),
            lir.IntType(64)])
        uoul__xxht = cgutils.get_or_insert_function(builder.module,
            kan__dfe, name='set_string_array_range')
        builder.call(uoul__xxht, [yox__ozjpm, adl__yznih, zrrb__cdcj,
            qutz__whbyr, pyk__wubq, mnm__biorg, wgc__mopta.n_arrays,
            num_total_chars])
        mzr__pabg = context.typing_context.resolve_value_type(copy_nulls_range)
        qqsi__aqcv = mzr__pabg.get_call_type(context.typing_context, (
            string_array_type, string_array_type, types.int64), {})
        sfsmi__ztq = context.get_function(mzr__pabg, qqsi__aqcv)
        sfsmi__ztq(builder, (out_arr, vaym__lamxi, pyk__wubq))
        return context.get_dummy_value()
    sig = types.void(out_typ, in_typ, types.intp, types.intp)
    return sig, codegen


@box(BinaryArrayType)
@box(StringArrayType)
def box_str_arr(typ, val, c):
    assert typ in [binary_array_type, string_array_type]
    zjcqz__szrdm = c.context.make_helper(c.builder, typ, val)
    ivp__pasz = ArrayItemArrayType(char_arr_type)
    xnshf__ogk = _get_array_item_arr_payload(c.context, c.builder,
        ivp__pasz, zjcqz__szrdm.data)
    sedx__gqeai = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    axvtm__qdg = 'np_array_from_string_array'
    if use_pd_string_array and typ != binary_array_type:
        axvtm__qdg = 'pd_array_from_string_array'
    kan__dfe = lir.FunctionType(c.context.get_argument_type(types.pyobject),
        [lir.IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
        lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
        IntType(32)])
    pujai__vvosf = cgutils.get_or_insert_function(c.builder.module,
        kan__dfe, name=axvtm__qdg)
    ejom__uxkj = c.context.make_array(offset_arr_type)(c.context, c.builder,
        xnshf__ogk.offsets).data
    qlhen__ohzgq = c.context.make_array(char_arr_type)(c.context, c.builder,
        xnshf__ogk.data).data
    wyxkk__sipg = c.context.make_array(null_bitmap_arr_type)(c.context, c.
        builder, xnshf__ogk.null_bitmap).data
    arr = c.builder.call(pujai__vvosf, [xnshf__ogk.n_arrays, ejom__uxkj,
        qlhen__ohzgq, wyxkk__sipg, sedx__gqeai])
    c.context.nrt.decref(c.builder, typ, val)
    return arr


@intrinsic
def str_arr_is_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        xnshf__ogk = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        wyxkk__sipg = context.make_array(null_bitmap_arr_type)(context,
            builder, xnshf__ogk.null_bitmap).data
        rgoh__mduxv = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        unsmk__dsf = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        atqb__win = builder.load(builder.gep(wyxkk__sipg, [rgoh__mduxv],
            inbounds=True))
        kbts__jydl = lir.ArrayType(lir.IntType(8), 8)
        tumc__mwfcc = cgutils.alloca_once_value(builder, lir.Constant(
            kbts__jydl, (1, 2, 4, 8, 16, 32, 64, 128)))
        pfhpd__szbb = builder.load(builder.gep(tumc__mwfcc, [lir.Constant(
            lir.IntType(64), 0), unsmk__dsf], inbounds=True))
        return builder.icmp_unsigned('==', builder.and_(atqb__win,
            pfhpd__szbb), lir.Constant(lir.IntType(8), 0))
    return types.bool_(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        xnshf__ogk = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        rgoh__mduxv = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        unsmk__dsf = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        wyxkk__sipg = context.make_array(null_bitmap_arr_type)(context,
            builder, xnshf__ogk.null_bitmap).data
        offsets = context.make_helper(builder, offset_arr_type, xnshf__ogk.
            offsets).data
        oxyox__zhsgt = builder.gep(wyxkk__sipg, [rgoh__mduxv], inbounds=True)
        atqb__win = builder.load(oxyox__zhsgt)
        kbts__jydl = lir.ArrayType(lir.IntType(8), 8)
        tumc__mwfcc = cgutils.alloca_once_value(builder, lir.Constant(
            kbts__jydl, (1, 2, 4, 8, 16, 32, 64, 128)))
        pfhpd__szbb = builder.load(builder.gep(tumc__mwfcc, [lir.Constant(
            lir.IntType(64), 0), unsmk__dsf], inbounds=True))
        pfhpd__szbb = builder.xor(pfhpd__szbb, lir.Constant(lir.IntType(8), -1)
            )
        builder.store(builder.and_(atqb__win, pfhpd__szbb), oxyox__zhsgt)
        if str_arr_typ == string_array_type:
            qdzf__sya = builder.add(ind, lir.Constant(lir.IntType(64), 1))
            jgyz__fbpp = builder.icmp_unsigned('!=', qdzf__sya, xnshf__ogk.
                n_arrays)
            with builder.if_then(jgyz__fbpp):
                builder.store(builder.load(builder.gep(offsets, [ind])),
                    builder.gep(offsets, [qdzf__sya]))
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_not_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        xnshf__ogk = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        rgoh__mduxv = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        unsmk__dsf = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        wyxkk__sipg = context.make_array(null_bitmap_arr_type)(context,
            builder, xnshf__ogk.null_bitmap).data
        oxyox__zhsgt = builder.gep(wyxkk__sipg, [rgoh__mduxv], inbounds=True)
        atqb__win = builder.load(oxyox__zhsgt)
        kbts__jydl = lir.ArrayType(lir.IntType(8), 8)
        tumc__mwfcc = cgutils.alloca_once_value(builder, lir.Constant(
            kbts__jydl, (1, 2, 4, 8, 16, 32, 64, 128)))
        pfhpd__szbb = builder.load(builder.gep(tumc__mwfcc, [lir.Constant(
            lir.IntType(64), 0), unsmk__dsf], inbounds=True))
        builder.store(builder.or_(atqb__win, pfhpd__szbb), oxyox__zhsgt)
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def set_null_bits_to_value(typingctx, arr_typ, value_typ=None):
    assert (arr_typ == string_array_type or arr_typ == binary_array_type
        ) and is_overload_constant_int(value_typ)

    def codegen(context, builder, sig, args):
        in_str_arr, value = args
        xnshf__ogk = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        cxvg__dhcrd = builder.udiv(builder.add(xnshf__ogk.n_arrays, lir.
            Constant(lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
        wyxkk__sipg = context.make_array(null_bitmap_arr_type)(context,
            builder, xnshf__ogk.null_bitmap).data
        cgutils.memset(builder, wyxkk__sipg, cxvg__dhcrd, value)
        return context.get_dummy_value()
    return types.none(arr_typ, types.int8), codegen


def _get_str_binary_arr_data_payload_ptr(context, builder, str_arr):
    dnki__oakqc = context.make_helper(builder, string_array_type, str_arr)
    ivp__pasz = ArrayItemArrayType(char_arr_type)
    wpiw__jmbcm = context.make_helper(builder, ivp__pasz, dnki__oakqc.data)
    simd__jaoq = ArrayItemArrayPayloadType(ivp__pasz)
    sor__ygz = context.nrt.meminfo_data(builder, wpiw__jmbcm.meminfo)
    fjjmw__ciwc = builder.bitcast(sor__ygz, context.get_value_type(
        simd__jaoq).as_pointer())
    return fjjmw__ciwc


@intrinsic
def move_str_binary_arr_payload(typingctx, to_arr_typ, from_arr_typ=None):
    assert to_arr_typ == string_array_type and from_arr_typ == string_array_type or to_arr_typ == binary_array_type and from_arr_typ == binary_array_type

    def codegen(context, builder, sig, args):
        qnjak__jxbrd, hcda__kenh = args
        vnjoh__dgz = _get_str_binary_arr_data_payload_ptr(context, builder,
            hcda__kenh)
        cnrp__eta = _get_str_binary_arr_data_payload_ptr(context, builder,
            qnjak__jxbrd)
        urvcd__nvles = _get_str_binary_arr_payload(context, builder,
            hcda__kenh, sig.args[1])
        fgdkk__szr = _get_str_binary_arr_payload(context, builder,
            qnjak__jxbrd, sig.args[0])
        context.nrt.incref(builder, char_arr_type, urvcd__nvles.data)
        context.nrt.incref(builder, offset_arr_type, urvcd__nvles.offsets)
        context.nrt.incref(builder, null_bitmap_arr_type, urvcd__nvles.
            null_bitmap)
        context.nrt.decref(builder, char_arr_type, fgdkk__szr.data)
        context.nrt.decref(builder, offset_arr_type, fgdkk__szr.offsets)
        context.nrt.decref(builder, null_bitmap_arr_type, fgdkk__szr.
            null_bitmap)
        builder.store(builder.load(vnjoh__dgz), cnrp__eta)
        return context.get_dummy_value()
    return types.none(to_arr_typ, from_arr_typ), codegen


dummy_use = numba.njit(lambda a: None)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_utf8_size(s):
    if isinstance(s, types.StringLiteral):
        l = len(s.literal_value.encode())
        return lambda s: l

    def impl(s):
        if s is None:
            return 0
        s = bodo.utils.indexing.unoptional(s)
        if s._is_ascii == 1:
            return len(s)
        tny__wvp = _get_utf8_size(s._data, s._length, s._kind)
        dummy_use(s)
        return tny__wvp
    return impl


@intrinsic
def setitem_str_arr_ptr(typingctx, str_arr_t, ind_t, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        arr, ind, ohla__geho, bkoy__iuzar = args
        xnshf__ogk = _get_str_binary_arr_payload(context, builder, arr, sig
            .args[0])
        offsets = context.make_helper(builder, offset_arr_type, xnshf__ogk.
            offsets).data
        data = context.make_helper(builder, char_arr_type, xnshf__ogk.data
            ).data
        kan__dfe = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64),
            lir.IntType(32), lir.IntType(32), lir.IntType(64)])
        rzvio__udhd = cgutils.get_or_insert_function(builder.module,
            kan__dfe, name='setitem_string_array')
        mzff__iyp = context.get_constant(types.int32, -1)
        mgmxv__qlpb = context.get_constant(types.int32, 1)
        num_total_chars = _get_num_total_chars(builder, offsets, xnshf__ogk
            .n_arrays)
        builder.call(rzvio__udhd, [offsets, data, num_total_chars, builder.
            extract_value(ohla__geho, 0), bkoy__iuzar, mzff__iyp,
            mgmxv__qlpb, ind])
        return context.get_dummy_value()
    return types.void(str_arr_t, ind_t, ptr_t, len_t), codegen


def lower_is_na(context, builder, bull_bitmap, ind):
    kan__dfe = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer(
        ), lir.IntType(64)])
    inxa__ygwr = cgutils.get_or_insert_function(builder.module, kan__dfe,
        name='is_na')
    return builder.call(inxa__ygwr, [bull_bitmap, ind])


@intrinsic
def _memcpy(typingctx, dest_t, src_t, count_t, item_size_t=None):

    def codegen(context, builder, sig, args):
        ruw__iomz, iuaug__lmaso, osp__quicc, mhf__zeune = args
        cgutils.raw_memcpy(builder, ruw__iomz, iuaug__lmaso, osp__quicc,
            mhf__zeune)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.voidptr, types.intp, types.intp
        ), codegen


@numba.njit
def print_str_arr(arr):
    _print_str_arr(num_strings(arr), num_total_chars(arr), get_offset_ptr(
        arr), get_data_ptr(arr))


def inplace_eq(A, i, val):
    return A[i] == val


@overload(inplace_eq)
def inplace_eq_overload(A, ind, val):

    def impl(A, ind, val):
        xpzdh__zyyo, rcd__nvfp = unicode_to_utf8_and_len(val)
        eagu__kks = getitem_str_offset(A, ind)
        vbizl__hnzmf = getitem_str_offset(A, ind + 1)
        add__hllx = vbizl__hnzmf - eagu__kks
        if add__hllx != rcd__nvfp:
            return False
        ohla__geho = get_data_ptr_ind(A, eagu__kks)
        return memcmp(ohla__geho, xpzdh__zyyo, rcd__nvfp) == 0
    return impl


def str_arr_setitem_int_to_str(A, ind, value):
    A[ind] = str(value)


@overload(str_arr_setitem_int_to_str)
def overload_str_arr_setitem_int_to_str(A, ind, val):

    def impl(A, ind, val):
        eagu__kks = getitem_str_offset(A, ind)
        add__hllx = bodo.libs.str_ext.int_to_str_len(val)
        hnjni__lmd = eagu__kks + add__hllx
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            eagu__kks, hnjni__lmd)
        ohla__geho = get_data_ptr_ind(A, eagu__kks)
        inplace_int64_to_str(ohla__geho, add__hllx, val)
        setitem_str_offset(A, ind + 1, eagu__kks + add__hllx)
        str_arr_set_not_na(A, ind)
    return impl


@intrinsic
def inplace_set_NA_str(typingctx, ptr_typ=None):

    def codegen(context, builder, sig, args):
        ohla__geho, = args
        zlrl__wizib = context.insert_const_string(builder.module, '<NA>')
        wjb__ubk = lir.Constant(lir.IntType(64), len('<NA>'))
        cgutils.raw_memcpy(builder, ohla__geho, zlrl__wizib, wjb__ubk, 1)
    return types.none(types.voidptr), codegen


def str_arr_setitem_NA_str(A, ind):
    A[ind] = '<NA>'


@overload(str_arr_setitem_NA_str)
def overload_str_arr_setitem_NA_str(A, ind):
    hqqxj__zbt = len('<NA>')

    def impl(A, ind):
        eagu__kks = getitem_str_offset(A, ind)
        hnjni__lmd = eagu__kks + hqqxj__zbt
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            eagu__kks, hnjni__lmd)
        ohla__geho = get_data_ptr_ind(A, eagu__kks)
        inplace_set_NA_str(ohla__geho)
        setitem_str_offset(A, ind + 1, eagu__kks + hqqxj__zbt)
        str_arr_set_not_na(A, ind)
    return impl


@overload(operator.getitem, no_unliteral=True)
def str_arr_getitem_int(A, ind):
    if A != string_array_type:
        return
    if isinstance(ind, types.Integer):

        def str_arr_getitem_impl(A, ind):
            if ind < 0:
                ind += A.size
            eagu__kks = getitem_str_offset(A, ind)
            vbizl__hnzmf = getitem_str_offset(A, ind + 1)
            bkoy__iuzar = vbizl__hnzmf - eagu__kks
            ohla__geho = get_data_ptr_ind(A, eagu__kks)
            vhfd__rzao = decode_utf8(ohla__geho, bkoy__iuzar)
            return vhfd__rzao
        return str_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def bool_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_ndarray(ind)
            tny__wvp = len(A)
            n_strs = 0
            n_chars = 0
            for i in range(tny__wvp):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    n_strs += 1
                    n_chars += get_str_arr_item_length(A, i)
            out_arr = pre_alloc_string_array(n_strs, n_chars)
            ykzd__wxgh = get_data_ptr(out_arr).data
            dclv__fhi = get_data_ptr(A).data
            alame__wzwi = 0
            qre__awgt = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(tny__wvp):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    cjzd__ovw = get_str_arr_item_length(A, i)
                    if cjzd__ovw == 1:
                        copy_single_char(ykzd__wxgh, qre__awgt, dclv__fhi,
                            getitem_str_offset(A, i))
                    else:
                        memcpy_region(ykzd__wxgh, qre__awgt, dclv__fhi,
                            getitem_str_offset(A, i), cjzd__ovw, 1)
                    qre__awgt += cjzd__ovw
                    setitem_str_offset(out_arr, alame__wzwi + 1, qre__awgt)
                    if str_arr_is_na(A, i):
                        str_arr_set_na(out_arr, alame__wzwi)
                    else:
                        str_arr_set_not_na(out_arr, alame__wzwi)
                    alame__wzwi += 1
            return out_arr
        return bool_impl
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def str_arr_arr_impl(A, ind):
            tny__wvp = len(ind)
            out_arr = pre_alloc_string_array(tny__wvp, -1)
            alame__wzwi = 0
            for i in range(tny__wvp):
                kbivn__qmpjz = A[ind[i]]
                out_arr[alame__wzwi] = kbivn__qmpjz
                if str_arr_is_na(A, ind[i]):
                    str_arr_set_na(out_arr, alame__wzwi)
                alame__wzwi += 1
            return out_arr
        return str_arr_arr_impl
    if isinstance(ind, types.SliceType):

        def str_arr_slice_impl(A, ind):
            tny__wvp = len(A)
            zuabv__ckwix = numba.cpython.unicode._normalize_slice(ind, tny__wvp
                )
            zzpuh__bncrr = numba.cpython.unicode._slice_span(zuabv__ckwix)
            if zuabv__ckwix.step == 1:
                eagu__kks = getitem_str_offset(A, zuabv__ckwix.start)
                vbizl__hnzmf = getitem_str_offset(A, zuabv__ckwix.stop)
                n_chars = vbizl__hnzmf - eagu__kks
                jti__fxqd = pre_alloc_string_array(zzpuh__bncrr, np.int64(
                    n_chars))
                for i in range(zzpuh__bncrr):
                    jti__fxqd[i] = A[zuabv__ckwix.start + i]
                    if str_arr_is_na(A, zuabv__ckwix.start + i):
                        str_arr_set_na(jti__fxqd, i)
                return jti__fxqd
            else:
                jti__fxqd = pre_alloc_string_array(zzpuh__bncrr, -1)
                for i in range(zzpuh__bncrr):
                    jti__fxqd[i] = A[zuabv__ckwix.start + i * zuabv__ckwix.step
                        ]
                    if str_arr_is_na(A, zuabv__ckwix.start + i *
                        zuabv__ckwix.step):
                        str_arr_set_na(jti__fxqd, i)
                return jti__fxqd
        return str_arr_slice_impl
    raise BodoError(
        f'getitem for StringArray with indexing type {ind} not supported.')


dummy_use = numba.njit(lambda a: None)


@overload(operator.setitem)
def str_arr_setitem(A, idx, val):
    if A != string_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    zhde__pqdg = (
        f'StringArray setitem with index {idx} and value {val} not supported yet.'
        )
    if isinstance(idx, types.Integer):
        if val != string_type:
            raise BodoError(zhde__pqdg)
        jiyo__qijqc = 4

        def impl_scalar(A, idx, val):
            duxrf__rwxw = (val._length if val._is_ascii else jiyo__qijqc *
                val._length)
            faoem__azgtf = A._data
            eagu__kks = np.int64(getitem_str_offset(A, idx))
            hnjni__lmd = eagu__kks + duxrf__rwxw
            bodo.libs.array_item_arr_ext.ensure_data_capacity(faoem__azgtf,
                eagu__kks, hnjni__lmd)
            setitem_string_array(get_offset_ptr(A), get_data_ptr(A),
                hnjni__lmd, val._data, val._length, val._kind, val.
                _is_ascii, idx)
            str_arr_set_not_na(A, idx)
            dummy_use(A)
            dummy_use(val)
        return impl_scalar
    if isinstance(idx, types.SliceType):
        if val == string_array_type:

            def impl_slice(A, idx, val):
                zuabv__ckwix = numba.cpython.unicode._normalize_slice(idx,
                    len(A))
                pftva__lgmql = zuabv__ckwix.start
                faoem__azgtf = A._data
                eagu__kks = np.int64(getitem_str_offset(A, pftva__lgmql))
                hnjni__lmd = eagu__kks + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(faoem__azgtf,
                    eagu__kks, hnjni__lmd)
                set_string_array_range(A, val, pftva__lgmql, eagu__kks)
                pki__kek = 0
                for i in range(zuabv__ckwix.start, zuabv__ckwix.stop,
                    zuabv__ckwix.step):
                    if str_arr_is_na(val, pki__kek):
                        str_arr_set_na(A, i)
                    else:
                        str_arr_set_not_na(A, i)
                    pki__kek += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == string_type:

            def impl_slice_list(A, idx, val):
                qhr__uuwu = str_list_to_array(val)
                A[idx] = qhr__uuwu
            return impl_slice_list
        elif val == string_type:

            def impl_slice(A, idx, val):
                zuabv__ckwix = numba.cpython.unicode._normalize_slice(idx,
                    len(A))
                for i in range(zuabv__ckwix.start, zuabv__ckwix.stop,
                    zuabv__ckwix.step):
                    A[i] = val
            return impl_slice
        else:
            raise BodoError(zhde__pqdg)
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if val == string_type:

            def impl_bool_scalar(A, idx, val):
                tny__wvp = len(A)
                idx = bodo.utils.conversion.coerce_to_ndarray(idx)
                out_arr = pre_alloc_string_array(tny__wvp, -1)
                for i in numba.parfors.parfor.internal_prange(tny__wvp):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        out_arr[i] = val
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        out_arr[i] = A[i]
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_scalar
        elif val == string_array_type or isinstance(val, types.Array
            ) and isinstance(val.dtype, types.UnicodeCharSeq):

            def impl_bool_arr(A, idx, val):
                tny__wvp = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx,
                    use_nullable_array=True)
                out_arr = pre_alloc_string_array(tny__wvp, -1)
                xfwho__vrfdj = 0
                for i in numba.parfors.parfor.internal_prange(tny__wvp):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        if bodo.libs.array_kernels.isna(val, xfwho__vrfdj):
                            out_arr[i] = ''
                            str_arr_set_na(out_arr, xfwho__vrfdj)
                        else:
                            out_arr[i] = str(val[xfwho__vrfdj])
                        xfwho__vrfdj += 1
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        out_arr[i] = A[i]
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_arr
        else:
            raise BodoError(zhde__pqdg)
    raise BodoError(zhde__pqdg)


@overload_attribute(StringArrayType, 'dtype')
def overload_str_arr_dtype(A):
    return lambda A: pd.StringDtype()


@overload_attribute(StringArrayType, 'ndim')
def overload_str_arr_ndim(A):
    return lambda A: 1


@overload_method(StringArrayType, 'astype', no_unliteral=True)
def overload_str_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "StringArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if isinstance(dtype, types.Function) and dtype.key[0] == str:
        return lambda A, dtype, copy=True: A
    pmkw__riylx = parse_dtype(dtype, 'StringArray.astype')
    if not isinstance(pmkw__riylx, (types.Float, types.Integer)):
        raise BodoError('invalid dtype in StringArray.astype()')
    if isinstance(pmkw__riylx, types.Float):

        def impl_float(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            tny__wvp = len(A)
            nleez__fnmuj = np.empty(tny__wvp, pmkw__riylx)
            for i in numba.parfors.parfor.internal_prange(tny__wvp):
                if bodo.libs.array_kernels.isna(A, i):
                    nleez__fnmuj[i] = np.nan
                else:
                    nleez__fnmuj[i] = float(A[i])
            return nleez__fnmuj
        return impl_float
    else:

        def impl_int(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            tny__wvp = len(A)
            nleez__fnmuj = np.empty(tny__wvp, pmkw__riylx)
            for i in numba.parfors.parfor.internal_prange(tny__wvp):
                nleez__fnmuj[i] = int(A[i])
            return nleez__fnmuj
        return impl_int


@intrinsic
def decode_utf8(typingctx, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        ohla__geho, bkoy__iuzar = args
        ltrk__voql = context.get_python_api(builder)
        jtv__aung = ltrk__voql.string_from_string_and_size(ohla__geho,
            bkoy__iuzar)
        fyahu__zvp = ltrk__voql.to_native_value(string_type, jtv__aung).value
        ikek__sjfsn = cgutils.create_struct_proxy(string_type)(context,
            builder, fyahu__zvp)
        ikek__sjfsn.hash = ikek__sjfsn.hash.type(-1)
        ltrk__voql.decref(jtv__aung)
        return ikek__sjfsn._getvalue()
    return string_type(types.voidptr, types.intp), codegen


def get_arr_data_ptr(arr, ind):
    return arr


@overload(get_arr_data_ptr, no_unliteral=True)
def overload_get_arr_data_ptr(arr, ind):
    assert isinstance(types.unliteral(ind), types.Integer)
    if isinstance(arr, bodo.libs.int_arr_ext.IntegerArrayType):

        def impl_int(arr, ind):
            return bodo.hiframes.split_impl.get_c_arr_ptr(arr._data.ctypes, ind
                )
        return impl_int
    assert isinstance(arr, types.Array)

    def impl_np(arr, ind):
        return bodo.hiframes.split_impl.get_c_arr_ptr(arr.ctypes, ind)
    return impl_np


def set_to_numeric_out_na_err(out_arr, out_ind, err_code):
    pass


@overload(set_to_numeric_out_na_err)
def set_to_numeric_out_na_err_overload(out_arr, out_ind, err_code):
    if isinstance(out_arr, bodo.libs.int_arr_ext.IntegerArrayType):

        def impl_int(out_arr, out_ind, err_code):
            bodo.libs.int_arr_ext.set_bit_to_arr(out_arr._null_bitmap,
                out_ind, 0 if err_code == -1 else 1)
        return impl_int
    assert isinstance(out_arr, types.Array)
    if isinstance(out_arr.dtype, types.Float):

        def impl_np(out_arr, out_ind, err_code):
            if err_code == -1:
                out_arr[out_ind] = np.nan
        return impl_np
    return lambda out_arr, out_ind, err_code: None


@numba.njit(no_cpython_wrapper=True)
def str_arr_item_to_numeric(out_arr, out_ind, str_arr, ind):
    err_code = _str_arr_item_to_numeric(get_arr_data_ptr(out_arr, out_ind),
        str_arr, ind, out_arr.dtype)
    set_to_numeric_out_na_err(out_arr, out_ind, err_code)


@intrinsic
def _str_arr_item_to_numeric(typingctx, out_ptr_t, str_arr_t, ind_t,
    out_dtype_t=None):
    assert str_arr_t == string_array_type
    assert ind_t == types.int64

    def codegen(context, builder, sig, args):
        rebqa__rqnwm, arr, ind, xhtm__iygy = args
        xnshf__ogk = _get_str_binary_arr_payload(context, builder, arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, xnshf__ogk.
            offsets).data
        data = context.make_helper(builder, char_arr_type, xnshf__ogk.data
            ).data
        kan__dfe = lir.FunctionType(lir.IntType(32), [rebqa__rqnwm.type,
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        ydaga__mnu = 'str_arr_to_int64'
        if sig.args[3].dtype == types.float64:
            ydaga__mnu = 'str_arr_to_float64'
        else:
            assert sig.args[3].dtype == types.int64
        jscia__ppi = cgutils.get_or_insert_function(builder.module,
            kan__dfe, ydaga__mnu)
        return builder.call(jscia__ppi, [rebqa__rqnwm, offsets, data, ind])
    return types.int32(out_ptr_t, string_array_type, types.int64, out_dtype_t
        ), codegen


@unbox(BinaryArrayType)
@unbox(StringArrayType)
def unbox_str_series(typ, val, c):
    sedx__gqeai = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    kan__dfe = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType(8
        ).as_pointer(), lir.IntType(32)])
    gxfqh__axcgh = cgutils.get_or_insert_function(c.builder.module,
        kan__dfe, name='string_array_from_sequence')
    qnyly__iyqw = c.builder.call(gxfqh__axcgh, [val, sedx__gqeai])
    ivp__pasz = ArrayItemArrayType(char_arr_type)
    wpiw__jmbcm = c.context.make_helper(c.builder, ivp__pasz)
    wpiw__jmbcm.meminfo = qnyly__iyqw
    dnki__oakqc = c.context.make_helper(c.builder, typ)
    faoem__azgtf = wpiw__jmbcm._getvalue()
    dnki__oakqc.data = faoem__azgtf
    ofmcq__vpg = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(dnki__oakqc._getvalue(), is_error=ofmcq__vpg)


@lower_constant(BinaryArrayType)
@lower_constant(StringArrayType)
def lower_constant_str_arr(context, builder, typ, pyval):
    tny__wvp = len(pyval)
    qre__awgt = 0
    rsfs__lcue = np.empty(tny__wvp + 1, np_offset_type)
    wvwku__gktl = []
    meqhn__oph = np.empty(tny__wvp + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        rsfs__lcue[i] = qre__awgt
        fpilc__cwamm = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(meqhn__oph, i, int(not
            fpilc__cwamm))
        if fpilc__cwamm:
            continue
        cemq__cwjp = list(s.encode()) if isinstance(s, str) else list(s)
        wvwku__gktl.extend(cemq__cwjp)
        qre__awgt += len(cemq__cwjp)
    rsfs__lcue[tny__wvp] = qre__awgt
    gknz__ngll = np.array(wvwku__gktl, np.uint8)
    eix__pagc = context.get_constant(types.int64, tny__wvp)
    ytwcm__glvke = context.get_constant_generic(builder, char_arr_type,
        gknz__ngll)
    ywstw__rahfk = context.get_constant_generic(builder, offset_arr_type,
        rsfs__lcue)
    vbd__zqj = context.get_constant_generic(builder, null_bitmap_arr_type,
        meqhn__oph)
    ivp__pasz = ArrayItemArrayType(char_arr_type)
    faoem__azgtf = bodo.libs.array_item_arr_ext.init_array_item_array_codegen(
        context, builder, ivp__pasz(types.int64, char_arr_type,
        offset_arr_type, null_bitmap_arr_type), [eix__pagc, ytwcm__glvke,
        ywstw__rahfk, vbd__zqj])
    dnki__oakqc = context.make_helper(builder, typ)
    dnki__oakqc.data = faoem__azgtf
    return dnki__oakqc._getvalue()


def pre_alloc_str_arr_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


from numba.parfors.array_analysis import ArrayAnalysis
(ArrayAnalysis._analyze_op_call_bodo_libs_str_arr_ext_pre_alloc_string_array
    ) = pre_alloc_str_arr_equiv


@overload(glob.glob, no_unliteral=True)
def overload_glob_glob(pathname, recursive=False):

    def _glob_glob_impl(pathname, recursive=False):
        with numba.objmode(l='list_str_type'):
            l = glob.glob(pathname, recursive=recursive)
        return l
    return _glob_glob_impl
