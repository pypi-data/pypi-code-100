"""
Indexing support for pd.DataFrame type.
"""
import operator
import numpy as np
import pandas as pd
from numba.core import cgutils, types
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.utils.transform import gen_const_tup
from bodo.utils.typing import BodoError, get_overload_const_int, get_overload_const_list, get_overload_const_str, is_immutable_array, is_list_like_index_type, is_overload_constant_int, is_overload_constant_list, is_overload_constant_str, raise_bodo_error


@infer_global(operator.getitem)
class DataFrameGetItemTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        if isinstance(args[0], DataFrameType):
            return self.typecheck_df_getitem(args)
        elif isinstance(args[0], DataFrameLocType):
            return self.typecheck_loc_getitem(args)
        else:
            return

    def typecheck_loc_getitem(self, args):
        I = args[0]
        idx = args[1]
        df = I.df_type
        if isinstance(df.columns[0], tuple):
            raise_bodo_error(
                'DataFrame.loc[] getitem (location-based indexing) with multi-indexed columns not supported yet'
                )
        if is_list_like_index_type(idx) and idx.dtype == types.bool_:
            tbr__jevp = idx
            qop__wgd = df.data
            oee__tcvxs = df.columns
            gwksu__xadd = self.replace_range_with_numeric_idx_if_needed(df,
                tbr__jevp)
            jrfz__wzgcl = DataFrameType(qop__wgd, gwksu__xadd, oee__tcvxs)
            return jrfz__wzgcl(*args)
        if isinstance(idx, types.BaseTuple) and len(idx) == 2:
            itys__qns = idx.types[0]
            zbni__jqtfl = idx.types[1]
            if isinstance(itys__qns, types.Integer):
                if not isinstance(df.index, bodo.hiframes.pd_index_ext.
                    RangeIndexType):
                    raise_bodo_error(
                        'Dataframe.loc[int, col_ind] getitem only supported for dataframes with RangeIndexes'
                        )
                if is_overload_constant_str(zbni__jqtfl):
                    tcy__lnlg = get_overload_const_str(zbni__jqtfl)
                    if tcy__lnlg not in df.columns:
                        raise_bodo_error(
                            'dataframe {} does not include column {}'.
                            format(df, tcy__lnlg))
                    xgveb__egtcd = df.columns.index(tcy__lnlg)
                    return df.data[xgveb__egtcd].dtype(*args)
                if isinstance(zbni__jqtfl, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
                        )
                else:
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
                        )
            if is_list_like_index_type(itys__qns
                ) and itys__qns.dtype == types.bool_ or isinstance(itys__qns,
                types.SliceType):
                gwksu__xadd = self.replace_range_with_numeric_idx_if_needed(df,
                    itys__qns)
                if is_overload_constant_str(zbni__jqtfl):
                    rvxd__vso = get_overload_const_str(zbni__jqtfl)
                    if rvxd__vso not in df.columns:
                        raise_bodo_error(
                            f'dataframe {df} does not include column {rvxd__vso}'
                            )
                    xgveb__egtcd = df.columns.index(rvxd__vso)
                    pfhh__mer = df.data[xgveb__egtcd]
                    icudy__qqrw = pfhh__mer.dtype
                    odquw__wqz = types.literal(df.columns[xgveb__egtcd])
                    jrfz__wzgcl = bodo.SeriesType(icudy__qqrw, pfhh__mer,
                        gwksu__xadd, odquw__wqz)
                    return jrfz__wzgcl(*args)
                if isinstance(zbni__jqtfl, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
                        )
                elif is_overload_constant_list(zbni__jqtfl):
                    djtr__blf = get_overload_const_list(zbni__jqtfl)
                    if zbni__jqtfl.dtype == types.bool_:
                        if len(df.columns) != len(djtr__blf):
                            raise_bodo_error(
                                f'dataframe {df} has {len(df.columns)} columns, but boolean array used with DataFrame.loc[] {djtr__blf} has {len(djtr__blf)} values'
                                )
                        xowy__rttfh = []
                        nvleu__ffbmo = []
                        for qzei__rgcx in range(len(djtr__blf)):
                            if djtr__blf[qzei__rgcx]:
                                xowy__rttfh.append(df.columns[qzei__rgcx])
                                nvleu__ffbmo.append(df.data[qzei__rgcx])
                        wkt__iac = tuple()
                        jrfz__wzgcl = DataFrameType(tuple(nvleu__ffbmo),
                            gwksu__xadd, tuple(xowy__rttfh))
                        return jrfz__wzgcl(*args)
                    elif zbni__jqtfl.dtype == bodo.string_type:
                        wkt__iac, nvleu__ffbmo = self.get_kept_cols_and_data(df
                            , djtr__blf)
                        jrfz__wzgcl = DataFrameType(nvleu__ffbmo,
                            gwksu__xadd, wkt__iac)
                        return jrfz__wzgcl(*args)
        raise_bodo_error(
            f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet. If you are trying to select a subset of the columns by passing a list of column names, that list must be a compile time constant. See https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
            )

    def typecheck_df_getitem(self, args):
        df = args[0]
        ind = args[1]
        if is_overload_constant_str(ind) or is_overload_constant_int(ind):
            ind_val = get_overload_const_str(ind) if is_overload_constant_str(
                ind) else get_overload_const_int(ind)
            if isinstance(df.columns[0], tuple):
                xowy__rttfh = []
                nvleu__ffbmo = []
                for qzei__rgcx, pps__tuzun in enumerate(df.columns):
                    if pps__tuzun[0] != ind_val:
                        continue
                    xowy__rttfh.append(pps__tuzun[1] if len(pps__tuzun) == 
                        2 else pps__tuzun[1:])
                    nvleu__ffbmo.append(df.data[qzei__rgcx])
                pfhh__mer = tuple(nvleu__ffbmo)
                minb__juw = df.index
                yzua__cbu = tuple(xowy__rttfh)
                jrfz__wzgcl = DataFrameType(pfhh__mer, minb__juw, yzua__cbu)
                return jrfz__wzgcl(*args)
            else:
                if ind_val not in df.columns:
                    raise_bodo_error('dataframe {} does not include column {}'
                        .format(df, ind_val))
                xgveb__egtcd = df.columns.index(ind_val)
                pfhh__mer = df.data[xgveb__egtcd]
                icudy__qqrw = pfhh__mer.dtype
                minb__juw = df.index
                odquw__wqz = types.literal(df.columns[xgveb__egtcd])
                jrfz__wzgcl = bodo.SeriesType(icudy__qqrw, pfhh__mer,
                    minb__juw, odquw__wqz)
                return jrfz__wzgcl(*args)
        if isinstance(ind, types.Integer) or isinstance(ind, types.UnicodeType
            ):
            raise_bodo_error(
                'df[] getitem selecting a subset of columns requires providing constant column names. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html'
                )
        if is_list_like_index_type(ind
            ) and ind.dtype == types.bool_ or isinstance(ind, types.SliceType):
            pfhh__mer = df.data
            minb__juw = self.replace_range_with_numeric_idx_if_needed(df, ind)
            yzua__cbu = df.columns
            jrfz__wzgcl = DataFrameType(pfhh__mer, minb__juw, yzua__cbu)
            return jrfz__wzgcl(*args)
        elif is_overload_constant_list(ind):
            jws__sahd = get_overload_const_list(ind)
            yzua__cbu, pfhh__mer = self.get_kept_cols_and_data(df, jws__sahd)
            minb__juw = df.index
            jrfz__wzgcl = DataFrameType(pfhh__mer, minb__juw, yzua__cbu)
            return jrfz__wzgcl(*args)
        raise_bodo_error(
            f'df[] getitem using {ind} not supported. If you are trying to select a subset of the columns, you must provide the column names you are selecting as a constant. See https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html'
            )

    def get_kept_cols_and_data(self, df, cols_to_keep_list):
        for ybth__crim in cols_to_keep_list:
            if ybth__crim not in df.columns:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(ybth__crim, df.columns))
        yzua__cbu = tuple(cols_to_keep_list)
        pfhh__mer = tuple(df.data[df.columns.index(ylmiq__mzug)] for
            ylmiq__mzug in yzua__cbu)
        return yzua__cbu, pfhh__mer

    def replace_range_with_numeric_idx_if_needed(self, df, ind):
        gwksu__xadd = bodo.hiframes.pd_index_ext.NumericIndexType(types.
            int64, df.index.name_typ) if not isinstance(ind, types.SliceType
            ) and isinstance(df.index, bodo.hiframes.pd_index_ext.
            RangeIndexType) else df.index
        return gwksu__xadd


DataFrameGetItemTemplate._no_unliteral = True


@lower_builtin(operator.getitem, DataFrameType, types.Any)
def getitem_df_lower(context, builder, sig, args):
    impl = df_getitem_overload(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def df_getitem_overload(df, ind):
    if not isinstance(df, DataFrameType):
        return
    if is_overload_constant_str(ind) or is_overload_constant_int(ind):
        ind_val = get_overload_const_str(ind) if is_overload_constant_str(ind
            ) else get_overload_const_int(ind)
        if isinstance(df.columns[0], tuple):
            xowy__rttfh = []
            nvleu__ffbmo = []
            for qzei__rgcx, pps__tuzun in enumerate(df.columns):
                if pps__tuzun[0] != ind_val:
                    continue
                xowy__rttfh.append(pps__tuzun[1] if len(pps__tuzun) == 2 else
                    pps__tuzun[1:])
                nvleu__ffbmo.append(
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'
                    .format(qzei__rgcx))
            erk__pihgm = 'def impl(df, ind):\n'
            xvq__jfcr = (
                'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
            return bodo.hiframes.dataframe_impl._gen_init_df(erk__pihgm,
                xowy__rttfh, ', '.join(nvleu__ffbmo), xvq__jfcr)
        if ind_val not in df.columns:
            raise_bodo_error('dataframe {} does not include column {}'.
                format(df, ind_val))
        col_no = df.columns.index(ind_val)
        return lambda df, ind: bodo.hiframes.pd_series_ext.init_series(bodo
            .hiframes.pd_dataframe_ext.get_dataframe_data(df, col_no), bodo
            .hiframes.pd_dataframe_ext.get_dataframe_index(df), ind_val)
    if is_overload_constant_list(ind):
        jws__sahd = get_overload_const_list(ind)
        for ybth__crim in jws__sahd:
            if ybth__crim not in df.columns:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(ybth__crim, df.columns))
        nvleu__ffbmo = ', '.join(
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}).copy()'
            .format(df.columns.index(ybth__crim)) for ybth__crim in jws__sahd)
        erk__pihgm = 'def impl(df, ind):\n'
        xvq__jfcr = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
        return bodo.hiframes.dataframe_impl._gen_init_df(erk__pihgm,
            jws__sahd, nvleu__ffbmo, xvq__jfcr)
    if is_list_like_index_type(ind) and ind.dtype == types.bool_ or isinstance(
        ind, types.SliceType):
        erk__pihgm = 'def impl(df, ind):\n'
        if not isinstance(ind, types.SliceType):
            erk__pihgm += (
                '  ind = bodo.utils.conversion.coerce_to_ndarray(ind)\n')
        xvq__jfcr = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[ind]')
        nvleu__ffbmo = ', '.join(
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})[ind]'
            .format(df.columns.index(ybth__crim)) for ybth__crim in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(erk__pihgm, df.
            columns, nvleu__ffbmo, xvq__jfcr)
    raise_bodo_error('df[] getitem using {} not supported'.format(ind))


@overload(operator.setitem, no_unliteral=True)
def df_setitem_overload(df, idx, val):
    if not isinstance(df, DataFrameType):
        return
    raise_bodo_error('DataFrame setitem: transform necessary')


class DataFrameILocType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        ylmiq__mzug = 'DataFrameILocType({})'.format(df_type)
        super(DataFrameILocType, self).__init__(ylmiq__mzug)
    ndim = 2


@register_model(DataFrameILocType)
class DataFrameILocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        fhocv__uipu = [('obj', fe_type.df_type)]
        super(DataFrameILocModel, self).__init__(dmm, fe_type, fhocv__uipu)


make_attribute_wrapper(DataFrameILocType, 'obj', '_obj')


@intrinsic
def init_dataframe_iloc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        qef__znb, = args
        waa__eyja = signature.return_type
        mtr__xpdlg = cgutils.create_struct_proxy(waa__eyja)(context, builder)
        mtr__xpdlg.obj = qef__znb
        context.nrt.incref(builder, signature.args[0], qef__znb)
        return mtr__xpdlg._getvalue()
    return DataFrameILocType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'iloc')
def overload_series_iloc(s):
    return lambda s: bodo.hiframes.dataframe_indexing.init_dataframe_iloc(s)


@overload(operator.getitem, no_unliteral=True)
def overload_iloc_getitem(I, idx):
    if not isinstance(I, DataFrameILocType):
        return
    df = I.df_type
    if isinstance(idx, types.Integer):
        return _gen_iloc_getitem_row_impl(df, df.columns, 'idx')
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and not isinstance(
        idx[1], types.SliceType):
        if not (is_overload_constant_list(idx.types[1]) or
            is_overload_constant_int(idx.types[1])):
            raise_bodo_error(
                'idx2 in df.iloc[idx1, idx2] should be a constant integer or constant list of integers. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
                )
        kczfg__jyihk = len(df.data)
        if is_overload_constant_int(idx.types[1]):
            is_out_series = True
            eob__pehn = get_overload_const_int(idx.types[1])
            if eob__pehn < 0 or eob__pehn >= kczfg__jyihk:
                raise BodoError(
                    'df.iloc: column integer must refer to a valid column number'
                    )
            dcm__gpxwa = [eob__pehn]
        else:
            is_out_series = False
            dcm__gpxwa = get_overload_const_list(idx.types[1])
            if any(not isinstance(ind, int) or ind < 0 or ind >=
                kczfg__jyihk for ind in dcm__gpxwa):
                raise BodoError(
                    'df.iloc: column list must be integers referring to a valid column number'
                    )
        col_names = tuple(pd.Series(df.columns, dtype=object)[dcm__gpxwa])
        if isinstance(idx.types[0], types.Integer):
            if isinstance(idx.types[1], types.Integer):
                eob__pehn = dcm__gpxwa[0]

                def impl(I, idx):
                    df = I._obj
                    return bodo.utils.conversion.box_if_dt64(bodo.hiframes.
                        pd_dataframe_ext.get_dataframe_data(df, eob__pehn)[
                        idx[0]])
                return impl
            return _gen_iloc_getitem_row_impl(df, col_names, 'idx[0]')
        if is_list_like_index_type(idx.types[0]) and isinstance(idx.types[0
            ].dtype, (types.Integer, types.Boolean)) or isinstance(idx.
            types[0], types.SliceType):
            return _gen_iloc_getitem_bool_slice_impl(df, col_names, idx.
                types[0], 'idx[0]', is_out_series)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, (types.
        Integer, types.Boolean)) or isinstance(idx, types.SliceType):
        return _gen_iloc_getitem_bool_slice_impl(df, df.columns, idx, 'idx',
            False)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):
        raise_bodo_error(
            'slice2 in df.iloc[slice1,slice2] should be constant. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
            )
    raise_bodo_error(f'df.iloc[] getitem using {idx} not supported')


def _gen_iloc_getitem_bool_slice_impl(df, col_names, idx_typ, idx,
    is_out_series):
    erk__pihgm = 'def impl(I, idx):\n'
    erk__pihgm += '  df = I._obj\n'
    if isinstance(idx_typ, types.SliceType):
        erk__pihgm += f'  idx_t = {idx}\n'
    else:
        erk__pihgm += (
            f'  idx_t = bodo.utils.conversion.coerce_to_ndarray({idx})\n')
    xvq__jfcr = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]'
    nvleu__ffbmo = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(ybth__crim)})[idx_t]'
         for ybth__crim in col_names)
    if is_out_series:
        lzxtd__frdje = f"'{col_names[0]}'" if isinstance(col_names[0], str
            ) else f'{col_names[0]}'
        erk__pihgm += f"""  return bodo.hiframes.pd_series_ext.init_series({nvleu__ffbmo}, {xvq__jfcr}, {lzxtd__frdje})
"""
        bsft__sag = {}
        exec(erk__pihgm, {'bodo': bodo}, bsft__sag)
        return bsft__sag['impl']
    return bodo.hiframes.dataframe_impl._gen_init_df(erk__pihgm, col_names,
        nvleu__ffbmo, xvq__jfcr)


def _gen_iloc_getitem_row_impl(df, col_names, idx):
    erk__pihgm = 'def impl(I, idx):\n'
    erk__pihgm += '  df = I._obj\n'
    cipk__cyrx = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(ybth__crim)})[{idx}]'
         for ybth__crim in col_names)
    erk__pihgm += f"""  row_idx = bodo.hiframes.pd_index_ext.init_heter_index({gen_const_tup(col_names)}, None)
"""
    erk__pihgm += f"""  return bodo.hiframes.pd_series_ext.init_series(({cipk__cyrx},), row_idx, None)
"""
    bsft__sag = {}
    exec(erk__pihgm, {'bodo': bodo}, bsft__sag)
    impl = bsft__sag['impl']
    return impl


@overload(operator.setitem, no_unliteral=True)
def df_iloc_setitem_overload(df, idx, val):
    if not isinstance(df, DataFrameILocType):
        return
    raise_bodo_error(
        f'DataFrame.iloc setitem unsupported for dataframe {df.df_type}, index {idx}, value {val}'
        )


class DataFrameLocType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        ylmiq__mzug = 'DataFrameLocType({})'.format(df_type)
        super(DataFrameLocType, self).__init__(ylmiq__mzug)
    ndim = 2


@register_model(DataFrameLocType)
class DataFrameLocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        fhocv__uipu = [('obj', fe_type.df_type)]
        super(DataFrameLocModel, self).__init__(dmm, fe_type, fhocv__uipu)


make_attribute_wrapper(DataFrameLocType, 'obj', '_obj')


@intrinsic
def init_dataframe_loc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        qef__znb, = args
        hnbg__edxv = signature.return_type
        jgdv__uvh = cgutils.create_struct_proxy(hnbg__edxv)(context, builder)
        jgdv__uvh.obj = qef__znb
        context.nrt.incref(builder, signature.args[0], qef__znb)
        return jgdv__uvh._getvalue()
    return DataFrameLocType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'loc')
def overload_dataframe_loc(s):
    return lambda s: bodo.hiframes.dataframe_indexing.init_dataframe_loc(s)


@lower_builtin(operator.getitem, DataFrameLocType, types.Any)
def loc_getitem_lower(context, builder, sig, args):
    impl = overload_loc_getitem(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def overload_loc_getitem(I, idx):
    if not isinstance(I, DataFrameLocType):
        return
    df = I.df_type
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        erk__pihgm = 'def impl(I, idx):\n'
        erk__pihgm += '  df = I._obj\n'
        erk__pihgm += (
            '  idx_t = bodo.utils.conversion.coerce_to_ndarray(idx)\n')
        xvq__jfcr = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
        nvleu__ffbmo = ', '.join(
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})[idx_t]'
            .format(df.columns.index(ybth__crim)) for ybth__crim in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(erk__pihgm, df.
            columns, nvleu__ffbmo, xvq__jfcr)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        rlh__nod = idx.types[1]
        if is_overload_constant_str(rlh__nod):
            zmh__cghn = get_overload_const_str(rlh__nod)
            eob__pehn = df.columns.index(zmh__cghn)

            def impl_col_name(I, idx):
                df = I._obj
                xvq__jfcr = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
                    df)
                eqnm__rkh = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
                    df, eob__pehn)
                return bodo.hiframes.pd_series_ext.init_series(eqnm__rkh,
                    xvq__jfcr, zmh__cghn).loc[idx[0]]
            return impl_col_name
        if is_overload_constant_list(rlh__nod):
            col_idx_list = get_overload_const_list(rlh__nod)
            if len(col_idx_list) > 0 and not isinstance(col_idx_list[0], (
                bool, np.bool_)) and not all(ybth__crim in df.columns for
                ybth__crim in col_idx_list):
                raise_bodo_error(
                    f'DataFrame.loc[]: invalid column list {col_idx_list}; not all in dataframe columns {df.columns}'
                    )
            return gen_df_loc_col_select_impl(df, col_idx_list)
    raise_bodo_error(
        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
        )


def gen_df_loc_col_select_impl(df, col_idx_list):
    if len(col_idx_list) > 0 and isinstance(col_idx_list[0], (bool, np.bool_)):
        col_idx_list = list(pd.Series(df.columns, dtype=object)[col_idx_list])
    nvleu__ffbmo = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})[idx[0]]'
        .format(df.columns.index(ybth__crim)) for ybth__crim in col_idx_list)
    xvq__jfcr = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx[0]]')
    erk__pihgm = 'def impl(I, idx):\n'
    erk__pihgm += '  df = I._obj\n'
    return bodo.hiframes.dataframe_impl._gen_init_df(erk__pihgm,
        col_idx_list, nvleu__ffbmo, xvq__jfcr)


@overload(operator.setitem, no_unliteral=True)
def df_loc_setitem_overload(df, idx, val):
    if not isinstance(df, DataFrameLocType):
        return
    raise_bodo_error(
        f'DataFrame.loc setitem unsupported for dataframe {df.df_type}, index {idx}, value {val}'
        )


class DataFrameIatType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        ylmiq__mzug = 'DataFrameIatType({})'.format(df_type)
        super(DataFrameIatType, self).__init__(ylmiq__mzug)
    ndim = 2


@register_model(DataFrameIatType)
class DataFrameIatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        fhocv__uipu = [('obj', fe_type.df_type)]
        super(DataFrameIatModel, self).__init__(dmm, fe_type, fhocv__uipu)


make_attribute_wrapper(DataFrameIatType, 'obj', '_obj')


@intrinsic
def init_dataframe_iat(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        qef__znb, = args
        wmvsp__lhhxl = signature.return_type
        prsu__zzha = cgutils.create_struct_proxy(wmvsp__lhhxl)(context, builder
            )
        prsu__zzha.obj = qef__znb
        context.nrt.incref(builder, signature.args[0], qef__znb)
        return prsu__zzha._getvalue()
    return DataFrameIatType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'iat')
def overload_series_iat(s):
    return lambda s: bodo.hiframes.dataframe_indexing.init_dataframe_iat(s)


@overload(operator.getitem, no_unliteral=True)
def overload_iat_getitem(I, idx):
    if not isinstance(I, DataFrameIatType):
        return
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        if not isinstance(idx.types[0], types.Integer):
            raise BodoError(
                'DataFrame.iat: iAt based indexing can only have integer indexers'
                )
        if not is_overload_constant_int(idx.types[1]):
            raise_bodo_error(
                'DataFrame.iat getitem: column index must be a constant integer. For more informaton, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
                )
        eob__pehn = get_overload_const_int(idx.types[1])

        def impl_col_ind(I, idx):
            df = I._obj
            eqnm__rkh = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                eob__pehn)
            return eqnm__rkh[idx[0]]
        return impl_col_ind
    raise BodoError('df.iat[] getitem using {} not supported'.format(idx))


@overload(operator.setitem, no_unliteral=True)
def overload_iat_setitem(I, idx, val):
    if not isinstance(I, DataFrameIatType):
        return
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        if not isinstance(idx.types[0], types.Integer):
            raise BodoError(
                'DataFrame.iat: iAt based indexing can only have integer indexers'
                )
        if not is_overload_constant_int(idx.types[1]):
            raise_bodo_error(
                'DataFrame.iat setitem: column index must be a constant integer. For more informaton, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html'
                )
        eob__pehn = get_overload_const_int(idx.types[1])
        if is_immutable_array(I.df_type.data[eob__pehn]):
            raise BodoError(
                f'DataFrame setitem not supported for column with immutable array type {I.df_type.data}'
                )

        def impl_col_ind(I, idx, val):
            df = I._obj
            eqnm__rkh = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                eob__pehn)
            eqnm__rkh[idx[0]] = bodo.utils.conversion.unbox_if_timestamp(val)
        return impl_col_ind
    raise BodoError('df.iat[] setitem using {} not supported'.format(idx))


@lower_cast(DataFrameIatType, DataFrameIatType)
@lower_cast(DataFrameILocType, DataFrameILocType)
@lower_cast(DataFrameLocType, DataFrameLocType)
def cast_series_iat(context, builder, fromty, toty, val):
    prsu__zzha = cgutils.create_struct_proxy(fromty)(context, builder, val)
    dpop__dkwz = context.cast(builder, prsu__zzha.obj, fromty.df_type, toty
        .df_type)
    wzyf__gweb = cgutils.create_struct_proxy(toty)(context, builder)
    wzyf__gweb.obj = dpop__dkwz
    return wzyf__gweb._getvalue()
