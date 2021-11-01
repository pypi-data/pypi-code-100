"""
Boxing and unboxing support for DataFrame, Series, etc.
"""
import datetime
import decimal
import warnings
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.typing import signature
from numba.extending import NativeValue, box, intrinsic, typeof_impl, unbox
from numba.np import numpy_support
from numba.typed.typeddict import Dict
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_dataframe_ext import DataFramePayloadType, DataFrameType, construct_dataframe
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.libs import hstr_ext
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.int_arr_ext import typeof_pd_int_dtype
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoError, BodoWarning, dtype_to_array_type, get_overload_const_int, is_overload_constant_int, to_nullable_type
ll.add_symbol('array_size', hstr_ext.array_size)
ll.add_symbol('array_getptr1', hstr_ext.array_getptr1)


def _set_bodo_meta_in_pandas():
    if '_bodo_meta' not in pd.Series._metadata:
        pd.Series._metadata.append('_bodo_meta')
    if '_bodo_meta' not in pd.DataFrame._metadata:
        pd.DataFrame._metadata.append('_bodo_meta')


_set_bodo_meta_in_pandas()


@typeof_impl.register(pd.DataFrame)
def typeof_pd_dataframe(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    ynssy__doo = tuple(val.columns.to_list())
    aarv__jch = get_hiframes_dtypes(val)
    kbb__legjn = numba.typeof(val.index)
    znjs__wutrl = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    return DataFrameType(aarv__jch, kbb__legjn, ynssy__doo, znjs__wutrl)


@typeof_impl.register(pd.Series)
def typeof_pd_series(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    znjs__wutrl = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    return SeriesType(_infer_series_dtype(val), index=numba.typeof(val.
        index), name_typ=numba.typeof(val.name), dist=znjs__wutrl)


@unbox(DataFrameType)
def unbox_dataframe(typ, val, c):
    pof__oxl = len(typ.columns)
    oza__mdvtk = c.context.get_constant(types.int8, 0)
    foiek__hkqdk = c.context.make_tuple(c.builder, types.UniTuple(types.
        int8, pof__oxl + 1), [oza__mdvtk] * (pof__oxl + 1))
    vlt__lutx = c.pyapi.object_getattr_string(val, 'index')
    jcr__tveyt = c.pyapi.to_native_value(typ.index, vlt__lutx).value
    c.pyapi.decref(vlt__lutx)
    bekd__fhi = [c.context.get_constant_null(ehxne__ckl) for ehxne__ckl in
        typ.data]
    qdi__zotzl = c.context.make_tuple(c.builder, types.Tuple(typ.data),
        bekd__fhi)
    oyzk__ufwcn = construct_dataframe(c.context, c.builder, typ, qdi__zotzl,
        jcr__tveyt, foiek__hkqdk, val)
    return NativeValue(oyzk__ufwcn)


def get_hiframes_dtypes(df):
    ucop__qccb = [dtype_to_array_type(_infer_series_dtype(df.iloc[:, i])) for
        i in range(len(df.columns))]
    return tuple(ucop__qccb)


def _infer_series_dtype(S):
    if S.dtype == np.dtype('O'):
        return numba.typeof(S.values).dtype
    if isinstance(S.dtype, pd.core.arrays.integer._IntegerDtype):
        return typeof_pd_int_dtype(S.dtype, None)
    elif isinstance(S.dtype, pd.CategoricalDtype):
        return bodo.typeof(S.dtype)
    elif isinstance(S.dtype, pd.StringDtype):
        return string_type
    elif isinstance(S.dtype, pd.BooleanDtype):
        return types.bool_
    if isinstance(S.dtype, pd.DatetimeTZDtype):
        raise BodoError('Timezone-aware datetime data type not supported yet')
    try:
        return numpy_support.from_dtype(S.dtype)
    except:
        raise BodoError(
            f'data type {S.dtype} for column {S.name} not supported yet')


@box(DataFrameType)
def box_dataframe(typ, val, c):
    context = c.context
    builder = c.builder
    pyapi = c.pyapi
    ush__uizys = bodo.hiframes.pd_dataframe_ext.get_dataframe_payload(c.
        context, c.builder, typ, val)
    lyzv__ilga = cgutils.create_struct_proxy(typ)(context, builder, value=val)
    obj = lyzv__ilga.parent
    pti__tarb = cgutils.alloca_once_value(c.builder, obj)
    vpkqg__sip = cgutils.is_not_null(builder, obj)
    bwfun__usgx = numba.typeof(typ.columns)
    tew__nkg = context.get_constant_generic(builder, bwfun__usgx, typ.columns)
    context.nrt.incref(builder, bwfun__usgx, tew__nkg)
    oqsul__hiu = pyapi.from_native_value(bwfun__usgx, tew__nkg, c.env_manager)
    with c.builder.if_else(vpkqg__sip) as (use_parent, otherwise):
        with use_parent:
            pyapi.incref(obj)
            lurb__aksf = context.insert_const_string(c.builder.module, 'numpy')
            iqn__fvwz = pyapi.import_module_noblock(lurb__aksf)
            kwfu__lbf = pyapi.long_from_longlong(lir.Constant(lir.IntType(
                64), len(typ.columns)))
            brfi__efel = pyapi.call_method(iqn__fvwz, 'arange', (kwfu__lbf,))
            pyapi.object_setattr_string(obj, 'columns', brfi__efel)
            pyapi.decref(iqn__fvwz)
            pyapi.decref(brfi__efel)
            pyapi.decref(kwfu__lbf)
        with otherwise:
            context.nrt.incref(builder, typ.index, ush__uizys.index)
            fbcvr__qlxd = c.pyapi.from_native_value(typ.index, ush__uizys.
                index, c.env_manager)
            lurb__aksf = context.insert_const_string(c.builder.module, 'pandas'
                )
            iqn__fvwz = pyapi.import_module_noblock(lurb__aksf)
            vqi__lxw = pyapi.call_method(iqn__fvwz, 'DataFrame', (pyapi.
                borrow_none(), fbcvr__qlxd))
            pyapi.decref(iqn__fvwz)
            pyapi.decref(fbcvr__qlxd)
            builder.store(vqi__lxw, pti__tarb)
    pof__oxl = len(typ.columns)
    nyzes__ccpum = [builder.extract_value(ush__uizys.data, i) for i in
        range(pof__oxl)]
    xjez__izf = typ.data
    for i, enqb__ybrr, kuy__gdlwn in zip(range(pof__oxl), nyzes__ccpum,
        xjez__izf):
        eeee__qpmo = builder.extract_value(ush__uizys.unboxed, i)
        zbona__lmxjh = builder.icmp_unsigned('==', eeee__qpmo, lir.Constant
            (eeee__qpmo.type, 1))
        nzsz__rnv = builder.or_(builder.not_(vpkqg__sip), builder.and_(
            vpkqg__sip, zbona__lmxjh))
        with builder.if_then(nzsz__rnv):
            hrwpw__gbhuh = pyapi.long_from_longlong(context.get_constant(
                types.int64, i))
            context.nrt.incref(builder, kuy__gdlwn, enqb__ybrr)
            arr_obj = pyapi.from_native_value(kuy__gdlwn, enqb__ybrr, c.
                env_manager)
            vqi__lxw = builder.load(pti__tarb)
            pyapi.object_setitem(vqi__lxw, hrwpw__gbhuh, arr_obj)
            pyapi.decref(arr_obj)
            pyapi.decref(hrwpw__gbhuh)
    vqi__lxw = builder.load(pti__tarb)
    pyapi.object_setattr_string(vqi__lxw, 'columns', oqsul__hiu)
    pyapi.decref(oqsul__hiu)
    _set_bodo_meta(vqi__lxw, pyapi, typ)
    c.context.nrt.decref(c.builder, typ, val)
    return vqi__lxw


@intrinsic
def unbox_dataframe_column(typingctx, df, i=None):
    assert isinstance(df, DataFrameType) and is_overload_constant_int(i)

    def codegen(context, builder, sig, args):
        pyapi = context.get_python_api(builder)
        c = numba.core.pythonapi._UnboxContext(context, builder, pyapi)
        zadb__tfz = pyapi.gil_ensure()
        fdzuf__sxm = sig.args[0]
        qhfko__idwun = get_overload_const_int(sig.args[1])
        data_typ = fdzuf__sxm.data[qhfko__idwun]
        lyzv__ilga = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        dbgu__ifmd = c.pyapi.borrow_none()
        fjrr__cbnfr = c.pyapi.unserialize(c.pyapi.serialize_object(slice))
        jvbm__ozzpq = c.pyapi.call_function_objargs(fjrr__cbnfr, [dbgu__ifmd])
        iofnl__lnv = c.pyapi.long_from_longlong(args[1])
        hhtgg__lacyp = c.pyapi.tuple_pack([jvbm__ozzpq, iofnl__lnv])
        zfyq__ijt = c.pyapi.object_getattr_string(lyzv__ilga.parent, 'iloc')
        wij__efsge = c.pyapi.object_getitem(zfyq__ijt, hhtgg__lacyp)
        gan__fedob = c.pyapi.object_getattr_string(wij__efsge, 'values')
        if isinstance(data_typ, types.Array):
            fddu__tqe = c.context.insert_const_string(c.builder.module, 'numpy'
                )
            yku__orfas = c.pyapi.import_module_noblock(fddu__tqe)
            arr_obj = c.pyapi.call_method(yku__orfas, 'ascontiguousarray',
                (gan__fedob,))
            c.pyapi.decref(gan__fedob)
            c.pyapi.decref(yku__orfas)
        else:
            arr_obj = gan__fedob
        gyacg__awd = _unbox_series_data(data_typ.dtype, data_typ, arr_obj, c)
        c.pyapi.decref(fjrr__cbnfr)
        c.pyapi.decref(jvbm__ozzpq)
        c.pyapi.decref(iofnl__lnv)
        c.pyapi.decref(hhtgg__lacyp)
        c.pyapi.decref(zfyq__ijt)
        c.pyapi.decref(wij__efsge)
        c.pyapi.decref(arr_obj)
        pyapi.gil_release(zadb__tfz)
        ush__uizys = bodo.hiframes.pd_dataframe_ext.get_dataframe_payload(c
            .context, c.builder, fdzuf__sxm, args[0])
        ush__uizys.data = builder.insert_value(ush__uizys.data, gyacg__awd.
            value, qhfko__idwun)
        ush__uizys.unboxed = builder.insert_value(ush__uizys.unboxed,
            context.get_constant(types.int8, 1), qhfko__idwun)
        jdbf__qtu = DataFramePayloadType(fdzuf__sxm)
        lbf__xit = context.nrt.meminfo_data(builder, lyzv__ilga.meminfo)
        foe__fzn = context.get_value_type(jdbf__qtu).as_pointer()
        lbf__xit = builder.bitcast(lbf__xit, foe__fzn)
        builder.store(ush__uizys._getvalue(), lbf__xit)
    return signature(types.none, df, i), codegen


@unbox(SeriesType)
def unbox_series(typ, val, c):
    gan__fedob = c.pyapi.object_getattr_string(val, 'values')
    if isinstance(typ.data, types.Array):
        fddu__tqe = c.context.insert_const_string(c.builder.module, 'numpy')
        yku__orfas = c.pyapi.import_module_noblock(fddu__tqe)
        arr_obj = c.pyapi.call_method(yku__orfas, 'ascontiguousarray', (
            gan__fedob,))
        c.pyapi.decref(gan__fedob)
        c.pyapi.decref(yku__orfas)
    else:
        arr_obj = gan__fedob
    hhjj__ikz = _unbox_series_data(typ.dtype, typ.data, arr_obj, c).value
    fbcvr__qlxd = c.pyapi.object_getattr_string(val, 'index')
    jcr__tveyt = c.pyapi.to_native_value(typ.index, fbcvr__qlxd).value
    wvnuj__lcof = c.pyapi.object_getattr_string(val, 'name')
    wyajm__oywrc = c.pyapi.to_native_value(typ.name_typ, wvnuj__lcof).value
    fegej__jfia = bodo.hiframes.pd_series_ext.construct_series(c.context, c
        .builder, typ, hhjj__ikz, jcr__tveyt, wyajm__oywrc)
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(fbcvr__qlxd)
    c.pyapi.decref(wvnuj__lcof)
    return NativeValue(fegej__jfia)


def _unbox_series_data(dtype, data_typ, arr_obj, c):
    if data_typ == string_array_split_view_type:
        bmqb__dua = c.context.make_helper(c.builder,
            string_array_split_view_type)
        return NativeValue(bmqb__dua._getvalue())
    return c.pyapi.to_native_value(data_typ, arr_obj)


@box(HeterogeneousSeriesType)
@box(SeriesType)
def box_series(typ, val, c):
    lurb__aksf = c.context.insert_const_string(c.builder.module, 'pandas')
    cts__lwlos = c.pyapi.import_module_noblock(lurb__aksf)
    irct__dqs = bodo.hiframes.pd_series_ext.get_series_payload(c.context, c
        .builder, typ, val)
    c.context.nrt.incref(c.builder, typ.data, irct__dqs.data)
    c.context.nrt.incref(c.builder, typ.index, irct__dqs.index)
    c.context.nrt.incref(c.builder, typ.name_typ, irct__dqs.name)
    arr_obj = c.pyapi.from_native_value(typ.data, irct__dqs.data, c.env_manager
        )
    fbcvr__qlxd = c.pyapi.from_native_value(typ.index, irct__dqs.index, c.
        env_manager)
    wvnuj__lcof = c.pyapi.from_native_value(typ.name_typ, irct__dqs.name, c
        .env_manager)
    dtype = c.pyapi.make_none()
    pti__tarb = c.pyapi.call_method(cts__lwlos, 'Series', (arr_obj,
        fbcvr__qlxd, dtype, wvnuj__lcof))
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(fbcvr__qlxd)
    c.pyapi.decref(wvnuj__lcof)
    _set_bodo_meta(pti__tarb, c.pyapi, typ)
    c.pyapi.decref(cts__lwlos)
    c.context.nrt.decref(c.builder, typ, val)
    return pti__tarb


def _set_bodo_meta(obj, pyapi, typ):
    ytit__tfnmy = pyapi.dict_new(1)
    raf__qutb = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ.
        dist.value))
    pyapi.dict_setitem_string(ytit__tfnmy, 'dist', raf__qutb)
    pyapi.object_setattr_string(obj, '_bodo_meta', ytit__tfnmy)
    pyapi.decref(ytit__tfnmy)
    pyapi.decref(raf__qutb)


@typeof_impl.register(np.ndarray)
def _typeof_ndarray(val, c):
    try:
        dtype = numba.np.numpy_support.from_dtype(val.dtype)
    except NotImplementedError as rwmz__wcdn:
        dtype = types.pyobject
    if dtype == types.pyobject:
        return _infer_ndarray_obj_dtype(val)
    dtj__suoz = numba.np.numpy_support.map_layout(val)
    rgpc__pouf = not val.flags.writeable
    return types.Array(dtype, val.ndim, dtj__suoz, readonly=rgpc__pouf)


def _infer_ndarray_obj_dtype(val):
    if not val.dtype == np.dtype('O'):
        raise BodoError('Unsupported array dtype: {}'.format(val.dtype))
    i = 0
    while i < len(val) and (pd.api.types.is_scalar(val[i]) and pd.isna(val[
        i]) or not pd.api.types.is_scalar(val[i]) and len(val[i]) == 0):
        i += 1
    if i == len(val):
        warnings.warn(BodoWarning(
            'Empty object array passed to Bodo, which causes ambiguity in typing. This can cause errors in parallel execution.'
            ))
        return string_array_type
    suoyk__hvaa = val[i]
    if isinstance(suoyk__hvaa, str):
        return string_array_type
    elif isinstance(suoyk__hvaa, bytes):
        return binary_array_type
    elif isinstance(suoyk__hvaa, bool):
        return bodo.libs.bool_arr_ext.boolean_array
    elif isinstance(suoyk__hvaa, (int, np.int32, np.int64)):
        return bodo.libs.int_arr_ext.IntegerArrayType(numba.typeof(suoyk__hvaa)
            )
    elif isinstance(suoyk__hvaa, (dict, Dict)) and all(isinstance(
        nwb__ohdxf, str) for nwb__ohdxf in suoyk__hvaa.keys()):
        xejm__vlg = tuple(suoyk__hvaa.keys())
        ctax__kfepv = tuple(_get_struct_value_arr_type(v) for v in
            suoyk__hvaa.values())
        return StructArrayType(ctax__kfepv, xejm__vlg)
    elif isinstance(suoyk__hvaa, (dict, Dict)):
        lutha__lbfze = numba.typeof(_value_to_array(list(suoyk__hvaa.keys())))
        wcaz__lmll = numba.typeof(_value_to_array(list(suoyk__hvaa.values())))
        return MapArrayType(lutha__lbfze, wcaz__lmll)
    elif isinstance(suoyk__hvaa, tuple):
        ctax__kfepv = tuple(_get_struct_value_arr_type(v) for v in suoyk__hvaa)
        return TupleArrayType(ctax__kfepv)
    if isinstance(suoyk__hvaa, (list, np.ndarray, pd.arrays.BooleanArray,
        pd.arrays.IntegerArray, pd.arrays.StringArray)):
        if isinstance(suoyk__hvaa, list):
            suoyk__hvaa = _value_to_array(suoyk__hvaa)
        brr__ovwzi = numba.typeof(suoyk__hvaa)
        return ArrayItemArrayType(brr__ovwzi)
    if isinstance(suoyk__hvaa, datetime.date):
        return datetime_date_array_type
    if isinstance(suoyk__hvaa, datetime.timedelta):
        return datetime_timedelta_array_type
    if isinstance(suoyk__hvaa, decimal.Decimal):
        return DecimalArrayType(38, 18)
    raise BodoError('Unsupported object array with first value: {}'.format(
        suoyk__hvaa))


def _value_to_array(val):
    assert isinstance(val, (list, dict, Dict))
    if isinstance(val, (dict, Dict)):
        val = dict(val)
        return np.array([val], np.object_)
    fumn__iedx = val.copy()
    fumn__iedx.append(None)
    enqb__ybrr = np.array(fumn__iedx, np.object_)
    if len(val) and isinstance(val[0], float):
        enqb__ybrr = np.array(val, np.float64)
    return enqb__ybrr


def _get_struct_value_arr_type(v):
    if isinstance(v, (dict, Dict)):
        return numba.typeof(_value_to_array(v))
    if isinstance(v, list):
        return dtype_to_array_type(numba.typeof(_value_to_array(v)))
    if pd.api.types.is_scalar(v) and pd.isna(v):
        warnings.warn(BodoWarning(
            'Field value in struct array is NA, which causes ambiguity in typing. This can cause errors in parallel execution.'
            ))
        return string_array_type
    kuy__gdlwn = dtype_to_array_type(numba.typeof(v))
    if isinstance(v, (int, bool)):
        kuy__gdlwn = to_nullable_type(kuy__gdlwn)
    return kuy__gdlwn
