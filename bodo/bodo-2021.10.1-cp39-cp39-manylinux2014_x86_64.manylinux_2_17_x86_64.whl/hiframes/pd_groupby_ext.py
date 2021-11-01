"""Support for Pandas Groupby operations
"""
import operator
from enum import Enum
import numba
import numpy as np
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.core.registry import CPUDispatcher
from numba.core.typing.templates import AbstractTemplate, AttributeTemplate, bound_function, infer_global, signature
from numba.extending import infer, infer_getattr, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_method, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import NumericIndexType, RangeIndexType
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_table, delete_table_decref_arrays, get_groupby_labels, get_shuffle_info, info_from_table, info_to_array, reverse_shuffle_table, shuffle_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.decimal_arr_ext import Decimal128Type
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.transform import gen_const_tup, get_call_expr_arg, get_const_func_output_type
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, dtype_to_array_type, get_index_data_arr_types, get_index_name_types, get_literal_value, get_overload_const_func, get_overload_const_list, get_overload_const_str, get_overload_constant_dict, get_udf_error_msg, get_udf_out_arr_type, is_dtype_nullable, is_literal_type, is_overload_constant_bool, is_overload_constant_dict, is_overload_constant_list, is_overload_constant_str, is_overload_none, is_overload_true, list_cumulative, raise_bodo_error, raise_const_error
from bodo.utils.utils import dt_err, is_expr


class DataFrameGroupByType(types.Type):

    def __init__(self, df_type, keys, selection, as_index, dropna=True,
        explicit_select=False, series_select=False):
        self.df_type = df_type
        self.keys = keys
        self.selection = selection
        self.as_index = as_index
        self.dropna = dropna
        self.explicit_select = explicit_select
        self.series_select = series_select
        super(DataFrameGroupByType, self).__init__(name=
            f'DataFrameGroupBy({df_type}, {keys}, {selection}, {as_index}, {dropna}, {explicit_select}, {series_select})'
            )

    def copy(self):
        return DataFrameGroupByType(self.df_type, self.keys, self.selection,
            self.as_index, self.dropna, self.explicit_select, self.
            series_select)


@register_model(DataFrameGroupByType)
class GroupbyModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        hbok__lwqb = [('obj', fe_type.df_type)]
        super(GroupbyModel, self).__init__(dmm, fe_type, hbok__lwqb)


make_attribute_wrapper(DataFrameGroupByType, 'obj', 'obj')


def validate_udf(func_name, func):
    if not isinstance(func, (types.functions.MakeFunctionLiteral, bodo.
        utils.typing.FunctionLiteral, types.Dispatcher, CPUDispatcher)):
        raise_const_error(
            f"Groupby.{func_name}: 'func' must be user defined function")


@intrinsic
def init_groupby(typingctx, obj_type, by_type, as_index_type=None,
    dropna_type=None):

    def codegen(context, builder, signature, args):
        sfrzq__zna = args[0]
        qlxd__rtm = signature.return_type
        xfwgy__ajk = cgutils.create_struct_proxy(qlxd__rtm)(context, builder)
        xfwgy__ajk.obj = sfrzq__zna
        context.nrt.incref(builder, signature.args[0], sfrzq__zna)
        return xfwgy__ajk._getvalue()
    if is_overload_constant_list(by_type):
        keys = tuple(get_overload_const_list(by_type))
    elif is_literal_type(by_type):
        keys = get_literal_value(by_type),
    else:
        assert False, 'Reached unreachable code in init_groupby; there is an validate_groupby_spec'
    selection = list(obj_type.columns)
    for fqc__bxvi in keys:
        selection.remove(fqc__bxvi)
    if is_overload_constant_bool(as_index_type):
        as_index = is_overload_true(as_index_type)
    else:
        as_index = True
    if is_overload_constant_bool(dropna_type):
        dropna = is_overload_true(dropna_type)
    else:
        dropna = True
    qlxd__rtm = DataFrameGroupByType(obj_type, keys, tuple(selection),
        as_index, dropna, False)
    return qlxd__rtm(obj_type, by_type, as_index_type, dropna_type), codegen


@lower_builtin('groupby.count', types.VarArg(types.Any))
@lower_builtin('groupby.size', types.VarArg(types.Any))
@lower_builtin('groupby.apply', types.VarArg(types.Any))
def lower_groupby_count_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


@infer
class StaticGetItemDataFrameGroupBy(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        grpby, reeup__dvdtk = args
        if isinstance(grpby, DataFrameGroupByType):
            series_select = False
            if isinstance(reeup__dvdtk, (tuple, list)):
                if len(set(reeup__dvdtk).difference(set(grpby.df_type.columns))
                    ) > 0:
                    raise_const_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(set(reeup__dvdtk).difference(set(grpby.
                        df_type.columns))))
                selection = reeup__dvdtk
            else:
                if reeup__dvdtk not in grpby.df_type.columns:
                    raise_const_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(reeup__dvdtk))
                selection = reeup__dvdtk,
                series_select = True
            hsrlh__monhn = DataFrameGroupByType(grpby.df_type, grpby.keys,
                selection, grpby.as_index, grpby.dropna, True, series_select)
            return signature(hsrlh__monhn, *args)


@infer_global(operator.getitem)
class GetItemDataFrameGroupBy(AbstractTemplate):

    def generic(self, args, kws):
        grpby, reeup__dvdtk = args
        if isinstance(grpby, DataFrameGroupByType) and is_literal_type(
            reeup__dvdtk):
            hsrlh__monhn = StaticGetItemDataFrameGroupBy.generic(self, (
                grpby, get_literal_value(reeup__dvdtk)), {}).return_type
            return signature(hsrlh__monhn, *args)


@lower_builtin('static_getitem', DataFrameGroupByType, types.Any)
@lower_builtin(operator.getitem, DataFrameGroupByType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


def get_groupby_output_dtype(arr_type, func_name, index_type=None):
    etj__ypdkj = arr_type == ArrayItemArrayType(string_array_type)
    psox__xjchb = arr_type.dtype
    if isinstance(psox__xjchb, bodo.hiframes.datetime_timedelta_ext.
        DatetimeTimeDeltaType):
        raise BodoError(
            f"""column type of {psox__xjchb} is not supported in groupby built-in function {func_name}.
{dt_err}"""
            )
    if func_name == 'median' and not isinstance(psox__xjchb, (
        Decimal128Type, types.Float, types.Integer)):
        return (None,
            'For median, only column of integer, float or Decimal type are allowed'
            )
    if func_name in ('first', 'last', 'sum', 'prod', 'min', 'max', 'count',
        'nunique') and isinstance(arr_type, (TupleArrayType,
        ArrayItemArrayType)):
        return (None,
            f'column type of list/tuple of {psox__xjchb} is not supported in groupby built-in function {func_name}'
            )
    if func_name in {'median', 'mean', 'var', 'std'} and isinstance(psox__xjchb
        , (Decimal128Type, types.Integer, types.Float)):
        return dtype_to_array_type(types.float64), 'ok'
    if not isinstance(psox__xjchb, (types.Integer, types.Float, types.Boolean)
        ):
        if etj__ypdkj or psox__xjchb == types.unicode_type:
            if func_name not in {'count', 'nunique', 'min', 'max', 'sum',
                'first', 'last'}:
                return (None,
                    f'column type of strings or list of strings is not supported in groupby built-in function {func_name}'
                    )
        else:
            if isinstance(psox__xjchb, bodo.PDCategoricalDtype):
                if func_name in ('min', 'max') and not psox__xjchb.ordered:
                    return (None,
                        f'categorical column must be ordered in groupby built-in function {func_name}'
                        )
            if func_name not in {'count', 'nunique', 'min', 'max', 'first',
                'last'}:
                return (None,
                    f'column type of {psox__xjchb} is not supported in groupby built-in function {func_name}'
                    )
    if isinstance(psox__xjchb, types.Boolean) and func_name in {'cumsum',
        'sum', 'mean', 'std', 'var'}:
        return (None,
            f'groupby built-in functions {func_name} does not support boolean column'
            )
    if func_name in {'idxmin', 'idxmax'}:
        return dtype_to_array_type(get_index_data_arr_types(index_type)[0].
            dtype), 'ok'
    if func_name in {'count', 'nunique'}:
        return dtype_to_array_type(types.int64), 'ok'
    else:
        return arr_type, 'ok'


def get_pivot_output_dtype(arr_type, func_name, index_type=None):
    psox__xjchb = arr_type.dtype
    if func_name in {'count'}:
        return IntDtype(types.int64)
    if func_name in {'sum', 'prod', 'min', 'max'}:
        if func_name in {'sum', 'prod'} and not isinstance(psox__xjchb, (
            types.Integer, types.Float)):
            raise BodoError(
                'pivot_table(): sum and prod operations require integer or float input'
                )
        if isinstance(psox__xjchb, types.Integer):
            return IntDtype(psox__xjchb)
        return psox__xjchb
    if func_name in {'mean', 'var', 'std'}:
        return types.float64
    raise BodoError('invalid pivot operation')


def check_args_kwargs(func_name, len_args, args, kws):
    if len(kws) > 0:
        xws__kflrt = list(kws.keys())[0]
        raise BodoError(
            f"Groupby.{func_name}() got an unexpected keyword argument '{xws__kflrt}'."
            )
    elif len(args) > len_args:
        raise BodoError(
            f'Groupby.{func_name}() takes {len_args + 1} positional argument but {len(args)} were given.'
            )


class ColumnType(Enum):
    KeyColumn = 0
    NumericalColumn = 1
    NonNumericalColumn = 2


def get_keys_not_as_index(grp, out_columns, out_data, out_column_type,
    multi_level_names=False):
    for fqc__bxvi in grp.keys:
        if multi_level_names:
            kdkgy__qoy = fqc__bxvi, ''
        else:
            kdkgy__qoy = fqc__bxvi
        ftck__qnbt = grp.df_type.columns.index(fqc__bxvi)
        data = grp.df_type.data[ftck__qnbt]
        out_columns.append(kdkgy__qoy)
        out_data.append(data)
        out_column_type.append(ColumnType.KeyColumn.value)


def get_agg_typ(grp, args, func_name, typing_context, target_context, func=
    None, kws=None):
    index = RangeIndexType(types.none)
    out_data = []
    out_columns = []
    out_column_type = []
    if not grp.as_index:
        get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
    elif len(grp.keys) > 1:
        ihhb__esjug = tuple(grp.df_type.columns.index(grp.keys[ebl__unuys]) for
            ebl__unuys in range(len(grp.keys)))
        hpost__ucaaf = tuple(grp.df_type.data[ftck__qnbt] for ftck__qnbt in
            ihhb__esjug)
        index = MultiIndexType(hpost__ucaaf, tuple(types.StringLiteral(
            fqc__bxvi) for fqc__bxvi in grp.keys))
    else:
        ftck__qnbt = grp.df_type.columns.index(grp.keys[0])
        index = bodo.hiframes.pd_index_ext.array_type_to_index(grp.df_type.
            data[ftck__qnbt], types.StringLiteral(grp.keys[0]))
    pgyr__pev = {}
    xsh__rcr = []
    if func_name in ('size', 'count'):
        kws = dict(kws) if kws else {}
        check_args_kwargs(func_name, 0, args, kws)
    if func_name == 'size':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('size')
        pgyr__pev[None, 'size'] = 'size'
    else:
        for sxmom__bxce in grp.selection:
            ftck__qnbt = grp.df_type.columns.index(sxmom__bxce)
            data = grp.df_type.data[ftck__qnbt]
            ypvwo__nve = ColumnType.NonNumericalColumn.value
            if isinstance(data, (types.Array, IntegerArrayType)
                ) and isinstance(data.dtype, (types.Integer, types.Float)):
                ypvwo__nve = ColumnType.NumericalColumn.value
            if func_name == 'agg':
                try:
                    rchn__sdgi = SeriesType(data.dtype, data, None, string_type
                        )
                    gyaou__vgi = get_const_func_output_type(func, (
                        rchn__sdgi,), {}, typing_context, target_context)
                    if gyaou__vgi != ArrayItemArrayType(string_array_type):
                        gyaou__vgi = dtype_to_array_type(gyaou__vgi)
                    err_msg = 'ok'
                except:
                    raise_bodo_error(
                        'Groupy.agg()/Groupy.aggregate(): column {col} of type {type} is unsupported/not a valid input type for user defined function'
                        .format(col=sxmom__bxce, type=data.dtype))
            else:
                if func_name in ('first', 'last', 'min', 'max'):
                    kws = dict(kws) if kws else {}
                    fhs__chvod = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', False)
                    ieda__mun = args[1] if len(args) > 1 else kws.pop(
                        'min_count', -1)
                    ftd__pvs = dict(numeric_only=fhs__chvod, min_count=
                        ieda__mun)
                    kzz__hqzo = dict(numeric_only=False, min_count=-1)
                    check_unsupported_args(f'Groupby.{func_name}', ftd__pvs,
                        kzz__hqzo)
                elif func_name in ('sum', 'prod'):
                    kws = dict(kws) if kws else {}
                    fhs__chvod = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    ieda__mun = args[1] if len(args) > 1 else kws.pop(
                        'min_count', 0)
                    ftd__pvs = dict(numeric_only=fhs__chvod, min_count=
                        ieda__mun)
                    kzz__hqzo = dict(numeric_only=True, min_count=0)
                    check_unsupported_args(f'Groupby.{func_name}', ftd__pvs,
                        kzz__hqzo)
                elif func_name in ('mean', 'median'):
                    kws = dict(kws) if kws else {}
                    fhs__chvod = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    ftd__pvs = dict(numeric_only=fhs__chvod)
                    kzz__hqzo = dict(numeric_only=True)
                    check_unsupported_args(f'Groupby.{func_name}', ftd__pvs,
                        kzz__hqzo)
                elif func_name in ('idxmin', 'idxmax'):
                    kws = dict(kws) if kws else {}
                    omg__qcqs = args[0] if len(args) > 0 else kws.pop('axis', 0
                        )
                    igkgx__gixn = args[1] if len(args) > 1 else kws.pop(
                        'skipna', True)
                    ftd__pvs = dict(axis=omg__qcqs, skipna=igkgx__gixn)
                    kzz__hqzo = dict(axis=0, skipna=True)
                    check_unsupported_args(f'Groupby.{func_name}', ftd__pvs,
                        kzz__hqzo)
                elif func_name in ('var', 'std'):
                    kws = dict(kws) if kws else {}
                    ihi__ehj = args[0] if len(args) > 0 else kws.pop('ddof', 1)
                    ftd__pvs = dict(ddof=ihi__ehj)
                    kzz__hqzo = dict(ddof=1)
                    check_unsupported_args(f'Groupby.{func_name}', ftd__pvs,
                        kzz__hqzo)
                elif func_name == 'nunique':
                    kws = dict(kws) if kws else {}
                    dropna = args[0] if len(args) > 0 else kws.pop('dropna', 1)
                    check_args_kwargs(func_name, 1, args, kws)
                gyaou__vgi, err_msg = get_groupby_output_dtype(data,
                    func_name, grp.df_type.index)
            if err_msg == 'ok':
                wtly__jiuu = gyaou__vgi
                out_data.append(wtly__jiuu)
                out_columns.append(sxmom__bxce)
                if func_name == 'agg':
                    xuq__jpdhv = bodo.ir.aggregate._get_udf_name(bodo.ir.
                        aggregate._get_const_agg_func(func, None))
                    pgyr__pev[sxmom__bxce, xuq__jpdhv] = sxmom__bxce
                else:
                    pgyr__pev[sxmom__bxce, func_name] = sxmom__bxce
                out_column_type.append(ypvwo__nve)
            else:
                xsh__rcr.append(err_msg)
    if func_name == 'sum':
        dbdz__jxg = any([(gygi__fyps == ColumnType.NumericalColumn.value) for
            gygi__fyps in out_column_type])
        if dbdz__jxg:
            out_data = [gygi__fyps for gygi__fyps, kzaly__pnp in zip(
                out_data, out_column_type) if kzaly__pnp != ColumnType.
                NonNumericalColumn.value]
            out_columns = [gygi__fyps for gygi__fyps, kzaly__pnp in zip(
                out_columns, out_column_type) if kzaly__pnp != ColumnType.
                NonNumericalColumn.value]
            pgyr__pev = {}
            for sxmom__bxce in out_columns:
                if grp.as_index is False and sxmom__bxce in grp.keys:
                    continue
                pgyr__pev[sxmom__bxce, func_name] = sxmom__bxce
    elpi__out = len(xsh__rcr)
    if len(out_data) == 0:
        if elpi__out == 0:
            raise BodoError('No columns in output.')
        else:
            raise BodoError(
                'No columns in output. {} column{} dropped for following reasons: {}'
                .format(elpi__out, ' was' if elpi__out == 1 else 's were',
                ','.join(xsh__rcr)))
    chr__uzwt = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if (len(grp.selection) == 1 and grp.series_select and grp.as_index or 
        func_name == 'size' and grp.as_index):
        if isinstance(out_data[0], IntegerArrayType):
            csfil__dkjie = IntDtype(out_data[0].dtype)
        else:
            csfil__dkjie = out_data[0].dtype
        gpw__lmuy = types.none if func_name == 'size' else types.StringLiteral(
            grp.selection[0])
        chr__uzwt = SeriesType(csfil__dkjie, index=index, name_typ=gpw__lmuy)
    return signature(chr__uzwt, *args), pgyr__pev


def get_agg_funcname_and_outtyp(grp, col, f_val, typing_context, target_context
    ):
    popk__zkh = True
    if isinstance(f_val, str):
        popk__zkh = False
        psza__anufk = f_val
    elif is_overload_constant_str(f_val):
        popk__zkh = False
        psza__anufk = get_overload_const_str(f_val)
    elif bodo.utils.typing.is_builtin_function(f_val):
        popk__zkh = False
        psza__anufk = bodo.utils.typing.get_builtin_function_name(f_val)
    if not popk__zkh:
        if psza__anufk not in bodo.ir.aggregate.supported_agg_funcs[:-1]:
            raise BodoError(f'unsupported aggregate function {psza__anufk}')
        hsrlh__monhn = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(hsrlh__monhn, (), psza__anufk, typing_context,
            target_context)[0].return_type
    else:
        if is_expr(f_val, 'make_function'):
            udq__cmdf = types.functions.MakeFunctionLiteral(f_val)
        else:
            udq__cmdf = f_val
        validate_udf('agg', udq__cmdf)
        func = get_overload_const_func(udq__cmdf, None)
        gefi__bsol = func.code if hasattr(func, 'code') else func.__code__
        psza__anufk = gefi__bsol.co_name
        hsrlh__monhn = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(hsrlh__monhn, (), 'agg', typing_context,
            target_context, udq__cmdf)[0].return_type
    return psza__anufk, out_tp


def resolve_agg(grp, args, kws, typing_context, target_context):
    func = get_call_expr_arg('agg', args, dict(kws), 0, 'func', default=
        types.none)
    xcjl__usg = kws and all(isinstance(vwu__yes, types.Tuple) and len(
        vwu__yes) == 2 for vwu__yes in kws.values())
    if is_overload_none(func) and not xcjl__usg:
        raise_bodo_error("Groupby.agg()/aggregate(): Must provide 'func'")
    if len(args) > 1 or kws and not xcjl__usg:
        raise_bodo_error(
            'Groupby.agg()/aggregate(): passing extra arguments to functions not supported yet.'
            )
    hbm__xpbof = False

    def _append_out_type(grp, out_data, out_tp):
        if grp.as_index is False:
            out_data.append(out_tp.data[len(grp.keys)])
        else:
            out_data.append(out_tp.data)
    if xcjl__usg or is_overload_constant_dict(func):
        if xcjl__usg:
            swlay__qxkx = [get_literal_value(ulzex__bnkj) for ulzex__bnkj,
                jrw__kkeds in kws.values()]
            relv__zcmi = [get_literal_value(fzkv__phkt) for jrw__kkeds,
                fzkv__phkt in kws.values()]
        else:
            nyjd__latr = get_overload_constant_dict(func)
            swlay__qxkx = tuple(nyjd__latr.keys())
            relv__zcmi = tuple(nyjd__latr.values())
        if any(sxmom__bxce not in grp.selection and sxmom__bxce not in grp.
            keys for sxmom__bxce in swlay__qxkx):
            raise_const_error(
                f'Selected column names {swlay__qxkx} not all available in dataframe column names {grp.selection}'
                )
        multi_level_names = any(isinstance(f_val, (tuple, list)) for f_val in
            relv__zcmi)
        if xcjl__usg and multi_level_names:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): cannot pass multiple functions in a single pd.NamedAgg()'
                )
        pgyr__pev = {}
        out_columns = []
        out_data = []
        out_column_type = []
        akzwb__uluy = []
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data,
                out_column_type, multi_level_names=multi_level_names)
        for sjljb__rhet, f_val in zip(swlay__qxkx, relv__zcmi):
            if isinstance(f_val, (tuple, list)):
                mqsn__sazia = 0
                for udq__cmdf in f_val:
                    psza__anufk, out_tp = get_agg_funcname_and_outtyp(grp,
                        sjljb__rhet, udq__cmdf, typing_context, target_context)
                    hbm__xpbof = psza__anufk in list_cumulative
                    if psza__anufk == '<lambda>' and len(f_val) > 1:
                        psza__anufk = '<lambda_' + str(mqsn__sazia) + '>'
                        mqsn__sazia += 1
                    out_columns.append((sjljb__rhet, psza__anufk))
                    pgyr__pev[sjljb__rhet, psza__anufk
                        ] = sjljb__rhet, psza__anufk
                    _append_out_type(grp, out_data, out_tp)
            else:
                psza__anufk, out_tp = get_agg_funcname_and_outtyp(grp,
                    sjljb__rhet, f_val, typing_context, target_context)
                hbm__xpbof = psza__anufk in list_cumulative
                if multi_level_names:
                    out_columns.append((sjljb__rhet, psza__anufk))
                    pgyr__pev[sjljb__rhet, psza__anufk
                        ] = sjljb__rhet, psza__anufk
                elif not xcjl__usg:
                    out_columns.append(sjljb__rhet)
                    pgyr__pev[sjljb__rhet, psza__anufk] = sjljb__rhet
                elif xcjl__usg:
                    akzwb__uluy.append(psza__anufk)
                _append_out_type(grp, out_data, out_tp)
        if xcjl__usg:
            for ebl__unuys, can__czprg in enumerate(kws.keys()):
                out_columns.append(can__czprg)
                pgyr__pev[swlay__qxkx[ebl__unuys], akzwb__uluy[ebl__unuys]
                    ] = can__czprg
        if hbm__xpbof:
            index = grp.df_type.index
        else:
            index = out_tp.index
        chr__uzwt = DataFrameType(tuple(out_data), index, tuple(out_columns))
        return signature(chr__uzwt, *args), pgyr__pev
    if isinstance(func, types.BaseTuple) and not isinstance(func, types.
        LiteralStrKeyDict):
        if not (len(grp.selection) == 1 and grp.explicit_select):
            raise_bodo_error(
                'Groupby.agg()/aggregate(): must select exactly one column when more than one functions supplied'
                )
        assert len(func) > 0
        out_data = []
        out_columns = []
        out_column_type = []
        mqsn__sazia = 0
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
        pgyr__pev = {}
        fbgh__koh = grp.selection[0]
        for f_val in func.types:
            psza__anufk, out_tp = get_agg_funcname_and_outtyp(grp,
                fbgh__koh, f_val, typing_context, target_context)
            hbm__xpbof = psza__anufk in list_cumulative
            if psza__anufk == '<lambda>':
                psza__anufk = '<lambda_' + str(mqsn__sazia) + '>'
                mqsn__sazia += 1
            out_columns.append(psza__anufk)
            pgyr__pev[fbgh__koh, psza__anufk] = psza__anufk
            _append_out_type(grp, out_data, out_tp)
        if hbm__xpbof:
            index = grp.df_type.index
        else:
            index = out_tp.index
        chr__uzwt = DataFrameType(tuple(out_data), index, tuple(out_columns))
        return signature(chr__uzwt, *args), pgyr__pev
    psza__anufk = ''
    if types.unliteral(func) == types.unicode_type:
        psza__anufk = get_overload_const_str(func)
    if bodo.utils.typing.is_builtin_function(func):
        psza__anufk = bodo.utils.typing.get_builtin_function_name(func)
    if psza__anufk:
        args = args[1:]
        kws.pop('func', None)
        return get_agg_typ(grp, args, psza__anufk, typing_context, kws)
    validate_udf('agg', func)
    return get_agg_typ(grp, args, 'agg', typing_context, target_context, func)


def resolve_transformative(grp, args, kws, msg, name_operation):
    index = grp.df_type.index
    out_columns = []
    out_data = []
    if name_operation in list_cumulative:
        kws = dict(kws) if kws else {}
        omg__qcqs = args[0] if len(args) > 0 else kws.pop('axis', 0)
        fhs__chvod = args[1] if len(args) > 1 else kws.pop('numeric_only', 
            False)
        igkgx__gixn = args[2] if len(args) > 2 else kws.pop('skipna', 1)
        ftd__pvs = dict(axis=omg__qcqs, numeric_only=fhs__chvod)
        kzz__hqzo = dict(axis=0, numeric_only=False)
        check_unsupported_args(f'Groupby.{name_operation}', ftd__pvs, kzz__hqzo
            )
        check_args_kwargs(name_operation, 3, args, kws)
    elif name_operation == 'shift':
        hvdk__eae = args[0] if len(args) > 0 else kws.pop('periods', 1)
        dlg__anfb = args[1] if len(args) > 1 else kws.pop('freq', None)
        omg__qcqs = args[2] if len(args) > 2 else kws.pop('axis', 0)
        tggeu__yfjzv = args[3] if len(args) > 3 else kws.pop('fill_value', None
            )
        ftd__pvs = dict(freq=dlg__anfb, axis=omg__qcqs, fill_value=tggeu__yfjzv
            )
        kzz__hqzo = dict(freq=None, axis=0, fill_value=None)
        check_unsupported_args(f'Groupby.{name_operation}', ftd__pvs, kzz__hqzo
            )
        check_args_kwargs(name_operation, 4, args, kws)
    elif name_operation == 'transform':
        kws = dict(kws)
        mnmd__rpwom = args[0] if len(args) > 0 else kws.pop('func', None)
        bfh__bnp = kws.pop('engine', None)
        yyq__lfbbl = kws.pop('engine_kwargs', None)
        ftd__pvs = dict(engine=bfh__bnp, engine_kwargs=yyq__lfbbl)
        kzz__hqzo = dict(engine=None, engine_kwargs=None)
        check_unsupported_args(f'Groupby.transform', ftd__pvs, kzz__hqzo)
    pgyr__pev = {}
    for sxmom__bxce in grp.selection:
        out_columns.append(sxmom__bxce)
        pgyr__pev[sxmom__bxce, name_operation] = sxmom__bxce
        ftck__qnbt = grp.df_type.columns.index(sxmom__bxce)
        data = grp.df_type.data[ftck__qnbt]
        if name_operation == 'cumprod':
            if not isinstance(data.dtype, (types.Integer, types.Float)):
                raise BodoError(msg)
        if name_operation == 'cumsum':
            if data.dtype != types.unicode_type and data != ArrayItemArrayType(
                string_array_type) and not isinstance(data.dtype, (types.
                Integer, types.Float)):
                raise BodoError(msg)
        if name_operation in ('cummin', 'cummax'):
            if not isinstance(data.dtype, types.Integer
                ) and not is_dtype_nullable(data.dtype):
                raise BodoError(msg)
        if name_operation == 'shift':
            if isinstance(data, (TupleArrayType, ArrayItemArrayType)):
                raise BodoError(msg)
            if isinstance(data.dtype, bodo.hiframes.datetime_timedelta_ext.
                DatetimeTimeDeltaType):
                raise BodoError(
                    f"""column type of {data.dtype} is not supported in groupby built-in function shift.
{dt_err}"""
                    )
        if name_operation == 'transform':
            gyaou__vgi, err_msg = get_groupby_output_dtype(data,
                get_literal_value(mnmd__rpwom), grp.df_type.index)
            if err_msg == 'ok':
                data = gyaou__vgi
            else:
                raise BodoError(
                    f'column type of {data.dtype} is not supported by {args[0]} yet.\n'
                    )
        out_data.append(data)
    if len(out_data) == 0:
        raise BodoError('No columns in output.')
    chr__uzwt = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if len(grp.selection) == 1 and grp.series_select and grp.as_index:
        chr__uzwt = SeriesType(out_data[0].dtype, data=out_data[0], index=
            index, name_typ=types.StringLiteral(grp.selection[0]))
    return signature(chr__uzwt, *args), pgyr__pev


def resolve_gb(grp, args, kws, func_name, typing_context, target_context,
    err_msg=''):
    if func_name in set(list_cumulative) | {'shift', 'transform'}:
        return resolve_transformative(grp, args, kws, err_msg, func_name)
    elif func_name in {'agg', 'aggregate'}:
        return resolve_agg(grp, args, kws, typing_context, target_context)
    else:
        return get_agg_typ(grp, args, func_name, typing_context,
            target_context, kws=kws)


@infer_getattr
class DataframeGroupByAttribute(AttributeTemplate):
    key = DataFrameGroupByType

    @bound_function('groupby.agg', no_unliteral=True)
    def resolve_agg(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'agg', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.aggregate', no_unliteral=True)
    def resolve_aggregate(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'agg', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.sum', no_unliteral=True)
    def resolve_sum(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'sum', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.count', no_unliteral=True)
    def resolve_count(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'count', self.context, numba.core
            .registry.cpu_target.target_context)[0]

    @bound_function('groupby.nunique', no_unliteral=True)
    def resolve_nunique(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'nunique', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.median', no_unliteral=True)
    def resolve_median(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'median', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.mean', no_unliteral=True)
    def resolve_mean(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'mean', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.min', no_unliteral=True)
    def resolve_min(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'min', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.max', no_unliteral=True)
    def resolve_max(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'max', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.prod', no_unliteral=True)
    def resolve_prod(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'prod', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.var', no_unliteral=True)
    def resolve_var(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'var', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.std', no_unliteral=True)
    def resolve_std(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'std', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.first', no_unliteral=True)
    def resolve_first(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'first', self.context, numba.core
            .registry.cpu_target.target_context)[0]

    @bound_function('groupby.last', no_unliteral=True)
    def resolve_last(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'last', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.idxmin', no_unliteral=True)
    def resolve_idxmin(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'idxmin', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.idxmax', no_unliteral=True)
    def resolve_idxmax(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'idxmax', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.size', no_unliteral=True)
    def resolve_size(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'size', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.cumsum', no_unliteral=True)
    def resolve_cumsum(self, grp, args, kws):
        msg = (
            'Groupby.cumsum() only supports columns of types integer, float, string or liststring'
            )
        return resolve_gb(grp, args, kws, 'cumsum', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cumprod', no_unliteral=True)
    def resolve_cumprod(self, grp, args, kws):
        msg = (
            'Groupby.cumprod() only supports columns of types integer and float'
            )
        return resolve_gb(grp, args, kws, 'cumprod', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cummin', no_unliteral=True)
    def resolve_cummin(self, grp, args, kws):
        msg = (
            'Groupby.cummin() only supports columns of types integer, float, string, liststring, date, datetime or timedelta'
            )
        return resolve_gb(grp, args, kws, 'cummin', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cummax', no_unliteral=True)
    def resolve_cummax(self, grp, args, kws):
        msg = (
            'Groupby.cummax() only supports columns of types integer, float, string, liststring, date, datetime or timedelta'
            )
        return resolve_gb(grp, args, kws, 'cummax', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.shift', no_unliteral=True)
    def resolve_shift(self, grp, args, kws):
        msg = (
            'Column type of list/tuple is not supported in groupby built-in function shift'
            )
        return resolve_gb(grp, args, kws, 'shift', self.context, numba.core
            .registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.pipe', no_unliteral=True)
    def resolve_pipe(self, grp, args, kws):
        return resolve_obj_pipe(self, grp, args, kws, 'GroupBy')

    @bound_function('groupby.transform', no_unliteral=True)
    def resolve_transform(self, grp, args, kws):
        msg = (
            'Groupby.transform() only supports sum, count, min, max, mean, and std operations'
            )
        return resolve_gb(grp, args, kws, 'transform', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.apply', no_unliteral=True)
    def resolve_apply(self, grp, args, kws):
        kws = dict(kws)
        func = args[0] if len(args) > 0 else kws.pop('func', None)
        f_args = tuple(args[1:]) if len(args) > 0 else ()
        vrvoo__ode = _get_groupby_apply_udf_out_type(func, grp, f_args, kws,
            self.context, numba.core.registry.cpu_target.target_context)
        nlnku__uah = isinstance(vrvoo__ode, (SeriesType,
            HeterogeneousSeriesType)
            ) and vrvoo__ode.const_info is not None or not isinstance(
            vrvoo__ode, (SeriesType, DataFrameType))
        if nlnku__uah:
            out_data = []
            out_columns = []
            out_column_type = []
            if not grp.as_index:
                get_keys_not_as_index(grp, out_columns, out_data,
                    out_column_type)
                ooflj__dke = NumericIndexType(types.int64, types.none)
            elif len(grp.keys) > 1:
                ihhb__esjug = tuple(grp.df_type.columns.index(grp.keys[
                    ebl__unuys]) for ebl__unuys in range(len(grp.keys)))
                hpost__ucaaf = tuple(grp.df_type.data[ftck__qnbt] for
                    ftck__qnbt in ihhb__esjug)
                ooflj__dke = MultiIndexType(hpost__ucaaf, tuple(types.
                    literal(fqc__bxvi) for fqc__bxvi in grp.keys))
            else:
                ftck__qnbt = grp.df_type.columns.index(grp.keys[0])
                ooflj__dke = bodo.hiframes.pd_index_ext.array_type_to_index(grp
                    .df_type.data[ftck__qnbt], types.literal(grp.keys[0]))
            out_data = tuple(out_data)
            out_columns = tuple(out_columns)
        else:
            ldlpw__ush = tuple(grp.df_type.data[grp.df_type.columns.index(
                sxmom__bxce)] for sxmom__bxce in grp.keys)
            kgef__qbbg = tuple(types.literal(vwu__yes) for vwu__yes in grp.keys
                ) + get_index_name_types(vrvoo__ode.index)
            if not grp.as_index:
                ldlpw__ush = types.Array(types.int64, 1, 'C'),
                kgef__qbbg = (types.none,) + get_index_name_types(vrvoo__ode
                    .index)
            ooflj__dke = MultiIndexType(ldlpw__ush +
                get_index_data_arr_types(vrvoo__ode.index), kgef__qbbg)
        if nlnku__uah:
            if isinstance(vrvoo__ode, HeterogeneousSeriesType):
                jrw__kkeds, bsasp__yiu = vrvoo__ode.const_info
                ntcsu__bhby = tuple(dtype_to_array_type(umqw__esbw) for
                    umqw__esbw in vrvoo__ode.data.types)
                ezk__zzfq = DataFrameType(out_data + ntcsu__bhby,
                    ooflj__dke, out_columns + bsasp__yiu)
            elif isinstance(vrvoo__ode, SeriesType):
                ataz__niihn, bsasp__yiu = vrvoo__ode.const_info
                ntcsu__bhby = tuple(dtype_to_array_type(vrvoo__ode.dtype) for
                    jrw__kkeds in range(ataz__niihn))
                ezk__zzfq = DataFrameType(out_data + ntcsu__bhby,
                    ooflj__dke, out_columns + bsasp__yiu)
            else:
                aiw__yxb = get_udf_out_arr_type(vrvoo__ode)
                if not grp.as_index:
                    ezk__zzfq = DataFrameType(out_data + (aiw__yxb,),
                        ooflj__dke, out_columns + ('',))
                else:
                    ezk__zzfq = SeriesType(aiw__yxb.dtype, aiw__yxb,
                        ooflj__dke, None)
        elif isinstance(vrvoo__ode, SeriesType):
            ezk__zzfq = SeriesType(vrvoo__ode.dtype, vrvoo__ode.data,
                ooflj__dke, vrvoo__ode.name_typ)
        else:
            ezk__zzfq = DataFrameType(vrvoo__ode.data, ooflj__dke,
                vrvoo__ode.columns)
        ech__jlmq = gen_apply_pysig(len(f_args), kws.keys())
        aypmy__afe = (func, *f_args) + tuple(kws.values())
        return signature(ezk__zzfq, *aypmy__afe).replace(pysig=ech__jlmq)

    def generic_resolve(self, grpby, attr):
        if attr in groupby_unsupported or attr in ('rolling', 'value_counts'):
            return
        if attr not in grpby.df_type.columns:
            raise_const_error(
                f'groupby: invalid attribute {attr} (column not found in dataframe or unsupported function)'
                )
        return DataFrameGroupByType(grpby.df_type, grpby.keys, (attr,),
            grpby.as_index, grpby.dropna, True, True)


def _get_groupby_apply_udf_out_type(func, grp, f_args, kws, typing_context,
    target_context):
    xpes__juk = grp.df_type
    if grp.explicit_select:
        if len(grp.selection) == 1:
            sjljb__rhet = grp.selection[0]
            aiw__yxb = xpes__juk.data[xpes__juk.columns.index(sjljb__rhet)]
            tzcu__ryk = SeriesType(aiw__yxb.dtype, aiw__yxb, xpes__juk.
                index, types.literal(sjljb__rhet))
        else:
            sggnt__gsou = tuple(xpes__juk.data[xpes__juk.columns.index(
                sxmom__bxce)] for sxmom__bxce in grp.selection)
            tzcu__ryk = DataFrameType(sggnt__gsou, xpes__juk.index, tuple(
                grp.selection))
    else:
        tzcu__ryk = xpes__juk
    rzw__ibni = tzcu__ryk,
    rzw__ibni += tuple(f_args)
    try:
        vrvoo__ode = get_const_func_output_type(func, rzw__ibni, kws,
            typing_context, target_context)
    except Exception as gsqs__yom:
        raise_bodo_error(get_udf_error_msg('GroupBy.apply()', gsqs__yom),
            getattr(gsqs__yom, 'loc', None))
    return vrvoo__ode


def resolve_obj_pipe(self, grp, args, kws, obj_name):
    kws = dict(kws)
    func = args[0] if len(args) > 0 else kws.pop('func', None)
    f_args = tuple(args[1:]) if len(args) > 0 else ()
    rzw__ibni = (grp,) + f_args
    try:
        vrvoo__ode = get_const_func_output_type(func, rzw__ibni, kws, self.
            context, numba.core.registry.cpu_target.target_context, False)
    except Exception as gsqs__yom:
        raise_bodo_error(get_udf_error_msg(f'{obj_name}.pipe()', gsqs__yom),
            getattr(gsqs__yom, 'loc', None))
    ech__jlmq = gen_apply_pysig(len(f_args), kws.keys())
    aypmy__afe = (func, *f_args) + tuple(kws.values())
    return signature(vrvoo__ode, *aypmy__afe).replace(pysig=ech__jlmq)


def gen_apply_pysig(n_args, kws):
    uqt__oomme = ', '.join(f'arg{ebl__unuys}' for ebl__unuys in range(n_args))
    uqt__oomme = uqt__oomme + ', ' if uqt__oomme else ''
    cqi__tcp = ', '.join(f"{gekf__qfc} = ''" for gekf__qfc in kws)
    bue__ctj = f'def apply_stub(func, {uqt__oomme}{cqi__tcp}):\n'
    bue__ctj += '    pass\n'
    hkqvp__iybgy = {}
    exec(bue__ctj, {}, hkqvp__iybgy)
    bjktq__kgs = hkqvp__iybgy['apply_stub']
    return numba.core.utils.pysignature(bjktq__kgs)


def pivot_table_dummy(df, values, index, columns, aggfunc, _pivot_values):
    return 0


@infer_global(pivot_table_dummy)
class PivotTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df, values, index, columns, aggfunc, _pivot_values = args
        if not (is_overload_constant_str(values) and
            is_overload_constant_str(index) and is_overload_constant_str(
            columns)):
            raise BodoError(
                "pivot_table() only support string constants for 'values', 'index' and 'columns' arguments"
                )
        values = values.literal_value
        index = index.literal_value
        columns = columns.literal_value
        data = df.data[df.columns.index(values)]
        gyaou__vgi = get_pivot_output_dtype(data, aggfunc.literal_value)
        zegkt__iscy = dtype_to_array_type(gyaou__vgi)
        buq__iseev = _pivot_values.meta
        fkfcd__jurlg = len(buq__iseev)
        ftck__qnbt = df.columns.index(index)
        xosnp__qij = bodo.hiframes.pd_index_ext.array_type_to_index(df.data
            [ftck__qnbt], types.StringLiteral(index))
        kuyc__mfp = DataFrameType((zegkt__iscy,) * fkfcd__jurlg, xosnp__qij,
            tuple(buq__iseev))
        return signature(kuyc__mfp, *args)


PivotTyper._no_unliteral = True


@lower_builtin(pivot_table_dummy, types.VarArg(types.Any))
def lower_pivot_table_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def crosstab_dummy(index, columns, _pivot_values):
    return 0


@infer_global(crosstab_dummy)
class CrossTabTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        index, columns, _pivot_values = args
        zegkt__iscy = types.Array(types.int64, 1, 'C')
        buq__iseev = _pivot_values.meta
        fkfcd__jurlg = len(buq__iseev)
        xosnp__qij = bodo.hiframes.pd_index_ext.array_type_to_index(index.
            data, types.StringLiteral('index'))
        kuyc__mfp = DataFrameType((zegkt__iscy,) * fkfcd__jurlg, xosnp__qij,
            tuple(buq__iseev))
        return signature(kuyc__mfp, *args)


CrossTabTyper._no_unliteral = True


@lower_builtin(crosstab_dummy, types.VarArg(types.Any))
def lower_crosstab_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def get_group_indices(keys, dropna, _is_parallel):
    return np.arange(len(keys))


@overload(get_group_indices)
def get_group_indices_overload(keys, dropna, _is_parallel):
    bue__ctj = 'def impl(keys, dropna, _is_parallel):\n'
    bue__ctj += (
        "    ev = bodo.utils.tracing.Event('get_group_indices', _is_parallel)\n"
        )
    bue__ctj += '    info_list = [{}]\n'.format(', '.join(
        f'array_to_info(keys[{ebl__unuys}])' for ebl__unuys in range(len(
        keys.types))))
    bue__ctj += '    table = arr_info_list_to_table(info_list)\n'
    bue__ctj += '    group_labels = np.empty(len(keys[0]), np.int64)\n'
    bue__ctj += '    sort_idx = np.empty(len(keys[0]), np.int64)\n'
    bue__ctj += """    ngroups = get_groupby_labels(table, group_labels.ctypes, sort_idx.ctypes, dropna, _is_parallel)
"""
    bue__ctj += '    delete_table_decref_arrays(table)\n'
    bue__ctj += '    ev.finalize()\n'
    bue__ctj += '    return sort_idx, group_labels, ngroups\n'
    hkqvp__iybgy = {}
    exec(bue__ctj, {'bodo': bodo, 'np': np, 'get_groupby_labels':
        get_groupby_labels, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, hkqvp__iybgy
        )
    ugxc__bus = hkqvp__iybgy['impl']
    return ugxc__bus


@numba.njit(no_cpython_wrapper=True)
def generate_slices(labels, ngroups):
    ekoxv__shrig = len(labels)
    uca__rpyqg = np.zeros(ngroups, dtype=np.int64)
    nfpyn__kyz = np.zeros(ngroups, dtype=np.int64)
    vgw__dirmw = 0
    bvur__imd = 0
    for ebl__unuys in range(ekoxv__shrig):
        yruor__inbdp = labels[ebl__unuys]
        if yruor__inbdp < 0:
            vgw__dirmw += 1
        else:
            bvur__imd += 1
            if ebl__unuys == ekoxv__shrig - 1 or yruor__inbdp != labels[
                ebl__unuys + 1]:
                uca__rpyqg[yruor__inbdp] = vgw__dirmw
                nfpyn__kyz[yruor__inbdp] = vgw__dirmw + bvur__imd
                vgw__dirmw += bvur__imd
                bvur__imd = 0
    return uca__rpyqg, nfpyn__kyz


def shuffle_dataframe(df, keys, _is_parallel):
    return df, keys, _is_parallel


@overload(shuffle_dataframe)
def overload_shuffle_dataframe(df, keys, _is_parallel):
    ataz__niihn = len(df.columns)
    tvu__jjbm = len(keys.types)
    dbxg__xywq = ', '.join('data_{}'.format(ebl__unuys) for ebl__unuys in
        range(ataz__niihn))
    bue__ctj = 'def impl(df, keys, _is_parallel):\n'
    for ebl__unuys in range(ataz__niihn):
        bue__ctj += f"""  in_arr{ebl__unuys} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {ebl__unuys})
"""
    bue__ctj += f"""  in_index_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
    bue__ctj += '  info_list = [{}, {}, {}]\n'.format(', '.join(
        f'array_to_info(keys[{ebl__unuys}])' for ebl__unuys in range(
        tvu__jjbm)), ', '.join(f'array_to_info(in_arr{ebl__unuys})' for
        ebl__unuys in range(ataz__niihn)), 'array_to_info(in_index_arr)')
    bue__ctj += '  table = arr_info_list_to_table(info_list)\n'
    bue__ctj += (
        f'  out_table = shuffle_table(table, {tvu__jjbm}, _is_parallel, 1)\n')
    for ebl__unuys in range(tvu__jjbm):
        bue__ctj += f"""  out_key{ebl__unuys} = info_to_array(info_from_table(out_table, {ebl__unuys}), keys[{ebl__unuys}])
"""
    for ebl__unuys in range(ataz__niihn):
        bue__ctj += f"""  out_arr{ebl__unuys} = info_to_array(info_from_table(out_table, {ebl__unuys + tvu__jjbm}), in_arr{ebl__unuys})
"""
    bue__ctj += f"""  out_arr_index = info_to_array(info_from_table(out_table, {tvu__jjbm + ataz__niihn}), in_index_arr)
"""
    bue__ctj += '  shuffle_info = get_shuffle_info(out_table)\n'
    bue__ctj += '  delete_table(out_table)\n'
    bue__ctj += '  delete_table(table)\n'
    out_data = ', '.join(f'out_arr{ebl__unuys}' for ebl__unuys in range(
        ataz__niihn))
    bue__ctj += (
        '  out_index = bodo.utils.conversion.index_from_array(out_arr_index)\n'
        )
    bue__ctj += f"""  out_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(({out_data},), out_index, {gen_const_tup(df.columns)})
"""
    bue__ctj += '  return out_df, ({},), shuffle_info\n'.format(', '.join(
        f'out_key{ebl__unuys}' for ebl__unuys in range(tvu__jjbm)))
    hkqvp__iybgy = {}
    exec(bue__ctj, {'bodo': bodo, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_from_table': info_from_table, 'info_to_array':
        info_to_array, 'delete_table': delete_table, 'get_shuffle_info':
        get_shuffle_info}, hkqvp__iybgy)
    ugxc__bus = hkqvp__iybgy['impl']
    return ugxc__bus


def reverse_shuffle(data, shuffle_info):
    return data


@overload(reverse_shuffle)
def overload_reverse_shuffle(data, shuffle_info):
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        ono__gca = len(data.array_types)
        bue__ctj = 'def impl(data, shuffle_info):\n'
        bue__ctj += '  info_list = [{}]\n'.format(', '.join(
            f'array_to_info(data._data[{ebl__unuys}])' for ebl__unuys in
            range(ono__gca)))
        bue__ctj += '  table = arr_info_list_to_table(info_list)\n'
        bue__ctj += (
            '  out_table = reverse_shuffle_table(table, shuffle_info)\n')
        for ebl__unuys in range(ono__gca):
            bue__ctj += f"""  out_arr{ebl__unuys} = info_to_array(info_from_table(out_table, {ebl__unuys}), data._data[{ebl__unuys}])
"""
        bue__ctj += '  delete_table(out_table)\n'
        bue__ctj += '  delete_table(table)\n'
        bue__ctj += (
            '  return init_multi_index(({},), data._names, data._name)\n'.
            format(', '.join(f'out_arr{ebl__unuys}' for ebl__unuys in range
            (ono__gca))))
        hkqvp__iybgy = {}
        exec(bue__ctj, {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'reverse_shuffle_table': reverse_shuffle_table,
            'info_from_table': info_from_table, 'info_to_array':
            info_to_array, 'delete_table': delete_table, 'init_multi_index':
            bodo.hiframes.pd_multi_index_ext.init_multi_index}, hkqvp__iybgy)
        ugxc__bus = hkqvp__iybgy['impl']
        return ugxc__bus
    if bodo.hiframes.pd_index_ext.is_index_type(data):

        def impl_index(data, shuffle_info):
            sput__hoqir = bodo.utils.conversion.index_to_array(data)
            wtly__jiuu = reverse_shuffle(sput__hoqir, shuffle_info)
            return bodo.utils.conversion.index_from_array(wtly__jiuu)
        return impl_index

    def impl_arr(data, shuffle_info):
        kyton__wwd = [array_to_info(data)]
        rkda__udfwz = arr_info_list_to_table(kyton__wwd)
        njl__dhy = reverse_shuffle_table(rkda__udfwz, shuffle_info)
        wtly__jiuu = info_to_array(info_from_table(njl__dhy, 0), data)
        delete_table(njl__dhy)
        delete_table(rkda__udfwz)
        return wtly__jiuu
    return impl_arr


@overload_method(DataFrameGroupByType, 'value_counts', inline='always',
    no_unliteral=True)
def groupby_value_counts(grp, normalize=False, sort=True, ascending=False,
    bins=None, dropna=True):
    ftd__pvs = dict(normalize=normalize, sort=sort, bins=bins, dropna=dropna)
    kzz__hqzo = dict(normalize=False, sort=True, bins=None, dropna=True)
    check_unsupported_args('Groupby.value_counts', ftd__pvs, kzz__hqzo)
    if len(grp.selection) > 1 or not grp.as_index:
        raise BodoError(
            "'DataFrameGroupBy' object has no attribute 'value_counts'")
    yxzld__dheif = grp.selection[0]
    bue__ctj = f"""def impl(grp, normalize=False, sort=True, ascending=False, bins=None, dropna=True):
"""
    qplet__eih = (
        f"lambda S : S.value_counts(ascending={ascending}, _index_name='{yxzld__dheif}')"
        )
    bue__ctj += f'    return grp.apply({qplet__eih})\n'
    hkqvp__iybgy = {}
    exec(bue__ctj, {'bodo': bodo}, hkqvp__iybgy)
    ugxc__bus = hkqvp__iybgy['impl']
    return ugxc__bus


groupby_unsupported = {'all', 'any', 'backfill', 'bfill', 'boxplot', 'corr',
    'corrwith', 'cumcount', 'cummax', 'cov', 'diff', 'fillna', 'hist',
    'idxmin', 'mad', 'skew', 'take', 'cummin', 'cumprod', 'describe',
    'ffill', 'filter', 'get_group', 'head', 'ngroup', 'nth', 'ohlc', 'pad',
    'pct_change', 'plot', 'quantile', 'rank', 'resample', 'sample', 'sem',
    'tail', 'tshift'}


def _install_groupy_unsupported():
    for prife__dglvn in groupby_unsupported:
        overload_method(DataFrameGroupByType, prife__dglvn, no_unliteral=True)(
            create_unsupported_overload(
            f"DataFrameGroupByType: '{prife__dglvn}'"))


_install_groupy_unsupported()
