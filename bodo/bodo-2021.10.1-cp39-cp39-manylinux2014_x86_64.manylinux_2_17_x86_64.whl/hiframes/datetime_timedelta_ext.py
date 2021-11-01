"""Numba extension support for datetime.timedelta objects and their arrays.
"""
import datetime
import operator
from collections import namedtuple
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.libs import hdatetime_ext
from bodo.utils.indexing import get_new_null_mask_bool_index, get_new_null_mask_int_index, get_new_null_mask_slice_index, setitem_slice_index_null_bits
from bodo.utils.typing import BodoError, get_overload_const_str, is_iterable_type, is_list_like_index_type, is_overload_constant_str
ll.add_symbol('box_datetime_timedelta_array', hdatetime_ext.
    box_datetime_timedelta_array)
ll.add_symbol('unbox_datetime_timedelta_array', hdatetime_ext.
    unbox_datetime_timedelta_array)


class NoInput:
    pass


_no_input = NoInput()


class NoInputType(types.Type):

    def __init__(self):
        super(NoInputType, self).__init__(name='NoInput')


register_model(NoInputType)(models.OpaqueModel)


@typeof_impl.register(NoInput)
def _typ_no_input(val, c):
    return NoInputType()


@lower_constant(NoInputType)
def constant_no_input(context, builder, ty, pyval):
    return context.get_dummy_value()


class PDTimeDeltaType(types.Type):

    def __init__(self):
        super(PDTimeDeltaType, self).__init__(name='PDTimeDeltaType()')


pd_timedelta_type = PDTimeDeltaType()
types.pd_timedelta_type = pd_timedelta_type


@typeof_impl.register(pd.Timedelta)
def typeof_pd_timedelta(val, c):
    return pd_timedelta_type


@register_model(PDTimeDeltaType)
class PDTimeDeltaModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        cgp__ypkl = [('value', types.int64)]
        super(PDTimeDeltaModel, self).__init__(dmm, fe_type, cgp__ypkl)


@box(PDTimeDeltaType)
def box_pd_timedelta(typ, val, c):
    ynwek__mgpmp = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    sos__awp = c.pyapi.long_from_longlong(ynwek__mgpmp.value)
    rvs__pzyr = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timedelta))
    res = c.pyapi.call_function_objargs(rvs__pzyr, (sos__awp,))
    c.pyapi.decref(sos__awp)
    c.pyapi.decref(rvs__pzyr)
    return res


@unbox(PDTimeDeltaType)
def unbox_pd_timedelta(typ, val, c):
    sos__awp = c.pyapi.object_getattr_string(val, 'value')
    cmiea__ded = c.pyapi.long_as_longlong(sos__awp)
    ynwek__mgpmp = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ynwek__mgpmp.value = cmiea__ded
    c.pyapi.decref(sos__awp)
    cmm__igdc = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ynwek__mgpmp._getvalue(), is_error=cmm__igdc)


@lower_constant(PDTimeDeltaType)
def lower_constant_pd_timedelta(context, builder, ty, pyval):
    value = context.get_constant(types.int64, pyval.value)
    pd_timedelta = cgutils.create_struct_proxy(ty)(context, builder)
    pd_timedelta.value = value
    return pd_timedelta._getvalue()


@overload(pd.Timedelta, no_unliteral=True)
def pd_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
    microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    if value == _no_input:

        def impl_timedelta_kw(value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
            days += weeks * 7
            hours += days * 24
            minutes += 60 * hours
            seconds += 60 * minutes
            milliseconds += 1000 * seconds
            microseconds += 1000 * milliseconds
            yunr__bgwfn = 1000 * microseconds
            return init_pd_timedelta(yunr__bgwfn)
        return impl_timedelta_kw
    if value == bodo.string_type or is_overload_constant_str(value):

        def impl_str(value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
            with numba.objmode(res='pd_timedelta_type'):
                res = pd.Timedelta(value)
            return res
        return impl_str
    if value == pd_timedelta_type:
        return (lambda value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0: value)
    if value == datetime_timedelta_type:

        def impl_timedelta_datetime(value=_no_input, unit='ns', days=0,
            seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0,
            weeks=0):
            days = value.days
            seconds = 60 * 60 * 24 * days + value.seconds
            microseconds = 1000 * 1000 * seconds + value.microseconds
            yunr__bgwfn = 1000 * microseconds
            return init_pd_timedelta(yunr__bgwfn)
        return impl_timedelta_datetime
    if not is_overload_constant_str(unit):
        raise BodoError('pd.to_timedelta(): unit should be a constant string')
    unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
        get_overload_const_str(unit))
    ufosn__ikyz, uynuf__evmkd = pd._libs.tslibs.conversion.precision_from_unit(
        unit)

    def impl_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
        microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return init_pd_timedelta(value * ufosn__ikyz)
    return impl_timedelta


@intrinsic
def init_pd_timedelta(typingctx, value):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        timedelta = cgutils.create_struct_proxy(typ)(context, builder)
        timedelta.value = args[0]
        return timedelta._getvalue()
    return PDTimeDeltaType()(value), codegen


make_attribute_wrapper(PDTimeDeltaType, 'value', '_value')


@overload_attribute(PDTimeDeltaType, 'value')
@overload_attribute(PDTimeDeltaType, 'delta')
def pd_timedelta_get_value(td):

    def impl(td):
        return td._value
    return impl


@overload_attribute(PDTimeDeltaType, 'days')
def pd_timedelta_get_days(td):

    def impl(td):
        return td._value // (1000 * 1000 * 1000 * 60 * 60 * 24)
    return impl


@overload_attribute(PDTimeDeltaType, 'seconds')
def pd_timedelta_get_seconds(td):

    def impl(td):
        return td._value // (1000 * 1000 * 1000) % (60 * 60 * 24)
    return impl


@overload_attribute(PDTimeDeltaType, 'microseconds')
def pd_timedelta_get_microseconds(td):

    def impl(td):
        return td._value // 1000 % 1000000
    return impl


@overload_attribute(PDTimeDeltaType, 'nanoseconds')
def pd_timedelta_get_nanoseconds(td):

    def impl(td):
        return td._value % 1000
    return impl


@register_jitable
def _to_hours_pd_td(td):
    return td._value // (1000 * 1000 * 1000 * 60 * 60) % 24


@register_jitable
def _to_minutes_pd_td(td):
    return td._value // (1000 * 1000 * 1000 * 60) % 60


@register_jitable
def _to_seconds_pd_td(td):
    return td._value // (1000 * 1000 * 1000) % 60


@register_jitable
def _to_milliseconds_pd_td(td):
    return td._value // (1000 * 1000) % 1000


@register_jitable
def _to_microseconds_pd_td(td):
    return td._value // 1000 % 1000


Components = namedtuple('Components', ['days', 'hours', 'minutes',
    'seconds', 'milliseconds', 'microseconds', 'nanoseconds'], defaults=[0,
    0, 0, 0, 0, 0, 0])


@overload_attribute(PDTimeDeltaType, 'components', no_unliteral=True)
def pd_timedelta_get_components(td):

    def impl(td):
        a = Components(td.days, _to_hours_pd_td(td), _to_minutes_pd_td(td),
            _to_seconds_pd_td(td), _to_milliseconds_pd_td(td),
            _to_microseconds_pd_td(td), td.nanoseconds)
        return a
    return impl


@overload_method(PDTimeDeltaType, '__hash__', no_unliteral=True)
def pd_td___hash__(td):

    def impl(td):
        return hash(td._value)
    return impl


@overload_method(PDTimeDeltaType, 'to_numpy', no_unliteral=True)
@overload_method(PDTimeDeltaType, 'to_timedelta64', no_unliteral=True)
def pd_td_to_numpy(td):
    from bodo.hiframes.pd_timestamp_ext import integer_to_timedelta64

    def impl(td):
        return integer_to_timedelta64(td.value)
    return impl


@overload_method(PDTimeDeltaType, 'to_pytimedelta', no_unliteral=True)
def pd_td_to_pytimedelta(td):

    def impl(td):
        return datetime.timedelta(microseconds=np.int64(td._value / 1000))
    return impl


@overload_method(PDTimeDeltaType, 'total_seconds', no_unliteral=True)
def pd_td_total_seconds(td):

    def impl(td):
        return td._value // 1000 / 10 ** 6
    return impl


def overload_add_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            val = lhs.value + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            zheb__gfmv = (rhs.microseconds + (rhs.seconds + rhs.days * 60 *
                60 * 24) * 1000 * 1000) * 1000
            val = lhs.value + zheb__gfmv
            return pd.Timedelta(val)
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            rwwjf__ini = (lhs.microseconds + (lhs.seconds + lhs.days * 60 *
                60 * 24) * 1000 * 1000) * 1000
            val = rwwjf__ini + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_datetime_type:
        from bodo.hiframes.pd_timestamp_ext import compute_pd_timestamp

        def impl(lhs, rhs):
            hvkg__nmitc = rhs.toordinal()
            ieb__frhud = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            natds__antd = rhs.microsecond
            brebt__kqq = lhs.value // 1000
            ncoz__runk = lhs.nanoseconds
            xxyl__xau = natds__antd + brebt__kqq
            mhn__dyxv = 1000000 * (hvkg__nmitc * 86400 + ieb__frhud
                ) + xxyl__xau
            spt__ohhys = ncoz__runk
            return compute_pd_timestamp(mhn__dyxv, spt__ohhys)
        return impl
    if lhs == datetime_datetime_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + rhs.to_pytimedelta()
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs.days + rhs.days
            s = lhs.seconds + rhs.seconds
            us = lhs.microseconds + rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            fld__hsa = datetime.timedelta(rhs.toordinal(), hours=rhs.hour,
                minutes=rhs.minute, seconds=rhs.second, microseconds=rhs.
                microsecond)
            fld__hsa = fld__hsa + lhs
            szyg__nvqrq, ecsu__pvv = divmod(fld__hsa.seconds, 3600)
            fne__clmyd, jamv__kqiah = divmod(ecsu__pvv, 60)
            if 0 < fld__hsa.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(fld__hsa
                    .days)
                return datetime.datetime(d.year, d.month, d.day,
                    szyg__nvqrq, fne__clmyd, jamv__kqiah, fld__hsa.microseconds
                    )
            raise OverflowError('result out of range')
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            fld__hsa = datetime.timedelta(lhs.toordinal(), hours=lhs.hour,
                minutes=lhs.minute, seconds=lhs.second, microseconds=lhs.
                microsecond)
            fld__hsa = fld__hsa + rhs
            szyg__nvqrq, ecsu__pvv = divmod(fld__hsa.seconds, 3600)
            fne__clmyd, jamv__kqiah = divmod(ecsu__pvv, 60)
            if 0 < fld__hsa.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(fld__hsa
                    .days)
                return datetime.datetime(d.year, d.month, d.day,
                    szyg__nvqrq, fne__clmyd, jamv__kqiah, fld__hsa.microseconds
                    )
            raise OverflowError('result out of range')
        return impl


def overload_sub_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            mmvu__tpdyb = lhs.value - rhs.value
            return pd.Timedelta(mmvu__tpdyb)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_datetime_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs.days - rhs.days
            s = lhs.seconds - rhs.seconds
            us = lhs.microseconds - rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_array_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            owqaq__zbhjd = lhs
            numba.parfors.parfor.init_prange()
            n = len(owqaq__zbhjd)
            A = alloc_datetime_timedelta_array(n)
            for feqi__rjm in numba.parfors.parfor.internal_prange(n):
                A[feqi__rjm] = owqaq__zbhjd[feqi__rjm] - rhs
            return A
        return impl


def overload_mul_operator_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value * rhs)
        return impl
    elif isinstance(lhs, types.Integer) and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return pd.Timedelta(rhs.value * lhs)
        return impl
    if lhs == datetime_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            d = lhs.days * rhs
            s = lhs.seconds * rhs
            us = lhs.microseconds * rhs
            return datetime.timedelta(d, s, us)
        return impl
    elif isinstance(lhs, types.Integer) and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs * rhs.days
            s = lhs * rhs.seconds
            us = lhs * rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl


def overload_floordiv_operator_pd_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs.value // rhs.value
        return impl
    elif lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value // rhs)
        return impl


def overload_truediv_operator_pd_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs.value / rhs.value
        return impl
    elif lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(int(lhs.value / rhs))
        return impl


def overload_mod_operator_timedeltas(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value % rhs.value)
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            mrqxb__gyg = _to_microseconds(lhs) % _to_microseconds(rhs)
            return datetime.timedelta(0, 0, mrqxb__gyg)
        return impl


def pd_create_cmp_op_overload(op):

    def overload_pd_timedelta_cmp(lhs, rhs):
        if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

            def impl(lhs, rhs):
                return op(lhs.value, rhs.value)
            return impl
        if lhs == pd_timedelta_type and rhs == bodo.timedelta64ns:
            return lambda lhs, rhs: op(bodo.hiframes.pd_timestamp_ext.
                integer_to_timedelta64(lhs.value), rhs)
        if lhs == bodo.timedelta64ns and rhs == pd_timedelta_type:
            return lambda lhs, rhs: op(lhs, bodo.hiframes.pd_timestamp_ext.
                integer_to_timedelta64(rhs.value))
    return overload_pd_timedelta_cmp


@overload(operator.neg, no_unliteral=True)
def pd_timedelta_neg(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            return pd.Timedelta(-lhs.value)
        return impl


@overload(operator.pos, no_unliteral=True)
def pd_timedelta_pos(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            return lhs
        return impl


@overload(divmod, no_unliteral=True)
def pd_timedelta_divmod(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            ntb__kabo, mrqxb__gyg = divmod(lhs.value, rhs.value)
            return ntb__kabo, pd.Timedelta(mrqxb__gyg)
        return impl


@overload(abs, no_unliteral=True)
def pd_timedelta_abs(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            if lhs.value < 0:
                return -lhs
            else:
                return lhs
        return impl


class DatetimeTimeDeltaType(types.Type):

    def __init__(self):
        super(DatetimeTimeDeltaType, self).__init__(name=
            'DatetimeTimeDeltaType()')


datetime_timedelta_type = DatetimeTimeDeltaType()


@typeof_impl.register(datetime.timedelta)
def typeof_datetime_timedelta(val, c):
    return datetime_timedelta_type


@register_model(DatetimeTimeDeltaType)
class DatetimeTimeDeltaModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        cgp__ypkl = [('days', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64)]
        super(DatetimeTimeDeltaModel, self).__init__(dmm, fe_type, cgp__ypkl)


@box(DatetimeTimeDeltaType)
def box_datetime_timedelta(typ, val, c):
    ynwek__mgpmp = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    lfnhb__kly = c.pyapi.long_from_longlong(ynwek__mgpmp.days)
    jgy__plrl = c.pyapi.long_from_longlong(ynwek__mgpmp.seconds)
    ppr__fvxt = c.pyapi.long_from_longlong(ynwek__mgpmp.microseconds)
    rvs__pzyr = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        timedelta))
    res = c.pyapi.call_function_objargs(rvs__pzyr, (lfnhb__kly, jgy__plrl,
        ppr__fvxt))
    c.pyapi.decref(lfnhb__kly)
    c.pyapi.decref(jgy__plrl)
    c.pyapi.decref(ppr__fvxt)
    c.pyapi.decref(rvs__pzyr)
    return res


@unbox(DatetimeTimeDeltaType)
def unbox_datetime_timedelta(typ, val, c):
    lfnhb__kly = c.pyapi.object_getattr_string(val, 'days')
    jgy__plrl = c.pyapi.object_getattr_string(val, 'seconds')
    ppr__fvxt = c.pyapi.object_getattr_string(val, 'microseconds')
    rrdos__celp = c.pyapi.long_as_longlong(lfnhb__kly)
    vdgfp__lydx = c.pyapi.long_as_longlong(jgy__plrl)
    cwg__uvre = c.pyapi.long_as_longlong(ppr__fvxt)
    ynwek__mgpmp = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ynwek__mgpmp.days = rrdos__celp
    ynwek__mgpmp.seconds = vdgfp__lydx
    ynwek__mgpmp.microseconds = cwg__uvre
    c.pyapi.decref(lfnhb__kly)
    c.pyapi.decref(jgy__plrl)
    c.pyapi.decref(ppr__fvxt)
    cmm__igdc = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ynwek__mgpmp._getvalue(), is_error=cmm__igdc)


@lower_constant(DatetimeTimeDeltaType)
def lower_constant_datetime_timedelta(context, builder, ty, pyval):
    days = context.get_constant(types.int64, pyval.days)
    seconds = context.get_constant(types.int64, pyval.seconds)
    microseconds = context.get_constant(types.int64, pyval.microseconds)
    datetime_timedelta = cgutils.create_struct_proxy(ty)(context, builder)
    datetime_timedelta.days = days
    datetime_timedelta.seconds = seconds
    datetime_timedelta.microseconds = microseconds
    return datetime_timedelta._getvalue()


@overload(datetime.timedelta, no_unliteral=True)
def datetime_timedelta(days=0, seconds=0, microseconds=0, milliseconds=0,
    minutes=0, hours=0, weeks=0):

    def impl_timedelta(days=0, seconds=0, microseconds=0, milliseconds=0,
        minutes=0, hours=0, weeks=0):
        d = s = us = 0
        days += weeks * 7
        seconds += minutes * 60 + hours * 3600
        microseconds += milliseconds * 1000
        d = days
        days, seconds = divmod(seconds, 24 * 3600)
        d += days
        s += int(seconds)
        seconds, us = divmod(microseconds, 1000000)
        days, seconds = divmod(seconds, 24 * 3600)
        d += days
        s += seconds
        return init_timedelta(d, s, us)
    return impl_timedelta


@intrinsic
def init_timedelta(typingctx, d, s, us):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        timedelta = cgutils.create_struct_proxy(typ)(context, builder)
        timedelta.days = args[0]
        timedelta.seconds = args[1]
        timedelta.microseconds = args[2]
        return timedelta._getvalue()
    return DatetimeTimeDeltaType()(d, s, us), codegen


make_attribute_wrapper(DatetimeTimeDeltaType, 'days', '_days')
make_attribute_wrapper(DatetimeTimeDeltaType, 'seconds', '_seconds')
make_attribute_wrapper(DatetimeTimeDeltaType, 'microseconds', '_microseconds')


@overload_attribute(DatetimeTimeDeltaType, 'days')
def timedelta_get_days(td):

    def impl(td):
        return td._days
    return impl


@overload_attribute(DatetimeTimeDeltaType, 'seconds')
def timedelta_get_seconds(td):

    def impl(td):
        return td._seconds
    return impl


@overload_attribute(DatetimeTimeDeltaType, 'microseconds')
def timedelta_get_microseconds(td):

    def impl(td):
        return td._microseconds
    return impl


@overload_method(DatetimeTimeDeltaType, 'total_seconds', no_unliteral=True)
def total_seconds(td):

    def impl(td):
        return ((td._days * 86400 + td._seconds) * 10 ** 6 + td._microseconds
            ) / 10 ** 6
    return impl


@overload_method(DatetimeTimeDeltaType, '__hash__', no_unliteral=True)
def __hash__(td):

    def impl(td):
        return hash((td._days, td._seconds, td._microseconds))
    return impl


@register_jitable
def _to_nanoseconds(td):
    return np.int64(((td._days * 86400 + td._seconds) * 1000000 + td.
        _microseconds) * 1000)


@register_jitable
def _to_microseconds(td):
    return (td._days * (24 * 3600) + td._seconds) * 1000000 + td._microseconds


@register_jitable
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


@register_jitable
def _getstate(td):
    return td._days, td._seconds, td._microseconds


@register_jitable
def _divide_and_round(a, b):
    ntb__kabo, mrqxb__gyg = divmod(a, b)
    mrqxb__gyg *= 2
    zum__ucd = mrqxb__gyg > b if b > 0 else mrqxb__gyg < b
    if zum__ucd or mrqxb__gyg == b and ntb__kabo % 2 == 1:
        ntb__kabo += 1
    return ntb__kabo


_MAXORDINAL = 3652059


def overload_floordiv_operator_dt_timedelta(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return us // _to_microseconds(rhs)
        return impl
    elif lhs == datetime_timedelta_type and rhs == types.int64:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return datetime.timedelta(0, 0, us // rhs)
        return impl


def overload_truediv_operator_dt_timedelta(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return us / _to_microseconds(rhs)
        return impl
    elif lhs == datetime_timedelta_type and rhs == types.int64:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return datetime.timedelta(0, 0, _divide_and_round(us, rhs))
        return impl


def create_cmp_op_overload(op):

    def overload_timedelta_cmp(lhs, rhs):
        if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

            def impl(lhs, rhs):
                lbsj__iwlk = _cmp(_getstate(lhs), _getstate(rhs))
                return op(lbsj__iwlk, 0)
            return impl
    return overload_timedelta_cmp


@overload(operator.neg, no_unliteral=True)
def timedelta_neg(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            return datetime.timedelta(-lhs.days, -lhs.seconds, -lhs.
                microseconds)
        return impl


@overload(operator.pos, no_unliteral=True)
def timedelta_pos(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            return lhs
        return impl


@overload(divmod, no_unliteral=True)
def timedelta_divmod(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            ntb__kabo, mrqxb__gyg = divmod(_to_microseconds(lhs),
                _to_microseconds(rhs))
            return ntb__kabo, datetime.timedelta(0, 0, mrqxb__gyg)
        return impl


@overload(abs, no_unliteral=True)
def timedelta_abs(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            if lhs.days < 0:
                return -lhs
            else:
                return lhs
        return impl


@intrinsic
def cast_numpy_timedelta_to_int(typingctx, val=None):
    assert val in (types.NPTimedelta('ns'), types.int64)

    def codegen(context, builder, signature, args):
        return args[0]
    return types.int64(val), codegen


@overload(bool, no_unliteral=True)
def timedelta_to_bool(timedelta):
    if timedelta != datetime_timedelta_type:
        return
    fmh__voz = datetime.timedelta(0)

    def impl(timedelta):
        return timedelta != fmh__voz
    return impl


class DatetimeTimeDeltaArrayType(types.ArrayCompatible):

    def __init__(self):
        super(DatetimeTimeDeltaArrayType, self).__init__(name=
            'DatetimeTimeDeltaArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return datetime_timedelta_type

    def copy(self):
        return DatetimeTimeDeltaArrayType()


datetime_timedelta_array_type = DatetimeTimeDeltaArrayType()
types.datetime_timedelta_array_type = datetime_timedelta_array_type
days_data_type = types.Array(types.int64, 1, 'C')
seconds_data_type = types.Array(types.int64, 1, 'C')
microseconds_data_type = types.Array(types.int64, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(DatetimeTimeDeltaArrayType)
class DatetimeTimeDeltaArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        cgp__ypkl = [('days_data', days_data_type), ('seconds_data',
            seconds_data_type), ('microseconds_data',
            microseconds_data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, cgp__ypkl)


make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'days_data', '_days_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'seconds_data',
    '_seconds_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'microseconds_data',
    '_microseconds_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'null_bitmap',
    '_null_bitmap')


@overload_method(DatetimeTimeDeltaArrayType, 'copy', no_unliteral=True)
def overload_datetime_timedelta_arr_copy(A):
    return (lambda A: bodo.hiframes.datetime_timedelta_ext.
        init_datetime_timedelta_array(A._days_data.copy(), A._seconds_data.
        copy(), A._microseconds_data.copy(), A._null_bitmap.copy()))


@unbox(DatetimeTimeDeltaArrayType)
def unbox_datetime_timedelta_array(typ, val, c):
    n = bodo.utils.utils.object_length(c, val)
    bqebb__kgouj = types.Array(types.intp, 1, 'C')
    dsr__cuxlw = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        bqebb__kgouj, [n])
    eqrlo__fyv = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        bqebb__kgouj, [n])
    oym__nzxd = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        bqebb__kgouj, [n])
    hnja__nhnsw = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    wcmj__orb = bodo.utils.utils._empty_nd_impl(c.context, c.builder, types
        .Array(types.uint8, 1, 'C'), [hnja__nhnsw])
    xkwj__sfci = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64), lir.IntType(64).as_pointer(), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (8).as_pointer()])
    imy__ufbbi = cgutils.get_or_insert_function(c.builder.module,
        xkwj__sfci, name='unbox_datetime_timedelta_array')
    c.builder.call(imy__ufbbi, [val, n, dsr__cuxlw.data, eqrlo__fyv.data,
        oym__nzxd.data, wcmj__orb.data])
    scu__oraea = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    scu__oraea.days_data = dsr__cuxlw._getvalue()
    scu__oraea.seconds_data = eqrlo__fyv._getvalue()
    scu__oraea.microseconds_data = oym__nzxd._getvalue()
    scu__oraea.null_bitmap = wcmj__orb._getvalue()
    cmm__igdc = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(scu__oraea._getvalue(), is_error=cmm__igdc)


@box(DatetimeTimeDeltaArrayType)
def box_datetime_timedelta_array(typ, val, c):
    owqaq__zbhjd = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    dsr__cuxlw = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, owqaq__zbhjd.days_data)
    eqrlo__fyv = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, owqaq__zbhjd.seconds_data).data
    oym__nzxd = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, owqaq__zbhjd.microseconds_data).data
    wckkd__zbgie = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, owqaq__zbhjd.null_bitmap).data
    n = c.builder.extract_value(dsr__cuxlw.shape, 0)
    xkwj__sfci = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (64).as_pointer(), lir.IntType(8).as_pointer()])
    yxfmi__xgt = cgutils.get_or_insert_function(c.builder.module,
        xkwj__sfci, name='box_datetime_timedelta_array')
    orild__lzd = c.builder.call(yxfmi__xgt, [n, dsr__cuxlw.data, eqrlo__fyv,
        oym__nzxd, wckkd__zbgie])
    c.context.nrt.decref(c.builder, typ, val)
    return orild__lzd


@intrinsic
def init_datetime_timedelta_array(typingctx, days_data, seconds_data,
    microseconds_data, nulls=None):
    assert days_data == types.Array(types.int64, 1, 'C')
    assert seconds_data == types.Array(types.int64, 1, 'C')
    assert microseconds_data == types.Array(types.int64, 1, 'C')
    assert nulls == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        flhpo__pzii, ofl__cdmv, bhfl__xli, tmbv__mvmr = args
        qai__osj = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        qai__osj.days_data = flhpo__pzii
        qai__osj.seconds_data = ofl__cdmv
        qai__osj.microseconds_data = bhfl__xli
        qai__osj.null_bitmap = tmbv__mvmr
        context.nrt.incref(builder, signature.args[0], flhpo__pzii)
        context.nrt.incref(builder, signature.args[1], ofl__cdmv)
        context.nrt.incref(builder, signature.args[2], bhfl__xli)
        context.nrt.incref(builder, signature.args[3], tmbv__mvmr)
        return qai__osj._getvalue()
    itsdf__hpftg = datetime_timedelta_array_type(days_data, seconds_data,
        microseconds_data, nulls)
    return itsdf__hpftg, codegen


@lower_constant(DatetimeTimeDeltaArrayType)
def lower_constant_datetime_timedelta_arr(context, builder, typ, pyval):
    n = len(pyval)
    dsr__cuxlw = np.empty(n, np.int64)
    eqrlo__fyv = np.empty(n, np.int64)
    oym__nzxd = np.empty(n, np.int64)
    fcsq__ezs = np.empty(n + 7 >> 3, np.uint8)
    for feqi__rjm, s in enumerate(pyval):
        vtvl__drhwi = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(fcsq__ezs, feqi__rjm, int(not
            vtvl__drhwi))
        if not vtvl__drhwi:
            dsr__cuxlw[feqi__rjm] = s.days
            eqrlo__fyv[feqi__rjm] = s.seconds
            oym__nzxd[feqi__rjm] = s.microseconds
    gxvko__yqiz = context.get_constant_generic(builder, days_data_type,
        dsr__cuxlw)
    zdvz__zhjb = context.get_constant_generic(builder, seconds_data_type,
        eqrlo__fyv)
    bze__wojf = context.get_constant_generic(builder,
        microseconds_data_type, oym__nzxd)
    wwmi__dfr = context.get_constant_generic(builder, nulls_type, fcsq__ezs)
    apvo__fbcpv = context.make_helper(builder, typ)
    apvo__fbcpv.days_data = gxvko__yqiz
    apvo__fbcpv.seconds_data = zdvz__zhjb
    apvo__fbcpv.microseconds_data = bze__wojf
    apvo__fbcpv.null_bitmap = wwmi__dfr
    return apvo__fbcpv._getvalue()


@numba.njit(no_cpython_wrapper=True)
def alloc_datetime_timedelta_array(n):
    dsr__cuxlw = np.empty(n, dtype=np.int64)
    eqrlo__fyv = np.empty(n, dtype=np.int64)
    oym__nzxd = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_datetime_timedelta_array(dsr__cuxlw, eqrlo__fyv, oym__nzxd,
        nulls)


def alloc_datetime_timedelta_array_equiv(self, scope, equiv_set, loc, args, kws
    ):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_datetime_timedelta_ext_alloc_datetime_timedelta_array
    ) = alloc_datetime_timedelta_array_equiv


@overload(operator.getitem, no_unliteral=True)
def dt_timedelta_arr_getitem(A, ind):
    if A != datetime_timedelta_array_type:
        return
    if isinstance(ind, types.Integer):

        def impl_int(A, ind):
            return datetime.timedelta(days=A._days_data[ind], seconds=A.
                _seconds_data[ind], microseconds=A._microseconds_data[ind])
        return impl_int
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            ywa__pgq = bodo.utils.conversion.coerce_to_ndarray(ind)
            svvgl__hokeq = A._null_bitmap
            oznst__zkbok = A._days_data[ywa__pgq]
            shk__xoc = A._seconds_data[ywa__pgq]
            ywlh__vlwxa = A._microseconds_data[ywa__pgq]
            n = len(oznst__zkbok)
            hlym__rny = get_new_null_mask_bool_index(svvgl__hokeq, ind, n)
            return init_datetime_timedelta_array(oznst__zkbok, shk__xoc,
                ywlh__vlwxa, hlym__rny)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            ywa__pgq = bodo.utils.conversion.coerce_to_ndarray(ind)
            svvgl__hokeq = A._null_bitmap
            oznst__zkbok = A._days_data[ywa__pgq]
            shk__xoc = A._seconds_data[ywa__pgq]
            ywlh__vlwxa = A._microseconds_data[ywa__pgq]
            n = len(oznst__zkbok)
            hlym__rny = get_new_null_mask_int_index(svvgl__hokeq, ywa__pgq, n)
            return init_datetime_timedelta_array(oznst__zkbok, shk__xoc,
                ywlh__vlwxa, hlym__rny)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            n = len(A._days_data)
            svvgl__hokeq = A._null_bitmap
            oznst__zkbok = np.ascontiguousarray(A._days_data[ind])
            shk__xoc = np.ascontiguousarray(A._seconds_data[ind])
            ywlh__vlwxa = np.ascontiguousarray(A._microseconds_data[ind])
            hlym__rny = get_new_null_mask_slice_index(svvgl__hokeq, ind, n)
            return init_datetime_timedelta_array(oznst__zkbok, shk__xoc,
                ywlh__vlwxa, hlym__rny)
        return impl_slice
    raise BodoError(
        f'getitem for DatetimeTimedeltaArray with indexing type {ind} not supported.'
        )


@overload(operator.setitem, no_unliteral=True)
def dt_timedelta_arr_setitem(A, ind, val):
    if A != datetime_timedelta_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    imy__jbawf = (
        f"setitem for DatetimeTimedeltaArray with indexing type {ind} received an incorrect 'value' type {val}."
        )
    if isinstance(ind, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl(A, ind, val):
                A._days_data[ind] = val._days
                A._seconds_data[ind] = val._seconds
                A._microseconds_data[ind] = val._microseconds
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, ind, 1)
            return impl
        else:
            raise BodoError(imy__jbawf)
    if not (is_iterable_type(val) and val.dtype == bodo.
        datetime_timedelta_type or types.unliteral(val) ==
        datetime_timedelta_type):
        raise BodoError(imy__jbawf)
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_arr_ind_scalar(A, ind, val):
                n = len(A)
                for feqi__rjm in range(n):
                    A._days_data[ind[feqi__rjm]] = val._days
                    A._seconds_data[ind[feqi__rjm]] = val._seconds
                    A._microseconds_data[ind[feqi__rjm]] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[feqi__rjm], 1)
            return impl_arr_ind_scalar
        else:

            def impl_arr_ind(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(val._days_data)
                for feqi__rjm in range(n):
                    A._days_data[ind[feqi__rjm]] = val._days_data[feqi__rjm]
                    A._seconds_data[ind[feqi__rjm]] = val._seconds_data[
                        feqi__rjm]
                    A._microseconds_data[ind[feqi__rjm]
                        ] = val._microseconds_data[feqi__rjm]
                    gtf__ctfy = bodo.libs.int_arr_ext.get_bit_bitmap_arr(val
                        ._null_bitmap, feqi__rjm)
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[feqi__rjm], gtf__ctfy)
            return impl_arr_ind
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_bool_ind_mask_scalar(A, ind, val):
                n = len(ind)
                for feqi__rjm in range(n):
                    if not bodo.libs.array_kernels.isna(ind, feqi__rjm
                        ) and ind[feqi__rjm]:
                        A._days_data[feqi__rjm] = val._days
                        A._seconds_data[feqi__rjm] = val._seconds
                        A._microseconds_data[feqi__rjm] = val._microseconds
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            feqi__rjm, 1)
            return impl_bool_ind_mask_scalar
        else:

            def impl_bool_ind_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(ind)
                errg__uhf = 0
                for feqi__rjm in range(n):
                    if not bodo.libs.array_kernels.isna(ind, feqi__rjm
                        ) and ind[feqi__rjm]:
                        A._days_data[feqi__rjm] = val._days_data[errg__uhf]
                        A._seconds_data[feqi__rjm] = val._seconds_data[
                            errg__uhf]
                        A._microseconds_data[feqi__rjm
                            ] = val._microseconds_data[errg__uhf]
                        gtf__ctfy = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                            val._null_bitmap, errg__uhf)
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            feqi__rjm, gtf__ctfy)
                        errg__uhf += 1
            return impl_bool_ind_mask
    if isinstance(ind, types.SliceType):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_slice_scalar(A, ind, val):
                mjgg__gaza = numba.cpython.unicode._normalize_slice(ind, len(A)
                    )
                for feqi__rjm in range(mjgg__gaza.start, mjgg__gaza.stop,
                    mjgg__gaza.step):
                    A._days_data[feqi__rjm] = val._days
                    A._seconds_data[feqi__rjm] = val._seconds
                    A._microseconds_data[feqi__rjm] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        feqi__rjm, 1)
            return impl_slice_scalar
        else:

            def impl_slice_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(A._days_data)
                A._days_data[ind] = val._days_data
                A._seconds_data[ind] = val._seconds_data
                A._microseconds_data[ind] = val._microseconds_data
                rfyvi__erw = val._null_bitmap.copy()
                setitem_slice_index_null_bits(A._null_bitmap, rfyvi__erw,
                    ind, n)
            return impl_slice_mask
    raise BodoError(
        f'setitem for DatetimeTimedeltaArray with indexing type {ind} not supported.'
        )


@overload(len, no_unliteral=True)
def overload_len_datetime_timedelta_arr(A):
    if A == datetime_timedelta_array_type:
        return lambda A: len(A._days_data)


@overload_attribute(DatetimeTimeDeltaArrayType, 'shape')
def overload_datetime_timedelta_arr_shape(A):
    return lambda A: (len(A._days_data),)


@overload_attribute(DatetimeTimeDeltaArrayType, 'nbytes')
def timedelta_arr_nbytes_overload(A):
    return (lambda A: A._days_data.nbytes + A._seconds_data.nbytes + A.
        _microseconds_data.nbytes + A._null_bitmap.nbytes)


def overload_datetime_timedelta_arr_sub(arg1, arg2):
    if (arg1 == datetime_timedelta_array_type and arg2 ==
        datetime_timedelta_type):

        def impl(arg1, arg2):
            owqaq__zbhjd = arg1
            numba.parfors.parfor.init_prange()
            n = len(owqaq__zbhjd)
            A = alloc_datetime_timedelta_array(n)
            for feqi__rjm in numba.parfors.parfor.internal_prange(n):
                A[feqi__rjm] = owqaq__zbhjd[feqi__rjm] - arg2
            return A
        return impl


def create_cmp_op_overload_arr(op):

    def overload_date_arr_cmp(lhs, rhs):
        if op == operator.ne:
            mtn__xuuuf = True
        else:
            mtn__xuuuf = False
        if (lhs == datetime_timedelta_array_type and rhs ==
            datetime_timedelta_array_type):

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                bqc__tjggn = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for feqi__rjm in numba.parfors.parfor.internal_prange(n):
                    qlwml__lfm = bodo.libs.array_kernels.isna(lhs, feqi__rjm)
                    vzfto__vcw = bodo.libs.array_kernels.isna(rhs, feqi__rjm)
                    if qlwml__lfm or vzfto__vcw:
                        ebd__bajnu = mtn__xuuuf
                    else:
                        ebd__bajnu = op(lhs[feqi__rjm], rhs[feqi__rjm])
                    bqc__tjggn[feqi__rjm] = ebd__bajnu
                return bqc__tjggn
            return impl
        elif lhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                bqc__tjggn = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for feqi__rjm in numba.parfors.parfor.internal_prange(n):
                    gtf__ctfy = bodo.libs.array_kernels.isna(lhs, feqi__rjm)
                    if gtf__ctfy:
                        ebd__bajnu = mtn__xuuuf
                    else:
                        ebd__bajnu = op(lhs[feqi__rjm], rhs)
                    bqc__tjggn[feqi__rjm] = ebd__bajnu
                return bqc__tjggn
            return impl
        elif rhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                bqc__tjggn = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for feqi__rjm in numba.parfors.parfor.internal_prange(n):
                    gtf__ctfy = bodo.libs.array_kernels.isna(rhs, feqi__rjm)
                    if gtf__ctfy:
                        ebd__bajnu = mtn__xuuuf
                    else:
                        ebd__bajnu = op(lhs, rhs[feqi__rjm])
                    bqc__tjggn[feqi__rjm] = ebd__bajnu
                return bqc__tjggn
            return impl
    return overload_date_arr_cmp
