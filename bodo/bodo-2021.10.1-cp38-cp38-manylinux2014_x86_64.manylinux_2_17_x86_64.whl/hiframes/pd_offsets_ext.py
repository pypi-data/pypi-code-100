"""
Implement support for the various classes in pd.tseries.offsets.
"""
import operator
import llvmlite.binding as ll
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, register_jitable, register_model, typeof_impl, unbox
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.hiframes.pd_timestamp_ext import get_days_in_month, pd_timestamp_type
from bodo.libs import hdatetime_ext
from bodo.utils.typing import BodoError, is_overload_none
ll.add_symbol('box_date_offset', hdatetime_ext.box_date_offset)
ll.add_symbol('unbox_date_offset', hdatetime_ext.unbox_date_offset)


class MonthBeginType(types.Type):

    def __init__(self):
        super(MonthBeginType, self).__init__(name='MonthBeginType()')


month_begin_type = MonthBeginType()


@typeof_impl.register(pd.tseries.offsets.MonthBegin)
def typeof_month_begin(val, c):
    return month_begin_type


@register_model(MonthBeginType)
class MonthBeginModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        lltjn__uai = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthBeginModel, self).__init__(dmm, fe_type, lltjn__uai)


@box(MonthBeginType)
def box_month_begin(typ, val, c):
    lnu__zmyoi = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    ftk__bvd = c.pyapi.long_from_longlong(lnu__zmyoi.n)
    biyj__sae = c.pyapi.from_native_value(types.boolean, lnu__zmyoi.
        normalize, c.env_manager)
    opcbl__qna = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthBegin))
    jymah__orqyy = c.pyapi.call_function_objargs(opcbl__qna, (ftk__bvd,
        biyj__sae))
    c.pyapi.decref(ftk__bvd)
    c.pyapi.decref(biyj__sae)
    c.pyapi.decref(opcbl__qna)
    return jymah__orqyy


@unbox(MonthBeginType)
def unbox_month_begin(typ, val, c):
    ftk__bvd = c.pyapi.object_getattr_string(val, 'n')
    biyj__sae = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(ftk__bvd)
    normalize = c.pyapi.to_native_value(types.bool_, biyj__sae).value
    lnu__zmyoi = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    lnu__zmyoi.n = n
    lnu__zmyoi.normalize = normalize
    c.pyapi.decref(ftk__bvd)
    c.pyapi.decref(biyj__sae)
    vchiz__meyz = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(lnu__zmyoi._getvalue(), is_error=vchiz__meyz)


@overload(pd.tseries.offsets.MonthBegin, no_unliteral=True)
def MonthBegin(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_begin(n, normalize)
    return impl


@intrinsic
def init_month_begin(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        lnu__zmyoi = cgutils.create_struct_proxy(typ)(context, builder)
        lnu__zmyoi.n = args[0]
        lnu__zmyoi.normalize = args[1]
        return lnu__zmyoi._getvalue()
    return MonthBeginType()(n, normalize), codegen


make_attribute_wrapper(MonthBeginType, 'n', 'n')
make_attribute_wrapper(MonthBeginType, 'normalize', 'normalize')


@register_jitable
def calculate_month_begin_date(year, month, day, n):
    if n <= 0:
        if day > 1:
            n += 1
    month = month + n
    month -= 1
    year += month // 12
    month = month % 12 + 1
    day = 1
    return year, month, day


def overload_add_operator_month_begin_offset_type(lhs, rhs):
    if lhs == month_begin_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond)
        return impl
    if lhs == month_begin_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond)
        return impl
    if lhs == month_begin_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            return pd.Timestamp(year=year, month=month, day=day)
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == month_begin_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


class MonthEndType(types.Type):

    def __init__(self):
        super(MonthEndType, self).__init__(name='MonthEndType()')


month_end_type = MonthEndType()


@typeof_impl.register(pd.tseries.offsets.MonthEnd)
def typeof_month_end(val, c):
    return month_end_type


@register_model(MonthEndType)
class MonthEndModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        lltjn__uai = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthEndModel, self).__init__(dmm, fe_type, lltjn__uai)


@box(MonthEndType)
def box_month_end(typ, val, c):
    qpt__scchi = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    ftk__bvd = c.pyapi.long_from_longlong(qpt__scchi.n)
    biyj__sae = c.pyapi.from_native_value(types.boolean, qpt__scchi.
        normalize, c.env_manager)
    aob__yvldl = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthEnd))
    jymah__orqyy = c.pyapi.call_function_objargs(aob__yvldl, (ftk__bvd,
        biyj__sae))
    c.pyapi.decref(ftk__bvd)
    c.pyapi.decref(biyj__sae)
    c.pyapi.decref(aob__yvldl)
    return jymah__orqyy


@unbox(MonthEndType)
def unbox_month_end(typ, val, c):
    ftk__bvd = c.pyapi.object_getattr_string(val, 'n')
    biyj__sae = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(ftk__bvd)
    normalize = c.pyapi.to_native_value(types.bool_, biyj__sae).value
    qpt__scchi = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qpt__scchi.n = n
    qpt__scchi.normalize = normalize
    c.pyapi.decref(ftk__bvd)
    c.pyapi.decref(biyj__sae)
    vchiz__meyz = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(qpt__scchi._getvalue(), is_error=vchiz__meyz)


@overload(pd.tseries.offsets.MonthEnd, no_unliteral=True)
def MonthEnd(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_end(n, normalize)
    return impl


@intrinsic
def init_month_end(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        qpt__scchi = cgutils.create_struct_proxy(typ)(context, builder)
        qpt__scchi.n = args[0]
        qpt__scchi.normalize = args[1]
        return qpt__scchi._getvalue()
    return MonthEndType()(n, normalize), codegen


make_attribute_wrapper(MonthEndType, 'n', 'n')
make_attribute_wrapper(MonthEndType, 'normalize', 'normalize')


@lower_constant(MonthBeginType)
@lower_constant(MonthEndType)
def lower_constant_month_end(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    qpt__scchi = cgutils.create_struct_proxy(ty)(context, builder)
    qpt__scchi.n = n
    qpt__scchi.normalize = normalize
    return qpt__scchi._getvalue()


@register_jitable
def calculate_month_end_date(year, month, day, n):
    if n > 0:
        qpt__scchi = get_days_in_month(year, month)
        if qpt__scchi > day:
            n -= 1
    month = month + n
    month -= 1
    year += month // 12
    month = month % 12 + 1
    day = get_days_in_month(year, month)
    return year, month, day


def overload_add_operator_month_end_offset_type(lhs, rhs):
    if lhs == month_end_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond)
        return impl
    if lhs == month_end_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond)
        return impl
    if lhs == month_end_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            return pd.Timestamp(year=year, month=month, day=day)
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == month_end_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


def overload_mul_date_offset_types(lhs, rhs):
    if lhs == month_begin_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.MonthBegin(lhs.n * rhs, lhs.normalize)
    if lhs == month_end_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.MonthEnd(lhs.n * rhs, lhs.normalize)
    if lhs == week_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.Week(lhs.n * rhs, lhs.normalize, lhs.
                weekday)
    if lhs == date_offset_type:

        def impl(lhs, rhs):
            n = lhs.n * rhs
            normalize = lhs.normalize
            nanoseconds = lhs._nanoseconds
            nanosecond = lhs._nanosecond
            if lhs._has_kws:
                years = lhs._years
                months = lhs._months
                weeks = lhs._weeks
                days = lhs._days
                hours = lhs._hours
                minutes = lhs._minutes
                seconds = lhs._seconds
                microseconds = lhs._microseconds
                year = lhs._year
                month = lhs._month
                day = lhs._day
                weekday = lhs._weekday
                hour = lhs._hour
                minute = lhs._minute
                second = lhs._second
                microsecond = lhs._microsecond
                return pd.tseries.offsets.DateOffset(n, normalize, years,
                    months, weeks, days, hours, minutes, seconds,
                    microseconds, nanoseconds, year, month, day, weekday,
                    hour, minute, second, microsecond, nanosecond)
            else:
                return pd.tseries.offsets.DateOffset(n, normalize,
                    nanoseconds=nanoseconds, nanosecond=nanosecond)
    if rhs in [week_type, month_end_type, month_begin_type, date_offset_type]:

        def impl(lhs, rhs):
            return rhs * lhs
        return impl
    return impl


class DateOffsetType(types.Type):

    def __init__(self):
        super(DateOffsetType, self).__init__(name='DateOffsetType()')


date_offset_type = DateOffsetType()
date_offset_fields = ['years', 'months', 'weeks', 'days', 'hours',
    'minutes', 'seconds', 'microseconds', 'nanoseconds', 'year', 'month',
    'day', 'weekday', 'hour', 'minute', 'second', 'microsecond', 'nanosecond']


@typeof_impl.register(pd.tseries.offsets.DateOffset)
def type_of_date_offset(val, c):
    return date_offset_type


@register_model(DateOffsetType)
class DateOffsetModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        lltjn__uai = [('n', types.int64), ('normalize', types.boolean), (
            'years', types.int64), ('months', types.int64), ('weeks', types
            .int64), ('days', types.int64), ('hours', types.int64), (
            'minutes', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64), ('nanoseconds', types.int64), (
            'year', types.int64), ('month', types.int64), ('day', types.
            int64), ('weekday', types.int64), ('hour', types.int64), (
            'minute', types.int64), ('second', types.int64), ('microsecond',
            types.int64), ('nanosecond', types.int64), ('has_kws', types.
            boolean)]
        super(DateOffsetModel, self).__init__(dmm, fe_type, lltjn__uai)


@box(DateOffsetType)
def box_date_offset(typ, val, c):
    nav__ynqya = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    mva__ezm = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    for hoe__qedsa, orv__sdx in enumerate(date_offset_fields):
        c.builder.store(getattr(nav__ynqya, orv__sdx), c.builder.inttoptr(c
            .builder.add(c.builder.ptrtoint(mva__ezm, lir.IntType(64)), lir
            .Constant(lir.IntType(64), 8 * hoe__qedsa)), lir.IntType(64).
            as_pointer()))
    lvge__hucwd = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(1), lir.IntType(64).as_pointer(), lir.IntType(1)])
    zsiu__bwmo = cgutils.get_or_insert_function(c.builder.module,
        lvge__hucwd, name='box_date_offset')
    lxbg__ffnaz = c.builder.call(zsiu__bwmo, [nav__ynqya.n, nav__ynqya.
        normalize, mva__ezm, nav__ynqya.has_kws])
    c.context.nrt.decref(c.builder, typ, val)
    return lxbg__ffnaz


@unbox(DateOffsetType)
def unbox_date_offset(typ, val, c):
    ftk__bvd = c.pyapi.object_getattr_string(val, 'n')
    biyj__sae = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(ftk__bvd)
    normalize = c.pyapi.to_native_value(types.bool_, biyj__sae).value
    mva__ezm = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    lvge__hucwd = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer()])
    jci__venu = cgutils.get_or_insert_function(c.builder.module,
        lvge__hucwd, name='unbox_date_offset')
    has_kws = c.builder.call(jci__venu, [val, mva__ezm])
    nav__ynqya = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    nav__ynqya.n = n
    nav__ynqya.normalize = normalize
    for hoe__qedsa, orv__sdx in enumerate(date_offset_fields):
        setattr(nav__ynqya, orv__sdx, c.builder.load(c.builder.inttoptr(c.
            builder.add(c.builder.ptrtoint(mva__ezm, lir.IntType(64)), lir.
            Constant(lir.IntType(64), 8 * hoe__qedsa)), lir.IntType(64).
            as_pointer())))
    nav__ynqya.has_kws = has_kws
    c.pyapi.decref(ftk__bvd)
    c.pyapi.decref(biyj__sae)
    vchiz__meyz = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(nav__ynqya._getvalue(), is_error=vchiz__meyz)


@lower_constant(DateOffsetType)
def lower_constant_date_offset(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    nav__ynqya = cgutils.create_struct_proxy(ty)(context, builder)
    nav__ynqya.n = n
    nav__ynqya.normalize = normalize
    has_kws = False
    vte__dkvgk = [0] * 9 + [-1] * 9
    for hoe__qedsa, orv__sdx in enumerate(date_offset_fields):
        if hasattr(pyval, orv__sdx):
            setattr(nav__ynqya, orv__sdx, context.get_constant(types.int64,
                getattr(pyval, orv__sdx)))
            if orv__sdx != 'nanoseconds' and orv__sdx != 'nanosecond':
                has_kws = True
        else:
            setattr(nav__ynqya, orv__sdx, context.get_constant(types.int64,
                vte__dkvgk[hoe__qedsa]))
    nav__ynqya.has_kws = context.get_constant(types.boolean, has_kws)
    return nav__ynqya._getvalue()


@overload(pd.tseries.offsets.DateOffset, no_unliteral=True)
def DateOffset(n=1, normalize=False, years=None, months=None, weeks=None,
    days=None, hours=None, minutes=None, seconds=None, microseconds=None,
    nanoseconds=None, year=None, month=None, day=None, weekday=None, hour=
    None, minute=None, second=None, microsecond=None, nanosecond=None):
    has_kws = False
    fuf__bnq = [years, months, weeks, days, hours, minutes, seconds,
        microseconds, year, month, day, weekday, hour, minute, second,
        microsecond]
    for cjsqo__zwz in fuf__bnq:
        if not is_overload_none(cjsqo__zwz):
            has_kws = True
            break

    def impl(n=1, normalize=False, years=None, months=None, weeks=None,
        days=None, hours=None, minutes=None, seconds=None, microseconds=
        None, nanoseconds=None, year=None, month=None, day=None, weekday=
        None, hour=None, minute=None, second=None, microsecond=None,
        nanosecond=None):
        years = 0 if years is None else years
        months = 0 if months is None else months
        weeks = 0 if weeks is None else weeks
        days = 0 if days is None else days
        hours = 0 if hours is None else hours
        minutes = 0 if minutes is None else minutes
        seconds = 0 if seconds is None else seconds
        microseconds = 0 if microseconds is None else microseconds
        nanoseconds = 0 if nanoseconds is None else nanoseconds
        year = -1 if year is None else year
        month = -1 if month is None else month
        weekday = -1 if weekday is None else weekday
        day = -1 if day is None else day
        hour = -1 if hour is None else hour
        minute = -1 if minute is None else minute
        second = -1 if second is None else second
        microsecond = -1 if microsecond is None else microsecond
        nanosecond = -1 if nanosecond is None else nanosecond
        return init_date_offset(n, normalize, years, months, weeks, days,
            hours, minutes, seconds, microseconds, nanoseconds, year, month,
            day, weekday, hour, minute, second, microsecond, nanosecond,
            has_kws)
    return impl


@intrinsic
def init_date_offset(typingctx, n, normalize, years, months, weeks, days,
    hours, minutes, seconds, microseconds, nanoseconds, year, month, day,
    weekday, hour, minute, second, microsecond, nanosecond, has_kws):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        nav__ynqya = cgutils.create_struct_proxy(typ)(context, builder)
        nav__ynqya.n = args[0]
        nav__ynqya.normalize = args[1]
        nav__ynqya.years = args[2]
        nav__ynqya.months = args[3]
        nav__ynqya.weeks = args[4]
        nav__ynqya.days = args[5]
        nav__ynqya.hours = args[6]
        nav__ynqya.minutes = args[7]
        nav__ynqya.seconds = args[8]
        nav__ynqya.microseconds = args[9]
        nav__ynqya.nanoseconds = args[10]
        nav__ynqya.year = args[11]
        nav__ynqya.month = args[12]
        nav__ynqya.day = args[13]
        nav__ynqya.weekday = args[14]
        nav__ynqya.hour = args[15]
        nav__ynqya.minute = args[16]
        nav__ynqya.second = args[17]
        nav__ynqya.microsecond = args[18]
        nav__ynqya.nanosecond = args[19]
        nav__ynqya.has_kws = args[20]
        return nav__ynqya._getvalue()
    return DateOffsetType()(n, normalize, years, months, weeks, days, hours,
        minutes, seconds, microseconds, nanoseconds, year, month, day,
        weekday, hour, minute, second, microsecond, nanosecond, has_kws
        ), codegen


make_attribute_wrapper(DateOffsetType, 'n', 'n')
make_attribute_wrapper(DateOffsetType, 'normalize', 'normalize')
make_attribute_wrapper(DateOffsetType, 'years', '_years')
make_attribute_wrapper(DateOffsetType, 'months', '_months')
make_attribute_wrapper(DateOffsetType, 'weeks', '_weeks')
make_attribute_wrapper(DateOffsetType, 'days', '_days')
make_attribute_wrapper(DateOffsetType, 'hours', '_hours')
make_attribute_wrapper(DateOffsetType, 'minutes', '_minutes')
make_attribute_wrapper(DateOffsetType, 'seconds', '_seconds')
make_attribute_wrapper(DateOffsetType, 'microseconds', '_microseconds')
make_attribute_wrapper(DateOffsetType, 'nanoseconds', '_nanoseconds')
make_attribute_wrapper(DateOffsetType, 'year', '_year')
make_attribute_wrapper(DateOffsetType, 'month', '_month')
make_attribute_wrapper(DateOffsetType, 'weekday', '_weekday')
make_attribute_wrapper(DateOffsetType, 'day', '_day')
make_attribute_wrapper(DateOffsetType, 'hour', '_hour')
make_attribute_wrapper(DateOffsetType, 'minute', '_minute')
make_attribute_wrapper(DateOffsetType, 'second', '_second')
make_attribute_wrapper(DateOffsetType, 'microsecond', '_microsecond')
make_attribute_wrapper(DateOffsetType, 'nanosecond', '_nanosecond')
make_attribute_wrapper(DateOffsetType, 'has_kws', '_has_kws')


@register_jitable
def relative_delta_addition(dateoffset, ts):
    if dateoffset._has_kws:
        mpgys__mwowv = -1 if dateoffset.n < 0 else 1
        for txknd__inb in range(np.abs(dateoffset.n)):
            year = ts.year
            month = ts.month
            day = ts.day
            hour = ts.hour
            minute = ts.minute
            second = ts.second
            microsecond = ts.microsecond
            nanosecond = ts.nanosecond
            if dateoffset._year != -1:
                year = dateoffset._year
            year += mpgys__mwowv * dateoffset._years
            if dateoffset._month != -1:
                month = dateoffset._month
            month += mpgys__mwowv * dateoffset._months
            year, month, zvaq__arf = calculate_month_end_date(year, month,
                day, 0)
            if day > zvaq__arf:
                day = zvaq__arf
            if dateoffset._day != -1:
                day = dateoffset._day
            if dateoffset._hour != -1:
                hour = dateoffset._hour
            if dateoffset._minute != -1:
                minute = dateoffset._minute
            if dateoffset._second != -1:
                second = dateoffset._second
            if dateoffset._microsecond != -1:
                microsecond = dateoffset._microsecond
            ts = pd.Timestamp(year=year, month=month, day=day, hour=hour,
                minute=minute, second=second, microsecond=microsecond,
                nanosecond=nanosecond)
            fpnam__myhq = pd.Timedelta(days=dateoffset._days + 7 *
                dateoffset._weeks, hours=dateoffset._hours, minutes=
                dateoffset._minutes, seconds=dateoffset._seconds,
                microseconds=dateoffset._microseconds)
            if mpgys__mwowv == -1:
                fpnam__myhq = -fpnam__myhq
            ts = ts + fpnam__myhq
            if dateoffset._weekday != -1:
                ocoea__ayjrq = ts.weekday()
                dqzx__lnie = (dateoffset._weekday - ocoea__ayjrq) % 7
                ts = ts + pd.Timedelta(days=dqzx__lnie)
        return ts
    else:
        return pd.Timedelta(days=dateoffset.n) + ts


def overload_add_operator_date_offset_type(lhs, rhs):
    if lhs == date_offset_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            ts = relative_delta_addition(lhs, rhs)
            if lhs.normalize:
                return ts.normalize()
            return ts
        return impl
    if lhs == date_offset_type and rhs in [datetime_date_type,
        datetime_datetime_type]:

        def impl(lhs, rhs):
            ts = relative_delta_addition(lhs, pd.Timestamp(rhs))
            if lhs.normalize:
                return ts.normalize()
            return ts
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == date_offset_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


def overload_sub_operator_offsets(lhs, rhs):
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs in [date_offset_type, month_begin_type, month_end_type,
        week_type]:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl


@overload(operator.neg, no_unliteral=True)
def overload_neg(lhs):
    if lhs == month_begin_type:

        def impl(lhs):
            return pd.tseries.offsets.MonthBegin(-lhs.n, lhs.normalize)
    if lhs == month_end_type:

        def impl(lhs):
            return pd.tseries.offsets.MonthEnd(-lhs.n, lhs.normalize)
    if lhs == week_type:

        def impl(lhs):
            return pd.tseries.offsets.Week(-lhs.n, lhs.normalize, lhs.weekday)
    if lhs == date_offset_type:

        def impl(lhs):
            n = -lhs.n
            normalize = lhs.normalize
            nanoseconds = lhs._nanoseconds
            nanosecond = lhs._nanosecond
            if lhs._has_kws:
                years = lhs._years
                months = lhs._months
                weeks = lhs._weeks
                days = lhs._days
                hours = lhs._hours
                minutes = lhs._minutes
                seconds = lhs._seconds
                microseconds = lhs._microseconds
                year = lhs._year
                month = lhs._month
                day = lhs._day
                weekday = lhs._weekday
                hour = lhs._hour
                minute = lhs._minute
                second = lhs._second
                microsecond = lhs._microsecond
                return pd.tseries.offsets.DateOffset(n, normalize, years,
                    months, weeks, days, hours, minutes, seconds,
                    microseconds, nanoseconds, year, month, day, weekday,
                    hour, minute, second, microsecond, nanosecond)
            else:
                return pd.tseries.offsets.DateOffset(n, normalize,
                    nanoseconds=nanoseconds, nanosecond=nanosecond)
    return impl


def is_offsets_type(val):
    return val in [date_offset_type, month_begin_type, month_end_type,
        week_type]


class WeekType(types.Type):

    def __init__(self):
        super(WeekType, self).__init__(name='WeekType()')


week_type = WeekType()


@typeof_impl.register(pd.tseries.offsets.Week)
def typeof_week(val, c):
    return week_type


@register_model(WeekType)
class WeekModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        lltjn__uai = [('n', types.int64), ('normalize', types.boolean), (
            'weekday', types.int64)]
        super(WeekModel, self).__init__(dmm, fe_type, lltjn__uai)


make_attribute_wrapper(WeekType, 'n', 'n')
make_attribute_wrapper(WeekType, 'normalize', 'normalize')
make_attribute_wrapper(WeekType, 'weekday', 'weekday')


@overload(pd.tseries.offsets.Week, no_unliteral=True)
def Week(n=1, normalize=False, weekday=None):

    def impl(n=1, normalize=False, weekday=None):
        jyxkb__fgde = -1 if weekday is None else weekday
        return init_week(n, normalize, jyxkb__fgde)
    return impl


@intrinsic
def init_week(typingctx, n, normalize, weekday):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        yew__nyny = cgutils.create_struct_proxy(typ)(context, builder)
        yew__nyny.n = args[0]
        yew__nyny.normalize = args[1]
        yew__nyny.weekday = args[2]
        return yew__nyny._getvalue()
    return WeekType()(n, normalize, weekday), codegen


@lower_constant(WeekType)
def lower_constant_week(context, builder, ty, pyval):
    yew__nyny = cgutils.create_struct_proxy(ty)(context, builder)
    yew__nyny.n = context.get_constant(types.int64, pyval.n)
    yew__nyny.normalize = context.get_constant(types.boolean, pyval.normalize)
    if pyval.weekday is not None:
        yew__nyny.weekday = context.get_constant(types.int64, pyval.weekday)
    else:
        yew__nyny.weekday = context.get_constant(types.int64, -1)
    return yew__nyny._getvalue()


@box(WeekType)
def box_week(typ, val, c):
    yew__nyny = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    ftk__bvd = c.pyapi.long_from_longlong(yew__nyny.n)
    biyj__sae = c.pyapi.from_native_value(types.boolean, yew__nyny.
        normalize, c.env_manager)
    oynqx__vvu = c.pyapi.long_from_longlong(yew__nyny.weekday)
    xcbh__ltctt = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.Week))
    junhq__oamjn = c.builder.icmp_signed('!=', lir.Constant(lir.IntType(64),
        -1), yew__nyny.weekday)
    with c.builder.if_else(junhq__oamjn) as (weekday_defined, weekday_undefined
        ):
        with weekday_defined:
            bjt__vzz = c.pyapi.call_function_objargs(xcbh__ltctt, (ftk__bvd,
                biyj__sae, oynqx__vvu))
            dwwex__pjh = c.builder.block
        with weekday_undefined:
            ihns__kev = c.pyapi.call_function_objargs(xcbh__ltctt, (
                ftk__bvd, biyj__sae))
            xprj__pmfl = c.builder.block
    jymah__orqyy = c.builder.phi(bjt__vzz.type)
    jymah__orqyy.add_incoming(bjt__vzz, dwwex__pjh)
    jymah__orqyy.add_incoming(ihns__kev, xprj__pmfl)
    c.pyapi.decref(oynqx__vvu)
    c.pyapi.decref(ftk__bvd)
    c.pyapi.decref(biyj__sae)
    c.pyapi.decref(xcbh__ltctt)
    return jymah__orqyy


@unbox(WeekType)
def unbox_week(typ, val, c):
    ftk__bvd = c.pyapi.object_getattr_string(val, 'n')
    biyj__sae = c.pyapi.object_getattr_string(val, 'normalize')
    oynqx__vvu = c.pyapi.object_getattr_string(val, 'weekday')
    n = c.pyapi.long_as_longlong(ftk__bvd)
    normalize = c.pyapi.to_native_value(types.bool_, biyj__sae).value
    gvrq__xwb = c.pyapi.make_none()
    hrdcv__dutt = c.builder.icmp_unsigned('==', oynqx__vvu, gvrq__xwb)
    with c.builder.if_else(hrdcv__dutt) as (weekday_undefined, weekday_defined
        ):
        with weekday_defined:
            bjt__vzz = c.pyapi.long_as_longlong(oynqx__vvu)
            dwwex__pjh = c.builder.block
        with weekday_undefined:
            ihns__kev = lir.Constant(lir.IntType(64), -1)
            xprj__pmfl = c.builder.block
    jymah__orqyy = c.builder.phi(bjt__vzz.type)
    jymah__orqyy.add_incoming(bjt__vzz, dwwex__pjh)
    jymah__orqyy.add_incoming(ihns__kev, xprj__pmfl)
    yew__nyny = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    yew__nyny.n = n
    yew__nyny.normalize = normalize
    yew__nyny.weekday = jymah__orqyy
    c.pyapi.decref(ftk__bvd)
    c.pyapi.decref(biyj__sae)
    c.pyapi.decref(oynqx__vvu)
    vchiz__meyz = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(yew__nyny._getvalue(), is_error=vchiz__meyz)


def overload_add_operator_week_offset_type(lhs, rhs):
    if lhs == week_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            nglr__iakl = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            if lhs.normalize:
                awi__zafq = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                awi__zafq = rhs
            return awi__zafq + nglr__iakl
        return impl
    if lhs == week_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            nglr__iakl = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            if lhs.normalize:
                awi__zafq = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                awi__zafq = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day, hour=rhs.hour, minute=rhs.minute, second=
                    rhs.second, microsecond=rhs.microsecond)
            return awi__zafq + nglr__iakl
        return impl
    if lhs == week_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            nglr__iakl = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            return rhs + nglr__iakl
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == week_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


@register_jitable
def calculate_week_date(n, weekday, other_weekday):
    if weekday == -1:
        return pd.Timedelta(weeks=n)
    if weekday != other_weekday:
        ruml__wutwd = (weekday - other_weekday) % 7
        if n > 0:
            n = n - 1
    return pd.Timedelta(weeks=n, days=ruml__wutwd)
