import operator
import llvmlite.binding as ll
import numba
import numba.core.typing.typeof
import numpy as np
from llvmlite import ir as lir
from llvmlite.llvmpy.core import Type as LLType
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, impl_ret_new_ref
from numba.extending import box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, register_model
import bodo
from bodo.libs import hstr_ext
from bodo.libs.array_item_arr_ext import offset_type
from bodo.libs.str_arr_ext import _get_str_binary_arr_payload, _memcpy, char_arr_type, get_data_ptr, null_bitmap_arr_type, offset_arr_type, string_array_type
ll.add_symbol('array_setitem', hstr_ext.array_setitem)
ll.add_symbol('array_getptr1', hstr_ext.array_getptr1)
ll.add_symbol('dtor_str_arr_split_view', hstr_ext.dtor_str_arr_split_view)
ll.add_symbol('str_arr_split_view_impl', hstr_ext.str_arr_split_view_impl)
ll.add_symbol('str_arr_split_view_alloc', hstr_ext.str_arr_split_view_alloc)
char_typ = types.uint8
data_ctypes_type = types.ArrayCTypes(types.Array(char_typ, 1, 'C'))
offset_ctypes_type = types.ArrayCTypes(types.Array(offset_type, 1, 'C'))


class StringArraySplitViewType(types.ArrayCompatible):

    def __init__(self):
        super(StringArraySplitViewType, self).__init__(name=
            'StringArraySplitViewType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_array_type

    def copy(self):
        return StringArraySplitViewType()


string_array_split_view_type = StringArraySplitViewType()


class StringArraySplitViewPayloadType(types.Type):

    def __init__(self):
        super(StringArraySplitViewPayloadType, self).__init__(name=
            'StringArraySplitViewPayloadType()')


str_arr_split_view_payload_type = StringArraySplitViewPayloadType()


@register_model(StringArraySplitViewPayloadType)
class StringArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        vpzv__qjxf = [('index_offsets', types.CPointer(offset_type)), (
            'data_offsets', types.CPointer(offset_type)), ('null_bitmap',
            types.CPointer(char_typ))]
        models.StructModel.__init__(self, dmm, fe_type, vpzv__qjxf)


str_arr_model_members = [('num_items', types.uint64), ('index_offsets',
    types.CPointer(offset_type)), ('data_offsets', types.CPointer(
    offset_type)), ('data', data_ctypes_type), ('null_bitmap', types.
    CPointer(char_typ)), ('meminfo', types.MemInfoPointer(
    str_arr_split_view_payload_type))]


@register_model(StringArraySplitViewType)
class StringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        models.StructModel.__init__(self, dmm, fe_type, str_arr_model_members)


make_attribute_wrapper(StringArraySplitViewType, 'num_items', '_num_items')
make_attribute_wrapper(StringArraySplitViewType, 'index_offsets',
    '_index_offsets')
make_attribute_wrapper(StringArraySplitViewType, 'data_offsets',
    '_data_offsets')
make_attribute_wrapper(StringArraySplitViewType, 'data', '_data')
make_attribute_wrapper(StringArraySplitViewType, 'null_bitmap', '_null_bitmap')


def construct_str_arr_split_view(context, builder):
    pmd__eivag = context.get_value_type(str_arr_split_view_payload_type)
    bowc__kpwyy = context.get_abi_sizeof(pmd__eivag)
    qaiw__ffop = context.get_value_type(types.voidptr)
    ljdwb__vrv = context.get_value_type(types.uintp)
    hwmwn__tgx = lir.FunctionType(lir.VoidType(), [qaiw__ffop, ljdwb__vrv,
        qaiw__ffop])
    ocki__xtd = cgutils.get_or_insert_function(builder.module, hwmwn__tgx,
        name='dtor_str_arr_split_view')
    xfog__qlex = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, bowc__kpwyy), ocki__xtd)
    vdm__qvgtn = context.nrt.meminfo_data(builder, xfog__qlex)
    bmxv__noryo = builder.bitcast(vdm__qvgtn, pmd__eivag.as_pointer())
    return xfog__qlex, bmxv__noryo


@intrinsic
def compute_split_view(typingctx, str_arr_typ, sep_typ=None):
    assert str_arr_typ == string_array_type and isinstance(sep_typ, types.
        StringLiteral)

    def codegen(context, builder, sig, args):
        rbhb__ohkg, wddwd__iylll = args
        xfog__qlex, bmxv__noryo = construct_str_arr_split_view(context, builder
            )
        szve__xok = _get_str_binary_arr_payload(context, builder,
            rbhb__ohkg, string_array_type)
        lnxcc__trvhn = lir.FunctionType(lir.VoidType(), [bmxv__noryo.type,
            lir.IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8)])
        penoe__xybk = cgutils.get_or_insert_function(builder.module,
            lnxcc__trvhn, name='str_arr_split_view_impl')
        ogy__qrl = context.make_helper(builder, offset_arr_type, szve__xok.
            offsets).data
        xurwj__sotb = context.make_helper(builder, char_arr_type, szve__xok
            .data).data
        djt__myazk = context.make_helper(builder, null_bitmap_arr_type,
            szve__xok.null_bitmap).data
        fxs__kdcke = context.get_constant(types.int8, ord(sep_typ.
            literal_value))
        builder.call(penoe__xybk, [bmxv__noryo, szve__xok.n_arrays,
            ogy__qrl, xurwj__sotb, djt__myazk, fxs__kdcke])
        ljpb__fomk = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(bmxv__noryo))
        jhpqo__wmbvr = context.make_helper(builder,
            string_array_split_view_type)
        jhpqo__wmbvr.num_items = szve__xok.n_arrays
        jhpqo__wmbvr.index_offsets = ljpb__fomk.index_offsets
        jhpqo__wmbvr.data_offsets = ljpb__fomk.data_offsets
        jhpqo__wmbvr.data = context.compile_internal(builder, lambda S:
            get_data_ptr(S), data_ctypes_type(string_array_type), [rbhb__ohkg])
        jhpqo__wmbvr.null_bitmap = ljpb__fomk.null_bitmap
        jhpqo__wmbvr.meminfo = xfog__qlex
        repl__tlsef = jhpqo__wmbvr._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, repl__tlsef)
    return string_array_split_view_type(string_array_type, sep_typ), codegen


@box(StringArraySplitViewType)
def box_str_arr_split_view(typ, val, c):
    context = c.context
    builder = c.builder
    izk__uwj = context.make_helper(builder, string_array_split_view_type, val)
    qjmp__ssca = context.insert_const_string(builder.module, 'numpy')
    ukk__eaqdj = c.pyapi.import_module_noblock(qjmp__ssca)
    dtype = c.pyapi.object_getattr_string(ukk__eaqdj, 'object_')
    mge__qjr = builder.sext(izk__uwj.num_items, c.pyapi.longlong)
    rudr__xug = c.pyapi.long_from_longlong(mge__qjr)
    hlvzo__bcxz = c.pyapi.call_method(ukk__eaqdj, 'ndarray', (rudr__xug, dtype)
        )
    crf__cgng = LLType.function(lir.IntType(8).as_pointer(), [c.pyapi.pyobj,
        c.pyapi.py_ssize_t])
    zpg__dkeb = c.pyapi._get_function(crf__cgng, name='array_getptr1')
    caex__wnt = LLType.function(lir.VoidType(), [c.pyapi.pyobj, lir.IntType
        (8).as_pointer(), c.pyapi.pyobj])
    mhajn__exde = c.pyapi._get_function(caex__wnt, name='array_setitem')
    dus__qia = c.pyapi.object_getattr_string(ukk__eaqdj, 'nan')
    with cgutils.for_range(builder, izk__uwj.num_items) as loop:
        str_ind = loop.index
        uyvt__ahp = builder.sext(builder.load(builder.gep(izk__uwj.
            index_offsets, [str_ind])), lir.IntType(64))
        qqtn__zanu = builder.sext(builder.load(builder.gep(izk__uwj.
            index_offsets, [builder.add(str_ind, str_ind.type(1))])), lir.
            IntType(64))
        uuym__lvvy = builder.lshr(str_ind, lir.Constant(lir.IntType(64), 3))
        sbk__ruzu = builder.gep(izk__uwj.null_bitmap, [uuym__lvvy])
        ucut__rad = builder.load(sbk__ruzu)
        djyp__djcj = builder.trunc(builder.and_(str_ind, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = builder.and_(builder.lshr(ucut__rad, djyp__djcj), lir.
            Constant(lir.IntType(8), 1))
        hfx__zbza = builder.sub(qqtn__zanu, uyvt__ahp)
        hfx__zbza = builder.sub(hfx__zbza, hfx__zbza.type(1))
        mivy__jqnu = builder.call(zpg__dkeb, [hlvzo__bcxz, str_ind])
        sdll__ljnp = c.builder.icmp_unsigned('!=', val, val.type(0))
        with c.builder.if_else(sdll__ljnp) as (then, otherwise):
            with then:
                lfv__nhmqk = c.pyapi.list_new(hfx__zbza)
                with c.builder.if_then(cgutils.is_not_null(c.builder,
                    lfv__nhmqk), likely=True):
                    with cgutils.for_range(c.builder, hfx__zbza) as loop:
                        hjwyq__caa = builder.add(uyvt__ahp, loop.index)
                        data_start = builder.load(builder.gep(izk__uwj.
                            data_offsets, [hjwyq__caa]))
                        data_start = builder.add(data_start, data_start.type(1)
                            )
                        fwvif__lfrb = builder.load(builder.gep(izk__uwj.
                            data_offsets, [builder.add(hjwyq__caa,
                            hjwyq__caa.type(1))]))
                        kuzw__yxg = builder.gep(builder.extract_value(
                            izk__uwj.data, 0), [data_start])
                        qatnn__lqf = builder.sext(builder.sub(fwvif__lfrb,
                            data_start), lir.IntType(64))
                        sgwqm__wjydq = c.pyapi.string_from_string_and_size(
                            kuzw__yxg, qatnn__lqf)
                        c.pyapi.list_setitem(lfv__nhmqk, loop.index,
                            sgwqm__wjydq)
                builder.call(mhajn__exde, [hlvzo__bcxz, mivy__jqnu, lfv__nhmqk]
                    )
            with otherwise:
                builder.call(mhajn__exde, [hlvzo__bcxz, mivy__jqnu, dus__qia])
    c.pyapi.decref(ukk__eaqdj)
    c.pyapi.decref(dtype)
    c.pyapi.decref(dus__qia)
    return hlvzo__bcxz


@intrinsic
def pre_alloc_str_arr_view(typingctx, num_items_t, num_offsets_t, data_t=None):
    assert num_items_t == types.intp and num_offsets_t == types.intp

    def codegen(context, builder, sig, args):
        qszt__guska, cxrqq__wzmy, kuzw__yxg = args
        xfog__qlex, bmxv__noryo = construct_str_arr_split_view(context, builder
            )
        lnxcc__trvhn = lir.FunctionType(lir.VoidType(), [bmxv__noryo.type,
            lir.IntType(64), lir.IntType(64)])
        penoe__xybk = cgutils.get_or_insert_function(builder.module,
            lnxcc__trvhn, name='str_arr_split_view_alloc')
        builder.call(penoe__xybk, [bmxv__noryo, qszt__guska, cxrqq__wzmy])
        ljpb__fomk = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(bmxv__noryo))
        jhpqo__wmbvr = context.make_helper(builder,
            string_array_split_view_type)
        jhpqo__wmbvr.num_items = qszt__guska
        jhpqo__wmbvr.index_offsets = ljpb__fomk.index_offsets
        jhpqo__wmbvr.data_offsets = ljpb__fomk.data_offsets
        jhpqo__wmbvr.data = kuzw__yxg
        jhpqo__wmbvr.null_bitmap = ljpb__fomk.null_bitmap
        context.nrt.incref(builder, data_t, kuzw__yxg)
        jhpqo__wmbvr.meminfo = xfog__qlex
        repl__tlsef = jhpqo__wmbvr._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, repl__tlsef)
    return string_array_split_view_type(types.intp, types.intp, data_t
        ), codegen


@intrinsic
def get_c_arr_ptr(typingctx, c_arr, ind_t=None):
    assert isinstance(c_arr, (types.CPointer, types.ArrayCTypes))

    def codegen(context, builder, sig, args):
        yaiyw__vfw, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            yaiyw__vfw = builder.extract_value(yaiyw__vfw, 0)
        return builder.bitcast(builder.gep(yaiyw__vfw, [ind]), lir.IntType(
            8).as_pointer())
    return types.voidptr(c_arr, ind_t), codegen


@intrinsic
def getitem_c_arr(typingctx, c_arr, ind_t=None):

    def codegen(context, builder, sig, args):
        yaiyw__vfw, ind = args
        return builder.load(builder.gep(yaiyw__vfw, [ind]))
    return c_arr.dtype(c_arr, ind_t), codegen


@intrinsic
def setitem_c_arr(typingctx, c_arr, ind_t, item_t=None):

    def codegen(context, builder, sig, args):
        yaiyw__vfw, ind, wyrjh__xxaf = args
        msp__qltly = builder.gep(yaiyw__vfw, [ind])
        builder.store(wyrjh__xxaf, msp__qltly)
    return types.void(c_arr, ind_t, c_arr.dtype), codegen


@intrinsic
def get_array_ctypes_ptr(typingctx, arr_ctypes_t, ind_t=None):

    def codegen(context, builder, sig, args):
        jhe__dug, ind = args
        dfzp__dkgp = context.make_helper(builder, arr_ctypes_t, jhe__dug)
        pvye__xgufv = context.make_helper(builder, arr_ctypes_t)
        pvye__xgufv.data = builder.gep(dfzp__dkgp.data, [ind])
        pvye__xgufv.meminfo = dfzp__dkgp.meminfo
        qvdbr__lvabh = pvye__xgufv._getvalue()
        return impl_ret_borrowed(context, builder, arr_ctypes_t, qvdbr__lvabh)
    return arr_ctypes_t(arr_ctypes_t, ind_t), codegen


@numba.njit(no_cpython_wrapper=True)
def get_split_view_index(arr, item_ind, str_ind):
    iixm__aqr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr._null_bitmap,
        item_ind)
    if not iixm__aqr:
        return 0, 0, 0
    hjwyq__caa = getitem_c_arr(arr._index_offsets, item_ind)
    oxury__bvnxf = getitem_c_arr(arr._index_offsets, item_ind + 1) - 1
    vpwg__ezuri = oxury__bvnxf - hjwyq__caa
    if str_ind >= vpwg__ezuri:
        return 0, 0, 0
    data_start = getitem_c_arr(arr._data_offsets, hjwyq__caa + str_ind)
    data_start += 1
    if hjwyq__caa + str_ind == 0:
        data_start = 0
    fwvif__lfrb = getitem_c_arr(arr._data_offsets, hjwyq__caa + str_ind + 1)
    fnll__gelc = fwvif__lfrb - data_start
    return 1, data_start, fnll__gelc


@numba.njit(no_cpython_wrapper=True)
def get_split_view_data_ptr(arr, data_start):
    return get_array_ctypes_ptr(arr._data, data_start)


@overload(len, no_unliteral=True)
def str_arr_split_view_len_overload(arr):
    if arr == string_array_split_view_type:
        return lambda arr: np.int64(arr._num_items)


@overload_attribute(StringArraySplitViewType, 'shape')
def overload_split_view_arr_shape(A):
    return lambda A: (np.int64(A._num_items),)


@overload(operator.getitem, no_unliteral=True)
def str_arr_split_view_getitem_overload(A, ind):
    if A != string_array_split_view_type:
        return
    if A == string_array_split_view_type and isinstance(ind, types.Integer):
        vgqb__rntv = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def _impl(A, ind):
            hjwyq__caa = getitem_c_arr(A._index_offsets, ind)
            oxury__bvnxf = getitem_c_arr(A._index_offsets, ind + 1)
            xui__bpe = oxury__bvnxf - hjwyq__caa - 1
            rbhb__ohkg = bodo.libs.str_arr_ext.pre_alloc_string_array(xui__bpe,
                -1)
            for sqtbl__mcaxn in range(xui__bpe):
                data_start = getitem_c_arr(A._data_offsets, hjwyq__caa +
                    sqtbl__mcaxn)
                data_start += 1
                if hjwyq__caa + sqtbl__mcaxn == 0:
                    data_start = 0
                fwvif__lfrb = getitem_c_arr(A._data_offsets, hjwyq__caa +
                    sqtbl__mcaxn + 1)
                fnll__gelc = fwvif__lfrb - data_start
                msp__qltly = get_array_ctypes_ptr(A._data, data_start)
                kbtl__bve = bodo.libs.str_arr_ext.decode_utf8(msp__qltly,
                    fnll__gelc)
                rbhb__ohkg[sqtbl__mcaxn] = kbtl__bve
            return rbhb__ohkg
        return _impl
    if A == string_array_split_view_type and ind == types.Array(types.bool_,
        1, 'C'):
        vwy__dzh = offset_type.bitwidth // 8

        def _impl(A, ind):
            xui__bpe = len(A)
            if xui__bpe != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            qszt__guska = 0
            cxrqq__wzmy = 0
            for sqtbl__mcaxn in range(xui__bpe):
                if ind[sqtbl__mcaxn]:
                    qszt__guska += 1
                    hjwyq__caa = getitem_c_arr(A._index_offsets, sqtbl__mcaxn)
                    oxury__bvnxf = getitem_c_arr(A._index_offsets, 
                        sqtbl__mcaxn + 1)
                    cxrqq__wzmy += oxury__bvnxf - hjwyq__caa
            hlvzo__bcxz = pre_alloc_str_arr_view(qszt__guska, cxrqq__wzmy,
                A._data)
            item_ind = 0
            vfq__sjmg = 0
            for sqtbl__mcaxn in range(xui__bpe):
                if ind[sqtbl__mcaxn]:
                    hjwyq__caa = getitem_c_arr(A._index_offsets, sqtbl__mcaxn)
                    oxury__bvnxf = getitem_c_arr(A._index_offsets, 
                        sqtbl__mcaxn + 1)
                    zhzux__oop = oxury__bvnxf - hjwyq__caa
                    setitem_c_arr(hlvzo__bcxz._index_offsets, item_ind,
                        vfq__sjmg)
                    msp__qltly = get_c_arr_ptr(A._data_offsets, hjwyq__caa)
                    pdt__qzw = get_c_arr_ptr(hlvzo__bcxz._data_offsets,
                        vfq__sjmg)
                    _memcpy(pdt__qzw, msp__qltly, zhzux__oop, vwy__dzh)
                    iixm__aqr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A.
                        _null_bitmap, sqtbl__mcaxn)
                    bodo.libs.int_arr_ext.set_bit_to_arr(hlvzo__bcxz.
                        _null_bitmap, item_ind, iixm__aqr)
                    item_ind += 1
                    vfq__sjmg += zhzux__oop
            setitem_c_arr(hlvzo__bcxz._index_offsets, item_ind, vfq__sjmg)
            return hlvzo__bcxz
        return _impl
