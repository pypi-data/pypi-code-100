import datetime
import operator
import llvmlite.llvmpy.core as lc
import numba
import numpy as np
import pandas as pd
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_new_ref, lower_constant
from numba.core.typing.templates import AttributeTemplate, signature
from numba.extending import NativeValue, box, infer_getattr, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
import bodo.hiframes
import bodo.utils.conversion
from bodo.hiframes.datetime_timedelta_ext import pd_timedelta_type
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_type
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.utils.transform import get_const_func_output_type
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, dtype_to_array_type, get_overload_const_func, get_overload_const_str, get_udf_error_msg, get_udf_out_arr_type, get_val_type_maybe_str_literal, is_const_func_type, is_heterogeneous_tuple_type, is_iterable_type, is_overload_false, is_overload_none, is_overload_true, raise_bodo_error, parse_dtype
_dt_index_data_typ = types.Array(types.NPDatetime('ns'), 1, 'C')
_timedelta_index_data_typ = types.Array(types.NPTimedelta('ns'), 1, 'C')
iNaT = pd._libs.tslibs.iNaT
NaT = types.NPDatetime('ns')('NaT')


@typeof_impl.register(pd.Index)
def typeof_pd_index(val, c):
    if val.inferred_type == 'string' or pd._libs.lib.infer_dtype(val, True
        ) == 'string':
        return StringIndexType(get_val_type_maybe_str_literal(val.name))
    if val.inferred_type == 'bytes' or pd._libs.lib.infer_dtype(val, True
        ) == 'bytes':
        return BinaryIndexType(get_val_type_maybe_str_literal(val.name))
    if val.equals(pd.Index([])):
        return StringIndexType(get_val_type_maybe_str_literal(val.name))
    if val.inferred_type == 'date':
        return DatetimeIndexType(get_val_type_maybe_str_literal(val.name))
    if val.inferred_type == 'integer' or pd._libs.lib.infer_dtype(val, True
        ) == 'integer':
        return NumericIndexType(types.int64, get_val_type_maybe_str_literal
            (val.name), IntegerArrayType(types.int64))
    if val.inferred_type == 'boolean' or pd._libs.lib.infer_dtype(val, True
        ) == 'boolean':
        return NumericIndexType(types.bool_, get_val_type_maybe_str_literal
            (val.name), boolean_array)
    raise NotImplementedError(f'unsupported pd.Index type {val}')


class DatetimeIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None):
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = types.Array(bodo.datetime64ns, 1, 'C')
        super(DatetimeIndexType, self).__init__(name=
            'DatetimeIndex(name = {})'.format(name_typ))
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return types.NPDatetime('ns')

    def copy(self):
        return DatetimeIndexType(self.name_typ)

    @property
    def key(self):
        return self.name_typ

    @property
    def iterator_type(self):
        return types.iterators.ArrayIterator(_dt_index_data_typ)


types.datetime_index = DatetimeIndexType()


@typeof_impl.register(pd.DatetimeIndex)
def typeof_datetime_index(val, c):
    return DatetimeIndexType(get_val_type_maybe_str_literal(val.name))


@register_model(DatetimeIndexType)
class DatetimeIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        and__chw = [('data', _dt_index_data_typ), ('name', fe_type.name_typ
            ), ('dict', types.DictType(_dt_index_data_typ.dtype, types.int64))]
        super(DatetimeIndexModel, self).__init__(dmm, fe_type, and__chw)


make_attribute_wrapper(DatetimeIndexType, 'data', '_data')
make_attribute_wrapper(DatetimeIndexType, 'name', '_name')
make_attribute_wrapper(DatetimeIndexType, 'dict', '_dict')


@overload_method(DatetimeIndexType, 'copy', no_unliteral=True)
def overload_datetime_index_copy(A):
    return lambda A: bodo.hiframes.pd_index_ext.init_datetime_index(A._data
        .copy(), A._name)


@box(DatetimeIndexType)
def box_dt_index(typ, val, c):
    dyehf__dpvnv = c.context.insert_const_string(c.builder.module, 'pandas')
    ury__funy = c.pyapi.import_module_noblock(dyehf__dpvnv)
    lfn__kfxi = numba.core.cgutils.create_struct_proxy(typ)(c.context, c.
        builder, val)
    c.context.nrt.incref(c.builder, _dt_index_data_typ, lfn__kfxi.data)
    wtfv__sij = c.pyapi.from_native_value(_dt_index_data_typ, lfn__kfxi.
        data, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, lfn__kfxi.name)
    shlcu__zxqrv = c.pyapi.from_native_value(typ.name_typ, lfn__kfxi.name,
        c.env_manager)
    args = c.pyapi.tuple_pack([wtfv__sij])
    kws = c.pyapi.dict_pack([('name', shlcu__zxqrv)])
    tfek__sqvod = c.pyapi.object_getattr_string(ury__funy, 'DatetimeIndex')
    vefhm__jck = c.pyapi.call(tfek__sqvod, args, kws)
    c.pyapi.decref(wtfv__sij)
    c.pyapi.decref(shlcu__zxqrv)
    c.pyapi.decref(ury__funy)
    c.pyapi.decref(tfek__sqvod)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return vefhm__jck


@unbox(DatetimeIndexType)
def unbox_datetime_index(typ, val, c):
    ujvmm__gdi = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(_dt_index_data_typ, ujvmm__gdi).value
    shlcu__zxqrv = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, shlcu__zxqrv).value
    c.pyapi.decref(ujvmm__gdi)
    c.pyapi.decref(shlcu__zxqrv)
    cgie__tcdit = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    cgie__tcdit.data = data
    cgie__tcdit.name = name
    dtype = _dt_index_data_typ.dtype
    kadpw__mur, nnr__mbexp = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    cgie__tcdit.dict = nnr__mbexp
    return NativeValue(cgie__tcdit._getvalue())


@intrinsic
def init_datetime_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        cqjz__nvoah, uto__hkmsz = args
        lfn__kfxi = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        lfn__kfxi.data = cqjz__nvoah
        lfn__kfxi.name = uto__hkmsz
        context.nrt.incref(builder, signature.args[0], cqjz__nvoah)
        context.nrt.incref(builder, signature.args[1], uto__hkmsz)
        dtype = _dt_index_data_typ.dtype
        lfn__kfxi.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return lfn__kfxi._getvalue()
    ncq__axg = DatetimeIndexType(name)
    sig = signature(ncq__axg, data, name)
    return sig, codegen


def init_index_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) >= 1 and not kws
    zxl__flf = args[0]
    if equiv_set.has_shape(zxl__flf):
        return ArrayAnalysis.AnalyzeResult(shape=zxl__flf, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_datetime_index
    ) = init_index_equiv


def gen_dti_field_impl(field):
    vxf__xsgo = 'def impl(dti):\n'
    vxf__xsgo += '    numba.parfors.parfor.init_prange()\n'
    vxf__xsgo += '    A = bodo.hiframes.pd_index_ext.get_index_data(dti)\n'
    vxf__xsgo += '    name = bodo.hiframes.pd_index_ext.get_index_name(dti)\n'
    vxf__xsgo += '    n = len(A)\n'
    vxf__xsgo += '    S = np.empty(n, np.int64)\n'
    vxf__xsgo += '    for i in numba.parfors.parfor.internal_prange(n):\n'
    vxf__xsgo += (
        '        dt64 = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(A[i])\n'
        )
    vxf__xsgo += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(dt64)
"""
    if field in ['weekday']:
        vxf__xsgo += '        S[i] = ts.' + field + '()\n'
    else:
        vxf__xsgo += '        S[i] = ts.' + field + '\n'
    vxf__xsgo += (
        '    return bodo.hiframes.pd_index_ext.init_numeric_index(S, name)\n')
    huj__llz = {}
    exec(vxf__xsgo, {'numba': numba, 'np': np, 'bodo': bodo}, huj__llz)
    impl = huj__llz['impl']
    return impl


def _install_dti_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        if field in ['is_leap_year']:
            continue
        impl = gen_dti_field_impl(field)
        overload_attribute(DatetimeIndexType, field)(lambda dti: impl)


_install_dti_date_fields()


@overload_attribute(DatetimeIndexType, 'is_leap_year')
def overload_datetime_index_is_leap_year(dti):

    def impl(dti):
        numba.parfors.parfor.init_prange()
        A = bodo.hiframes.pd_index_ext.get_index_data(dti)
        wxqom__mdnd = len(A)
        S = np.empty(wxqom__mdnd, np.bool_)
        for i in numba.parfors.parfor.internal_prange(wxqom__mdnd):
            epxmu__jiba = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(A[i])
            jtck__pbb = (bodo.hiframes.pd_timestamp_ext.
                convert_datetime64_to_timestamp(epxmu__jiba))
            S[i] = bodo.hiframes.pd_timestamp_ext.is_leap_year(jtck__pbb.year)
        return S
    return impl


@overload_attribute(DatetimeIndexType, 'date')
def overload_datetime_index_date(dti):

    def impl(dti):
        numba.parfors.parfor.init_prange()
        A = bodo.hiframes.pd_index_ext.get_index_data(dti)
        wxqom__mdnd = len(A)
        S = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
            wxqom__mdnd)
        for i in numba.parfors.parfor.internal_prange(wxqom__mdnd):
            epxmu__jiba = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(A[i])
            jtck__pbb = (bodo.hiframes.pd_timestamp_ext.
                convert_datetime64_to_timestamp(epxmu__jiba))
            S[i] = datetime.date(jtck__pbb.year, jtck__pbb.month, jtck__pbb.day
                )
        return S
    return impl


@numba.njit(no_cpython_wrapper=True)
def _dti_val_finalize(s, count):
    if not count:
        s = iNaT
    return bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(s)


@numba.njit(no_cpython_wrapper=True)
def _tdi_val_finalize(s, count):
    return pd.Timedelta('nan') if not count else pd.Timedelta(s)


@overload_method(DatetimeIndexType, 'min', no_unliteral=True)
def overload_datetime_index_min(dti, axis=None, skipna=True):
    lmmer__fzbf = dict(axis=axis, skipna=skipna)
    yog__ujpbd = dict(axis=None, skipna=True)
    check_unsupported_args('DatetimeIndex.min', lmmer__fzbf, yog__ujpbd)

    def impl(dti, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        qlr__bfhlu = bodo.hiframes.pd_index_ext.get_index_data(dti)
        s = numba.cpython.builtins.get_type_max_value(numba.core.types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(len(qlr__bfhlu)):
            if not bodo.libs.array_kernels.isna(qlr__bfhlu, i):
                val = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(qlr__bfhlu
                    [i])
                s = min(s, val)
                count += 1
        return bodo.hiframes.pd_index_ext._dti_val_finalize(s, count)
    return impl


@overload_method(DatetimeIndexType, 'max', no_unliteral=True)
def overload_datetime_index_max(dti, axis=None, skipna=True):
    lmmer__fzbf = dict(axis=axis, skipna=skipna)
    yog__ujpbd = dict(axis=None, skipna=True)
    check_unsupported_args('DatetimeIndex.max', lmmer__fzbf, yog__ujpbd)

    def impl(dti, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        qlr__bfhlu = bodo.hiframes.pd_index_ext.get_index_data(dti)
        s = numba.cpython.builtins.get_type_min_value(numba.core.types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(len(qlr__bfhlu)):
            if not bodo.libs.array_kernels.isna(qlr__bfhlu, i):
                val = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(qlr__bfhlu
                    [i])
                s = max(s, val)
                count += 1
        return bodo.hiframes.pd_index_ext._dti_val_finalize(s, count)
    return impl


@infer_getattr
class DatetimeIndexAttribute(AttributeTemplate):
    key = DatetimeIndexType

    def resolve_values(self, ary):
        return _dt_index_data_typ


@overload(pd.DatetimeIndex, no_unliteral=True)
def pd_datetimeindex_overload(data=None, freq=None, start=None, end=None,
    periods=None, tz=None, normalize=False, closed=None, ambiguous='raise',
    dayfirst=False, yearfirst=False, dtype=None, copy=False, name=None,
    verify_integrity=True):
    if is_overload_none(data):
        raise BodoError('data argument in pd.DatetimeIndex() expected')
    if any(not is_overload_none(a) for a in (freq, start, end, periods, tz,
        closed)):
        raise BodoError('only data argument in pd.DatetimeIndex() supported')

    def f(data=None, freq=None, start=None, end=None, periods=None, tz=None,
        normalize=False, closed=None, ambiguous='raise', dayfirst=False,
        yearfirst=False, dtype=None, copy=False, name=None,
        verify_integrity=True):
        jtoi__fbqb = bodo.utils.conversion.coerce_to_array(data)
        S = bodo.utils.conversion.convert_to_dt64ns(jtoi__fbqb)
        return bodo.hiframes.pd_index_ext.init_datetime_index(S, name)
    return f


def overload_sub_operator_datetime_index(lhs, rhs):
    if isinstance(lhs, DatetimeIndexType
        ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        tsu__bcux = np.dtype('timedelta64[ns]')

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            qlr__bfhlu = bodo.hiframes.pd_index_ext.get_index_data(lhs)
            name = bodo.hiframes.pd_index_ext.get_index_name(lhs)
            wxqom__mdnd = len(qlr__bfhlu)
            S = np.empty(wxqom__mdnd, tsu__bcux)
            ivg__fejox = rhs.value
            for i in numba.parfors.parfor.internal_prange(wxqom__mdnd):
                S[i] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    qlr__bfhlu[i]) - ivg__fejox)
            return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
        return impl
    if isinstance(rhs, DatetimeIndexType
        ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        tsu__bcux = np.dtype('timedelta64[ns]')

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            qlr__bfhlu = bodo.hiframes.pd_index_ext.get_index_data(rhs)
            name = bodo.hiframes.pd_index_ext.get_index_name(rhs)
            wxqom__mdnd = len(qlr__bfhlu)
            S = np.empty(wxqom__mdnd, tsu__bcux)
            ivg__fejox = lhs.value
            for i in numba.parfors.parfor.internal_prange(wxqom__mdnd):
                S[i] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    ivg__fejox - bodo.hiframes.pd_timestamp_ext.
                    dt64_to_integer(qlr__bfhlu[i]))
            return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
        return impl


def gen_dti_str_binop_impl(op, is_lhs_dti):
    kthpd__replo = numba.core.utils.OPERATORS_TO_BUILTINS[op]
    vxf__xsgo = 'def impl(lhs, rhs):\n'
    if is_lhs_dti:
        vxf__xsgo += '  dt_index, _str = lhs, rhs\n'
        elzl__dnagq = 'arr[i] {} other'.format(kthpd__replo)
    else:
        vxf__xsgo += '  dt_index, _str = rhs, lhs\n'
        elzl__dnagq = 'other {} arr[i]'.format(kthpd__replo)
    vxf__xsgo += (
        '  arr = bodo.hiframes.pd_index_ext.get_index_data(dt_index)\n')
    vxf__xsgo += '  l = len(arr)\n'
    vxf__xsgo += (
        '  other = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(_str)\n')
    vxf__xsgo += '  S = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    vxf__xsgo += '  for i in numba.parfors.parfor.internal_prange(l):\n'
    vxf__xsgo += '    S[i] = {}\n'.format(elzl__dnagq)
    vxf__xsgo += '  return S\n'
    huj__llz = {}
    exec(vxf__xsgo, {'bodo': bodo, 'numba': numba, 'np': np}, huj__llz)
    impl = huj__llz['impl']
    return impl


def overload_binop_dti_str(op):

    def overload_impl(lhs, rhs):
        if isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
            ) == string_type:
            return gen_dti_str_binop_impl(op, True)
        if isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
            ) == string_type:
            return gen_dti_str_binop_impl(op, False)
    return overload_impl


@overload(pd.Index, inline='always', no_unliteral=True)
def pd_index_overload(data=None, dtype=None, copy=False, name=None,
    tupleize_cols=True):
    data = types.unliteral(data) if not isinstance(data, types.LiteralList
        ) else data
    lwpqd__wtk = getattr(data, 'dtype', None)
    if not is_overload_none(dtype):
        pfime__akus = parse_dtype(dtype, 'pandas.Index')
    else:
        pfime__akus = lwpqd__wtk
    if isinstance(pfime__akus, types.misc.PyObject):
        raise BodoError(
            "pd.Index() object 'dtype' is not specific enough for typing. Please provide a more exact type (e.g. str)."
            )
    if isinstance(data, RangeIndexType):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.RangeIndex(data, name=name)
    elif isinstance(data, DatetimeIndexType
        ) or pfime__akus == types.NPDatetime('ns'):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.DatetimeIndex(data, name=name)
    elif isinstance(data, TimedeltaIndexType
        ) or pfime__akus == types.NPTimedelta('ns'):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return pd.TimedeltaIndex(data, name=name)
    elif is_heterogeneous_tuple_type(data):

        def impl(data=None, dtype=None, copy=False, name=None,
            tupleize_cols=True):
            return bodo.hiframes.pd_index_ext.init_heter_index(data, name)
        return impl
    elif bodo.utils.utils.is_array_typ(data, False) or isinstance(data, (
        SeriesType, types.List, types.UniTuple)):
        if isinstance(pfime__akus, (types.Integer, types.Float, types.Boolean)
            ):

            def impl(data=None, dtype=None, copy=False, name=None,
                tupleize_cols=True):
                jtoi__fbqb = bodo.utils.conversion.coerce_to_array(data)
                vhul__oyioc = bodo.utils.conversion.fix_arr_dtype(jtoi__fbqb,
                    pfime__akus)
                return bodo.hiframes.pd_index_ext.init_numeric_index(
                    vhul__oyioc, name)
        elif pfime__akus in [types.string, bytes_type]:

            def impl(data=None, dtype=None, copy=False, name=None,
                tupleize_cols=True):
                return bodo.hiframes.pd_index_ext.init_binary_str_index(bodo
                    .utils.conversion.coerce_to_array(data), name)
        else:
            raise BodoError(
                'pd.Index(): provided array is of unsupported type.')
    elif is_overload_none(data):
        raise BodoError(
            'data argument in pd.Index() is invalid: None or scalar is not acceptable'
            )
    else:
        raise BodoError(
            f'pd.Index(): the provided argument type {data} is not supported')
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_datetime_index_getitem(dti, ind):
    if isinstance(dti, DatetimeIndexType):
        if isinstance(ind, types.Integer):

            def impl(dti, ind):
                fqxci__zsvo = bodo.hiframes.pd_index_ext.get_index_data(dti)
                epxmu__jiba = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    fqxci__zsvo[ind])
                return (bodo.hiframes.pd_timestamp_ext.
                    convert_datetime64_to_timestamp(epxmu__jiba))
            return impl
        else:

            def impl(dti, ind):
                fqxci__zsvo = bodo.hiframes.pd_index_ext.get_index_data(dti)
                name = bodo.hiframes.pd_index_ext.get_index_name(dti)
                fjajt__tcpv = fqxci__zsvo[ind]
                return bodo.hiframes.pd_index_ext.init_datetime_index(
                    fjajt__tcpv, name)
            return impl


@overload(operator.getitem, no_unliteral=True)
def overload_timedelta_index_getitem(I, ind):
    if not isinstance(I, TimedeltaIndexType):
        return
    if isinstance(ind, types.Integer):

        def impl(I, ind):
            nnxt__zfeu = bodo.hiframes.pd_index_ext.get_index_data(I)
            return pd.Timedelta(nnxt__zfeu[ind])
        return impl

    def impl(I, ind):
        nnxt__zfeu = bodo.hiframes.pd_index_ext.get_index_data(I)
        name = bodo.hiframes.pd_index_ext.get_index_name(I)
        fjajt__tcpv = nnxt__zfeu[ind]
        return bodo.hiframes.pd_index_ext.init_timedelta_index(fjajt__tcpv,
            name)
    return impl


@numba.njit(no_cpython_wrapper=True)
def validate_endpoints(closed):
    cbfyi__fmh = False
    ktkk__jcd = False
    if closed is None:
        cbfyi__fmh = True
        ktkk__jcd = True
    elif closed == 'left':
        cbfyi__fmh = True
    elif closed == 'right':
        ktkk__jcd = True
    else:
        raise ValueError("Closed has to be either 'left', 'right' or None")
    return cbfyi__fmh, ktkk__jcd


@numba.njit(no_cpython_wrapper=True)
def to_offset_value(freq):
    if freq is None:
        return None
    with numba.objmode(r='int64'):
        r = pd.tseries.frequencies.to_offset(freq).nanos
    return r


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _dummy_convert_none_to_int(val):
    if is_overload_none(val):

        def impl(val):
            return 0
        return impl
    if isinstance(val, types.Optional):

        def impl(val):
            if val is None:
                return 0
            return bodo.utils.indexing.unoptional(val)
        return impl
    return lambda val: val


@overload(pd.date_range, no_unliteral=True)
def pd_date_range_overload(start=None, end=None, periods=None, freq=None,
    tz=None, normalize=False, name=None, closed=None):
    lmmer__fzbf = dict(tz=tz, normalize=normalize)
    yog__ujpbd = dict(tz=None, normalize=False)
    check_unsupported_args('pd.date_range', lmmer__fzbf, yog__ujpbd)
    if not is_overload_none(tz):
        raise BodoError('pd.date_range(): tz argument not supported yet')
    if is_overload_none(freq) and any(is_overload_none(t) for t in (start,
        end, periods)):
        freq = 'D'
    if sum(not is_overload_none(t) for t in (start, end, periods, freq)) != 3:
        raise BodoError(
            'Of the four parameters: start, end, periods, and freq, exactly three must be specified'
            )

    def f(start=None, end=None, periods=None, freq=None, tz=None, normalize
        =False, name=None, closed=None):
        if freq is None and (start is None or end is None or periods is None):
            freq = 'D'
        freq = bodo.hiframes.pd_index_ext.to_offset_value(freq)
        tbwaw__qpuqi = pd.Timestamp('2018-01-01')
        if start is not None:
            tbwaw__qpuqi = pd.Timestamp(start)
        xqy__dyud = pd.Timestamp('2018-01-01')
        if end is not None:
            xqy__dyud = pd.Timestamp(end)
        if start is None and end is None and closed is not None:
            raise ValueError(
                'Closed has to be None if not both of startand end are defined'
                )
        cbfyi__fmh, ktkk__jcd = bodo.hiframes.pd_index_ext.validate_endpoints(
            closed)
        if freq is not None:
            dsq__wrd = _dummy_convert_none_to_int(freq)
            if periods is None:
                b = tbwaw__qpuqi.value
                gkir__hpssm = b + (xqy__dyud.value - b
                    ) // dsq__wrd * dsq__wrd + dsq__wrd // 2 + 1
            elif start is not None:
                periods = _dummy_convert_none_to_int(periods)
                b = tbwaw__qpuqi.value
                aln__maa = np.int64(periods) * np.int64(dsq__wrd)
                gkir__hpssm = np.int64(b) + aln__maa
            elif end is not None:
                periods = _dummy_convert_none_to_int(periods)
                gkir__hpssm = xqy__dyud.value + dsq__wrd
                aln__maa = np.int64(periods) * np.int64(-dsq__wrd)
                b = np.int64(gkir__hpssm) + aln__maa
            else:
                raise ValueError(
                    "at least 'start' or 'end' should be specified if a 'period' is given."
                    )
            uhlkt__qat = np.arange(b, gkir__hpssm, dsq__wrd, np.int64)
        else:
            periods = _dummy_convert_none_to_int(periods)
            itvu__ngta = xqy__dyud.value - tbwaw__qpuqi.value
            step = itvu__ngta / (periods - 1)
            zhhz__uak = np.arange(0, periods, 1, np.float64)
            zhhz__uak *= step
            zhhz__uak += tbwaw__qpuqi.value
            uhlkt__qat = zhhz__uak.astype(np.int64)
            uhlkt__qat[-1] = xqy__dyud.value
        if not cbfyi__fmh and len(uhlkt__qat) and uhlkt__qat[0
            ] == tbwaw__qpuqi.value:
            uhlkt__qat = uhlkt__qat[1:]
        if not ktkk__jcd and len(uhlkt__qat) and uhlkt__qat[-1
            ] == xqy__dyud.value:
            uhlkt__qat = uhlkt__qat[:-1]
        S = bodo.utils.conversion.convert_to_dt64ns(uhlkt__qat)
        return bodo.hiframes.pd_index_ext.init_datetime_index(S, name)
    return f


@overload(pd.timedelta_range, no_unliteral=True)
def pd_timedelta_range_overload(start=None, end=None, periods=None, freq=
    None, name=None, closed=None):
    if is_overload_none(freq) and any(is_overload_none(t) for t in (start,
        end, periods)):
        freq = 'D'
    if sum(not is_overload_none(t) for t in (start, end, periods, freq)) != 3:
        raise BodoError(
            'Of the four parameters: start, end, periods, and freq, exactly three must be specified'
            )

    def f(start=None, end=None, periods=None, freq=None, name=None, closed=None
        ):
        if freq is None and (start is None or end is None or periods is None):
            freq = 'D'
        freq = bodo.hiframes.pd_index_ext.to_offset_value(freq)
        tbwaw__qpuqi = pd.Timedelta('1 day')
        if start is not None:
            tbwaw__qpuqi = pd.Timedelta(start)
        xqy__dyud = pd.Timedelta('1 day')
        if end is not None:
            xqy__dyud = pd.Timedelta(end)
        if start is None and end is None and closed is not None:
            raise ValueError(
                'Closed has to be None if not both of start and end are defined'
                )
        cbfyi__fmh, ktkk__jcd = bodo.hiframes.pd_index_ext.validate_endpoints(
            closed)
        if freq is not None:
            dsq__wrd = _dummy_convert_none_to_int(freq)
            if periods is None:
                b = tbwaw__qpuqi.value
                gkir__hpssm = b + (xqy__dyud.value - b
                    ) // dsq__wrd * dsq__wrd + dsq__wrd // 2 + 1
            elif start is not None:
                periods = _dummy_convert_none_to_int(periods)
                b = tbwaw__qpuqi.value
                aln__maa = np.int64(periods) * np.int64(dsq__wrd)
                gkir__hpssm = np.int64(b) + aln__maa
            elif end is not None:
                periods = _dummy_convert_none_to_int(periods)
                gkir__hpssm = xqy__dyud.value + dsq__wrd
                aln__maa = np.int64(periods) * np.int64(-dsq__wrd)
                b = np.int64(gkir__hpssm) + aln__maa
            else:
                raise ValueError(
                    "at least 'start' or 'end' should be specified if a 'period' is given."
                    )
            uhlkt__qat = np.arange(b, gkir__hpssm, dsq__wrd, np.int64)
        else:
            periods = _dummy_convert_none_to_int(periods)
            itvu__ngta = xqy__dyud.value - tbwaw__qpuqi.value
            step = itvu__ngta / (periods - 1)
            zhhz__uak = np.arange(0, periods, 1, np.float64)
            zhhz__uak *= step
            zhhz__uak += tbwaw__qpuqi.value
            uhlkt__qat = zhhz__uak.astype(np.int64)
            uhlkt__qat[-1] = xqy__dyud.value
        if not cbfyi__fmh and len(uhlkt__qat) and uhlkt__qat[0
            ] == tbwaw__qpuqi.value:
            uhlkt__qat = uhlkt__qat[1:]
        if not ktkk__jcd and len(uhlkt__qat) and uhlkt__qat[-1
            ] == xqy__dyud.value:
            uhlkt__qat = uhlkt__qat[:-1]
        S = bodo.utils.conversion.convert_to_dt64ns(uhlkt__qat)
        return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
    return f


@overload_method(DatetimeIndexType, 'isocalendar', inline='always',
    no_unliteral=True)
def overload_pd_timestamp_isocalendar(idx):

    def impl(idx):
        A = bodo.hiframes.pd_index_ext.get_index_data(idx)
        numba.parfors.parfor.init_prange()
        wxqom__mdnd = len(A)
        axm__hcn = bodo.libs.int_arr_ext.alloc_int_array(wxqom__mdnd, np.uint32
            )
        ykn__xmebi = bodo.libs.int_arr_ext.alloc_int_array(wxqom__mdnd, np.
            uint32)
        bbqu__qyjnn = bodo.libs.int_arr_ext.alloc_int_array(wxqom__mdnd, np
            .uint32)
        for i in numba.parfors.parfor.internal_prange(wxqom__mdnd):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(axm__hcn, i)
                bodo.libs.array_kernels.setna(ykn__xmebi, i)
                bodo.libs.array_kernels.setna(bbqu__qyjnn, i)
                continue
            axm__hcn[i], ykn__xmebi[i], bbqu__qyjnn[i
                ] = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(
                A[i]).isocalendar()
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((axm__hcn,
            ykn__xmebi, bbqu__qyjnn), idx, ('year', 'week', 'day'))
    return impl


class TimedeltaIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None):
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = types.Array(bodo.timedelta64ns, 1, 'C')
        super(TimedeltaIndexType, self).__init__(name=
            'TimedeltaIndexType(named = {})'.format(name_typ))
    ndim = 1

    def copy(self):
        return TimedeltaIndexType(self.name_typ)

    @property
    def dtype(self):
        return types.NPTimedelta('ns')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def key(self):
        return self.name_typ

    @property
    def iterator_type(self):
        return types.iterators.ArrayIterator(_timedelta_index_data_typ)


timedelta_index = TimedeltaIndexType()
types.timedelta_index = timedelta_index


@register_model(TimedeltaIndexType)
class TimedeltaIndexTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        and__chw = [('data', _timedelta_index_data_typ), ('name', fe_type.
            name_typ), ('dict', types.DictType(_timedelta_index_data_typ.
            dtype, types.int64))]
        super(TimedeltaIndexTypeModel, self).__init__(dmm, fe_type, and__chw)


@typeof_impl.register(pd.TimedeltaIndex)
def typeof_timedelta_index(val, c):
    return TimedeltaIndexType(get_val_type_maybe_str_literal(val.name))


@box(TimedeltaIndexType)
def box_timedelta_index(typ, val, c):
    dyehf__dpvnv = c.context.insert_const_string(c.builder.module, 'pandas')
    ury__funy = c.pyapi.import_module_noblock(dyehf__dpvnv)
    timedelta_index = numba.core.cgutils.create_struct_proxy(typ)(c.context,
        c.builder, val)
    c.context.nrt.incref(c.builder, _timedelta_index_data_typ,
        timedelta_index.data)
    wtfv__sij = c.pyapi.from_native_value(_timedelta_index_data_typ,
        timedelta_index.data, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, timedelta_index.name)
    shlcu__zxqrv = c.pyapi.from_native_value(typ.name_typ, timedelta_index.
        name, c.env_manager)
    args = c.pyapi.tuple_pack([wtfv__sij])
    kws = c.pyapi.dict_pack([('name', shlcu__zxqrv)])
    tfek__sqvod = c.pyapi.object_getattr_string(ury__funy, 'TimedeltaIndex')
    vefhm__jck = c.pyapi.call(tfek__sqvod, args, kws)
    c.pyapi.decref(wtfv__sij)
    c.pyapi.decref(shlcu__zxqrv)
    c.pyapi.decref(ury__funy)
    c.pyapi.decref(tfek__sqvod)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return vefhm__jck


@unbox(TimedeltaIndexType)
def unbox_timedelta_index(typ, val, c):
    ujvmm__gdi = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(_timedelta_index_data_typ, ujvmm__gdi).value
    shlcu__zxqrv = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, shlcu__zxqrv).value
    c.pyapi.decref(ujvmm__gdi)
    c.pyapi.decref(shlcu__zxqrv)
    cgie__tcdit = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    cgie__tcdit.data = data
    cgie__tcdit.name = name
    dtype = _timedelta_index_data_typ.dtype
    kadpw__mur, nnr__mbexp = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    cgie__tcdit.dict = nnr__mbexp
    return NativeValue(cgie__tcdit._getvalue())


@intrinsic
def init_timedelta_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        cqjz__nvoah, uto__hkmsz = args
        timedelta_index = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        timedelta_index.data = cqjz__nvoah
        timedelta_index.name = uto__hkmsz
        context.nrt.incref(builder, signature.args[0], cqjz__nvoah)
        context.nrt.incref(builder, signature.args[1], uto__hkmsz)
        dtype = _timedelta_index_data_typ.dtype
        timedelta_index.dict = context.compile_internal(builder, lambda :
            numba.typed.Dict.empty(dtype, types.int64), types.DictType(
            dtype, types.int64)(), [])
        return timedelta_index._getvalue()
    ncq__axg = TimedeltaIndexType(name)
    sig = signature(ncq__axg, data, name)
    return sig, codegen


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_timedelta_index
    ) = init_index_equiv


@infer_getattr
class TimedeltaIndexAttribute(AttributeTemplate):
    key = TimedeltaIndexType

    def resolve_values(self, ary):
        return _timedelta_index_data_typ


make_attribute_wrapper(TimedeltaIndexType, 'data', '_data')
make_attribute_wrapper(TimedeltaIndexType, 'name', '_name')
make_attribute_wrapper(TimedeltaIndexType, 'dict', '_dict')


@overload_method(TimedeltaIndexType, 'copy', no_unliteral=True)
def overload_timedelta_index_copy(A):
    return lambda A: bodo.hiframes.pd_index_ext.init_timedelta_index(A.
        _data.copy(), A._name)


@overload_method(TimedeltaIndexType, 'min', inline='always', no_unliteral=True)
def overload_timedelta_index_min(tdi, axis=None, skipna=True):
    lmmer__fzbf = dict(axis=axis, skipna=skipna)
    yog__ujpbd = dict(axis=None, skipna=True)
    check_unsupported_args('TimedeltaIndex.min', lmmer__fzbf, yog__ujpbd)

    def impl(tdi, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        data = bodo.hiframes.pd_index_ext.get_index_data(tdi)
        wxqom__mdnd = len(data)
        igj__cmgu = numba.cpython.builtins.get_type_max_value(numba.core.
            types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(wxqom__mdnd):
            if bodo.libs.array_kernels.isna(data, i):
                continue
            val = (bodo.hiframes.datetime_timedelta_ext.
                cast_numpy_timedelta_to_int(data[i]))
            count += 1
            igj__cmgu = min(igj__cmgu, val)
        qyoj__rqce = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
            igj__cmgu)
        return bodo.hiframes.pd_index_ext._tdi_val_finalize(qyoj__rqce, count)
    return impl


@overload_method(TimedeltaIndexType, 'max', inline='always', no_unliteral=True)
def overload_timedelta_index_max(tdi, axis=None, skipna=True):
    lmmer__fzbf = dict(axis=axis, skipna=skipna)
    yog__ujpbd = dict(axis=None, skipna=True)
    check_unsupported_args('TimedeltaIndex.max', lmmer__fzbf, yog__ujpbd)
    if not is_overload_none(axis) or not is_overload_true(skipna):
        raise BodoError(
            'Index.min(): axis and skipna arguments not supported yet')

    def impl(tdi, axis=None, skipna=True):
        numba.parfors.parfor.init_prange()
        data = bodo.hiframes.pd_index_ext.get_index_data(tdi)
        wxqom__mdnd = len(data)
        hpfeh__twtx = numba.cpython.builtins.get_type_min_value(numba.core.
            types.int64)
        count = 0
        for i in numba.parfors.parfor.internal_prange(wxqom__mdnd):
            if bodo.libs.array_kernels.isna(data, i):
                continue
            val = (bodo.hiframes.datetime_timedelta_ext.
                cast_numpy_timedelta_to_int(data[i]))
            count += 1
            hpfeh__twtx = max(hpfeh__twtx, val)
        qyoj__rqce = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
            hpfeh__twtx)
        return bodo.hiframes.pd_index_ext._tdi_val_finalize(qyoj__rqce, count)
    return impl


def gen_tdi_field_impl(field):
    vxf__xsgo = 'def impl(tdi):\n'
    vxf__xsgo += '    numba.parfors.parfor.init_prange()\n'
    vxf__xsgo += '    A = bodo.hiframes.pd_index_ext.get_index_data(tdi)\n'
    vxf__xsgo += '    name = bodo.hiframes.pd_index_ext.get_index_name(tdi)\n'
    vxf__xsgo += '    n = len(A)\n'
    vxf__xsgo += '    S = np.empty(n, np.int64)\n'
    vxf__xsgo += '    for i in numba.parfors.parfor.internal_prange(n):\n'
    vxf__xsgo += (
        '        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])\n'
        )
    if field == 'nanoseconds':
        vxf__xsgo += '        S[i] = td64 % 1000\n'
    elif field == 'microseconds':
        vxf__xsgo += '        S[i] = td64 // 1000 % 100000\n'
    elif field == 'seconds':
        vxf__xsgo += (
            '        S[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
    elif field == 'days':
        vxf__xsgo += '        S[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n'
    else:
        assert False, 'invalid timedelta field'
    vxf__xsgo += (
        '    return bodo.hiframes.pd_index_ext.init_numeric_index(S, name)\n')
    huj__llz = {}
    exec(vxf__xsgo, {'numba': numba, 'np': np, 'bodo': bodo}, huj__llz)
    impl = huj__llz['impl']
    return impl


def _install_tdi_time_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        impl = gen_tdi_field_impl(field)
        overload_attribute(TimedeltaIndexType, field)(lambda tdi: impl)


_install_tdi_time_fields()


@overload(pd.TimedeltaIndex, no_unliteral=True)
def pd_timedelta_index_overload(data=None, unit=None, freq=None, start=None,
    end=None, periods=None, closed=None, dtype=None, copy=False, name=None,
    verify_integrity=None):
    if is_overload_none(data):
        raise BodoError('data argument in pd.TimedeltaIndex() expected')
    if any(not is_overload_none(a) for a in (unit, freq, start, end,
        periods, closed, dtype)):
        raise BodoError('only data argument in pd.TimedeltaIndex() supported')

    def impl(data=None, unit=None, freq=None, start=None, end=None, periods
        =None, closed=None, dtype=None, copy=False, name=None,
        verify_integrity=None):
        jtoi__fbqb = bodo.utils.conversion.coerce_to_array(data)
        S = bodo.utils.conversion.convert_to_td64ns(jtoi__fbqb)
        return bodo.hiframes.pd_index_ext.init_timedelta_index(S, name)
    return impl


class RangeIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ):
        self.name_typ = name_typ
        super(RangeIndexType, self).__init__(name='RangeIndexType({})'.
            format(name_typ))
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return RangeIndexType(self.name_typ)

    @property
    def iterator_type(self):
        return types.iterators.RangeIteratorType(types.int64)

    @property
    def dtype(self):
        return types.int64

    @property
    def pandas_type_name(self):
        return str(self.dtype)

    @property
    def numpy_type_name(self):
        return str(self.dtype)

    def unify(self, typingctx, other):
        if isinstance(other, NumericIndexType):
            name_typ = self.name_typ.unify(typingctx, other.name_typ)
            if name_typ is None:
                name_typ = types.none
            return NumericIndexType(types.int64, name_typ)


@typeof_impl.register(pd.RangeIndex)
def typeof_pd_range_index(val, c):
    return RangeIndexType(get_val_type_maybe_str_literal(val.name))


@register_model(RangeIndexType)
class RangeIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        and__chw = [('start', types.int64), ('stop', types.int64), ('step',
            types.int64), ('name', fe_type.name_typ)]
        super(RangeIndexModel, self).__init__(dmm, fe_type, and__chw)


make_attribute_wrapper(RangeIndexType, 'start', '_start')
make_attribute_wrapper(RangeIndexType, 'stop', '_stop')
make_attribute_wrapper(RangeIndexType, 'step', '_step')
make_attribute_wrapper(RangeIndexType, 'name', '_name')


@overload_method(RangeIndexType, 'copy', no_unliteral=True)
def overload_range_index_copy(A):
    return lambda A: bodo.hiframes.pd_index_ext.init_range_index(A._start,
        A._stop, A._step, A._name)


@box(RangeIndexType)
def box_range_index(typ, val, c):
    dyehf__dpvnv = c.context.insert_const_string(c.builder.module, 'pandas')
    fatg__wwpx = c.pyapi.import_module_noblock(dyehf__dpvnv)
    otj__fbfns = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    rey__yyux = c.pyapi.from_native_value(types.int64, otj__fbfns.start, c.
        env_manager)
    ffe__drhjy = c.pyapi.from_native_value(types.int64, otj__fbfns.stop, c.
        env_manager)
    hlkua__fxbat = c.pyapi.from_native_value(types.int64, otj__fbfns.step,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, otj__fbfns.name)
    shlcu__zxqrv = c.pyapi.from_native_value(typ.name_typ, otj__fbfns.name,
        c.env_manager)
    args = c.pyapi.tuple_pack([rey__yyux, ffe__drhjy, hlkua__fxbat])
    kws = c.pyapi.dict_pack([('name', shlcu__zxqrv)])
    tfek__sqvod = c.pyapi.object_getattr_string(fatg__wwpx, 'RangeIndex')
    nnwyj__hexmz = c.pyapi.call(tfek__sqvod, args, kws)
    c.pyapi.decref(rey__yyux)
    c.pyapi.decref(ffe__drhjy)
    c.pyapi.decref(hlkua__fxbat)
    c.pyapi.decref(shlcu__zxqrv)
    c.pyapi.decref(fatg__wwpx)
    c.pyapi.decref(tfek__sqvod)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return nnwyj__hexmz


@intrinsic
def init_range_index(typingctx, start, stop, step, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        assert len(args) == 4
        otj__fbfns = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        otj__fbfns.start = args[0]
        otj__fbfns.stop = args[1]
        otj__fbfns.step = args[2]
        otj__fbfns.name = args[3]
        context.nrt.incref(builder, signature.return_type.name_typ, args[3])
        return otj__fbfns._getvalue()
    return RangeIndexType(name)(start, stop, step, name), codegen


def init_range_index_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 4 and not kws
    start, stop, step, slqq__mmb = args
    if self.typemap[start.name] == types.IntegerLiteral(0) and self.typemap[
        step.name] == types.IntegerLiteral(1) and equiv_set.has_shape(stop):
        return ArrayAnalysis.AnalyzeResult(shape=stop, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_range_index
    ) = init_range_index_equiv


@unbox(RangeIndexType)
def unbox_range_index(typ, val, c):
    rey__yyux = c.pyapi.object_getattr_string(val, 'start')
    start = c.pyapi.to_native_value(types.int64, rey__yyux).value
    ffe__drhjy = c.pyapi.object_getattr_string(val, 'stop')
    stop = c.pyapi.to_native_value(types.int64, ffe__drhjy).value
    hlkua__fxbat = c.pyapi.object_getattr_string(val, 'step')
    step = c.pyapi.to_native_value(types.int64, hlkua__fxbat).value
    shlcu__zxqrv = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, shlcu__zxqrv).value
    c.pyapi.decref(rey__yyux)
    c.pyapi.decref(ffe__drhjy)
    c.pyapi.decref(hlkua__fxbat)
    c.pyapi.decref(shlcu__zxqrv)
    otj__fbfns = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    otj__fbfns.start = start
    otj__fbfns.stop = stop
    otj__fbfns.step = step
    otj__fbfns.name = name
    return NativeValue(otj__fbfns._getvalue())


@lower_constant(RangeIndexType)
def lower_constant_range_index(context, builder, ty, pyval):
    start = context.get_constant(types.int64, pyval.start)
    stop = context.get_constant(types.int64, pyval.stop)
    step = context.get_constant(types.int64, pyval.step)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    otj__fbfns = cgutils.create_struct_proxy(ty)(context, builder)
    otj__fbfns.start = start
    otj__fbfns.stop = stop
    otj__fbfns.step = step
    otj__fbfns.name = name
    return otj__fbfns._getvalue()


@overload(pd.RangeIndex, no_unliteral=True, inline='always')
def range_index_overload(start=None, stop=None, step=None, dtype=None, copy
    =False, name=None, fastpath=None):

    def _ensure_int_or_none(value, field):
        tzbl__kunk = (
            'RangeIndex(...) must be called with integers, {value} was passed for {field}'
            )
        if not is_overload_none(value) and not isinstance(value, types.
            IntegerLiteral) and not isinstance(value, types.Integer):
            raise BodoError(tzbl__kunk.format(value=value, field=field))
    _ensure_int_or_none(start, 'start')
    _ensure_int_or_none(stop, 'stop')
    _ensure_int_or_none(step, 'step')
    if is_overload_none(start) and is_overload_none(stop) and is_overload_none(
        step):
        tzbl__kunk = 'RangeIndex(...) must be called with integers'
        raise BodoError(tzbl__kunk)
    iil__ttwcl = 'start'
    rrzg__dysjb = 'stop'
    kpy__hhyh = 'step'
    if is_overload_none(start):
        iil__ttwcl = '0'
    if is_overload_none(stop):
        rrzg__dysjb = 'start'
        iil__ttwcl = '0'
    if is_overload_none(step):
        kpy__hhyh = '1'
    vxf__xsgo = """def _pd_range_index_imp(start=None, stop=None, step=None, dtype=None, copy=False, name=None, fastpath=None):
"""
    vxf__xsgo += '  return init_range_index({}, {}, {}, name)\n'.format(
        iil__ttwcl, rrzg__dysjb, kpy__hhyh)
    huj__llz = {}
    exec(vxf__xsgo, {'init_range_index': init_range_index}, huj__llz)
    rbbo__ajgs = huj__llz['_pd_range_index_imp']
    return rbbo__ajgs


@overload_attribute(RangeIndexType, 'start')
def rangeIndex_get_start(ri):

    def impl(ri):
        return ri._start
    return impl


@overload_attribute(RangeIndexType, 'stop')
def rangeIndex_get_stop(ri):

    def impl(ri):
        return ri._stop
    return impl


@overload_attribute(RangeIndexType, 'step')
def rangeIndex_get_step(ri):

    def impl(ri):
        return ri._step
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_range_index_getitem(I, idx):
    if isinstance(I, RangeIndexType):
        if isinstance(types.unliteral(idx), types.Integer):
            return lambda I, idx: idx * I._step + I._start
        if isinstance(idx, types.SliceType):

            def impl(I, idx):
                qagmb__opwk = numba.cpython.unicode._normalize_slice(idx,
                    len(I))
                name = bodo.hiframes.pd_index_ext.get_index_name(I)
                start = I._start + I._step * qagmb__opwk.start
                stop = I._start + I._step * qagmb__opwk.stop
                step = I._step * qagmb__opwk.step
                return bodo.hiframes.pd_index_ext.init_range_index(start,
                    stop, step, name)
            return impl
        return lambda I, idx: bodo.hiframes.pd_index_ext.init_numeric_index(np
            .arange(I._start, I._stop, I._step, np.int64)[idx], bodo.
            hiframes.pd_index_ext.get_index_name(I))


@overload(len, no_unliteral=True)
def overload_range_len(r):
    if isinstance(r, RangeIndexType):
        return lambda r: max(0, -(-(r._stop - r._start) // r._step))


class PeriodIndexType(types.IterableType):

    def __init__(self, freq, name_typ=None):
        name_typ = types.none if name_typ is None else name_typ
        self.freq = freq
        self.name_typ = name_typ
        super(PeriodIndexType, self).__init__(name=
            'PeriodIndexType({}, {})'.format(freq, name_typ))
    ndim = 1

    def copy(self):
        return PeriodIndexType(self.freq, self.name_typ)

    @property
    def iterator_type(self):
        return types.iterators.ArrayIterator(types.Array(types.int64, 1, 'C'))


@typeof_impl.register(pd.PeriodIndex)
def typeof_pd_period_index(val, c):
    return PeriodIndexType(val.freqstr, get_val_type_maybe_str_literal(val.
        name))


@register_model(PeriodIndexType)
class PeriodIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        and__chw = [('data', types.Array(types.int64, 1, 'C')), ('name',
            fe_type.name_typ), ('dict', types.DictType(types.int64, types.
            int64))]
        super(PeriodIndexModel, self).__init__(dmm, fe_type, and__chw)


make_attribute_wrapper(PeriodIndexType, 'data', '_data')
make_attribute_wrapper(PeriodIndexType, 'name', '_name')
make_attribute_wrapper(PeriodIndexType, 'dict', '_dict')


@overload_method(PeriodIndexType, 'copy', no_unliteral=True)
def overload_period_index_copy(A):
    freq = A.freq
    return lambda A: bodo.hiframes.pd_index_ext.init_period_index(A._data.
        copy(), A._name, freq)


@intrinsic
def init_period_index(typingctx, data, name, freq):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        cqjz__nvoah, uto__hkmsz, slqq__mmb = args
        dyt__bwlv = signature.return_type
        zdnq__ayub = cgutils.create_struct_proxy(dyt__bwlv)(context, builder)
        zdnq__ayub.data = cqjz__nvoah
        zdnq__ayub.name = uto__hkmsz
        context.nrt.incref(builder, signature.args[0], args[0])
        context.nrt.incref(builder, signature.args[1], args[1])
        zdnq__ayub.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(types.int64, types.int64), types.DictType(
            types.int64, types.int64)(), [])
        return zdnq__ayub._getvalue()
    ydkqr__sxqhm = get_overload_const_str(freq)
    ncq__axg = PeriodIndexType(ydkqr__sxqhm, name)
    sig = signature(ncq__axg, data, name, freq)
    return sig, codegen


@box(PeriodIndexType)
def box_period_index(typ, val, c):
    dyehf__dpvnv = c.context.insert_const_string(c.builder.module, 'pandas')
    fatg__wwpx = c.pyapi.import_module_noblock(dyehf__dpvnv)
    cgie__tcdit = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Array(types.int64, 1, 'C'),
        cgie__tcdit.data)
    zfky__xrwm = c.pyapi.from_native_value(types.Array(types.int64, 1, 'C'),
        cgie__tcdit.data, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, cgie__tcdit.name)
    shlcu__zxqrv = c.pyapi.from_native_value(typ.name_typ, cgie__tcdit.name,
        c.env_manager)
    jzlv__lcod = c.pyapi.string_from_constant_string(typ.freq)
    args = c.pyapi.tuple_pack([])
    kws = c.pyapi.dict_pack([('ordinal', zfky__xrwm), ('name', shlcu__zxqrv
        ), ('freq', jzlv__lcod)])
    tfek__sqvod = c.pyapi.object_getattr_string(fatg__wwpx, 'PeriodIndex')
    nnwyj__hexmz = c.pyapi.call(tfek__sqvod, args, kws)
    c.pyapi.decref(zfky__xrwm)
    c.pyapi.decref(shlcu__zxqrv)
    c.pyapi.decref(jzlv__lcod)
    c.pyapi.decref(fatg__wwpx)
    c.pyapi.decref(tfek__sqvod)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return nnwyj__hexmz


@unbox(PeriodIndexType)
def unbox_period_index(typ, val, c):
    arr_typ = types.Array(types.int64, 1, 'C')
    xcv__onxt = c.pyapi.object_getattr_string(val, 'asi8')
    data = c.pyapi.to_native_value(arr_typ, xcv__onxt).value
    shlcu__zxqrv = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, shlcu__zxqrv).value
    c.pyapi.decref(xcv__onxt)
    c.pyapi.decref(shlcu__zxqrv)
    cgie__tcdit = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    cgie__tcdit.data = data
    cgie__tcdit.name = name
    kadpw__mur, nnr__mbexp = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(types.int64, types.int64), types.DictType(types.int64,
        types.int64)(), [])
    cgie__tcdit.dict = nnr__mbexp
    return NativeValue(cgie__tcdit._getvalue())


class CategoricalIndexType(types.ArrayCompatible):

    def __init__(self, data, name_typ=None):
        from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
        assert isinstance(data, CategoricalArrayType
            ), 'CategoricalIndexType expects CategoricalArrayType'
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = data
        super(CategoricalIndexType, self).__init__(name=
            f'CategoricalIndexType(data={self.data}, name={name_typ})')
    ndim = 1

    def copy(self):
        return CategoricalIndexType(self.data, self.name_typ)

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return self.data.dtype

    @property
    def key(self):
        return self.data, self.name_typ


@register_model(CategoricalIndexType)
class CategoricalIndexTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        from bodo.hiframes.pd_categorical_ext import get_categories_int_type
        sui__zkd = get_categories_int_type(fe_type.data.dtype)
        and__chw = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(sui__zkd, types.int64))]
        super(CategoricalIndexTypeModel, self).__init__(dmm, fe_type, and__chw)


@typeof_impl.register(pd.CategoricalIndex)
def typeof_categorical_index(val, c):
    return CategoricalIndexType(bodo.typeof(val.values),
        get_val_type_maybe_str_literal(val.name))


@box(CategoricalIndexType)
def box_categorical_index(typ, val, c):
    dyehf__dpvnv = c.context.insert_const_string(c.builder.module, 'pandas')
    ury__funy = c.pyapi.import_module_noblock(dyehf__dpvnv)
    dxwb__islv = numba.core.cgutils.create_struct_proxy(typ)(c.context, c.
        builder, val)
    c.context.nrt.incref(c.builder, typ.data, dxwb__islv.data)
    wtfv__sij = c.pyapi.from_native_value(typ.data, dxwb__islv.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, dxwb__islv.name)
    shlcu__zxqrv = c.pyapi.from_native_value(typ.name_typ, dxwb__islv.name,
        c.env_manager)
    args = c.pyapi.tuple_pack([wtfv__sij])
    kws = c.pyapi.dict_pack([('name', shlcu__zxqrv)])
    tfek__sqvod = c.pyapi.object_getattr_string(ury__funy, 'CategoricalIndex')
    vefhm__jck = c.pyapi.call(tfek__sqvod, args, kws)
    c.pyapi.decref(wtfv__sij)
    c.pyapi.decref(shlcu__zxqrv)
    c.pyapi.decref(ury__funy)
    c.pyapi.decref(tfek__sqvod)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return vefhm__jck


@unbox(CategoricalIndexType)
def unbox_categorical_index(typ, val, c):
    from bodo.hiframes.pd_categorical_ext import get_categories_int_type
    ujvmm__gdi = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, ujvmm__gdi).value
    shlcu__zxqrv = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, shlcu__zxqrv).value
    c.pyapi.decref(ujvmm__gdi)
    c.pyapi.decref(shlcu__zxqrv)
    cgie__tcdit = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    cgie__tcdit.data = data
    cgie__tcdit.name = name
    dtype = get_categories_int_type(typ.data.dtype)
    kadpw__mur, nnr__mbexp = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    cgie__tcdit.dict = nnr__mbexp
    return NativeValue(cgie__tcdit._getvalue())


@intrinsic
def init_categorical_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        from bodo.hiframes.pd_categorical_ext import get_categories_int_type
        cqjz__nvoah, uto__hkmsz = args
        dxwb__islv = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        dxwb__islv.data = cqjz__nvoah
        dxwb__islv.name = uto__hkmsz
        context.nrt.incref(builder, signature.args[0], cqjz__nvoah)
        context.nrt.incref(builder, signature.args[1], uto__hkmsz)
        dtype = get_categories_int_type(signature.return_type.data.dtype)
        dxwb__islv.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return dxwb__islv._getvalue()
    ncq__axg = CategoricalIndexType(data, name)
    sig = signature(ncq__axg, data, name)
    return sig, codegen


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_index_ext_init_categorical_index
    ) = init_index_equiv
make_attribute_wrapper(CategoricalIndexType, 'data', '_data')
make_attribute_wrapper(CategoricalIndexType, 'name', '_name')
make_attribute_wrapper(CategoricalIndexType, 'dict', '_dict')


@overload_method(CategoricalIndexType, 'copy', no_unliteral=True)
def overload_categorical_index_copy(A):
    return lambda A: bodo.hiframes.pd_index_ext.init_categorical_index(A.
        _data.copy(), A._name)


class IntervalIndexType(types.ArrayCompatible):

    def __init__(self, data, name_typ=None):
        from bodo.libs.interval_arr_ext import IntervalArrayType
        assert isinstance(data, IntervalArrayType
            ), 'IntervalIndexType expects IntervalArrayType'
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = data
        super(IntervalIndexType, self).__init__(name=
            f'IntervalIndexType(data={self.data}, name={name_typ})')
    ndim = 1

    def copy(self):
        return IntervalIndexType(self.data, self.name_typ)

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def key(self):
        return self.data, self.name_typ


@register_model(IntervalIndexType)
class IntervalIndexTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        and__chw = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(types.UniTuple(fe_type.data.arr_type.
            dtype, 2), types.int64))]
        super(IntervalIndexTypeModel, self).__init__(dmm, fe_type, and__chw)


@typeof_impl.register(pd.IntervalIndex)
def typeof_interval_index(val, c):
    return IntervalIndexType(bodo.typeof(val.values),
        get_val_type_maybe_str_literal(val.name))


@box(IntervalIndexType)
def box_interval_index(typ, val, c):
    dyehf__dpvnv = c.context.insert_const_string(c.builder.module, 'pandas')
    ury__funy = c.pyapi.import_module_noblock(dyehf__dpvnv)
    nzze__rqw = numba.core.cgutils.create_struct_proxy(typ)(c.context, c.
        builder, val)
    c.context.nrt.incref(c.builder, typ.data, nzze__rqw.data)
    wtfv__sij = c.pyapi.from_native_value(typ.data, nzze__rqw.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, nzze__rqw.name)
    shlcu__zxqrv = c.pyapi.from_native_value(typ.name_typ, nzze__rqw.name,
        c.env_manager)
    args = c.pyapi.tuple_pack([wtfv__sij])
    kws = c.pyapi.dict_pack([('name', shlcu__zxqrv)])
    tfek__sqvod = c.pyapi.object_getattr_string(ury__funy, 'IntervalIndex')
    vefhm__jck = c.pyapi.call(tfek__sqvod, args, kws)
    c.pyapi.decref(wtfv__sij)
    c.pyapi.decref(shlcu__zxqrv)
    c.pyapi.decref(ury__funy)
    c.pyapi.decref(tfek__sqvod)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    c.context.nrt.decref(c.builder, typ, val)
    return vefhm__jck


@unbox(IntervalIndexType)
def unbox_interval_index(typ, val, c):
    ujvmm__gdi = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, ujvmm__gdi).value
    shlcu__zxqrv = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, shlcu__zxqrv).value
    c.pyapi.decref(ujvmm__gdi)
    c.pyapi.decref(shlcu__zxqrv)
    cgie__tcdit = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    cgie__tcdit.data = data
    cgie__tcdit.name = name
    dtype = types.UniTuple(typ.data.arr_type.dtype, 2)
    kadpw__mur, nnr__mbexp = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    cgie__tcdit.dict = nnr__mbexp
    return NativeValue(cgie__tcdit._getvalue())


@intrinsic
def init_interval_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        cqjz__nvoah, uto__hkmsz = args
        nzze__rqw = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        nzze__rqw.data = cqjz__nvoah
        nzze__rqw.name = uto__hkmsz
        context.nrt.incref(builder, signature.args[0], cqjz__nvoah)
        context.nrt.incref(builder, signature.args[1], uto__hkmsz)
        dtype = types.UniTuple(data.arr_type.dtype, 2)
        nzze__rqw.dict = context.compile_internal(builder, lambda : numba.
            typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return nzze__rqw._getvalue()
    ncq__axg = IntervalIndexType(data, name)
    sig = signature(ncq__axg, data, name)
    return sig, codegen


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_interval_index
    ) = init_index_equiv
make_attribute_wrapper(IntervalIndexType, 'data', '_data')
make_attribute_wrapper(IntervalIndexType, 'name', '_name')
make_attribute_wrapper(IntervalIndexType, 'dict', '_dict')


class NumericIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, dtype, name_typ=None, data=None):
        name_typ = types.none if name_typ is None else name_typ
        self.dtype = dtype
        self.name_typ = name_typ
        data = dtype_to_array_type(dtype) if data is None else data
        self.data = data
        super(NumericIndexType, self).__init__(name=
            f'NumericIndexType({dtype}, {name_typ}, {data})')
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return NumericIndexType(self.dtype, self.name_typ, self.data)

    @property
    def iterator_type(self):
        return types.iterators.ArrayIterator(types.Array(self.dtype, 1, 'C'))

    @property
    def pandas_type_name(self):
        return str(self.dtype)

    @property
    def numpy_type_name(self):
        return str(self.dtype)


@typeof_impl.register(pd.Int64Index)
def typeof_pd_int64_index(val, c):
    return NumericIndexType(types.int64, get_val_type_maybe_str_literal(val
        .name))


@typeof_impl.register(pd.UInt64Index)
def typeof_pd_uint64_index(val, c):
    return NumericIndexType(types.uint64, get_val_type_maybe_str_literal(
        val.name))


@typeof_impl.register(pd.Float64Index)
def typeof_pd_float64_index(val, c):
    return NumericIndexType(types.float64, get_val_type_maybe_str_literal(
        val.name))


@register_model(NumericIndexType)
class NumericIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        and__chw = [('data', fe_type.data), ('name', fe_type.name_typ), (
            'dict', types.DictType(fe_type.dtype, types.int64))]
        super(NumericIndexModel, self).__init__(dmm, fe_type, and__chw)


make_attribute_wrapper(NumericIndexType, 'data', '_data')
make_attribute_wrapper(NumericIndexType, 'name', '_name')
make_attribute_wrapper(NumericIndexType, 'dict', '_dict')


@overload_method(NumericIndexType, 'copy', no_unliteral=True)
def overload_numeric_index_copy(A):
    return lambda A: bodo.hiframes.pd_index_ext.init_numeric_index(A._data.
        copy(), A._name)


@box(NumericIndexType)
def box_numeric_index(typ, val, c):
    dyehf__dpvnv = c.context.insert_const_string(c.builder.module, 'pandas')
    fatg__wwpx = c.pyapi.import_module_noblock(dyehf__dpvnv)
    cgie__tcdit = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.data, cgie__tcdit.data)
    zfky__xrwm = c.pyapi.from_native_value(typ.data, cgie__tcdit.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, cgie__tcdit.name)
    shlcu__zxqrv = c.pyapi.from_native_value(typ.name_typ, cgie__tcdit.name,
        c.env_manager)
    asqz__cftzh = c.pyapi.make_none()
    qch__pfnje = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    nnwyj__hexmz = c.pyapi.call_method(fatg__wwpx, 'Index', (zfky__xrwm,
        asqz__cftzh, qch__pfnje, shlcu__zxqrv))
    c.pyapi.decref(zfky__xrwm)
    c.pyapi.decref(asqz__cftzh)
    c.pyapi.decref(qch__pfnje)
    c.pyapi.decref(shlcu__zxqrv)
    c.pyapi.decref(fatg__wwpx)
    c.context.nrt.decref(c.builder, typ, val)
    return nnwyj__hexmz


@intrinsic
def init_numeric_index(typingctx, data, name=None):
    name = types.none if is_overload_none(name) else name

    def codegen(context, builder, signature, args):
        assert len(args) == 2
        dyt__bwlv = signature.return_type
        cgie__tcdit = cgutils.create_struct_proxy(dyt__bwlv)(context, builder)
        cgie__tcdit.data = args[0]
        cgie__tcdit.name = args[1]
        context.nrt.incref(builder, dyt__bwlv.data, args[0])
        context.nrt.incref(builder, dyt__bwlv.name_typ, args[1])
        dtype = dyt__bwlv.dtype
        cgie__tcdit.dict = context.compile_internal(builder, lambda : numba
            .typed.Dict.empty(dtype, types.int64), types.DictType(dtype,
            types.int64)(), [])
        return cgie__tcdit._getvalue()
    return NumericIndexType(data.dtype, name, data)(data, name), codegen


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_init_numeric_index
    ) = init_index_equiv


@unbox(NumericIndexType)
def unbox_numeric_index(typ, val, c):
    ujvmm__gdi = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(typ.data, ujvmm__gdi).value
    shlcu__zxqrv = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, shlcu__zxqrv).value
    c.pyapi.decref(ujvmm__gdi)
    c.pyapi.decref(shlcu__zxqrv)
    cgie__tcdit = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    cgie__tcdit.data = data
    cgie__tcdit.name = name
    dtype = typ.dtype
    kadpw__mur, nnr__mbexp = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)(
        ), [])
    cgie__tcdit.dict = nnr__mbexp
    return NativeValue(cgie__tcdit._getvalue())


def create_numeric_constructor(func, default_dtype):

    def overload_impl(data=None, dtype=None, copy=False, name=None,
        fastpath=None):
        if is_overload_false(copy):

            def impl(data=None, dtype=None, copy=False, name=None, fastpath
                =None):
                jtoi__fbqb = bodo.utils.conversion.coerce_to_ndarray(data)
                hlb__sit = bodo.utils.conversion.fix_arr_dtype(jtoi__fbqb,
                    np.dtype(default_dtype))
                return bodo.hiframes.pd_index_ext.init_numeric_index(hlb__sit,
                    name)
        else:

            def impl(data=None, dtype=None, copy=False, name=None, fastpath
                =None):
                jtoi__fbqb = bodo.utils.conversion.coerce_to_ndarray(data)
                if copy:
                    jtoi__fbqb = jtoi__fbqb.copy()
                hlb__sit = bodo.utils.conversion.fix_arr_dtype(jtoi__fbqb,
                    np.dtype(default_dtype))
                return bodo.hiframes.pd_index_ext.init_numeric_index(hlb__sit,
                    name)
        return impl
    return overload_impl


def _install_numeric_constructors():
    for func, default_dtype in ((pd.Int64Index, np.int64), (pd.UInt64Index,
        np.uint64), (pd.Float64Index, np.float64)):
        overload_impl = create_numeric_constructor(func, default_dtype)
        overload(func, no_unliteral=True)(overload_impl)


_install_numeric_constructors()


class StringIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None):
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = string_array_type
        super(StringIndexType, self).__init__(name='StringIndexType({})'.
            format(name_typ))
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return StringIndexType(self.name_typ)

    @property
    def dtype(self):
        return string_type

    @property
    def pandas_type_name(self):
        return 'unicode'

    @property
    def numpy_type_name(self):
        return 'object'

    @property
    def iterator_type(self):
        return bodo.libs.str_arr_ext.StringArrayIterator()


@register_model(StringIndexType)
class StringIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        and__chw = [('data', string_array_type), ('name', fe_type.name_typ),
            ('dict', types.DictType(string_type, types.int64))]
        super(StringIndexModel, self).__init__(dmm, fe_type, and__chw)


make_attribute_wrapper(StringIndexType, 'data', '_data')
make_attribute_wrapper(StringIndexType, 'name', '_name')
make_attribute_wrapper(StringIndexType, 'dict', '_dict')


class BinaryIndexType(types.IterableType, types.ArrayCompatible):

    def __init__(self, name_typ=None):
        name_typ = types.none if name_typ is None else name_typ
        self.name_typ = name_typ
        self.data = binary_array_type
        super(BinaryIndexType, self).__init__(name='BinaryIndexType({})'.
            format(name_typ))
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return BinaryIndexType(self.name_typ)

    @property
    def dtype(self):
        return bytes_type

    @property
    def pandas_type_name(self):
        return 'bytes'

    @property
    def numpy_type_name(self):
        return 'object'

    @property
    def iterator_type(self):
        return bodo.libs.binary_arr_ext.BinaryArrayIterator()


@register_model(BinaryIndexType)
class BinaryIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        and__chw = [('data', binary_array_type), ('name', fe_type.name_typ),
            ('dict', types.DictType(bytes_type, types.int64))]
        super(BinaryIndexModel, self).__init__(dmm, fe_type, and__chw)


make_attribute_wrapper(BinaryIndexType, 'data', '_data')
make_attribute_wrapper(BinaryIndexType, 'name', '_name')
make_attribute_wrapper(BinaryIndexType, 'dict', '_dict')


@unbox(BinaryIndexType)
@unbox(StringIndexType)
def unbox_binary_str_index(typ, val, c):
    nilv__zqj = typ.data
    scalar_type = typ.data.dtype
    ujvmm__gdi = c.pyapi.object_getattr_string(val, 'values')
    data = c.pyapi.to_native_value(nilv__zqj, ujvmm__gdi).value
    shlcu__zxqrv = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, shlcu__zxqrv).value
    c.pyapi.decref(ujvmm__gdi)
    c.pyapi.decref(shlcu__zxqrv)
    cgie__tcdit = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    cgie__tcdit.data = data
    cgie__tcdit.name = name
    kadpw__mur, nnr__mbexp = c.pyapi.call_jit_code(lambda : numba.typed.
        Dict.empty(scalar_type, types.int64), types.DictType(scalar_type,
        types.int64)(), [])
    cgie__tcdit.dict = nnr__mbexp
    return NativeValue(cgie__tcdit._getvalue())


@box(BinaryIndexType)
@box(StringIndexType)
def box_binary_str_index(typ, val, c):
    nilv__zqj = typ.data
    dyehf__dpvnv = c.context.insert_const_string(c.builder.module, 'pandas')
    fatg__wwpx = c.pyapi.import_module_noblock(dyehf__dpvnv)
    cgie__tcdit = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, nilv__zqj, cgie__tcdit.data)
    zfky__xrwm = c.pyapi.from_native_value(nilv__zqj, cgie__tcdit.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, cgie__tcdit.name)
    shlcu__zxqrv = c.pyapi.from_native_value(typ.name_typ, cgie__tcdit.name,
        c.env_manager)
    asqz__cftzh = c.pyapi.make_none()
    qch__pfnje = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    nnwyj__hexmz = c.pyapi.call_method(fatg__wwpx, 'Index', (zfky__xrwm,
        asqz__cftzh, qch__pfnje, shlcu__zxqrv))
    c.pyapi.decref(zfky__xrwm)
    c.pyapi.decref(asqz__cftzh)
    c.pyapi.decref(qch__pfnje)
    c.pyapi.decref(shlcu__zxqrv)
    c.pyapi.decref(fatg__wwpx)
    c.context.nrt.decref(c.builder, typ, val)
    return nnwyj__hexmz


@intrinsic
def init_binary_str_index(typingctx, data, name=None):
    name = types.none if name is None else name
    sig = type(bodo.utils.typing.get_index_type_from_dtype(data.dtype))(name)(
        data, name)
    hmwqk__emm = get_binary_str_codegen(is_binary=data.dtype == bytes_type)
    return sig, hmwqk__emm


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_index_ext_init_binary_str_index
    ) = init_index_equiv


def get_binary_str_codegen(is_binary=False):
    if is_binary:
        eqz__ponws = 'binary_array_type'
        jppws__hiqyc = 'bytes_type'
    else:
        eqz__ponws = 'string_array_type'
        jppws__hiqyc = 'string_type'
    vxf__xsgo = 'def impl(context, builder, signature, args):\n'
    vxf__xsgo += '    assert len(args) == 2\n'
    vxf__xsgo += '    index_typ = signature.return_type\n'
    vxf__xsgo += (
        '    index_val = cgutils.create_struct_proxy(index_typ)(context, builder)\n'
        )
    vxf__xsgo += '    index_val.data = args[0]\n'
    vxf__xsgo += '    index_val.name = args[1]\n'
    vxf__xsgo += '    # increase refcount of stored values\n'
    vxf__xsgo += f'    context.nrt.incref(builder, {eqz__ponws}, args[0])\n'
    vxf__xsgo += (
        '    context.nrt.incref(builder, index_typ.name_typ, args[1])\n')
    vxf__xsgo += '    # create empty dict for get_loc hashmap\n'
    vxf__xsgo += '    index_val.dict = context.compile_internal(\n'
    vxf__xsgo += '       builder,\n'
    vxf__xsgo += (
        f'       lambda: numba.typed.Dict.empty({jppws__hiqyc}, types.int64),\n'
        )
    vxf__xsgo += (
        f'        types.DictType({jppws__hiqyc}, types.int64)(), [],)\n')
    vxf__xsgo += '    return index_val._getvalue()\n'
    huj__llz = {}
    exec(vxf__xsgo, {'bodo': bodo, 'signature': signature, 'cgutils':
        cgutils, 'numba': numba, 'types': types, 'bytes_type': bytes_type,
        'string_type': string_type, 'string_array_type': string_array_type,
        'binary_array_type': binary_array_type}, huj__llz)
    impl = huj__llz['impl']
    return impl


@overload_method(BinaryIndexType, 'copy', no_unliteral=True)
@overload_method(StringIndexType, 'copy', no_unliteral=True)
def overload_binary_string_index_copy(A):
    return lambda A: bodo.hiframes.pd_index_ext.init_binary_str_index(A.
        _data.copy(), A._name)


@overload_attribute(BinaryIndexType, 'name')
@overload_attribute(StringIndexType, 'name')
@overload_attribute(DatetimeIndexType, 'name')
@overload_attribute(TimedeltaIndexType, 'name')
@overload_attribute(RangeIndexType, 'name')
@overload_attribute(PeriodIndexType, 'name')
@overload_attribute(NumericIndexType, 'name')
@overload_attribute(StringIndexType, 'name')
def Index_get_name(i):

    def impl(i):
        return i._name
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_index_getitem(I, ind):
    if isinstance(I, (NumericIndexType, StringIndexType, BinaryIndexType)
        ) and isinstance(ind, types.Integer):
        return lambda I, ind: bodo.hiframes.pd_index_ext.get_index_data(I)[ind]
    if isinstance(I, NumericIndexType):
        return lambda I, ind: bodo.hiframes.pd_index_ext.init_numeric_index(
            bodo.hiframes.pd_index_ext.get_index_data(I)[ind], bodo.
            hiframes.pd_index_ext.get_index_name(I))
    if isinstance(I, (StringIndexType, BinaryIndexType)):
        return lambda I, ind: bodo.hiframes.pd_index_ext.init_binary_str_index(
            bodo.hiframes.pd_index_ext.get_index_data(I)[ind], bodo.
            hiframes.pd_index_ext.get_index_name(I))


def array_type_to_index(arr_typ, name_typ=None):
    if arr_typ == bodo.string_array_type:
        return StringIndexType(name_typ)
    if arr_typ == bodo.binary_array_type:
        return BinaryIndexType(name_typ)
    assert isinstance(arr_typ, (types.Array, IntegerArrayType, bodo.
        CategoricalArrayType)) or arr_typ in (bodo.datetime_date_array_type,
        bodo.boolean_array
        ), f'Converting array type {arr_typ} to index not supported'
    if (arr_typ == bodo.datetime_date_array_type or arr_typ.dtype == types.
        NPDatetime('ns')):
        return DatetimeIndexType(name_typ)
    if isinstance(arr_typ, bodo.CategoricalArrayType):
        return CategoricalIndexType(arr_typ, name_typ)
    if arr_typ.dtype == types.NPTimedelta('ns'):
        return TimedeltaIndexType(name_typ)
    if isinstance(arr_typ.dtype, (types.Integer, types.Float, types.Boolean)):
        return NumericIndexType(arr_typ.dtype, name_typ, arr_typ)
    raise BodoError(f'invalid index type {arr_typ}')


def is_pd_index_type(t):
    return isinstance(t, (NumericIndexType, DatetimeIndexType,
        TimedeltaIndexType, IntervalIndexType, CategoricalIndexType,
        PeriodIndexType, StringIndexType, BinaryIndexType, RangeIndexType,
        HeterogeneousIndexType))


@overload_method(RangeIndexType, 'take', no_unliteral=True)
@overload_method(NumericIndexType, 'take', no_unliteral=True)
@overload_method(StringIndexType, 'take', no_unliteral=True)
@overload_method(BinaryIndexType, 'take', no_unliteral=True)
@overload_method(CategoricalIndexType, 'take', no_unliteral=True)
@overload_method(PeriodIndexType, 'take', no_unliteral=True)
@overload_method(DatetimeIndexType, 'take', no_unliteral=True)
@overload_method(TimedeltaIndexType, 'take', no_unliteral=True)
def overload_index_take(I, indices):
    return lambda I, indices: I[indices]


@numba.njit(no_cpython_wrapper=True)
def _init_engine(I):
    if len(I) > 0 and not I._dict:
        uhlkt__qat = bodo.utils.conversion.coerce_to_array(I)
        for i in range(len(uhlkt__qat)):
            val = uhlkt__qat[i]
            if val in I._dict:
                raise ValueError(
                    'Index.get_loc(): non-unique Index not supported yet')
            I._dict[val] = i


@overload(operator.contains, no_unliteral=True)
def index_contains(I, val):
    if not is_index_type(I):
        return
    if isinstance(I, RangeIndexType):
        return lambda I, val: range_contains(I.start, I.stop, I.step, val)

    def impl(I, val):
        _init_engine(I)
        return bodo.utils.conversion.unbox_if_timestamp(val) in I._dict
    return impl


@register_jitable
def range_contains(start, stop, step, val):
    if step > 0 and not start <= val < stop:
        return False
    if step < 0 and not stop <= val < start:
        return False
    return (val - start) % step == 0


@overload_method(RangeIndexType, 'get_loc', no_unliteral=True)
@overload_method(NumericIndexType, 'get_loc', no_unliteral=True)
@overload_method(StringIndexType, 'get_loc', no_unliteral=True)
@overload_method(BinaryIndexType, 'get_loc', no_unliteral=True)
@overload_method(PeriodIndexType, 'get_loc', no_unliteral=True)
@overload_method(DatetimeIndexType, 'get_loc', no_unliteral=True)
@overload_method(TimedeltaIndexType, 'get_loc', no_unliteral=True)
def overload_index_get_loc(I, key, method=None, tolerance=None):
    lmmer__fzbf = dict(method=method, tolerance=tolerance)
    yog__ujpbd = dict(method=None, tolerance=None)
    check_unsupported_args('Index.get_loc', lmmer__fzbf, yog__ujpbd)
    key = types.unliteral(key)
    if key == pd_timestamp_type:
        key = bodo.datetime64ns
    if key == pd_timedelta_type:
        key = bodo.timedelta64ns
    if key != I.dtype:
        raise_bodo_error(
            'Index.get_loc(): invalid label type in Index.get_loc()')
    if isinstance(I, RangeIndexType):

        def impl_range(I, key, method=None, tolerance=None):
            if not range_contains(I.start, I.stop, I.step, key):
                raise KeyError('Index.get_loc(): key not found')
            return key - I.start if I.step == 1 else (key - I.start) // I.step
        return impl_range

    def impl(I, key, method=None, tolerance=None):
        _init_engine(I)
        key = bodo.utils.conversion.unbox_if_timestamp(key)
        ind = I._dict.get(key, -1)
        if ind == -1:
            raise KeyError('Index.get_loc(): key not found')
        return ind
    return impl


@overload_method(RangeIndexType, 'isna', no_unliteral=True)
@overload_method(NumericIndexType, 'isna', no_unliteral=True)
@overload_method(StringIndexType, 'isna', no_unliteral=True)
@overload_method(BinaryIndexType, 'isna', no_unliteral=True)
@overload_method(CategoricalIndexType, 'isna', no_unliteral=True)
@overload_method(PeriodIndexType, 'isna', no_unliteral=True)
@overload_method(DatetimeIndexType, 'isna', no_unliteral=True)
@overload_method(TimedeltaIndexType, 'isna', no_unliteral=True)
@overload_method(RangeIndexType, 'isnull', no_unliteral=True)
@overload_method(NumericIndexType, 'isnull', no_unliteral=True)
@overload_method(StringIndexType, 'isnull', no_unliteral=True)
@overload_method(BinaryIndexType, 'isnull', no_unliteral=True)
@overload_method(CategoricalIndexType, 'isnull', no_unliteral=True)
@overload_method(PeriodIndexType, 'isnull', no_unliteral=True)
@overload_method(DatetimeIndexType, 'isnull', no_unliteral=True)
@overload_method(TimedeltaIndexType, 'isnull', no_unliteral=True)
def overload_index_isna(I):
    if isinstance(I, RangeIndexType):

        def impl(I):
            numba.parfors.parfor.init_prange()
            wxqom__mdnd = len(I)
            qjxhk__osk = np.empty(wxqom__mdnd, np.bool_)
            for i in numba.parfors.parfor.internal_prange(wxqom__mdnd):
                qjxhk__osk[i] = False
            return qjxhk__osk
        return impl

    def impl(I):
        numba.parfors.parfor.init_prange()
        uhlkt__qat = bodo.hiframes.pd_index_ext.get_index_data(I)
        wxqom__mdnd = len(uhlkt__qat)
        qjxhk__osk = np.empty(wxqom__mdnd, np.bool_)
        for i in numba.parfors.parfor.internal_prange(wxqom__mdnd):
            qjxhk__osk[i] = bodo.libs.array_kernels.isna(uhlkt__qat, i)
        return qjxhk__osk
    return impl


@overload_attribute(RangeIndexType, 'values')
@overload_attribute(NumericIndexType, 'values')
@overload_attribute(StringIndexType, 'values')
@overload_attribute(BinaryIndexType, 'values')
@overload_attribute(CategoricalIndexType, 'values')
@overload_attribute(PeriodIndexType, 'values')
@overload_attribute(DatetimeIndexType, 'values')
@overload_attribute(TimedeltaIndexType, 'values')
def overload_values(I):
    return lambda I: bodo.utils.conversion.coerce_to_array(I)


@overload(len, no_unliteral=True)
def overload_index_len(I):
    if isinstance(I, (NumericIndexType, StringIndexType, BinaryIndexType,
        PeriodIndexType, IntervalIndexType, CategoricalIndexType,
        DatetimeIndexType, TimedeltaIndexType)):
        return lambda I: len(bodo.hiframes.pd_index_ext.get_index_data(I))


@overload_attribute(DatetimeIndexType, 'shape')
@overload_attribute(NumericIndexType, 'shape')
@overload_attribute(StringIndexType, 'shape')
@overload_attribute(BinaryIndexType, 'shape')
@overload_attribute(PeriodIndexType, 'shape')
@overload_attribute(TimedeltaIndexType, 'shape')
@overload_attribute(IntervalIndexType, 'shape')
@overload_attribute(CategoricalIndexType, 'shape')
def overload_index_shape(s):
    return lambda s: (len(bodo.hiframes.pd_index_ext.get_index_data(s)),)


@overload_attribute(RangeIndexType, 'shape')
def overload_range_index_shape(s):
    return lambda s: (len(s),)


@numba.generated_jit(nopython=True)
def get_index_data(S):
    return lambda S: S._data


@numba.generated_jit(nopython=True)
def get_index_name(S):
    return lambda S: S._name


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_index_data',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_datetime_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_timedelta_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_numeric_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_binary_str_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['init_categorical_index',
    'bodo.hiframes.pd_index_ext'] = alias_ext_dummy_func


def get_index_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    zxl__flf = args[0]
    if equiv_set.has_shape(zxl__flf):
        return ArrayAnalysis.AnalyzeResult(shape=zxl__flf, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_index_ext_get_index_data
    ) = get_index_data_equiv


@overload_method(RangeIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(NumericIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(StringIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(BinaryIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(CategoricalIndexType, 'map', inline='always', no_unliteral
    =True)
@overload_method(PeriodIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(DatetimeIndexType, 'map', inline='always', no_unliteral=True)
@overload_method(TimedeltaIndexType, 'map', inline='always', no_unliteral=True)
def overload_index_map(I, mapper, na_action=None):
    if not is_const_func_type(mapper):
        raise BodoError("Index.map(): 'mapper' should be a function")
    dtype = I.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = pd_timestamp_type
    if dtype == types.NPTimedelta('ns'):
        dtype = pd_timedelta_type
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):
        dtype = dtype.elem_type
    qbsk__cfc = numba.core.registry.cpu_target.typing_context
    tliw__ckdmv = numba.core.registry.cpu_target.target_context
    try:
        hdrno__ntxvr = get_const_func_output_type(mapper, (dtype,), {},
            qbsk__cfc, tliw__ckdmv)
    except Exception as gkir__hpssm:
        raise_bodo_error(get_udf_error_msg('Index.map()', gkir__hpssm))
    coeb__meak = get_udf_out_arr_type(hdrno__ntxvr)
    func = get_overload_const_func(mapper, None)
    vxf__xsgo = 'def f(I, mapper, na_action=None):\n'
    vxf__xsgo += '  name = bodo.hiframes.pd_index_ext.get_index_name(I)\n'
    vxf__xsgo += '  A = bodo.utils.conversion.coerce_to_array(I)\n'
    vxf__xsgo += '  numba.parfors.parfor.init_prange()\n'
    vxf__xsgo += '  n = len(A)\n'
    vxf__xsgo += '  S = bodo.utils.utils.alloc_type(n, _arr_typ, (-1,))\n'
    vxf__xsgo += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    vxf__xsgo += '    t2 = bodo.utils.conversion.box_if_dt64(A[i])\n'
    vxf__xsgo += '    v = map_func(t2)\n'
    vxf__xsgo += '    S[i] = bodo.utils.conversion.unbox_if_timestamp(v)\n'
    vxf__xsgo += '  return bodo.utils.conversion.index_from_array(S, name)\n'
    chvk__qmnfa = bodo.compiler.udf_jit(func)
    huj__llz = {}
    exec(vxf__xsgo, {'numba': numba, 'np': np, 'pd': pd, 'bodo': bodo,
        'map_func': chvk__qmnfa, '_arr_typ': coeb__meak,
        'init_nested_counts': bodo.utils.indexing.init_nested_counts,
        'add_nested_counts': bodo.utils.indexing.add_nested_counts,
        'data_arr_type': coeb__meak.dtype}, huj__llz)
    f = huj__llz['f']
    return f


@lower_builtin(operator.is_, NumericIndexType, NumericIndexType)
@lower_builtin(operator.is_, StringIndexType, StringIndexType)
@lower_builtin(operator.is_, BinaryIndexType, BinaryIndexType)
@lower_builtin(operator.is_, PeriodIndexType, PeriodIndexType)
@lower_builtin(operator.is_, DatetimeIndexType, DatetimeIndexType)
@lower_builtin(operator.is_, TimedeltaIndexType, TimedeltaIndexType)
@lower_builtin(operator.is_, IntervalIndexType, IntervalIndexType)
@lower_builtin(operator.is_, CategoricalIndexType, CategoricalIndexType)
def index_is(context, builder, sig, args):
    trdlo__antuh, axx__ogo = sig.args
    if trdlo__antuh != axx__ogo:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return a._data is b._data and a._name is b._name
    return context.compile_internal(builder, index_is_impl, sig, args)


@lower_builtin(operator.is_, RangeIndexType, RangeIndexType)
def range_index_is(context, builder, sig, args):
    trdlo__antuh, axx__ogo = sig.args
    if trdlo__antuh != axx__ogo:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._start == b._start and a._stop == b._stop and a._step ==
            b._step and a._name is b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)


def create_binary_op_overload(op):

    def overload_index_binary_op(lhs, rhs):
        if is_index_type(lhs):

            def impl(lhs, rhs):
                uhlkt__qat = bodo.utils.conversion.coerce_to_array(lhs)
                koz__cjq = bodo.utils.conversion.get_array_if_series_or_index(
                    rhs)
                qjxhk__osk = op(uhlkt__qat, koz__cjq)
                return qjxhk__osk
            return impl
        if is_index_type(rhs):

            def impl2(lhs, rhs):
                uhlkt__qat = bodo.utils.conversion.coerce_to_array(rhs)
                koz__cjq = bodo.utils.conversion.get_array_if_series_or_index(
                    lhs)
                qjxhk__osk = op(koz__cjq, uhlkt__qat)
                return qjxhk__osk
            return impl2
        if isinstance(lhs, HeterogeneousIndexType):
            if not is_heterogeneous_tuple_type(lhs.data):

                def impl3(lhs, rhs):
                    data = bodo.utils.conversion.coerce_to_array(lhs)
                    uhlkt__qat = bodo.utils.conversion.coerce_to_array(data)
                    koz__cjq = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    qjxhk__osk = op(uhlkt__qat, koz__cjq)
                    return qjxhk__osk
                return impl3
            count = len(lhs.data.types)
            vxf__xsgo = 'def f(lhs, rhs):\n'
            vxf__xsgo += '  return [{}]\n'.format(','.join(
                'op(lhs[{}], rhs{})'.format(i, f'[{i}]' if is_iterable_type
                (rhs) else '') for i in range(count)))
            huj__llz = {}
            exec(vxf__xsgo, {'op': op, 'np': np}, huj__llz)
            impl = huj__llz['f']
            return impl
        if isinstance(rhs, HeterogeneousIndexType):
            if not is_heterogeneous_tuple_type(rhs.data):

                def impl4(lhs, rhs):
                    data = bodo.hiframes.pd_index_ext.get_index_data(rhs)
                    uhlkt__qat = bodo.utils.conversion.coerce_to_array(data)
                    koz__cjq = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    qjxhk__osk = op(koz__cjq, uhlkt__qat)
                    return qjxhk__osk
                return impl4
            count = len(rhs.data.types)
            vxf__xsgo = 'def f(lhs, rhs):\n'
            vxf__xsgo += '  return [{}]\n'.format(','.join(
                'op(lhs{}, rhs[{}])'.format(f'[{i}]' if is_iterable_type(
                lhs) else '', i) for i in range(count)))
            huj__llz = {}
            exec(vxf__xsgo, {'op': op, 'np': np}, huj__llz)
            impl = huj__llz['f']
            return impl
    return overload_index_binary_op


skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        overload_impl = create_binary_op_overload(op)
        overload(op, inline='always')(overload_impl)


_install_binary_ops()


def is_index_type(t):
    return isinstance(t, (RangeIndexType, NumericIndexType, StringIndexType,
        BinaryIndexType, PeriodIndexType, DatetimeIndexType,
        TimedeltaIndexType, IntervalIndexType, CategoricalIndexType))


@lower_cast(RangeIndexType, NumericIndexType)
def cast_range_index_to_int_index(context, builder, fromty, toty, val):
    f = lambda I: init_numeric_index(np.arange(I._start, I._stop, I._step),
        bodo.hiframes.pd_index_ext.get_index_name(I))
    return context.compile_internal(builder, f, toty(fromty), [val])


class HeterogeneousIndexType(types.Type):
    ndim = 1

    def __init__(self, data=None, name_type=None):
        self.data = data
        name_type = types.none if name_type is None else name_type
        self.name_type = name_type
        super(HeterogeneousIndexType, self).__init__(name=
            f'heter_index({data}, {name_type})')

    def copy(self):
        return HeterogeneousIndexType(self.data, self.name_type)

    @property
    def key(self):
        return self.data, self.name_type


@register_model(HeterogeneousIndexType)
class HeterogeneousIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        and__chw = [('data', fe_type.data), ('name', fe_type.name_type)]
        super(HeterogeneousIndexModel, self).__init__(dmm, fe_type, and__chw)


make_attribute_wrapper(HeterogeneousIndexType, 'data', '_data')
make_attribute_wrapper(HeterogeneousIndexType, 'name', '_name')


@overload_method(HeterogeneousIndexType, 'copy', no_unliteral=True)
def overload_heter_index_copy(A):
    return lambda A: bodo.hiframes.pd_index_ext.init_heter_index(A._data, A
        ._name)


@box(HeterogeneousIndexType)
def box_heter_index(typ, val, c):
    dyehf__dpvnv = c.context.insert_const_string(c.builder.module, 'pandas')
    fatg__wwpx = c.pyapi.import_module_noblock(dyehf__dpvnv)
    cgie__tcdit = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.data, cgie__tcdit.data)
    zfky__xrwm = c.pyapi.from_native_value(typ.data, cgie__tcdit.data, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.name_type, cgie__tcdit.name)
    shlcu__zxqrv = c.pyapi.from_native_value(typ.name_type, cgie__tcdit.
        name, c.env_manager)
    asqz__cftzh = c.pyapi.make_none()
    qch__pfnje = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    nnwyj__hexmz = c.pyapi.call_method(fatg__wwpx, 'Index', (zfky__xrwm,
        asqz__cftzh, qch__pfnje, shlcu__zxqrv))
    c.pyapi.decref(zfky__xrwm)
    c.pyapi.decref(asqz__cftzh)
    c.pyapi.decref(qch__pfnje)
    c.pyapi.decref(shlcu__zxqrv)
    c.pyapi.decref(fatg__wwpx)
    c.context.nrt.decref(c.builder, typ, val)
    return nnwyj__hexmz


@intrinsic
def init_heter_index(typingctx, data, name=None):
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        assert len(args) == 2
        dyt__bwlv = signature.return_type
        cgie__tcdit = cgutils.create_struct_proxy(dyt__bwlv)(context, builder)
        cgie__tcdit.data = args[0]
        cgie__tcdit.name = args[1]
        context.nrt.incref(builder, dyt__bwlv.data, args[0])
        context.nrt.incref(builder, dyt__bwlv.name_type, args[1])
        return cgie__tcdit._getvalue()
    return HeterogeneousIndexType(data, name)(data, name), codegen


@overload_attribute(HeterogeneousIndexType, 'name')
def heter_index_get_name(i):

    def impl(i):
        return i._name
    return impl


@overload_attribute(NumericIndexType, 'nbytes')
@overload_attribute(DatetimeIndexType, 'nbytes')
@overload_attribute(TimedeltaIndexType, 'nbytes')
@overload_attribute(RangeIndexType, 'nbytes')
@overload_attribute(StringIndexType, 'nbytes')
@overload_attribute(BinaryIndexType, 'nbytes')
@overload_attribute(CategoricalIndexType, 'nbytes')
@overload_attribute(PeriodIndexType, 'nbytes')
def overload_nbytes(I):
    if isinstance(I, RangeIndexType):

        def _impl_nbytes(I):
            return bodo.io.np_io.get_dtype_size(type(I._start)
                ) + bodo.io.np_io.get_dtype_size(type(I._step)
                ) + bodo.io.np_io.get_dtype_size(type(I._stop))
        return _impl_nbytes
    else:

        def _impl_nbytes(I):
            return I._data.nbytes
        return _impl_nbytes


@overload(operator.getitem, no_unliteral=True)
def overload_heter_index_getitem(I, ind):
    if not isinstance(I, HeterogeneousIndexType):
        return
    if isinstance(ind, types.Integer):
        return lambda I, ind: bodo.hiframes.pd_index_ext.get_index_data(I)[ind]
    if isinstance(I, HeterogeneousIndexType):
        return lambda I, ind: bodo.hiframes.pd_index_ext.init_heter_index(bodo
            .hiframes.pd_index_ext.get_index_data(I)[ind], bodo.hiframes.
            pd_index_ext.get_index_name(I))


@lower_constant(DatetimeIndexType)
@lower_constant(TimedeltaIndexType)
def lower_constant_time_index(context, builder, ty, pyval):
    data = context.get_constant_generic(builder, types.Array(types.int64, 1,
        'C'), pyval.values.view(np.int64))
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    evby__pgz = cgutils.create_struct_proxy(ty)(context, builder)
    evby__pgz.data = data
    evby__pgz.name = name
    dtype = ty.dtype
    evby__pgz.dict = context.compile_internal(builder, lambda : numba.typed
        .Dict.empty(dtype, types.int64), types.DictType(dtype, types.int64)
        (), [])
    return evby__pgz._getvalue()


@lower_constant(PeriodIndexType)
def lower_constant_period_index(context, builder, ty, pyval):
    data = context.get_constant_generic(builder, types.Array(types.int64, 1,
        'C'), pyval.asi8)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    cgie__tcdit = cgutils.create_struct_proxy(ty)(context, builder)
    cgie__tcdit.data = data
    cgie__tcdit.name = name
    cgie__tcdit.dict = context.compile_internal(builder, lambda : numba.
        typed.Dict.empty(types.int64, types.int64), types.DictType(types.
        int64, types.int64)(), [])
    return cgie__tcdit._getvalue()


@lower_constant(NumericIndexType)
def lower_constant_numeric_index(context, builder, ty, pyval):
    assert isinstance(ty.dtype, (types.Integer, types.Float, types.Boolean))
    data = context.get_constant_generic(builder, types.Array(ty.dtype, 1,
        'C'), pyval.values)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    cgie__tcdit = cgutils.create_struct_proxy(ty)(context, builder)
    cgie__tcdit.data = data
    cgie__tcdit.name = name
    dtype = ty.dtype
    cgie__tcdit.dict = context.compile_internal(builder, lambda : numba.
        typed.Dict.empty(dtype, types.int64), types.DictType(dtype, types.
        int64)(), [])
    return cgie__tcdit._getvalue()


@lower_constant(StringIndexType)
@lower_constant(BinaryIndexType)
def lower_constant_binary_string_index(context, builder, ty, pyval):
    nilv__zqj = ty.data
    scalar_type = ty.data.dtype
    data = context.get_constant_generic(builder, nilv__zqj, pyval.values)
    name = context.get_constant_generic(builder, ty.name_typ, pyval.name)
    cgie__tcdit = cgutils.create_struct_proxy(ty)(context, builder)
    cgie__tcdit.data = data
    cgie__tcdit.name = name
    cgie__tcdit.dict = context.compile_internal(builder, lambda : numba.
        typed.Dict.empty(scalar_type, types.int64), types.DictType(
        scalar_type, types.int64)(), [])
    return cgie__tcdit._getvalue()


@lower_builtin('getiter', RangeIndexType)
def getiter_range_index(context, builder, sig, args):
    [hcyy__amf] = sig.args
    [vmd__teg] = args
    pth__ebb = context.make_helper(builder, hcyy__amf, value=vmd__teg)
    iycjh__cklk = context.make_helper(builder, sig.return_type)
    ugx__xtorv = cgutils.alloca_once_value(builder, pth__ebb.start)
    hdrbx__sxjt = context.get_constant(types.intp, 0)
    sgcc__unzuv = cgutils.alloca_once_value(builder, hdrbx__sxjt)
    iycjh__cklk.iter = ugx__xtorv
    iycjh__cklk.stop = pth__ebb.stop
    iycjh__cklk.step = pth__ebb.step
    iycjh__cklk.count = sgcc__unzuv
    hbs__qhgc = builder.sub(pth__ebb.stop, pth__ebb.start)
    cefkk__znzb = context.get_constant(types.intp, 1)
    lggl__btbm = builder.icmp(lc.ICMP_SGT, hbs__qhgc, hdrbx__sxjt)
    bcrbv__dlh = builder.icmp(lc.ICMP_SGT, pth__ebb.step, hdrbx__sxjt)
    voixr__svdua = builder.not_(builder.xor(lggl__btbm, bcrbv__dlh))
    with builder.if_then(voixr__svdua):
        hldn__wft = builder.srem(hbs__qhgc, pth__ebb.step)
        hldn__wft = builder.select(lggl__btbm, hldn__wft, builder.neg(
            hldn__wft))
        lawin__rpe = builder.icmp(lc.ICMP_SGT, hldn__wft, hdrbx__sxjt)
        acetv__svg = builder.add(builder.sdiv(hbs__qhgc, pth__ebb.step),
            builder.select(lawin__rpe, cefkk__znzb, hdrbx__sxjt))
        builder.store(acetv__svg, sgcc__unzuv)
    vefhm__jck = iycjh__cklk._getvalue()
    uem__xhwa = impl_ret_new_ref(context, builder, sig.return_type, vefhm__jck)
    return uem__xhwa


def getiter_index(context, builder, sig, args):
    [hcyy__amf] = sig.args
    [vmd__teg] = args
    pth__ebb = context.make_helper(builder, hcyy__amf, value=vmd__teg)
    return numba.np.arrayobj.getiter_array(context, builder, signature(sig.
        return_type, sig.args[0].data), (pth__ebb.data,))


def _install_index_getiter():
    qqs__bldt = [NumericIndexType, StringIndexType, BinaryIndexType,
        CategoricalIndexType, TimedeltaIndexType, DatetimeIndexType]
    for typ in qqs__bldt:
        lower_builtin('getiter', typ)(getiter_index)


_install_index_getiter()
index_unsupported = ['all', 'any', 'append', 'argmax', 'argmin', 'argsort',
    'asof', 'asof_locs', 'astype', 'delete', 'difference', 'drop',
    'drop_duplicates', 'droplevel', 'dropna', 'duplicated', 'equals',
    'factorize', 'fillna', 'format', 'get_indexer', 'get_indexer_for',
    'get_indexer_non_unique', 'get_level_values', 'get_slice_bound',
    'get_value', 'groupby', 'holds_integer', 'identical', 'insert',
    'intersection', 'is_', 'is_boolean', 'is_categorical', 'is_floating',
    'is_integer', 'is_interval', 'is_mixed', 'is_numeric', 'is_object',
    'is_type_compatible', 'isin', 'item', 'join', 'memory_usage', 'notna',
    'notnull', 'nunique', 'putmask', 'ravel', 'reindex', 'rename', 'repeat',
    'searchsorted', 'set_names', 'set_value', 'shift', 'slice_indexer',
    'slice_locs', 'sort', 'sort_values', 'sortlevel', 'str',
    'symmetric_difference', 'to_flat_index', 'to_frame', 'to_list',
    'to_native_types', 'to_numpy', 'to_series', 'tolist', 'transpose',
    'union', 'unique', 'value_counts', 'view', 'where']


def _install_index_unsupported():
    qqs__bldt = [('NumericIndexType.', NumericIndexType), (
        'StringIndexType.', StringIndexType), ('BinaryIndexType.',
        BinaryIndexType), ('TimedeltaIndexType.', TimedeltaIndexType), (
        'IntervalIndexType.', IntervalIndexType), ('CategoricalIndexType.',
        CategoricalIndexType), ('PeriodIndexType.', PeriodIndexType), (
        'DatetimeIndexType.', DatetimeIndexType)]
    for zin__wlpf in index_unsupported:
        for uplgw__nfgwt, typ in qqs__bldt:
            overload_method(typ, zin__wlpf, no_unliteral=True)(
                create_unsupported_overload(uplgw__nfgwt + zin__wlpf))


_install_index_unsupported()
