"""helper functions for code generation with llvmlite
"""
import llvmlite.binding as ll
from llvmlite import ir as lir
from numba.core import cgutils, types
import bodo
from bodo.libs import array_ext, hdist
ll.add_symbol('array_getitem', array_ext.array_getitem)
ll.add_symbol('seq_getitem', array_ext.seq_getitem)
ll.add_symbol('list_check', array_ext.list_check)
ll.add_symbol('dict_keys', array_ext.dict_keys)
ll.add_symbol('dict_values', array_ext.dict_values)
ll.add_symbol('dict_merge_from_seq2', array_ext.dict_merge_from_seq2)
ll.add_symbol('is_na_value', array_ext.is_na_value)


def set_bitmap_bit(builder, null_bitmap_ptr, ind, val):
    theil__stsu = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    hbtf__szj = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    cvjy__gpdqj = builder.gep(null_bitmap_ptr, [theil__stsu], inbounds=True)
    ebwmr__nae = builder.load(cvjy__gpdqj)
    xkrop__ioomm = lir.ArrayType(lir.IntType(8), 8)
    ivpb__zon = cgutils.alloca_once_value(builder, lir.Constant(
        xkrop__ioomm, (1, 2, 4, 8, 16, 32, 64, 128)))
    hujai__jqxzv = builder.load(builder.gep(ivpb__zon, [lir.Constant(lir.
        IntType(64), 0), hbtf__szj], inbounds=True))
    if val:
        builder.store(builder.or_(ebwmr__nae, hujai__jqxzv), cvjy__gpdqj)
    else:
        hujai__jqxzv = builder.xor(hujai__jqxzv, lir.Constant(lir.IntType(8
            ), -1))
        builder.store(builder.and_(ebwmr__nae, hujai__jqxzv), cvjy__gpdqj)


def get_bitmap_bit(builder, null_bitmap_ptr, ind):
    theil__stsu = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    hbtf__szj = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    ebwmr__nae = builder.load(builder.gep(null_bitmap_ptr, [theil__stsu],
        inbounds=True))
    xkrop__ioomm = lir.ArrayType(lir.IntType(8), 8)
    ivpb__zon = cgutils.alloca_once_value(builder, lir.Constant(
        xkrop__ioomm, (1, 2, 4, 8, 16, 32, 64, 128)))
    hujai__jqxzv = builder.load(builder.gep(ivpb__zon, [lir.Constant(lir.
        IntType(64), 0), hbtf__szj], inbounds=True))
    return builder.and_(ebwmr__nae, hujai__jqxzv)


def pyarray_getitem(builder, context, arr_obj, ind):
    phr__baq = context.get_argument_type(types.pyobject)
    asnp__dbon = context.get_value_type(types.intp)
    frl__dkk = lir.FunctionType(lir.IntType(8).as_pointer(), [phr__baq,
        asnp__dbon])
    ncczl__utzum = cgutils.get_or_insert_function(builder.module, frl__dkk,
        name='array_getptr1')
    unw__zan = lir.FunctionType(phr__baq, [phr__baq, lir.IntType(8).
        as_pointer()])
    cgds__zcfrd = cgutils.get_or_insert_function(builder.module, unw__zan,
        name='array_getitem')
    jvd__vigoo = builder.call(ncczl__utzum, [arr_obj, ind])
    return builder.call(cgds__zcfrd, [arr_obj, jvd__vigoo])


def pyarray_setitem(builder, context, arr_obj, ind, val_obj):
    phr__baq = context.get_argument_type(types.pyobject)
    asnp__dbon = context.get_value_type(types.intp)
    frl__dkk = lir.FunctionType(lir.IntType(8).as_pointer(), [phr__baq,
        asnp__dbon])
    ncczl__utzum = cgutils.get_or_insert_function(builder.module, frl__dkk,
        name='array_getptr1')
    kwx__mumsl = lir.FunctionType(lir.VoidType(), [phr__baq, lir.IntType(8)
        .as_pointer(), phr__baq])
    cignc__eil = cgutils.get_or_insert_function(builder.module, kwx__mumsl,
        name='array_setitem')
    jvd__vigoo = builder.call(ncczl__utzum, [arr_obj, ind])
    builder.call(cignc__eil, [arr_obj, jvd__vigoo, val_obj])


def seq_getitem(builder, context, obj, ind):
    phr__baq = context.get_argument_type(types.pyobject)
    asnp__dbon = context.get_value_type(types.intp)
    ekwst__lgoy = lir.FunctionType(phr__baq, [phr__baq, asnp__dbon])
    rlj__wzp = cgutils.get_or_insert_function(builder.module, ekwst__lgoy,
        name='seq_getitem')
    return builder.call(rlj__wzp, [obj, ind])


def is_na_value(builder, context, val, C_NA):
    phr__baq = context.get_argument_type(types.pyobject)
    tcu__ckckp = lir.FunctionType(lir.IntType(32), [phr__baq, phr__baq])
    ohra__bqtm = cgutils.get_or_insert_function(builder.module, tcu__ckckp,
        name='is_na_value')
    return builder.call(ohra__bqtm, [val, C_NA])


def list_check(builder, context, obj):
    phr__baq = context.get_argument_type(types.pyobject)
    tcqx__acro = context.get_value_type(types.int32)
    wtr__wxri = lir.FunctionType(tcqx__acro, [phr__baq])
    mkqi__ywjng = cgutils.get_or_insert_function(builder.module, wtr__wxri,
        name='list_check')
    return builder.call(mkqi__ywjng, [obj])


def dict_keys(builder, context, obj):
    phr__baq = context.get_argument_type(types.pyobject)
    wtr__wxri = lir.FunctionType(phr__baq, [phr__baq])
    mkqi__ywjng = cgutils.get_or_insert_function(builder.module, wtr__wxri,
        name='dict_keys')
    return builder.call(mkqi__ywjng, [obj])


def dict_values(builder, context, obj):
    phr__baq = context.get_argument_type(types.pyobject)
    wtr__wxri = lir.FunctionType(phr__baq, [phr__baq])
    mkqi__ywjng = cgutils.get_or_insert_function(builder.module, wtr__wxri,
        name='dict_values')
    return builder.call(mkqi__ywjng, [obj])


def dict_merge_from_seq2(builder, context, dict_obj, seq2_obj):
    phr__baq = context.get_argument_type(types.pyobject)
    wtr__wxri = lir.FunctionType(lir.VoidType(), [phr__baq, phr__baq])
    mkqi__ywjng = cgutils.get_or_insert_function(builder.module, wtr__wxri,
        name='dict_merge_from_seq2')
    builder.call(mkqi__ywjng, [dict_obj, seq2_obj])


def to_arr_obj_if_list_obj(c, context, builder, val, typ):
    if not (isinstance(typ, types.List) or bodo.utils.utils.is_array_typ(
        typ, False)):
        return val
    rvl__aka = cgutils.alloca_once_value(builder, val)
    ichex__gxv = list_check(builder, context, val)
    wwzk__tmpmc = builder.icmp_unsigned('!=', ichex__gxv, lir.Constant(
        ichex__gxv.type, 0))
    with builder.if_then(wwzk__tmpmc):
        ajrod__gevsw = context.insert_const_string(builder.module, 'numpy')
        lyynv__fvqd = c.pyapi.import_module_noblock(ajrod__gevsw)
        zedwd__utp = 'object_'
        if isinstance(typ, types.Array) or isinstance(typ.dtype, types.Float):
            zedwd__utp = str(typ.dtype)
        mwpw__ytlpn = c.pyapi.object_getattr_string(lyynv__fvqd, zedwd__utp)
        odygy__qjil = builder.load(rvl__aka)
        fhoqy__hpt = c.pyapi.call_method(lyynv__fvqd, 'asarray', (
            odygy__qjil, mwpw__ytlpn))
        builder.store(fhoqy__hpt, rvl__aka)
        c.pyapi.decref(lyynv__fvqd)
        c.pyapi.decref(mwpw__ytlpn)
    val = builder.load(rvl__aka)
    return val


def get_array_elem_counts(c, builder, context, arr_obj, typ):
    from bodo.libs.array_item_arr_ext import ArrayItemArrayType
    from bodo.libs.map_arr_ext import MapArrayType
    from bodo.libs.str_arr_ext import get_utf8_size, string_array_type
    from bodo.libs.struct_arr_ext import StructArrayType, StructType
    from bodo.libs.tuple_arr_ext import TupleArrayType
    if typ == bodo.string_type:
        ldjvz__qth = c.pyapi.to_native_value(bodo.string_type, arr_obj).value
        rfq__mtdzm, kqkyf__ovyr = c.pyapi.call_jit_code(lambda a:
            get_utf8_size(a), types.int64(bodo.string_type), [ldjvz__qth])
        context.nrt.decref(builder, typ, ldjvz__qth)
        return cgutils.pack_array(builder, [kqkyf__ovyr])
    if isinstance(typ, (StructType, types.BaseTuple)):
        ajrod__gevsw = context.insert_const_string(builder.module, 'pandas')
        lhi__lty = c.pyapi.import_module_noblock(ajrod__gevsw)
        C_NA = c.pyapi.object_getattr_string(lhi__lty, 'NA')
        pfx__pyrxu = bodo.utils.transform.get_type_alloc_counts(typ)
        cipad__mmo = context.make_tuple(builder, types.Tuple(pfx__pyrxu * [
            types.int64]), pfx__pyrxu * [context.get_constant(types.int64, 0)])
        liva__kam = cgutils.alloca_once_value(builder, cipad__mmo)
        mqkz__thr = 0
        wbqvm__hloal = typ.data if isinstance(typ, StructType) else typ.types
        for bmak__xvvp, t in enumerate(wbqvm__hloal):
            tokz__kprxr = bodo.utils.transform.get_type_alloc_counts(t)
            if tokz__kprxr == 0:
                continue
            if isinstance(typ, StructType):
                val_obj = c.pyapi.dict_getitem_string(arr_obj, typ.names[
                    bmak__xvvp])
            else:
                val_obj = c.pyapi.tuple_getitem(arr_obj, bmak__xvvp)
            adphy__lfcaq = is_na_value(builder, context, val_obj, C_NA)
            fnkqj__pko = builder.icmp_unsigned('!=', adphy__lfcaq, lir.
                Constant(adphy__lfcaq.type, 1))
            with builder.if_then(fnkqj__pko):
                cipad__mmo = builder.load(liva__kam)
                gmjlz__wbm = get_array_elem_counts(c, builder, context,
                    val_obj, t)
                for bmak__xvvp in range(tokz__kprxr):
                    ymqu__anyi = builder.extract_value(cipad__mmo, 
                        mqkz__thr + bmak__xvvp)
                    mxjvr__wxntb = builder.extract_value(gmjlz__wbm, bmak__xvvp
                        )
                    cipad__mmo = builder.insert_value(cipad__mmo, builder.
                        add(ymqu__anyi, mxjvr__wxntb), mqkz__thr + bmak__xvvp)
                builder.store(cipad__mmo, liva__kam)
            mqkz__thr += tokz__kprxr
        c.pyapi.decref(lhi__lty)
        c.pyapi.decref(C_NA)
        return builder.load(liva__kam)
    if not bodo.utils.utils.is_array_typ(typ, False):
        return cgutils.pack_array(builder, [], lir.IntType(64))
    n = bodo.utils.utils.object_length(c, arr_obj)
    if not (isinstance(typ, (ArrayItemArrayType, StructArrayType,
        TupleArrayType, MapArrayType)) or typ == string_array_type):
        return cgutils.pack_array(builder, [n])
    ajrod__gevsw = context.insert_const_string(builder.module, 'pandas')
    lhi__lty = c.pyapi.import_module_noblock(ajrod__gevsw)
    C_NA = c.pyapi.object_getattr_string(lhi__lty, 'NA')
    pfx__pyrxu = bodo.utils.transform.get_type_alloc_counts(typ)
    cipad__mmo = context.make_tuple(builder, types.Tuple(pfx__pyrxu * [
        types.int64]), [n] + (pfx__pyrxu - 1) * [context.get_constant(types
        .int64, 0)])
    liva__kam = cgutils.alloca_once_value(builder, cipad__mmo)
    with cgutils.for_range(builder, n) as loop:
        fhns__onphs = loop.index
        uqa__oey = seq_getitem(builder, context, arr_obj, fhns__onphs)
        adphy__lfcaq = is_na_value(builder, context, uqa__oey, C_NA)
        fnkqj__pko = builder.icmp_unsigned('!=', adphy__lfcaq, lir.Constant
            (adphy__lfcaq.type, 1))
        with builder.if_then(fnkqj__pko):
            if isinstance(typ, ArrayItemArrayType) or typ == string_array_type:
                cipad__mmo = builder.load(liva__kam)
                gmjlz__wbm = get_array_elem_counts(c, builder, context,
                    uqa__oey, typ.dtype)
                for bmak__xvvp in range(pfx__pyrxu - 1):
                    ymqu__anyi = builder.extract_value(cipad__mmo, 
                        bmak__xvvp + 1)
                    mxjvr__wxntb = builder.extract_value(gmjlz__wbm, bmak__xvvp
                        )
                    cipad__mmo = builder.insert_value(cipad__mmo, builder.
                        add(ymqu__anyi, mxjvr__wxntb), bmak__xvvp + 1)
                builder.store(cipad__mmo, liva__kam)
            elif isinstance(typ, (StructArrayType, TupleArrayType)):
                mqkz__thr = 1
                for bmak__xvvp, t in enumerate(typ.data):
                    tokz__kprxr = bodo.utils.transform.get_type_alloc_counts(t
                        .dtype)
                    if tokz__kprxr == 0:
                        continue
                    if isinstance(typ, TupleArrayType):
                        val_obj = c.pyapi.tuple_getitem(uqa__oey, bmak__xvvp)
                    else:
                        val_obj = c.pyapi.dict_getitem_string(uqa__oey, typ
                            .names[bmak__xvvp])
                    adphy__lfcaq = is_na_value(builder, context, val_obj, C_NA)
                    fnkqj__pko = builder.icmp_unsigned('!=', adphy__lfcaq,
                        lir.Constant(adphy__lfcaq.type, 1))
                    with builder.if_then(fnkqj__pko):
                        cipad__mmo = builder.load(liva__kam)
                        gmjlz__wbm = get_array_elem_counts(c, builder,
                            context, val_obj, t.dtype)
                        for bmak__xvvp in range(tokz__kprxr):
                            ymqu__anyi = builder.extract_value(cipad__mmo, 
                                mqkz__thr + bmak__xvvp)
                            mxjvr__wxntb = builder.extract_value(gmjlz__wbm,
                                bmak__xvvp)
                            cipad__mmo = builder.insert_value(cipad__mmo,
                                builder.add(ymqu__anyi, mxjvr__wxntb), 
                                mqkz__thr + bmak__xvvp)
                        builder.store(cipad__mmo, liva__kam)
                    mqkz__thr += tokz__kprxr
            else:
                assert isinstance(typ, MapArrayType), typ
                cipad__mmo = builder.load(liva__kam)
                lkh__soxb = dict_keys(builder, context, uqa__oey)
                png__viij = dict_values(builder, context, uqa__oey)
                msfr__msvw = get_array_elem_counts(c, builder, context,
                    lkh__soxb, typ.key_arr_type)
                tqq__mqp = bodo.utils.transform.get_type_alloc_counts(typ.
                    key_arr_type)
                for bmak__xvvp in range(1, tqq__mqp + 1):
                    ymqu__anyi = builder.extract_value(cipad__mmo, bmak__xvvp)
                    mxjvr__wxntb = builder.extract_value(msfr__msvw, 
                        bmak__xvvp - 1)
                    cipad__mmo = builder.insert_value(cipad__mmo, builder.
                        add(ymqu__anyi, mxjvr__wxntb), bmak__xvvp)
                uhuv__yaqd = get_array_elem_counts(c, builder, context,
                    png__viij, typ.value_arr_type)
                for bmak__xvvp in range(tqq__mqp + 1, pfx__pyrxu):
                    ymqu__anyi = builder.extract_value(cipad__mmo, bmak__xvvp)
                    mxjvr__wxntb = builder.extract_value(uhuv__yaqd, 
                        bmak__xvvp - tqq__mqp)
                    cipad__mmo = builder.insert_value(cipad__mmo, builder.
                        add(ymqu__anyi, mxjvr__wxntb), bmak__xvvp)
                builder.store(cipad__mmo, liva__kam)
                c.pyapi.decref(lkh__soxb)
                c.pyapi.decref(png__viij)
        c.pyapi.decref(uqa__oey)
    c.pyapi.decref(lhi__lty)
    c.pyapi.decref(C_NA)
    return builder.load(liva__kam)


def gen_allocate_array(context, builder, arr_type, n_elems, c=None):
    oyu__zkevd = n_elems.type.count
    assert oyu__zkevd >= 1
    uiiy__owj = builder.extract_value(n_elems, 0)
    if oyu__zkevd != 1:
        axyla__lko = cgutils.pack_array(builder, [builder.extract_value(
            n_elems, bmak__xvvp) for bmak__xvvp in range(1, oyu__zkevd)])
        wmm__mpt = types.Tuple([types.int64] * (oyu__zkevd - 1))
    else:
        axyla__lko = context.get_dummy_value()
        wmm__mpt = types.none
    miv__jxy = types.TypeRef(arr_type)
    pfq__yadb = arr_type(types.int64, miv__jxy, wmm__mpt)
    args = [uiiy__owj, context.get_dummy_value(), axyla__lko]
    nzc__cecmj = lambda n, t, s: bodo.utils.utils.alloc_type(n, t, s)
    if c:
        rfq__mtdzm, jlim__pusq = c.pyapi.call_jit_code(nzc__cecmj,
            pfq__yadb, args)
    else:
        jlim__pusq = context.compile_internal(builder, nzc__cecmj,
            pfq__yadb, args)
    return jlim__pusq
