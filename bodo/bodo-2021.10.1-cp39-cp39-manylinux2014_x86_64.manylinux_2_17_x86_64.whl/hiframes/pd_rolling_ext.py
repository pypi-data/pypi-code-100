"""typing for rolling window functions
"""
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.core.typing.templates import AbstractTemplate, AttributeTemplate, signature
from numba.extending import infer, infer_getattr, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_method, register_model
import bodo
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_type, pd_timedelta_type
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_groupby_ext import DataFrameGroupByType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.rolling import supported_rolling_funcs
from bodo.utils.typing import BodoError, check_unsupported_args, get_literal_value, is_const_func_type, is_literal_type, is_overload_bool, is_overload_constant_str, is_overload_int, is_overload_none, raise_const_error


class RollingType(types.Type):

    def __init__(self, obj_type, window_type, on, selection,
        explicit_select=False, series_select=False):
        self.obj_type = obj_type
        self.window_type = window_type
        self.on = on
        self.selection = selection
        self.explicit_select = explicit_select
        self.series_select = series_select
        super(RollingType, self).__init__(name=
            f'RollingType({obj_type}, {window_type}, {on}, {selection}, {explicit_select}, {series_select})'
            )

    def copy(self):
        return RollingType(self.obj_type, self.window_type, self.on, self.
            selection, self.explicit_select, self.series_select)


@register_model(RollingType)
class RollingModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        wml__qvp = [('obj', fe_type.obj_type), ('window', fe_type.
            window_type), ('min_periods', types.int64), ('center', types.bool_)
            ]
        super(RollingModel, self).__init__(dmm, fe_type, wml__qvp)


make_attribute_wrapper(RollingType, 'obj', 'obj')
make_attribute_wrapper(RollingType, 'window', 'window')
make_attribute_wrapper(RollingType, 'center', 'center')
make_attribute_wrapper(RollingType, 'min_periods', 'min_periods')


@overload_method(DataFrameType, 'rolling', inline='always', no_unliteral=True)
def df_rolling_overload(df, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    cth__eblx = dict(win_type=win_type, axis=axis, closed=closed)
    vvi__pmlbi = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('DataFrame.rolling', cth__eblx, vvi__pmlbi)
    _validate_rolling_args(df, window, min_periods, center, on)

    def impl(df, window, min_periods=None, center=False, win_type=None, on=
        None, axis=0, closed=None):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(df, window,
            min_periods, center, on)
    return impl


@overload_method(SeriesType, 'rolling', inline='always', no_unliteral=True)
def overload_series_rolling(S, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    cth__eblx = dict(win_type=win_type, axis=axis, closed=closed)
    vvi__pmlbi = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('Series.rolling', cth__eblx, vvi__pmlbi)
    _validate_rolling_args(S, window, min_periods, center, on)

    def impl(S, window, min_periods=None, center=False, win_type=None, on=
        None, axis=0, closed=None):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(S, window,
            min_periods, center, on)
    return impl


@intrinsic
def init_rolling(typingctx, obj_type, window_type, min_periods_type,
    center_type, on_type=None):

    def codegen(context, builder, signature, args):
        jjz__kjgx, kggwo__ldonx, rwuyl__xgctv, tkl__iqk, jsvfz__wtzwh = args
        odu__mqnt = signature.return_type
        pvjy__zwloh = cgutils.create_struct_proxy(odu__mqnt)(context, builder)
        pvjy__zwloh.obj = jjz__kjgx
        pvjy__zwloh.window = kggwo__ldonx
        pvjy__zwloh.min_periods = rwuyl__xgctv
        pvjy__zwloh.center = tkl__iqk
        context.nrt.incref(builder, signature.args[0], jjz__kjgx)
        context.nrt.incref(builder, signature.args[1], kggwo__ldonx)
        context.nrt.incref(builder, signature.args[2], rwuyl__xgctv)
        context.nrt.incref(builder, signature.args[3], tkl__iqk)
        return pvjy__zwloh._getvalue()
    on = get_literal_value(on_type)
    if isinstance(obj_type, SeriesType):
        selection = None
    elif isinstance(obj_type, DataFrameType):
        selection = obj_type.columns
    else:
        assert isinstance(obj_type, DataFrameGroupByType
            ), f'invalid obj type for rolling: {obj_type}'
        selection = obj_type.selection
    odu__mqnt = RollingType(obj_type, window_type, on, selection, False)
    return odu__mqnt(obj_type, window_type, min_periods_type, center_type,
        on_type), codegen


def _handle_default_min_periods(min_periods, window):
    return min_periods


@overload(_handle_default_min_periods)
def overload_handle_default_min_periods(min_periods, window):
    if is_overload_none(min_periods):
        if isinstance(window, types.Integer):
            return lambda min_periods, window: window
        else:
            return lambda min_periods, window: 1
    else:
        return lambda min_periods, window: min_periods


def _gen_df_rolling_out_data(rolling):
    wiid__glh = not isinstance(rolling.window_type, types.Integer)
    urhiw__uxb = 'variable' if wiid__glh else 'fixed'
    pxfr__mef = 'None'
    if wiid__glh:
        pxfr__mef = ('bodo.utils.conversion.index_to_array(index)' if 
            rolling.on is None else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rolling.obj_type.columns.index(rolling.on)})'
            )
    fcsw__jwlen = []
    neju__ndus = 'on_arr, ' if wiid__glh else ''
    if isinstance(rolling.obj_type, SeriesType):
        return (
            f'bodo.hiframes.rolling.rolling_{urhiw__uxb}(bodo.hiframes.pd_series_ext.get_series_data(df), {neju__ndus}index_arr, window, minp, center, func, raw)'
            , pxfr__mef, rolling.selection)
    assert isinstance(rolling.obj_type, DataFrameType
        ), 'expected df in rolling obj'
    koyby__ijgz = rolling.obj_type.data
    out_cols = []
    for lsh__iyk in rolling.selection:
        lje__xbky = rolling.obj_type.columns.index(lsh__iyk)
        if lsh__iyk == rolling.on:
            if len(rolling.selection) == 2 and rolling.series_select:
                continue
            tutb__ywpq = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {lje__xbky})'
                )
            out_cols.append(lsh__iyk)
        else:
            if not isinstance(koyby__ijgz[lje__xbky].dtype, (types.Boolean,
                types.Number)):
                continue
            tutb__ywpq = (
                f'bodo.hiframes.rolling.rolling_{urhiw__uxb}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {lje__xbky}), {neju__ndus}index_arr, window, minp, center, func, raw)'
                )
            out_cols.append(lsh__iyk)
        fcsw__jwlen.append(tutb__ywpq)
    return ', '.join(fcsw__jwlen), pxfr__mef, tuple(out_cols)


@overload_method(RollingType, 'apply', inline='always', no_unliteral=True)
def overload_rolling_apply(rolling, func, raw=False, engine=None,
    engine_kwargs=None, args=None, kwargs=None):
    cth__eblx = dict(engine=engine, engine_kwargs=engine_kwargs, args=args,
        kwargs=kwargs)
    vvi__pmlbi = dict(engine=None, engine_kwargs=None, args=None, kwargs=None)
    check_unsupported_args('Rolling.apply', cth__eblx, vvi__pmlbi)
    if not is_const_func_type(func):
        raise BodoError(
            f"Rolling.apply(): 'func' parameter must be a function, not {func} (builtin functions not supported yet)."
            )
    if not is_overload_bool(raw):
        raise BodoError(
            f"Rolling.apply(): 'raw' parameter must be bool, not {raw}.")
    return _gen_rolling_impl(rolling, 'apply')


@overload_method(DataFrameGroupByType, 'rolling', inline='always',
    no_unliteral=True)
def groupby_rolling_overload(grp, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    cth__eblx = dict(win_type=win_type, axis=axis, closed=closed)
    vvi__pmlbi = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('GroupBy.rolling', cth__eblx, vvi__pmlbi)
    _validate_rolling_args(grp, window, min_periods, center, on)

    def _impl(grp, window, min_periods=None, center=False, win_type=None,
        on=None, axis=0, closed=None):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(grp, window,
            min_periods, center, on)
    return _impl


def _gen_rolling_impl(rolling, fname, other=None):
    if isinstance(rolling.obj_type, DataFrameGroupByType):
        shfe__ghv = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
        dfq__ayyww = f"'{rolling.on}'" if isinstance(rolling.on, str
            ) else f'{rolling.on}'
        selection = ''
        if rolling.explicit_select:
            selection = '[{}]'.format(', '.join(f"'{sngi__dqgd}'" if
                isinstance(sngi__dqgd, str) else f'{sngi__dqgd}' for
                sngi__dqgd in rolling.selection if sngi__dqgd != rolling.on))
        ufqn__tuexr = eckb__dkfrp = ''
        if fname == 'apply':
            ufqn__tuexr = 'func, raw, args, kwargs'
            eckb__dkfrp = 'func, raw, None, None, args, kwargs'
        if fname == 'corr':
            ufqn__tuexr = eckb__dkfrp = 'other, pairwise'
        if fname == 'cov':
            ufqn__tuexr = eckb__dkfrp = 'other, pairwise, ddof'
        gyilr__akhq = (
            f'lambda df, window, minp, center, {ufqn__tuexr}: bodo.hiframes.pd_rolling_ext.init_rolling(df, window, minp, center, {dfq__ayyww}){selection}.{fname}({eckb__dkfrp})'
            )
        shfe__ghv += f"""  return rolling.obj.apply({gyilr__akhq}, rolling.window, rolling.min_periods, rolling.center, {ufqn__tuexr})
"""
        itzil__cffjp = {}
        exec(shfe__ghv, {'bodo': bodo}, itzil__cffjp)
        impl = itzil__cffjp['impl']
        return impl
    zpqgr__jadwp = isinstance(rolling.obj_type, SeriesType)
    if fname in ('corr', 'cov'):
        out_cols = None if zpqgr__jadwp else _get_corr_cov_out_cols(rolling,
            other, fname)
        df_cols = None if zpqgr__jadwp else rolling.obj_type.columns
        other_cols = None if zpqgr__jadwp else other.columns
        fcsw__jwlen, pxfr__mef = _gen_corr_cov_out_data(out_cols, df_cols,
            other_cols, rolling.window_type, fname)
    else:
        fcsw__jwlen, pxfr__mef, out_cols = _gen_df_rolling_out_data(rolling)
    zimn__zlqpr = zpqgr__jadwp or len(rolling.selection) == (1 if rolling.
        on is None else 2) and rolling.series_select
    uxne__wtpn = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
    uxne__wtpn += '  df = rolling.obj\n'
    uxne__wtpn += '  index = {}\n'.format(
        'bodo.hiframes.pd_series_ext.get_series_index(df)' if zpqgr__jadwp else
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
    elwxm__zxr = 'None'
    if zpqgr__jadwp:
        elwxm__zxr = 'bodo.hiframes.pd_series_ext.get_series_name(df)'
    elif zimn__zlqpr:
        lsh__iyk = (set(out_cols) - set([rolling.on])).pop()
        elwxm__zxr = f"'{lsh__iyk}'" if isinstance(lsh__iyk, str) else str(
            lsh__iyk)
    uxne__wtpn += f'  name = {elwxm__zxr}\n'
    uxne__wtpn += '  window = rolling.window\n'
    uxne__wtpn += '  center = rolling.center\n'
    uxne__wtpn += '  minp = rolling.min_periods\n'
    uxne__wtpn += f'  on_arr = {pxfr__mef}\n'
    if fname == 'apply':
        uxne__wtpn += (
            f'  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    else:
        uxne__wtpn += f"  func = '{fname}'\n"
        uxne__wtpn += f'  index_arr = None\n'
        uxne__wtpn += f'  raw = False\n'
    if zimn__zlqpr:
        uxne__wtpn += (
            f'  return bodo.hiframes.pd_series_ext.init_series({fcsw__jwlen}, index, name)'
            )
        itzil__cffjp = {}
        jjpjx__gmt = {'bodo': bodo}
        exec(uxne__wtpn, jjpjx__gmt, itzil__cffjp)
        impl = itzil__cffjp['impl']
        return impl
    return bodo.hiframes.dataframe_impl._gen_init_df(uxne__wtpn, out_cols,
        fcsw__jwlen)


def _get_rolling_func_args(fname):
    if fname == 'apply':
        return (
            'func, raw=False, engine=None, engine_kwargs=None, args=None, kwargs=None\n'
            )
    elif fname == 'corr':
        return 'other=None, pairwise=None\n'
    elif fname == 'cov':
        return 'other=None, pairwise=None, ddof=1\n'
    return ''


def create_rolling_overload(fname):

    def overload_rolling_func(rolling):
        return _gen_rolling_impl(rolling, fname)
    return overload_rolling_func


def _install_rolling_methods():
    for fname in supported_rolling_funcs:
        if fname in ('apply', 'corr', 'cov'):
            continue
        henfa__ihf = create_rolling_overload(fname)
        overload_method(RollingType, fname, inline='always', no_unliteral=True
            )(henfa__ihf)


_install_rolling_methods()


def _get_corr_cov_out_cols(rolling, other, func_name):
    jmf__ylfum = rolling.selection
    if rolling.on is not None:
        raise BodoError(
            f'variable window rolling {func_name} not supported yet.')
    out_cols = tuple(sorted(set(jmf__ylfum) | set(other.columns), key=lambda
        k: str(k)))
    return out_cols


def _gen_corr_cov_out_data(out_cols, df_cols, other_cols, window_type,
    func_name):
    wiid__glh = not isinstance(window_type, types.Integer)
    pxfr__mef = 'None'
    if wiid__glh:
        pxfr__mef = 'bodo.utils.conversion.index_to_array(index)'
    neju__ndus = 'on_arr, ' if wiid__glh else ''
    fcsw__jwlen = []
    if out_cols is None:
        return (
            f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_series_ext.get_series_data(df), bodo.hiframes.pd_series_ext.get_series_data(other), {neju__ndus}window, minp, center)'
            , pxfr__mef)
    for lsh__iyk in out_cols:
        if lsh__iyk in df_cols and lsh__iyk in other_cols:
            mpmst__qasf = df_cols.index(lsh__iyk)
            epbw__euuch = other_cols.index(lsh__iyk)
            tutb__ywpq = (
                f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {mpmst__qasf}), bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {epbw__euuch}), {neju__ndus}window, minp, center)'
                )
        else:
            tutb__ywpq = 'np.full(len(df), np.nan)'
        fcsw__jwlen.append(tutb__ywpq)
    return ', '.join(fcsw__jwlen), pxfr__mef


@overload_method(RollingType, 'corr', inline='always', no_unliteral=True)
def overload_rolling_corr(rolling, other=None, pairwise=None):
    return _gen_rolling_impl(rolling, 'corr', other)


@overload_method(RollingType, 'cov', inline='always', no_unliteral=True)
def overload_rolling_cov(rolling, other=None, pairwise=None, ddof=1):
    return _gen_rolling_impl(rolling, 'cov', other)


@infer
class GetItemDataFrameRolling2(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        rolling, kke__weo = args
        if isinstance(rolling, RollingType):
            jmf__ylfum = rolling.obj_type.selection if isinstance(rolling.
                obj_type, DataFrameGroupByType) else rolling.obj_type.columns
            series_select = False
            if isinstance(kke__weo, (tuple, list)):
                if len(set(kke__weo).difference(set(jmf__ylfum))) > 0:
                    raise_const_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(set(kke__weo).difference(set(jmf__ylfum))))
                selection = list(kke__weo)
            else:
                if kke__weo not in jmf__ylfum:
                    raise_const_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(kke__weo))
                selection = [kke__weo]
                series_select = True
            if rolling.on is not None:
                selection.append(rolling.on)
            neuzo__zhd = RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, tuple(selection), True, series_select)
            return signature(neuzo__zhd, *args)


@lower_builtin('static_getitem', RollingType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@infer_getattr
class RollingAttribute(AttributeTemplate):
    key = RollingType

    def generic_resolve(self, rolling, attr):
        jmf__ylfum = ()
        if isinstance(rolling.obj_type, DataFrameGroupByType):
            jmf__ylfum = rolling.obj_type.selection
        if isinstance(rolling.obj_type, DataFrameType):
            jmf__ylfum = rolling.obj_type.columns
        if attr in jmf__ylfum:
            return RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, (attr,) if rolling.on is None else (attr,
                rolling.on), True, True)


def _validate_rolling_args(obj, window, min_periods, center, on):
    assert isinstance(obj, (SeriesType, DataFrameType, DataFrameGroupByType)
        ), 'invalid rolling obj'
    func_name = 'Series' if isinstance(obj, SeriesType
        ) else 'DataFrame' if isinstance(obj, DataFrameType
        ) else 'DataFrameGroupBy'
    if not (is_overload_int(window) or is_overload_constant_str(window) or 
        window == bodo.string_type or window in (pd_timedelta_type,
        datetime_timedelta_type)):
        raise BodoError(
            f"{func_name}.rolling(): 'window' should be int or time offset (str, pd.Timedelta, datetime.timedelta), not {window}"
            )
    if not is_overload_bool(center):
        raise BodoError(
            f'{func_name}.rolling(): center must be a boolean, not {center}')
    if not (is_overload_none(min_periods) or isinstance(min_periods, types.
        Integer)):
        raise BodoError(
            f'{func_name}.rolling(): min_periods must be an integer, not {min_periods}'
            )
    if isinstance(obj, SeriesType) and not is_overload_none(on):
        raise BodoError(
            f"{func_name}.rolling(): 'on' not supported for Series yet (can use a DataFrame instead)."
            )
    jfg__kkcc = obj.columns if isinstance(obj, DataFrameType
        ) else obj.df_type.columns if isinstance(obj, DataFrameGroupByType
        ) else []
    koyby__ijgz = [obj.data] if isinstance(obj, SeriesType
        ) else obj.data if isinstance(obj, DataFrameType) else obj.df_type.data
    if not is_overload_none(on) and (not is_literal_type(on) or 
        get_literal_value(on) not in jfg__kkcc):
        raise BodoError(
            f"{func_name}.rolling(): 'on' should be a constant column name.")
    if not is_overload_none(on):
        hskws__yfl = koyby__ijgz[jfg__kkcc.index(get_literal_value(on))]
        if not isinstance(hskws__yfl, types.Array
            ) or hskws__yfl.dtype != bodo.datetime64ns:
            raise BodoError(
                f"{func_name}.rolling(): 'on' column should have datetime64 data."
                )
    if not any(isinstance(pjz__yup.dtype, (types.Boolean, types.Number)) for
        pjz__yup in koyby__ijgz):
        raise BodoError(f'{func_name}.rolling(): No numeric types to aggregate'
            )
