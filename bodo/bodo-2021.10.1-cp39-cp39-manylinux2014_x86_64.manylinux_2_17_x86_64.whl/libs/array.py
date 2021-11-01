"""Tools for handling bodo arrays, e.g. passing to C/C++ code
"""
import llvmlite.binding as ll
import numba
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.typing.templates import signature
from numba.extending import intrinsic, models, register_model
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, get_categories_int_type
from bodo.libs import array_ext
from bodo.libs.array_item_arr_ext import ArrayItemArrayPayloadType, ArrayItemArrayType, _get_array_item_arr_payload, define_array_item_dtor, offset_type
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType, int128_type
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.str_arr_ext import _get_str_binary_arr_payload, char_arr_type, null_bitmap_arr_type, offset_arr_type, string_array_type
from bodo.libs.struct_arr_ext import StructArrayPayloadType, StructArrayType, StructType, _get_struct_arr_payload, define_struct_arr_dtor
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoError
from bodo.utils.utils import CTypeEnum, check_and_propagate_cpp_exception, numba_to_c_type
ll.add_symbol('list_string_array_to_info', array_ext.list_string_array_to_info)
ll.add_symbol('nested_array_to_info', array_ext.nested_array_to_info)
ll.add_symbol('string_array_to_info', array_ext.string_array_to_info)
ll.add_symbol('numpy_array_to_info', array_ext.numpy_array_to_info)
ll.add_symbol('categorical_array_to_info', array_ext.categorical_array_to_info)
ll.add_symbol('nullable_array_to_info', array_ext.nullable_array_to_info)
ll.add_symbol('interval_array_to_info', array_ext.interval_array_to_info)
ll.add_symbol('decimal_array_to_info', array_ext.decimal_array_to_info)
ll.add_symbol('info_to_nested_array', array_ext.info_to_nested_array)
ll.add_symbol('info_to_list_string_array', array_ext.info_to_list_string_array)
ll.add_symbol('info_to_string_array', array_ext.info_to_string_array)
ll.add_symbol('info_to_numpy_array', array_ext.info_to_numpy_array)
ll.add_symbol('info_to_nullable_array', array_ext.info_to_nullable_array)
ll.add_symbol('info_to_interval_array', array_ext.info_to_interval_array)
ll.add_symbol('alloc_numpy', array_ext.alloc_numpy)
ll.add_symbol('alloc_string_array', array_ext.alloc_string_array)
ll.add_symbol('arr_info_list_to_table', array_ext.arr_info_list_to_table)
ll.add_symbol('info_from_table', array_ext.info_from_table)
ll.add_symbol('delete_info_decref_array', array_ext.delete_info_decref_array)
ll.add_symbol('delete_table_decref_arrays', array_ext.
    delete_table_decref_arrays)
ll.add_symbol('delete_table', array_ext.delete_table)
ll.add_symbol('shuffle_table', array_ext.shuffle_table)
ll.add_symbol('get_shuffle_info', array_ext.get_shuffle_info)
ll.add_symbol('delete_shuffle_info', array_ext.delete_shuffle_info)
ll.add_symbol('reverse_shuffle_table', array_ext.reverse_shuffle_table)
ll.add_symbol('hash_join_table', array_ext.hash_join_table)
ll.add_symbol('drop_duplicates_table', array_ext.drop_duplicates_table)
ll.add_symbol('sort_values_table', array_ext.sort_values_table)
ll.add_symbol('sample_table', array_ext.sample_table)
ll.add_symbol('shuffle_renormalization', array_ext.shuffle_renormalization)
ll.add_symbol('shuffle_renormalization_group', array_ext.
    shuffle_renormalization_group)
ll.add_symbol('groupby_and_aggregate', array_ext.groupby_and_aggregate)
ll.add_symbol('pivot_groupby_and_aggregate', array_ext.
    pivot_groupby_and_aggregate)
ll.add_symbol('get_groupby_labels', array_ext.get_groupby_labels)
ll.add_symbol('array_isin', array_ext.array_isin)
ll.add_symbol('get_search_regex', array_ext.get_search_regex)
ll.add_symbol('compute_node_partition_by_hash', array_ext.
    compute_node_partition_by_hash)
ll.add_symbol('array_info_getitem', array_ext.array_info_getitem)


class ArrayInfoType(types.Type):

    def __init__(self):
        super(ArrayInfoType, self).__init__(name='ArrayInfoType()')


array_info_type = ArrayInfoType()
register_model(ArrayInfoType)(models.OpaqueModel)


class TableType(types.Type):

    def __init__(self):
        super(TableType, self).__init__(name='TableType()')


table_type = TableType()
register_model(TableType)(models.OpaqueModel)


@intrinsic
def array_to_info(typingctx, arr_type_t=None):

    def codegen(context, builder, sig, args):
        in_arr, = args
        arr_type = arr_type_t
        if isinstance(arr_type, TupleArrayType):
            bgg__pzqfi = context.make_helper(builder, arr_type, in_arr)
            in_arr = bgg__pzqfi.data
            arr_type = StructArrayType(arr_type.data, ('dummy',) * len(
                arr_type.data))
        context.nrt.incref(builder, arr_type, in_arr)
        if isinstance(arr_type, ArrayItemArrayType
            ) and arr_type.dtype == string_array_type:
            fjo__jai = context.make_helper(builder, arr_type, in_arr)
            itlky__tfp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(8).as_pointer()])
            hpo__igkon = cgutils.get_or_insert_function(builder.module,
                itlky__tfp, name='list_string_array_to_info')
            return builder.call(hpo__igkon, [fjo__jai.meminfo])
        if isinstance(arr_type, (ArrayItemArrayType, StructArrayType)):

            def get_types(arr_typ):
                if isinstance(arr_typ, ArrayItemArrayType):
                    return [CTypeEnum.LIST.value] + get_types(arr_typ.dtype)
                elif isinstance(arr_typ, (StructType, StructArrayType)):
                    muskc__erabx = [CTypeEnum.STRUCT.value, len(arr_typ.names)]
                    for znnsz__zzdjc in arr_typ.data:
                        muskc__erabx += get_types(znnsz__zzdjc)
                    return muskc__erabx
                elif isinstance(arr_typ, (types.Array, IntegerArrayType)
                    ) or arr_typ == boolean_array:
                    return get_types(arr_typ.dtype)
                elif arr_typ == string_array_type:
                    return [CTypeEnum.STRING.value]
                elif arr_typ == binary_array_type:
                    return [CTypeEnum.BINARY.value]
                elif isinstance(arr_typ, DecimalArrayType):
                    return [CTypeEnum.Decimal.value, arr_typ.precision,
                        arr_typ.scale]
                else:
                    return [numba_to_c_type(arr_typ)]

            def get_lengths(arr_typ, arr):
                bjiu__ymzhc = context.compile_internal(builder, lambda a:
                    len(a), types.intp(arr_typ), [arr])
                if isinstance(arr_typ, ArrayItemArrayType):
                    shug__tdjxs = _get_array_item_arr_payload(context,
                        builder, arr_typ, arr)
                    beho__zqs = get_lengths(arr_typ.dtype, shug__tdjxs.data)
                    beho__zqs = cgutils.pack_array(builder, [shug__tdjxs.
                        n_arrays] + [builder.extract_value(beho__zqs,
                        yeb__vto) for yeb__vto in range(beho__zqs.type.count)])
                elif isinstance(arr_typ, StructArrayType):
                    shug__tdjxs = _get_struct_arr_payload(context, builder,
                        arr_typ, arr)
                    beho__zqs = []
                    for yeb__vto, znnsz__zzdjc in enumerate(arr_typ.data):
                        pofoa__kah = get_lengths(znnsz__zzdjc, builder.
                            extract_value(shug__tdjxs.data, yeb__vto))
                        beho__zqs += [builder.extract_value(pofoa__kah,
                            khigg__hbsuh) for khigg__hbsuh in range(
                            pofoa__kah.type.count)]
                    beho__zqs = cgutils.pack_array(builder, [bjiu__ymzhc,
                        context.get_constant(types.int64, -1)] + beho__zqs)
                elif isinstance(arr_typ, (IntegerArrayType,
                    DecimalArrayType, types.Array)) or arr_typ in (
                    boolean_array, datetime_date_array_type,
                    string_array_type, binary_array_type):
                    beho__zqs = cgutils.pack_array(builder, [bjiu__ymzhc])
                else:
                    raise RuntimeError(
                        'array_to_info: unsupported type for subarray')
                return beho__zqs

            def get_buffers(arr_typ, arr):
                if isinstance(arr_typ, ArrayItemArrayType):
                    shug__tdjxs = _get_array_item_arr_payload(context,
                        builder, arr_typ, arr)
                    ncfc__mng = get_buffers(arr_typ.dtype, shug__tdjxs.data)
                    igigu__etxj = context.make_array(types.Array(
                        offset_type, 1, 'C'))(context, builder, shug__tdjxs
                        .offsets)
                    oat__uevs = builder.bitcast(igigu__etxj.data, lir.
                        IntType(8).as_pointer())
                    rok__pai = context.make_array(types.Array(types.uint8, 
                        1, 'C'))(context, builder, shug__tdjxs.null_bitmap)
                    dyrja__nuean = builder.bitcast(rok__pai.data, lir.
                        IntType(8).as_pointer())
                    app__cfn = cgutils.pack_array(builder, [oat__uevs,
                        dyrja__nuean] + [builder.extract_value(ncfc__mng,
                        yeb__vto) for yeb__vto in range(ncfc__mng.type.count)])
                elif isinstance(arr_typ, StructArrayType):
                    shug__tdjxs = _get_struct_arr_payload(context, builder,
                        arr_typ, arr)
                    ncfc__mng = []
                    for yeb__vto, znnsz__zzdjc in enumerate(arr_typ.data):
                        xcw__shj = get_buffers(znnsz__zzdjc, builder.
                            extract_value(shug__tdjxs.data, yeb__vto))
                        ncfc__mng += [builder.extract_value(xcw__shj,
                            khigg__hbsuh) for khigg__hbsuh in range(
                            xcw__shj.type.count)]
                    rok__pai = context.make_array(types.Array(types.uint8, 
                        1, 'C'))(context, builder, shug__tdjxs.null_bitmap)
                    dyrja__nuean = builder.bitcast(rok__pai.data, lir.
                        IntType(8).as_pointer())
                    app__cfn = cgutils.pack_array(builder, [dyrja__nuean] +
                        ncfc__mng)
                elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
                    ) or arr_typ in (boolean_array, datetime_date_array_type):
                    hqh__qjriy = arr_typ.dtype
                    if isinstance(arr_typ, DecimalArrayType):
                        hqh__qjriy = int128_type
                    elif arr_typ == datetime_date_array_type:
                        hqh__qjriy = types.int64
                    arr = cgutils.create_struct_proxy(arr_typ)(context,
                        builder, arr)
                    smkg__cgsdq = context.make_array(types.Array(hqh__qjriy,
                        1, 'C'))(context, builder, arr.data)
                    rok__pai = context.make_array(types.Array(types.uint8, 
                        1, 'C'))(context, builder, arr.null_bitmap)
                    mrtsw__fzf = builder.bitcast(smkg__cgsdq.data, lir.
                        IntType(8).as_pointer())
                    dyrja__nuean = builder.bitcast(rok__pai.data, lir.
                        IntType(8).as_pointer())
                    app__cfn = cgutils.pack_array(builder, [dyrja__nuean,
                        mrtsw__fzf])
                elif arr_typ in (string_array_type, binary_array_type):
                    shug__tdjxs = _get_str_binary_arr_payload(context,
                        builder, arr, arr_typ)
                    rndw__oyyy = context.make_helper(builder,
                        offset_arr_type, shug__tdjxs.offsets).data
                    bfr__lqs = context.make_helper(builder, char_arr_type,
                        shug__tdjxs.data).data
                    ojt__whujb = context.make_helper(builder,
                        null_bitmap_arr_type, shug__tdjxs.null_bitmap).data
                    app__cfn = cgutils.pack_array(builder, [builder.bitcast
                        (rndw__oyyy, lir.IntType(8).as_pointer()), builder.
                        bitcast(ojt__whujb, lir.IntType(8).as_pointer()),
                        builder.bitcast(bfr__lqs, lir.IntType(8).as_pointer())]
                        )
                elif isinstance(arr_typ, types.Array):
                    arr = context.make_array(arr_typ)(context, builder, arr)
                    mrtsw__fzf = builder.bitcast(arr.data, lir.IntType(8).
                        as_pointer())
                    pfz__zsyd = lir.Constant(lir.IntType(8).as_pointer(), None)
                    app__cfn = cgutils.pack_array(builder, [pfz__zsyd,
                        mrtsw__fzf])
                else:
                    raise RuntimeError(
                        'array_to_info: unsupported type for subarray ' +
                        str(arr_typ))
                return app__cfn

            def get_field_names(arr_typ):
                vli__qviu = []
                if isinstance(arr_typ, StructArrayType):
                    for kmsxf__fbwon, wth__nfno in zip(arr_typ.dtype.names,
                        arr_typ.data):
                        vli__qviu.append(kmsxf__fbwon)
                        vli__qviu += get_field_names(wth__nfno)
                elif isinstance(arr_typ, ArrayItemArrayType):
                    vli__qviu += get_field_names(arr_typ.dtype)
                return vli__qviu
            muskc__erabx = get_types(arr_type)
            ggb__vyf = cgutils.pack_array(builder, [context.get_constant(
                types.int32, jag__tsbbg) for jag__tsbbg in muskc__erabx])
            cpb__zmuxy = cgutils.alloca_once_value(builder, ggb__vyf)
            beho__zqs = get_lengths(arr_type, in_arr)
            lengths_ptr = cgutils.alloca_once_value(builder, beho__zqs)
            app__cfn = get_buffers(arr_type, in_arr)
            mapf__wgj = cgutils.alloca_once_value(builder, app__cfn)
            vli__qviu = get_field_names(arr_type)
            if len(vli__qviu) == 0:
                vli__qviu = ['irrelevant']
            nfx__ebnhg = cgutils.pack_array(builder, [context.
                insert_const_string(builder.module, a) for a in vli__qviu])
            shktt__gidj = cgutils.alloca_once_value(builder, nfx__ebnhg)
            kxq__vryic = context.make_helper(builder, arr_type, in_arr)
            itlky__tfp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(32).as_pointer(), lir.IntType(8).as_pointer().
                as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer()])
            hpo__igkon = cgutils.get_or_insert_function(builder.module,
                itlky__tfp, name='nested_array_to_info')
            lrqx__wvos = builder.call(hpo__igkon, [builder.bitcast(
                cpb__zmuxy, lir.IntType(32).as_pointer()), builder.bitcast(
                mapf__wgj, lir.IntType(8).as_pointer().as_pointer()),
                builder.bitcast(lengths_ptr, lir.IntType(64).as_pointer()),
                builder.bitcast(shktt__gidj, lir.IntType(8).as_pointer()),
                kxq__vryic.meminfo])
            context.compile_internal(builder, lambda :
                check_and_propagate_cpp_exception(), types.none(), [])
            return lrqx__wvos
        if arr_type in (string_array_type, binary_array_type):
            rigpq__wvc = context.make_helper(builder, arr_type, in_arr)
            qflrg__wsew = ArrayItemArrayType(char_arr_type)
            fjo__jai = context.make_helper(builder, qflrg__wsew, rigpq__wvc
                .data)
            shug__tdjxs = _get_str_binary_arr_payload(context, builder,
                in_arr, arr_type)
            rndw__oyyy = context.make_helper(builder, offset_arr_type,
                shug__tdjxs.offsets).data
            bfr__lqs = context.make_helper(builder, char_arr_type,
                shug__tdjxs.data).data
            ojt__whujb = context.make_helper(builder, null_bitmap_arr_type,
                shug__tdjxs.null_bitmap).data
            lnwc__bsf = builder.zext(builder.load(builder.gep(rndw__oyyy, [
                shug__tdjxs.n_arrays])), lir.IntType(64))
            fgxqd__gpnzu = context.get_constant(types.int32, int(arr_type ==
                binary_array_type))
            itlky__tfp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(64), lir.IntType(8).as_pointer(),
                lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType
                (8).as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32)]
                )
            hpo__igkon = cgutils.get_or_insert_function(builder.module,
                itlky__tfp, name='string_array_to_info')
            return builder.call(hpo__igkon, [shug__tdjxs.n_arrays,
                lnwc__bsf, bfr__lqs, rndw__oyyy, ojt__whujb, fjo__jai.
                meminfo, fgxqd__gpnzu])
        kexzk__gzsfk = False
        if isinstance(arr_type, CategoricalArrayType):
            context.nrt.decref(builder, arr_type, in_arr)
            swh__dyul = context.compile_internal(builder, lambda a: len(a.
                dtype.categories), types.intp(arr_type), [in_arr])
            in_arr = cgutils.create_struct_proxy(arr_type)(context, builder,
                in_arr).codes
            opaxd__gks = get_categories_int_type(arr_type.dtype)
            arr_type = types.Array(opaxd__gks, 1, 'C')
            kexzk__gzsfk = True
            context.nrt.incref(builder, arr_type, in_arr)
        if isinstance(arr_type, types.Array):
            arr = context.make_array(arr_type)(context, builder, in_arr)
            assert arr_type.ndim == 1, 'only 1D array shuffle supported'
            bjiu__ymzhc = builder.extract_value(arr.shape, 0)
            qbnq__ipq = arr_type.dtype
            tcd__qea = numba_to_c_type(qbnq__ipq)
            dptrj__bow = cgutils.alloca_once_value(builder, lir.Constant(
                lir.IntType(32), tcd__qea))
            if kexzk__gzsfk:
                itlky__tfp = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
                    IntType(32), lir.IntType(64), lir.IntType(8).as_pointer()])
                hpo__igkon = cgutils.get_or_insert_function(builder.module,
                    itlky__tfp, name='categorical_array_to_info')
                return builder.call(hpo__igkon, [bjiu__ymzhc, builder.
                    bitcast(arr.data, lir.IntType(8).as_pointer()), builder
                    .load(dptrj__bow), swh__dyul, arr.meminfo])
            else:
                itlky__tfp = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
                    IntType(32), lir.IntType(8).as_pointer()])
                hpo__igkon = cgutils.get_or_insert_function(builder.module,
                    itlky__tfp, name='numpy_array_to_info')
                return builder.call(hpo__igkon, [bjiu__ymzhc, builder.
                    bitcast(arr.data, lir.IntType(8).as_pointer()), builder
                    .load(dptrj__bow), arr.meminfo])
        if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
            ) or arr_type in (boolean_array, datetime_date_array_type):
            arr = cgutils.create_struct_proxy(arr_type)(context, builder,
                in_arr)
            qbnq__ipq = arr_type.dtype
            hqh__qjriy = qbnq__ipq
            if isinstance(arr_type, DecimalArrayType):
                hqh__qjriy = int128_type
            if arr_type == datetime_date_array_type:
                hqh__qjriy = types.int64
            smkg__cgsdq = context.make_array(types.Array(hqh__qjriy, 1, 'C'))(
                context, builder, arr.data)
            bjiu__ymzhc = builder.extract_value(smkg__cgsdq.shape, 0)
            rpm__hsmsk = context.make_array(types.Array(types.uint8, 1, 'C'))(
                context, builder, arr.null_bitmap)
            tcd__qea = numba_to_c_type(qbnq__ipq)
            dptrj__bow = cgutils.alloca_once_value(builder, lir.Constant(
                lir.IntType(32), tcd__qea))
            if isinstance(arr_type, DecimalArrayType):
                itlky__tfp = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
                    IntType(32), lir.IntType(8).as_pointer(), lir.IntType(8
                    ).as_pointer(), lir.IntType(8).as_pointer(), lir.
                    IntType(32), lir.IntType(32)])
                hpo__igkon = cgutils.get_or_insert_function(builder.module,
                    itlky__tfp, name='decimal_array_to_info')
                return builder.call(hpo__igkon, [bjiu__ymzhc, builder.
                    bitcast(smkg__cgsdq.data, lir.IntType(8).as_pointer()),
                    builder.load(dptrj__bow), builder.bitcast(rpm__hsmsk.
                    data, lir.IntType(8).as_pointer()), smkg__cgsdq.meminfo,
                    rpm__hsmsk.meminfo, context.get_constant(types.int32,
                    arr_type.precision), context.get_constant(types.int32,
                    arr_type.scale)])
            else:
                itlky__tfp = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
                    IntType(32), lir.IntType(8).as_pointer(), lir.IntType(8
                    ).as_pointer(), lir.IntType(8).as_pointer()])
                hpo__igkon = cgutils.get_or_insert_function(builder.module,
                    itlky__tfp, name='nullable_array_to_info')
                return builder.call(hpo__igkon, [bjiu__ymzhc, builder.
                    bitcast(smkg__cgsdq.data, lir.IntType(8).as_pointer()),
                    builder.load(dptrj__bow), builder.bitcast(rpm__hsmsk.
                    data, lir.IntType(8).as_pointer()), smkg__cgsdq.meminfo,
                    rpm__hsmsk.meminfo])
        if isinstance(arr_type, IntervalArrayType):
            assert isinstance(arr_type.arr_type, types.Array
                ), 'array_to_info(): only IntervalArrayType with Numpy arrays supported'
            arr = cgutils.create_struct_proxy(arr_type)(context, builder,
                in_arr)
            qwep__jxuqq = context.make_array(arr_type.arr_type)(context,
                builder, arr.left)
            xuj__ryc = context.make_array(arr_type.arr_type)(context,
                builder, arr.right)
            bjiu__ymzhc = builder.extract_value(qwep__jxuqq.shape, 0)
            tcd__qea = numba_to_c_type(arr_type.arr_type.dtype)
            dptrj__bow = cgutils.alloca_once_value(builder, lir.Constant(
                lir.IntType(32), tcd__qea))
            itlky__tfp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir
                .IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer()])
            hpo__igkon = cgutils.get_or_insert_function(builder.module,
                itlky__tfp, name='interval_array_to_info')
            return builder.call(hpo__igkon, [bjiu__ymzhc, builder.bitcast(
                qwep__jxuqq.data, lir.IntType(8).as_pointer()), builder.
                bitcast(xuj__ryc.data, lir.IntType(8).as_pointer()),
                builder.load(dptrj__bow), qwep__jxuqq.meminfo, xuj__ryc.
                meminfo])
        raise BodoError(
            f'array_to_info(): array type {arr_type} is not supported')
    return array_info_type(arr_type_t), codegen


def _lower_info_to_array_numpy(arr_type, context, builder, in_info):
    assert arr_type.ndim == 1, 'only 1D array supported'
    arr = context.make_array(arr_type)(context, builder)
    vxuct__gvyut = cgutils.alloca_once(builder, lir.IntType(64))
    mrtsw__fzf = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    udc__aiyhm = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    itlky__tfp = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    hpo__igkon = cgutils.get_or_insert_function(builder.module, itlky__tfp,
        name='info_to_numpy_array')
    builder.call(hpo__igkon, [in_info, vxuct__gvyut, mrtsw__fzf, udc__aiyhm])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    iiqrh__utz = context.get_value_type(types.intp)
    rqkwz__eop = cgutils.pack_array(builder, [builder.load(vxuct__gvyut)],
        ty=iiqrh__utz)
    tnhrh__theoc = context.get_constant(types.intp, context.get_abi_sizeof(
        context.get_data_type(arr_type.dtype)))
    vuajb__vkr = cgutils.pack_array(builder, [tnhrh__theoc], ty=iiqrh__utz)
    bfr__lqs = builder.bitcast(builder.load(mrtsw__fzf), context.
        get_data_type(arr_type.dtype).as_pointer())
    numba.np.arrayobj.populate_array(arr, data=bfr__lqs, shape=rqkwz__eop,
        strides=vuajb__vkr, itemsize=tnhrh__theoc, meminfo=builder.load(
        udc__aiyhm))
    return arr._getvalue()


def _lower_info_to_array_list_string_array(arr_type, context, builder, in_info
    ):
    umv__quf = context.make_helper(builder, arr_type)
    itlky__tfp = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    hpo__igkon = cgutils.get_or_insert_function(builder.module, itlky__tfp,
        name='info_to_list_string_array')
    builder.call(hpo__igkon, [in_info, umv__quf._get_ptr_by_name('meminfo')])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    return umv__quf._getvalue()


def nested_to_array(context, builder, arr_typ, lengths_ptr, array_infos_ptr,
    lengths_pos, infos_pos):
    nxbw__wnu = context.get_data_type(array_info_type)
    if isinstance(arr_typ, ArrayItemArrayType):
        zkgk__uyql = lengths_pos
        mocoa__mhgzh = infos_pos
        kbyew__huyir, lengths_pos, infos_pos = nested_to_array(context,
            builder, arr_typ.dtype, lengths_ptr, array_infos_ptr, 
            lengths_pos + 1, infos_pos + 2)
        tmtsu__wkvb = ArrayItemArrayPayloadType(arr_typ)
        nnpo__gxg = context.get_data_type(tmtsu__wkvb)
        flvr__uzhjh = context.get_abi_sizeof(nnpo__gxg)
        wcb__hks = define_array_item_dtor(context, builder, arr_typ,
            tmtsu__wkvb)
        qls__kohxf = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, flvr__uzhjh), wcb__hks)
        brh__rqe = context.nrt.meminfo_data(builder, qls__kohxf)
        oubzd__sdc = builder.bitcast(brh__rqe, nnpo__gxg.as_pointer())
        shug__tdjxs = cgutils.create_struct_proxy(tmtsu__wkvb)(context, builder
            )
        shug__tdjxs.n_arrays = builder.extract_value(builder.load(
            lengths_ptr), zkgk__uyql)
        shug__tdjxs.data = kbyew__huyir
        zghya__qhvy = builder.load(array_infos_ptr)
        najg__dsp = builder.bitcast(builder.extract_value(zghya__qhvy,
            mocoa__mhgzh), nxbw__wnu)
        shug__tdjxs.offsets = _lower_info_to_array_numpy(types.Array(
            offset_type, 1, 'C'), context, builder, najg__dsp)
        hcw__luqkd = builder.bitcast(builder.extract_value(zghya__qhvy, 
            mocoa__mhgzh + 1), nxbw__wnu)
        shug__tdjxs.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, hcw__luqkd)
        builder.store(shug__tdjxs._getvalue(), oubzd__sdc)
        fjo__jai = context.make_helper(builder, arr_typ)
        fjo__jai.meminfo = qls__kohxf
        return fjo__jai._getvalue(), lengths_pos, infos_pos
    elif isinstance(arr_typ, StructArrayType):
        sxurt__gkc = []
        mocoa__mhgzh = infos_pos
        lengths_pos += 1
        infos_pos += 1
        for vqys__pvvma in arr_typ.data:
            kbyew__huyir, lengths_pos, infos_pos = nested_to_array(context,
                builder, vqys__pvvma, lengths_ptr, array_infos_ptr,
                lengths_pos, infos_pos)
            sxurt__gkc.append(kbyew__huyir)
        tmtsu__wkvb = StructArrayPayloadType(arr_typ.data)
        nnpo__gxg = context.get_value_type(tmtsu__wkvb)
        flvr__uzhjh = context.get_abi_sizeof(nnpo__gxg)
        wcb__hks = define_struct_arr_dtor(context, builder, arr_typ,
            tmtsu__wkvb)
        qls__kohxf = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, flvr__uzhjh), wcb__hks)
        brh__rqe = context.nrt.meminfo_data(builder, qls__kohxf)
        oubzd__sdc = builder.bitcast(brh__rqe, nnpo__gxg.as_pointer())
        shug__tdjxs = cgutils.create_struct_proxy(tmtsu__wkvb)(context, builder
            )
        shug__tdjxs.data = cgutils.pack_array(builder, sxurt__gkc
            ) if types.is_homogeneous(*arr_typ.data) else cgutils.pack_struct(
            builder, sxurt__gkc)
        zghya__qhvy = builder.load(array_infos_ptr)
        hcw__luqkd = builder.bitcast(builder.extract_value(zghya__qhvy,
            mocoa__mhgzh), nxbw__wnu)
        shug__tdjxs.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, hcw__luqkd)
        builder.store(shug__tdjxs._getvalue(), oubzd__sdc)
        dtugy__mzdo = context.make_helper(builder, arr_typ)
        dtugy__mzdo.meminfo = qls__kohxf
        return dtugy__mzdo._getvalue(), lengths_pos, infos_pos
    elif arr_typ in (string_array_type, binary_array_type):
        zghya__qhvy = builder.load(array_infos_ptr)
        jplrc__ulf = builder.bitcast(builder.extract_value(zghya__qhvy,
            infos_pos), nxbw__wnu)
        rigpq__wvc = context.make_helper(builder, arr_typ)
        qflrg__wsew = ArrayItemArrayType(char_arr_type)
        fjo__jai = context.make_helper(builder, qflrg__wsew)
        itlky__tfp = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        hpo__igkon = cgutils.get_or_insert_function(builder.module,
            itlky__tfp, name='info_to_string_array')
        builder.call(hpo__igkon, [jplrc__ulf, fjo__jai._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        rigpq__wvc.data = fjo__jai._getvalue()
        return rigpq__wvc._getvalue(), lengths_pos + 1, infos_pos + 2
    elif isinstance(arr_typ, types.Array):
        zghya__qhvy = builder.load(array_infos_ptr)
        cky__nitu = builder.bitcast(builder.extract_value(zghya__qhvy, 
            infos_pos + 1), nxbw__wnu)
        return _lower_info_to_array_numpy(arr_typ, context, builder, cky__nitu
            ), lengths_pos + 1, infos_pos + 2
    elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
        ) or arr_typ in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_typ)(context, builder)
        hqh__qjriy = arr_typ.dtype
        if isinstance(arr_typ, DecimalArrayType):
            hqh__qjriy = int128_type
        elif arr_typ == datetime_date_array_type:
            hqh__qjriy = types.int64
        zghya__qhvy = builder.load(array_infos_ptr)
        hcw__luqkd = builder.bitcast(builder.extract_value(zghya__qhvy,
            infos_pos), nxbw__wnu)
        arr.null_bitmap = _lower_info_to_array_numpy(types.Array(types.
            uint8, 1, 'C'), context, builder, hcw__luqkd)
        cky__nitu = builder.bitcast(builder.extract_value(zghya__qhvy, 
            infos_pos + 1), nxbw__wnu)
        arr.data = _lower_info_to_array_numpy(types.Array(hqh__qjriy, 1,
            'C'), context, builder, cky__nitu)
        return arr._getvalue(), lengths_pos + 1, infos_pos + 2


@intrinsic
def info_to_array(typingctx, info_type, array_type):
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    assert info_type == array_info_type

    def codegen(context, builder, sig, args):
        in_info, eorfp__azc = args
        if isinstance(arr_type, ArrayItemArrayType
            ) and arr_type.dtype == string_array_type:
            return _lower_info_to_array_list_string_array(arr_type, context,
                builder, in_info)
        if isinstance(arr_type, (ArrayItemArrayType, StructArrayType,
            TupleArrayType)):

            def get_num_arrays(arr_typ):
                if isinstance(arr_typ, ArrayItemArrayType):
                    return 1 + get_num_arrays(arr_typ.dtype)
                elif isinstance(arr_typ, StructArrayType):
                    return 1 + sum([get_num_arrays(vqys__pvvma) for
                        vqys__pvvma in arr_typ.data])
                else:
                    return 1

            def get_num_infos(arr_typ):
                if isinstance(arr_typ, ArrayItemArrayType):
                    return 2 + get_num_infos(arr_typ.dtype)
                elif isinstance(arr_typ, StructArrayType):
                    return 1 + sum([get_num_infos(vqys__pvvma) for
                        vqys__pvvma in arr_typ.data])
                elif arr_typ in (string_array_type, binary_array_type):
                    return 1
                else:
                    return 2
            if isinstance(arr_type, TupleArrayType):
                ksz__hbp = StructArrayType(arr_type.data, ('dummy',) * len(
                    arr_type.data))
            else:
                ksz__hbp = arr_type
            rrp__abul = get_num_arrays(ksz__hbp)
            beho__zqs = cgutils.pack_array(builder, [lir.Constant(lir.
                IntType(64), 0) for eorfp__azc in range(rrp__abul)])
            lengths_ptr = cgutils.alloca_once_value(builder, beho__zqs)
            pfz__zsyd = lir.Constant(lir.IntType(8).as_pointer(), None)
            cvgcn__gxxk = cgutils.pack_array(builder, [pfz__zsyd for
                eorfp__azc in range(get_num_infos(ksz__hbp))])
            array_infos_ptr = cgutils.alloca_once_value(builder, cvgcn__gxxk)
            itlky__tfp = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
                as_pointer().as_pointer()])
            hpo__igkon = cgutils.get_or_insert_function(builder.module,
                itlky__tfp, name='info_to_nested_array')
            builder.call(hpo__igkon, [in_info, builder.bitcast(lengths_ptr,
                lir.IntType(64).as_pointer()), builder.bitcast(
                array_infos_ptr, lir.IntType(8).as_pointer().as_pointer())])
            context.compile_internal(builder, lambda :
                check_and_propagate_cpp_exception(), types.none(), [])
            arr, eorfp__azc, eorfp__azc = nested_to_array(context, builder,
                ksz__hbp, lengths_ptr, array_infos_ptr, 0, 0)
            if isinstance(arr_type, TupleArrayType):
                bgg__pzqfi = context.make_helper(builder, arr_type)
                bgg__pzqfi.data = arr
                context.nrt.incref(builder, ksz__hbp, arr)
                arr = bgg__pzqfi._getvalue()
            return arr
        if arr_type in (string_array_type, binary_array_type):
            rigpq__wvc = context.make_helper(builder, arr_type)
            qflrg__wsew = ArrayItemArrayType(char_arr_type)
            fjo__jai = context.make_helper(builder, qflrg__wsew)
            itlky__tfp = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
            hpo__igkon = cgutils.get_or_insert_function(builder.module,
                itlky__tfp, name='info_to_string_array')
            builder.call(hpo__igkon, [in_info, fjo__jai._get_ptr_by_name(
                'meminfo')])
            context.compile_internal(builder, lambda :
                check_and_propagate_cpp_exception(), types.none(), [])
            rigpq__wvc.data = fjo__jai._getvalue()
            return rigpq__wvc._getvalue()
        if isinstance(arr_type, CategoricalArrayType):
            out_arr = cgutils.create_struct_proxy(arr_type)(context, builder)
            opaxd__gks = get_categories_int_type(arr_type.dtype)
            jtiu__cwk = types.Array(opaxd__gks, 1, 'C')
            out_arr.codes = _lower_info_to_array_numpy(jtiu__cwk, context,
                builder, in_info)
            if isinstance(array_type, types.TypeRef):
                assert arr_type.dtype.categories is not None, 'info_to_array: unknown categories'
                aylw__gyz = pd.CategoricalDtype(arr_type.dtype.categories,
                    arr_type.dtype.ordered)
                qbnq__ipq = context.get_constant_generic(builder, arr_type.
                    dtype, aylw__gyz)
            else:
                qbnq__ipq = cgutils.create_struct_proxy(arr_type)(context,
                    builder, args[1]).dtype
            out_arr.dtype = qbnq__ipq
            context.nrt.incref(builder, arr_type.dtype, qbnq__ipq)
            return out_arr._getvalue()
        if isinstance(arr_type, types.Array):
            return _lower_info_to_array_numpy(arr_type, context, builder,
                in_info)
        if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
            ) or arr_type in (boolean_array, datetime_date_array_type):
            arr = cgutils.create_struct_proxy(arr_type)(context, builder)
            hqh__qjriy = arr_type.dtype
            if isinstance(arr_type, DecimalArrayType):
                hqh__qjriy = int128_type
            elif arr_type == datetime_date_array_type:
                hqh__qjriy = types.int64
            ngajn__yfuf = types.Array(hqh__qjriy, 1, 'C')
            smkg__cgsdq = context.make_array(ngajn__yfuf)(context, builder)
            fcg__aot = types.Array(types.uint8, 1, 'C')
            wtpze__hkkg = context.make_array(fcg__aot)(context, builder)
            vxuct__gvyut = cgutils.alloca_once(builder, lir.IntType(64))
            jtvj__ygue = cgutils.alloca_once(builder, lir.IntType(64))
            mrtsw__fzf = cgutils.alloca_once(builder, lir.IntType(8).
                as_pointer())
            jburk__sqi = cgutils.alloca_once(builder, lir.IntType(8).
                as_pointer())
            udc__aiyhm = cgutils.alloca_once(builder, lir.IntType(8).
                as_pointer())
            dxaa__ovkax = cgutils.alloca_once(builder, lir.IntType(8).
                as_pointer())
            itlky__tfp = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64)
                .as_pointer(), lir.IntType(8).as_pointer().as_pointer(),
                lir.IntType(8).as_pointer().as_pointer(), lir.IntType(8).
                as_pointer().as_pointer(), lir.IntType(8).as_pointer().
                as_pointer()])
            hpo__igkon = cgutils.get_or_insert_function(builder.module,
                itlky__tfp, name='info_to_nullable_array')
            builder.call(hpo__igkon, [in_info, vxuct__gvyut, jtvj__ygue,
                mrtsw__fzf, jburk__sqi, udc__aiyhm, dxaa__ovkax])
            context.compile_internal(builder, lambda :
                check_and_propagate_cpp_exception(), types.none(), [])
            iiqrh__utz = context.get_value_type(types.intp)
            rqkwz__eop = cgutils.pack_array(builder, [builder.load(
                vxuct__gvyut)], ty=iiqrh__utz)
            tnhrh__theoc = context.get_constant(types.intp, context.
                get_abi_sizeof(context.get_data_type(hqh__qjriy)))
            vuajb__vkr = cgutils.pack_array(builder, [tnhrh__theoc], ty=
                iiqrh__utz)
            bfr__lqs = builder.bitcast(builder.load(mrtsw__fzf), context.
                get_data_type(hqh__qjriy).as_pointer())
            numba.np.arrayobj.populate_array(smkg__cgsdq, data=bfr__lqs,
                shape=rqkwz__eop, strides=vuajb__vkr, itemsize=tnhrh__theoc,
                meminfo=builder.load(udc__aiyhm))
            arr.data = smkg__cgsdq._getvalue()
            rqkwz__eop = cgutils.pack_array(builder, [builder.load(
                jtvj__ygue)], ty=iiqrh__utz)
            tnhrh__theoc = context.get_constant(types.intp, context.
                get_abi_sizeof(context.get_data_type(types.uint8)))
            vuajb__vkr = cgutils.pack_array(builder, [tnhrh__theoc], ty=
                iiqrh__utz)
            bfr__lqs = builder.bitcast(builder.load(jburk__sqi), context.
                get_data_type(types.uint8).as_pointer())
            numba.np.arrayobj.populate_array(wtpze__hkkg, data=bfr__lqs,
                shape=rqkwz__eop, strides=vuajb__vkr, itemsize=tnhrh__theoc,
                meminfo=builder.load(dxaa__ovkax))
            arr.null_bitmap = wtpze__hkkg._getvalue()
            return arr._getvalue()
        if isinstance(arr_type, IntervalArrayType):
            arr = cgutils.create_struct_proxy(arr_type)(context, builder)
            qwep__jxuqq = context.make_array(arr_type.arr_type)(context,
                builder)
            xuj__ryc = context.make_array(arr_type.arr_type)(context, builder)
            vxuct__gvyut = cgutils.alloca_once(builder, lir.IntType(64))
            mdvg__ezjw = cgutils.alloca_once(builder, lir.IntType(8).
                as_pointer())
            tdnp__aqn = cgutils.alloca_once(builder, lir.IntType(8).
                as_pointer())
            ezbcx__akh = cgutils.alloca_once(builder, lir.IntType(8).
                as_pointer())
            zjbfl__ewe = cgutils.alloca_once(builder, lir.IntType(8).
                as_pointer())
            itlky__tfp = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
                as_pointer().as_pointer(), lir.IntType(8).as_pointer().
                as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir
                .IntType(8).as_pointer().as_pointer()])
            hpo__igkon = cgutils.get_or_insert_function(builder.module,
                itlky__tfp, name='info_to_interval_array')
            builder.call(hpo__igkon, [in_info, vxuct__gvyut, mdvg__ezjw,
                tdnp__aqn, ezbcx__akh, zjbfl__ewe])
            context.compile_internal(builder, lambda :
                check_and_propagate_cpp_exception(), types.none(), [])
            iiqrh__utz = context.get_value_type(types.intp)
            rqkwz__eop = cgutils.pack_array(builder, [builder.load(
                vxuct__gvyut)], ty=iiqrh__utz)
            tnhrh__theoc = context.get_constant(types.intp, context.
                get_abi_sizeof(context.get_data_type(arr_type.arr_type.dtype)))
            vuajb__vkr = cgutils.pack_array(builder, [tnhrh__theoc], ty=
                iiqrh__utz)
            nocwu__vob = builder.bitcast(builder.load(mdvg__ezjw), context.
                get_data_type(arr_type.arr_type.dtype).as_pointer())
            numba.np.arrayobj.populate_array(qwep__jxuqq, data=nocwu__vob,
                shape=rqkwz__eop, strides=vuajb__vkr, itemsize=tnhrh__theoc,
                meminfo=builder.load(ezbcx__akh))
            arr.left = qwep__jxuqq._getvalue()
            qbvgt__hbyd = builder.bitcast(builder.load(tdnp__aqn), context.
                get_data_type(arr_type.arr_type.dtype).as_pointer())
            numba.np.arrayobj.populate_array(xuj__ryc, data=qbvgt__hbyd,
                shape=rqkwz__eop, strides=vuajb__vkr, itemsize=tnhrh__theoc,
                meminfo=builder.load(zjbfl__ewe))
            arr.right = xuj__ryc._getvalue()
            return arr._getvalue()
        raise BodoError(
            f'info_to_array(): array type {arr_type} is not supported')
    return arr_type(info_type, array_type), codegen


@intrinsic
def test_alloc_np(typingctx, len_typ, arr_type):
    array_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type

    def codegen(context, builder, sig, args):
        bjiu__ymzhc, eorfp__azc = args
        tcd__qea = numba_to_c_type(array_type.dtype)
        dptrj__bow = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), tcd__qea))
        itlky__tfp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(32)])
        hpo__igkon = cgutils.get_or_insert_function(builder.module,
            itlky__tfp, name='alloc_numpy')
        return builder.call(hpo__igkon, [bjiu__ymzhc, builder.load(dptrj__bow)]
            )
    return array_info_type(len_typ, arr_type), codegen


@intrinsic
def test_alloc_string(typingctx, len_typ, n_chars_typ):

    def codegen(context, builder, sig, args):
        bjiu__ymzhc, vst__bcyr = args
        itlky__tfp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64)])
        hpo__igkon = cgutils.get_or_insert_function(builder.module,
            itlky__tfp, name='alloc_string_array')
        return builder.call(hpo__igkon, [bjiu__ymzhc, vst__bcyr])
    return array_info_type(len_typ, n_chars_typ), codegen


@intrinsic
def arr_info_list_to_table(typingctx, list_arr_info_typ=None):
    assert list_arr_info_typ == types.List(array_info_type)

    def codegen(context, builder, sig, args):
        zgx__tme, = args
        ltcht__reglj = numba.cpython.listobj.ListInstance(context, builder,
            sig.args[0], zgx__tme)
        itlky__tfp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer().as_pointer(), lir.IntType(64)])
        hpo__igkon = cgutils.get_or_insert_function(builder.module,
            itlky__tfp, name='arr_info_list_to_table')
        return builder.call(hpo__igkon, [ltcht__reglj.data, ltcht__reglj.size])
    return table_type(list_arr_info_typ), codegen


@intrinsic
def info_from_table(typingctx, table_t, ind_t):

    def codegen(context, builder, sig, args):
        itlky__tfp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        hpo__igkon = cgutils.get_or_insert_function(builder.module,
            itlky__tfp, name='info_from_table')
        return builder.call(hpo__igkon, args)
    return array_info_type(table_t, ind_t), codegen


delete_info_decref_array = types.ExternalFunction('delete_info_decref_array',
    types.void(array_info_type))
delete_table_decref_arrays = types.ExternalFunction(
    'delete_table_decref_arrays', types.void(table_type))


@intrinsic
def delete_table(typingctx, table_t=None):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        itlky__tfp = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        hpo__igkon = cgutils.get_or_insert_function(builder.module,
            itlky__tfp, name='delete_table')
        builder.call(hpo__igkon, args)
    return types.void(table_t), codegen


@intrinsic
def shuffle_table(typingctx, table_t, n_keys_t, _is_parallel, keep_comm_info_t
    ):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        itlky__tfp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(32)])
        hpo__igkon = cgutils.get_or_insert_function(builder.module,
            itlky__tfp, name='shuffle_table')
        lrqx__wvos = builder.call(hpo__igkon, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return lrqx__wvos
    return table_type(table_t, types.int64, types.boolean, types.int32
        ), codegen


class ShuffleInfoType(types.Type):

    def __init__(self):
        super(ShuffleInfoType, self).__init__(name='ShuffleInfoType()')


shuffle_info_type = ShuffleInfoType()
register_model(ShuffleInfoType)(models.OpaqueModel)
get_shuffle_info = types.ExternalFunction('get_shuffle_info',
    shuffle_info_type(table_type))
delete_shuffle_info = types.ExternalFunction('delete_shuffle_info', types.
    void(shuffle_info_type))
reverse_shuffle_table = types.ExternalFunction('reverse_shuffle_table',
    table_type(table_type, shuffle_info_type))


@intrinsic
def hash_join_table(typingctx, left_table_t, right_table_t, left_parallel_t,
    right_parallel_t, n_keys_t, n_data_left_t, n_data_right_t, same_vect_t,
    same_need_typechange_t, is_left_t, is_right_t, is_join_t,
    optional_col_t, indicator, _bodo_na_equal, cond_func, left_col_nums,
    left_col_nums_len, right_col_nums, right_col_nums_len):
    assert left_table_t == table_type
    assert right_table_t == table_type

    def codegen(context, builder, sig, args):
        itlky__tfp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(64), lir.IntType(64),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(1), lir.IntType(1), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(8).as_pointer(), lir.IntType(64)])
        hpo__igkon = cgutils.get_or_insert_function(builder.module,
            itlky__tfp, name='hash_join_table')
        lrqx__wvos = builder.call(hpo__igkon, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return lrqx__wvos
    return table_type(left_table_t, right_table_t, types.boolean, types.
        boolean, types.int64, types.int64, types.int64, types.voidptr,
        types.voidptr, types.boolean, types.boolean, types.boolean, types.
        boolean, types.boolean, types.boolean, types.voidptr, types.voidptr,
        types.int64, types.voidptr, types.int64), codegen


@intrinsic
def compute_node_partition_by_hash(typingctx, table_t, n_keys_t, n_pes_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        itlky__tfp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(64)])
        hpo__igkon = cgutils.get_or_insert_function(builder.module,
            itlky__tfp, name='compute_node_partition_by_hash')
        lrqx__wvos = builder.call(hpo__igkon, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return lrqx__wvos
    return table_type(table_t, types.int64, types.int64), codegen


@intrinsic
def sort_values_table(typingctx, table_t, n_keys_t, vect_ascending_t,
    na_position_b_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        itlky__tfp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        hpo__igkon = cgutils.get_or_insert_function(builder.module,
            itlky__tfp, name='sort_values_table')
        lrqx__wvos = builder.call(hpo__igkon, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return lrqx__wvos
    return table_type(table_t, types.int64, types.voidptr, types.voidptr,
        types.boolean), codegen


@intrinsic
def sample_table(typingctx, table_t, n_keys_t, frac_t, replace_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        itlky__tfp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.DoubleType(), lir
            .IntType(1), lir.IntType(1)])
        hpo__igkon = cgutils.get_or_insert_function(builder.module,
            itlky__tfp, name='sample_table')
        lrqx__wvos = builder.call(hpo__igkon, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return lrqx__wvos
    return table_type(table_t, types.int64, types.float64, types.boolean,
        types.boolean), codegen


@intrinsic
def shuffle_renormalization(typingctx, table_t, random_t, random_seed_t,
    is_parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        itlky__tfp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1)])
        hpo__igkon = cgutils.get_or_insert_function(builder.module,
            itlky__tfp, name='shuffle_renormalization')
        lrqx__wvos = builder.call(hpo__igkon, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return lrqx__wvos
    return table_type(table_t, types.int32, types.int64, types.boolean
        ), codegen


@intrinsic
def shuffle_renormalization_group(typingctx, table_t, random_t,
    random_seed_t, is_parallel_t, num_ranks_t, ranks_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        itlky__tfp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1), lir.IntType(64), lir.IntType(8).as_pointer()])
        hpo__igkon = cgutils.get_or_insert_function(builder.module,
            itlky__tfp, name='shuffle_renormalization_group')
        lrqx__wvos = builder.call(hpo__igkon, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return lrqx__wvos
    return table_type(table_t, types.int32, types.int64, types.boolean,
        types.int64, types.voidptr), codegen


@intrinsic
def drop_duplicates_table(typingctx, table_t, parallel_t, nkey_t, keep_t,
    ncols, dropna):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        itlky__tfp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(64), lir.IntType(64), lir.IntType(1)])
        hpo__igkon = cgutils.get_or_insert_function(builder.module,
            itlky__tfp, name='drop_duplicates_table')
        lrqx__wvos = builder.call(hpo__igkon, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return lrqx__wvos
    return table_type(table_t, types.boolean, types.int64, types.int64,
        types.int64, types.boolean), codegen


@intrinsic
def pivot_groupby_and_aggregate(typingctx, table_t, n_keys_t,
    dispatch_table_t, dispatch_info_t, input_has_index, ftypes,
    func_offsets, udf_n_redvars, is_parallel, is_crosstab, skipdropna_t,
    return_keys, return_index, update_cb, combine_cb, eval_cb,
    udf_table_dummy_t):
    assert table_t == table_type
    assert dispatch_table_t == table_type
    assert dispatch_info_t == table_type
    assert udf_table_dummy_t == table_type

    def codegen(context, builder, sig, args):
        itlky__tfp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        hpo__igkon = cgutils.get_or_insert_function(builder.module,
            itlky__tfp, name='pivot_groupby_and_aggregate')
        lrqx__wvos = builder.call(hpo__igkon, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return lrqx__wvos
    return table_type(table_t, types.int64, table_t, table_t, types.boolean,
        types.voidptr, types.voidptr, types.voidptr, types.boolean, types.
        boolean, types.boolean, types.boolean, types.boolean, types.voidptr,
        types.voidptr, types.voidptr, table_t), codegen


@intrinsic
def groupby_and_aggregate(typingctx, table_t, n_keys_t, input_has_index,
    ftypes, func_offsets, udf_n_redvars, is_parallel, skipdropna_t,
    shift_periods_t, transform_func, return_keys, return_index, dropna,
    update_cb, combine_cb, eval_cb, general_udfs_cb, udf_table_dummy_t):
    assert table_t == table_type
    assert udf_table_dummy_t == table_type

    def codegen(context, builder, sig, args):
        itlky__tfp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(64), lir.IntType(1), lir.IntType(1),
            lir.IntType(1), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        hpo__igkon = cgutils.get_or_insert_function(builder.module,
            itlky__tfp, name='groupby_and_aggregate')
        lrqx__wvos = builder.call(hpo__igkon, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return lrqx__wvos
    return table_type(table_t, types.int64, types.boolean, types.voidptr,
        types.voidptr, types.voidptr, types.boolean, types.boolean, types.
        int64, types.int64, types.boolean, types.boolean, types.boolean,
        types.voidptr, types.voidptr, types.voidptr, types.voidptr, table_t
        ), codegen


get_groupby_labels = types.ExternalFunction('get_groupby_labels', types.
    int64(table_type, types.voidptr, types.voidptr, types.boolean, types.bool_)
    )
_array_isin = types.ExternalFunction('array_isin', types.void(
    array_info_type, array_info_type, array_info_type, types.bool_))


@numba.njit
def array_isin(out_arr, in_arr, in_values, is_parallel):
    crky__jyqc = array_to_info(in_arr)
    zvr__vpslo = array_to_info(in_values)
    sxand__xho = array_to_info(out_arr)
    tlkt__thkgp = arr_info_list_to_table([crky__jyqc, zvr__vpslo, sxand__xho])
    _array_isin(sxand__xho, crky__jyqc, zvr__vpslo, is_parallel)
    check_and_propagate_cpp_exception()
    delete_table(tlkt__thkgp)


_get_search_regex = types.ExternalFunction('get_search_regex', types.void(
    array_info_type, types.bool_, types.voidptr, array_info_type))


@numba.njit
def get_search_regex(in_arr, case, pat, out_arr):
    crky__jyqc = array_to_info(in_arr)
    sxand__xho = array_to_info(out_arr)
    _get_search_regex(crky__jyqc, case, pat, sxand__xho)
    check_and_propagate_cpp_exception()


def _gen_row_access_intrinsic(col_dtype, c_ind):
    from llvmlite import ir as lir
    if isinstance(col_dtype, types.Number) or col_dtype in [bodo.
        datetime_date_type, bodo.datetime64ns, bodo.timedelta64ns, types.bool_
        ]:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                utq__ayldt, czg__byg = args
                utq__ayldt = builder.bitcast(utq__ayldt, lir.IntType(8).
                    as_pointer().as_pointer())
                mbzy__dyig = lir.Constant(lir.IntType(64), c_ind)
                tkw__bbh = builder.load(builder.gep(utq__ayldt, [mbzy__dyig]))
                tkw__bbh = builder.bitcast(tkw__bbh, context.get_data_type(
                    col_dtype).as_pointer())
                return builder.load(builder.gep(tkw__bbh, [czg__byg]))
            return col_dtype(types.voidptr, types.int64), codegen
        return getitem_func
    if col_dtype == types.unicode_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                utq__ayldt, czg__byg = args
                itlky__tfp = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64), lir.IntType(64).as_pointer()])
                nyq__qxr = cgutils.get_or_insert_function(builder.module,
                    itlky__tfp, name='array_info_getitem')
                mbzy__dyig = lir.Constant(lir.IntType(64), c_ind)
                hod__ywdwk = cgutils.alloca_once(builder, lir.IntType(64))
                args = utq__ayldt, mbzy__dyig, czg__byg, hod__ywdwk
                mrtsw__fzf = builder.call(nyq__qxr, args)
                return context.make_tuple(builder, sig.return_type, [
                    mrtsw__fzf, builder.load(hod__ywdwk)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    raise BodoError(
        f"General Join Conditions with '{col_dtype}' column data type not supported"
        )


def _gen_row_na_check_intrinsic(col_array_dtype, c_ind):
    if isinstance(col_array_dtype, bodo.libs.int_arr_ext.IntegerArrayType
        ) or col_array_dtype in [bodo.libs.bool_arr_ext.boolean_array, bodo
        .libs.str_arr_ext.string_array_type] or isinstance(col_array_dtype,
        types.Array) and col_array_dtype.dtype == bodo.datetime_date_type:

        @intrinsic
        def checkna_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                tawk__jqibx, czg__byg = args
                tawk__jqibx = builder.bitcast(tawk__jqibx, lir.IntType(8).
                    as_pointer().as_pointer())
                mbzy__dyig = lir.Constant(lir.IntType(64), c_ind)
                tkw__bbh = builder.load(builder.gep(tawk__jqibx, [mbzy__dyig]))
                ojt__whujb = builder.bitcast(tkw__bbh, context.
                    get_data_type(types.bool_).as_pointer())
                vjgm__yxd = bodo.utils.cg_helpers.get_bitmap_bit(builder,
                    ojt__whujb, czg__byg)
                qoo__itf = builder.icmp_unsigned('!=', vjgm__yxd, lir.
                    Constant(lir.IntType(8), 0))
                return builder.sext(qoo__itf, lir.IntType(8))
            return types.int8(types.voidptr, types.int64), codegen
        return checkna_func
    elif isinstance(col_array_dtype, types.Array):
        col_dtype = col_array_dtype.dtype
        if col_dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    utq__ayldt, czg__byg = args
                    utq__ayldt = builder.bitcast(utq__ayldt, lir.IntType(8)
                        .as_pointer().as_pointer())
                    mbzy__dyig = lir.Constant(lir.IntType(64), c_ind)
                    tkw__bbh = builder.load(builder.gep(utq__ayldt, [
                        mbzy__dyig]))
                    tkw__bbh = builder.bitcast(tkw__bbh, context.
                        get_data_type(col_dtype).as_pointer())
                    pgg__mep = builder.load(builder.gep(tkw__bbh, [czg__byg]))
                    qoo__itf = builder.icmp_unsigned('!=', pgg__mep, lir.
                        Constant(lir.IntType(64), pd._libs.iNaT))
                    return builder.sext(qoo__itf, lir.IntType(8))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
        elif isinstance(col_dtype, types.Float):

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    utq__ayldt, czg__byg = args
                    utq__ayldt = builder.bitcast(utq__ayldt, lir.IntType(8)
                        .as_pointer().as_pointer())
                    mbzy__dyig = lir.Constant(lir.IntType(64), c_ind)
                    tkw__bbh = builder.load(builder.gep(utq__ayldt, [
                        mbzy__dyig]))
                    tkw__bbh = builder.bitcast(tkw__bbh, context.
                        get_data_type(col_dtype).as_pointer())
                    pgg__mep = builder.load(builder.gep(tkw__bbh, [czg__byg]))
                    jlrog__kpu = signature(types.bool_, col_dtype)
                    vjgm__yxd = numba.np.npyfuncs.np_real_isnan_impl(context,
                        builder, jlrog__kpu, (pgg__mep,))
                    return builder.not_(builder.sext(vjgm__yxd, lir.IntType(8))
                        )
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
    raise BodoError(
        f"General Join Conditions with '{col_array_dtype}' column type not supported"
        )
