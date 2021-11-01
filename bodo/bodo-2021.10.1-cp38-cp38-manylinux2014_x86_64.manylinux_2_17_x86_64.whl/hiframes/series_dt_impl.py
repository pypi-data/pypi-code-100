"""
Support for Series.dt attributes and methods
"""
import datetime
import operator
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import intrinsic, make_attribute_wrapper, models, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, raise_bodo_error
dt64_dtype = np.dtype('datetime64[ns]')
timedelta64_dtype = np.dtype('timedelta64[ns]')


class SeriesDatetimePropertiesType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        amc__lqw = 'SeriesDatetimePropertiesType({})'.format(stype)
        super(SeriesDatetimePropertiesType, self).__init__(amc__lqw)


@register_model(SeriesDatetimePropertiesType)
class SeriesDtModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        vteka__clkhh = [('obj', fe_type.stype)]
        super(SeriesDtModel, self).__init__(dmm, fe_type, vteka__clkhh)


make_attribute_wrapper(SeriesDatetimePropertiesType, 'obj', '_obj')


@intrinsic
def init_series_dt_properties(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        yyg__fky, = args
        xvdz__mna = signature.return_type
        yzbfw__yit = cgutils.create_struct_proxy(xvdz__mna)(context, builder)
        yzbfw__yit.obj = yyg__fky
        context.nrt.incref(builder, signature.args[0], yyg__fky)
        return yzbfw__yit._getvalue()
    return SeriesDatetimePropertiesType(obj)(obj), codegen


@overload_attribute(SeriesType, 'dt')
def overload_series_dt(s):
    if not (bodo.hiframes.pd_series_ext.is_dt64_series_typ(s) or bodo.
        hiframes.pd_series_ext.is_timedelta64_series_typ(s)):
        raise_bodo_error('Can only use .dt accessor with datetimelike values.')
    return lambda s: bodo.hiframes.series_dt_impl.init_series_dt_properties(s)


def create_date_field_overload(field):

    def overload_field(S_dt):
        if not S_dt.stype.dtype == types.NPDatetime('ns'):
            return
        dyl__few = 'def impl(S_dt):\n'
        dyl__few += '    S = S_dt._obj\n'
        dyl__few += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        dyl__few += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        dyl__few += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        dyl__few += '    numba.parfors.parfor.init_prange()\n'
        dyl__few += '    n = len(arr)\n'
        if field in ('is_leap_year', 'is_month_start', 'is_month_end',
            'is_quarter_start', 'is_quarter_end', 'is_year_start',
            'is_year_end'):
            dyl__few += '    out_arr = np.empty(n, np.bool_)\n'
        else:
            dyl__few += (
                '    out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n'
                )
        dyl__few += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        dyl__few += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        dyl__few += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
        dyl__few += '            continue\n'
        dyl__few += (
            '        dt64 = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arr[i])\n'
            )
        if field in ('year', 'month', 'day'):
            dyl__few += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            if field in ('month', 'day'):
                dyl__few += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            dyl__few += '        out_arr[i] = {}\n'.format(field)
        elif field in ('dayofyear', 'dayofweek', 'weekday'):
            tupwu__mwa = {'dayofyear': 'get_day_of_year', 'dayofweek':
                'get_day_of_week', 'weekday': 'get_day_of_week'}
            dyl__few += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            dyl__few += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            dyl__few += (
                """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month, day)
"""
                .format(tupwu__mwa[field]))
        elif field == 'is_leap_year':
            dyl__few += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            dyl__few += (
                '        out_arr[i] = bodo.hiframes.pd_timestamp_ext.is_leap_year(year)\n'
                )
        elif field in ('daysinmonth', 'days_in_month'):
            tupwu__mwa = {'days_in_month': 'get_days_in_month',
                'daysinmonth': 'get_days_in_month'}
            dyl__few += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            dyl__few += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            dyl__few += (
                '        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month)\n'
                .format(tupwu__mwa[field]))
        else:
            dyl__few += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(dt64)
"""
            dyl__few += '        out_arr[i] = ts.' + field + '\n'
        dyl__few += (
            '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        jvi__vwu = {}
        exec(dyl__few, {'bodo': bodo, 'numba': numba, 'np': np}, jvi__vwu)
        impl = jvi__vwu['impl']
        return impl
    return overload_field


def _install_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        gmm__rybr = create_date_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(gmm__rybr)


_install_date_fields()


def create_date_method_overload(method):
    jgpo__bvm = method in ['day_name', 'month_name']

    def overload_method(S_dt):
        if not S_dt.stype.dtype == types.NPDatetime('ns'):
            return
        dyl__few = 'def impl(S_dt):\n'
        dyl__few += '    S = S_dt._obj\n'
        dyl__few += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        dyl__few += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        dyl__few += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        dyl__few += '    numba.parfors.parfor.init_prange()\n'
        dyl__few += '    n = len(arr)\n'
        if jgpo__bvm:
            dyl__few += """    out_arr = bodo.utils.utils.alloc_type(n, bodo.string_array_type, (-1,))
"""
        else:
            dyl__few += (
                "    out_arr = np.empty(n, np.dtype('datetime64[ns]'))\n")
        dyl__few += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        dyl__few += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        dyl__few += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
        dyl__few += '            continue\n'
        dyl__few += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(arr[i])
"""
        dyl__few += f'        method_val = ts.{method}()\n'
        if jgpo__bvm:
            dyl__few += '        out_arr[i] = method_val\n'
        else:
            dyl__few += """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(method_val.value)
"""
        dyl__few += (
            '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        jvi__vwu = {}
        exec(dyl__few, {'bodo': bodo, 'numba': numba, 'np': np}, jvi__vwu)
        impl = jvi__vwu['impl']
        return impl
    return overload_method


def _install_date_methods():
    for method in bodo.hiframes.pd_timestamp_ext.date_methods:
        gmm__rybr = create_date_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            gmm__rybr)


_install_date_methods()


@overload_attribute(SeriesDatetimePropertiesType, 'date')
def series_dt_date_overload(S_dt):
    if not S_dt.stype.dtype == types.NPDatetime('ns'):
        return

    def impl(S_dt):
        xzns__wdy = S_dt._obj
        szcul__pzug = bodo.hiframes.pd_series_ext.get_series_data(xzns__wdy)
        keyt__vrrgv = bodo.hiframes.pd_series_ext.get_series_index(xzns__wdy)
        amc__lqw = bodo.hiframes.pd_series_ext.get_series_name(xzns__wdy)
        numba.parfors.parfor.init_prange()
        kfwxt__xnrte = len(szcul__pzug)
        ema__byic = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
            kfwxt__xnrte)
        for ngvn__oit in numba.parfors.parfor.internal_prange(kfwxt__xnrte):
            muor__hxfd = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                szcul__pzug[ngvn__oit])
            cltn__nofpe = (bodo.hiframes.pd_timestamp_ext.
                convert_datetime64_to_timestamp(muor__hxfd))
            ema__byic[ngvn__oit] = datetime.date(cltn__nofpe.year,
                cltn__nofpe.month, cltn__nofpe.day)
        return bodo.hiframes.pd_series_ext.init_series(ema__byic,
            keyt__vrrgv, amc__lqw)
    return impl


def create_series_dt_df_output_overload(attr):

    def series_dt_df_output_overload(S_dt):
        if not (attr == 'components' and S_dt.stype.dtype == types.
            NPTimedelta('ns') or attr == 'isocalendar' and S_dt.stype.dtype ==
            types.NPDatetime('ns')):
            return
        if attr == 'components':
            vsr__dwrxu = ['days', 'hours', 'minutes', 'seconds',
                'milliseconds', 'microseconds', 'nanoseconds']
            muqcb__zio = 'convert_numpy_timedelta64_to_pd_timedelta'
            rdwkg__dpxjq = 'np.empty(n, np.int64)'
            wzlfp__dknc = attr
        elif attr == 'isocalendar':
            vsr__dwrxu = ['year', 'week', 'day']
            muqcb__zio = 'convert_datetime64_to_timestamp'
            rdwkg__dpxjq = (
                'bodo.libs.int_arr_ext.alloc_int_array(n, np.uint32)')
            wzlfp__dknc = attr + '()'
        dyl__few = 'def impl(S_dt):\n'
        dyl__few += '    S = S_dt._obj\n'
        dyl__few += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        dyl__few += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        dyl__few += '    numba.parfors.parfor.init_prange()\n'
        dyl__few += '    n = len(arr)\n'
        for field in vsr__dwrxu:
            dyl__few += '    {} = {}\n'.format(field, rdwkg__dpxjq)
        dyl__few += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        dyl__few += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        for field in vsr__dwrxu:
            dyl__few += ('            bodo.libs.array_kernels.setna({}, i)\n'
                .format(field))
        dyl__few += '            continue\n'
        jqufq__emr = '(' + '[i], '.join(vsr__dwrxu) + '[i])'
        dyl__few += (
            '        {} = bodo.hiframes.pd_timestamp_ext.{}(arr[i]).{}\n'.
            format(jqufq__emr, muqcb__zio, wzlfp__dknc))
        zel__odle = '(' + ', '.join(vsr__dwrxu) + ')'
        frspl__mnle = "('" + "', '".join(vsr__dwrxu) + "')"
        dyl__few += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, index, {})\n'
            .format(zel__odle, frspl__mnle))
        jvi__vwu = {}
        exec(dyl__few, {'bodo': bodo, 'numba': numba, 'np': np}, jvi__vwu)
        impl = jvi__vwu['impl']
        return impl
    return series_dt_df_output_overload


def _install_df_output_overload():
    zipj__duxl = [('components', overload_attribute), ('isocalendar',
        overload_method)]
    for attr, hmv__fnl in zipj__duxl:
        gmm__rybr = create_series_dt_df_output_overload(attr)
        hmv__fnl(SeriesDatetimePropertiesType, attr, inline='always')(gmm__rybr
            )


_install_df_output_overload()


def create_timedelta_field_overload(field):

    def overload_field(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        dyl__few = 'def impl(S_dt):\n'
        dyl__few += '    S = S_dt._obj\n'
        dyl__few += '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        dyl__few += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        dyl__few += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        dyl__few += '    numba.parfors.parfor.init_prange()\n'
        dyl__few += '    n = len(A)\n'
        dyl__few += (
            '    B = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
        dyl__few += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        dyl__few += '        if bodo.libs.array_kernels.isna(A, i):\n'
        dyl__few += '            bodo.libs.array_kernels.setna(B, i)\n'
        dyl__few += '            continue\n'
        dyl__few += (
            '        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])\n'
            )
        if field == 'nanoseconds':
            dyl__few += '        B[i] = td64 % 1000\n'
        elif field == 'microseconds':
            dyl__few += '        B[i] = td64 // 1000 % 1000000\n'
        elif field == 'seconds':
            dyl__few += (
                '        B[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
        elif field == 'days':
            dyl__few += (
                '        B[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
        else:
            assert False, 'invalid timedelta field'
        dyl__few += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        jvi__vwu = {}
        exec(dyl__few, {'numba': numba, 'np': np, 'bodo': bodo}, jvi__vwu)
        impl = jvi__vwu['impl']
        return impl
    return overload_field


def create_timedelta_method_overload(method):

    def overload_method(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        dyl__few = 'def impl(S_dt):\n'
        dyl__few += '    S = S_dt._obj\n'
        dyl__few += '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        dyl__few += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        dyl__few += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        dyl__few += '    numba.parfors.parfor.init_prange()\n'
        dyl__few += '    n = len(A)\n'
        if method == 'total_seconds':
            dyl__few += '    B = np.empty(n, np.float64)\n'
        else:
            dyl__few += """    B = bodo.hiframes.datetime_timedelta_ext.alloc_datetime_timedelta_array(n)
"""
        dyl__few += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        dyl__few += '        if bodo.libs.array_kernels.isna(A, i):\n'
        dyl__few += '            bodo.libs.array_kernels.setna(B, i)\n'
        dyl__few += '            continue\n'
        dyl__few += (
            '        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])\n'
            )
        if method == 'total_seconds':
            dyl__few += '        B[i] = td64 / (1000.0 * 1000000.0)\n'
        elif method == 'to_pytimedelta':
            dyl__few += (
                '        B[i] = datetime.timedelta(microseconds=td64 // 1000)\n'
                )
        else:
            assert False, 'invalid timedelta method'
        if method == 'total_seconds':
            dyl__few += (
                '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
                )
        else:
            dyl__few += '    return B\n'
        jvi__vwu = {}
        exec(dyl__few, {'numba': numba, 'np': np, 'bodo': bodo, 'datetime':
            datetime}, jvi__vwu)
        impl = jvi__vwu['impl']
        return impl
    return overload_method


def _install_S_dt_timedelta_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        gmm__rybr = create_timedelta_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(gmm__rybr)


_install_S_dt_timedelta_fields()


def _install_S_dt_timedelta_methods():
    for method in bodo.hiframes.pd_timestamp_ext.timedelta_methods:
        gmm__rybr = create_timedelta_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            gmm__rybr)


_install_S_dt_timedelta_methods()


@overload_method(SeriesDatetimePropertiesType, 'strftime', inline='always',
    no_unliteral=True)
def dt_strftime(S_dt, format_str):
    if S_dt.stype.dtype != types.NPDatetime('ns'):
        return

    def impl(S_dt, format_str):
        xzns__wdy = S_dt._obj
        pbyp__qwqr = bodo.hiframes.pd_series_ext.get_series_data(xzns__wdy)
        keyt__vrrgv = bodo.hiframes.pd_series_ext.get_series_index(xzns__wdy)
        amc__lqw = bodo.hiframes.pd_series_ext.get_series_name(xzns__wdy)
        numba.parfors.parfor.init_prange()
        kfwxt__xnrte = len(pbyp__qwqr)
        cyha__mvcnn = bodo.libs.str_arr_ext.pre_alloc_string_array(kfwxt__xnrte
            , -1)
        for htyc__ybhjf in numba.parfors.parfor.internal_prange(kfwxt__xnrte):
            if bodo.libs.array_kernels.isna(pbyp__qwqr, htyc__ybhjf):
                bodo.libs.array_kernels.setna(cyha__mvcnn, htyc__ybhjf)
                continue
            cyha__mvcnn[htyc__ybhjf
                ] = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(
                pbyp__qwqr[htyc__ybhjf]).strftime(format_str)
        return bodo.hiframes.pd_series_ext.init_series(cyha__mvcnn,
            keyt__vrrgv, amc__lqw)
    return impl


def create_timedelta_freq_overload(method):

    def freq_overload(S_dt, freq, ambiguous='raise', nonexistent='raise'):
        if S_dt.stype.dtype != types.NPTimedelta('ns'
            ) and S_dt.stype.dtype != types.NPDatetime('ns'):
            return
        rmmy__lrj = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        jtx__frpfq = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args('floor', rmmy__lrj, jtx__frpfq)
        dyl__few = (
            "def impl(S_dt, freq, ambiguous='raise', nonexistent='raise'):\n")
        dyl__few += '    S = S_dt._obj\n'
        dyl__few += '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        dyl__few += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        dyl__few += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        dyl__few += '    numba.parfors.parfor.init_prange()\n'
        dyl__few += '    n = len(A)\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            dyl__few += "    B = np.empty(n, np.dtype('timedelta64[ns]'))\n"
        else:
            dyl__few += "    B = np.empty(n, np.dtype('datetime64[ns]'))\n"
        dyl__few += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        dyl__few += '        if bodo.libs.array_kernels.isna(A, i):\n'
        dyl__few += '            bodo.libs.array_kernels.setna(B, i)\n'
        dyl__few += '            continue\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            xxd__xcib = (
                'bodo.hiframes.pd_timestamp_ext.convert_numpy_timedelta64_to_pd_timedelta'
                )
            fvypy__tmi = (
                'bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64')
        else:
            xxd__xcib = (
                'bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp'
                )
            fvypy__tmi = 'bodo.hiframes.pd_timestamp_ext.integer_to_dt64'
        dyl__few += '        B[i] = {}({}(A[i]).{}(freq).value)\n'.format(
            fvypy__tmi, xxd__xcib, method)
        dyl__few += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        jvi__vwu = {}
        exec(dyl__few, {'numba': numba, 'np': np, 'bodo': bodo}, jvi__vwu)
        impl = jvi__vwu['impl']
        return impl
    return freq_overload


def _install_S_dt_timedelta_freq_methods():
    nzd__pesi = ['ceil', 'floor', 'round']
    for method in nzd__pesi:
        gmm__rybr = create_timedelta_freq_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            gmm__rybr)


_install_S_dt_timedelta_freq_methods()


def create_bin_op_overload(op):

    def overload_series_dt_binop(lhs, rhs):
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs):
            yjujv__riof = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                dqqb__lzyza = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                keyt__vrrgv = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                amc__lqw = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                xump__gke = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                kfwxt__xnrte = len(dqqb__lzyza)
                xzns__wdy = np.empty(kfwxt__xnrte, timedelta64_dtype)
                zspg__bfead = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yjujv__riof)
                for ngvn__oit in numba.parfors.parfor.internal_prange(
                    kfwxt__xnrte):
                    qxf__qhyu = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        dqqb__lzyza[ngvn__oit])
                    tts__iewii = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(xump__gke[ngvn__oit]))
                    if qxf__qhyu == zspg__bfead or tts__iewii == zspg__bfead:
                        cej__ijcik = zspg__bfead
                    else:
                        cej__ijcik = op(qxf__qhyu, tts__iewii)
                    xzns__wdy[ngvn__oit
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        cej__ijcik)
                return bodo.hiframes.pd_series_ext.init_series(xzns__wdy,
                    keyt__vrrgv, amc__lqw)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs):
            yjujv__riof = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                szcul__pzug = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                keyt__vrrgv = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                amc__lqw = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                xump__gke = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                kfwxt__xnrte = len(szcul__pzug)
                xzns__wdy = np.empty(kfwxt__xnrte, dt64_dtype)
                zspg__bfead = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yjujv__riof)
                for ngvn__oit in numba.parfors.parfor.internal_prange(
                    kfwxt__xnrte):
                    gidul__mpxjk = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(szcul__pzug[ngvn__oit]))
                    sjql__dlqt = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(xump__gke[ngvn__oit]))
                    if (gidul__mpxjk == zspg__bfead or sjql__dlqt ==
                        zspg__bfead):
                        cej__ijcik = zspg__bfead
                    else:
                        cej__ijcik = op(gidul__mpxjk, sjql__dlqt)
                    xzns__wdy[ngvn__oit
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        cej__ijcik)
                return bodo.hiframes.pd_series_ext.init_series(xzns__wdy,
                    keyt__vrrgv, amc__lqw)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs):
            yjujv__riof = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                szcul__pzug = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                keyt__vrrgv = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                amc__lqw = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                xump__gke = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                kfwxt__xnrte = len(szcul__pzug)
                xzns__wdy = np.empty(kfwxt__xnrte, dt64_dtype)
                zspg__bfead = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yjujv__riof)
                for ngvn__oit in numba.parfors.parfor.internal_prange(
                    kfwxt__xnrte):
                    gidul__mpxjk = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(szcul__pzug[ngvn__oit]))
                    sjql__dlqt = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(xump__gke[ngvn__oit]))
                    if (gidul__mpxjk == zspg__bfead or sjql__dlqt ==
                        zspg__bfead):
                        cej__ijcik = zspg__bfead
                    else:
                        cej__ijcik = op(gidul__mpxjk, sjql__dlqt)
                    xzns__wdy[ngvn__oit
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        cej__ijcik)
                return bodo.hiframes.pd_series_ext.init_series(xzns__wdy,
                    keyt__vrrgv, amc__lqw)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            yjujv__riof = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                szcul__pzug = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                keyt__vrrgv = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                amc__lqw = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                kfwxt__xnrte = len(szcul__pzug)
                xzns__wdy = np.empty(kfwxt__xnrte, timedelta64_dtype)
                zspg__bfead = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yjujv__riof)
                cjiw__wvm = rhs.value
                for ngvn__oit in numba.parfors.parfor.internal_prange(
                    kfwxt__xnrte):
                    gidul__mpxjk = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(szcul__pzug[ngvn__oit]))
                    if gidul__mpxjk == zspg__bfead or cjiw__wvm == zspg__bfead:
                        cej__ijcik = zspg__bfead
                    else:
                        cej__ijcik = op(gidul__mpxjk, cjiw__wvm)
                    xzns__wdy[ngvn__oit
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        cej__ijcik)
                return bodo.hiframes.pd_series_ext.init_series(xzns__wdy,
                    keyt__vrrgv, amc__lqw)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            yjujv__riof = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                szcul__pzug = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                keyt__vrrgv = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                amc__lqw = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                kfwxt__xnrte = len(szcul__pzug)
                xzns__wdy = np.empty(kfwxt__xnrte, timedelta64_dtype)
                zspg__bfead = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yjujv__riof)
                cjiw__wvm = lhs.value
                for ngvn__oit in numba.parfors.parfor.internal_prange(
                    kfwxt__xnrte):
                    gidul__mpxjk = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(szcul__pzug[ngvn__oit]))
                    if cjiw__wvm == zspg__bfead or gidul__mpxjk == zspg__bfead:
                        cej__ijcik = zspg__bfead
                    else:
                        cej__ijcik = op(cjiw__wvm, gidul__mpxjk)
                    xzns__wdy[ngvn__oit
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        cej__ijcik)
                return bodo.hiframes.pd_series_ext.init_series(xzns__wdy,
                    keyt__vrrgv, amc__lqw)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            yjujv__riof = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                szcul__pzug = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                keyt__vrrgv = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                amc__lqw = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                kfwxt__xnrte = len(szcul__pzug)
                xzns__wdy = np.empty(kfwxt__xnrte, dt64_dtype)
                zspg__bfead = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yjujv__riof)
                xkvv__jpkm = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                sjql__dlqt = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(xkvv__jpkm))
                for ngvn__oit in numba.parfors.parfor.internal_prange(
                    kfwxt__xnrte):
                    gidul__mpxjk = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(szcul__pzug[ngvn__oit]))
                    if (gidul__mpxjk == zspg__bfead or sjql__dlqt ==
                        zspg__bfead):
                        cej__ijcik = zspg__bfead
                    else:
                        cej__ijcik = op(gidul__mpxjk, sjql__dlqt)
                    xzns__wdy[ngvn__oit
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        cej__ijcik)
                return bodo.hiframes.pd_series_ext.init_series(xzns__wdy,
                    keyt__vrrgv, amc__lqw)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            yjujv__riof = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                szcul__pzug = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                keyt__vrrgv = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                amc__lqw = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                kfwxt__xnrte = len(szcul__pzug)
                xzns__wdy = np.empty(kfwxt__xnrte, dt64_dtype)
                zspg__bfead = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yjujv__riof)
                xkvv__jpkm = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                sjql__dlqt = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(xkvv__jpkm))
                for ngvn__oit in numba.parfors.parfor.internal_prange(
                    kfwxt__xnrte):
                    gidul__mpxjk = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(szcul__pzug[ngvn__oit]))
                    if (gidul__mpxjk == zspg__bfead or sjql__dlqt ==
                        zspg__bfead):
                        cej__ijcik = zspg__bfead
                    else:
                        cej__ijcik = op(gidul__mpxjk, sjql__dlqt)
                    xzns__wdy[ngvn__oit
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        cej__ijcik)
                return bodo.hiframes.pd_series_ext.init_series(xzns__wdy,
                    keyt__vrrgv, amc__lqw)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            yjujv__riof = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                szcul__pzug = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                keyt__vrrgv = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                amc__lqw = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                kfwxt__xnrte = len(szcul__pzug)
                xzns__wdy = np.empty(kfwxt__xnrte, timedelta64_dtype)
                zspg__bfead = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yjujv__riof)
                muor__hxfd = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(rhs))
                gidul__mpxjk = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    muor__hxfd)
                for ngvn__oit in numba.parfors.parfor.internal_prange(
                    kfwxt__xnrte):
                    vrpp__fbxym = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(szcul__pzug[ngvn__oit]))
                    if (vrpp__fbxym == zspg__bfead or gidul__mpxjk ==
                        zspg__bfead):
                        cej__ijcik = zspg__bfead
                    else:
                        cej__ijcik = op(vrpp__fbxym, gidul__mpxjk)
                    xzns__wdy[ngvn__oit
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        cej__ijcik)
                return bodo.hiframes.pd_series_ext.init_series(xzns__wdy,
                    keyt__vrrgv, amc__lqw)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            yjujv__riof = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                szcul__pzug = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                keyt__vrrgv = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                amc__lqw = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                kfwxt__xnrte = len(szcul__pzug)
                xzns__wdy = np.empty(kfwxt__xnrte, timedelta64_dtype)
                zspg__bfead = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yjujv__riof)
                muor__hxfd = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(lhs))
                gidul__mpxjk = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    muor__hxfd)
                for ngvn__oit in numba.parfors.parfor.internal_prange(
                    kfwxt__xnrte):
                    vrpp__fbxym = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(szcul__pzug[ngvn__oit]))
                    if (gidul__mpxjk == zspg__bfead or vrpp__fbxym ==
                        zspg__bfead):
                        cej__ijcik = zspg__bfead
                    else:
                        cej__ijcik = op(gidul__mpxjk, vrpp__fbxym)
                    xzns__wdy[ngvn__oit
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        cej__ijcik)
                return bodo.hiframes.pd_series_ext.init_series(xzns__wdy,
                    keyt__vrrgv, amc__lqw)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            yjujv__riof = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                szcul__pzug = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                keyt__vrrgv = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                amc__lqw = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                kfwxt__xnrte = len(szcul__pzug)
                xzns__wdy = np.empty(kfwxt__xnrte, timedelta64_dtype)
                zspg__bfead = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(yjujv__riof))
                xkvv__jpkm = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                sjql__dlqt = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(xkvv__jpkm))
                for ngvn__oit in numba.parfors.parfor.internal_prange(
                    kfwxt__xnrte):
                    rwsb__spf = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(szcul__pzug[ngvn__oit]))
                    if sjql__dlqt == zspg__bfead or rwsb__spf == zspg__bfead:
                        cej__ijcik = zspg__bfead
                    else:
                        cej__ijcik = op(rwsb__spf, sjql__dlqt)
                    xzns__wdy[ngvn__oit
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        cej__ijcik)
                return bodo.hiframes.pd_series_ext.init_series(xzns__wdy,
                    keyt__vrrgv, amc__lqw)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            yjujv__riof = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                szcul__pzug = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                keyt__vrrgv = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                amc__lqw = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                kfwxt__xnrte = len(szcul__pzug)
                xzns__wdy = np.empty(kfwxt__xnrte, timedelta64_dtype)
                zspg__bfead = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(yjujv__riof))
                xkvv__jpkm = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                sjql__dlqt = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(xkvv__jpkm))
                for ngvn__oit in numba.parfors.parfor.internal_prange(
                    kfwxt__xnrte):
                    rwsb__spf = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(szcul__pzug[ngvn__oit]))
                    if sjql__dlqt == zspg__bfead or rwsb__spf == zspg__bfead:
                        cej__ijcik = zspg__bfead
                    else:
                        cej__ijcik = op(sjql__dlqt, rwsb__spf)
                    xzns__wdy[ngvn__oit
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        cej__ijcik)
                return bodo.hiframes.pd_series_ext.init_series(xzns__wdy,
                    keyt__vrrgv, amc__lqw)
            return impl
        raise BodoError(f'{op} not supported for data types {lhs} and {rhs}.')
    return overload_series_dt_binop


def create_cmp_op_overload(op):

    def overload_series_dt64_cmp(lhs, rhs):
        if op == operator.ne:
            nnyvv__cmho = True
        else:
            nnyvv__cmho = False
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            yjujv__riof = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                szcul__pzug = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                keyt__vrrgv = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                amc__lqw = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                kfwxt__xnrte = len(szcul__pzug)
                ema__byic = bodo.libs.bool_arr_ext.alloc_bool_array(
                    kfwxt__xnrte)
                zspg__bfead = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(yjujv__riof))
                klugq__vriw = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                wvei__aik = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(klugq__vriw))
                for ngvn__oit in numba.parfors.parfor.internal_prange(
                    kfwxt__xnrte):
                    wuv__ybud = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(szcul__pzug[ngvn__oit]))
                    if wuv__ybud == zspg__bfead or wvei__aik == zspg__bfead:
                        cej__ijcik = nnyvv__cmho
                    else:
                        cej__ijcik = op(wuv__ybud, wvei__aik)
                    ema__byic[ngvn__oit] = cej__ijcik
                return bodo.hiframes.pd_series_ext.init_series(ema__byic,
                    keyt__vrrgv, amc__lqw)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            yjujv__riof = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                szcul__pzug = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                keyt__vrrgv = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                amc__lqw = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                kfwxt__xnrte = len(szcul__pzug)
                ema__byic = bodo.libs.bool_arr_ext.alloc_bool_array(
                    kfwxt__xnrte)
                zspg__bfead = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(yjujv__riof))
                toqm__dbhf = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                wuv__ybud = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(toqm__dbhf))
                for ngvn__oit in numba.parfors.parfor.internal_prange(
                    kfwxt__xnrte):
                    wvei__aik = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(szcul__pzug[ngvn__oit]))
                    if wuv__ybud == zspg__bfead or wvei__aik == zspg__bfead:
                        cej__ijcik = nnyvv__cmho
                    else:
                        cej__ijcik = op(wuv__ybud, wvei__aik)
                    ema__byic[ngvn__oit] = cej__ijcik
                return bodo.hiframes.pd_series_ext.init_series(ema__byic,
                    keyt__vrrgv, amc__lqw)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            yjujv__riof = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                szcul__pzug = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                keyt__vrrgv = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                amc__lqw = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                kfwxt__xnrte = len(szcul__pzug)
                ema__byic = bodo.libs.bool_arr_ext.alloc_bool_array(
                    kfwxt__xnrte)
                zspg__bfead = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yjujv__riof)
                for ngvn__oit in numba.parfors.parfor.internal_prange(
                    kfwxt__xnrte):
                    wuv__ybud = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        szcul__pzug[ngvn__oit])
                    if wuv__ybud == zspg__bfead or rhs.value == zspg__bfead:
                        cej__ijcik = nnyvv__cmho
                    else:
                        cej__ijcik = op(wuv__ybud, rhs.value)
                    ema__byic[ngvn__oit] = cej__ijcik
                return bodo.hiframes.pd_series_ext.init_series(ema__byic,
                    keyt__vrrgv, amc__lqw)
            return impl
        if (lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type and
            bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs)):
            yjujv__riof = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                szcul__pzug = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                keyt__vrrgv = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                amc__lqw = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                kfwxt__xnrte = len(szcul__pzug)
                ema__byic = bodo.libs.bool_arr_ext.alloc_bool_array(
                    kfwxt__xnrte)
                zspg__bfead = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yjujv__riof)
                for ngvn__oit in numba.parfors.parfor.internal_prange(
                    kfwxt__xnrte):
                    wvei__aik = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        szcul__pzug[ngvn__oit])
                    if wvei__aik == zspg__bfead or lhs.value == zspg__bfead:
                        cej__ijcik = nnyvv__cmho
                    else:
                        cej__ijcik = op(lhs.value, wvei__aik)
                    ema__byic[ngvn__oit] = cej__ijcik
                return bodo.hiframes.pd_series_ext.init_series(ema__byic,
                    keyt__vrrgv, amc__lqw)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (rhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(rhs)):
            yjujv__riof = lhs.dtype('NaT')

            def impl(lhs, rhs):
                szcul__pzug = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                keyt__vrrgv = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                amc__lqw = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                kfwxt__xnrte = len(szcul__pzug)
                ema__byic = bodo.libs.bool_arr_ext.alloc_bool_array(
                    kfwxt__xnrte)
                zspg__bfead = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yjujv__riof)
                rwoa__rhe = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    rhs)
                qofxt__uuru = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    rwoa__rhe)
                for ngvn__oit in numba.parfors.parfor.internal_prange(
                    kfwxt__xnrte):
                    wuv__ybud = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        szcul__pzug[ngvn__oit])
                    if wuv__ybud == zspg__bfead or qofxt__uuru == zspg__bfead:
                        cej__ijcik = nnyvv__cmho
                    else:
                        cej__ijcik = op(wuv__ybud, qofxt__uuru)
                    ema__byic[ngvn__oit] = cej__ijcik
                return bodo.hiframes.pd_series_ext.init_series(ema__byic,
                    keyt__vrrgv, amc__lqw)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (lhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(lhs)):
            yjujv__riof = rhs.dtype('NaT')

            def impl(lhs, rhs):
                szcul__pzug = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                keyt__vrrgv = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                amc__lqw = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                numba.parfors.parfor.init_prange()
                kfwxt__xnrte = len(szcul__pzug)
                ema__byic = bodo.libs.bool_arr_ext.alloc_bool_array(
                    kfwxt__xnrte)
                zspg__bfead = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    yjujv__riof)
                rwoa__rhe = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    lhs)
                qofxt__uuru = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    rwoa__rhe)
                for ngvn__oit in numba.parfors.parfor.internal_prange(
                    kfwxt__xnrte):
                    muor__hxfd = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(szcul__pzug[ngvn__oit]))
                    if muor__hxfd == zspg__bfead or qofxt__uuru == zspg__bfead:
                        cej__ijcik = nnyvv__cmho
                    else:
                        cej__ijcik = op(qofxt__uuru, muor__hxfd)
                    ema__byic[ngvn__oit] = cej__ijcik
                return bodo.hiframes.pd_series_ext.init_series(ema__byic,
                    keyt__vrrgv, amc__lqw)
            return impl
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_series_dt64_cmp


series_dt_unsupported_methods = {'asfreq', 'normalize', 'to_period',
    'to_pydatetime', 'to_timestamp', 'tz_convert', 'tz_localize'}
series_dt_unsupported_attrs = {'end_time', 'freq', 'qyear', 'start_time',
    'time', 'timetz', 'tz', 'week', 'weekday', 'weekofyear'}


def _install_series_dt_unsupported():
    for ohxv__zmoq in series_dt_unsupported_attrs:
        wgyin__jjv = 'Series.dt.' + ohxv__zmoq
        overload_attribute(SeriesDatetimePropertiesType, ohxv__zmoq)(
            create_unsupported_overload(wgyin__jjv))
    for rzxq__svnc in series_dt_unsupported_methods:
        wgyin__jjv = 'Series.dt.' + rzxq__svnc
        overload_method(SeriesDatetimePropertiesType, rzxq__svnc,
            no_unliteral=True)(create_unsupported_overload(wgyin__jjv))


_install_series_dt_unsupported()
