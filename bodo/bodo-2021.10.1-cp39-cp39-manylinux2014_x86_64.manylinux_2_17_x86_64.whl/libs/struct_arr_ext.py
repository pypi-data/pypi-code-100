"""Array implementation for structs of values.
Corresponds to Spark's StructType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Struct arrays: https://arrow.apache.org/docs/format/Columnar.html

The values are stored in contiguous data arrays; one array per field. For example:
A:             ["AA", "B", "C"]
B:             [1, 2, 4]
"""
import operator
import llvmlite.binding as ll
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import NativeValue, box, intrinsic, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
from numba.typed.typedobjectutils import _cast
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.libs import array_ext
from bodo.utils.cg_helpers import gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit, to_arr_obj_if_list_obj
from bodo.utils.typing import BodoError, dtype_to_array_type, get_overload_const_int, get_overload_const_str, is_list_like_index_type, is_overload_constant_int, is_overload_constant_str, is_overload_none
ll.add_symbol('struct_array_from_sequence', array_ext.
    struct_array_from_sequence)
ll.add_symbol('np_array_from_struct_array', array_ext.
    np_array_from_struct_array)


class StructArrayType(types.ArrayCompatible):

    def __init__(self, data, names=None):
        assert isinstance(data, tuple) and len(data) > 0 and all(bodo.utils
            .utils.is_array_typ(odv__rarx, False) for odv__rarx in data)
        if names is not None:
            assert isinstance(names, tuple) and all(isinstance(odv__rarx,
                str) for odv__rarx in names) and len(names) == len(data)
        else:
            names = tuple('f{}'.format(i) for i in range(len(data)))
        self.data = data
        self.names = names
        super(StructArrayType, self).__init__(name=
            'StructArrayType({}, {})'.format(data, names))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return StructType(tuple(efyd__roxeu.dtype for efyd__roxeu in self.
            data), self.names)

    @classmethod
    def from_dict(cls, d):
        assert isinstance(d, dict)
        names = tuple(str(odv__rarx) for odv__rarx in d.keys())
        data = tuple(dtype_to_array_type(efyd__roxeu) for efyd__roxeu in d.
            values())
        return StructArrayType(data, names)

    def copy(self):
        return StructArrayType(self.data, self.names)


class StructArrayPayloadType(types.Type):

    def __init__(self, data):
        assert isinstance(data, tuple) and all(bodo.utils.utils.
            is_array_typ(odv__rarx, False) for odv__rarx in data)
        self.data = data
        super(StructArrayPayloadType, self).__init__(name=
            'StructArrayPayloadType({})'.format(data))


@register_model(StructArrayPayloadType)
class StructArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        xphte__jzwvo = [('data', types.BaseTuple.from_types(fe_type.data)),
            ('null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, xphte__jzwvo)


@register_model(StructArrayType)
class StructArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructArrayPayloadType(fe_type.data)
        xphte__jzwvo = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, xphte__jzwvo)


def define_struct_arr_dtor(context, builder, struct_arr_type, payload_type):
    rwsey__bydnn = builder.module
    zkyn__ukow = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    wvmnf__rfg = cgutils.get_or_insert_function(rwsey__bydnn, zkyn__ukow,
        name='.dtor.struct_arr.{}.{}.'.format(struct_arr_type.data,
        struct_arr_type.names))
    if not wvmnf__rfg.is_declaration:
        return wvmnf__rfg
    wvmnf__rfg.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(wvmnf__rfg.append_basic_block())
    fkqo__edm = wvmnf__rfg.args[0]
    cmww__xiq = context.get_value_type(payload_type).as_pointer()
    onp__rtg = builder.bitcast(fkqo__edm, cmww__xiq)
    buq__zhmfs = context.make_helper(builder, payload_type, ref=onp__rtg)
    context.nrt.decref(builder, types.BaseTuple.from_types(struct_arr_type.
        data), buq__zhmfs.data)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        buq__zhmfs.null_bitmap)
    builder.ret_void()
    return wvmnf__rfg


def construct_struct_array(context, builder, struct_arr_type, n_structs,
    n_elems, c=None):
    payload_type = StructArrayPayloadType(struct_arr_type.data)
    rqna__bku = context.get_value_type(payload_type)
    dsp__vph = context.get_abi_sizeof(rqna__bku)
    mhij__uam = define_struct_arr_dtor(context, builder, struct_arr_type,
        payload_type)
    wlbn__zwhyd = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, dsp__vph), mhij__uam)
    aot__zhrjn = context.nrt.meminfo_data(builder, wlbn__zwhyd)
    vtxf__hzptg = builder.bitcast(aot__zhrjn, rqna__bku.as_pointer())
    buq__zhmfs = cgutils.create_struct_proxy(payload_type)(context, builder)
    rau__gzx = []
    qmnfj__tulz = 0
    for arr_typ in struct_arr_type.data:
        vaowj__swwfv = bodo.utils.transform.get_type_alloc_counts(arr_typ.dtype
            )
        tsokz__gji = cgutils.pack_array(builder, [n_structs] + [builder.
            extract_value(n_elems, i) for i in range(qmnfj__tulz, 
            qmnfj__tulz + vaowj__swwfv)])
        arr = gen_allocate_array(context, builder, arr_typ, tsokz__gji, c)
        rau__gzx.append(arr)
        qmnfj__tulz += vaowj__swwfv
    buq__zhmfs.data = cgutils.pack_array(builder, rau__gzx
        ) if types.is_homogeneous(*struct_arr_type.data
        ) else cgutils.pack_struct(builder, rau__gzx)
    ncc__hkqql = builder.udiv(builder.add(n_structs, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    suje__odli = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [ncc__hkqql])
    null_bitmap_ptr = suje__odli.data
    buq__zhmfs.null_bitmap = suje__odli._getvalue()
    builder.store(buq__zhmfs._getvalue(), vtxf__hzptg)
    return wlbn__zwhyd, buq__zhmfs.data, null_bitmap_ptr


def _get_C_API_ptrs(c, data_tup, data_typ, names):
    empx__azp = []
    assert len(data_typ) > 0
    for i, arr_typ in enumerate(data_typ):
        fhtg__hcja = c.builder.extract_value(data_tup, i)
        arr = c.context.make_array(arr_typ)(c.context, c.builder, value=
            fhtg__hcja)
        empx__azp.append(arr.data)
    prxk__ygnfk = cgutils.pack_array(c.builder, empx__azp
        ) if types.is_homogeneous(*data_typ) else cgutils.pack_struct(c.
        builder, empx__azp)
    owott__icgwf = cgutils.alloca_once_value(c.builder, prxk__ygnfk)
    obn__pdd = [c.context.get_constant(types.int32, bodo.utils.utils.
        numba_to_c_type(odv__rarx.dtype)) for odv__rarx in data_typ]
    dlh__hdrx = cgutils.alloca_once_value(c.builder, cgutils.pack_array(c.
        builder, obn__pdd))
    flgdo__wcd = cgutils.pack_array(c.builder, [c.context.
        insert_const_string(c.builder.module, odv__rarx) for odv__rarx in
        names])
    pac__cxwi = cgutils.alloca_once_value(c.builder, flgdo__wcd)
    return owott__icgwf, dlh__hdrx, pac__cxwi


@unbox(StructArrayType)
def unbox_struct_array(typ, val, c, is_tuple_array=False):
    from bodo.libs.tuple_arr_ext import TupleArrayType
    n_structs = bodo.utils.utils.object_length(c, val)
    usbte__nxcnb = all(isinstance(efyd__roxeu, types.Array) and efyd__roxeu
        .dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for efyd__roxeu in typ.data)
    if usbte__nxcnb:
        n_elems = cgutils.pack_array(c.builder, [], lir.IntType(64))
    else:
        xtiv__pwk = get_array_elem_counts(c, c.builder, c.context, val, 
            TupleArrayType(typ.data) if is_tuple_array else typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            xtiv__pwk, i) for i in range(1, xtiv__pwk.type.count)], lir.
            IntType(64))
    wlbn__zwhyd, data_tup, null_bitmap_ptr = construct_struct_array(c.
        context, c.builder, typ, n_structs, n_elems, c)
    if usbte__nxcnb:
        owott__icgwf, dlh__hdrx, pac__cxwi = _get_C_API_ptrs(c, data_tup,
            typ.data, typ.names)
        zkyn__ukow = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1)])
        wvmnf__rfg = cgutils.get_or_insert_function(c.builder.module,
            zkyn__ukow, name='struct_array_from_sequence')
        c.builder.call(wvmnf__rfg, [val, c.context.get_constant(types.int32,
            len(typ.data)), c.builder.bitcast(owott__icgwf, lir.IntType(8).
            as_pointer()), null_bitmap_ptr, c.builder.bitcast(dlh__hdrx,
            lir.IntType(8).as_pointer()), c.builder.bitcast(pac__cxwi, lir.
            IntType(8).as_pointer()), c.context.get_constant(types.bool_,
            is_tuple_array)])
    else:
        _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
            null_bitmap_ptr, is_tuple_array)
    cqtrt__yrx = c.context.make_helper(c.builder, typ)
    cqtrt__yrx.meminfo = wlbn__zwhyd
    fwr__osops = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cqtrt__yrx._getvalue(), is_error=fwr__osops)


def _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    inah__qethi = context.insert_const_string(builder.module, 'pandas')
    eyvry__utbs = c.pyapi.import_module_noblock(inah__qethi)
    qyvfa__uaavz = c.pyapi.object_getattr_string(eyvry__utbs, 'NA')
    with cgutils.for_range(builder, n_structs) as loop:
        yljee__gvvda = loop.index
        bsm__xrbag = seq_getitem(builder, context, val, yljee__gvvda)
        set_bitmap_bit(builder, null_bitmap_ptr, yljee__gvvda, 0)
        for zsemj__epht in range(len(typ.data)):
            arr_typ = typ.data[zsemj__epht]
            data_arr = builder.extract_value(data_tup, zsemj__epht)

            def set_na(data_arr, i):
                bodo.libs.array_kernels.setna(data_arr, i)
            sig = types.none(arr_typ, types.int64)
            vyq__vpkfh, vjk__ajzlw = c.pyapi.call_jit_code(set_na, sig, [
                data_arr, yljee__gvvda])
        khqk__cur = is_na_value(builder, context, bsm__xrbag, qyvfa__uaavz)
        saqyo__tuiar = builder.icmp_unsigned('!=', khqk__cur, lir.Constant(
            khqk__cur.type, 1))
        with builder.if_then(saqyo__tuiar):
            set_bitmap_bit(builder, null_bitmap_ptr, yljee__gvvda, 1)
            for zsemj__epht in range(len(typ.data)):
                arr_typ = typ.data[zsemj__epht]
                if is_tuple_array:
                    ljt__oomz = c.pyapi.tuple_getitem(bsm__xrbag, zsemj__epht)
                else:
                    ljt__oomz = c.pyapi.dict_getitem_string(bsm__xrbag, typ
                        .names[zsemj__epht])
                khqk__cur = is_na_value(builder, context, ljt__oomz,
                    qyvfa__uaavz)
                saqyo__tuiar = builder.icmp_unsigned('!=', khqk__cur, lir.
                    Constant(khqk__cur.type, 1))
                with builder.if_then(saqyo__tuiar):
                    ljt__oomz = to_arr_obj_if_list_obj(c, context, builder,
                        ljt__oomz, arr_typ.dtype)
                    field_val = c.pyapi.to_native_value(arr_typ.dtype,
                        ljt__oomz).value
                    data_arr = builder.extract_value(data_tup, zsemj__epht)

                    def set_data(data_arr, i, field_val):
                        data_arr[i] = field_val
                    sig = types.none(arr_typ, types.int64, arr_typ.dtype)
                    vyq__vpkfh, vjk__ajzlw = c.pyapi.call_jit_code(set_data,
                        sig, [data_arr, yljee__gvvda, field_val])
                    c.context.nrt.decref(builder, arr_typ.dtype, field_val)
        c.pyapi.decref(bsm__xrbag)
    c.pyapi.decref(eyvry__utbs)
    c.pyapi.decref(qyvfa__uaavz)


def _get_struct_arr_payload(context, builder, arr_typ, arr):
    cqtrt__yrx = context.make_helper(builder, arr_typ, arr)
    payload_type = StructArrayPayloadType(arr_typ.data)
    aot__zhrjn = context.nrt.meminfo_data(builder, cqtrt__yrx.meminfo)
    vtxf__hzptg = builder.bitcast(aot__zhrjn, context.get_value_type(
        payload_type).as_pointer())
    buq__zhmfs = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(vtxf__hzptg))
    return buq__zhmfs


@box(StructArrayType)
def box_struct_arr(typ, val, c, is_tuple_array=False):
    buq__zhmfs = _get_struct_arr_payload(c.context, c.builder, typ, val)
    vyq__vpkfh, length = c.pyapi.call_jit_code(lambda A: len(A), types.
        int64(typ), [val])
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), buq__zhmfs.null_bitmap).data
    usbte__nxcnb = all(isinstance(efyd__roxeu, types.Array) and efyd__roxeu
        .dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for efyd__roxeu in typ.data)
    if usbte__nxcnb:
        owott__icgwf, dlh__hdrx, pac__cxwi = _get_C_API_ptrs(c, buq__zhmfs.
            data, typ.data, typ.names)
        zkyn__ukow = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        nxkqg__ffvas = cgutils.get_or_insert_function(c.builder.module,
            zkyn__ukow, name='np_array_from_struct_array')
        arr = c.builder.call(nxkqg__ffvas, [length, c.context.get_constant(
            types.int32, len(typ.data)), c.builder.bitcast(owott__icgwf,
            lir.IntType(8).as_pointer()), null_bitmap_ptr, c.builder.
            bitcast(dlh__hdrx, lir.IntType(8).as_pointer()), c.builder.
            bitcast(pac__cxwi, lir.IntType(8).as_pointer()), c.context.
            get_constant(types.bool_, is_tuple_array)])
    else:
        arr = _box_struct_array_generic(typ, c, length, buq__zhmfs.data,
            null_bitmap_ptr, is_tuple_array)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_struct_array_generic(typ, c, length, data_arrs_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    inah__qethi = context.insert_const_string(builder.module, 'numpy')
    cjkde__zxoba = c.pyapi.import_module_noblock(inah__qethi)
    lwzpe__pra = c.pyapi.object_getattr_string(cjkde__zxoba, 'object_')
    lou__lumqw = c.pyapi.long_from_longlong(length)
    qgesg__usm = c.pyapi.call_method(cjkde__zxoba, 'ndarray', (lou__lumqw,
        lwzpe__pra))
    bqqc__flgf = c.pyapi.object_getattr_string(cjkde__zxoba, 'nan')
    with cgutils.for_range(builder, length) as loop:
        yljee__gvvda = loop.index
        pyarray_setitem(builder, context, qgesg__usm, yljee__gvvda, bqqc__flgf)
        akhy__evmq = get_bitmap_bit(builder, null_bitmap_ptr, yljee__gvvda)
        mxsg__bkb = builder.icmp_unsigned('!=', akhy__evmq, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(mxsg__bkb):
            if is_tuple_array:
                bsm__xrbag = c.pyapi.tuple_new(len(typ.data))
            else:
                bsm__xrbag = c.pyapi.dict_new(len(typ.data))
            for i, arr_typ in enumerate(typ.data):
                if is_tuple_array:
                    c.pyapi.incref(bqqc__flgf)
                    c.pyapi.tuple_setitem(bsm__xrbag, i, bqqc__flgf)
                else:
                    c.pyapi.dict_setitem_string(bsm__xrbag, typ.names[i],
                        bqqc__flgf)
                data_arr = c.builder.extract_value(data_arrs_tup, i)
                vyq__vpkfh, brth__xbdwj = c.pyapi.call_jit_code(lambda
                    data_arr, ind: not bodo.libs.array_kernels.isna(
                    data_arr, ind), types.bool_(arr_typ, types.int64), [
                    data_arr, yljee__gvvda])
                with builder.if_then(brth__xbdwj):
                    vyq__vpkfh, field_val = c.pyapi.call_jit_code(lambda
                        data_arr, ind: data_arr[ind], arr_typ.dtype(arr_typ,
                        types.int64), [data_arr, yljee__gvvda])
                    irb__qbk = c.pyapi.from_native_value(arr_typ.dtype,
                        field_val, c.env_manager)
                    if is_tuple_array:
                        c.pyapi.tuple_setitem(bsm__xrbag, i, irb__qbk)
                    else:
                        c.pyapi.dict_setitem_string(bsm__xrbag, typ.names[i
                            ], irb__qbk)
                        c.pyapi.decref(irb__qbk)
            pyarray_setitem(builder, context, qgesg__usm, yljee__gvvda,
                bsm__xrbag)
            c.pyapi.decref(bsm__xrbag)
    c.pyapi.decref(cjkde__zxoba)
    c.pyapi.decref(lwzpe__pra)
    c.pyapi.decref(lou__lumqw)
    c.pyapi.decref(bqqc__flgf)
    return qgesg__usm


def _fix_nested_counts(nested_counts, struct_arr_type, nested_counts_type,
    builder):
    tkvoz__bdf = bodo.utils.transform.get_type_alloc_counts(struct_arr_type
        ) - 1
    if tkvoz__bdf == 0:
        return nested_counts
    if not isinstance(nested_counts_type, types.UniTuple):
        nested_counts = cgutils.pack_array(builder, [lir.Constant(lir.
            IntType(64), -1) for pmtk__oxvj in range(tkvoz__bdf)])
    elif nested_counts_type.count < tkvoz__bdf:
        nested_counts = cgutils.pack_array(builder, [builder.extract_value(
            nested_counts, i) for i in range(nested_counts_type.count)] + [
            lir.Constant(lir.IntType(64), -1) for pmtk__oxvj in range(
            tkvoz__bdf - nested_counts_type.count)])
    return nested_counts


@intrinsic
def pre_alloc_struct_array(typingctx, num_structs_typ, nested_counts_typ,
    dtypes_typ, names_typ=None):
    assert isinstance(num_structs_typ, types.Integer) and isinstance(dtypes_typ
        , types.BaseTuple)
    if is_overload_none(names_typ):
        names = tuple(f'f{i}' for i in range(len(dtypes_typ)))
    else:
        names = tuple(get_overload_const_str(efyd__roxeu) for efyd__roxeu in
            names_typ.types)
    gafub__bmm = tuple(efyd__roxeu.instance_type for efyd__roxeu in
        dtypes_typ.types)
    struct_arr_type = StructArrayType(gafub__bmm, names)

    def codegen(context, builder, sig, args):
        lyta__vtd, nested_counts, pmtk__oxvj, pmtk__oxvj = args
        nested_counts_type = sig.args[1]
        nested_counts = _fix_nested_counts(nested_counts, struct_arr_type,
            nested_counts_type, builder)
        wlbn__zwhyd, pmtk__oxvj, pmtk__oxvj = construct_struct_array(context,
            builder, struct_arr_type, lyta__vtd, nested_counts)
        cqtrt__yrx = context.make_helper(builder, struct_arr_type)
        cqtrt__yrx.meminfo = wlbn__zwhyd
        return cqtrt__yrx._getvalue()
    return struct_arr_type(num_structs_typ, nested_counts_typ, dtypes_typ,
        names_typ), codegen


def pre_alloc_struct_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 4 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_struct_arr_ext_pre_alloc_struct_array
    ) = pre_alloc_struct_array_equiv


class StructType(types.Type):

    def __init__(self, data, names):
        assert isinstance(data, tuple) and len(data) > 0
        assert isinstance(names, tuple) and all(isinstance(odv__rarx, str) for
            odv__rarx in names) and len(names) == len(data)
        self.data = data
        self.names = names
        super(StructType, self).__init__(name='StructType({}, {})'.format(
            data, names))


class StructPayloadType(types.Type):

    def __init__(self, data):
        assert isinstance(data, tuple)
        self.data = data
        super(StructPayloadType, self).__init__(name=
            'StructPayloadType({})'.format(data))


@register_model(StructPayloadType)
class StructPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        xphte__jzwvo = [('data', types.BaseTuple.from_types(fe_type.data)),
            ('null_bitmap', types.UniTuple(types.int8, len(fe_type.data)))]
        models.StructModel.__init__(self, dmm, fe_type, xphte__jzwvo)


@register_model(StructType)
class StructModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructPayloadType(fe_type.data)
        xphte__jzwvo = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, xphte__jzwvo)


def define_struct_dtor(context, builder, struct_type, payload_type):
    rwsey__bydnn = builder.module
    zkyn__ukow = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    wvmnf__rfg = cgutils.get_or_insert_function(rwsey__bydnn, zkyn__ukow,
        name='.dtor.struct.{}.{}.'.format(struct_type.data, struct_type.names))
    if not wvmnf__rfg.is_declaration:
        return wvmnf__rfg
    wvmnf__rfg.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(wvmnf__rfg.append_basic_block())
    fkqo__edm = wvmnf__rfg.args[0]
    cmww__xiq = context.get_value_type(payload_type).as_pointer()
    onp__rtg = builder.bitcast(fkqo__edm, cmww__xiq)
    buq__zhmfs = context.make_helper(builder, payload_type, ref=onp__rtg)
    for i in range(len(struct_type.data)):
        popz__gwzlw = builder.extract_value(buq__zhmfs.null_bitmap, i)
        mxsg__bkb = builder.icmp_unsigned('==', popz__gwzlw, lir.Constant(
            popz__gwzlw.type, 1))
        with builder.if_then(mxsg__bkb):
            val = builder.extract_value(buq__zhmfs.data, i)
            context.nrt.decref(builder, struct_type.data[i], val)
    builder.ret_void()
    return wvmnf__rfg


def _get_struct_payload(context, builder, typ, struct):
    struct = context.make_helper(builder, typ, struct)
    payload_type = StructPayloadType(typ.data)
    aot__zhrjn = context.nrt.meminfo_data(builder, struct.meminfo)
    vtxf__hzptg = builder.bitcast(aot__zhrjn, context.get_value_type(
        payload_type).as_pointer())
    buq__zhmfs = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(vtxf__hzptg))
    return buq__zhmfs, vtxf__hzptg


@unbox(StructType)
def unbox_struct(typ, val, c):
    context = c.context
    builder = c.builder
    inah__qethi = context.insert_const_string(builder.module, 'pandas')
    eyvry__utbs = c.pyapi.import_module_noblock(inah__qethi)
    qyvfa__uaavz = c.pyapi.object_getattr_string(eyvry__utbs, 'NA')
    lnryt__mgopg = []
    nulls = []
    for i, efyd__roxeu in enumerate(typ.data):
        irb__qbk = c.pyapi.dict_getitem_string(val, typ.names[i])
        anbhx__aepo = cgutils.alloca_once_value(c.builder, context.
            get_constant(types.uint8, 0))
        yfp__gcsu = cgutils.alloca_once_value(c.builder, cgutils.
            get_null_value(context.get_value_type(efyd__roxeu)))
        khqk__cur = is_na_value(builder, context, irb__qbk, qyvfa__uaavz)
        mxsg__bkb = builder.icmp_unsigned('!=', khqk__cur, lir.Constant(
            khqk__cur.type, 1))
        with builder.if_then(mxsg__bkb):
            builder.store(context.get_constant(types.uint8, 1), anbhx__aepo)
            field_val = c.pyapi.to_native_value(efyd__roxeu, irb__qbk).value
            builder.store(field_val, yfp__gcsu)
        lnryt__mgopg.append(builder.load(yfp__gcsu))
        nulls.append(builder.load(anbhx__aepo))
    c.pyapi.decref(eyvry__utbs)
    c.pyapi.decref(qyvfa__uaavz)
    wlbn__zwhyd = construct_struct(context, builder, typ, lnryt__mgopg, nulls)
    struct = context.make_helper(builder, typ)
    struct.meminfo = wlbn__zwhyd
    fwr__osops = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(struct._getvalue(), is_error=fwr__osops)


@box(StructType)
def box_struct(typ, val, c):
    qvbtm__ncikg = c.pyapi.dict_new(len(typ.data))
    buq__zhmfs, pmtk__oxvj = _get_struct_payload(c.context, c.builder, typ, val
        )
    assert len(typ.data) > 0
    for i, val_typ in enumerate(typ.data):
        c.pyapi.dict_setitem_string(qvbtm__ncikg, typ.names[i], c.pyapi.
            borrow_none())
        popz__gwzlw = c.builder.extract_value(buq__zhmfs.null_bitmap, i)
        mxsg__bkb = c.builder.icmp_unsigned('==', popz__gwzlw, lir.Constant
            (popz__gwzlw.type, 1))
        with c.builder.if_then(mxsg__bkb):
            xnpy__dsntg = c.builder.extract_value(buq__zhmfs.data, i)
            c.context.nrt.incref(c.builder, val_typ, xnpy__dsntg)
            ljt__oomz = c.pyapi.from_native_value(val_typ, xnpy__dsntg, c.
                env_manager)
            c.pyapi.dict_setitem_string(qvbtm__ncikg, typ.names[i], ljt__oomz)
            c.pyapi.decref(ljt__oomz)
    c.context.nrt.decref(c.builder, typ, val)
    return qvbtm__ncikg


@intrinsic
def init_struct(typingctx, data_typ, names_typ=None):
    names = tuple(get_overload_const_str(efyd__roxeu) for efyd__roxeu in
        names_typ.types)
    struct_type = StructType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, tnyao__xmw = args
        payload_type = StructPayloadType(struct_type.data)
        rqna__bku = context.get_value_type(payload_type)
        dsp__vph = context.get_abi_sizeof(rqna__bku)
        mhij__uam = define_struct_dtor(context, builder, struct_type,
            payload_type)
        wlbn__zwhyd = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, dsp__vph), mhij__uam)
        aot__zhrjn = context.nrt.meminfo_data(builder, wlbn__zwhyd)
        vtxf__hzptg = builder.bitcast(aot__zhrjn, rqna__bku.as_pointer())
        buq__zhmfs = cgutils.create_struct_proxy(payload_type)(context, builder
            )
        buq__zhmfs.data = data
        buq__zhmfs.null_bitmap = cgutils.pack_array(builder, [context.
            get_constant(types.uint8, 1) for pmtk__oxvj in range(len(
            data_typ.types))])
        builder.store(buq__zhmfs._getvalue(), vtxf__hzptg)
        context.nrt.incref(builder, data_typ, data)
        struct = context.make_helper(builder, struct_type)
        struct.meminfo = wlbn__zwhyd
        return struct._getvalue()
    return struct_type(data_typ, names_typ), codegen


@intrinsic
def get_struct_data(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        buq__zhmfs, pmtk__oxvj = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            buq__zhmfs.data)
    return types.BaseTuple.from_types(struct_typ.data)(struct_typ), codegen


@intrinsic
def get_struct_null_bitmap(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        buq__zhmfs, pmtk__oxvj = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            buq__zhmfs.null_bitmap)
    knpip__xctx = types.UniTuple(types.int8, len(struct_typ.data))
    return knpip__xctx(struct_typ), codegen


@intrinsic
def set_struct_data(typingctx, struct_typ, field_ind_typ, val_typ=None):
    assert isinstance(struct_typ, StructType) and is_overload_constant_int(
        field_ind_typ)
    field_ind = get_overload_const_int(field_ind_typ)

    def codegen(context, builder, sig, args):
        struct, pmtk__oxvj, val = args
        buq__zhmfs, vtxf__hzptg = _get_struct_payload(context, builder,
            struct_typ, struct)
        jbfi__nvgzq = buq__zhmfs.data
        czb__pgwb = builder.insert_value(jbfi__nvgzq, val, field_ind)
        fmfe__qxn = types.BaseTuple.from_types(struct_typ.data)
        context.nrt.decref(builder, fmfe__qxn, jbfi__nvgzq)
        context.nrt.incref(builder, fmfe__qxn, czb__pgwb)
        buq__zhmfs.data = czb__pgwb
        builder.store(buq__zhmfs._getvalue(), vtxf__hzptg)
        return context.get_dummy_value()
    return types.none(struct_typ, field_ind_typ, val_typ), codegen


def _get_struct_field_ind(struct, ind, op):
    if not is_overload_constant_str(ind):
        raise BodoError(
            'structs (from struct array) only support constant strings for {}, not {}'
            .format(op, ind))
    kegij__qsqck = get_overload_const_str(ind)
    if kegij__qsqck not in struct.names:
        raise BodoError('Field {} does not exist in struct {}'.format(
            kegij__qsqck, struct))
    return struct.names.index(kegij__qsqck)


def is_field_value_null(s, field_name):
    pass


@overload(is_field_value_null, no_unliteral=True)
def overload_is_field_value_null(s, field_name):
    field_ind = _get_struct_field_ind(s, field_name, 'element access (getitem)'
        )
    return lambda s, field_name: get_struct_null_bitmap(s)[field_ind] == 0


@overload(operator.getitem, no_unliteral=True)
def struct_getitem(struct, ind):
    if not isinstance(struct, StructType):
        return
    field_ind = _get_struct_field_ind(struct, ind, 'element access (getitem)')
    return lambda struct, ind: get_struct_data(struct)[field_ind]


@overload(operator.setitem, no_unliteral=True)
def struct_setitem(struct, ind, val):
    if not isinstance(struct, StructType):
        return
    field_ind = _get_struct_field_ind(struct, ind, 'item assignment (setitem)')
    field_typ = struct.data[field_ind]
    return lambda struct, ind, val: set_struct_data(struct, field_ind,
        _cast(val, field_typ))


@overload(len, no_unliteral=True)
def overload_struct_arr_len(struct):
    if isinstance(struct, StructType):
        num_fields = len(struct.data)
        return lambda struct: num_fields


def construct_struct(context, builder, struct_type, values, nulls):
    payload_type = StructPayloadType(struct_type.data)
    rqna__bku = context.get_value_type(payload_type)
    dsp__vph = context.get_abi_sizeof(rqna__bku)
    mhij__uam = define_struct_dtor(context, builder, struct_type, payload_type)
    wlbn__zwhyd = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, dsp__vph), mhij__uam)
    aot__zhrjn = context.nrt.meminfo_data(builder, wlbn__zwhyd)
    vtxf__hzptg = builder.bitcast(aot__zhrjn, rqna__bku.as_pointer())
    buq__zhmfs = cgutils.create_struct_proxy(payload_type)(context, builder)
    buq__zhmfs.data = cgutils.pack_array(builder, values
        ) if types.is_homogeneous(*struct_type.data) else cgutils.pack_struct(
        builder, values)
    buq__zhmfs.null_bitmap = cgutils.pack_array(builder, nulls)
    builder.store(buq__zhmfs._getvalue(), vtxf__hzptg)
    return wlbn__zwhyd


@intrinsic
def struct_array_get_struct(typingctx, struct_arr_typ, ind_typ=None):
    assert isinstance(struct_arr_typ, StructArrayType) and isinstance(ind_typ,
        types.Integer)
    ljo__bko = tuple(d.dtype for d in struct_arr_typ.data)
    wcpmd__gzx = StructType(ljo__bko, struct_arr_typ.names)

    def codegen(context, builder, sig, args):
        yvb__oxjqy, ind = args
        buq__zhmfs = _get_struct_arr_payload(context, builder,
            struct_arr_typ, yvb__oxjqy)
        lnryt__mgopg = []
        cobv__huj = []
        for i, arr_typ in enumerate(struct_arr_typ.data):
            fhtg__hcja = builder.extract_value(buq__zhmfs.data, i)
            zym__uhcm = context.compile_internal(builder, lambda arr, ind: 
                np.uint8(0) if bodo.libs.array_kernels.isna(arr, ind) else
                np.uint8(1), types.uint8(arr_typ, types.int64), [fhtg__hcja,
                ind])
            cobv__huj.append(zym__uhcm)
            injzj__umz = cgutils.alloca_once_value(builder, context.
                get_constant_null(arr_typ.dtype))
            mxsg__bkb = builder.icmp_unsigned('==', zym__uhcm, lir.Constant
                (zym__uhcm.type, 1))
            with builder.if_then(mxsg__bkb):
                ijjz__zcews = context.compile_internal(builder, lambda arr,
                    ind: arr[ind], arr_typ.dtype(arr_typ, types.int64), [
                    fhtg__hcja, ind])
                builder.store(ijjz__zcews, injzj__umz)
            lnryt__mgopg.append(builder.load(injzj__umz))
        if isinstance(wcpmd__gzx, types.DictType):
            jhp__mwal = [context.insert_const_string(builder.module,
                dxjiv__fng) for dxjiv__fng in struct_arr_typ.names]
            uyq__yze = cgutils.pack_array(builder, lnryt__mgopg)
            ldgoq__kup = cgutils.pack_array(builder, jhp__mwal)

            def impl(names, vals):
                d = {}
                for i, dxjiv__fng in enumerate(names):
                    d[dxjiv__fng] = vals[i]
                return d
            svu__zma = context.compile_internal(builder, impl, wcpmd__gzx(
                types.Tuple(tuple(types.StringLiteral(dxjiv__fng) for
                dxjiv__fng in struct_arr_typ.names)), types.Tuple(ljo__bko)
                ), [ldgoq__kup, uyq__yze])
            context.nrt.decref(builder, types.BaseTuple.from_types(ljo__bko
                ), uyq__yze)
            return svu__zma
        wlbn__zwhyd = construct_struct(context, builder, wcpmd__gzx,
            lnryt__mgopg, cobv__huj)
        struct = context.make_helper(builder, wcpmd__gzx)
        struct.meminfo = wlbn__zwhyd
        return struct._getvalue()
    return wcpmd__gzx(struct_arr_typ, ind_typ), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        buq__zhmfs = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            buq__zhmfs.data)
    return types.BaseTuple.from_types(arr_typ.data)(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        buq__zhmfs = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            buq__zhmfs.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


@intrinsic
def init_struct_arr(typingctx, data_typ, null_bitmap_typ, names_typ=None):
    names = tuple(get_overload_const_str(efyd__roxeu) for efyd__roxeu in
        names_typ.types)
    struct_arr_type = StructArrayType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, suje__odli, tnyao__xmw = args
        payload_type = StructArrayPayloadType(struct_arr_type.data)
        rqna__bku = context.get_value_type(payload_type)
        dsp__vph = context.get_abi_sizeof(rqna__bku)
        mhij__uam = define_struct_arr_dtor(context, builder,
            struct_arr_type, payload_type)
        wlbn__zwhyd = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, dsp__vph), mhij__uam)
        aot__zhrjn = context.nrt.meminfo_data(builder, wlbn__zwhyd)
        vtxf__hzptg = builder.bitcast(aot__zhrjn, rqna__bku.as_pointer())
        buq__zhmfs = cgutils.create_struct_proxy(payload_type)(context, builder
            )
        buq__zhmfs.data = data
        buq__zhmfs.null_bitmap = suje__odli
        builder.store(buq__zhmfs._getvalue(), vtxf__hzptg)
        context.nrt.incref(builder, data_typ, data)
        context.nrt.incref(builder, null_bitmap_typ, suje__odli)
        cqtrt__yrx = context.make_helper(builder, struct_arr_type)
        cqtrt__yrx.meminfo = wlbn__zwhyd
        return cqtrt__yrx._getvalue()
    return struct_arr_type(data_typ, null_bitmap_typ, names_typ), codegen


@overload(operator.getitem, no_unliteral=True)
def struct_arr_getitem(arr, ind):
    if not isinstance(arr, StructArrayType):
        return
    if isinstance(ind, types.Integer):

        def struct_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            return struct_array_get_struct(arr, ind)
        return struct_arr_getitem_impl
    nqoe__xdja = len(arr.data)
    hejn__lsr = 'def impl(arr, ind):\n'
    hejn__lsr += '  data = get_data(arr)\n'
    hejn__lsr += '  null_bitmap = get_null_bitmap(arr)\n'
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        hejn__lsr += """  out_null_bitmap = get_new_null_mask_bool_index(null_bitmap, ind, len(data[0]))
"""
    elif is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        hejn__lsr += """  out_null_bitmap = get_new_null_mask_int_index(null_bitmap, ind, len(data[0]))
"""
    elif isinstance(ind, types.SliceType):
        hejn__lsr += """  out_null_bitmap = get_new_null_mask_slice_index(null_bitmap, ind, len(data[0]))
"""
    else:
        raise BodoError('invalid index {} in struct array indexing'.format(ind)
            )
    hejn__lsr += ('  return init_struct_arr(({},), out_null_bitmap, ({},))\n'
        .format(', '.join('ensure_contig_if_np(data[{}][ind])'.format(i) for
        i in range(nqoe__xdja)), ', '.join("'{}'".format(dxjiv__fng) for
        dxjiv__fng in arr.names)))
    zckk__oibvg = {}
    exec(hejn__lsr, {'init_struct_arr': init_struct_arr, 'get_data':
        get_data, 'get_null_bitmap': get_null_bitmap, 'ensure_contig_if_np':
        bodo.utils.conversion.ensure_contig_if_np,
        'get_new_null_mask_bool_index': bodo.utils.indexing.
        get_new_null_mask_bool_index, 'get_new_null_mask_int_index': bodo.
        utils.indexing.get_new_null_mask_int_index,
        'get_new_null_mask_slice_index': bodo.utils.indexing.
        get_new_null_mask_slice_index}, zckk__oibvg)
    impl = zckk__oibvg['impl']
    return impl


@overload(operator.setitem, no_unliteral=True)
def struct_arr_setitem(arr, ind, val):
    if not isinstance(arr, StructArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if isinstance(ind, types.Integer):
        nqoe__xdja = len(arr.data)
        hejn__lsr = 'def impl(arr, ind, val):\n'
        hejn__lsr += '  data = get_data(arr)\n'
        hejn__lsr += '  null_bitmap = get_null_bitmap(arr)\n'
        hejn__lsr += '  set_bit_to_arr(null_bitmap, ind, 1)\n'
        for i in range(nqoe__xdja):
            if isinstance(val, StructType):
                hejn__lsr += "  if is_field_value_null(val, '{}'):\n".format(
                    arr.names[i])
                hejn__lsr += (
                    '    bodo.libs.array_kernels.setna(data[{}], ind)\n'.
                    format(i))
                hejn__lsr += '  else:\n'
                hejn__lsr += "    data[{}][ind] = val['{}']\n".format(i,
                    arr.names[i])
            else:
                hejn__lsr += "  data[{}][ind] = val['{}']\n".format(i, arr.
                    names[i])
        zckk__oibvg = {}
        exec(hejn__lsr, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'is_field_value_null':
            is_field_value_null}, zckk__oibvg)
        impl = zckk__oibvg['impl']
        return impl
    if isinstance(ind, types.SliceType):
        nqoe__xdja = len(arr.data)
        hejn__lsr = 'def impl(arr, ind, val):\n'
        hejn__lsr += '  data = get_data(arr)\n'
        hejn__lsr += '  null_bitmap = get_null_bitmap(arr)\n'
        hejn__lsr += '  val_data = get_data(val)\n'
        hejn__lsr += '  val_null_bitmap = get_null_bitmap(val)\n'
        hejn__lsr += """  setitem_slice_index_null_bits(null_bitmap, val_null_bitmap, ind, len(arr))
"""
        for i in range(nqoe__xdja):
            hejn__lsr += '  data[{0}][ind] = val_data[{0}]\n'.format(i)
        zckk__oibvg = {}
        exec(hejn__lsr, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'setitem_slice_index_null_bits':
            bodo.utils.indexing.setitem_slice_index_null_bits}, zckk__oibvg)
        impl = zckk__oibvg['impl']
        return impl
    raise BodoError(
        'only setitem with scalar/slice index is currently supported for struct arrays'
        )


@overload(len, no_unliteral=True)
def overload_struct_arr_len(A):
    if isinstance(A, StructArrayType):
        return lambda A: len(get_data(A)[0])


@overload_attribute(StructArrayType, 'shape')
def overload_struct_arr_shape(A):
    return lambda A: (len(get_data(A)[0]),)


@overload_attribute(StructArrayType, 'dtype')
def overload_struct_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(StructArrayType, 'ndim')
def overload_struct_arr_ndim(A):
    return lambda A: 1


@overload_attribute(StructArrayType, 'nbytes')
def overload_struct_arr_nbytes(A):
    hejn__lsr = 'def impl(A):\n'
    hejn__lsr += '  total_nbytes = 0\n'
    hejn__lsr += '  data = get_data(A)\n'
    for i in range(len(A.data)):
        hejn__lsr += f'  total_nbytes += data[{i}].nbytes\n'
    hejn__lsr += '  total_nbytes += get_null_bitmap(A).nbytes\n'
    hejn__lsr += '  return total_nbytes\n'
    zckk__oibvg = {}
    exec(hejn__lsr, {'get_data': get_data, 'get_null_bitmap':
        get_null_bitmap}, zckk__oibvg)
    impl = zckk__oibvg['impl']
    return impl


@overload_method(StructArrayType, 'copy', no_unliteral=True)
def overload_struct_arr_copy(A):
    names = A.names

    def copy_impl(A):
        data = get_data(A)
        suje__odli = get_null_bitmap(A)
        bhjg__cmflp = bodo.ir.join.copy_arr_tup(data)
        mez__ugxdl = suje__odli.copy()
        return init_struct_arr(bhjg__cmflp, mez__ugxdl, names)
    return copy_impl
