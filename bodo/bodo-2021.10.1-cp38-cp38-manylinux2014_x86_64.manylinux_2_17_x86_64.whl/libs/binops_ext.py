""" Implementation of binary operators for the different types.
    Currently implemented operators:
        arith: add, sub, mul, truediv, floordiv, mod, pow
        cmp: lt, le, eq, ne, ge, gt
"""
import operator
import numba
from numba.core import types
from numba.core.imputils import lower_builtin
from numba.core.typing.builtins import machine_ints
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import overload
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type, datetime_date_type, datetime_timedelta_type
from bodo.hiframes.datetime_timedelta_ext import datetime_datetime_type, datetime_timedelta_array_type, pd_timedelta_type
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import DatetimeIndexType, HeterogeneousIndexType, is_index_type
from bodo.hiframes.pd_offsets_ext import date_offset_type, month_begin_type, month_end_type, week_type
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_type
from bodo.hiframes.series_impl import SeriesType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import Decimal128Type
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.utils.typing import BodoError, is_overload_bool, is_timedelta_type


class SeriesCmpOpTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        lhs, rhs = args
        if cmp_timeseries(lhs, rhs) or (isinstance(lhs, DataFrameType) or
            isinstance(rhs, DataFrameType)) or not (isinstance(lhs,
            SeriesType) or isinstance(rhs, SeriesType)):
            return
        mpbx__rsyu = lhs.data if isinstance(lhs, SeriesType) else lhs
        fch__eqkon = rhs.data if isinstance(rhs, SeriesType) else rhs
        if mpbx__rsyu in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and fch__eqkon.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            mpbx__rsyu = fch__eqkon.dtype
        elif fch__eqkon in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and mpbx__rsyu.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            fch__eqkon = mpbx__rsyu.dtype
        qrab__yddbh = mpbx__rsyu, fch__eqkon
        dwa__lqzac = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            xmstn__akco = self.context.resolve_function_type(self.key,
                qrab__yddbh, {}).return_type
        except Exception as jjy__pzp:
            raise BodoError(dwa__lqzac)
        if is_overload_bool(xmstn__akco):
            raise BodoError(dwa__lqzac)
        ppli__wbgzz = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        ydbov__tqtr = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        xbnq__rzfec = types.bool_
        pcy__nvov = SeriesType(xbnq__rzfec, xmstn__akco, ppli__wbgzz,
            ydbov__tqtr)
        return pcy__nvov(*args)


def series_cmp_op_lower(op):

    def lower_impl(context, builder, sig, args):
        mfylj__icdra = bodo.hiframes.series_impl.create_binary_op_overload(op)(
            *sig.args)
        if mfylj__icdra is None:
            mfylj__icdra = create_overload_cmp_operator(op)(*sig.args)
        return context.compile_internal(builder, mfylj__icdra, sig, args)
    return lower_impl


class SeriesAndOrTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        lhs, rhs = args
        if not (isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType)):
            return
        mpbx__rsyu = lhs.data if isinstance(lhs, SeriesType) else lhs
        fch__eqkon = rhs.data if isinstance(rhs, SeriesType) else rhs
        qrab__yddbh = mpbx__rsyu, fch__eqkon
        dwa__lqzac = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            xmstn__akco = self.context.resolve_function_type(self.key,
                qrab__yddbh, {}).return_type
        except Exception as tnjso__bwvwz:
            raise BodoError(dwa__lqzac)
        ppli__wbgzz = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        ydbov__tqtr = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        xbnq__rzfec = xmstn__akco.dtype
        pcy__nvov = SeriesType(xbnq__rzfec, xmstn__akco, ppli__wbgzz,
            ydbov__tqtr)
        return pcy__nvov(*args)


def lower_series_and_or(op):

    def lower_and_or_impl(context, builder, sig, args):
        mfylj__icdra = bodo.hiframes.series_impl.create_binary_op_overload(op)(
            *sig.args)
        if mfylj__icdra is None:
            lhs, rhs = sig.args
            if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType
                ):
                mfylj__icdra = (bodo.hiframes.dataframe_impl.
                    create_binary_op_overload(op)(*sig.args))
        return context.compile_internal(builder, mfylj__icdra, sig, args)
    return lower_and_or_impl


def overload_add_operator_scalars(lhs, rhs):
    if lhs == week_type or rhs == week_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_week_offset_type(lhs, rhs))
    if lhs == month_begin_type or rhs == month_begin_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_month_begin_offset_type(lhs, rhs))
    if lhs == month_end_type or rhs == month_end_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_month_end_offset_type(lhs, rhs))
    if lhs == date_offset_type or rhs == date_offset_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_date_offset_type(lhs, rhs))
    if add_timestamp(lhs, rhs):
        return bodo.hiframes.pd_timestamp_ext.overload_add_operator_timestamp(
            lhs, rhs)
    if add_dt_td_and_dt_date(lhs, rhs):
        return (bodo.hiframes.datetime_date_ext.
            overload_add_operator_datetime_date(lhs, rhs))
    if add_datetime_and_timedeltas(lhs, rhs):
        return (bodo.hiframes.datetime_timedelta_ext.
            overload_add_operator_datetime_timedelta(lhs, rhs))
    raise_error_if_not_numba_supported(operator.add, lhs, rhs)


def overload_sub_operator_scalars(lhs, rhs):
    if sub_offset_to_datetime_or_timestamp(lhs, rhs):
        return bodo.hiframes.pd_offsets_ext.overload_sub_operator_offsets(lhs,
            rhs)
    if lhs == pd_timestamp_type and rhs in [pd_timestamp_type,
        datetime_timedelta_type, pd_timedelta_type]:
        return bodo.hiframes.pd_timestamp_ext.overload_sub_operator_timestamp(
            lhs, rhs)
    if sub_dt_or_td(lhs, rhs):
        return (bodo.hiframes.datetime_date_ext.
            overload_sub_operator_datetime_date(lhs, rhs))
    if sub_datetime_and_timedeltas(lhs, rhs):
        return (bodo.hiframes.datetime_timedelta_ext.
            overload_sub_operator_datetime_timedelta(lhs, rhs))
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:
        return (bodo.hiframes.datetime_datetime_ext.
            overload_sub_operator_datetime_datetime(lhs, rhs))
    raise_error_if_not_numba_supported(operator.sub, lhs, rhs)


def create_overload_arith_op(op):

    def overload_arith_operator(lhs, rhs):
        if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType):
            return bodo.hiframes.dataframe_impl.create_binary_op_overload(op)(
                lhs, rhs)
        if time_series_operation(lhs, rhs) and op in [operator.add,
            operator.sub]:
            return bodo.hiframes.series_dt_impl.create_bin_op_overload(op)(lhs,
                rhs)
        if isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType):
            return bodo.hiframes.series_impl.create_binary_op_overload(op)(lhs,
                rhs)
        if sub_dt_index_and_timestamp(lhs, rhs) and op == operator.sub:
            return (bodo.hiframes.pd_index_ext.
                overload_sub_operator_datetime_index(lhs, rhs))
        if operand_is_index(lhs) or operand_is_index(rhs):
            return bodo.hiframes.pd_index_ext.create_binary_op_overload(op)(lhs
                , rhs)
        if args_td_and_int_array(lhs, rhs):
            return bodo.libs.int_arr_ext.get_int_array_op_pd_td(op)(lhs, rhs)
        if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
            IntegerArrayType):
            return bodo.libs.int_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if lhs == boolean_array or rhs == boolean_array:
            return bodo.libs.bool_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if op == operator.add and (lhs == string_array_type or types.
            unliteral(lhs) == string_type):
            return bodo.libs.str_arr_ext.overload_add_operator_string_array(lhs
                , rhs)
        if op == operator.add:
            return overload_add_operator_scalars(lhs, rhs)
        if op == operator.sub:
            return overload_sub_operator_scalars(lhs, rhs)
        if op == operator.mul:
            if mul_timedelta_and_int(lhs, rhs):
                return (bodo.hiframes.datetime_timedelta_ext.
                    overload_mul_operator_timedelta(lhs, rhs))
            if mul_string_arr_and_int(lhs, rhs):
                return bodo.libs.str_arr_ext.overload_mul_operator_str_arr(lhs,
                    rhs)
            if mul_date_offset_and_int(lhs, rhs):
                return (bodo.hiframes.pd_offsets_ext.
                    overload_mul_date_offset_types(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op in [operator.truediv, operator.floordiv]:
            if div_timedelta_and_int(lhs, rhs):
                if op == operator.truediv:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_truediv_operator_pd_timedelta(lhs, rhs))
                else:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_floordiv_operator_pd_timedelta(lhs, rhs))
            if div_datetime_timedelta(lhs, rhs):
                if op == operator.truediv:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_truediv_operator_dt_timedelta(lhs, rhs))
                else:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_floordiv_operator_dt_timedelta(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op == operator.mod:
            if mod_timedeltas(lhs, rhs):
                return (bodo.hiframes.datetime_timedelta_ext.
                    overload_mod_operator_timedeltas(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op == operator.pow:
            raise_error_if_not_numba_supported(op, lhs, rhs)
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_arith_operator


def create_overload_cmp_operator(op):

    def overload_cmp_operator(lhs, rhs):
        if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType):
            return bodo.hiframes.dataframe_impl.create_binary_op_overload(op)(
                lhs, rhs)
        if cmp_timeseries(lhs, rhs):
            return bodo.hiframes.series_dt_impl.create_cmp_op_overload(op)(lhs,
                rhs)
        if isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType):
            return
        if lhs == datetime_date_array_type or rhs == datetime_date_array_type:
            return bodo.hiframes.datetime_date_ext.create_cmp_op_overload_arr(
                op)(lhs, rhs)
        if (lhs == datetime_timedelta_array_type or rhs ==
            datetime_timedelta_array_type):
            mfylj__icdra = (bodo.hiframes.datetime_timedelta_ext.
                create_cmp_op_overload(op))
            return mfylj__icdra(lhs, rhs)
        if lhs == string_array_type or rhs == string_array_type:
            return bodo.libs.str_arr_ext.create_binary_op_overload(op)(lhs, rhs
                )
        if isinstance(lhs, Decimal128Type) and isinstance(rhs, Decimal128Type):
            return bodo.libs.decimal_arr_ext.decimal_create_cmp_op_overload(op
                )(lhs, rhs)
        if lhs == boolean_array or rhs == boolean_array:
            return bodo.libs.bool_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
            IntegerArrayType):
            return bodo.libs.int_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if binary_array_cmp(lhs, rhs):
            return bodo.libs.binary_arr_ext.create_binary_cmp_op_overload(op)(
                lhs, rhs)
        if cmp_dt_index_to_string(lhs, rhs):
            return bodo.hiframes.pd_index_ext.overload_binop_dti_str(op)(lhs,
                rhs)
        if operand_is_index(lhs) or operand_is_index(rhs):
            return bodo.hiframes.pd_index_ext.create_binary_op_overload(op)(lhs
                , rhs)
        if lhs == datetime_date_type and rhs == datetime_date_type:
            return bodo.hiframes.datetime_date_ext.create_cmp_op_overload(op)(
                lhs, rhs)
        if can_cmp_date_datetime(lhs, rhs, op):
            return (bodo.hiframes.datetime_date_ext.
                create_datetime_date_cmp_op_overload(op)(lhs, rhs))
        if lhs == datetime_datetime_type and rhs == datetime_datetime_type:
            return bodo.hiframes.datetime_datetime_ext.create_cmp_op_overload(
                op)(lhs, rhs)
        if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:
            return bodo.hiframes.datetime_timedelta_ext.create_cmp_op_overload(
                op)(lhs, rhs)
        if cmp_timedeltas(lhs, rhs):
            mfylj__icdra = (bodo.hiframes.datetime_timedelta_ext.
                pd_create_cmp_op_overload(op))
            return mfylj__icdra(lhs, rhs)
        if cmp_timestamp_or_date(lhs, rhs):
            return (bodo.hiframes.pd_timestamp_ext.
                create_timestamp_cmp_op_overload(op)(lhs, rhs))
        if cmp_op_supported_by_numba(lhs, rhs):
            return
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_cmp_operator


def add_dt_td_and_dt_date(lhs, rhs):
    htt__bad = lhs == datetime_timedelta_type and rhs == datetime_date_type
    pzri__fpy = rhs == datetime_timedelta_type and lhs == datetime_date_type
    return htt__bad or pzri__fpy


def add_timestamp(lhs, rhs):
    sqgf__swg = lhs == pd_timestamp_type and is_timedelta_type(rhs)
    jsrvp__xwi = is_timedelta_type(lhs) and rhs == pd_timestamp_type
    return sqgf__swg or jsrvp__xwi


def add_datetime_and_timedeltas(lhs, rhs):
    xxffs__ayoxw = [datetime_timedelta_type, pd_timedelta_type]
    izulb__aylob = [datetime_timedelta_type, pd_timedelta_type,
        datetime_datetime_type]
    sctaj__upq = lhs in xxffs__ayoxw and rhs in xxffs__ayoxw
    vlzs__nshq = (lhs == datetime_datetime_type and rhs in xxffs__ayoxw or 
        rhs == datetime_datetime_type and lhs in xxffs__ayoxw)
    return sctaj__upq or vlzs__nshq


def mul_string_arr_and_int(lhs, rhs):
    fch__eqkon = isinstance(lhs, types.Integer) and rhs == string_array_type
    mpbx__rsyu = lhs == string_array_type and isinstance(rhs, types.Integer)
    return fch__eqkon or mpbx__rsyu


def mul_timedelta_and_int(lhs, rhs):
    htt__bad = lhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(rhs, types.Integer)
    pzri__fpy = rhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(lhs, types.Integer)
    return htt__bad or pzri__fpy


def mul_date_offset_and_int(lhs, rhs):
    hpbdh__sir = lhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(rhs, types.Integer)
    guir__cgqcb = rhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(lhs, types.Integer)
    return hpbdh__sir or guir__cgqcb


def sub_offset_to_datetime_or_timestamp(lhs, rhs):
    qpjzd__jgyuj = [datetime_datetime_type, pd_timestamp_type,
        datetime_date_type]
    bkao__myevd = [date_offset_type, month_begin_type, month_end_type,
        week_type]
    return rhs in bkao__myevd and lhs in qpjzd__jgyuj


def sub_dt_index_and_timestamp(lhs, rhs):
    htzt__syqf = isinstance(lhs, DatetimeIndexType
        ) and rhs == pd_timestamp_type
    wnied__miuo = isinstance(rhs, DatetimeIndexType
        ) and lhs == pd_timestamp_type
    return htzt__syqf or wnied__miuo


def sub_dt_or_td(lhs, rhs):
    puck__hfcn = lhs == datetime_date_type and rhs == datetime_timedelta_type
    vlx__hzr = lhs == datetime_date_type and rhs == datetime_date_type
    icqxx__dbtff = (lhs == datetime_date_array_type and rhs ==
        datetime_timedelta_type)
    return puck__hfcn or vlx__hzr or icqxx__dbtff


def sub_datetime_and_timedeltas(lhs, rhs):
    pybg__yny = (is_timedelta_type(lhs) or lhs == datetime_datetime_type
        ) and is_timedelta_type(rhs)
    lno__fwdvg = (lhs == datetime_timedelta_array_type and rhs ==
        datetime_timedelta_type)
    return pybg__yny or lno__fwdvg


def div_timedelta_and_int(lhs, rhs):
    sctaj__upq = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    iaz__nfncw = lhs == pd_timedelta_type and isinstance(rhs, types.Integer)
    return sctaj__upq or iaz__nfncw


def div_datetime_timedelta(lhs, rhs):
    sctaj__upq = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    iaz__nfncw = lhs == datetime_timedelta_type and rhs == types.int64
    return sctaj__upq or iaz__nfncw


def mod_timedeltas(lhs, rhs):
    vdh__xohb = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    zwreu__tnx = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    return vdh__xohb or zwreu__tnx


def cmp_dt_index_to_string(lhs, rhs):
    htzt__syqf = isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
        ) == string_type
    wnied__miuo = isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
        ) == string_type
    return htzt__syqf or wnied__miuo


def cmp_timestamp_or_date(lhs, rhs):
    spsj__jpjy = (lhs == pd_timestamp_type and rhs == bodo.hiframes.
        datetime_date_ext.datetime_date_type)
    sxaz__hlko = (lhs == bodo.hiframes.datetime_date_ext.datetime_date_type and
        rhs == pd_timestamp_type)
    out__lgqu = lhs == pd_timestamp_type and rhs == pd_timestamp_type
    abo__iou = lhs == pd_timestamp_type and rhs == bodo.datetime64ns
    jpwme__vmu = rhs == pd_timestamp_type and lhs == bodo.datetime64ns
    return spsj__jpjy or sxaz__hlko or out__lgqu or abo__iou or jpwme__vmu


def cmp_timeseries(lhs, rhs):
    dmjqm__czvm = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (bodo
        .utils.typing.is_overload_constant_str(lhs) or lhs == bodo.libs.
        str_ext.string_type or lhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    frtst__zdu = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (bodo
        .utils.typing.is_overload_constant_str(rhs) or rhs == bodo.libs.
        str_ext.string_type or rhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    qrpq__irbr = dmjqm__czvm or frtst__zdu
    ethj__tgu = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    mwgs__wemq = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    eokmz__nxn = ethj__tgu or mwgs__wemq
    return qrpq__irbr or eokmz__nxn


def cmp_timedeltas(lhs, rhs):
    sctaj__upq = [pd_timedelta_type, bodo.timedelta64ns]
    return lhs in sctaj__upq and rhs in sctaj__upq


def operand_is_index(operand):
    return is_index_type(operand) or isinstance(operand, HeterogeneousIndexType
        )


def helper_time_series_checks(operand):
    ylyvy__epdhf = bodo.hiframes.pd_series_ext.is_dt64_series_typ(operand
        ) or bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(operand
        ) or operand in [datetime_timedelta_type, datetime_datetime_type,
        pd_timestamp_type]
    return ylyvy__epdhf


def binary_array_cmp(lhs, rhs):
    return lhs == binary_array_type and rhs in [bytes_type, binary_array_type
        ] or lhs in [bytes_type, binary_array_type
        ] and rhs == binary_array_type


def can_cmp_date_datetime(lhs, rhs, op):
    return op in (operator.eq, operator.ne) and (lhs == datetime_date_type and
        rhs == datetime_datetime_type or lhs == datetime_datetime_type and 
        rhs == datetime_date_type)


def time_series_operation(lhs, rhs):
    cph__xze = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == datetime_timedelta_type
    cxoo__jao = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == datetime_timedelta_type
    vbg__obdca = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
        ) and helper_time_series_checks(rhs)
    kjkd__fwmwm = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
        ) and helper_time_series_checks(lhs)
    return cph__xze or cxoo__jao or vbg__obdca or kjkd__fwmwm


def args_td_and_int_array(lhs, rhs):
    eau__thfrj = (isinstance(lhs, IntegerArrayType) or isinstance(lhs,
        types.Array) and isinstance(lhs.dtype, types.Integer)) or (isinstance
        (rhs, IntegerArrayType) or isinstance(rhs, types.Array) and
        isinstance(rhs.dtype, types.Integer))
    izixi__eho = lhs in [pd_timedelta_type] or rhs in [pd_timedelta_type]
    return eau__thfrj and izixi__eho


def arith_op_supported_by_numba(op, lhs, rhs):
    if op == operator.mul:
        pzri__fpy = isinstance(lhs, (types.Integer, types.Float)
            ) and isinstance(rhs, types.NPTimedelta)
        htt__bad = isinstance(rhs, (types.Integer, types.Float)
            ) and isinstance(lhs, types.NPTimedelta)
        hxf__qjc = pzri__fpy or htt__bad
        rgb__tgkdp = isinstance(rhs, types.UnicodeType) and isinstance(lhs,
            types.Integer)
        fikd__vtut = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.Integer)
        sksf__bwesd = rgb__tgkdp or fikd__vtut
        zds__yzke = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        qwevb__fdegr = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        zvpvr__bqome = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        uosf__whu = zds__yzke or qwevb__fdegr or zvpvr__bqome
        pjsy__psoa = isinstance(lhs, types.List) and isinstance(rhs, types.
            Integer)
        tys = types.UnicodeCharSeq, types.CharSeq, types.Bytes
        ilcuv__gknvx = isinstance(lhs, tys) or isinstance(rhs, tys)
        lcixm__tfgrl = isinstance(lhs, types.Array) or isinstance(rhs,
            types.Array)
        return (hxf__qjc or sksf__bwesd or uosf__whu or pjsy__psoa or
            ilcuv__gknvx or lcixm__tfgrl)
    if op == operator.pow:
        lujc__kjyb = isinstance(lhs, types.Integer) and isinstance(rhs, (
            types.IntegerLiteral, types.Integer))
        xhn__mto = isinstance(lhs, types.Float) and isinstance(rhs, (types.
            IntegerLiteral, types.Float, types.Integer) or rhs in types.
            unsigned_domain or rhs in types.signed_domain)
        zvpvr__bqome = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        lcixm__tfgrl = isinstance(lhs, types.Array) or isinstance(rhs,
            types.Array)
        return lujc__kjyb or xhn__mto or zvpvr__bqome or lcixm__tfgrl
    if op == operator.floordiv:
        qwevb__fdegr = lhs in types.real_domain and rhs in types.real_domain
        zds__yzke = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        nlzg__sar = isinstance(lhs, types.Float) and isinstance(rhs, types.
            Float)
        sctaj__upq = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        lcixm__tfgrl = isinstance(lhs, types.Array) or isinstance(rhs,
            types.Array)
        return (qwevb__fdegr or zds__yzke or nlzg__sar or sctaj__upq or
            lcixm__tfgrl)
    if op == operator.truediv:
        eob__twmr = lhs in machine_ints and rhs in machine_ints
        qwevb__fdegr = lhs in types.real_domain and rhs in types.real_domain
        zvpvr__bqome = (lhs in types.complex_domain and rhs in types.
            complex_domain)
        zds__yzke = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        nlzg__sar = isinstance(lhs, types.Float) and isinstance(rhs, types.
            Float)
        jryb__laiht = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        sctaj__upq = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        lcixm__tfgrl = isinstance(lhs, types.Array) or isinstance(rhs,
            types.Array)
        return (eob__twmr or qwevb__fdegr or zvpvr__bqome or zds__yzke or
            nlzg__sar or jryb__laiht or sctaj__upq or lcixm__tfgrl)
    if op == operator.mod:
        eob__twmr = lhs in machine_ints and rhs in machine_ints
        qwevb__fdegr = lhs in types.real_domain and rhs in types.real_domain
        zds__yzke = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        nlzg__sar = isinstance(lhs, types.Float) and isinstance(rhs, types.
            Float)
        lcixm__tfgrl = isinstance(lhs, types.Array) or isinstance(rhs,
            types.Array)
        return (eob__twmr or qwevb__fdegr or zds__yzke or nlzg__sar or
            lcixm__tfgrl)
    if op == operator.add or op == operator.sub:
        hxf__qjc = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            types.NPTimedelta)
        sldfl__mkfc = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPDatetime)
        yqaac__kegq = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPTimedelta)
        jxqp__kjbxj = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
        zds__yzke = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        qwevb__fdegr = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        zvpvr__bqome = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        uosf__whu = zds__yzke or qwevb__fdegr or zvpvr__bqome
        lcixm__tfgrl = isinstance(lhs, types.Array) or isinstance(rhs,
            types.Array)
        lvcw__woxn = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
            types.BaseTuple)
        pjsy__psoa = isinstance(lhs, types.List) and isinstance(rhs, types.List
            )
        xfz__brqkp = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeType)
        lueoo__lfk = isinstance(rhs, types.UnicodeCharSeq) and isinstance(lhs,
            types.UnicodeType)
        vmdfd__eqcpm = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs
            , types.UnicodeCharSeq)
        mgqbl__xyob = isinstance(lhs, (types.CharSeq, types.Bytes)
            ) and isinstance(rhs, (types.CharSeq, types.Bytes))
        jbse__lycxc = xfz__brqkp or lueoo__lfk or vmdfd__eqcpm or mgqbl__xyob
        sksf__bwesd = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeType)
        uuf__vuocf = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeCharSeq)
        rqq__kiro = sksf__bwesd or uuf__vuocf
        odkc__fihb = lhs == types.NPTimedelta and rhs == types.NPDatetime
        awsk__ubtgn = (lvcw__woxn or pjsy__psoa or jbse__lycxc or rqq__kiro or
            odkc__fihb)
        mohnk__qokur = op == operator.add and awsk__ubtgn
        return (hxf__qjc or sldfl__mkfc or yqaac__kegq or jxqp__kjbxj or
            uosf__whu or lcixm__tfgrl or mohnk__qokur)


def cmp_op_supported_by_numba(lhs, rhs):
    lcixm__tfgrl = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
    pjsy__psoa = isinstance(lhs, types.ListType) and isinstance(rhs, types.
        ListType)
    hxf__qjc = isinstance(lhs, types.NPTimedelta) and isinstance(rhs, types
        .NPTimedelta)
    yyq__ghg = isinstance(lhs, types.NPDatetime) and isinstance(rhs, types.
        NPDatetime)
    unicode_types = (types.UnicodeType, types.StringLiteral, types.CharSeq,
        types.Bytes, types.UnicodeCharSeq)
    sksf__bwesd = isinstance(lhs, unicode_types) and isinstance(rhs,
        unicode_types)
    lvcw__woxn = isinstance(lhs, types.BaseTuple) and isinstance(rhs, types
        .BaseTuple)
    jxqp__kjbxj = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
    uosf__whu = isinstance(lhs, types.Number) and isinstance(rhs, types.Number)
    gdgu__psaa = isinstance(lhs, types.Boolean) and isinstance(rhs, types.
        Boolean)
    ikx__xkye = isinstance(lhs, types.NoneType) or isinstance(rhs, types.
        NoneType)
    dwr__ovm = isinstance(lhs, types.DictType) and isinstance(rhs, types.
        DictType)
    tnhd__pbpik = isinstance(lhs, types.EnumMember) and isinstance(rhs,
        types.EnumMember)
    ynh__ndvl = isinstance(lhs, types.Literal) and isinstance(rhs, types.
        Literal)
    return (pjsy__psoa or hxf__qjc or yyq__ghg or sksf__bwesd or lvcw__woxn or
        jxqp__kjbxj or uosf__whu or gdgu__psaa or ikx__xkye or dwr__ovm or
        lcixm__tfgrl or tnhd__pbpik or ynh__ndvl)


def raise_error_if_not_numba_supported(op, lhs, rhs):
    if arith_op_supported_by_numba(op, lhs, rhs):
        return
    raise BodoError(
        f'{op} operator not supported for data types {lhs} and {rhs}.')


def _install_series_and_or():
    for op in (operator.or_, operator.and_):
        infer_global(op)(SeriesAndOrTyper)
        lower_impl = lower_series_and_or(op)
        lower_builtin(op, SeriesType, SeriesType)(lower_impl)
        lower_builtin(op, SeriesType, types.Any)(lower_impl)
        lower_builtin(op, types.Any, SeriesType)(lower_impl)


_install_series_and_or()


def _install_cmp_ops():
    for op in (operator.lt, operator.eq, operator.ne, operator.ge, operator
        .gt, operator.le):
        infer_global(op)(SeriesCmpOpTemplate)
        lower_impl = series_cmp_op_lower(op)
        lower_builtin(op, SeriesType, SeriesType)(lower_impl)
        lower_builtin(op, SeriesType, types.Any)(lower_impl)
        lower_builtin(op, types.Any, SeriesType)(lower_impl)
        wurq__xcpl = create_overload_cmp_operator(op)
        overload(op, no_unliteral=True)(wurq__xcpl)


_install_cmp_ops()


def install_arith_ops():
    for op in (operator.add, operator.sub, operator.mul, operator.truediv,
        operator.floordiv, operator.mod, operator.pow):
        wurq__xcpl = create_overload_arith_op(op)
        overload(op, no_unliteral=True)(wurq__xcpl)


install_arith_ops()
