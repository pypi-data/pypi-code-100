"""Array implementation for map values.
Corresponds to Spark's MapType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Map arrays: https://github.com/apache/arrow/blob/master/format/Schema.fbs

The implementation uses an array(struct) array underneath similar to Spark and Arrow.
For example: [{1: 2.1, 3: 1.1}, {5: -1.0}]
[[{"key": 1, "value" 2.1}, {"key": 3, "value": 1.1}], [{"key": 5, "value": -1.0}]]
"""
import operator
import llvmlite.binding as ll
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, register_model, unbox
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, _get_array_item_arr_payload, offset_type
from bodo.libs.struct_arr_ext import StructArrayType, _get_struct_arr_payload
from bodo.utils.cg_helpers import dict_keys, dict_merge_from_seq2, dict_values, gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit
from bodo.libs import array_ext, hdist
ll.add_symbol('count_total_elems_list_array', array_ext.
    count_total_elems_list_array)
ll.add_symbol('map_array_from_sequence', array_ext.map_array_from_sequence)
ll.add_symbol('np_array_from_map_array', array_ext.np_array_from_map_array)


class MapArrayType(types.ArrayCompatible):

    def __init__(self, key_arr_type, value_arr_type):
        self.key_arr_type = key_arr_type
        self.value_arr_type = value_arr_type
        super(MapArrayType, self).__init__(name='MapArrayType({}, {})'.
            format(key_arr_type, value_arr_type))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return types.DictType(self.key_arr_type.dtype, self.value_arr_type.
            dtype)

    def copy(self):
        return MapArrayType(self.key_arr_type, self.value_arr_type)


def _get_map_arr_data_type(map_type):
    gnon__lcvcb = StructArrayType((map_type.key_arr_type, map_type.
        value_arr_type), ('key', 'value'))
    return ArrayItemArrayType(gnon__lcvcb)


@register_model(MapArrayType)
class MapArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        nmpso__fpuf = _get_map_arr_data_type(fe_type)
        bvdqv__fnszh = [('data', nmpso__fpuf)]
        models.StructModel.__init__(self, dmm, fe_type, bvdqv__fnszh)


make_attribute_wrapper(MapArrayType, 'data', '_data')


@unbox(MapArrayType)
def unbox_map_array(typ, val, c):
    n_maps = bodo.utils.utils.object_length(c, val)
    avbh__fioon = all(isinstance(ralm__qfh, types.Array) and ralm__qfh.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for ralm__qfh in (typ.key_arr_type, typ.
        value_arr_type))
    if avbh__fioon:
        dluqw__dyd = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        haw__nru = cgutils.get_or_insert_function(c.builder.module,
            dluqw__dyd, name='count_total_elems_list_array')
        dvu__nbkr = cgutils.pack_array(c.builder, [n_maps, c.builder.call(
            haw__nru, [val])])
    else:
        dvu__nbkr = get_array_elem_counts(c, c.builder, c.context, val, typ)
    nmpso__fpuf = _get_map_arr_data_type(typ)
    data_arr = gen_allocate_array(c.context, c.builder, nmpso__fpuf,
        dvu__nbkr, c)
    bswb__vsnm = _get_array_item_arr_payload(c.context, c.builder,
        nmpso__fpuf, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, bswb__vsnm.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, bswb__vsnm.offsets).data
    mnlg__pfggp = _get_struct_arr_payload(c.context, c.builder, nmpso__fpuf
        .dtype, bswb__vsnm.data)
    key_arr = c.builder.extract_value(mnlg__pfggp.data, 0)
    value_arr = c.builder.extract_value(mnlg__pfggp.data, 1)
    sig = types.none(types.Array(types.uint8, 1, 'C'))
    cqt__fpd, dazl__lxqx = c.pyapi.call_jit_code(lambda A: A.fill(255), sig,
        [mnlg__pfggp.null_bitmap])
    if avbh__fioon:
        sddk__lyzgk = c.context.make_array(nmpso__fpuf.dtype.data[0])(c.
            context, c.builder, key_arr).data
        adnxp__ubf = c.context.make_array(nmpso__fpuf.dtype.data[1])(c.
            context, c.builder, value_arr).data
        dluqw__dyd = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
        kria__nreqv = cgutils.get_or_insert_function(c.builder.module,
            dluqw__dyd, name='map_array_from_sequence')
        dzben__jhmx = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        hocyj__bien = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype
            )
        c.builder.call(kria__nreqv, [val, c.builder.bitcast(sddk__lyzgk,
            lir.IntType(8).as_pointer()), c.builder.bitcast(adnxp__ubf, lir
            .IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), dzben__jhmx), lir.Constant(lir.
            IntType(32), hocyj__bien)])
    else:
        _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
            offsets_ptr, null_bitmap_ptr)
    rhg__byt = c.context.make_helper(c.builder, typ)
    rhg__byt.data = data_arr
    ktab__jtx = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(rhg__byt._getvalue(), is_error=ktab__jtx)


def _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
    offsets_ptr, null_bitmap_ptr):
    from bodo.libs.array_item_arr_ext import _unbox_array_item_array_copy_data
    context = c.context
    builder = c.builder
    ueij__eobbb = context.insert_const_string(builder.module, 'pandas')
    ygp__qiv = c.pyapi.import_module_noblock(ueij__eobbb)
    iymfc__pfxu = c.pyapi.object_getattr_string(ygp__qiv, 'NA')
    uiy__lbdd = c.context.get_constant(offset_type, 0)
    builder.store(uiy__lbdd, offsets_ptr)
    yveb__vgmw = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_maps) as loop:
        awiv__cigy = loop.index
        item_ind = builder.load(yveb__vgmw)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [awiv__cigy]))
        clkev__kwdzu = seq_getitem(builder, context, val, awiv__cigy)
        set_bitmap_bit(builder, null_bitmap_ptr, awiv__cigy, 0)
        amta__ivjv = is_na_value(builder, context, clkev__kwdzu, iymfc__pfxu)
        sem__ngqnh = builder.icmp_unsigned('!=', amta__ivjv, lir.Constant(
            amta__ivjv.type, 1))
        with builder.if_then(sem__ngqnh):
            set_bitmap_bit(builder, null_bitmap_ptr, awiv__cigy, 1)
            jlp__fkzfh = dict_keys(builder, context, clkev__kwdzu)
            lrkah__jptvr = dict_values(builder, context, clkev__kwdzu)
            n_items = bodo.utils.utils.object_length(c, jlp__fkzfh)
            _unbox_array_item_array_copy_data(typ.key_arr_type, jlp__fkzfh,
                c, key_arr, item_ind, n_items)
            _unbox_array_item_array_copy_data(typ.value_arr_type,
                lrkah__jptvr, c, value_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), yveb__vgmw)
            c.pyapi.decref(jlp__fkzfh)
            c.pyapi.decref(lrkah__jptvr)
        c.pyapi.decref(clkev__kwdzu)
    builder.store(builder.trunc(builder.load(yveb__vgmw), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_maps]))
    c.pyapi.decref(ygp__qiv)
    c.pyapi.decref(iymfc__pfxu)


@box(MapArrayType)
def box_map_arr(typ, val, c):
    rhg__byt = c.context.make_helper(c.builder, typ, val)
    data_arr = rhg__byt.data
    nmpso__fpuf = _get_map_arr_data_type(typ)
    bswb__vsnm = _get_array_item_arr_payload(c.context, c.builder,
        nmpso__fpuf, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, bswb__vsnm.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, bswb__vsnm.offsets).data
    mnlg__pfggp = _get_struct_arr_payload(c.context, c.builder, nmpso__fpuf
        .dtype, bswb__vsnm.data)
    key_arr = c.builder.extract_value(mnlg__pfggp.data, 0)
    value_arr = c.builder.extract_value(mnlg__pfggp.data, 1)
    if all(isinstance(ralm__qfh, types.Array) and ralm__qfh.dtype in (types
        .int64, types.float64, types.bool_, datetime_date_type) for
        ralm__qfh in (typ.key_arr_type, typ.value_arr_type)):
        sddk__lyzgk = c.context.make_array(nmpso__fpuf.dtype.data[0])(c.
            context, c.builder, key_arr).data
        adnxp__ubf = c.context.make_array(nmpso__fpuf.dtype.data[1])(c.
            context, c.builder, value_arr).data
        dluqw__dyd = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(offset_type.bitwidth).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(32)])
        cyd__ogfpw = cgutils.get_or_insert_function(c.builder.module,
            dluqw__dyd, name='np_array_from_map_array')
        dzben__jhmx = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        hocyj__bien = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype
            )
        arr = c.builder.call(cyd__ogfpw, [bswb__vsnm.n_arrays, c.builder.
            bitcast(sddk__lyzgk, lir.IntType(8).as_pointer()), c.builder.
            bitcast(adnxp__ubf, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), dzben__jhmx),
            lir.Constant(lir.IntType(32), hocyj__bien)])
    else:
        arr = _box_map_array_generic(typ, c, bswb__vsnm.n_arrays, key_arr,
            value_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_map_array_generic(typ, c, n_maps, key_arr, value_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    ueij__eobbb = context.insert_const_string(builder.module, 'numpy')
    tpwea__jhmfs = c.pyapi.import_module_noblock(ueij__eobbb)
    osq__cnac = c.pyapi.object_getattr_string(tpwea__jhmfs, 'object_')
    xzdh__nmqow = c.pyapi.long_from_longlong(n_maps)
    ijl__tqpn = c.pyapi.call_method(tpwea__jhmfs, 'ndarray', (xzdh__nmqow,
        osq__cnac))
    zmjb__uxp = c.pyapi.object_getattr_string(tpwea__jhmfs, 'nan')
    mbszp__vlbnr = c.pyapi.unserialize(c.pyapi.serialize_object(zip))
    yveb__vgmw = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_maps) as loop:
        xxs__pdhfq = loop.index
        pyarray_setitem(builder, context, ijl__tqpn, xxs__pdhfq, zmjb__uxp)
        wtq__hsl = get_bitmap_bit(builder, null_bitmap_ptr, xxs__pdhfq)
        wsb__hodua = builder.icmp_unsigned('!=', wtq__hsl, lir.Constant(lir
            .IntType(8), 0))
        with builder.if_then(wsb__hodua):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(xxs__pdhfq, lir.Constant(
                xxs__pdhfq.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [xxs__pdhfq]))), lir.IntType(64))
            item_ind = builder.load(yveb__vgmw)
            clkev__kwdzu = c.pyapi.dict_new()
            lks__ybsg = lambda data_arr, item_ind, n_items: data_arr[item_ind
                :item_ind + n_items]
            cqt__fpd, jfglt__qilt = c.pyapi.call_jit_code(lks__ybsg, typ.
                key_arr_type(typ.key_arr_type, types.int64, types.int64), [
                key_arr, item_ind, n_items])
            cqt__fpd, ibkf__jqyh = c.pyapi.call_jit_code(lks__ybsg, typ.
                value_arr_type(typ.value_arr_type, types.int64, types.int64
                ), [value_arr, item_ind, n_items])
            ess__fni = c.pyapi.from_native_value(typ.key_arr_type,
                jfglt__qilt, c.env_manager)
            btu__zadwe = c.pyapi.from_native_value(typ.value_arr_type,
                ibkf__jqyh, c.env_manager)
            uwoq__tswec = c.pyapi.call_function_objargs(mbszp__vlbnr, (
                ess__fni, btu__zadwe))
            dict_merge_from_seq2(builder, context, clkev__kwdzu, uwoq__tswec)
            builder.store(builder.add(item_ind, n_items), yveb__vgmw)
            pyarray_setitem(builder, context, ijl__tqpn, xxs__pdhfq,
                clkev__kwdzu)
            c.pyapi.decref(uwoq__tswec)
            c.pyapi.decref(ess__fni)
            c.pyapi.decref(btu__zadwe)
            c.pyapi.decref(clkev__kwdzu)
    c.pyapi.decref(mbszp__vlbnr)
    c.pyapi.decref(tpwea__jhmfs)
    c.pyapi.decref(osq__cnac)
    c.pyapi.decref(xzdh__nmqow)
    c.pyapi.decref(zmjb__uxp)
    return ijl__tqpn


@intrinsic
def init_map_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType) and isinstance(data_typ
        .dtype, StructArrayType)
    eyv__pkoa = MapArrayType(data_typ.dtype.data[0], data_typ.dtype.data[1])

    def codegen(context, builder, sig, args):
        data_arr, = args
        rhg__byt = context.make_helper(builder, eyv__pkoa)
        rhg__byt.data = data_arr
        context.nrt.incref(builder, data_typ, data_arr)
        return rhg__byt._getvalue()
    return eyv__pkoa(data_typ), codegen


@overload(len, no_unliteral=True)
def overload_map_arr_len(A):
    if isinstance(A, MapArrayType):
        return lambda A: len(A._data)


@overload_attribute(MapArrayType, 'shape')
def overload_map_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(MapArrayType, 'dtype')
def overload_map_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(MapArrayType, 'ndim')
def overload_map_arr_ndim(A):
    return lambda A: 1


@overload_attribute(MapArrayType, 'nbytes')
def overload_map_arr_nbytes(A):
    return lambda A: A._data.nbytes


@overload(operator.getitem, no_unliteral=True)
def map_arr_getitem(arr, ind):
    if not isinstance(arr, MapArrayType):
        return
    if isinstance(ind, types.Integer):

        def map_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            ycrtc__scd = dict()
            xxqj__qcdz = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            tplle__vwbfe = bodo.libs.array_item_arr_ext.get_data(arr._data)
            nzm__zaiy, bwz__vkbv = bodo.libs.struct_arr_ext.get_data(
                tplle__vwbfe)
            qkfa__ackn = xxqj__qcdz[ind]
            yqs__hdqzp = xxqj__qcdz[ind + 1]
            for bux__sebu in range(qkfa__ackn, yqs__hdqzp):
                ycrtc__scd[nzm__zaiy[bux__sebu]] = bwz__vkbv[bux__sebu]
            return ycrtc__scd
        return map_arr_getitem_impl
