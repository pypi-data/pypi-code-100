"""Array implementation for variable-size array items.
Corresponds to Spark's ArrayType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Variable-size List: https://arrow.apache.org/docs/format/Columnar.html

The values are stored in a contingous data array, while an offsets array marks the
individual arrays. For example:
value:             [[1, 2], [3], None, [5, 4, 6], []]
data:              [1, 2, 3, 5, 4, 6]
offsets:           [0, 2, 3, 3, 6, 6]
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import NativeValue, box, intrinsic, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.libs import array_ext
from bodo.utils.cg_helpers import gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit, to_arr_obj_if_list_obj
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.typing import BodoError, is_iterable_type, is_list_like_index_type
ll.add_symbol('count_total_elems_list_array', array_ext.
    count_total_elems_list_array)
ll.add_symbol('array_item_array_from_sequence', array_ext.
    array_item_array_from_sequence)
ll.add_symbol('np_array_from_array_item_array', array_ext.
    np_array_from_array_item_array)
offset_type = types.uint64
np_offset_type = numba.np.numpy_support.as_dtype(offset_type)


class ArrayItemArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        assert bodo.utils.utils.is_array_typ(dtype, False)
        self.dtype = dtype
        super(ArrayItemArrayType, self).__init__(name=
            'ArrayItemArrayType({})'.format(dtype))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return ArrayItemArrayType(self.dtype)


class ArrayItemArrayPayloadType(types.Type):

    def __init__(self, array_type):
        self.array_type = array_type
        super(ArrayItemArrayPayloadType, self).__init__(name=
            'ArrayItemArrayPayloadType({})'.format(array_type))


@register_model(ArrayItemArrayPayloadType)
class ArrayItemArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ojjmv__rtpha = [('n_arrays', types.int64), ('data', fe_type.
            array_type.dtype), ('offsets', types.Array(offset_type, 1, 'C')
            ), ('null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, ojjmv__rtpha)


@register_model(ArrayItemArrayType)
class ArrayItemArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = ArrayItemArrayPayloadType(fe_type)
        ojjmv__rtpha = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, ojjmv__rtpha)


def define_array_item_dtor(context, builder, array_item_type, payload_type):
    eykb__uwfxs = builder.module
    wcjz__cmc = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    lxc__avr = cgutils.get_or_insert_function(eykb__uwfxs, wcjz__cmc, name=
        '.dtor.array_item.{}'.format(array_item_type.dtype))
    if not lxc__avr.is_declaration:
        return lxc__avr
    lxc__avr.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(lxc__avr.append_basic_block())
    thh__louw = lxc__avr.args[0]
    ttxt__tqtu = context.get_value_type(payload_type).as_pointer()
    irrq__xhudo = builder.bitcast(thh__louw, ttxt__tqtu)
    rbzn__cdr = context.make_helper(builder, payload_type, ref=irrq__xhudo)
    context.nrt.decref(builder, array_item_type.dtype, rbzn__cdr.data)
    context.nrt.decref(builder, types.Array(offset_type, 1, 'C'), rbzn__cdr
        .offsets)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'), rbzn__cdr
        .null_bitmap)
    builder.ret_void()
    return lxc__avr


def construct_array_item_array(context, builder, array_item_type, n_arrays,
    n_elems, c=None):
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    ifptn__vdgl = context.get_value_type(payload_type)
    dhper__mmeq = context.get_abi_sizeof(ifptn__vdgl)
    doci__fosv = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    camiy__rrsc = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, dhper__mmeq), doci__fosv)
    oum__nij = context.nrt.meminfo_data(builder, camiy__rrsc)
    coj__oxoks = builder.bitcast(oum__nij, ifptn__vdgl.as_pointer())
    rbzn__cdr = cgutils.create_struct_proxy(payload_type)(context, builder)
    rbzn__cdr.n_arrays = n_arrays
    gor__uwkdn = n_elems.type.count
    rrj__ghucp = builder.extract_value(n_elems, 0)
    epp__dpcz = cgutils.alloca_once_value(builder, rrj__ghucp)
    cws__wmyl = builder.icmp_signed('==', rrj__ghucp, lir.Constant(
        rrj__ghucp.type, -1))
    with builder.if_then(cws__wmyl):
        builder.store(n_arrays, epp__dpcz)
    n_elems = cgutils.pack_array(builder, [builder.load(epp__dpcz)] + [
        builder.extract_value(n_elems, rrunb__yjd) for rrunb__yjd in range(
        1, gor__uwkdn)])
    rbzn__cdr.data = gen_allocate_array(context, builder, array_item_type.
        dtype, n_elems, c)
    xaga__woihy = builder.add(n_arrays, lir.Constant(lir.IntType(64), 1))
    dxfv__knc = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(offset_type, 1, 'C'), [xaga__woihy])
    offsets_ptr = dxfv__knc.data
    builder.store(context.get_constant(offset_type, 0), offsets_ptr)
    builder.store(builder.trunc(builder.extract_value(n_elems, 0), lir.
        IntType(offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    rbzn__cdr.offsets = dxfv__knc._getvalue()
    wegb__vspy = builder.udiv(builder.add(n_arrays, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    hwozt__oahud = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [wegb__vspy])
    null_bitmap_ptr = hwozt__oahud.data
    rbzn__cdr.null_bitmap = hwozt__oahud._getvalue()
    builder.store(rbzn__cdr._getvalue(), coj__oxoks)
    return camiy__rrsc, rbzn__cdr.data, offsets_ptr, null_bitmap_ptr


def _unbox_array_item_array_copy_data(arr_typ, arr_obj, c, data_arr,
    item_ind, n_items):
    context = c.context
    builder = c.builder
    arr_obj = to_arr_obj_if_list_obj(c, context, builder, arr_obj, arr_typ)
    arr_val = c.pyapi.to_native_value(arr_typ, arr_obj).value
    sig = types.none(arr_typ, types.int64, types.int64, arr_typ)

    def copy_data(data_arr, item_ind, n_items, arr_val):
        data_arr[item_ind:item_ind + n_items] = arr_val
    qsh__gxdrs, cvy__hawha = c.pyapi.call_jit_code(copy_data, sig, [
        data_arr, item_ind, n_items, arr_val])
    c.context.nrt.decref(builder, arr_typ, arr_val)


def _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
    offsets_ptr, null_bitmap_ptr):
    context = c.context
    builder = c.builder
    jzk__hcyho = context.insert_const_string(builder.module, 'pandas')
    agfv__ucp = c.pyapi.import_module_noblock(jzk__hcyho)
    ubzt__qox = c.pyapi.object_getattr_string(agfv__ucp, 'NA')
    gmm__kmml = c.context.get_constant(offset_type, 0)
    builder.store(gmm__kmml, offsets_ptr)
    lil__ofhgm = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_arrays) as loop:
        juujv__rgbzt = loop.index
        item_ind = builder.load(lil__ofhgm)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [juujv__rgbzt]))
        arr_obj = seq_getitem(builder, context, val, juujv__rgbzt)
        set_bitmap_bit(builder, null_bitmap_ptr, juujv__rgbzt, 0)
        gpnhs__jvxx = is_na_value(builder, context, arr_obj, ubzt__qox)
        zmm__knktz = builder.icmp_unsigned('!=', gpnhs__jvxx, lir.Constant(
            gpnhs__jvxx.type, 1))
        with builder.if_then(zmm__knktz):
            set_bitmap_bit(builder, null_bitmap_ptr, juujv__rgbzt, 1)
            n_items = bodo.utils.utils.object_length(c, arr_obj)
            _unbox_array_item_array_copy_data(typ.dtype, arr_obj, c,
                data_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), lil__ofhgm)
        c.pyapi.decref(arr_obj)
    builder.store(builder.trunc(builder.load(lil__ofhgm), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    c.pyapi.decref(agfv__ucp)
    c.pyapi.decref(ubzt__qox)


@unbox(ArrayItemArrayType)
def unbox_array_item_array(typ, val, c):
    ztdt__yot = isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type)
    n_arrays = bodo.utils.utils.object_length(c, val)
    if ztdt__yot:
        wcjz__cmc = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        asng__wuzbw = cgutils.get_or_insert_function(c.builder.module,
            wcjz__cmc, name='count_total_elems_list_array')
        n_elems = cgutils.pack_array(c.builder, [c.builder.call(asng__wuzbw,
            [val])])
    else:
        vpq__gvuve = get_array_elem_counts(c, c.builder, c.context, val, typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            vpq__gvuve, rrunb__yjd) for rrunb__yjd in range(1, vpq__gvuve.
            type.count)])
    camiy__rrsc, data_arr, offsets_ptr, null_bitmap_ptr = (
        construct_array_item_array(c.context, c.builder, typ, n_arrays,
        n_elems, c))
    if ztdt__yot:
        cti__yld = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        waaaj__qxu = c.context.make_array(typ.dtype)(c.context, c.builder,
            data_arr).data
        wcjz__cmc = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(32)])
        lxc__avr = cgutils.get_or_insert_function(c.builder.module,
            wcjz__cmc, name='array_item_array_from_sequence')
        c.builder.call(lxc__avr, [val, c.builder.bitcast(waaaj__qxu, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), cti__yld)])
    else:
        _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
            offsets_ptr, null_bitmap_ptr)
    fsb__ahtug = c.context.make_helper(c.builder, typ)
    fsb__ahtug.meminfo = camiy__rrsc
    vuz__cpyo = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(fsb__ahtug._getvalue(), is_error=vuz__cpyo)


def _get_array_item_arr_payload(context, builder, arr_typ, arr):
    fsb__ahtug = context.make_helper(builder, arr_typ, arr)
    payload_type = ArrayItemArrayPayloadType(arr_typ)
    oum__nij = context.nrt.meminfo_data(builder, fsb__ahtug.meminfo)
    coj__oxoks = builder.bitcast(oum__nij, context.get_value_type(
        payload_type).as_pointer())
    rbzn__cdr = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(coj__oxoks))
    return rbzn__cdr


def _box_array_item_array_generic(typ, c, n_arrays, data_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    jzk__hcyho = context.insert_const_string(builder.module, 'numpy')
    rdjdt__opy = c.pyapi.import_module_noblock(jzk__hcyho)
    nak__bcueg = c.pyapi.object_getattr_string(rdjdt__opy, 'object_')
    nvsid__vfea = c.pyapi.long_from_longlong(n_arrays)
    mnakx__moa = c.pyapi.call_method(rdjdt__opy, 'ndarray', (nvsid__vfea,
        nak__bcueg))
    fkp__gjz = c.pyapi.object_getattr_string(rdjdt__opy, 'nan')
    lil__ofhgm = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_arrays) as loop:
        juujv__rgbzt = loop.index
        pyarray_setitem(builder, context, mnakx__moa, juujv__rgbzt, fkp__gjz)
        fgv__gfqw = get_bitmap_bit(builder, null_bitmap_ptr, juujv__rgbzt)
        sud__ydzj = builder.icmp_unsigned('!=', fgv__gfqw, lir.Constant(lir
            .IntType(8), 0))
        with builder.if_then(sud__ydzj):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(juujv__rgbzt, lir.Constant(
                juujv__rgbzt.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [juujv__rgbzt]))), lir.IntType(64))
            item_ind = builder.load(lil__ofhgm)
            qsh__gxdrs, hqdl__hlemy = c.pyapi.call_jit_code(lambda data_arr,
                item_ind, n_items: data_arr[item_ind:item_ind + n_items],
                typ.dtype(typ.dtype, types.int64, types.int64), [data_arr,
                item_ind, n_items])
            builder.store(builder.add(item_ind, n_items), lil__ofhgm)
            arr_obj = c.pyapi.from_native_value(typ.dtype, hqdl__hlemy, c.
                env_manager)
            pyarray_setitem(builder, context, mnakx__moa, juujv__rgbzt, arr_obj
                )
            c.pyapi.decref(arr_obj)
    c.pyapi.decref(rdjdt__opy)
    c.pyapi.decref(nak__bcueg)
    c.pyapi.decref(nvsid__vfea)
    c.pyapi.decref(fkp__gjz)
    return mnakx__moa


@box(ArrayItemArrayType)
def box_array_item_arr(typ, val, c):
    rbzn__cdr = _get_array_item_arr_payload(c.context, c.builder, typ, val)
    data_arr = rbzn__cdr.data
    offsets_ptr = c.context.make_helper(c.builder, types.Array(offset_type,
        1, 'C'), rbzn__cdr.offsets).data
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), rbzn__cdr.null_bitmap).data
    if isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type):
        cti__yld = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        waaaj__qxu = c.context.make_helper(c.builder, typ.dtype, data_arr).data
        wcjz__cmc = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32)])
        mug__gkj = cgutils.get_or_insert_function(c.builder.module,
            wcjz__cmc, name='np_array_from_array_item_array')
        arr = c.builder.call(mug__gkj, [rbzn__cdr.n_arrays, c.builder.
            bitcast(waaaj__qxu, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), cti__yld)])
    else:
        arr = _box_array_item_array_generic(typ, c, rbzn__cdr.n_arrays,
            data_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def lower_pre_alloc_array_item_array(context, builder, sig, args):
    array_item_type = sig.return_type
    xoh__fbyb, smv__cdmf, emgh__emb = args
    dya__xiz = bodo.utils.transform.get_type_alloc_counts(array_item_type.dtype
        )
    ssn__yaxym = sig.args[1]
    if not isinstance(ssn__yaxym, types.UniTuple):
        smv__cdmf = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), -1) for emgh__emb in range(dya__xiz)])
    elif ssn__yaxym.count < dya__xiz:
        smv__cdmf = cgutils.pack_array(builder, [builder.extract_value(
            smv__cdmf, rrunb__yjd) for rrunb__yjd in range(ssn__yaxym.count
            )] + [lir.Constant(lir.IntType(64), -1) for emgh__emb in range(
            dya__xiz - ssn__yaxym.count)])
    camiy__rrsc, emgh__emb, emgh__emb, emgh__emb = construct_array_item_array(
        context, builder, array_item_type, xoh__fbyb, smv__cdmf)
    fsb__ahtug = context.make_helper(builder, array_item_type)
    fsb__ahtug.meminfo = camiy__rrsc
    return fsb__ahtug._getvalue()


@intrinsic
def pre_alloc_array_item_array(typingctx, num_arrs_typ, num_values_typ,
    dtype_typ=None):
    assert isinstance(num_arrs_typ, types.Integer)
    array_item_type = ArrayItemArrayType(dtype_typ.instance_type)
    num_values_typ = types.unliteral(num_values_typ)
    return array_item_type(types.int64, num_values_typ, dtype_typ
        ), lower_pre_alloc_array_item_array


def pre_alloc_array_item_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_libs_array_item_arr_ext_pre_alloc_array_item_array
    ) = pre_alloc_array_item_array_equiv


def init_array_item_array_codegen(context, builder, signature, args):
    n_arrays, rfy__lcxdt, dxfv__knc, hwozt__oahud = args
    array_item_type = signature.return_type
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    ifptn__vdgl = context.get_value_type(payload_type)
    dhper__mmeq = context.get_abi_sizeof(ifptn__vdgl)
    doci__fosv = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    camiy__rrsc = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, dhper__mmeq), doci__fosv)
    oum__nij = context.nrt.meminfo_data(builder, camiy__rrsc)
    coj__oxoks = builder.bitcast(oum__nij, ifptn__vdgl.as_pointer())
    rbzn__cdr = cgutils.create_struct_proxy(payload_type)(context, builder)
    rbzn__cdr.n_arrays = n_arrays
    rbzn__cdr.data = rfy__lcxdt
    rbzn__cdr.offsets = dxfv__knc
    rbzn__cdr.null_bitmap = hwozt__oahud
    builder.store(rbzn__cdr._getvalue(), coj__oxoks)
    context.nrt.incref(builder, signature.args[1], rfy__lcxdt)
    context.nrt.incref(builder, signature.args[2], dxfv__knc)
    context.nrt.incref(builder, signature.args[3], hwozt__oahud)
    fsb__ahtug = context.make_helper(builder, array_item_type)
    fsb__ahtug.meminfo = camiy__rrsc
    return fsb__ahtug._getvalue()


@intrinsic
def init_array_item_array(typingctx, n_arrays_typ, data_type, offsets_typ,
    null_bitmap_typ=None):
    assert null_bitmap_typ == types.Array(types.uint8, 1, 'C')
    rcdc__cef = ArrayItemArrayType(data_type)
    sig = rcdc__cef(types.int64, data_type, offsets_typ, null_bitmap_typ)
    return sig, init_array_item_array_codegen


@intrinsic
def get_offsets(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        rbzn__cdr = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            rbzn__cdr.offsets)
    return types.Array(offset_type, 1, 'C')(arr_typ), codegen


@intrinsic
def get_offsets_ind(typingctx, arr_typ, ind_t=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, ind = args
        rbzn__cdr = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        waaaj__qxu = context.make_array(types.Array(offset_type, 1, 'C'))(
            context, builder, rbzn__cdr.offsets).data
        dxfv__knc = builder.bitcast(waaaj__qxu, lir.IntType(offset_type.
            bitwidth).as_pointer())
        return builder.load(builder.gep(dxfv__knc, [ind]))
    return offset_type(arr_typ, types.int64), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        rbzn__cdr = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            rbzn__cdr.data)
    return arr_typ.dtype(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        rbzn__cdr = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            rbzn__cdr.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


@intrinsic
def get_n_arrays(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        rbzn__cdr = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return rbzn__cdr.n_arrays
    return types.int64(arr_typ), codegen


@intrinsic
def replace_data_arr(typingctx, arr_typ, data_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType
        ) and data_typ == arr_typ.dtype

    def codegen(context, builder, sig, args):
        arr, zlcy__qygpi = args
        fsb__ahtug = context.make_helper(builder, arr_typ, arr)
        payload_type = ArrayItemArrayPayloadType(arr_typ)
        oum__nij = context.nrt.meminfo_data(builder, fsb__ahtug.meminfo)
        coj__oxoks = builder.bitcast(oum__nij, context.get_value_type(
            payload_type).as_pointer())
        rbzn__cdr = cgutils.create_struct_proxy(payload_type)(context,
            builder, builder.load(coj__oxoks))
        context.nrt.decref(builder, data_typ, rbzn__cdr.data)
        rbzn__cdr.data = zlcy__qygpi
        context.nrt.incref(builder, data_typ, zlcy__qygpi)
        builder.store(rbzn__cdr._getvalue(), coj__oxoks)
    return types.none(arr_typ, data_typ), codegen


@numba.njit(no_cpython_wrapper=True)
def ensure_data_capacity(arr, old_size, new_size):
    rfy__lcxdt = get_data(arr)
    inrwo__ugb = len(rfy__lcxdt)
    if inrwo__ugb < new_size:
        efjpz__rtobr = max(2 * inrwo__ugb, new_size)
        zlcy__qygpi = bodo.libs.array_kernels.resize_and_copy(rfy__lcxdt,
            old_size, efjpz__rtobr)
        replace_data_arr(arr, zlcy__qygpi)


@overload(len, no_unliteral=True)
def overload_array_item_arr_len(A):
    if isinstance(A, ArrayItemArrayType):
        return lambda A: get_n_arrays(A)


@overload_attribute(ArrayItemArrayType, 'shape')
def overload_array_item_arr_shape(A):
    return lambda A: (get_n_arrays(A),)


@overload_attribute(ArrayItemArrayType, 'dtype')
def overload_array_item_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(ArrayItemArrayType, 'ndim')
def overload_array_item_arr_ndim(A):
    return lambda A: 1


@overload_attribute(ArrayItemArrayType, 'nbytes')
def overload_array_item_arr_nbytes(A):
    return lambda A: get_data(A).nbytes + get_offsets(A
        ).nbytes + get_null_bitmap(A).nbytes


@overload(operator.getitem, no_unliteral=True)
def array_item_arr_getitem_array(arr, ind):
    if not isinstance(arr, ArrayItemArrayType):
        return
    if isinstance(ind, types.Integer):

        def array_item_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            dxfv__knc = get_offsets(arr)
            rfy__lcxdt = get_data(arr)
            cdt__duinb = dxfv__knc[ind]
            mnuww__fuhzx = dxfv__knc[ind + 1]
            return rfy__lcxdt[cdt__duinb:mnuww__fuhzx]
        return array_item_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        crvkg__ggzly = arr.dtype

        def impl_bool(arr, ind):
            kecmj__aacn = len(arr)
            if kecmj__aacn != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            hwozt__oahud = get_null_bitmap(arr)
            n_arrays = 0
            uveuz__rlj = init_nested_counts(crvkg__ggzly)
            for rrunb__yjd in range(kecmj__aacn):
                if ind[rrunb__yjd]:
                    n_arrays += 1
                    yjqig__dncdj = arr[rrunb__yjd]
                    uveuz__rlj = add_nested_counts(uveuz__rlj, yjqig__dncdj)
            mnakx__moa = pre_alloc_array_item_array(n_arrays, uveuz__rlj,
                crvkg__ggzly)
            oaie__qfs = get_null_bitmap(mnakx__moa)
            rrk__bymgy = 0
            for spn__jaqr in range(kecmj__aacn):
                if ind[spn__jaqr]:
                    mnakx__moa[rrk__bymgy] = arr[spn__jaqr]
                    zqa__zrek = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        hwozt__oahud, spn__jaqr)
                    bodo.libs.int_arr_ext.set_bit_to_arr(oaie__qfs,
                        rrk__bymgy, zqa__zrek)
                    rrk__bymgy += 1
            return mnakx__moa
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        crvkg__ggzly = arr.dtype

        def impl_int(arr, ind):
            hwozt__oahud = get_null_bitmap(arr)
            kecmj__aacn = len(ind)
            n_arrays = kecmj__aacn
            uveuz__rlj = init_nested_counts(crvkg__ggzly)
            for cuple__emwcj in range(kecmj__aacn):
                rrunb__yjd = ind[cuple__emwcj]
                yjqig__dncdj = arr[rrunb__yjd]
                uveuz__rlj = add_nested_counts(uveuz__rlj, yjqig__dncdj)
            mnakx__moa = pre_alloc_array_item_array(n_arrays, uveuz__rlj,
                crvkg__ggzly)
            oaie__qfs = get_null_bitmap(mnakx__moa)
            for cysdp__hor in range(kecmj__aacn):
                spn__jaqr = ind[cysdp__hor]
                mnakx__moa[cysdp__hor] = arr[spn__jaqr]
                zqa__zrek = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    hwozt__oahud, spn__jaqr)
                bodo.libs.int_arr_ext.set_bit_to_arr(oaie__qfs, cysdp__hor,
                    zqa__zrek)
            return mnakx__moa
        return impl_int
    if isinstance(ind, types.SliceType):

        def impl_slice(arr, ind):
            kecmj__aacn = len(arr)
            yqtt__gusc = numba.cpython.unicode._normalize_slice(ind,
                kecmj__aacn)
            kusr__vui = np.arange(yqtt__gusc.start, yqtt__gusc.stop,
                yqtt__gusc.step)
            return arr[kusr__vui]
        return impl_slice


@overload(operator.setitem)
def array_item_arr_setitem(A, idx, val):
    if not isinstance(A, ArrayItemArrayType):
        return
    if isinstance(idx, types.Integer):

        def impl_scalar(A, idx, val):
            dxfv__knc = get_offsets(A)
            hwozt__oahud = get_null_bitmap(A)
            if idx == 0:
                dxfv__knc[0] = 0
            n_items = len(val)
            zuteb__mkw = dxfv__knc[idx] + n_items
            ensure_data_capacity(A, dxfv__knc[idx], zuteb__mkw)
            rfy__lcxdt = get_data(A)
            dxfv__knc[idx + 1] = dxfv__knc[idx] + n_items
            rfy__lcxdt[dxfv__knc[idx]:dxfv__knc[idx + 1]] = val
            bodo.libs.int_arr_ext.set_bit_to_arr(hwozt__oahud, idx, 1)
        return impl_scalar
    if isinstance(idx, types.SliceType) and A.dtype == val:

        def impl_slice_elem(A, idx, val):
            yqtt__gusc = numba.cpython.unicode._normalize_slice(idx, len(A))
            for rrunb__yjd in range(yqtt__gusc.start, yqtt__gusc.stop,
                yqtt__gusc.step):
                A[rrunb__yjd] = val
        return impl_slice_elem
    if isinstance(idx, types.SliceType) and is_iterable_type(val):

        def impl_slice(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            dxfv__knc = get_offsets(A)
            hwozt__oahud = get_null_bitmap(A)
            mjra__kvnh = get_offsets(val)
            lxf__isrxt = get_data(val)
            skl__stp = get_null_bitmap(val)
            kecmj__aacn = len(A)
            yqtt__gusc = numba.cpython.unicode._normalize_slice(idx,
                kecmj__aacn)
            adco__ycyqt, pbeyy__lkyyc = yqtt__gusc.start, yqtt__gusc.stop
            assert yqtt__gusc.step == 1
            if adco__ycyqt == 0:
                dxfv__knc[adco__ycyqt] = 0
            tgb__poy = dxfv__knc[adco__ycyqt]
            zuteb__mkw = tgb__poy + len(lxf__isrxt)
            ensure_data_capacity(A, tgb__poy, zuteb__mkw)
            rfy__lcxdt = get_data(A)
            rfy__lcxdt[tgb__poy:tgb__poy + len(lxf__isrxt)] = lxf__isrxt
            dxfv__knc[adco__ycyqt:pbeyy__lkyyc + 1] = mjra__kvnh + tgb__poy
            zny__quqly = 0
            for rrunb__yjd in range(adco__ycyqt, pbeyy__lkyyc):
                zqa__zrek = bodo.libs.int_arr_ext.get_bit_bitmap_arr(skl__stp,
                    zny__quqly)
                bodo.libs.int_arr_ext.set_bit_to_arr(hwozt__oahud,
                    rrunb__yjd, zqa__zrek)
                zny__quqly += 1
        return impl_slice
    raise BodoError(
        'only setitem with scalar index is currently supported for list arrays'
        )


@overload_method(ArrayItemArrayType, 'copy', no_unliteral=True)
def overload_array_item_arr_copy(A):

    def copy_impl(A):
        return init_array_item_array(len(A), get_data(A).copy(),
            get_offsets(A).copy(), get_null_bitmap(A).copy())
    return copy_impl
