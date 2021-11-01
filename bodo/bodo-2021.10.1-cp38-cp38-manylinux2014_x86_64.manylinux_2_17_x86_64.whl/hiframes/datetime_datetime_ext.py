import datetime
import numba
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
"""
Implementation is based on
https://github.com/python/cpython/blob/39a5c889d30d03a88102e56f03ee0c95db198fb3/Lib/datetime.py
"""


class DatetimeDatetimeType(types.Type):

    def __init__(self):
        super(DatetimeDatetimeType, self).__init__(name=
            'DatetimeDatetimeType()')


datetime_datetime_type = DatetimeDatetimeType()
types.datetime_datetime_type = datetime_datetime_type


@typeof_impl.register(datetime.datetime)
def typeof_datetime_datetime(val, c):
    return datetime_datetime_type


@register_model(DatetimeDatetimeType)
class DatetimeDateTimeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        cold__knmk = [('year', types.int64), ('month', types.int64), ('day',
            types.int64), ('hour', types.int64), ('minute', types.int64), (
            'second', types.int64), ('microsecond', types.int64)]
        super(DatetimeDateTimeModel, self).__init__(dmm, fe_type, cold__knmk)


@box(DatetimeDatetimeType)
def box_datetime_datetime(typ, val, c):
    mpcfo__ksw = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    zqqlx__kahy = c.pyapi.long_from_longlong(mpcfo__ksw.year)
    btqd__hxcz = c.pyapi.long_from_longlong(mpcfo__ksw.month)
    oiyjc__csab = c.pyapi.long_from_longlong(mpcfo__ksw.day)
    vjp__zabgm = c.pyapi.long_from_longlong(mpcfo__ksw.hour)
    amfy__nuy = c.pyapi.long_from_longlong(mpcfo__ksw.minute)
    phoy__kvn = c.pyapi.long_from_longlong(mpcfo__ksw.second)
    bbake__ymn = c.pyapi.long_from_longlong(mpcfo__ksw.microsecond)
    iwbdn__xtlam = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        datetime))
    lts__vhtrz = c.pyapi.call_function_objargs(iwbdn__xtlam, (zqqlx__kahy,
        btqd__hxcz, oiyjc__csab, vjp__zabgm, amfy__nuy, phoy__kvn, bbake__ymn))
    c.pyapi.decref(zqqlx__kahy)
    c.pyapi.decref(btqd__hxcz)
    c.pyapi.decref(oiyjc__csab)
    c.pyapi.decref(vjp__zabgm)
    c.pyapi.decref(amfy__nuy)
    c.pyapi.decref(phoy__kvn)
    c.pyapi.decref(bbake__ymn)
    c.pyapi.decref(iwbdn__xtlam)
    return lts__vhtrz


@unbox(DatetimeDatetimeType)
def unbox_datetime_datetime(typ, val, c):
    zqqlx__kahy = c.pyapi.object_getattr_string(val, 'year')
    btqd__hxcz = c.pyapi.object_getattr_string(val, 'month')
    oiyjc__csab = c.pyapi.object_getattr_string(val, 'day')
    vjp__zabgm = c.pyapi.object_getattr_string(val, 'hour')
    amfy__nuy = c.pyapi.object_getattr_string(val, 'minute')
    phoy__kvn = c.pyapi.object_getattr_string(val, 'second')
    bbake__ymn = c.pyapi.object_getattr_string(val, 'microsecond')
    mpcfo__ksw = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    mpcfo__ksw.year = c.pyapi.long_as_longlong(zqqlx__kahy)
    mpcfo__ksw.month = c.pyapi.long_as_longlong(btqd__hxcz)
    mpcfo__ksw.day = c.pyapi.long_as_longlong(oiyjc__csab)
    mpcfo__ksw.hour = c.pyapi.long_as_longlong(vjp__zabgm)
    mpcfo__ksw.minute = c.pyapi.long_as_longlong(amfy__nuy)
    mpcfo__ksw.second = c.pyapi.long_as_longlong(phoy__kvn)
    mpcfo__ksw.microsecond = c.pyapi.long_as_longlong(bbake__ymn)
    c.pyapi.decref(zqqlx__kahy)
    c.pyapi.decref(btqd__hxcz)
    c.pyapi.decref(oiyjc__csab)
    c.pyapi.decref(vjp__zabgm)
    c.pyapi.decref(amfy__nuy)
    c.pyapi.decref(phoy__kvn)
    c.pyapi.decref(bbake__ymn)
    uvln__mdee = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(mpcfo__ksw._getvalue(), is_error=uvln__mdee)


@lower_constant(DatetimeDatetimeType)
def constant_datetime(context, builder, ty, pyval):
    year = context.get_constant(types.int64, pyval.year)
    month = context.get_constant(types.int64, pyval.month)
    day = context.get_constant(types.int64, pyval.day)
    hour = context.get_constant(types.int64, pyval.hour)
    minute = context.get_constant(types.int64, pyval.minute)
    second = context.get_constant(types.int64, pyval.second)
    microsecond = context.get_constant(types.int64, pyval.microsecond)
    gniy__tctkw = cgutils.create_struct_proxy(ty)(context, builder)
    gniy__tctkw.year = year
    gniy__tctkw.month = month
    gniy__tctkw.day = day
    gniy__tctkw.hour = hour
    gniy__tctkw.minute = minute
    gniy__tctkw.second = second
    gniy__tctkw.microsecond = microsecond
    return gniy__tctkw._getvalue()


@overload(datetime.datetime, no_unliteral=True)
def datetime_datetime(year, month, day, hour=0, minute=0, second=0,
    microsecond=0):

    def impl_datetime(year, month, day, hour=0, minute=0, second=0,
        microsecond=0):
        return init_datetime(year, month, day, hour, minute, second,
            microsecond)
    return impl_datetime


@intrinsic
def init_datetime(typingctx, year, month, day, hour, minute, second,
    microsecond):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        mpcfo__ksw = cgutils.create_struct_proxy(typ)(context, builder)
        mpcfo__ksw.year = args[0]
        mpcfo__ksw.month = args[1]
        mpcfo__ksw.day = args[2]
        mpcfo__ksw.hour = args[3]
        mpcfo__ksw.minute = args[4]
        mpcfo__ksw.second = args[5]
        mpcfo__ksw.microsecond = args[6]
        return mpcfo__ksw._getvalue()
    return DatetimeDatetimeType()(year, month, day, hour, minute, second,
        microsecond), codegen


make_attribute_wrapper(DatetimeDatetimeType, 'year', '_year')
make_attribute_wrapper(DatetimeDatetimeType, 'month', '_month')
make_attribute_wrapper(DatetimeDatetimeType, 'day', '_day')
make_attribute_wrapper(DatetimeDatetimeType, 'hour', '_hour')
make_attribute_wrapper(DatetimeDatetimeType, 'minute', '_minute')
make_attribute_wrapper(DatetimeDatetimeType, 'second', '_second')
make_attribute_wrapper(DatetimeDatetimeType, 'microsecond', '_microsecond')


@overload_attribute(DatetimeDatetimeType, 'year')
def datetime_get_year(dt):

    def impl(dt):
        return dt._year
    return impl


@overload_attribute(DatetimeDatetimeType, 'month')
def datetime_get_month(dt):

    def impl(dt):
        return dt._month
    return impl


@overload_attribute(DatetimeDatetimeType, 'day')
def datetime_get_day(dt):

    def impl(dt):
        return dt._day
    return impl


@overload_attribute(DatetimeDatetimeType, 'hour')
def datetime_get_hour(dt):

    def impl(dt):
        return dt._hour
    return impl


@overload_attribute(DatetimeDatetimeType, 'minute')
def datetime_get_minute(dt):

    def impl(dt):
        return dt._minute
    return impl


@overload_attribute(DatetimeDatetimeType, 'second')
def datetime_get_second(dt):

    def impl(dt):
        return dt._second
    return impl


@overload_attribute(DatetimeDatetimeType, 'microsecond')
def datetime_get_microsecond(dt):

    def impl(dt):
        return dt._microsecond
    return impl


@overload_method(DatetimeDatetimeType, 'date', no_unliteral=True)
def date(dt):

    def impl(dt):
        return datetime.date(dt.year, dt.month, dt.day)
    return impl


@register_jitable
def now_impl():
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.now()
    return d


@register_jitable
def strptime_impl(date_string, dtformat):
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.strptime(date_string, dtformat)
    return d


@register_jitable
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


def create_cmp_op_overload(op):

    def overload_datetime_cmp(lhs, rhs):
        if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

            def impl(lhs, rhs):
                y, kuw__dfybg = lhs.year, rhs.year
                nmzs__uvlek, rbq__atm = lhs.month, rhs.month
                d, dwv__ieymi = lhs.day, rhs.day
                ewg__bcan, juawm__ubfz = lhs.hour, rhs.hour
                nwwjw__jxj, rwwj__mfgxl = lhs.minute, rhs.minute
                bgmo__gjm, tpo__axwh = lhs.second, rhs.second
                lhnd__efja, jigyr__jgu = lhs.microsecond, rhs.microsecond
                return op(_cmp((y, nmzs__uvlek, d, ewg__bcan, nwwjw__jxj,
                    bgmo__gjm, lhnd__efja), (kuw__dfybg, rbq__atm,
                    dwv__ieymi, juawm__ubfz, rwwj__mfgxl, tpo__axwh,
                    jigyr__jgu)), 0)
            return impl
    return overload_datetime_cmp


def overload_sub_operator_datetime_datetime(lhs, rhs):
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            vton__ysls = lhs.toordinal()
            jvdi__zun = rhs.toordinal()
            wxe__hbbzc = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            ritye__dwgv = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            olv__mokb = datetime.timedelta(vton__ysls - jvdi__zun, 
                wxe__hbbzc - ritye__dwgv, lhs.microsecond - rhs.microsecond)
            return olv__mokb
        return impl


@lower_cast(types.Optional(numba.core.types.NPTimedelta('ns')), numba.core.
    types.NPTimedelta('ns'))
@lower_cast(types.Optional(numba.core.types.NPDatetime('ns')), numba.core.
    types.NPDatetime('ns'))
def optional_dt64_to_dt64(context, builder, fromty, toty, val):
    bclzz__ocpm = context.make_helper(builder, fromty, value=val)
    psbd__jldc = cgutils.as_bool_bit(builder, bclzz__ocpm.valid)
    with builder.if_else(psbd__jldc) as (then, orelse):
        with then:
            voej__mpzr = context.cast(builder, bclzz__ocpm.data, fromty.
                type, toty)
            jxt__lqe = builder.block
        with orelse:
            tgr__vrdj = numba.np.npdatetime.NAT
            meq__yll = builder.block
    lts__vhtrz = builder.phi(voej__mpzr.type)
    lts__vhtrz.add_incoming(voej__mpzr, jxt__lqe)
    lts__vhtrz.add_incoming(tgr__vrdj, meq__yll)
    return lts__vhtrz
