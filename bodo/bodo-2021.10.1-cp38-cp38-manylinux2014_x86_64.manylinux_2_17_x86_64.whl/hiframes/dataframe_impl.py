"""
Implementation of DataFrame attributes and methods using overload.
"""
import operator
import re
import warnings
from collections import namedtuple
import llvmlite.llvmpy.core as lc
import numba
import numpy as np
import pandas as pd
from numba.core import cgutils, ir, types
from numba.core.imputils import RefType, impl_ret_borrowed, impl_ret_new_ref, iternext_impl, lower_builtin
from numba.core.ir_utils import mk_unique_var, next_label
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import models, overload, overload_attribute, overload_method, register_model, type_callable
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType, handle_inplace_df_type_change
from bodo.hiframes.pd_index_ext import StringIndexType
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import SeriesType, if_series_to_array_type
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_type
from bodo.hiframes.rolling import is_supported_shift_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_ext import string_type
from bodo.utils.transform import bodo_types_with_params, gen_const_tup, no_side_effect_call_tuples
from bodo.utils.typing import BodoError, BodoWarning, check_unsupported_args, dtype_to_array_type, ensure_constant_arg, ensure_constant_values, get_index_data_arr_types, get_index_names, get_nullable_and_non_nullable_types, get_overload_const_bool, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_const_tuple, get_overload_constant_dict, get_overload_constant_series, is_common_scalar_dtype, is_literal_type, is_overload_bool, is_overload_bool_list, is_overload_constant_bool, is_overload_constant_dict, is_overload_constant_int, is_overload_constant_list, is_overload_constant_series, is_overload_constant_str, is_overload_constant_tuple, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_overload_zero, parse_dtype, raise_bodo_error, raise_const_error, unliteral_val
from bodo.utils.utils import is_array_typ


@overload_attribute(DataFrameType, 'index', inline='always')
def overload_dataframe_index(df):
    return lambda df: bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)


def generate_col_to_index_func_text(col_names):
    if all(isinstance(a, str) for a in col_names) or all(isinstance(a,
        bytes) for a in col_names):
        jyj__ymsj = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return (
            f'bodo.hiframes.pd_index_ext.init_binary_str_index({jyj__ymsj})\n')
    elif all(isinstance(a, (int, float)) for a in col_names):
        arr = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return f'bodo.hiframes.pd_index_ext.init_numeric_index({arr})\n'
    else:
        return f'bodo.hiframes.pd_index_ext.init_heter_index({col_names})\n'


@overload_attribute(DataFrameType, 'columns', inline='always')
def overload_dataframe_columns(df):
    aaw__xjp = 'def impl(df):\n'
    ely__qbuy = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(df
        .columns)
    aaw__xjp += f'  return {ely__qbuy}'
    wyudp__cpm = {}
    exec(aaw__xjp, {'bodo': bodo}, wyudp__cpm)
    impl = wyudp__cpm['impl']
    return impl


@overload_attribute(DataFrameType, 'values')
def overload_dataframe_values(df):
    istxx__jnt = len(df.columns)
    uxl__oumzb = set(i for i in range(istxx__jnt) if isinstance(df.data[i],
        IntegerArrayType))
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(i, '.astype(float)' if i in uxl__oumzb else '') for i in
        range(istxx__jnt))
    aaw__xjp = 'def f(df):\n'.format()
    aaw__xjp += '    return np.stack(({},), 1)\n'.format(data_args)
    wyudp__cpm = {}
    exec(aaw__xjp, {'bodo': bodo, 'np': np}, wyudp__cpm)
    ivc__kpm = wyudp__cpm['f']
    return ivc__kpm


@overload_method(DataFrameType, 'to_numpy', inline='always', no_unliteral=True)
def overload_dataframe_to_numpy(df, dtype=None, copy=False):
    mwezv__himy = {'dtype': dtype}
    bnhi__bodsb = {'dtype': None}
    check_unsupported_args('to_numpy', mwezv__himy, bnhi__bodsb)

    def impl(df, dtype=None, copy=False):
        return df.values
    return impl


@overload_attribute(DataFrameType, 'ndim', inline='always')
def overload_dataframe_ndim(df):
    return lambda df: 2


@overload_attribute(DataFrameType, 'size')
def overload_dataframe_size(df):
    ncols = len(df.columns)
    return lambda df: ncols * len(df)


@overload_attribute(DataFrameType, 'shape')
def overload_dataframe_shape(df):
    ncols = len(df.columns)
    return lambda df: (len(df), types.int64(ncols))


@overload_attribute(DataFrameType, 'dtypes')
def overload_dataframe_dtypes(df):
    aaw__xjp = 'def impl(df):\n'
    data = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype\n'
         for i in range(len(df.columns)))
    fpowr__ixu = ',' if len(df.columns) == 1 else ''
    index = f'bodo.hiframes.pd_index_ext.init_heter_index({df.columns})'
    aaw__xjp += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}{fpowr__ixu}), {index}, None)
"""
    wyudp__cpm = {}
    exec(aaw__xjp, {'bodo': bodo}, wyudp__cpm)
    impl = wyudp__cpm['impl']
    return impl


@overload_attribute(DataFrameType, 'empty')
def overload_dataframe_empty(df):
    if len(df.columns) == 0:
        return lambda df: True
    return lambda df: len(df) == 0


@overload_method(DataFrameType, 'assign', no_unliteral=True)
def overload_dataframe_assign(df, **kwargs):
    raise_bodo_error('Invalid df.assign() call')


@overload_method(DataFrameType, 'insert', no_unliteral=True)
def overload_dataframe_insert(df, loc, column, value, allow_duplicates=False):
    raise_bodo_error('Invalid df.insert() call')


def _get_dtype_str(dtype):
    if isinstance(dtype, types.Function):
        if dtype.key[0] == str:
            return "'str'"
        elif dtype.key[0] == float:
            return 'float'
        elif dtype.key[0] == int:
            return 'int'
        elif dtype.key[0] == bool:
            return 'bool'
        else:
            raise BodoError(f'invalid dtype: {dtype}')
    if isinstance(dtype, types.DTypeSpec):
        dtype = dtype.dtype
    if isinstance(dtype, types.functions.NumberClass):
        return f"'{dtype.key}'"
    if dtype in (bodo.libs.str_arr_ext.string_dtype, pd.StringDtype()):
        return 'str'
    return f"'{dtype}'"


@overload_method(DataFrameType, 'astype', inline='always', no_unliteral=True)
def overload_dataframe_astype(df, dtype, copy=True, errors='raise',
    _bodo_nan_to_str=True):
    mwezv__himy = {'copy': copy, 'errors': errors}
    bnhi__bodsb = {'copy': True, 'errors': 'raise'}
    check_unsupported_args('df.astype', mwezv__himy, bnhi__bodsb)
    if dtype == types.unicode_type:
        raise_bodo_error(
            "DataFrame.astype(): 'dtype' when passed as string must be a constant value"
            )
    if is_overload_constant_dict(dtype) or is_overload_constant_series(dtype):
        stro__ojn = get_overload_constant_dict(dtype
            ) if is_overload_constant_dict(dtype) else dict(
            get_overload_constant_series(dtype))
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {_get_dtype_str(stro__ojn[ebc__koy])}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             if ebc__koy in stro__ojn else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for
            i, ebc__koy in enumerate(df.columns))
    else:
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dtype, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             for i in range(len(df.columns)))
    header = (
        "def impl(df, dtype, copy=True, errors='raise', _bodo_nan_to_str=True):\n"
        )
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'copy', inline='always', no_unliteral=True)
def overload_dataframe_copy(df, deep=True):
    bpk__anfwi = []
    for i in range(len(df.columns)):
        arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
        if is_overload_true(deep):
            bpk__anfwi.append(arr + '.copy()')
        elif is_overload_false(deep):
            bpk__anfwi.append(arr)
        else:
            bpk__anfwi.append(f'{arr}.copy() if deep else {arr}')
    header = 'def impl(df, deep=True):\n'
    return _gen_init_df(header, df.columns, ', '.join(bpk__anfwi))


@overload_method(DataFrameType, 'rename', inline='always', no_unliteral=True)
def overload_dataframe_rename(df, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False, level=None, errors='ignore',
    _bodo_transformed=False):
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'rename')
    mwezv__himy = {'index': index, 'level': level, 'errors': errors}
    bnhi__bodsb = {'index': None, 'level': None, 'errors': 'ignore'}
    check_unsupported_args('DataFrame.rename', mwezv__himy, bnhi__bodsb)
    if not is_overload_constant_bool(inplace):
        raise BodoError(
            "DataFrame.rename(): 'inplace' keyword only supports boolean constant assignment"
            )
    if not is_overload_none(mapper):
        if not is_overload_none(columns):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'mapper' and 'columns'"
                )
        if not (is_overload_constant_int(axis) and get_overload_const_int(
            axis) == 1):
            raise BodoError(
                "DataFrame.rename(): 'mapper' only supported with axis=1")
        if not is_overload_constant_dict(mapper):
            raise_bodo_error(
                "'mapper' argument to DataFrame.rename() should be a constant dictionary"
                )
        kjjy__ukmk = get_overload_constant_dict(mapper)
    elif not is_overload_none(columns):
        if not is_overload_none(axis):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'axis' and 'columns'")
        if not is_overload_constant_dict(columns):
            raise_bodo_error(
                "'columns' argument to DataFrame.rename() should be a constant dictionary"
                )
        kjjy__ukmk = get_overload_constant_dict(columns)
    else:
        raise_bodo_error(
            "DataFrame.rename(): must pass columns either via 'mapper' and 'axis'=1 or 'columns'"
            )
    dxhyd__krkcp = [kjjy__ukmk.get(df.columns[i], df.columns[i]) for i in
        range(len(df.columns))]
    bpk__anfwi = []
    for i in range(len(df.columns)):
        arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
        if is_overload_true(copy):
            bpk__anfwi.append(arr + '.copy()')
        elif is_overload_false(copy):
            bpk__anfwi.append(arr)
        else:
            bpk__anfwi.append(f'{arr}.copy() if copy else {arr}')
    header = """def impl(df, mapper=None, index=None, columns=None, axis=None, copy=True, inplace=False, level=None, errors='ignore', _bodo_transformed=False):
"""
    return _gen_init_df(header, dxhyd__krkcp, ', '.join(bpk__anfwi))


@overload_method(DataFrameType, 'filter', no_unliteral=True)
def overload_dataframe_filter(df, items=None, like=None, regex=None, axis=None
    ):
    mcls__idsxn = not is_overload_none(items)
    fou__wbjuz = not is_overload_none(like)
    wzlly__numwh = not is_overload_none(regex)
    vua__efm = mcls__idsxn ^ fou__wbjuz ^ wzlly__numwh
    if not vua__efm:
        raise BodoError(
            'DataFrame.filter(): keyword arguments `items`, `like`, and `regex` are mutually exclusive'
            )
    if is_overload_none(axis):
        axis = 'columns'
    if is_overload_constant_str(axis):
        axis = get_overload_const_str(axis)
        assert axis in {'index', 'columns'}
        ywhsi__jhnd = 0 if axis == 'index' else 1
    else:
        ywhsi__jhnd = axis
    assert ywhsi__jhnd in {0, 1}
    aaw__xjp = 'def impl(df, items=None, like=None, regex=None, axis=None):\n'
    if ywhsi__jhnd == 0:
        raise BodoError(
            'DataFrame.filter(): filtering based on index is not supported.')
    if ywhsi__jhnd == 1:
        yti__gypk = []
        yhm__emzdm = []
        jklmy__zord = []
        if mcls__idsxn:
            if is_overload_constant_list(items):
                crf__tqah = get_overload_const_list(items)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'items' must be a list of constant strings."
                    )
        if fou__wbjuz:
            if is_overload_constant_str(like):
                dhc__wuq = get_overload_const_str(like)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'like' must be a constant string."
                    )
        if wzlly__numwh:
            if is_overload_constant_str(regex):
                shq__kxg = get_overload_const_str(regex)
                gcd__kgk = re.compile(shq__kxg)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'regex' must be a constant string."
                    )
        for i, ebc__koy in enumerate(df.columns):
            if not is_overload_none(items
                ) and ebc__koy in crf__tqah or not is_overload_none(like
                ) and dhc__wuq in str(ebc__koy) or not is_overload_none(regex
                ) and gcd__kgk.search(str(ebc__koy)):
                yhm__emzdm.append(ebc__koy)
                jklmy__zord.append(i)
        for i in jklmy__zord:
            apm__usv = f'data_{i}'
            yti__gypk.append(apm__usv)
            aaw__xjp += f"""  {apm__usv} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})
"""
        data_args = ', '.join(yti__gypk)
        return _gen_init_df(aaw__xjp, yhm__emzdm, data_args)


@overload_method(DataFrameType, 'isna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'isnull', inline='always', no_unliteral=True)
def overload_dataframe_isna(df):
    data_args = ', '.join(
        f'bodo.libs.array_ops.array_op_isna(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
         for i in range(len(df.columns)))
    header = 'def impl(df):\n'
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'select_dtypes', inline='always',
    no_unliteral=True)
def overload_dataframe_select_dtypes(df, include=None, exclude=None):
    yhdj__dezc = is_overload_none(include)
    uqj__eea = is_overload_none(exclude)
    jii__cusx = 'DataFrame.select_dtypes'
    if yhdj__dezc and uqj__eea:
        raise_bodo_error(
            'DataFrame.select_dtypes() At least one of include or exclude must not be none'
            )

    def is_legal_input(elem):
        return is_overload_constant_str(elem) or isinstance(elem, types.
            DTypeSpec) or isinstance(elem, types.Function)
    if not yhdj__dezc:
        if is_overload_constant_list(include):
            include = get_overload_const_list(include)
            pgpt__hhl = [dtype_to_array_type(parse_dtype(elem, jii__cusx)) for
                elem in include]
        elif is_legal_input(include):
            pgpt__hhl = [dtype_to_array_type(parse_dtype(include, jii__cusx))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        pgpt__hhl = get_nullable_and_non_nullable_types(pgpt__hhl)
        jwbt__lhxhb = tuple(ebc__koy for i, ebc__koy in enumerate(df.
            columns) if df.data[i] in pgpt__hhl)
    else:
        jwbt__lhxhb = df.columns
    if not uqj__eea:
        if is_overload_constant_list(exclude):
            exclude = get_overload_const_list(exclude)
            oav__blyyc = [dtype_to_array_type(parse_dtype(elem, jii__cusx)) for
                elem in exclude]
        elif is_legal_input(exclude):
            oav__blyyc = [dtype_to_array_type(parse_dtype(exclude, jii__cusx))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        oav__blyyc = get_nullable_and_non_nullable_types(oav__blyyc)
        jwbt__lhxhb = tuple(ebc__koy for ebc__koy in jwbt__lhxhb if df.data
            [df.columns.index(ebc__koy)] not in oav__blyyc)
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(ebc__koy)})'
         for ebc__koy in jwbt__lhxhb)
    header = 'def impl(df, include=None, exclude=None):\n'
    return _gen_init_df(header, jwbt__lhxhb, data_args)


@overload_method(DataFrameType, 'notna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'notnull', inline='always', no_unliteral=True)
def overload_dataframe_notna(df):
    data_args = ', '.join(
        f'bodo.libs.array_ops.array_op_isna(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})) == False'
         for i in range(len(df.columns)))
    header = 'def impl(df):\n'
    return _gen_init_df(header, df.columns, data_args)


def overload_dataframe_head(df, n=5):
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[:n]' for
        i in range(len(df.columns)))
    header = 'def impl(df, n=5):\n'
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[:n]'
    return _gen_init_df(header, df.columns, data_args, index)


@lower_builtin('df.head', DataFrameType, types.Integer)
@lower_builtin('df.head', DataFrameType, types.Omitted)
def dataframe_head_lower(context, builder, sig, args):
    impl = overload_dataframe_head(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'tail', inline='always', no_unliteral=True)
def overload_dataframe_tail(df, n=5):
    if not is_overload_int(n):
        raise BodoError("Dataframe.tail(): 'n' must be an Integer")
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[m:]' for
        i in range(len(df.columns)))
    header = 'def impl(df, n=5):\n'
    header += '  m = bodo.hiframes.series_impl.tail_slice(len(df), n)\n'
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[m:]'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'to_string', no_unliteral=True)
def to_string_overload(df, buf=None, columns=None, col_space=None, header=
    True, index=True, na_rep='NaN', formatters=None, float_format=None,
    sparsify=None, index_names=True, justify=None, max_rows=None, min_rows=
    None, max_cols=None, show_dimensions=False, decimal='.', line_width=
    None, max_colwidth=None, encoding=None):

    def impl(df, buf=None, columns=None, col_space=None, header=True, index
        =True, na_rep='NaN', formatters=None, float_format=None, sparsify=
        None, index_names=True, justify=None, max_rows=None, min_rows=None,
        max_cols=None, show_dimensions=False, decimal='.', line_width=None,
        max_colwidth=None, encoding=None):
        with numba.objmode(res='string'):
            res = df.to_string(buf=buf, columns=columns, col_space=
                col_space, header=header, index=index, na_rep=na_rep,
                formatters=formatters, float_format=float_format, sparsify=
                sparsify, index_names=index_names, justify=justify,
                max_rows=max_rows, min_rows=min_rows, max_cols=max_cols,
                show_dimensions=show_dimensions, decimal=decimal,
                line_width=line_width, max_colwidth=max_colwidth, encoding=
                encoding)
        return res
    return impl


@overload_method(DataFrameType, 'isin', inline='always', no_unliteral=True)
def overload_dataframe_isin(df, values):
    aaw__xjp = 'def impl(df, values):\n'
    yso__lmb = {}
    ynh__beful = False
    if isinstance(values, DataFrameType):
        ynh__beful = True
        for i, ebc__koy in enumerate(df.columns):
            if ebc__koy in values.columns:
                jwy__yowv = 'val{}'.format(i)
                aaw__xjp += (
                    """  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(values, {})
"""
                    .format(jwy__yowv, values.columns.index(ebc__koy)))
                yso__lmb[ebc__koy] = jwy__yowv
    else:
        yso__lmb = {ebc__koy: 'values' for ebc__koy in df.columns}
    data = []
    for i in range(len(df.columns)):
        jwy__yowv = 'data{}'.format(i)
        aaw__xjp += (
            '  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})\n'
            .format(jwy__yowv, i))
        data.append(jwy__yowv)
    chzch__aaya = ['out{}'.format(i) for i in range(len(df.columns))]
    hazgy__demne = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  m = len({1})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] == {1}[i] if i < m else False
"""
    twv__xqxv = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] in {1}
"""
    mrccn__ctoc = '  {} = np.zeros(len(df), np.bool_)\n'
    for i, (cname, jcp__zesqm) in enumerate(zip(df.columns, data)):
        if cname in yso__lmb:
            unvnl__kdtig = yso__lmb[cname]
            if ynh__beful:
                aaw__xjp += hazgy__demne.format(jcp__zesqm, unvnl__kdtig,
                    chzch__aaya[i])
            else:
                aaw__xjp += twv__xqxv.format(jcp__zesqm, unvnl__kdtig,
                    chzch__aaya[i])
        else:
            aaw__xjp += mrccn__ctoc.format(chzch__aaya[i])
    return _gen_init_df(aaw__xjp, df.columns, ','.join(chzch__aaya))


@overload_method(DataFrameType, 'abs', inline='always', no_unliteral=True)
def overload_dataframe_abs(df):
    istxx__jnt = len(df.columns)
    data_args = ', '.join(
        'np.abs(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
        .format(i) for i in range(istxx__jnt))
    header = 'def impl(df):\n'
    return _gen_init_df(header, df.columns, data_args)


def overload_dataframe_corr(df, method='pearson', min_periods=1):
    lczyn__ujg = [ebc__koy for ebc__koy, blxy__gpt in zip(df.columns, df.
        data) if bodo.utils.typing._is_pandas_numeric_dtype(blxy__gpt.dtype)]
    assert len(lczyn__ujg) != 0
    mco__qsu = ''
    if not any(blxy__gpt == types.float64 for blxy__gpt in df.data):
        mco__qsu = '.astype(np.float64)'
    rihia__zqfj = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.columns.index(ebc__koy), '.astype(np.float64)' if 
        isinstance(df.data[df.columns.index(ebc__koy)], IntegerArrayType) or
        df.data[df.columns.index(ebc__koy)] == boolean_array else '') for
        ebc__koy in lczyn__ujg)
    ujp__njss = 'np.stack(({},), 1){}'.format(rihia__zqfj, mco__qsu)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(lczyn__ujg))
        )
    index = f'{generate_col_to_index_func_text(lczyn__ujg)}\n'
    header = "def impl(df, method='pearson', min_periods=1):\n"
    header += '  mat = {}\n'.format(ujp__njss)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 0, min_periods)\n'
    return _gen_init_df(header, lczyn__ujg, data_args, index)


@lower_builtin('df.corr', DataFrameType, types.VarArg(types.Any))
def dataframe_corr_lower(context, builder, sig, args):
    impl = overload_dataframe_corr(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'cov', inline='always', no_unliteral=True)
def overload_dataframe_cov(df, min_periods=None, ddof=1):
    qhdms__tpnw = dict(ddof=ddof)
    aijik__yom = dict(ddof=1)
    check_unsupported_args('DataFrame.cov', qhdms__tpnw, aijik__yom)
    gaunf__qzu = '1' if is_overload_none(min_periods) else 'min_periods'
    lczyn__ujg = [ebc__koy for ebc__koy, blxy__gpt in zip(df.columns, df.
        data) if bodo.utils.typing._is_pandas_numeric_dtype(blxy__gpt.dtype)]
    assert len(lczyn__ujg) != 0
    mco__qsu = ''
    if not any(blxy__gpt == types.float64 for blxy__gpt in df.data):
        mco__qsu = '.astype(np.float64)'
    rihia__zqfj = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.columns.index(ebc__koy), '.astype(np.float64)' if 
        isinstance(df.data[df.columns.index(ebc__koy)], IntegerArrayType) or
        df.data[df.columns.index(ebc__koy)] == boolean_array else '') for
        ebc__koy in lczyn__ujg)
    ujp__njss = 'np.stack(({},), 1){}'.format(rihia__zqfj, mco__qsu)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(lczyn__ujg))
        )
    index = f'pd.Index({lczyn__ujg})\n'
    header = 'def impl(df, min_periods=None, ddof=1):\n'
    header += '  mat = {}\n'.format(ujp__njss)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 1, {})\n'.format(
        gaunf__qzu)
    return _gen_init_df(header, lczyn__ujg, data_args, index)


@overload_method(DataFrameType, 'count', inline='always', no_unliteral=True)
def overload_dataframe_count(df, axis=0, level=None, numeric_only=False):
    data_args = ', '.join(
        f'bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
         for i in range(len(df.columns)))
    aaw__xjp = 'def impl(df, axis=0, level=None, numeric_only=False):\n'
    aaw__xjp += '  data = np.array([{}])\n'.format(data_args)
    ely__qbuy = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(df
        .columns)
    aaw__xjp += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {ely__qbuy})\n'
        )
    wyudp__cpm = {}
    exec(aaw__xjp, {'bodo': bodo, 'np': np}, wyudp__cpm)
    impl = wyudp__cpm['impl']
    return impl


@overload_method(DataFrameType, 'nunique', inline='always', no_unliteral=True)
def overload_dataframe_nunique(df, axis=0, dropna=True):
    qhdms__tpnw = dict(axis=axis)
    aijik__yom = dict(axis=0)
    if not is_overload_bool(dropna):
        raise BodoError('DataFrame.nunique: dropna must be a boolean value')
    check_unsupported_args('DataFrame.nunique', qhdms__tpnw, aijik__yom)
    data_args = ', '.join(
        f'bodo.libs.array_kernels.nunique(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dropna)'
         for i in range(len(df.columns)))
    aaw__xjp = 'def impl(df, axis=0, dropna=True):\n'
    aaw__xjp += '  data = np.asarray(({},))\n'.format(data_args)
    ely__qbuy = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(df
        .columns)
    aaw__xjp += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {ely__qbuy})\n'
        )
    wyudp__cpm = {}
    exec(aaw__xjp, {'bodo': bodo, 'np': np}, wyudp__cpm)
    impl = wyudp__cpm['impl']
    return impl


@overload_method(DataFrameType, 'prod', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'product', inline='always', no_unliteral=True)
def overload_dataframe_prod(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    qhdms__tpnw = dict(skipna=skipna, level=level, numeric_only=
        numeric_only, min_count=min_count)
    aijik__yom = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.prod/product', qhdms__tpnw, aijik__yom)
    return _gen_reduce_impl(df, 'prod', axis=axis)


@overload_method(DataFrameType, 'sum', inline='always', no_unliteral=True)
def overload_dataframe_sum(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    qhdms__tpnw = dict(skipna=skipna, level=level, numeric_only=
        numeric_only, min_count=min_count)
    aijik__yom = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.sum', qhdms__tpnw, aijik__yom)
    return _gen_reduce_impl(df, 'sum', axis=axis)


@overload_method(DataFrameType, 'max', inline='always', no_unliteral=True)
def overload_dataframe_max(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    qhdms__tpnw = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    aijik__yom = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.max', qhdms__tpnw, aijik__yom)
    return _gen_reduce_impl(df, 'max', axis=axis)


@overload_method(DataFrameType, 'min', inline='always', no_unliteral=True)
def overload_dataframe_min(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    qhdms__tpnw = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    aijik__yom = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.min', qhdms__tpnw, aijik__yom)
    return _gen_reduce_impl(df, 'min', axis=axis)


@overload_method(DataFrameType, 'mean', inline='always', no_unliteral=True)
def overload_dataframe_mean(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    qhdms__tpnw = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    aijik__yom = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.mean', qhdms__tpnw, aijik__yom)
    return _gen_reduce_impl(df, 'mean', axis=axis)


@overload_method(DataFrameType, 'var', inline='always', no_unliteral=True)
def overload_dataframe_var(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    qhdms__tpnw = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    aijik__yom = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.mean', qhdms__tpnw, aijik__yom)
    return _gen_reduce_impl(df, 'var', axis=axis)


@overload_method(DataFrameType, 'std', inline='always', no_unliteral=True)
def overload_dataframe_std(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    qhdms__tpnw = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    aijik__yom = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.std', qhdms__tpnw, aijik__yom)
    return _gen_reduce_impl(df, 'std', axis=axis)


@overload_method(DataFrameType, 'median', inline='always', no_unliteral=True)
def overload_dataframe_median(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    qhdms__tpnw = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    aijik__yom = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.median', qhdms__tpnw, aijik__yom)
    return _gen_reduce_impl(df, 'median', axis=axis)


@overload_method(DataFrameType, 'quantile', inline='always', no_unliteral=True)
def overload_dataframe_quantile(df, q=0.5, axis=0, numeric_only=True,
    interpolation='linear'):
    qhdms__tpnw = dict(numeric_only=numeric_only, interpolation=interpolation)
    aijik__yom = dict(numeric_only=True, interpolation='linear')
    check_unsupported_args('DataFrame.quantile', qhdms__tpnw, aijik__yom)
    return _gen_reduce_impl(df, 'quantile', 'q', axis=axis)


@overload_method(DataFrameType, 'idxmax', inline='always', no_unliteral=True)
def overload_dataframe_idxmax(df, axis=0, skipna=True):
    qhdms__tpnw = dict(axis=axis, skipna=skipna)
    aijik__yom = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmax', qhdms__tpnw, aijik__yom)
    for puzfv__myhr in df.data:
        if not (bodo.utils.utils.is_np_array_typ(puzfv__myhr) and (
            puzfv__myhr.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(puzfv__myhr.dtype, (types.Number, types.Boolean))) or
            isinstance(puzfv__myhr, (bodo.IntegerArrayType, bodo.
            CategoricalArrayType)) or puzfv__myhr in [bodo.boolean_array,
            bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmax() only supported for numeric column types. Column type: {puzfv__myhr} not supported.'
                )
        if isinstance(puzfv__myhr, bodo.CategoricalArrayType
            ) and not puzfv__myhr.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmax(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmax', axis=axis)


@overload_method(DataFrameType, 'idxmin', inline='always', no_unliteral=True)
def overload_dataframe_idxmin(df, axis=0, skipna=True):
    qhdms__tpnw = dict(axis=axis, skipna=skipna)
    aijik__yom = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmin', qhdms__tpnw, aijik__yom)
    for puzfv__myhr in df.data:
        if not (bodo.utils.utils.is_np_array_typ(puzfv__myhr) and (
            puzfv__myhr.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(puzfv__myhr.dtype, (types.Number, types.Boolean))) or
            isinstance(puzfv__myhr, (bodo.IntegerArrayType, bodo.
            CategoricalArrayType)) or puzfv__myhr in [bodo.boolean_array,
            bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmin() only supported for numeric column types. Column type: {puzfv__myhr} not supported.'
                )
        if isinstance(puzfv__myhr, bodo.CategoricalArrayType
            ) and not puzfv__myhr.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmin(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmin', axis=axis)


def _gen_reduce_impl(df, func_name, args=None, axis=None):
    args = '' if is_overload_none(args) else args
    if is_overload_none(axis):
        axis = 0
    else:
        axis = get_overload_const_int(axis)
    assert axis in (0, 1), 'invalid axis argument for DataFrame.{}'.format(
        func_name)
    if func_name in ('idxmax', 'idxmin'):
        out_colnames = df.columns
    else:
        lczyn__ujg = tuple(ebc__koy for ebc__koy, blxy__gpt in zip(df.
            columns, df.data) if bodo.utils.typing._is_pandas_numeric_dtype
            (blxy__gpt.dtype))
        out_colnames = lczyn__ujg
    assert len(out_colnames) != 0
    try:
        if func_name in ('idxmax', 'idxmin') and axis == 0:
            comm_dtype = None
        else:
            djzx__fao = [numba.np.numpy_support.as_dtype(df.data[df.columns
                .index(ebc__koy)].dtype) for ebc__koy in out_colnames]
            comm_dtype = numba.np.numpy_support.from_dtype(np.
                find_common_type(djzx__fao, []))
    except NotImplementedError as lcj__zzalk:
        raise BodoError(
            f'Dataframe.{func_name}() with column types: {df.data} could not be merged to a common type.'
            )
    xxu__dags = ''
    if func_name in ('sum', 'prod'):
        xxu__dags = ', min_count=0'
    ddof = ''
    if func_name in ('var', 'std'):
        ddof = 'ddof=1, '
    aaw__xjp = (
        'def impl(df, axis=None, skipna=None, level=None,{} numeric_only=None{}):\n'
        .format(ddof, xxu__dags))
    if func_name == 'quantile':
        aaw__xjp = (
            "def impl(df, q=0.5, axis=0, numeric_only=True, interpolation='linear'):\n"
            )
    if func_name in ('idxmax', 'idxmin'):
        aaw__xjp = 'def impl(df, axis=0, skipna=True):\n'
    if axis == 0:
        aaw__xjp += _gen_reduce_impl_axis0(df, func_name, out_colnames,
            comm_dtype, args)
    else:
        aaw__xjp += _gen_reduce_impl_axis1(func_name, out_colnames,
            comm_dtype, df)
    wyudp__cpm = {}
    exec(aaw__xjp, {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba},
        wyudp__cpm)
    impl = wyudp__cpm['impl']
    return impl


def _gen_reduce_impl_axis0(df, func_name, out_colnames, comm_dtype, args):
    qlq__rps = ''
    if func_name in ('min', 'max'):
        qlq__rps = ', dtype=np.{}'.format(comm_dtype)
    if comm_dtype == types.float32 and func_name in ('sum', 'prod', 'mean',
        'var', 'std', 'median'):
        qlq__rps = ', dtype=np.float32'
    snw__qmfd = f'bodo.libs.array_ops.array_op_{func_name}'
    dva__ozod = ''
    if func_name in ['sum', 'prod']:
        dva__ozod = 'True, min_count'
    elif func_name in ['idxmax', 'idxmin']:
        dva__ozod = 'index'
    elif func_name == 'quantile':
        dva__ozod = 'q'
    elif func_name in ['std', 'var']:
        dva__ozod = 'True, ddof'
    elif func_name == 'median':
        dva__ozod = 'True'
    data_args = ', '.join(
        f'{snw__qmfd}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(ebc__koy)}), {dva__ozod})'
         for ebc__koy in out_colnames)
    aaw__xjp = ''
    if func_name in ('idxmax', 'idxmin'):
        aaw__xjp += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        aaw__xjp += ('  data = bodo.utils.conversion.coerce_to_array(({},))\n'
            .format(data_args))
    else:
        aaw__xjp += '  data = np.asarray(({},){})\n'.format(data_args, qlq__rps
            )
    aaw__xjp += f"""  return bodo.hiframes.pd_series_ext.init_series(data, pd.Index({out_colnames}))
"""
    return aaw__xjp


def _gen_reduce_impl_axis1(func_name, out_colnames, comm_dtype, df_type):
    ybmky__xcime = [df_type.columns.index(ebc__koy) for ebc__koy in
        out_colnames]
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    data_args = '\n    '.join(
        'arr_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
        .format(i) for i in ybmky__xcime)
    qkbnh__lblpf = '\n        '.join(f'row[{i}] = arr_{ybmky__xcime[i]}[i]' for
        i in range(len(out_colnames)))
    assert len(data_args) > 0, f'empty dataframe in DataFrame.{func_name}()'
    mkl__fkoup = f'len(arr_{ybmky__xcime[0]})'
    nxs__vgwtu = {'max': 'np.nanmax', 'min': 'np.nanmin', 'sum':
        'np.nansum', 'prod': 'np.nanprod', 'mean': 'np.nanmean', 'median':
        'np.nanmedian', 'var': 'bodo.utils.utils.nanvar_ddof1', 'std':
        'bodo.utils.utils.nanstd_ddof1'}
    if func_name in nxs__vgwtu:
        mmom__yeg = nxs__vgwtu[func_name]
        ocz__zjbe = 'float64' if func_name in ['mean', 'median', 'std', 'var'
            ] else comm_dtype
        aaw__xjp = f"""
    {data_args}
    numba.parfors.parfor.init_prange()
    n = {mkl__fkoup}
    row = np.empty({len(out_colnames)}, np.{comm_dtype})
    A = np.empty(n, np.{ocz__zjbe})
    for i in numba.parfors.parfor.internal_prange(n):
        {qkbnh__lblpf}
        A[i] = {mmom__yeg}(row)
    return bodo.hiframes.pd_series_ext.init_series(A, {index})
"""
        return aaw__xjp
    else:
        raise BodoError(f'DataFrame.{func_name}(): Not supported for axis=1')


@overload_method(DataFrameType, 'pct_change', inline='always', no_unliteral
    =True)
def overload_dataframe_pct_change(df, periods=1, fill_method='pad', limit=
    None, freq=None):
    qhdms__tpnw = dict(fill_method=fill_method, limit=limit, freq=freq)
    aijik__yom = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('DataFrame.pct_change', qhdms__tpnw, aijik__yom)
    data_args = ', '.join(
        f'bodo.hiframes.rolling.pct_change(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), periods, False)'
         for i in range(len(df.columns)))
    header = (
        "def impl(df, periods=1, fill_method='pad', limit=None, freq=None):\n")
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'cumprod', inline='always', no_unliteral=True)
def overload_dataframe_cumprod(df, axis=None, skipna=True):
    qhdms__tpnw = dict(skipna=skipna)
    aijik__yom = dict(skipna=True)
    check_unsupported_args('DataFrame.cumprod', qhdms__tpnw, aijik__yom)
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).cumprod()'
         for i in range(len(df.columns)))
    header = 'def impl(df, axis=None, skipna=True):\n'
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'cumsum', inline='always', no_unliteral=True)
def overload_dataframe_cumsum(df, axis=None, skipna=True):
    qhdms__tpnw = dict(skipna=skipna)
    aijik__yom = dict(skipna=True)
    check_unsupported_args('DataFrame.cumsum', qhdms__tpnw, aijik__yom)
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).cumsum()'
         for i in range(len(df.columns)))
    header = 'def impl(df, axis=None, skipna=True):\n'
    return _gen_init_df(header, df.columns, data_args)


def _is_describe_type(data):
    return isinstance(data, IntegerArrayType) or isinstance(data, types.Array
        ) and isinstance(data.dtype, types.Number
        ) or data.dtype == bodo.datetime64ns


@overload_method(DataFrameType, 'describe', inline='always', no_unliteral=True)
def overload_dataframe_describe(df, percentiles=None, include=None, exclude
    =None, datetime_is_numeric=True):
    qhdms__tpnw = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    aijik__yom = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('DataFrame.describe', qhdms__tpnw, aijik__yom)
    lczyn__ujg = [ebc__koy for ebc__koy, blxy__gpt in zip(df.columns, df.
        data) if _is_describe_type(blxy__gpt)]
    if len(lczyn__ujg) == 0:
        raise BodoError('df.describe() only supports numeric columns')
    dxx__nfc = sum(df.data[df.columns.index(ebc__koy)].dtype == bodo.
        datetime64ns for ebc__koy in lczyn__ujg)

    def _get_describe(col_ind):
        fjlx__vajuo = df.data[col_ind].dtype == bodo.datetime64ns
        if dxx__nfc and dxx__nfc != len(lczyn__ujg):
            if fjlx__vajuo:
                return f'des_{col_ind} + (np.nan,)'
            return (
                f'des_{col_ind}[:2] + des_{col_ind}[3:] + (des_{col_ind}[2],)')
        return f'des_{col_ind}'
    header = """def impl(df, percentiles=None, include=None, exclude=None, datetime_is_numeric=True):
"""
    for ebc__koy in lczyn__ujg:
        col_ind = df.columns.index(ebc__koy)
        header += f"""  des_{col_ind} = bodo.libs.array_ops.array_op_describe(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {col_ind}))
"""
    data_args = ', '.join(_get_describe(df.columns.index(ebc__koy)) for
        ebc__koy in lczyn__ujg)
    kst__sdyy = "['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']"
    if dxx__nfc == len(lczyn__ujg):
        kst__sdyy = "['count', 'mean', 'min', '25%', '50%', '75%', 'max']"
    elif dxx__nfc:
        kst__sdyy = (
            "['count', 'mean', 'min', '25%', '50%', '75%', 'max', 'std']")
    index = f'bodo.utils.conversion.convert_to_index({kst__sdyy})'
    return _gen_init_df(header, lczyn__ujg, data_args, index)


@overload_method(DataFrameType, 'take', inline='always', no_unliteral=True)
def overload_dataframe_take(df, indices, axis=0, convert=None, is_copy=True):
    qhdms__tpnw = dict(axis=axis, convert=convert, is_copy=is_copy)
    aijik__yom = dict(axis=0, convert=None, is_copy=True)
    check_unsupported_args('DataFrame.take', qhdms__tpnw, aijik__yom)
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})[indices_t]'
        .format(i) for i in range(len(df.columns)))
    header = 'def impl(df, indices, axis=0, convert=None, is_copy=True):\n'
    header += (
        '  indices_t = bodo.utils.conversion.coerce_to_ndarray(indices)\n')
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[indices_t]'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'shift', inline='always', no_unliteral=True)
def overload_dataframe_shift(df, periods=1, freq=None, axis=0, fill_value=None
    ):
    qhdms__tpnw = dict(freq=freq, axis=axis, fill_value=fill_value)
    aijik__yom = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('DataFrame.shift', qhdms__tpnw, aijik__yom)
    for zcw__vjflb in df.data:
        if not is_supported_shift_array_type(zcw__vjflb):
            raise BodoError(
                f'Dataframe.shift() column input type {zcw__vjflb.dtype} not supported yet.'
                )
    if not is_overload_int(periods):
        raise BodoError(
            "DataFrame.shift(): 'periods' input must be an integer.")
    data_args = ', '.join(
        f'bodo.hiframes.rolling.shift(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), periods, False)'
         for i in range(len(df.columns)))
    header = 'def impl(df, periods=1, freq=None, axis=0, fill_value=None):\n'
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'diff', inline='always', no_unliteral=True)
def overload_dataframe_diff(df, periods=1, axis=0):
    qhdms__tpnw = dict(axis=axis)
    aijik__yom = dict(axis=0)
    check_unsupported_args('DataFrame.diff', qhdms__tpnw, aijik__yom)
    for zcw__vjflb in df.data:
        if not (isinstance(zcw__vjflb, types.Array) and (isinstance(
            zcw__vjflb.dtype, types.Number) or zcw__vjflb.dtype == bodo.
            datetime64ns)):
            raise BodoError(
                f'DataFrame.diff() column input type {zcw__vjflb.dtype} not supported.'
                )
    if not is_overload_int(periods):
        raise BodoError("DataFrame.diff(): 'periods' input must be an integer."
            )
    header = 'def impl(df, periods=1, axis= 0):\n'
    for i in range(len(df.columns)):
        header += (
            f'  data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})\n'
            )
    data_args = ', '.join(
        f'bodo.hiframes.series_impl.dt64_arr_sub(data_{i}, bodo.hiframes.rolling.shift(data_{i}, periods, False))'
         if df.data[i] == types.Array(bodo.datetime64ns, 1, 'C') else
        f'data_{i} - bodo.hiframes.rolling.shift(data_{i}, periods, False)' for
        i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'set_index', inline='always', no_unliteral=True
    )
def overload_dataframe_set_index(df, keys, drop=True, append=False, inplace
    =False, verify_integrity=False):
    mwezv__himy = {'inplace': inplace, 'append': append, 'verify_integrity':
        verify_integrity}
    bnhi__bodsb = {'inplace': False, 'append': False, 'verify_integrity': False
        }
    check_unsupported_args('DataFrame.set_index', mwezv__himy, bnhi__bodsb)
    if not is_overload_constant_str(keys):
        raise_bodo_error(
            "DataFrame.set_index(): 'keys' must be a constant string")
    col_name = get_overload_const_str(keys)
    col_ind = df.columns.index(col_name)
    if len(df.columns) == 1:
        raise BodoError(
            'DataFrame.set_index(): Not supported on single column DataFrames.'
            )
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'.format(
        i) for i in range(len(df.columns)) if i != col_ind)
    header = """def impl(df, keys, drop=True, append=False, inplace=False, verify_integrity=False):
"""
    columns = tuple(ebc__koy for ebc__koy in df.columns if ebc__koy != col_name
        )
    index = (
        'bodo.utils.conversion.index_from_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}), {})'
        .format(col_ind, f"'{col_name}'" if isinstance(col_name, str) else
        col_name))
    return _gen_init_df(header, columns, data_args, index)


@overload_method(DataFrameType, 'query', no_unliteral=True)
def overload_dataframe_query(df, expr, inplace=False):
    mwezv__himy = {'inplace': inplace}
    bnhi__bodsb = {'inplace': False}
    check_unsupported_args('query', mwezv__himy, bnhi__bodsb)
    if not isinstance(expr, (types.StringLiteral, types.UnicodeType)):
        raise BodoError('query(): expr argument should be a string')

    def impl(df, expr, inplace=False):
        onj__qsd = bodo.hiframes.pd_dataframe_ext.query_dummy(df, expr)
        return df[onj__qsd]
    return impl


@overload_method(DataFrameType, 'duplicated', inline='always', no_unliteral
    =True)
def overload_dataframe_duplicated(df, subset=None, keep='first'):
    mwezv__himy = {'subset': subset, 'keep': keep}
    bnhi__bodsb = {'subset': None, 'keep': 'first'}
    check_unsupported_args('DataFrame.duplicated', mwezv__himy, bnhi__bodsb)
    istxx__jnt = len(df.columns)
    aaw__xjp = "def impl(df, subset=None, keep='first'):\n"
    for i in range(istxx__jnt):
        aaw__xjp += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    aaw__xjp += (
        '  duplicated, index_arr = bodo.libs.array_kernels.duplicated(({},), {})\n'
        .format(', '.join('data_{}'.format(i) for i in range(istxx__jnt)),
        index))
    aaw__xjp += '  index = bodo.utils.conversion.index_from_array(index_arr)\n'
    aaw__xjp += (
        '  return bodo.hiframes.pd_series_ext.init_series(duplicated, index)\n'
        )
    wyudp__cpm = {}
    exec(aaw__xjp, {'bodo': bodo}, wyudp__cpm)
    impl = wyudp__cpm['impl']
    return impl


@overload_method(DataFrameType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_dataframe_drop_duplicates(df, subset=None, keep='first',
    inplace=False, ignore_index=False):
    mwezv__himy = {'keep': keep, 'inplace': inplace, 'subset': subset,
        'ignore_index': ignore_index}
    bnhi__bodsb = {'keep': 'first', 'inplace': False, 'subset': None,
        'ignore_index': False}
    check_unsupported_args('DataFrame.drop_duplicates', mwezv__himy,
        bnhi__bodsb)
    istxx__jnt = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(istxx__jnt))
    aaw__xjp = (
        "def impl(df, subset=None, keep='first', inplace=False, ignore_index=False):\n"
        )
    for i in range(istxx__jnt):
        aaw__xjp += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    aaw__xjp += (
        '  ({0},), index_arr = bodo.libs.array_kernels.drop_duplicates(({0},), {1})\n'
        .format(data_args, index))
    aaw__xjp += '  index = bodo.utils.conversion.index_from_array(index_arr)\n'
    return _gen_init_df(aaw__xjp, df.columns, data_args, 'index')


def _gen_init_df(header, columns, data_args, index=None, extra_globals=None):
    if index is None:
        index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    if extra_globals is None:
        extra_globals = {}
    ebpx__xqqk = gen_const_tup(columns)
    data_args = '({}{})'.format(data_args, ',' if len(columns) == 1 else '')
    aaw__xjp = (
        '{}  return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, {}, {})\n'
        .format(header, data_args, index, ebpx__xqqk))
    wyudp__cpm = {}
    blf__albsx = {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba}
    blf__albsx.update(extra_globals)
    exec(aaw__xjp, blf__albsx, wyudp__cpm)
    impl = wyudp__cpm['impl']
    return impl


def _get_binop_columns(lhs, rhs, is_inplace=False):
    if lhs.columns != rhs.columns:
        skjxd__tjz = pd.Index(lhs.columns)
        gix__lophg = pd.Index(rhs.columns)
        hgkv__ufm, hmin__ixao, jqtlm__ytlji = skjxd__tjz.join(gix__lophg,
            how='left' if is_inplace else 'outer', level=None,
            return_indexers=True)
        return tuple(hgkv__ufm), hmin__ixao, jqtlm__ytlji
    return lhs.columns, range(len(lhs.columns)), range(len(lhs.columns))


def create_binary_op_overload(op):

    def overload_dataframe_binary_op(lhs, rhs):
        fjnfx__rrtzf = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        opkp__sss = operator.eq, operator.ne
        if isinstance(lhs, DataFrameType):
            if isinstance(rhs, DataFrameType):
                hgkv__ufm, hmin__ixao, jqtlm__ytlji = _get_binop_columns(lhs,
                    rhs)
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {bkt__zmth}) {fjnfx__rrtzf}bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {dobfb__kawk})'
                     if bkt__zmth != -1 and dobfb__kawk != -1 else
                    f'bodo.libs.array_kernels.gen_na_array(len(lhs), float64_arr_type)'
                     for bkt__zmth, dobfb__kawk in zip(hmin__ixao,
                    jqtlm__ytlji))
                header = 'def impl(lhs, rhs):\n'
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)')
                return _gen_init_df(header, hgkv__ufm, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            xgry__zgk = []
            mmti__uzgka = []
            if op in opkp__sss:
                for i, cbk__gbsdv in enumerate(lhs.data):
                    if is_common_scalar_dtype([cbk__gbsdv.dtype, rhs]):
                        xgry__zgk.append(
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {fjnfx__rrtzf} rhs'
                            )
                    else:
                        nwrj__pbkno = f'arr{i}'
                        mmti__uzgka.append(nwrj__pbkno)
                        xgry__zgk.append(nwrj__pbkno)
                data_args = ', '.join(xgry__zgk)
            else:
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {fjnfx__rrtzf} rhs'
                     for i in range(len(lhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(mmti__uzgka) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(lhs)\n'
                header += ''.join(
                    f'  {nwrj__pbkno} = np.empty(n, dtype=np.bool_)\n' for
                    nwrj__pbkno in mmti__uzgka)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(nwrj__pbkno, 
                    op == operator.ne) for nwrj__pbkno in mmti__uzgka)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)'
            return _gen_init_df(header, lhs.columns, data_args, index)
        if isinstance(rhs, DataFrameType):
            xgry__zgk = []
            mmti__uzgka = []
            if op in opkp__sss:
                for i, cbk__gbsdv in enumerate(rhs.data):
                    if is_common_scalar_dtype([lhs, cbk__gbsdv.dtype]):
                        xgry__zgk.append(
                            f'lhs {fjnfx__rrtzf} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {i})'
                            )
                    else:
                        nwrj__pbkno = f'arr{i}'
                        mmti__uzgka.append(nwrj__pbkno)
                        xgry__zgk.append(nwrj__pbkno)
                data_args = ', '.join(xgry__zgk)
            else:
                data_args = ', '.join(
                    'lhs {1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {0})'
                    .format(i, fjnfx__rrtzf) for i in range(len(rhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(mmti__uzgka) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(rhs)\n'
                header += ''.join('  {0} = np.empty(n, dtype=np.bool_)\n'.
                    format(nwrj__pbkno) for nwrj__pbkno in mmti__uzgka)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(nwrj__pbkno, 
                    op == operator.ne) for nwrj__pbkno in mmti__uzgka)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(rhs)'
            return _gen_init_df(header, rhs.columns, data_args, index)
    return overload_dataframe_binary_op


skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        zwci__yye = create_binary_op_overload(op)
        overload(op)(zwci__yye)


_install_binary_ops()


def create_inplace_binary_op_overload(op):

    def overload_dataframe_inplace_binary_op(left, right):
        if isinstance(left, DataFrameType):
            fjnfx__rrtzf = numba.core.utils.OPERATORS_TO_BUILTINS[op]
            if isinstance(right, DataFrameType):
                hgkv__ufm, tin__dhao, jqtlm__ytlji = _get_binop_columns(left,
                    right, True)
                aaw__xjp = 'def impl(left, right):\n'
                for i, dobfb__kawk in enumerate(jqtlm__ytlji):
                    if dobfb__kawk == -1:
                        aaw__xjp += f"""  df_arr{i} = bodo.libs.array_kernels.gen_na_array(len(left), float64_arr_type)
"""
                        continue
                    aaw__xjp += f"""  df_arr{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {i})
"""
                    aaw__xjp += f"""  df_arr{i} {fjnfx__rrtzf} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(right, {dobfb__kawk})
"""
                data_args = ', '.join(f'df_arr{i}' for i in range(len(
                    hgkv__ufm)))
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)')
                return _gen_init_df(aaw__xjp, hgkv__ufm, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            aaw__xjp = 'def impl(left, right):\n'
            for i in range(len(left.columns)):
                aaw__xjp += (
                    """  df_arr{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {0})
"""
                    .format(i))
                aaw__xjp += '  df_arr{0} {1} right\n'.format(i, fjnfx__rrtzf)
            data_args = ', '.join('df_arr{}'.format(i) for i in range(len(
                left.columns)))
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)'
            return _gen_init_df(aaw__xjp, left.columns, data_args, index)
    return overload_dataframe_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        zwci__yye = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(zwci__yye)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_dataframe_unary_op(df):
        if isinstance(df, DataFrameType):
            fjnfx__rrtzf = numba.core.utils.OPERATORS_TO_BUILTINS[op]
            data_args = ', '.join(
                '{1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
                .format(i, fjnfx__rrtzf) for i in range(len(df.columns)))
            header = 'def impl(df):\n'
            return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        zwci__yye = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(zwci__yye)


_install_unary_ops()


def overload_isna(obj):
    if isinstance(obj, (DataFrameType, SeriesType)
        ) or bodo.hiframes.pd_index_ext.is_pd_index_type(obj):
        return lambda obj: obj.isna()
    if is_array_typ(obj):

        def impl(obj):
            numba.parfors.parfor.init_prange()
            n = len(obj)
            wtc__nlzy = np.empty(n, np.bool_)
            for i in numba.parfors.parfor.internal_prange(n):
                wtc__nlzy[i] = bodo.libs.array_kernels.isna(obj, i)
            return wtc__nlzy
        return impl


overload(pd.isna, inline='always')(overload_isna)
overload(pd.isnull, inline='always')(overload_isna)


@overload(pd.isna)
@overload(pd.isnull)
def overload_isna_scalar(obj):
    if isinstance(obj, (DataFrameType, SeriesType)
        ) or bodo.hiframes.pd_index_ext.is_pd_index_type(obj) or is_array_typ(
        obj):
        return
    if isinstance(obj, (types.List, types.UniTuple)):

        def impl(obj):
            n = len(obj)
            wtc__nlzy = np.empty(n, np.bool_)
            for i in range(n):
                wtc__nlzy[i] = pd.isna(obj[i])
            return wtc__nlzy
        return impl
    obj = types.unliteral(obj)
    if obj == bodo.string_type:
        return lambda obj: unliteral_val(False)
    if isinstance(obj, types.Integer):
        return lambda obj: unliteral_val(False)
    if isinstance(obj, types.Float):
        return lambda obj: np.isnan(obj)
    if isinstance(obj, (types.NPDatetime, types.NPTimedelta)):
        return lambda obj: np.isnat(obj)
    if obj == types.none:
        return lambda obj: unliteral_val(True)
    if obj == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        return lambda obj: np.isnat(bodo.hiframes.pd_timestamp_ext.
            integer_to_dt64(obj.value))
    if obj == bodo.hiframes.datetime_timedelta_ext.pd_timedelta_type:
        return lambda obj: np.isnat(bodo.hiframes.pd_timestamp_ext.
            integer_to_timedelta64(obj.value))
    if isinstance(obj, types.Optional):
        return lambda obj: obj is None
    return lambda obj: unliteral_val(False)


@overload(operator.setitem, no_unliteral=True)
def overload_setitem_arr_none(A, idx, val):
    if is_array_typ(A, False) and isinstance(idx, types.Integer
        ) and val == types.none:
        return lambda A, idx, val: bodo.libs.array_kernels.setna(A, idx)


def overload_notna(obj):
    if isinstance(obj, DataFrameType):
        return lambda obj: obj.notna()
    if isinstance(obj, (SeriesType, types.Array, types.List, types.UniTuple)
        ) or bodo.hiframes.pd_index_ext.is_pd_index_type(obj
        ) or obj == bodo.string_array_type:
        return lambda obj: ~pd.isna(obj)
    return lambda obj: not pd.isna(obj)


overload(pd.notna, inline='always', no_unliteral=True)(overload_notna)
overload(pd.notnull, inline='always', no_unliteral=True)(overload_notna)


def _get_pd_dtype_str(t):
    if t.dtype == types.NPDatetime('ns'):
        return "'datetime64[ns]'"
    return bodo.ir.csv_ext._get_pd_dtype_str(t)


@overload_method(DataFrameType, 'replace', inline='always', no_unliteral=True)
def overload_dataframe_replace(df, to_replace=None, value=None, inplace=
    False, limit=None, regex=False, method='pad'):
    if is_overload_none(to_replace):
        raise BodoError('replace(): to_replace value of None is not supported')
    mwezv__himy = {'inplace': inplace, 'limit': limit, 'regex': regex,
        'method': method}
    bnhi__bodsb = {'inplace': False, 'limit': None, 'regex': False,
        'method': 'pad'}
    check_unsupported_args('replace', mwezv__himy, bnhi__bodsb)
    data_args = ', '.join(
        f'df.iloc[:, {i}].replace(to_replace, value).values' for i in range
        (len(df.columns)))
    header = """def impl(df, to_replace=None, value=None, inplace=False, limit=None, regex=False, method='pad'):
"""
    return _gen_init_df(header, df.columns, data_args)


def _is_col_access(expr_node):
    leqdn__hoc = str(expr_node)
    return leqdn__hoc.startswith('left.') or leqdn__hoc.startswith('right.')


def _insert_NA_cond(expr_node, left_columns, left_data, right_columns,
    right_data):
    hbgn__xkj = {'left': 0, 'right': 0, 'NOT_NA': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (hbgn__xkj,))
    desd__dstw = pd.core.computation.parsing.clean_column_name

    def append_null_checks(expr_node, null_set):
        if not null_set:
            return expr_node
        ths__lph = ' & '.join([('NOT_NA.`' + ixvq__dtvhk + '`') for
            ixvq__dtvhk in null_set])
        jkf__frw = {('NOT_NA', desd__dstw(cbk__gbsdv)): cbk__gbsdv for
            cbk__gbsdv in null_set}
        sleyn__soy, tin__dhao, tin__dhao = _parse_query_expr(ths__lph, env,
            [], [], None, join_cleaned_cols=jkf__frw)
        nyr__kevjm = (pd.core.computation.ops.BinOp.
            _disallow_scalar_only_bool_ops)
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        try:
            bkb__uyo = pd.core.computation.ops.BinOp('&', sleyn__soy, expr_node
                )
        finally:
            (pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
                ) = nyr__kevjm
        return bkb__uyo

    def _insert_NA_cond_body(expr_node, null_set):
        if isinstance(expr_node, pd.core.computation.ops.BinOp):
            if expr_node.op == '|':
                vcg__jul = set()
                ivxu__echr = set()
                icb__dgjpp = _insert_NA_cond_body(expr_node.lhs, vcg__jul)
                vtl__rmoht = _insert_NA_cond_body(expr_node.rhs, ivxu__echr)
                qhi__lll = vcg__jul.intersection(ivxu__echr)
                vcg__jul.difference_update(qhi__lll)
                ivxu__echr.difference_update(qhi__lll)
                null_set.update(qhi__lll)
                expr_node.lhs = append_null_checks(icb__dgjpp, vcg__jul)
                expr_node.rhs = append_null_checks(vtl__rmoht, ivxu__echr)
                expr_node.operands = expr_node.lhs, expr_node.rhs
            else:
                expr_node.lhs = _insert_NA_cond_body(expr_node.lhs, null_set)
                expr_node.rhs = _insert_NA_cond_body(expr_node.rhs, null_set)
        elif _is_col_access(expr_node):
            szrxm__ufhr = expr_node.name
            vco__yduaa, col_name = szrxm__ufhr.split('.')
            if vco__yduaa == 'left':
                wurmt__kvziz = left_columns
                data = left_data
            else:
                wurmt__kvziz = right_columns
                data = right_data
            kqogr__ffzi = data[wurmt__kvziz.index(col_name)]
            if bodo.utils.typing.is_nullable(kqogr__ffzi):
                null_set.add(expr_node.name)
        return expr_node
    null_set = set()
    uuh__qprg = _insert_NA_cond_body(expr_node, null_set)
    return append_null_checks(expr_node, null_set)


def _extract_equal_conds(expr_node):
    if not hasattr(expr_node, 'op'):
        return [], [], expr_node
    if expr_node.op == '==' and _is_col_access(expr_node.lhs
        ) and _is_col_access(expr_node.rhs):
        lgzwk__pwgl = str(expr_node.lhs)
        urxb__lazx = str(expr_node.rhs)
        if lgzwk__pwgl.startswith('left.') and urxb__lazx.startswith('left.'
            ) or lgzwk__pwgl.startswith('right.') and urxb__lazx.startswith(
            'right.'):
            return [], [], expr_node
        left_on = [lgzwk__pwgl.split('.')[1]]
        right_on = [urxb__lazx.split('.')[1]]
        if lgzwk__pwgl.startswith('right.'):
            return right_on, left_on, None
        return left_on, right_on, None
    if expr_node.op == '&':
        hrft__pbu, fzwr__yfigi, mpz__bir = _extract_equal_conds(expr_node.lhs)
        ihju__ckvo, gtqo__kdgi, yuv__yuadq = _extract_equal_conds(expr_node.rhs
            )
        left_on = hrft__pbu + ihju__ckvo
        right_on = fzwr__yfigi + gtqo__kdgi
        if mpz__bir is None:
            return left_on, right_on, yuv__yuadq
        if yuv__yuadq is None:
            return left_on, right_on, mpz__bir
        expr_node.lhs = mpz__bir
        expr_node.rhs = yuv__yuadq
        expr_node.operands = expr_node.lhs, expr_node.rhs
        return left_on, right_on, expr_node
    return [], [], expr_node


def _parse_merge_cond(on_str, left_columns, left_data, right_columns,
    right_data):
    hbgn__xkj = {'left': 0, 'right': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (hbgn__xkj,))
    kjjy__ukmk = dict()
    desd__dstw = pd.core.computation.parsing.clean_column_name
    for name, llmep__svq in (('left', left_columns), ('right', right_columns)):
        for cbk__gbsdv in llmep__svq:
            leza__fhb = desd__dstw(cbk__gbsdv)
            wad__pahs = name, leza__fhb
            if wad__pahs in kjjy__ukmk:
                raise BodoException(
                    f"pd.merge(): {name} table contains two columns that are escaped to the same Python identifier '{cbk__gbsdv}' and '{kjjy__ukmk[leza__fhb]}' Please rename one of these columns. To avoid this issue, please use names that are valid Python identifiers."
                    )
            kjjy__ukmk[wad__pahs] = cbk__gbsdv
    nuk__gtbe, tin__dhao, tin__dhao = _parse_query_expr(on_str, env, [], [],
        None, join_cleaned_cols=kjjy__ukmk)
    left_on, right_on, ybdmn__yxl = _extract_equal_conds(nuk__gtbe.terms)
    return left_on, right_on, _insert_NA_cond(ybdmn__yxl, left_columns,
        left_data, right_columns, right_data)


@overload_method(DataFrameType, 'merge', inline='always', no_unliteral=True)
@overload(pd.merge, inline='always', no_unliteral=True)
def overload_dataframe_merge(left, right, how='inner', on=None, left_on=
    None, right_on=None, left_index=False, right_index=False, sort=False,
    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None,
    _bodo_na_equal=True):
    qhdms__tpnw = dict(sort=sort, copy=copy, validate=validate)
    aijik__yom = dict(sort=False, copy=True, validate=None)
    check_unsupported_args('DataFrame.merge', qhdms__tpnw, aijik__yom)
    validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
        right_index, sort, suffixes, copy, indicator, validate)
    how = get_overload_const_str(how)
    brhk__dslm = tuple(sorted(set(left.columns) & set(right.columns), key=
        lambda k: str(k)))
    uowx__wit = ''
    if not is_overload_none(on):
        left_on = right_on = on
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            if on_str not in brhk__dslm and ('left.' in on_str or 'right.' in
                on_str):
                left_on, right_on, jxt__snx = _parse_merge_cond(on_str,
                    left.columns, left.data, right.columns, right.data)
                if jxt__snx is None:
                    uowx__wit = ''
                else:
                    uowx__wit = str(jxt__snx)
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = brhk__dslm
        right_keys = brhk__dslm
    else:
        if is_overload_true(left_index):
            left_keys = ['$_bodo_index_']
        else:
            left_keys = get_overload_const_list(left_on)
            validate_keys(left_keys, left.columns)
        if is_overload_true(right_index):
            right_keys = ['$_bodo_index_']
        else:
            right_keys = get_overload_const_list(right_on)
            validate_keys(right_keys, right.columns)
    if (not left_on or not right_on) and not is_overload_none(on):
        raise BodoError(
            f"DataFrame.merge(): Merge condition '{get_overload_const_str(on)}' requires a cross join to implement, but cross join is not supported."
            )
    if not is_overload_bool(indicator):
        raise_bodo_error(
            'DataFrame.merge(): indicator must be a constant boolean')
    indicator_val = get_overload_const_bool(indicator)
    if not is_overload_bool(_bodo_na_equal):
        raise_bodo_error(
            'DataFrame.merge(): bodo extension _bodo_na_equal must be a constant boolean'
            )
    bjesq__crxt = get_overload_const_bool(_bodo_na_equal)
    validate_keys_length(left_index, right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    if is_overload_constant_tuple(suffixes):
        eklyz__snq = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        eklyz__snq = list(get_overload_const_list(suffixes))
    suffix_x = eklyz__snq[0]
    suffix_y = eklyz__snq[1]
    validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
        right_keys, left.columns, right.columns, indicator_val)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    aaw__xjp = "def _impl(left, right, how='inner', on=None, left_on=None,\n"
    aaw__xjp += (
        '    right_on=None, left_index=False, right_index=False, sort=False,\n'
        )
    aaw__xjp += """    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None, _bodo_na_equal=True):
"""
    aaw__xjp += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, '{}', '{}', '{}', False, {}, {}, '{}')
"""
        .format(left_keys, right_keys, how, suffix_x, suffix_y,
        indicator_val, bjesq__crxt, uowx__wit))
    wyudp__cpm = {}
    exec(aaw__xjp, {'bodo': bodo}, wyudp__cpm)
    _impl = wyudp__cpm['_impl']
    return _impl


def common_validate_merge_merge_asof_spec(name_func, left, right, on,
    left_on, right_on, left_index, right_index, suffixes):
    if not isinstance(left, DataFrameType) or not isinstance(right,
        DataFrameType):
        raise BodoError(name_func + '() requires dataframe inputs')
    ensure_constant_arg(name_func, 'left_index', left_index, bool)
    ensure_constant_arg(name_func, 'right_index', right_index, bool)
    if not is_overload_constant_tuple(suffixes
        ) and not is_overload_constant_list(suffixes):
        raise_const_error(name_func +
            "(): suffixes parameters should be ['_left', '_right']")
    if is_overload_constant_tuple(suffixes):
        eklyz__snq = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        eklyz__snq = list(get_overload_const_list(suffixes))
    if len(eklyz__snq) != 2:
        raise BodoError(name_func +
            '(): The number of suffixes should be exactly 2')
    brhk__dslm = tuple(set(left.columns) & set(right.columns))
    if not is_overload_none(on):
        dcq__bzlp = False
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            dcq__bzlp = on_str not in brhk__dslm and ('left.' in on_str or 
                'right.' in on_str)
        if len(brhk__dslm) == 0 and not dcq__bzlp:
            raise_bodo_error(name_func +
                '(): No common columns to perform merge on. Merge options: left_on={lon}, right_on={ron}, left_index={lidx}, right_index={ridx}'
                .format(lon=is_overload_true(left_on), ron=is_overload_true
                (right_on), lidx=is_overload_true(left_index), ridx=
                is_overload_true(right_index)))
        if not is_overload_none(left_on) or not is_overload_none(right_on):
            raise BodoError(name_func +
                '(): Can only pass argument "on" OR "left_on" and "right_on", not a combination of both.'
                )
    if (is_overload_true(left_index) or not is_overload_none(left_on)
        ) and is_overload_none(right_on) and not is_overload_true(right_index):
        raise BodoError(name_func +
            '(): Must pass right_on or right_index=True')
    if (is_overload_true(right_index) or not is_overload_none(right_on)
        ) and is_overload_none(left_on) and not is_overload_true(left_index):
        raise BodoError(name_func + '(): Must pass left_on or left_index=True')


def validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
    right_index, sort, suffixes, copy, indicator, validate):
    common_validate_merge_merge_asof_spec('merge', left, right, on, left_on,
        right_on, left_index, right_index, suffixes)
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))


def validate_merge_asof_spec(left, right, on, left_on, right_on, left_index,
    right_index, by, left_by, right_by, suffixes, tolerance,
    allow_exact_matches, direction):
    common_validate_merge_merge_asof_spec('merge_asof', left, right, on,
        left_on, right_on, left_index, right_index, suffixes)
    if not is_overload_true(allow_exact_matches):
        raise BodoError(
            'merge_asof(): allow_exact_matches parameter only supports default value True'
            )
    if not is_overload_none(tolerance):
        raise BodoError(
            'merge_asof(): tolerance parameter only supports default value None'
            )
    if not is_overload_none(by):
        raise BodoError(
            'merge_asof(): by parameter only supports default value None')
    if not is_overload_none(left_by):
        raise BodoError(
            'merge_asof(): left_by parameter only supports default value None')
    if not is_overload_none(right_by):
        raise BodoError(
            'merge_asof(): right_by parameter only supports default value None'
            )
    if not is_overload_constant_str(direction):
        raise BodoError(
            'merge_asof(): direction parameter should be of type str')
    else:
        direction = get_overload_const_str(direction)
        if direction != 'backward':
            raise BodoError(
                "merge_asof(): direction parameter only supports default value 'backward'"
                )


def validate_merge_asof_keys_length(left_on, right_on, left_index,
    right_index, left_keys, right_keys):
    if not is_overload_true(left_index) and not is_overload_true(right_index):
        if len(right_keys) != len(left_keys):
            raise BodoError('merge(): len(right_on) must equal len(left_on)')
    if not is_overload_none(left_on) and is_overload_true(right_index):
        raise BodoError(
            'merge(): right_index = True and specifying left_on is not suppported yet.'
            )
    if not is_overload_none(right_on) and is_overload_true(left_index):
        raise BodoError(
            'merge(): left_index = True and specifying right_on is not suppported yet.'
            )


def validate_keys_length(left_index, right_index, left_keys, right_keys):
    if not is_overload_true(left_index) and not is_overload_true(right_index):
        if len(right_keys) != len(left_keys):
            raise BodoError('merge(): len(right_on) must equal len(left_on)')
    if is_overload_true(right_index):
        if len(left_keys) != 1:
            raise BodoError(
                'merge(): len(left_on) must equal the number of levels in the index of "right", which is 1'
                )
    if is_overload_true(left_index):
        if len(right_keys) != 1:
            raise BodoError(
                'merge(): len(right_on) must equal the number of levels in the index of "left", which is 1'
                )


def validate_keys_dtypes(left, right, left_index, right_index, left_keys,
    right_keys):
    ijvkm__iuu = numba.core.registry.cpu_target.typing_context
    if is_overload_true(left_index) or is_overload_true(right_index):
        if is_overload_true(left_index) and is_overload_true(right_index):
            ryzmj__avqqh = left.index
            omes__jqk = isinstance(ryzmj__avqqh, StringIndexType)
            xetc__bcil = right.index
            ppziu__zzuz = isinstance(xetc__bcil, StringIndexType)
        elif is_overload_true(left_index):
            ryzmj__avqqh = left.index
            omes__jqk = isinstance(ryzmj__avqqh, StringIndexType)
            xetc__bcil = right.data[right.columns.index(right_keys[0])]
            ppziu__zzuz = xetc__bcil.dtype == string_type
        elif is_overload_true(right_index):
            ryzmj__avqqh = left.data[left.columns.index(left_keys[0])]
            omes__jqk = ryzmj__avqqh.dtype == string_type
            xetc__bcil = right.index
            ppziu__zzuz = isinstance(xetc__bcil, StringIndexType)
        if omes__jqk and ppziu__zzuz:
            return
        ryzmj__avqqh = ryzmj__avqqh.dtype
        xetc__bcil = xetc__bcil.dtype
        try:
            hux__rrjyo = ijvkm__iuu.resolve_function_type(operator.eq, (
                ryzmj__avqqh, xetc__bcil), {})
        except:
            raise_bodo_error(
                'merge: You are trying to merge on {lk_dtype} and {rk_dtype} columns. If you wish to proceed you should use pd.concat'
                .format(lk_dtype=ryzmj__avqqh, rk_dtype=xetc__bcil))
    else:
        for darvs__gcn, bnys__scve in zip(left_keys, right_keys):
            ryzmj__avqqh = left.data[left.columns.index(darvs__gcn)].dtype
            fbqaa__kul = left.data[left.columns.index(darvs__gcn)]
            xetc__bcil = right.data[right.columns.index(bnys__scve)].dtype
            dqccc__elx = right.data[right.columns.index(bnys__scve)]
            if fbqaa__kul == dqccc__elx:
                continue
            rwb__ciovk = (
                'merge: You are trying to merge on column {lk} of {lk_dtype} and column {rk} of {rk_dtype}. If you wish to proceed you should use pd.concat'
                .format(lk=darvs__gcn, lk_dtype=ryzmj__avqqh, rk=bnys__scve,
                rk_dtype=xetc__bcil))
            xioi__atq = ryzmj__avqqh == string_type
            fbjhc__aella = xetc__bcil == string_type
            if xioi__atq ^ fbjhc__aella:
                raise_bodo_error(rwb__ciovk)
            try:
                hux__rrjyo = ijvkm__iuu.resolve_function_type(operator.eq,
                    (ryzmj__avqqh, xetc__bcil), {})
            except:
                raise_bodo_error(rwb__ciovk)


def validate_keys(keys, columns):
    if len(set(keys).difference(set(columns))) > 0:
        raise_bodo_error('merge(): invalid key {} for on/left_on/right_on'.
            format(set(keys).difference(set(columns))))


@overload_method(DataFrameType, 'join', inline='always', no_unliteral=True)
def overload_dataframe_join(left, other, on=None, how='left', lsuffix='',
    rsuffix='', sort=False):
    qhdms__tpnw = dict(lsuffix=lsuffix, rsuffix=rsuffix)
    aijik__yom = dict(lsuffix='', rsuffix='')
    check_unsupported_args('DataFrame.join', qhdms__tpnw, aijik__yom)
    validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort)
    how = get_overload_const_str(how)
    if not is_overload_none(on):
        left_keys = get_overload_const_list(on)
    else:
        left_keys = ['$_bodo_index_']
    right_keys = ['$_bodo_index_']
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    aaw__xjp = "def _impl(left, other, on=None, how='left',\n"
    aaw__xjp += "    lsuffix='', rsuffix='', sort=False):\n"
    aaw__xjp += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, other, {}, {}, '{}', '{}', '{}', True, False, True, '')
"""
        .format(left_keys, right_keys, how, lsuffix, rsuffix))
    wyudp__cpm = {}
    exec(aaw__xjp, {'bodo': bodo}, wyudp__cpm)
    _impl = wyudp__cpm['_impl']
    return _impl


def validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort):
    if not isinstance(other, DataFrameType):
        raise BodoError('join() requires dataframe inputs')
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))
    if not is_overload_none(on) and len(get_overload_const_list(on)) != 1:
        raise BodoError('join(): len(on) must equals to 1 when specified.')
    if not is_overload_none(on):
        ashkl__thjq = get_overload_const_list(on)
        validate_keys(ashkl__thjq, left.columns)
    if not is_overload_false(sort):
        raise BodoError(
            'join(): sort parameter only supports default value False')
    brhk__dslm = tuple(set(left.columns) & set(other.columns))
    if len(brhk__dslm) > 0:
        raise_bodo_error(
            'join(): not supporting joining on overlapping columns:{cols} Use DataFrame.merge() instead.'
            .format(cols=brhk__dslm))


def validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
    right_keys, left_columns, right_columns, indicator_val):
    aetky__nipe = set(left_keys) & set(right_keys)
    tsooc__qkcz = set(left_columns) & set(right_columns)
    jnkeb__xmd = tsooc__qkcz - aetky__nipe
    dvcg__tqxwu = set(left_columns) - tsooc__qkcz
    nvc__ahz = set(right_columns) - tsooc__qkcz
    eocgk__cju = {}

    def insertOutColumn(col_name):
        if col_name in eocgk__cju:
            raise_bodo_error(
                'join(): two columns happen to have the same name : {}'.
                format(col_name))
        eocgk__cju[col_name] = 0
    for dfjx__jlio in aetky__nipe:
        insertOutColumn(dfjx__jlio)
    for dfjx__jlio in jnkeb__xmd:
        kzu__fgdpv = str(dfjx__jlio) + suffix_x
        ixt__ace = str(dfjx__jlio) + suffix_y
        insertOutColumn(kzu__fgdpv)
        insertOutColumn(ixt__ace)
    for dfjx__jlio in dvcg__tqxwu:
        insertOutColumn(dfjx__jlio)
    for dfjx__jlio in nvc__ahz:
        insertOutColumn(dfjx__jlio)
    if indicator_val:
        insertOutColumn('_merge')


@overload(pd.merge_asof, inline='always', no_unliteral=True)
def overload_dataframe_merge_asof(left, right, on=None, left_on=None,
    right_on=None, left_index=False, right_index=False, by=None, left_by=
    None, right_by=None, suffixes=('_x', '_y'), tolerance=None,
    allow_exact_matches=True, direction='backward'):
    validate_merge_asof_spec(left, right, on, left_on, right_on, left_index,
        right_index, by, left_by, right_by, suffixes, tolerance,
        allow_exact_matches, direction)
    if not isinstance(left, DataFrameType) or not isinstance(right,
        DataFrameType):
        raise BodoError('merge_asof() requires dataframe inputs')
    brhk__dslm = tuple(sorted(set(left.columns) & set(right.columns), key=
        lambda k: str(k)))
    if not is_overload_none(on):
        left_on = right_on = on
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = brhk__dslm
        right_keys = brhk__dslm
    else:
        if is_overload_true(left_index):
            left_keys = ['$_bodo_index_']
        else:
            left_keys = get_overload_const_list(left_on)
            validate_keys(left_keys, left.columns)
        if is_overload_true(right_index):
            right_keys = ['$_bodo_index_']
        else:
            right_keys = get_overload_const_list(right_on)
            validate_keys(right_keys, right.columns)
    validate_merge_asof_keys_length(left_on, right_on, left_index,
        right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    if isinstance(suffixes, tuple):
        eklyz__snq = suffixes
    if is_overload_constant_list(suffixes):
        eklyz__snq = list(get_overload_const_list(suffixes))
    if isinstance(suffixes, types.Omitted):
        eklyz__snq = suffixes.value
    suffix_x = eklyz__snq[0]
    suffix_y = eklyz__snq[1]
    aaw__xjp = 'def _impl(left, right, on=None, left_on=None, right_on=None,\n'
    aaw__xjp += (
        '    left_index=False, right_index=False, by=None, left_by=None,\n')
    aaw__xjp += "    right_by=None, suffixes=('_x', '_y'), tolerance=None,\n"
    aaw__xjp += "    allow_exact_matches=True, direction='backward'):\n"
    aaw__xjp += '  suffix_x = suffixes[0]\n'
    aaw__xjp += '  suffix_y = suffixes[1]\n'
    aaw__xjp += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, 'asof', '{}', '{}', False, False, True, '')
"""
        .format(left_keys, right_keys, suffix_x, suffix_y))
    wyudp__cpm = {}
    exec(aaw__xjp, {'bodo': bodo}, wyudp__cpm)
    _impl = wyudp__cpm['_impl']
    return _impl


@overload_method(DataFrameType, 'groupby', inline='always', no_unliteral=True)
def overload_dataframe_groupby(df, by=None, axis=0, level=None, as_index=
    True, sort=False, group_keys=True, squeeze=False, observed=True, dropna
    =True):
    validate_groupby_spec(df, by, axis, level, as_index, sort, group_keys,
        squeeze, observed, dropna)

    def _impl(df, by=None, axis=0, level=None, as_index=True, sort=False,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        return bodo.hiframes.pd_groupby_ext.init_groupby(df, by, as_index,
            dropna)
    return _impl


def validate_groupby_spec(df, by, axis, level, as_index, sort, group_keys,
    squeeze, observed, dropna):
    if is_overload_none(by):
        raise BodoError("groupby(): 'by' must be supplied.")
    if not is_overload_zero(axis):
        raise BodoError(
            "groupby(): 'axis' parameter only supports integer value 0.")
    if not is_overload_none(level):
        raise BodoError(
            "groupby(): 'level' is not supported since MultiIndex is not supported."
            )
    if not is_literal_type(by) and not is_overload_constant_list(by):
        raise_const_error(
            f"groupby(): 'by' parameter only supports a constant column label or column labels, not {by}."
            )
    if len(set(get_overload_const_list(by)).difference(set(df.columns))) > 0:
        raise_const_error(
            "groupby(): invalid key {} for 'by' (not available in columns {})."
            .format(get_overload_const_list(by), df.columns))
    if not is_overload_constant_bool(as_index):
        raise_const_error(
            "groupby(): 'as_index' parameter must be a constant bool, not {}."
            .format(as_index))
    if not is_overload_constant_bool(dropna):
        raise_const_error(
            "groupby(): 'dropna' parameter must be a constant bool, not {}."
            .format(dropna))
    qhdms__tpnw = dict(sort=sort, group_keys=group_keys, squeeze=squeeze,
        observed=observed)
    uyhw__uml = dict(sort=False, group_keys=True, squeeze=False, observed=True)
    check_unsupported_args('Dataframe.groupby', qhdms__tpnw, uyhw__uml)


@overload_method(DataFrameType, 'pivot_table', inline='always',
    no_unliteral=True)
def overload_dataframe_pivot_table(df, values=None, index=None, columns=
    None, aggfunc='mean', fill_value=None, margins=False, dropna=True,
    margins_name='All', observed=True, _pivot_values=None):
    qhdms__tpnw = dict(fill_value=fill_value, margins=margins, dropna=
        dropna, margins_name=margins_name, observed=observed)
    aijik__yom = dict(fill_value=None, margins=False, dropna=True,
        margins_name='All', observed=True)
    check_unsupported_args('DataFrame.pivot_table', qhdms__tpnw, aijik__yom)
    if aggfunc == 'mean':

        def _impl(df, values=None, index=None, columns=None, aggfunc='mean',
            fill_value=None, margins=False, dropna=True, margins_name='All',
            observed=True, _pivot_values=None):
            return bodo.hiframes.pd_groupby_ext.pivot_table_dummy(df,
                values, index, columns, 'mean', _pivot_values)
        return _impl

    def _impl(df, values=None, index=None, columns=None, aggfunc='mean',
        fill_value=None, margins=False, dropna=True, margins_name='All',
        observed=True, _pivot_values=None):
        return bodo.hiframes.pd_groupby_ext.pivot_table_dummy(df, values,
            index, columns, aggfunc, _pivot_values)
    return _impl


@overload(pd.crosstab, inline='always', no_unliteral=True)
def crosstab_overload(index, columns, values=None, rownames=None, colnames=
    None, aggfunc=None, margins=False, margins_name='All', dropna=True,
    normalize=False, _pivot_values=None):
    qhdms__tpnw = dict(values=values, rownames=rownames, colnames=colnames,
        aggfunc=aggfunc, margins=margins, margins_name=margins_name, dropna
        =dropna, normalize=normalize)
    aijik__yom = dict(values=None, rownames=None, colnames=None, aggfunc=
        None, margins=False, margins_name='All', dropna=True, normalize=False)
    check_unsupported_args('pd.crosstab', qhdms__tpnw, aijik__yom)

    def _impl(index, columns, values=None, rownames=None, colnames=None,
        aggfunc=None, margins=False, margins_name='All', dropna=True,
        normalize=False, _pivot_values=None):
        return bodo.hiframes.pd_groupby_ext.crosstab_dummy(index, columns,
            _pivot_values)
    return _impl


@overload_method(DataFrameType, 'sort_values', inline='always',
    no_unliteral=True)
def overload_dataframe_sort_values(df, by, axis=0, ascending=True, inplace=
    False, kind='quicksort', na_position='last', ignore_index=False, key=
    None, _bodo_transformed=False):
    qhdms__tpnw = dict(ignore_index=ignore_index, key=key)
    aijik__yom = dict(ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_values', qhdms__tpnw, aijik__yom)
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'sort_values')
    validate_sort_values_spec(df, by, axis, ascending, inplace, kind,
        na_position)

    def _impl(df, by, axis=0, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', ignore_index=False, key=None,
        _bodo_transformed=False):
        return bodo.hiframes.pd_dataframe_ext.sort_values_dummy(df, by,
            ascending, inplace, na_position)
    return _impl


def validate_sort_values_spec(df, by, axis, ascending, inplace, kind,
    na_position):
    if is_overload_none(by) or not is_literal_type(by
        ) and not is_overload_constant_list(by):
        raise_const_error(
            "sort_values(): 'by' parameter only supports a constant column label or column labels. by={}"
            .format(by))
    pbnrd__mdt = set(df.columns)
    if is_overload_constant_str(df.index.name_typ):
        pbnrd__mdt.add(get_overload_const_str(df.index.name_typ))
    if is_overload_constant_tuple(by):
        uat__nxzd = [get_overload_const_tuple(by)]
    else:
        uat__nxzd = get_overload_const_list(by)
    uat__nxzd = set((k, '') if (k, '') in pbnrd__mdt else k for k in uat__nxzd)
    if len(uat__nxzd.difference(pbnrd__mdt)) > 0:
        wyxk__nuq = list(set(get_overload_const_list(by)).difference(
            pbnrd__mdt))
        raise_bodo_error(f'sort_values(): invalid keys {wyxk__nuq} for by.')
    if not is_overload_zero(axis):
        raise_bodo_error(
            "sort_values(): 'axis' parameter only supports integer value 0.")
    if not is_overload_bool(ascending) and not is_overload_bool_list(ascending
        ):
        raise_bodo_error(
            "sort_values(): 'ascending' parameter must be of type bool or list of bool, not {}."
            .format(ascending))
    if not is_overload_bool(inplace):
        raise_bodo_error(
            "sort_values(): 'inplace' parameter must be of type bool, not {}."
            .format(inplace))
    if kind != 'quicksort' and not isinstance(kind, types.Omitted):
        warnings.warn(BodoWarning(
            'sort_values(): specifying sorting algorithm is not supported in Bodo. Bodo uses stable sort.'
            ))
    if is_overload_constant_str(na_position):
        na_position = get_overload_const_str(na_position)
        if na_position not in ('first', 'last'):
            raise BodoError(
                "sort_values(): na_position should either be 'first' or 'last'"
                )
    elif is_overload_constant_list(na_position):
        fat__mgkgy = get_overload_const_list(na_position)
        for na_position in fat__mgkgy:
            if na_position not in ('first', 'last'):
                raise BodoError(
                    "sort_values(): Every value in na_position should either be 'first' or 'last'"
                    )
    else:
        raise_const_error(
            f'sort_values(): na_position parameter must be a literal constant of type str or a constant list of str with 1 entry per key column, not {na_position}'
            )
    na_position = get_overload_const_str(na_position)
    if na_position not in ['first', 'last']:
        raise BodoError(
            "sort_values(): na_position should either be 'first' or 'last'")


@overload_method(DataFrameType, 'sort_index', inline='always', no_unliteral
    =True)
def overload_dataframe_sort_index(df, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None, by=None):
    qhdms__tpnw = dict(axis=axis, level=level, kind=kind, sort_remaining=
        sort_remaining, ignore_index=ignore_index, key=key)
    aijik__yom = dict(axis=0, level=None, kind='quicksort', sort_remaining=
        True, ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_index', qhdms__tpnw, aijik__yom)

    def _impl(df, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None, by=None):
        return bodo.hiframes.pd_dataframe_ext.sort_values_dummy(df,
            '$_bodo_index_', ascending, inplace, na_position)
    return _impl


@overload_method(DataFrameType, 'fillna', inline='always', no_unliteral=True)
def overload_dataframe_fillna(df, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    qhdms__tpnw = dict(method=method, limit=limit, downcast=downcast)
    aijik__yom = dict(method=None, limit=None, downcast=None)
    check_unsupported_args('DataFrame.fillna', qhdms__tpnw, aijik__yom)
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError('DataFrame.fillna: axis argument not supported')
    data_args = [(f"df['{ebc__koy}'].fillna(value, inplace=inplace)" if
        isinstance(ebc__koy, str) else
        f'df[{ebc__koy}].fillna(value, inplace=inplace)') for ebc__koy in
        df.columns]
    aaw__xjp = """def impl(df, value=None, method=None, axis=None, inplace=False, limit=None, downcast=None):
"""
    if is_overload_true(inplace):
        aaw__xjp += '  ' + '  \n'.join(data_args) + '\n'
        wyudp__cpm = {}
        exec(aaw__xjp, {}, wyudp__cpm)
        impl = wyudp__cpm['impl']
        return impl
    else:
        return _gen_init_df(aaw__xjp, df.columns, ', '.join(blxy__gpt +
            '.values' for blxy__gpt in data_args))


@overload_method(DataFrameType, 'reset_index', inline='always',
    no_unliteral=True)
def overload_dataframe_reset_index(df, level=None, drop=False, inplace=
    False, col_level=0, col_fill='', _bodo_transformed=False):
    qhdms__tpnw = dict(col_level=col_level, col_fill=col_fill)
    aijik__yom = dict(col_level=0, col_fill='')
    check_unsupported_args('DataFrame.reset_index', qhdms__tpnw, aijik__yom)
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'reset_index')
    if not _is_all_levels(df, level):
        raise_bodo_error(
            'DataFrame.reset_index(): only dropping all index levels supported'
            )
    if not is_overload_constant_bool(drop):
        raise BodoError(
            "DataFrame.reset_index(): 'drop' parameter should be a constant boolean value"
            )
    if not is_overload_constant_bool(inplace):
        raise BodoError(
            "DataFrame.reset_index(): 'inplace' parameter should be a constant boolean value"
            )
    aaw__xjp = """def impl(df, level=None, drop=False, inplace=False, col_level=0, col_fill='', _bodo_transformed=False,):
"""
    aaw__xjp += (
        '  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(df), 1, None)\n'
        )
    drop = is_overload_true(drop)
    inplace = is_overload_true(inplace)
    columns = df.columns
    data_args = [
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}\n'.
        format(i, '' if inplace else '.copy()') for i in range(len(df.columns))
        ]
    if not drop:
        apz__hrx = 'index' if 'index' not in columns else 'level_0'
        index_names = get_index_names(df.index, 'DataFrame.reset_index()',
            apz__hrx)
        columns = index_names + columns
        if isinstance(df.index, MultiIndexType):
            aaw__xjp += (
                '  m_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
                )
            tlihy__dpi = ['m_index._data[{}]'.format(i) for i in range(df.
                index.nlevels)]
            data_args = tlihy__dpi + data_args
        else:
            bsbp__mcyp = (
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
                )
            data_args = [bsbp__mcyp] + data_args
    return _gen_init_df(aaw__xjp, columns, ', '.join(data_args), 'index')


def _is_all_levels(df, level):
    whu__xge = len(get_index_data_arr_types(df.index))
    return is_overload_none(level) or is_overload_constant_int(level
        ) and get_overload_const_int(level
        ) == 0 and whu__xge == 1 or is_overload_constant_list(level) and list(
        get_overload_const_list(level)) == list(range(whu__xge))


@overload_method(DataFrameType, 'dropna', inline='always', no_unliteral=True)
def overload_dataframe_dropna(df, axis=0, how='any', thresh=None, subset=
    None, inplace=False):
    if not is_overload_constant_bool(inplace) or is_overload_true(inplace):
        raise BodoError('DataFrame.dropna(): inplace=True is not supported')
    if not is_overload_zero(axis):
        raise_bodo_error(f'df.dropna(): only axis=0 supported')
    ensure_constant_values('dropna', 'how', how, ('any', 'all'))
    if is_overload_none(subset):
        zmau__rwby = list(range(len(df.columns)))
    elif not is_overload_constant_list(subset):
        raise_bodo_error(
            f'df.dropna(): subset argument should a constant list, not {subset}'
            )
    else:
        vampe__cjg = get_overload_const_list(subset)
        zmau__rwby = []
        for kbit__wyrt in vampe__cjg:
            if kbit__wyrt not in df.columns:
                raise_bodo_error(
                    f"df.dropna(): column '{kbit__wyrt}' not in data frame columns {df}"
                    )
            zmau__rwby.append(df.columns.index(kbit__wyrt))
    istxx__jnt = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(istxx__jnt))
    aaw__xjp = (
        "def impl(df, axis=0, how='any', thresh=None, subset=None, inplace=False):\n"
        )
    for i in range(istxx__jnt):
        aaw__xjp += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    aaw__xjp += (
        """  ({0}, index_arr) = bodo.libs.array_kernels.dropna(({0}, {1}), how, thresh, ({2},))
"""
        .format(data_args, index, ', '.join(str(a) for a in zmau__rwby)))
    aaw__xjp += '  index = bodo.utils.conversion.index_from_array(index_arr)\n'
    return _gen_init_df(aaw__xjp, df.columns, data_args, 'index')


@overload_method(DataFrameType, 'drop', inline='always', no_unliteral=True)
def overload_dataframe_drop(df, labels=None, axis=0, index=None, columns=
    None, level=None, inplace=False, errors='raise', _bodo_transformed=False):
    qhdms__tpnw = dict(index=index, level=level, errors=errors)
    aijik__yom = dict(index=None, level=None, errors='raise')
    check_unsupported_args('DataFrame.drop', qhdms__tpnw, aijik__yom)
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'drop')
    if not is_overload_constant_bool(inplace):
        raise_bodo_error(
            "DataFrame.drop(): 'inplace' parameter should be a constant bool")
    if not is_overload_none(labels):
        if not is_overload_none(columns):
            raise BodoError(
                "Dataframe.drop(): Cannot specify both 'labels' and 'columns'")
        if not is_overload_constant_int(axis) or get_overload_const_int(axis
            ) != 1:
            raise_bodo_error('DataFrame.drop(): only axis=1 supported')
        if is_overload_constant_str(labels):
            wxdg__wab = get_overload_const_str(labels),
        elif is_overload_constant_list(labels):
            wxdg__wab = get_overload_const_list(labels)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    else:
        if is_overload_none(columns):
            raise BodoError(
                "DataFrame.drop(): Need to specify at least one of 'labels' or 'columns'"
                )
        if is_overload_constant_str(columns):
            wxdg__wab = get_overload_const_str(columns),
        elif is_overload_constant_list(columns):
            wxdg__wab = get_overload_const_list(columns)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    for ebc__koy in wxdg__wab:
        if ebc__koy not in df.columns:
            raise_bodo_error(
                'DataFrame.drop(): column {} not in DataFrame columns {}'.
                format(ebc__koy, df.columns))
    if len(set(wxdg__wab)) == len(df.columns):
        raise BodoError('DataFrame.drop(): Dropping all columns not supported.'
            )
    inplace = is_overload_true(inplace)
    dxhyd__krkcp = tuple(ebc__koy for ebc__koy in df.columns if ebc__koy not in
        wxdg__wab)
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.columns.index(ebc__koy), '.copy()' if not inplace else ''
        ) for ebc__koy in dxhyd__krkcp)
    aaw__xjp = 'def impl(df, labels=None, axis=0, index=None, columns=None,\n'
    aaw__xjp += (
        "     level=None, inplace=False, errors='raise', _bodo_transformed=False):\n"
        )
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    return _gen_init_df(aaw__xjp, dxhyd__krkcp, data_args, index)


@overload_method(DataFrameType, 'append', inline='always', no_unliteral=True)
def overload_dataframe_append(df, other, ignore_index=False,
    verify_integrity=False, sort=None):
    if isinstance(other, DataFrameType):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat((df, other), ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    if isinstance(other, types.BaseTuple):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat((df,) + other, ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    if isinstance(other, types.List) and isinstance(other.dtype, DataFrameType
        ):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat([df] + other, ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    raise BodoError(
        'invalid df.append() input. Only dataframe and list/tuple of dataframes supported'
        )


@overload_method(DataFrameType, 'sample', inline='always', no_unliteral=True)
def overload_dataframe_sample(df, n=None, frac=None, replace=False, weights
    =None, random_state=None, axis=None):
    qhdms__tpnw = dict(random_state=random_state, weights=weights, axis=axis)
    bgxf__zeruc = dict(random_state=None, weights=None, axis=None)
    check_unsupported_args('sample', qhdms__tpnw, bgxf__zeruc)
    if not is_overload_none(n) and not is_overload_none(frac):
        raise BodoError(
            'sample(): only one of n and frac option can be selected')
    istxx__jnt = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(istxx__jnt))
    aaw__xjp = """def impl(df, n=None, frac=None, replace=False, weights=None, random_state=None, axis=None):
"""
    for i in range(istxx__jnt):
        aaw__xjp += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    aaw__xjp += '  if frac is None:\n'
    aaw__xjp += '    frac_d = -1.0\n'
    aaw__xjp += '  else:\n'
    aaw__xjp += '    frac_d = frac\n'
    aaw__xjp += '  if n is None:\n'
    aaw__xjp += '    n_i = 0\n'
    aaw__xjp += '  else:\n'
    aaw__xjp += '    n_i = n\n'
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    aaw__xjp += (
        """  ({0},), index_arr = bodo.libs.array_kernels.sample_table_operation(({0},), {1}, n_i, frac_d, replace)
"""
        .format(data_args, index))
    aaw__xjp += '  index = bodo.utils.conversion.index_from_array(index_arr)\n'
    return bodo.hiframes.dataframe_impl._gen_init_df(aaw__xjp, df.columns,
        data_args, 'index')


@numba.njit
def _sizeof_fmt(num, size_qualifier=''):
    for ixvq__dtvhk in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return f'{num:3.1f}{size_qualifier} {ixvq__dtvhk}'
        num /= 1024.0
    return f'{num:3.1f}{size_qualifier} PB'


@overload_method(DataFrameType, 'info', no_unliteral=True)
def overload_dataframe_info(df, verbose=None, buf=None, max_cols=None,
    memory_usage=None, show_counts=None, null_counts=None):
    mwezv__himy = {'verbose': verbose, 'buf': buf, 'max_cols': max_cols,
        'memory_usage': memory_usage, 'show_counts': show_counts,
        'null_counts': null_counts}
    bnhi__bodsb = {'verbose': None, 'buf': None, 'max_cols': None,
        'memory_usage': None, 'show_counts': None, 'null_counts': None}
    check_unsupported_args('DataFrame.info', mwezv__himy, bnhi__bodsb)
    vjojd__hiip = f"<class '{str(type(df)).split('.')[-1]}"
    if len(df.columns) == 0:

        def _info_impl(df, verbose=None, buf=None, max_cols=None,
            memory_usage=None, show_counts=None, null_counts=None):
            vza__cktl = vjojd__hiip + '\n'
            vza__cktl += 'Index: 0 entries\n'
            vza__cktl += 'Empty DataFrame'
            print(vza__cktl)
        return _info_impl
    else:
        aaw__xjp = """def _info_impl(df, verbose=None, buf=None, max_cols=None, memory_usage=None, show_counts=None, null_counts=None): #pragma: no cover
"""
        aaw__xjp += '    ncols = df.shape[1]\n'
        aaw__xjp += f'    lines = "{vjojd__hiip}\\n"\n'
        aaw__xjp += f'    lines += "{df.index}: "\n'
        aaw__xjp += (
            '    index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        if isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType):
            aaw__xjp += """    lines += f"{len(index)} entries, {index.start} to {index.stop-1}\\n\"
"""
        elif isinstance(df.index, bodo.hiframes.pd_index_ext.StringIndexType):
            aaw__xjp += """    lines += f"{len(index)} entries, {index[0]} to {index[len(index)-1]}\\n\"
"""
        else:
            aaw__xjp += (
                '    lines += f"{len(index)} entries, {index[0]} to {index[-1]}\\n"\n'
                )
        aaw__xjp += (
            '    lines += f"Data columns (total {ncols} columns):\\n"\n')
        aaw__xjp += f'    space = {max(len(str(k)) for k in df.columns) + 1}\n'
        aaw__xjp += '    column_width = max(space, 7)\n'
        aaw__xjp += '    column= "Column"\n'
        aaw__xjp += '    underl= "------"\n'
        aaw__xjp += (
            '    lines += f"#   {column:<{column_width}} Non-Null Count  Dtype\\n"\n'
            )
        aaw__xjp += (
            '    lines += f"--- {underl:<{column_width}} --------------  -----\\n"\n'
            )
        aaw__xjp += '    mem_size = 0\n'
        aaw__xjp += (
            '    col_name = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        aaw__xjp += """    non_null_count = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)
"""
        aaw__xjp += (
            '    col_dtype = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        ipis__smgb = dict()
        for i in range(len(df.columns)):
            aaw__xjp += f"""    non_null_count[{i}] = str(bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})))
"""
            xmsx__rsmj = f'{df.data[i].dtype}'
            if isinstance(df.data[i], bodo.CategoricalArrayType):
                xmsx__rsmj = 'category'
            elif isinstance(df.data[i], bodo.IntegerArrayType):
                sjij__ynmp = bodo.libs.int_arr_ext.IntDtype(df.data[i].dtype
                    ).name
                xmsx__rsmj = f'{sjij__ynmp[:-7]}'
            aaw__xjp += f'    col_dtype[{i}] = "{xmsx__rsmj}"\n'
            if xmsx__rsmj in ipis__smgb:
                ipis__smgb[xmsx__rsmj] += 1
            else:
                ipis__smgb[xmsx__rsmj] = 1
            aaw__xjp += f'    col_name[{i}] = "{df.columns[i]}"\n'
            aaw__xjp += f"""    mem_size += bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).nbytes
"""
        aaw__xjp += """    column_info = [f'{i:^3} {name:<{column_width}} {count} non-null      {dtype}' for i, (name, count, dtype) in enumerate(zip(col_name, non_null_count, col_dtype))]
"""
        aaw__xjp += '    for i in column_info:\n'
        aaw__xjp += "        lines += f'{i}\\n'\n"
        kiya__nvc = ', '.join(f'{k}({ipis__smgb[k]})' for k in sorted(
            ipis__smgb))
        aaw__xjp += f"    lines += 'dtypes: {kiya__nvc}\\n'\n"
        aaw__xjp += '    mem_size += df.index.nbytes\n'
        aaw__xjp += '    total_size = _sizeof_fmt(mem_size)\n'
        aaw__xjp += "    lines += f'memory usage: {total_size}'\n"
        aaw__xjp += '    print(lines)\n'
        wyudp__cpm = {}
        exec(aaw__xjp, {'_sizeof_fmt': _sizeof_fmt, 'pd': pd, 'bodo': bodo,
            'np': np}, wyudp__cpm)
        _info_impl = wyudp__cpm['_info_impl']
        return _info_impl


@overload_method(DataFrameType, 'memory_usage', inline='always',
    no_unliteral=True)
def overload_dataframe_memory_usage(df, index=True, deep=False):
    aaw__xjp = 'def impl(df, index=True, deep=False):\n'
    data = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).nbytes'
         for i in range(len(df.columns)))
    if is_overload_true(index):
        yjgua__fzqr = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df).nbytes\n,')
        essu__ywfpq = ','.join(f"'{ebc__koy}'" for ebc__koy in df.columns)
        arr = f"bodo.utils.conversion.coerce_to_array(('Index',{essu__ywfpq}))"
        index = f'bodo.hiframes.pd_index_ext.init_binary_str_index({arr})'
        aaw__xjp += f"""  return bodo.hiframes.pd_series_ext.init_series(({yjgua__fzqr}{data}), {index}, None)
"""
    else:
        fpowr__ixu = ',' if len(df.columns) == 1 else ''
        ebpx__xqqk = gen_const_tup(df.columns)
        aaw__xjp += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}{fpowr__ixu}), pd.Index({ebpx__xqqk}), None)
"""
    wyudp__cpm = {}
    exec(aaw__xjp, {'bodo': bodo, 'pd': pd}, wyudp__cpm)
    impl = wyudp__cpm['impl']
    return impl


@overload(pd.read_excel, no_unliteral=True)
def overload_read_excel(io, sheet_name=0, header=0, names=None, index_col=
    None, usecols=None, squeeze=False, dtype=None, engine=None, converters=
    None, true_values=None, false_values=None, skiprows=None, nrows=None,
    na_values=None, keep_default_na=True, na_filter=True, verbose=False,
    parse_dates=False, date_parser=None, thousands=None, comment=None,
    skipfooter=0, convert_float=True, mangle_dupe_cols=True, _bodo_df_type=None
    ):
    df_type = _bodo_df_type.instance_type
    oqq__hdp = 'read_excel_df{}'.format(next_label())
    setattr(types, oqq__hdp, df_type)
    dwe__vbh = False
    if is_overload_constant_list(parse_dates):
        dwe__vbh = get_overload_const_list(parse_dates)
    bjs__wuc = ', '.join(["'{}':{}".format(cname, _get_pd_dtype_str(t)) for
        cname, t in zip(df_type.columns, df_type.data)])
    aaw__xjp = (
        """
def impl(
    io,
    sheet_name=0,
    header=0,
    names=None,
    index_col=None,
    usecols=None,
    squeeze=False,
    dtype=None,
    engine=None,
    converters=None,
    true_values=None,
    false_values=None,
    skiprows=None,
    nrows=None,
    na_values=None,
    keep_default_na=True,
    na_filter=True,
    verbose=False,
    parse_dates=False,
    date_parser=None,
    thousands=None,
    comment=None,
    skipfooter=0,
    convert_float=True,
    mangle_dupe_cols=True,
    _bodo_df_type=None,
):
    with numba.objmode(df="{}"):
        df = pd.read_excel(
            io,
            sheet_name,
            header,
            {},
            index_col,
            usecols,
            squeeze,
            {{{}}},
            engine,
            converters,
            true_values,
            false_values,
            skiprows,
            nrows,
            na_values,
            keep_default_na,
            na_filter,
            verbose,
            {},
            date_parser,
            thousands,
            comment,
            skipfooter,
            convert_float,
            mangle_dupe_cols,
        )
    return df
    """
        .format(oqq__hdp, list(df_type.columns), bjs__wuc, dwe__vbh))
    wyudp__cpm = {}
    exec(aaw__xjp, globals(), wyudp__cpm)
    impl = wyudp__cpm['impl']
    return impl


def typeref_to_type(v):
    if isinstance(v, types.BaseTuple):
        return types.BaseTuple.from_types(tuple(typeref_to_type(a) for a in v))
    return v.instance_type if isinstance(v, (types.TypeRef, types.NumberClass)
        ) else v


def _install_typer_for_type(type_name, typ):

    @type_callable(typ)
    def type_call_type(context):

        def typer(*args, **kws):
            args = tuple(typeref_to_type(v) for v in args)
            kws = {name: typeref_to_type(v) for name, v in kws.items()}
            return types.TypeRef(typ(*args, **kws))
        return typer
    no_side_effect_call_tuples.add((type_name, bodo))
    no_side_effect_call_tuples.add((typ,))


def _install_type_call_typers():
    for type_name in bodo_types_with_params:
        typ = getattr(bodo, type_name)
        _install_typer_for_type(type_name, typ)


_install_type_call_typers()


def set_df_col(df, cname, arr, inplace):
    df[cname] = arr


@infer_global(set_df_col)
class SetDfColInfer(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        assert not kws
        assert len(args) == 4
        assert isinstance(args[1], types.Literal)
        vjjn__yyp = args[0]
        pmpr__pambu = args[1].literal_value
        val = args[2]
        assert val != types.unknown
        lugl__lptr = vjjn__yyp
        if isinstance(vjjn__yyp, DataFrameType):
            index = vjjn__yyp.index
            if len(vjjn__yyp.columns) == 0:
                index = bodo.hiframes.pd_index_ext.RangeIndexType(types.none)
            if isinstance(val, SeriesType):
                if len(vjjn__yyp.columns) == 0:
                    index = val.index
                val = val.data
            if isinstance(val, types.List):
                val = dtype_to_array_type(val.dtype)
            if not is_array_typ(val):
                val = dtype_to_array_type(val)
            if pmpr__pambu in vjjn__yyp.columns:
                dxhyd__krkcp = vjjn__yyp.columns
                dacic__btp = vjjn__yyp.columns.index(pmpr__pambu)
                npa__ubx = list(vjjn__yyp.data)
                npa__ubx[dacic__btp] = val
                npa__ubx = tuple(npa__ubx)
            else:
                dxhyd__krkcp = vjjn__yyp.columns + (pmpr__pambu,)
                npa__ubx = vjjn__yyp.data + (val,)
            lugl__lptr = DataFrameType(npa__ubx, index, dxhyd__krkcp)
        return lugl__lptr(*args)


def _parse_query_expr(expr, env, columns, cleaned_columns, index_name=None,
    join_cleaned_cols=()):
    tlo__hvbe = {}

    def _rewrite_membership_op(self, node, left, right):
        kckr__eqs = node.op
        op = self.visit(kckr__eqs)
        return op, kckr__eqs, left, right

    def _maybe_evaluate_binop(self, op, op_class, lhs, rhs, eval_in_python=
        ('in', 'not in'), maybe_eval_in_python=('==', '!=', '<', '>', '<=',
        '>=')):
        res = op(lhs, rhs)
        return res
    wcg__pubb = []


    class NewFuncNode(pd.core.computation.ops.FuncNode):

        def __init__(self, name):
            if (name not in pd.core.computation.ops.MATHOPS or pd.core.
                computation.check._NUMEXPR_INSTALLED and pd.core.
                computation.check_NUMEXPR_VERSION < pd.core.computation.ops
                .LooseVersion('2.6.9') and name in ('floor', 'ceil')):
                if name not in wcg__pubb:
                    raise BodoError('"{0}" is not a supported function'.
                        format(name))
            self.name = name
            if name in wcg__pubb:
                self.func = name
            else:
                self.func = getattr(np, name)

        def __call__(self, *args):
            return pd.core.computation.ops.MathCall(self, args)

        def __repr__(self):
            return pd.io.formats.printing.pprint_thing(self.name)

    def visit_Attribute(self, node, **kwargs):
        fjth__vfmt = node.attr
        value = node.value
        qoya__cmr = pd.core.computation.ops.LOCAL_TAG
        if fjth__vfmt in ('str', 'dt'):
            try:
                emxxr__xsmv = str(self.visit(value))
            except pd.core.computation.ops.UndefinedVariableError as bfy__dcxr:
                col_name = bfy__dcxr.args[0].split("'")[1]
                raise BodoError(
                    'df.query(): column {} is not found in dataframe columns {}'
                    .format(col_name, columns))
        else:
            emxxr__xsmv = str(self.visit(value))
        wad__pahs = emxxr__xsmv, fjth__vfmt
        if wad__pahs in join_cleaned_cols:
            fjth__vfmt = join_cleaned_cols[wad__pahs]
        name = emxxr__xsmv + '.' + fjth__vfmt
        if name.startswith(qoya__cmr):
            name = name[len(qoya__cmr):]
        if fjth__vfmt in ('str', 'dt'):
            wov__dlwax = columns[cleaned_columns.index(emxxr__xsmv)]
            tlo__hvbe[wov__dlwax] = emxxr__xsmv
            self.env.scope[name] = 0
            return self.term_type(qoya__cmr + name, self.env)
        wcg__pubb.append(name)
        return NewFuncNode(name)

    def __str__(self):
        if isinstance(self.value, list):
            return '{}'.format(self.value)
        if isinstance(self.value, str):
            return "'{}'".format(self.value)
        return pd.io.formats.printing.pprint_thing(self.name)

    def math__str__(self):
        if self.op in wcg__pubb:
            return pd.io.formats.printing.pprint_thing('{0}({1})'.format(
                self.op, ','.join(map(str, self.operands))))
        vrufw__rswv = map(lambda a:
            'bodo.hiframes.pd_series_ext.get_series_data({})'.format(str(a)
            ), self.operands)
        op = 'np.{}'.format(self.op)
        pmpr__pambu = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len({}), 1, None)'
            .format(str(self.operands[0])))
        return pd.io.formats.printing.pprint_thing(
            'bodo.hiframes.pd_series_ext.init_series({0}({1}), {2})'.format
            (op, ','.join(vrufw__rswv), pmpr__pambu))

    def op__str__(self):
        bsq__yhy = ('({0})'.format(pd.io.formats.printing.pprint_thing(
            vqlj__flsi)) for vqlj__flsi in self.operands)
        if self.op == 'in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_isin_dummy({})'.format(
                ', '.join(bsq__yhy)))
        if self.op == 'not in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_notin_dummy({})'.format
                (', '.join(bsq__yhy)))
        return pd.io.formats.printing.pprint_thing(' {0} '.format(self.op).
            join(bsq__yhy))
    kzrma__kqi = (pd.core.computation.expr.BaseExprVisitor.
        _rewrite_membership_op)
    ibxn__vmweb = (pd.core.computation.expr.BaseExprVisitor.
        _maybe_evaluate_binop)
    nruf__fghj = pd.core.computation.expr.BaseExprVisitor.visit_Attribute
    uvy__dsea = (pd.core.computation.expr.BaseExprVisitor.
        _maybe_downcast_constants)
    qjybe__oue = pd.core.computation.ops.Term.__str__
    xjozv__rctj = pd.core.computation.ops.MathCall.__str__
    cekeu__kzda = pd.core.computation.ops.Op.__str__
    nyr__kevjm = pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
    try:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            _rewrite_membership_op)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            _maybe_evaluate_binop)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = (
            visit_Attribute)
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = lambda self, left, right: (left, right)
        pd.core.computation.ops.Term.__str__ = __str__
        pd.core.computation.ops.MathCall.__str__ = math__str__
        pd.core.computation.ops.Op.__str__ = op__str__
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        nuk__gtbe = pd.core.computation.expr.Expr(expr, env=env)
        lum__ixll = str(nuk__gtbe)
    except pd.core.computation.ops.UndefinedVariableError as bfy__dcxr:
        if not is_overload_none(index_name) and get_overload_const_str(
            index_name) == bfy__dcxr.args[0].split("'")[1]:
            raise BodoError(
                "df.query(): Refering to named index ('{}') by name is not supported"
                .format(get_overload_const_str(index_name)))
        else:
            raise BodoError(f'df.query(): undefined variable, {bfy__dcxr}')
    finally:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            kzrma__kqi)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            ibxn__vmweb)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = nruf__fghj
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = uvy__dsea
        pd.core.computation.ops.Term.__str__ = qjybe__oue
        pd.core.computation.ops.MathCall.__str__ = xjozv__rctj
        pd.core.computation.ops.Op.__str__ = cekeu__kzda
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (
            nyr__kevjm)
    alqu__eiza = pd.core.computation.parsing.clean_column_name
    tlo__hvbe.update({ebc__koy: alqu__eiza(ebc__koy) for ebc__koy in
        columns if alqu__eiza(ebc__koy) in nuk__gtbe.names})
    return nuk__gtbe, lum__ixll, tlo__hvbe


class DataFrameTupleIterator(types.SimpleIteratorType):

    def __init__(self, col_names, arr_typs):
        self.array_types = arr_typs
        self.col_names = col_names
        qrh__ujw = ['{}={}'.format(col_names[i], arr_typs[i]) for i in
            range(len(col_names))]
        name = 'itertuples({})'.format(','.join(qrh__ujw))
        cbp__eshxu = namedtuple('Pandas', col_names)
        qcq__ifmne = types.NamedTuple([_get_series_dtype(a) for a in
            arr_typs], cbp__eshxu)
        super(DataFrameTupleIterator, self).__init__(name, qcq__ifmne)


def _get_series_dtype(arr_typ):
    if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
        return pd_timestamp_type
    return arr_typ.dtype


def get_itertuples():
    pass


@infer_global(get_itertuples)
class TypeIterTuples(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) % 2 == 0, 'name and column pairs expected'
        col_names = [a.literal_value for a in args[:len(args) // 2]]
        vgsq__xgor = [if_series_to_array_type(a) for a in args[len(args) // 2:]
            ]
        assert 'Index' not in col_names[0]
        col_names = ['Index'] + col_names
        vgsq__xgor = [types.Array(types.int64, 1, 'C')] + vgsq__xgor
        ekd__xsc = DataFrameTupleIterator(col_names, vgsq__xgor)
        return ekd__xsc(*args)


@register_model(DataFrameTupleIterator)
class DataFrameTupleIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        vikr__gar = [('index', types.EphemeralPointer(types.uintp))] + [(
            'array{}'.format(i), arr) for i, arr in enumerate(fe_type.
            array_types[1:])]
        super(DataFrameTupleIteratorModel, self).__init__(dmm, fe_type,
            vikr__gar)

    def from_return(self, builder, value):
        return value


@lower_builtin(get_itertuples, types.VarArg(types.Any))
def get_itertuples_impl(context, builder, sig, args):
    rhiq__eall = args[len(args) // 2:]
    jrbd__vfw = sig.args[len(sig.args) // 2:]
    rtka__wrtbh = context.make_helper(builder, sig.return_type)
    qcd__lfa = context.get_constant(types.intp, 0)
    cjryb__ymkrn = cgutils.alloca_once_value(builder, qcd__lfa)
    rtka__wrtbh.index = cjryb__ymkrn
    for i, arr in enumerate(rhiq__eall):
        setattr(rtka__wrtbh, 'array{}'.format(i), arr)
    for arr, arr_typ in zip(rhiq__eall, jrbd__vfw):
        context.nrt.incref(builder, arr_typ, arr)
    res = rtka__wrtbh._getvalue()
    return impl_ret_new_ref(context, builder, sig.return_type, res)


@lower_builtin('getiter', DataFrameTupleIterator)
def getiter_itertuples(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', DataFrameTupleIterator)
@iternext_impl(RefType.UNTRACKED)
def iternext_itertuples(context, builder, sig, args, result):
    fhpl__fvb, = sig.args
    qiqk__caar, = args
    rtka__wrtbh = context.make_helper(builder, fhpl__fvb, value=qiqk__caar)
    vwngx__dlh = signature(types.intp, fhpl__fvb.array_types[1])
    kjww__glk = context.compile_internal(builder, lambda a: len(a),
        vwngx__dlh, [rtka__wrtbh.array0])
    index = builder.load(rtka__wrtbh.index)
    arjz__jgd = builder.icmp(lc.ICMP_SLT, index, kjww__glk)
    result.set_valid(arjz__jgd)
    with builder.if_then(arjz__jgd):
        values = [index]
        for i, arr_typ in enumerate(fhpl__fvb.array_types[1:]):
            fwkx__yqnf = getattr(rtka__wrtbh, 'array{}'.format(i))
            if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
                sqv__njps = signature(pd_timestamp_type, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: bodo.
                    hiframes.pd_timestamp_ext.
                    convert_datetime64_to_timestamp(np.int64(a[i])),
                    sqv__njps, [fwkx__yqnf, index])
            else:
                sqv__njps = signature(arr_typ.dtype, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: a[i],
                    sqv__njps, [fwkx__yqnf, index])
            values.append(val)
        value = context.make_tuple(builder, fhpl__fvb.yield_type, values)
        result.yield_(value)
        emfk__uwyp = cgutils.increment_index(builder, index)
        builder.store(emfk__uwyp, rtka__wrtbh.index)


def _analyze_op_pair_first(self, scope, equiv_set, expr, lhs):
    typ = self.typemap[expr.value.name].first_type
    if not isinstance(typ, types.NamedTuple):
        return None
    lhs = ir.Var(scope, mk_unique_var('tuple_var'), expr.loc)
    self.typemap[lhs.name] = typ
    rhs = ir.Expr.pair_first(expr.value, expr.loc)
    zvbut__yjah = ir.Assign(rhs, lhs, expr.loc)
    wyw__vgn = lhs
    gdmr__ilh = []
    hjofh__tql = []
    udeh__gjrdc = typ.count
    for i in range(udeh__gjrdc):
        kxovl__zyim = ir.Var(wyw__vgn.scope, mk_unique_var('{}_size{}'.
            format(wyw__vgn.name, i)), wyw__vgn.loc)
        ekse__xgmjs = ir.Expr.static_getitem(lhs, i, None, wyw__vgn.loc)
        self.calltypes[ekse__xgmjs] = None
        gdmr__ilh.append(ir.Assign(ekse__xgmjs, kxovl__zyim, wyw__vgn.loc))
        self._define(equiv_set, kxovl__zyim, types.intp, ekse__xgmjs)
        hjofh__tql.append(kxovl__zyim)
    nxvb__sudj = tuple(hjofh__tql)
    return numba.parfors.array_analysis.ArrayAnalysis.AnalyzeResult(shape=
        nxvb__sudj, pre=[zvbut__yjah] + gdmr__ilh)


numba.parfors.array_analysis.ArrayAnalysis._analyze_op_pair_first = (
    _analyze_op_pair_first)
