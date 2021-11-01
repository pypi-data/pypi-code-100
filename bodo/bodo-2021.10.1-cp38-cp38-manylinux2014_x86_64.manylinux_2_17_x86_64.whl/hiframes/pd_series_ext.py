"""
Implement pd.Series typing and data model handling.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.core.typing.templates import AttributeTemplate, bound_function, signature
from numba.extending import infer_getattr, intrinsic, lower_builtin, lower_cast, models, overload, overload_attribute, overload_method, register_model
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.datetime_timedelta_ext import pd_timedelta_type
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_type
from bodo.io import csv_cpp
from bodo.libs.int_arr_ext import IntDtype
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.utils.transform import get_const_func_output_type
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, dtype_to_array_type, get_overload_const_str, get_overload_const_tuple, get_udf_error_msg, get_udf_out_arr_type, is_heterogeneous_tuple_type, is_overload_constant_str, is_overload_constant_tuple, is_overload_false, is_overload_int, is_overload_none
_csv_output_is_dir = types.ExternalFunction('csv_output_is_dir', types.int8
    (types.voidptr))
ll.add_symbol('csv_output_is_dir', csv_cpp.csv_output_is_dir)


class SeriesType(types.IterableType, types.ArrayCompatible):
    ndim = 1

    def __init__(self, dtype, data=None, index=None, name_typ=None, dist=None):
        from bodo.hiframes.pd_index_ext import RangeIndexType
        from bodo.transforms.distributed_analysis import Distribution
        data = dtype_to_array_type(dtype) if data is None else data
        dtype = dtype.dtype if isinstance(dtype, IntDtype) else dtype
        self.dtype = dtype
        self.data = data
        name_typ = types.none if name_typ is None else name_typ
        index = RangeIndexType(types.none) if index is None else index
        self.index = index
        self.name_typ = name_typ
        dist = Distribution.OneD_Var if dist is None else dist
        self.dist = dist
        super(SeriesType, self).__init__(name=
            f'series({dtype}, {data}, {index}, {name_typ}, {dist})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self, dtype=None, index=None, dist=None):
        if index is None:
            index = self.index
        if dist is None:
            dist = self.dist
        if dtype is None:
            dtype = self.dtype
            data = self.data
        else:
            data = dtype_to_array_type(dtype)
        return SeriesType(dtype, data, index, self.name_typ, dist)

    @property
    def key(self):
        return self.dtype, self.data, self.index, self.name_typ, self.dist

    def unify(self, typingctx, other):
        from bodo.transforms.distributed_analysis import Distribution
        if isinstance(other, SeriesType):
            zmdx__dptiu = (self.index if self.index == other.index else
                self.index.unify(typingctx, other.index))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if other.dtype == self.dtype or not other.dtype.is_precise():
                return SeriesType(self.dtype, self.data.unify(typingctx,
                    other.data), zmdx__dptiu, dist=dist)
        return super(SeriesType, self).unify(typingctx, other)

    def can_convert_to(self, typingctx, other):
        from numba.core.typeconv import Conversion
        if (isinstance(other, SeriesType) and self.dtype == other.dtype and
            self.data == other.data and self.index == other.index and self.
            name_typ == other.name_typ and self.dist != other.dist):
            return Conversion.safe

    def is_precise(self):
        return self.dtype.is_precise()

    @property
    def iterator_type(self):
        return self.data.iterator_type


class HeterogeneousSeriesType(types.Type):
    ndim = 1

    def __init__(self, data=None, index=None, name_typ=None):
        from bodo.hiframes.pd_index_ext import RangeIndexType
        from bodo.transforms.distributed_analysis import Distribution
        self.data = data
        name_typ = types.none if name_typ is None else name_typ
        index = RangeIndexType(types.none) if index is None else index
        self.index = index
        self.name_typ = name_typ
        self.dist = Distribution.REP
        super(HeterogeneousSeriesType, self).__init__(name=
            f'heter_series({data}, {index}, {name_typ})')

    def copy(self, index=None, dist=None):
        from bodo.transforms.distributed_analysis import Distribution
        assert dist == Distribution.REP, 'invalid distribution for HeterogeneousSeriesType'
        if index is None:
            index = self.index.copy()
        return HeterogeneousSeriesType(self.data, index, self.name_typ)

    @property
    def key(self):
        return self.data, self.index, self.name_typ


@lower_builtin('getiter', SeriesType)
def series_getiter(context, builder, sig, args):
    oszb__seef = get_series_payload(context, builder, sig.args[0], args[0])
    impl = context.get_function('getiter', sig.return_type(sig.args[0].data))
    return impl(builder, (oszb__seef.data,))


@infer_getattr
class HeterSeriesAttribute(AttributeTemplate):
    key = HeterogeneousSeriesType

    def generic_resolve(self, S, attr):
        from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
        if isinstance(S.index, HeterogeneousIndexType
            ) and is_overload_constant_tuple(S.index.data):
            dnicg__vqpa = get_overload_const_tuple(S.index.data)
            if attr in dnicg__vqpa:
                lfead__tagy = dnicg__vqpa.index(attr)
                return S.data[lfead__tagy]


def is_str_series_typ(t):
    return isinstance(t, SeriesType) and t.dtype == string_type


def is_dt64_series_typ(t):
    return isinstance(t, SeriesType) and t.dtype == types.NPDatetime('ns')


def is_timedelta64_series_typ(t):
    return isinstance(t, SeriesType) and t.dtype == types.NPTimedelta('ns')


def is_datetime_date_series_typ(t):
    return isinstance(t, SeriesType) and t.dtype == datetime_date_type


class SeriesPayloadType(types.Type):

    def __init__(self, series_type):
        self.series_type = series_type
        super(SeriesPayloadType, self).__init__(name=
            f'SeriesPayloadType({series_type})')


@register_model(SeriesPayloadType)
class SeriesPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        cgi__rajh = [('data', fe_type.series_type.data), ('index', fe_type.
            series_type.index), ('name', fe_type.series_type.name_typ)]
        super(SeriesPayloadModel, self).__init__(dmm, fe_type, cgi__rajh)


@register_model(HeterogeneousSeriesType)
@register_model(SeriesType)
class SeriesModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = SeriesPayloadType(fe_type)
        cgi__rajh = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(SeriesModel, self).__init__(dmm, fe_type, cgi__rajh)


def define_series_dtor(context, builder, series_type, payload_type):
    lkhxj__lgyj = builder.module
    wtmm__ssnml = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    ypbv__wrebt = cgutils.get_or_insert_function(lkhxj__lgyj, wtmm__ssnml,
        name='.dtor.series.{}'.format(series_type))
    if not ypbv__wrebt.is_declaration:
        return ypbv__wrebt
    ypbv__wrebt.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(ypbv__wrebt.append_basic_block())
    dbpcp__fst = ypbv__wrebt.args[0]
    slum__gkro = context.get_value_type(payload_type).as_pointer()
    mnl__btlmp = builder.bitcast(dbpcp__fst, slum__gkro)
    xcob__chb = context.make_helper(builder, payload_type, ref=mnl__btlmp)
    context.nrt.decref(builder, series_type.data, xcob__chb.data)
    context.nrt.decref(builder, series_type.index, xcob__chb.index)
    context.nrt.decref(builder, series_type.name_typ, xcob__chb.name)
    builder.ret_void()
    return ypbv__wrebt


def construct_series(context, builder, series_type, data_val, index_val,
    name_val):
    payload_type = SeriesPayloadType(series_type)
    oszb__seef = cgutils.create_struct_proxy(payload_type)(context, builder)
    oszb__seef.data = data_val
    oszb__seef.index = index_val
    oszb__seef.name = name_val
    kuw__irds = context.get_value_type(payload_type)
    wtcp__euay = context.get_abi_sizeof(kuw__irds)
    hhn__eat = define_series_dtor(context, builder, series_type, payload_type)
    poi__lvtf = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, wtcp__euay), hhn__eat)
    manx__papf = context.nrt.meminfo_data(builder, poi__lvtf)
    bbnfz__xlrqw = builder.bitcast(manx__papf, kuw__irds.as_pointer())
    builder.store(oszb__seef._getvalue(), bbnfz__xlrqw)
    series = cgutils.create_struct_proxy(series_type)(context, builder)
    series.meminfo = poi__lvtf
    series.parent = cgutils.get_null_value(series.parent.type)
    return series._getvalue()


@intrinsic
def init_series(typingctx, data, index, name=None):
    from bodo.hiframes.pd_index_ext import is_pd_index_type
    from bodo.hiframes.pd_multi_index_ext import MultiIndexType
    assert is_pd_index_type(index) or isinstance(index, MultiIndexType)
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        data_val, index_val, name_val = args
        series_type = signature.return_type
        vfjm__vla = construct_series(context, builder, series_type,
            data_val, index_val, name_val)
        context.nrt.incref(builder, signature.args[0], data_val)
        context.nrt.incref(builder, signature.args[1], index_val)
        context.nrt.incref(builder, signature.args[2], name_val)
        return vfjm__vla
    if is_heterogeneous_tuple_type(data):
        aujc__pqgfp = HeterogeneousSeriesType(data, index, name)
    else:
        dtype = data.dtype
        data = if_series_to_array_type(data)
        aujc__pqgfp = SeriesType(dtype, data, index, name)
    sig = signature(aujc__pqgfp, data, index, name)
    return sig, codegen


def init_series_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) >= 2 and not kws
    data = args[0]
    index = args[1]
    sgmj__aev = self.typemap[data.name]
    if is_heterogeneous_tuple_type(sgmj__aev) or isinstance(sgmj__aev,
        types.BaseTuple):
        return None
    grkk__euvx = self.typemap[index.name]
    if not isinstance(grkk__euvx, HeterogeneousIndexType
        ) and equiv_set.has_shape(data) and equiv_set.has_shape(index):
        equiv_set.insert_equiv(data, index)
    if equiv_set.has_shape(data):
        return ArrayAnalysis.AnalyzeResult(shape=data, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_series_ext_init_series = (
    init_series_equiv)


def get_series_payload(context, builder, series_type, value):
    poi__lvtf = cgutils.create_struct_proxy(series_type)(context, builder,
        value).meminfo
    payload_type = SeriesPayloadType(series_type)
    xcob__chb = context.nrt.meminfo_data(builder, poi__lvtf)
    slum__gkro = context.get_value_type(payload_type).as_pointer()
    xcob__chb = builder.bitcast(xcob__chb, slum__gkro)
    return context.make_helper(builder, payload_type, ref=xcob__chb)


@intrinsic
def get_series_data(typingctx, series_typ=None):

    def codegen(context, builder, signature, args):
        oszb__seef = get_series_payload(context, builder, signature.args[0],
            args[0])
        return impl_ret_borrowed(context, builder, series_typ.data,
            oszb__seef.data)
    aujc__pqgfp = series_typ.data
    sig = signature(aujc__pqgfp, series_typ)
    return sig, codegen


@intrinsic
def get_series_index(typingctx, series_typ=None):

    def codegen(context, builder, signature, args):
        oszb__seef = get_series_payload(context, builder, signature.args[0],
            args[0])
        return impl_ret_borrowed(context, builder, series_typ.index,
            oszb__seef.index)
    aujc__pqgfp = series_typ.index
    sig = signature(aujc__pqgfp, series_typ)
    return sig, codegen


@intrinsic
def get_series_name(typingctx, series_typ=None):

    def codegen(context, builder, signature, args):
        oszb__seef = get_series_payload(context, builder, signature.args[0],
            args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            oszb__seef.name)
    sig = signature(series_typ.name_typ, series_typ)
    return sig, codegen


def get_series_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    jttht__dfcq = args[0]
    sgmj__aev = self.typemap[jttht__dfcq.name].data
    if is_heterogeneous_tuple_type(sgmj__aev) or isinstance(sgmj__aev,
        types.BaseTuple):
        return None
    if equiv_set.has_shape(jttht__dfcq):
        return ArrayAnalysis.AnalyzeResult(shape=jttht__dfcq, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_series_ext_get_series_data
    ) = get_series_data_equiv


def get_series_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    jttht__dfcq = args[0]
    grkk__euvx = self.typemap[jttht__dfcq.name].index
    if isinstance(grkk__euvx, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(jttht__dfcq):
        return ArrayAnalysis.AnalyzeResult(shape=jttht__dfcq, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_series_ext_get_series_index
    ) = get_series_index_equiv


def alias_ext_init_series(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    if len(args) > 1:
        numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
            arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_series',
    'bodo.hiframes.pd_series_ext'] = alias_ext_init_series


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_series_data',
    'bodo.hiframes.pd_series_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_series_index',
    'bodo.hiframes.pd_series_ext'] = alias_ext_dummy_func


def is_series_type(typ):
    return isinstance(typ, SeriesType)


def if_series_to_array_type(typ):
    if isinstance(typ, SeriesType):
        return typ.data
    return typ


@lower_cast(SeriesType, SeriesType)
def cast_series(context, builder, fromty, toty, val):
    if fromty.copy(index=toty.index) == toty and isinstance(fromty.index,
        bodo.hiframes.pd_index_ext.RangeIndexType) and isinstance(toty.
        index, bodo.hiframes.pd_index_ext.NumericIndexType):
        oszb__seef = get_series_payload(context, builder, fromty, val)
        zmdx__dptiu = context.cast(builder, oszb__seef.index, fromty.index,
            toty.index)
        context.nrt.incref(builder, fromty.data, oszb__seef.data)
        context.nrt.incref(builder, fromty.name_typ, oszb__seef.name)
        return construct_series(context, builder, toty, oszb__seef.data,
            zmdx__dptiu, oszb__seef.name)
    if (fromty.dtype == toty.dtype and fromty.data == toty.data and fromty.
        index == toty.index and fromty.name_typ == toty.name_typ and fromty
        .dist != toty.dist):
        return val
    return val


@infer_getattr
class SeriesAttribute(AttributeTemplate):
    key = SeriesType

    @bound_function('series.head')
    def resolve_head(self, ary, args, kws):
        snu__gaghz = 'Series.head'
        gpvma__bcf = 'n',
        lzx__dbv = {'n': 5}
        pysig, undx__cyx = bodo.utils.typing.fold_typing_args(snu__gaghz,
            args, kws, gpvma__bcf, lzx__dbv)
        wnisl__yhci = undx__cyx[0]
        if not is_overload_int(wnisl__yhci):
            raise BodoError(f"{snu__gaghz}(): 'n' must be an Integer")
        fbbj__dfo = ary
        return fbbj__dfo(*undx__cyx).replace(pysig=pysig)

    def _resolve_map_func(self, ary, func, pysig, fname, f_args=None, kws=None
        ):
        dtype = ary.dtype
        if dtype == types.NPDatetime('ns'):
            dtype = pd_timestamp_type
        if dtype == types.NPTimedelta('ns'):
            dtype = pd_timedelta_type
        ssmy__qpb = dtype,
        if f_args is not None:
            ssmy__qpb += tuple(f_args.types)
        if kws is None:
            kws = {}
        oxhci__ilev = False
        ljw__ctipr = True
        if fname == 'map' and isinstance(func, types.DictType):
            aya__idv = func.value_type
            oxhci__ilev = True
        else:
            try:
                if types.unliteral(func) == types.unicode_type:
                    if not is_overload_constant_str(func):
                        raise BodoError(
                            f'Series.apply(): string argument (for builtins) must be a compile time constant'
                            )
                    aya__idv = bodo.utils.transform.get_udf_str_return_type(ary
                        , get_overload_const_str(func), self.context,
                        'Series.apply')
                    ljw__ctipr = False
                elif bodo.utils.typing.is_numpy_ufunc(func):
                    aya__idv = func.get_call_type(self.context, (ary,), {}
                        ).return_type
                    ljw__ctipr = False
                else:
                    aya__idv = get_const_func_output_type(func, ssmy__qpb,
                        kws, self.context, numba.core.registry.cpu_target.
                        target_context)
            except Exception as ymfl__szuzz:
                raise BodoError(get_udf_error_msg(f'Series.{fname}()',
                    ymfl__szuzz))
        if ljw__ctipr:
            if isinstance(aya__idv, (SeriesType, HeterogeneousSeriesType)
                ) and aya__idv.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(aya__idv, HeterogeneousSeriesType):
                vchob__xveg, veffp__ggefl = aya__idv.const_info
                nqzte__qao = tuple(dtype_to_array_type(t) for t in aya__idv
                    .data.types)
                gwbq__bvhmp = bodo.DataFrameType(nqzte__qao, ary.index,
                    veffp__ggefl)
            elif isinstance(aya__idv, SeriesType):
                hgcls__mua, veffp__ggefl = aya__idv.const_info
                nqzte__qao = tuple(dtype_to_array_type(aya__idv.dtype) for
                    vchob__xveg in range(hgcls__mua))
                gwbq__bvhmp = bodo.DataFrameType(nqzte__qao, ary.index,
                    veffp__ggefl)
            else:
                nfwi__dlhr = get_udf_out_arr_type(aya__idv, oxhci__ilev)
                gwbq__bvhmp = SeriesType(nfwi__dlhr.dtype, nfwi__dlhr, ary.
                    index, ary.name_typ)
        else:
            gwbq__bvhmp = aya__idv
        return signature(gwbq__bvhmp, (func,)).replace(pysig=pysig)

    @bound_function('series.map', no_unliteral=True)
    def resolve_map(self, ary, args, kws):
        kws = dict(kws)
        func = args[0] if len(args) > 0 else kws['arg']
        kws.pop('arg', None)
        na_action = args[1] if len(args) > 1 else kws.pop('na_action',
            types.none)
        dfvd__rerm = dict(na_action=na_action)
        zoerg__hoa = dict(na_action=None)
        check_unsupported_args('Series.map', dfvd__rerm, zoerg__hoa)

        def map_stub(arg, na_action=None):
            pass
        pysig = numba.core.utils.pysignature(map_stub)
        return self._resolve_map_func(ary, func, pysig, 'map')

    @bound_function('series.apply', no_unliteral=True)
    def resolve_apply(self, ary, args, kws):
        kws = dict(kws)
        func = args[0] if len(args) > 0 else kws['func']
        kws.pop('func', None)
        zgu__qah = args[1] if len(args) > 1 else kws.pop('convert_dtype',
            types.literal(True))
        f_args = args[2] if len(args) > 2 else kws.pop('args', None)
        dfvd__rerm = dict(convert_dtype=zgu__qah)
        jius__iihej = dict(convert_dtype=True)
        check_unsupported_args('Series.apply', dfvd__rerm, jius__iihej)
        obk__pecgb = ', '.join("{} = ''".format(xxsrs__gldy) for
            xxsrs__gldy in kws.keys())
        wsbtl__welqz = (
            f'def apply_stub(func, convert_dtype=True, args=(), {obk__pecgb}):\n'
            )
        wsbtl__welqz += '    pass\n'
        shf__qzq = {}
        exec(wsbtl__welqz, {}, shf__qzq)
        dxo__vtp = shf__qzq['apply_stub']
        pysig = numba.core.utils.pysignature(dxo__vtp)
        return self._resolve_map_func(ary, func, pysig, 'apply', f_args, kws)

    def _resolve_combine_func(self, ary, args, kws):
        kwargs = dict(kws)
        other = args[0] if len(args) > 0 else types.unliteral(kwargs['other'])
        func = args[1] if len(args) > 1 else kwargs['func']
        fill_value = args[2] if len(args) > 2 else types.unliteral(kwargs.
            get('fill_value', types.none))

        def combine_stub(other, func, fill_value=None):
            pass
        pysig = numba.core.utils.pysignature(combine_stub)
        htl__nyrs = ary.dtype
        if htl__nyrs == types.NPDatetime('ns'):
            htl__nyrs = pd_timestamp_type
        yuwcl__rdy = other.dtype
        if yuwcl__rdy == types.NPDatetime('ns'):
            yuwcl__rdy = pd_timestamp_type
        aya__idv = get_const_func_output_type(func, (htl__nyrs, yuwcl__rdy),
            {}, self.context, numba.core.registry.cpu_target.target_context)
        sig = signature(SeriesType(aya__idv, index=ary.index, name_typ=
            types.none), (other, func, fill_value))
        return sig.replace(pysig=pysig)

    @bound_function('series.combine', no_unliteral=True)
    def resolve_combine(self, ary, args, kws):
        return self._resolve_combine_func(ary, args, kws)

    @bound_function('series.pipe', no_unliteral=True)
    def resolve_pipe(self, ary, args, kws):
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, ary,
            args, kws, 'Series')

    def generic_resolve(self, S, attr):
        from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
        if isinstance(S.index, HeterogeneousIndexType
            ) and is_overload_constant_tuple(S.index.data):
            dnicg__vqpa = get_overload_const_tuple(S.index.data)
            if attr in dnicg__vqpa:
                lfead__tagy = dnicg__vqpa.index(attr)
                return S.data[lfead__tagy]


series_binary_ops = tuple(op for op in numba.core.typing.npydecl.
    NumpyRulesArrayOperator._op_map.keys() if op not in (operator.lshift,
    operator.rshift))
series_inplace_binary_ops = tuple(op for op in numba.core.typing.npydecl.
    NumpyRulesInplaceArrayOperator._op_map.keys() if op not in (operator.
    ilshift, operator.irshift, operator.itruediv))
inplace_binop_to_imm = {operator.iadd: operator.add, operator.isub:
    operator.sub, operator.imul: operator.mul, operator.ifloordiv: operator
    .floordiv, operator.imod: operator.mod, operator.ipow: operator.pow,
    operator.iand: operator.and_, operator.ior: operator.or_, operator.ixor:
    operator.xor}
series_unary_ops = operator.neg, operator.invert, operator.pos
str2str_methods = ('capitalize', 'lower', 'lstrip', 'rstrip', 'strip',
    'swapcase', 'title', 'upper')
str2bool_methods = ('isalnum', 'isalpha', 'isdigit', 'isspace', 'islower',
    'isupper', 'istitle', 'isnumeric', 'isdecimal')


@overload(pd.Series, no_unliteral=True)
def pd_series_overload(data=None, index=None, dtype=None, name=None, copy=
    False, fastpath=False):
    if not is_overload_false(fastpath):
        raise BodoError("pd.Series(): 'fastpath' argument not supported.")
    vubcr__qpcuf = is_overload_none(data)
    dbh__qran = is_overload_none(index)
    cor__wbfh = is_overload_none(dtype)
    if vubcr__qpcuf and dbh__qran and cor__wbfh:
        raise BodoError(
            'pd.Series() requires at least 1 of data, index, and dtype to not be none'
            )
    if is_heterogeneous_tuple_type(data) and is_overload_none(dtype):

        def impl_heter(data=None, index=None, dtype=None, name=None, copy=
            False, fastpath=False):
            squ__ivolv = bodo.utils.conversion.extract_index_if_none(data,
                index)
            sbhgz__ikvy = bodo.utils.conversion.to_tuple(data)
            return bodo.hiframes.pd_series_ext.init_series(sbhgz__ikvy,
                bodo.utils.conversion.convert_to_index(squ__ivolv), name)
        return impl_heter
    if vubcr__qpcuf:
        if cor__wbfh:

            def impl(data=None, index=None, dtype=None, name=None, copy=
                False, fastpath=False):
                tfk__oqlr = bodo.utils.conversion.extract_name_if_none(data,
                    name)
                squ__ivolv = bodo.utils.conversion.extract_index_if_none(data,
                    index)
                numba.parfors.parfor.init_prange()
                ujd__rjnvf = len(squ__ivolv)
                sbhgz__ikvy = np.empty(ujd__rjnvf, np.float64)
                for kej__xjf in numba.parfors.parfor.internal_prange(ujd__rjnvf
                    ):
                    bodo.libs.array_kernels.setna(sbhgz__ikvy, kej__xjf)
                return bodo.hiframes.pd_series_ext.init_series(sbhgz__ikvy,
                    bodo.utils.conversion.convert_to_index(squ__ivolv),
                    tfk__oqlr)
            return impl
        if bodo.utils.conversion._is_str_dtype(dtype):
            euse__qxcxl = bodo.string_array_type
        else:
            fqf__jyg = bodo.utils.typing.parse_dtype(dtype, 'pandas.Series')
            if isinstance(fqf__jyg, bodo.libs.int_arr_ext.IntDtype):
                euse__qxcxl = bodo.IntegerArrayType(fqf__jyg.dtype)
            elif fqf__jyg == bodo.libs.bool_arr_ext.boolean_dtype:
                euse__qxcxl = bodo.boolean_array
            elif isinstance(fqf__jyg, types.Number) or fqf__jyg in [bodo.
                datetime64ns, bodo.timedelta64ns]:
                euse__qxcxl = types.Array(fqf__jyg, 1, 'C')
            else:
                raise BodoError(
                    'pd.Series with dtype: {dtype} not currently supported')
        if dbh__qran:

            def impl(data=None, index=None, dtype=None, name=None, copy=
                False, fastpath=False):
                tfk__oqlr = bodo.utils.conversion.extract_name_if_none(data,
                    name)
                squ__ivolv = bodo.hiframes.pd_index_ext.init_range_index(0,
                    0, 1, None)
                numba.parfors.parfor.init_prange()
                ujd__rjnvf = len(squ__ivolv)
                sbhgz__ikvy = bodo.utils.utils.alloc_type(ujd__rjnvf,
                    euse__qxcxl, (-1,))
                return bodo.hiframes.pd_series_ext.init_series(sbhgz__ikvy,
                    squ__ivolv, tfk__oqlr)
            return impl
        else:

            def impl(data=None, index=None, dtype=None, name=None, copy=
                False, fastpath=False):
                tfk__oqlr = bodo.utils.conversion.extract_name_if_none(data,
                    name)
                squ__ivolv = bodo.utils.conversion.extract_index_if_none(data,
                    index)
                numba.parfors.parfor.init_prange()
                ujd__rjnvf = len(squ__ivolv)
                sbhgz__ikvy = bodo.utils.utils.alloc_type(ujd__rjnvf,
                    euse__qxcxl, (-1,))
                for kej__xjf in numba.parfors.parfor.internal_prange(ujd__rjnvf
                    ):
                    bodo.libs.array_kernels.setna(sbhgz__ikvy, kej__xjf)
                return bodo.hiframes.pd_series_ext.init_series(sbhgz__ikvy,
                    bodo.utils.conversion.convert_to_index(squ__ivolv),
                    tfk__oqlr)
            return impl

    def impl(data=None, index=None, dtype=None, name=None, copy=False,
        fastpath=False):
        tfk__oqlr = bodo.utils.conversion.extract_name_if_none(data, name)
        squ__ivolv = bodo.utils.conversion.extract_index_if_none(data, index)
        uuurs__yru = bodo.utils.conversion.coerce_to_array(data, True,
            scalar_to_arr_len=len(squ__ivolv))
        bncn__ztv = bodo.utils.conversion.fix_arr_dtype(uuurs__yru, dtype,
            None, False)
        return bodo.hiframes.pd_series_ext.init_series(bncn__ztv, bodo.
            utils.conversion.convert_to_index(squ__ivolv), tfk__oqlr)
    return impl


@overload_method(SeriesType, 'to_csv', no_unliteral=True)
def to_csv_overload(series, path_or_buf=None, sep=',', na_rep='',
    float_format=None, columns=None, header=True, index=True, index_label=
    None, mode='w', encoding=None, compression='infer', quoting=None,
    quotechar='"', line_terminator=None, chunksize=None, date_format=None,
    doublequote=True, escapechar=None, decimal='.', errors='strict',
    _is_parallel=False):
    if not (is_overload_none(path_or_buf) or is_overload_constant_str(
        path_or_buf) or path_or_buf == string_type):
        raise BodoError(
            "Series.to_csv(): 'path_or_buf' argument should be None or string")
    if is_overload_none(path_or_buf):

        def _impl(series, path_or_buf=None, sep=',', na_rep='',
            float_format=None, columns=None, header=True, index=True,
            index_label=None, mode='w', encoding=None, compression='infer',
            quoting=None, quotechar='"', line_terminator=None, chunksize=
            None, date_format=None, doublequote=True, escapechar=None,
            decimal='.', errors='strict', _is_parallel=False):
            with numba.objmode(D='unicode_type'):
                D = series.to_csv(None, sep, na_rep, float_format, columns,
                    header, index, index_label, mode, encoding, compression,
                    quoting, quotechar, line_terminator, chunksize,
                    date_format, doublequote, escapechar, decimal, errors)
            return D
        return _impl

    def _impl(series, path_or_buf=None, sep=',', na_rep='', float_format=
        None, columns=None, header=True, index=True, index_label=None, mode
        ='w', encoding=None, compression='infer', quoting=None, quotechar=
        '"', line_terminator=None, chunksize=None, date_format=None,
        doublequote=True, escapechar=None, decimal='.', errors='strict',
        _is_parallel=False):
        if _is_parallel:
            header &= (bodo.libs.distributed_api.get_rank() == 0
                ) | _csv_output_is_dir(unicode_to_utf8(path_or_buf))
        with numba.objmode(D='unicode_type'):
            D = series.to_csv(None, sep, na_rep, float_format, columns,
                header, index, index_label, mode, encoding, compression,
                quoting, quotechar, line_terminator, chunksize, date_format,
                doublequote, escapechar, decimal, errors)
        bodo.io.fs_io.csv_write(path_or_buf, D, _is_parallel)
    return _impl


series_unsupported_attrs = ('array', 'at', 'attrs', 'axes', 'is_unique',
    'sparse')
series_unsupported_methods = ('convert_dtypes', 'infer_objects', 'bool',
    'to_period', 'to_timestamp', '__array__', 'get', 'at', '__iter__',
    'items', 'iteritems', 'keys', 'pop', 'item', 'xs', 'combine_first',
    'agg', 'aggregate', 'transform', 'expanding', 'ewm', 'clip',
    'factorize', 'mode', 'rank', 'align', 'drop', 'droplevel', 'duplicated',
    'first', 'last', 'reindex', 'reindex_like', 'rename_axis', 'sample',
    'set_axis', 'truncate', 'add_prefix', 'add_suffix', 'filter',
    'backfill', 'bfill', 'ffill', 'interpolate', 'pad', 'argmin', 'argmax',
    'reorder_levels', 'swaplevel', 'unstack', 'searchsorted', 'ravel',
    'squeeze', 'view', 'compare', 'update', 'asfreq', 'asof',
    'first_valid_index', 'last_valid_index', 'resample', 'tz_convert',
    'tz_localize', 'at_time', 'between_time', 'tshift', 'slice_shift',
    'plot', 'hist', 'to_pickle', 'to_excel', 'to_xarray', 'to_hdf',
    'to_string', 'to_clipboard', 'to_latex', 'to_markdown')


def _install_series_unsupported():
    for pgruc__dhvdv in series_unsupported_attrs:
        mid__cnbqw = 'Series.' + pgruc__dhvdv
        overload_attribute(SeriesType, pgruc__dhvdv)(
            create_unsupported_overload(mid__cnbqw))
    for fname in series_unsupported_methods:
        mid__cnbqw = 'Series.' + fname
        overload_method(SeriesType, fname, no_unliteral=True)(
            create_unsupported_overload(mid__cnbqw))


_install_series_unsupported()
