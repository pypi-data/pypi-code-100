"""
Implement pd.DataFrame typing and data model handling.
"""
import json
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.typing.templates import AbstractTemplate, AttributeTemplate, bound_function, infer_global, signature
from numba.extending import infer_getattr, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.hiframes.pd_index_ext import HeterogeneousIndexType, NumericIndexType, RangeIndexType, is_pd_index_type
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.hiframes.series_indexing import SeriesIlocType
from bodo.io import json_cpp
from bodo.libs.array import arr_info_list_to_table, array_to_info
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.distributed_api import bcast_scalar
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import str_arr_from_sequence, string_array_type
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils.conversion import index_to_array
from bodo.utils.transform import gen_const_tup, get_const_func_output_type, get_const_tup_vals
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, dtype_to_array_type, get_index_data_arr_types, get_literal_value, get_overload_const, get_overload_const_bool, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_udf_error_msg, get_udf_out_arr_type, is_heterogeneous_tuple_type, is_iterable_type, is_literal_type, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_str, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_tuple_like_type, raise_bodo_error, to_nullable_type
from bodo.utils.utils import is_null_pointer
_json_write = types.ExternalFunction('json_write', types.void(types.voidptr,
    types.voidptr, types.int64, types.int64, types.bool_, types.bool_,
    types.voidptr))
ll.add_symbol('json_write', json_cpp.json_write)


class DataFrameType(types.ArrayCompatible):
    ndim = 2

    def __init__(self, data=None, index=None, columns=None, dist=None):
        from bodo.transforms.distributed_analysis import Distribution
        self.data = data
        if index is None:
            index = RangeIndexType(types.none)
        self.index = index
        self.columns = columns
        dist = Distribution.OneD_Var if dist is None else dist
        self.dist = dist
        super(DataFrameType, self).__init__(name=
            f'dataframe({data}, {index}, {columns}, {dist})')

    def copy(self, index=None, dist=None):
        if index is None:
            index = self.index
        if dist is None:
            dist = self.dist
        return DataFrameType(self.data, index, self.columns, dist)

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    @property
    def key(self):
        return self.data, self.index, self.columns, self.dist

    def unify(self, typingctx, other):
        from bodo.transforms.distributed_analysis import Distribution
        if isinstance(other, DataFrameType) and len(other.data) == len(self
            .data) and other.columns == self.columns:
            cay__zpdmj = (self.index if self.index == other.index else self
                .index.unify(typingctx, other.index))
            data = tuple(bixh__qxzqm.unify(typingctx, rxjpg__afiqk) if 
                bixh__qxzqm != rxjpg__afiqk else bixh__qxzqm for 
                bixh__qxzqm, rxjpg__afiqk in zip(self.data, other.data))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if cay__zpdmj is not None and None not in data:
                return DataFrameType(data, cay__zpdmj, self.columns, dist)
        if isinstance(other, DataFrameType) and len(self.data) == 0:
            return other

    def can_convert_to(self, typingctx, other):
        from numba.core.typeconv import Conversion
        if (isinstance(other, DataFrameType) and self.data == other.data and
            self.index == other.index and self.columns == other.columns and
            self.dist != other.dist):
            return Conversion.safe

    def is_precise(self):
        return all(bixh__qxzqm.is_precise() for bixh__qxzqm in self.data
            ) and self.index.is_precise()


class DataFramePayloadType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        super(DataFramePayloadType, self).__init__(name=
            f'DataFramePayloadType({df_type})')


@register_model(DataFramePayloadType)
class DataFramePayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        yso__aiti = len(fe_type.df_type.columns)
        znwwb__govsd = [('data', types.Tuple(fe_type.df_type.data)), (
            'index', fe_type.df_type.index), ('unboxed', types.UniTuple(
            types.int8, yso__aiti + 1)), ('parent', types.pyobject)]
        super(DataFramePayloadModel, self).__init__(dmm, fe_type, znwwb__govsd)


@register_model(DataFrameType)
class DataFrameModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = DataFramePayloadType(fe_type)
        znwwb__govsd = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(DataFrameModel, self).__init__(dmm, fe_type, znwwb__govsd)


make_attribute_wrapper(DataFrameType, 'meminfo', '_meminfo')


@infer_getattr
class DataFrameAttribute(AttributeTemplate):
    key = DataFrameType

    @bound_function('df.head')
    def resolve_head(self, df, args, kws):
        func_name = 'DataFrame.head'
        tpfge__pxg = 'n',
        qvz__ssdqw = {'n': 5}
        rbtxz__vgxm, waind__rcxor = bodo.utils.typing.fold_typing_args(
            func_name, args, kws, tpfge__pxg, qvz__ssdqw)
        nvdny__dyhyg = waind__rcxor[0]
        if not is_overload_int(nvdny__dyhyg):
            raise BodoError(f"{func_name}(): 'n' must be an Integer")
        hwc__bmoxw = df
        return hwc__bmoxw(*waind__rcxor).replace(pysig=rbtxz__vgxm)

    @bound_function('df.corr')
    def resolve_corr(self, df, args, kws):
        func_name = 'DataFrame.corr'
        qwh__lsza = (df,) + args
        tpfge__pxg = 'df', 'method', 'min_periods'
        qvz__ssdqw = {'method': 'pearson', 'min_periods': 1}
        hilc__lux = 'method',
        rbtxz__vgxm, waind__rcxor = bodo.utils.typing.fold_typing_args(
            func_name, qwh__lsza, kws, tpfge__pxg, qvz__ssdqw, hilc__lux)
        qtrw__qqf = waind__rcxor[2]
        if not is_overload_int(qtrw__qqf):
            raise BodoError(f"{func_name}(): 'min_periods' must be an Integer")
        aaenq__prkik = []
        qwwul__kmsen = []
        for xcgcs__wgbld, nywvn__vsar in zip(df.columns, df.data):
            if bodo.utils.typing._is_pandas_numeric_dtype(nywvn__vsar.dtype):
                aaenq__prkik.append(xcgcs__wgbld)
                qwwul__kmsen.append(types.Array(types.float64, 1, 'A'))
        assert len(aaenq__prkik) != 0
        qwwul__kmsen = tuple(qwwul__kmsen)
        aaenq__prkik = tuple(aaenq__prkik)
        index_typ = bodo.utils.typing.type_col_to_index(aaenq__prkik)
        hwc__bmoxw = DataFrameType(qwwul__kmsen, index_typ, aaenq__prkik)
        return hwc__bmoxw(*waind__rcxor).replace(pysig=rbtxz__vgxm)

    @bound_function('df.pipe', no_unliteral=True)
    def resolve_pipe(self, df, args, kws):
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, df, args,
            kws, 'DataFrame')

    @bound_function('df.apply', no_unliteral=True)
    def resolve_apply(self, df, args, kws):
        kws = dict(kws)
        flb__iipiw = args[0] if len(args) > 0 else kws.pop('func', None)
        axis = args[1] if len(args) > 1 else kws.pop('axis', types.literal(0))
        hiwri__yitha = args[2] if len(args) > 2 else kws.pop('raw', types.
            literal(False))
        dukj__aydn = args[3] if len(args) > 3 else kws.pop('result_type',
            types.none)
        flj__atv = args[4] if len(args) > 4 else kws.pop('args', types.
            Tuple([]))
        mxurk__qfc = dict(raw=hiwri__yitha, result_type=dukj__aydn)
        hgs__nndmu = dict(raw=False, result_type=None)
        check_unsupported_args('Dataframe.apply', mxurk__qfc, hgs__nndmu)
        ankaw__smreo = True
        if types.unliteral(flb__iipiw) == types.unicode_type:
            if not is_overload_constant_str(flb__iipiw):
                raise BodoError(
                    f'DataFrame.apply(): string argument (for builtins) must be a compile time constant'
                    )
            ankaw__smreo = False
        if not is_overload_constant_int(axis):
            raise BodoError(
                'Dataframe.apply(): axis argument must be a compile time constant.'
                )
        tzf__ikkog = get_overload_const_int(axis)
        if ankaw__smreo and tzf__ikkog != 1:
            raise BodoError(
                'Dataframe.apply(): only axis=1 supported for user-defined functions'
                )
        elif tzf__ikkog not in (0, 1):
            raise BodoError('Dataframe.apply(): axis must be either 0 or 1')
        jxo__xgduk = []
        for arr_typ in df.data:
            wqmb__occ = SeriesType(arr_typ.dtype, arr_typ, df.index,
                string_type)
            qirug__ulrs = self.context.resolve_function_type(operator.
                getitem, (SeriesIlocType(wqmb__occ), types.int64), {}
                ).return_type
            jxo__xgduk.append(qirug__ulrs)
        borwg__mxod = types.none
        mlnwp__fuw = HeterogeneousIndexType(types.BaseTuple.from_types(
            tuple(types.literal(xcgcs__wgbld) for xcgcs__wgbld in df.
            columns)), None)
        occbc__lod = types.BaseTuple.from_types(jxo__xgduk)
        yugor__ljwl = df.index.dtype
        if yugor__ljwl == types.NPDatetime('ns'):
            yugor__ljwl = bodo.pd_timestamp_type
        if yugor__ljwl == types.NPTimedelta('ns'):
            yugor__ljwl = bodo.pd_timedelta_type
        if is_heterogeneous_tuple_type(occbc__lod):
            pfjfo__ndv = HeterogeneousSeriesType(occbc__lod, mlnwp__fuw,
                yugor__ljwl)
        else:
            pfjfo__ndv = SeriesType(occbc__lod.dtype, occbc__lod,
                mlnwp__fuw, yugor__ljwl)
        wgsjt__houvr = pfjfo__ndv,
        if flj__atv is not None:
            wgsjt__houvr += tuple(flj__atv.types)
        try:
            if not ankaw__smreo:
                ymyh__mag = bodo.utils.transform.get_udf_str_return_type(df,
                    get_overload_const_str(flb__iipiw), self.context,
                    'DataFrame.apply', axis if tzf__ikkog == 1 else None)
            else:
                ymyh__mag = get_const_func_output_type(flb__iipiw,
                    wgsjt__houvr, kws, self.context, numba.core.registry.
                    cpu_target.target_context)
        except Exception as ror__rmbhq:
            raise_bodo_error(get_udf_error_msg('DataFrame.apply()', ror__rmbhq)
                )
        if ankaw__smreo:
            if not (is_overload_constant_int(axis) and 
                get_overload_const_int(axis) == 1):
                raise BodoError(
                    'Dataframe.apply(): only user-defined functions with axis=1 supported'
                    )
            if isinstance(ymyh__mag, (SeriesType, HeterogeneousSeriesType)
                ) and ymyh__mag.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(ymyh__mag, HeterogeneousSeriesType):
                imlmh__cmyjk, pkuz__jaib = ymyh__mag.const_info
                kuk__ygq = tuple(dtype_to_array_type(byt__ylqs) for
                    byt__ylqs in ymyh__mag.data.types)
                inlxt__okhsq = DataFrameType(kuk__ygq, df.index, pkuz__jaib)
            elif isinstance(ymyh__mag, SeriesType):
                yso__aiti, pkuz__jaib = ymyh__mag.const_info
                kuk__ygq = tuple(dtype_to_array_type(ymyh__mag.dtype) for
                    imlmh__cmyjk in range(yso__aiti))
                inlxt__okhsq = DataFrameType(kuk__ygq, df.index, pkuz__jaib)
            else:
                jqsif__rhglq = get_udf_out_arr_type(ymyh__mag)
                inlxt__okhsq = SeriesType(jqsif__rhglq.dtype, jqsif__rhglq,
                    df.index, None)
        else:
            inlxt__okhsq = ymyh__mag
        rzyi__vlvjr = ', '.join("{} = ''".format(bixh__qxzqm) for
            bixh__qxzqm in kws.keys())
        sfl__aza = f"""def apply_stub(func, axis=0, raw=False, result_type=None, args=(), {rzyi__vlvjr}):
"""
        sfl__aza += '    pass\n'
        ozlqp__onkk = {}
        exec(sfl__aza, {}, ozlqp__onkk)
        oov__mibs = ozlqp__onkk['apply_stub']
        rbtxz__vgxm = numba.core.utils.pysignature(oov__mibs)
        qxuif__onnmv = (flb__iipiw, axis, hiwri__yitha, dukj__aydn, flj__atv
            ) + tuple(kws.values())
        return signature(inlxt__okhsq, *qxuif__onnmv).replace(pysig=rbtxz__vgxm
            )

    def generic_resolve(self, df, attr):
        if attr in df.columns:
            wlgq__clj = df.columns.index(attr)
            arr_typ = df.data[wlgq__clj]
            return SeriesType(arr_typ.dtype, arr_typ, df.index, types.
                StringLiteral(attr))
        if len(df.columns) > 0 and isinstance(df.columns[0], tuple):
            dhjx__mbw = []
            dsbds__sgr = []
            qapha__qyr = False
            for i, hzh__yiyw in enumerate(df.columns):
                if hzh__yiyw[0] != attr:
                    continue
                qapha__qyr = True
                dhjx__mbw.append(hzh__yiyw[1] if len(hzh__yiyw) == 2 else
                    hzh__yiyw[1:])
                dsbds__sgr.append(df.data[i])
            if qapha__qyr:
                return DataFrameType(tuple(dsbds__sgr), df.index, tuple(
                    dhjx__mbw))


DataFrameAttribute._no_unliteral = True


@overload(operator.getitem, no_unliteral=True)
def namedtuple_getitem_overload(tup, idx):
    if isinstance(tup, types.BaseNamedTuple) and is_overload_constant_str(idx):
        vhimi__xzj = get_overload_const_str(idx)
        val_ind = tup.instance_class._fields.index(vhimi__xzj)
        return lambda tup, idx: tup[val_ind]


def decref_df_data(context, builder, payload, df_type):
    for i in range(len(df_type.data)):
        rqdvz__brr = builder.extract_value(payload.unboxed, i)
        nzr__vovjm = builder.icmp_unsigned('==', rqdvz__brr, lir.Constant(
            rqdvz__brr.type, 1))
        with builder.if_then(nzr__vovjm):
            dokv__hkv = builder.extract_value(payload.data, i)
            context.nrt.decref(builder, df_type.data[i], dokv__hkv)
    context.nrt.decref(builder, df_type.index, payload.index)


def define_df_dtor(context, builder, df_type, payload_type):
    nnv__nvtlf = builder.module
    asw__rzyxy = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    tpbfx__cbjbo = cgutils.get_or_insert_function(nnv__nvtlf, asw__rzyxy,
        name='.dtor.df.{}'.format(df_type))
    if not tpbfx__cbjbo.is_declaration:
        return tpbfx__cbjbo
    tpbfx__cbjbo.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(tpbfx__cbjbo.append_basic_block())
    vwyn__kyzu = tpbfx__cbjbo.args[0]
    zgviv__qnboi = context.get_value_type(payload_type).as_pointer()
    szh__dyj = builder.bitcast(vwyn__kyzu, zgviv__qnboi)
    payload = context.make_helper(builder, payload_type, ref=szh__dyj)
    decref_df_data(context, builder, payload, df_type)
    has_parent = cgutils.is_not_null(builder, payload.parent)
    with builder.if_then(has_parent):
        tyr__rexx = context.get_python_api(builder)
        jtmd__vqv = tyr__rexx.gil_ensure()
        tyr__rexx.decref(payload.parent)
        tyr__rexx.gil_release(jtmd__vqv)
    builder.ret_void()
    return tpbfx__cbjbo


def construct_dataframe(context, builder, df_type, data_tup, index_val,
    unboxed_tup, parent=None):
    payload_type = DataFramePayloadType(df_type)
    nci__yea = cgutils.create_struct_proxy(payload_type)(context, builder)
    nci__yea.data = data_tup
    nci__yea.index = index_val
    nci__yea.unboxed = unboxed_tup
    jtdwb__nuls = context.get_value_type(payload_type)
    cvpxr__ltyh = context.get_abi_sizeof(jtdwb__nuls)
    bqfe__rij = define_df_dtor(context, builder, df_type, payload_type)
    zuzoa__xwuxp = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, cvpxr__ltyh), bqfe__rij)
    klib__ytkl = context.nrt.meminfo_data(builder, zuzoa__xwuxp)
    fedcv__cbs = builder.bitcast(klib__ytkl, jtdwb__nuls.as_pointer())
    meuj__jzxdp = cgutils.create_struct_proxy(df_type)(context, builder)
    meuj__jzxdp.meminfo = zuzoa__xwuxp
    if parent is None:
        meuj__jzxdp.parent = cgutils.get_null_value(meuj__jzxdp.parent.type)
    else:
        meuj__jzxdp.parent = parent
        nci__yea.parent = parent
        has_parent = cgutils.is_not_null(builder, parent)
        with builder.if_then(has_parent):
            tyr__rexx = context.get_python_api(builder)
            jtmd__vqv = tyr__rexx.gil_ensure()
            tyr__rexx.incref(parent)
            tyr__rexx.gil_release(jtmd__vqv)
    builder.store(nci__yea._getvalue(), fedcv__cbs)
    return meuj__jzxdp._getvalue()


@intrinsic
def init_dataframe(typingctx, data_tup_typ, index_typ, col_names_typ=None):
    assert is_pd_index_type(index_typ) or isinstance(index_typ, MultiIndexType
        ), 'init_dataframe(): invalid index type'
    yso__aiti = len(data_tup_typ.types)
    if yso__aiti == 0:
        yxh__jjuu = ()
    else:
        yxh__jjuu = get_const_tup_vals(col_names_typ)
    assert len(yxh__jjuu
        ) == yso__aiti, 'init_dataframe(): number of column names does not match number of columns'

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup = args[0]
        index_val = args[1]
        tzl__hogea = context.get_constant(types.int8, 1)
        unboxed_tup = context.make_tuple(builder, types.UniTuple(types.int8,
            yso__aiti + 1), [tzl__hogea] * (yso__aiti + 1))
        edwd__atpwv = construct_dataframe(context, builder, df_type,
            data_tup, index_val, unboxed_tup)
        context.nrt.incref(builder, data_tup_typ, data_tup)
        context.nrt.incref(builder, index_typ, index_val)
        return edwd__atpwv
    iwn__kxgh = DataFrameType(data_tup_typ.types, index_typ, yxh__jjuu)
    sig = signature(iwn__kxgh, data_tup_typ, index_typ, col_names_typ)
    return sig, codegen


@intrinsic
def has_parent(typingctx, df=None):

    def codegen(context, builder, sig, args):
        meuj__jzxdp = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        return cgutils.is_not_null(builder, meuj__jzxdp.parent)
    return signature(types.bool_, df), codegen


def get_dataframe_payload(context, builder, df_type, value):
    zuzoa__xwuxp = cgutils.create_struct_proxy(df_type)(context, builder, value
        ).meminfo
    payload_type = DataFramePayloadType(df_type)
    payload = context.nrt.meminfo_data(builder, zuzoa__xwuxp)
    zgviv__qnboi = context.get_value_type(payload_type).as_pointer()
    payload = builder.bitcast(payload, zgviv__qnboi)
    return context.make_helper(builder, payload_type, ref=payload)


@intrinsic
def _get_dataframe_unboxed(typingctx, df_typ=None):
    yso__aiti = len(df_typ.columns)
    iwn__kxgh = types.UniTuple(types.int8, yso__aiti + 1)
    sig = signature(iwn__kxgh, df_typ)

    def codegen(context, builder, signature, args):
        nci__yea = get_dataframe_payload(context, builder, signature.args[0
            ], args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            nci__yea.unboxed)
    return sig, codegen


@intrinsic
def _get_dataframe_data(typingctx, df_typ=None):
    iwn__kxgh = types.Tuple(df_typ.data)
    sig = signature(iwn__kxgh, df_typ)

    def codegen(context, builder, signature, args):
        nci__yea = get_dataframe_payload(context, builder, signature.args[0
            ], args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            nci__yea.data)
    return sig, codegen


@intrinsic
def get_dataframe_index(typingctx, df_typ=None):

    def codegen(context, builder, signature, args):
        nci__yea = get_dataframe_payload(context, builder, signature.args[0
            ], args[0])
        return impl_ret_borrowed(context, builder, df_typ.index, nci__yea.index
            )
    iwn__kxgh = df_typ.index
    sig = signature(iwn__kxgh, df_typ)
    return sig, codegen


def get_dataframe_data(df, i):
    return df[i]


@infer_global(get_dataframe_data)
class GetDataFrameDataInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        assert is_overload_constant_int(args[1])
        df = args[0]
        i = get_overload_const_int(args[1])
        hwc__bmoxw = df.data[i]
        return hwc__bmoxw(*args)


def get_dataframe_data_impl(df, i):

    def _impl(df, i):
        if has_parent(df) and _get_dataframe_unboxed(df)[i] == 0:
            bodo.hiframes.boxing.unbox_dataframe_column(df, i)
        return _get_dataframe_data(df)[i]
    return _impl


@lower_builtin(get_dataframe_data, DataFrameType, types.IntegerLiteral)
def lower_get_dataframe_data(context, builder, sig, args):
    impl = get_dataframe_data_impl(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_dataframe_data',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_dataframe_index',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func


def alias_ext_init_dataframe(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 3
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_dataframe',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_init_dataframe


def init_dataframe_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 3 and not kws
    data_tup = args[0]
    index = args[1]
    occbc__lod = self.typemap[data_tup.name]
    if any(is_tuple_like_type(byt__ylqs) for byt__ylqs in occbc__lod.types):
        return None
    if equiv_set.has_shape(data_tup):
        mhpm__tbm = equiv_set.get_shape(data_tup)
        if len(mhpm__tbm) > 1:
            equiv_set.insert_equiv(*mhpm__tbm)
        if len(mhpm__tbm) > 0:
            mlnwp__fuw = self.typemap[index.name]
            if not isinstance(mlnwp__fuw, HeterogeneousIndexType
                ) and equiv_set.has_shape(index):
                equiv_set.insert_equiv(mhpm__tbm[0], index)
            return ArrayAnalysis.AnalyzeResult(shape=(mhpm__tbm[0], len(
                mhpm__tbm)), pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_dataframe_ext_init_dataframe
    ) = init_dataframe_equiv


def get_dataframe_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    jdf__bly = args[0]
    xvw__zzaj = self.typemap[jdf__bly.name].data
    if any(is_tuple_like_type(byt__ylqs) for byt__ylqs in xvw__zzaj):
        return None
    if equiv_set.has_shape(jdf__bly):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            jdf__bly)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_data
    ) = get_dataframe_data_equiv


def get_dataframe_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    jdf__bly = args[0]
    mlnwp__fuw = self.typemap[jdf__bly.name].index
    if isinstance(mlnwp__fuw, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(jdf__bly):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            jdf__bly)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_index
    ) = get_dataframe_index_equiv


@intrinsic
def set_dataframe_data(typingctx, df_typ, c_ind_typ, arr_typ=None):
    assert is_overload_constant_int(c_ind_typ)
    wsdq__ntqmp = get_overload_const_int(c_ind_typ)
    if df_typ.data[wsdq__ntqmp] != arr_typ:
        raise BodoError(
            'Changing dataframe column data type inplace is not supported in conditionals/loops or for dataframe arguments'
            )

    def codegen(context, builder, signature, args):
        ayit__dmg, imlmh__cmyjk, yofz__rdufh = args
        nci__yea = get_dataframe_payload(context, builder, df_typ, ayit__dmg)
        rqdvz__brr = builder.extract_value(nci__yea.unboxed, wsdq__ntqmp)
        nzr__vovjm = builder.icmp_unsigned('==', rqdvz__brr, lir.Constant(
            rqdvz__brr.type, 1))
        with builder.if_then(nzr__vovjm):
            dokv__hkv = builder.extract_value(nci__yea.data, wsdq__ntqmp)
            context.nrt.decref(builder, df_typ.data[wsdq__ntqmp], dokv__hkv)
        nci__yea.data = builder.insert_value(nci__yea.data, yofz__rdufh,
            wsdq__ntqmp)
        nci__yea.unboxed = builder.insert_value(nci__yea.unboxed, context.
            get_constant(types.int8, 1), wsdq__ntqmp)
        context.nrt.incref(builder, arr_typ, yofz__rdufh)
        meuj__jzxdp = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=ayit__dmg)
        payload_type = DataFramePayloadType(df_typ)
        szh__dyj = context.nrt.meminfo_data(builder, meuj__jzxdp.meminfo)
        zgviv__qnboi = context.get_value_type(payload_type).as_pointer()
        szh__dyj = builder.bitcast(szh__dyj, zgviv__qnboi)
        builder.store(nci__yea._getvalue(), szh__dyj)
        return impl_ret_borrowed(context, builder, df_typ, ayit__dmg)
    sig = signature(df_typ, df_typ, c_ind_typ, arr_typ)
    return sig, codegen


@intrinsic
def set_df_index(typingctx, df_t, index_t=None):

    def codegen(context, builder, signature, args):
        zad__yorfp = args[0]
        index_val = args[1]
        df_typ = signature.args[0]
        bgpd__lkqov = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=zad__yorfp)
        ypo__htx = get_dataframe_payload(context, builder, df_typ, zad__yorfp)
        meuj__jzxdp = construct_dataframe(context, builder, signature.
            return_type, ypo__htx.data, index_val, ypo__htx.unboxed,
            bgpd__lkqov.parent)
        context.nrt.incref(builder, index_t, index_val)
        context.nrt.incref(builder, types.Tuple(df_t.data), ypo__htx.data)
        return meuj__jzxdp
    iwn__kxgh = DataFrameType(df_t.data, index_t, df_t.columns)
    sig = signature(iwn__kxgh, df_t, index_t)
    return sig, codegen


@intrinsic
def set_df_column_with_reflect(typingctx, df_type, cname_type, arr_type=None):
    assert is_literal_type(cname_type), 'constant column name expected'
    upeqb__aekae = get_literal_value(cname_type)
    yso__aiti = len(df_type.columns)
    ays__tmtn = yso__aiti
    gtwj__uyr = df_type.data
    yxh__jjuu = df_type.columns
    index_typ = df_type.index
    sdthn__aphna = upeqb__aekae not in df_type.columns
    wsdq__ntqmp = yso__aiti
    if sdthn__aphna:
        gtwj__uyr += arr_type,
        yxh__jjuu += upeqb__aekae,
        ays__tmtn += 1
    else:
        wsdq__ntqmp = df_type.columns.index(upeqb__aekae)
        gtwj__uyr = tuple(arr_type if i == wsdq__ntqmp else gtwj__uyr[i] for
            i in range(yso__aiti))

    def codegen(context, builder, signature, args):
        ayit__dmg, imlmh__cmyjk, yofz__rdufh = args
        vwet__vqh = get_dataframe_payload(context, builder, df_type, ayit__dmg)
        ypv__uleev = cgutils.create_struct_proxy(df_type)(context, builder,
            value=ayit__dmg)
        btnfw__kab = [(builder.extract_value(vwet__vqh.data, i) if i !=
            wsdq__ntqmp else yofz__rdufh) for i in range(yso__aiti)]
        if sdthn__aphna:
            btnfw__kab.append(yofz__rdufh)
        iqxle__fxohc = context.get_constant(types.int8, 0)
        tzl__hogea = context.get_constant(types.int8, 1)
        gys__mez = [(builder.extract_value(vwet__vqh.unboxed, i) if i !=
            wsdq__ntqmp else tzl__hogea) for i in range(yso__aiti)]
        if sdthn__aphna:
            gys__mez.append(tzl__hogea)
        gys__mez.append(iqxle__fxohc)
        index_val = vwet__vqh.index
        data_tup = context.make_tuple(builder, types.Tuple(gtwj__uyr),
            btnfw__kab)
        unboxed_tup = context.make_tuple(builder, types.UniTuple(types.int8,
            ays__tmtn + 1), gys__mez)
        mgdx__cyb = construct_dataframe(context, builder, signature.
            return_type, data_tup, index_val, unboxed_tup, ypv__uleev.parent)
        context.nrt.incref(builder, index_typ, index_val)
        for jdf__bly, gyd__tklu in zip(btnfw__kab, gtwj__uyr):
            context.nrt.incref(builder, gyd__tklu, jdf__bly)
        if not sdthn__aphna and arr_type == df_type.data[wsdq__ntqmp]:
            decref_df_data(context, builder, vwet__vqh, df_type)
            payload_type = DataFramePayloadType(df_type)
            szh__dyj = context.nrt.meminfo_data(builder, ypv__uleev.meminfo)
            zgviv__qnboi = context.get_value_type(payload_type).as_pointer()
            szh__dyj = builder.bitcast(szh__dyj, zgviv__qnboi)
            ttpfi__rwwi = get_dataframe_payload(context, builder, df_type,
                mgdx__cyb)
            builder.store(ttpfi__rwwi._getvalue(), szh__dyj)
            context.nrt.incref(builder, index_typ, index_val)
            for jdf__bly, gyd__tklu in zip(btnfw__kab, gtwj__uyr):
                context.nrt.incref(builder, gyd__tklu, jdf__bly)
        has_parent = cgutils.is_not_null(builder, ypv__uleev.parent)
        with builder.if_then(has_parent):
            tyr__rexx = context.get_python_api(builder)
            jtmd__vqv = tyr__rexx.gil_ensure()
            ciim__iijup = context.get_env_manager(builder)
            context.nrt.incref(builder, arr_type, yofz__rdufh)
            xcgcs__wgbld = numba.core.pythonapi._BoxContext(context,
                builder, tyr__rexx, ciim__iijup)
            wjd__cph = xcgcs__wgbld.pyapi.from_native_value(arr_type,
                yofz__rdufh, xcgcs__wgbld.env_manager)
            if isinstance(upeqb__aekae, str):
                ackaw__qslv = context.insert_const_string(builder.module,
                    upeqb__aekae)
                anodq__vji = tyr__rexx.string_from_string(ackaw__qslv)
            else:
                assert isinstance(upeqb__aekae, int)
                anodq__vji = tyr__rexx.long_from_longlong(context.
                    get_constant(types.intp, upeqb__aekae))
            tyr__rexx.object_setitem(ypv__uleev.parent, anodq__vji, wjd__cph)
            tyr__rexx.decref(wjd__cph)
            tyr__rexx.decref(anodq__vji)
            tyr__rexx.gil_release(jtmd__vqv)
        return mgdx__cyb
    iwn__kxgh = DataFrameType(gtwj__uyr, index_typ, yxh__jjuu)
    sig = signature(iwn__kxgh, df_type, cname_type, arr_type)
    return sig, codegen


@lower_constant(DataFrameType)
def lower_constant_dataframe(context, builder, df_type, pyval):
    yso__aiti = len(pyval.columns)
    data_tup = context.get_constant_generic(builder, types.Tuple(df_type.
        data), tuple(pyval.iloc[:, i].values for i in range(yso__aiti)))
    index_val = context.get_constant_generic(builder, df_type.index, pyval.
        index)
    tzl__hogea = context.get_constant(types.int8, 1)
    unboxed_tup = context.make_tuple(builder, types.UniTuple(types.int8, 
        yso__aiti + 1), [tzl__hogea] * (yso__aiti + 1))
    edwd__atpwv = construct_dataframe(context, builder, df_type, data_tup,
        index_val, unboxed_tup)
    return edwd__atpwv


@lower_cast(DataFrameType, DataFrameType)
def cast_df_to_df(context, builder, fromty, toty, val):
    if len(fromty.data) == len(toty.data) and isinstance(fromty.index,
        RangeIndexType) and isinstance(toty.index, NumericIndexType):
        nci__yea = get_dataframe_payload(context, builder, fromty, val)
        cay__zpdmj = context.cast(builder, nci__yea.index, fromty.index,
            toty.index)
        dsbds__sgr = nci__yea.data
        context.nrt.incref(builder, types.BaseTuple.from_types(fromty.data),
            dsbds__sgr)
        df = construct_dataframe(context, builder, toty, dsbds__sgr,
            cay__zpdmj, nci__yea.unboxed, nci__yea.parent)
        return df
    if (fromty.data == toty.data and fromty.index == toty.index and fromty.
        columns == toty.columns and fromty.dist != toty.dist):
        return val
    if not len(fromty.data) == 0:
        raise BodoError(f'Invalid dataframe cast from {fromty} to {toty}')
    ugtv__yrldi = {}
    if isinstance(toty.index, RangeIndexType):
        index = 'bodo.hiframes.pd_index_ext.init_range_index(0, 0, 1, None)'
    else:
        rzfj__zbghy = get_index_data_arr_types(toty.index)[0]
        ink__vcozm = bodo.utils.transform.get_type_alloc_counts(rzfj__zbghy
            ) - 1
        ysbz__anpa = ', '.join('0' for imlmh__cmyjk in range(ink__vcozm))
        index = (
            'bodo.utils.conversion.index_from_array(bodo.utils.utils.alloc_type(0, index_arr_type, ({}{})))'
            .format(ysbz__anpa, ', ' if ink__vcozm == 1 else ''))
        ugtv__yrldi['index_arr_type'] = rzfj__zbghy
    sxzlw__joi = []
    for i, arr_typ in enumerate(toty.data):
        ink__vcozm = bodo.utils.transform.get_type_alloc_counts(arr_typ) - 1
        ysbz__anpa = ', '.join('0' for imlmh__cmyjk in range(ink__vcozm))
        zly__uog = 'bodo.utils.utils.alloc_type(0, arr_type{}, ({}{}))'.format(
            i, ysbz__anpa, ', ' if ink__vcozm == 1 else '')
        sxzlw__joi.append(zly__uog)
        ugtv__yrldi[f'arr_type{i}'] = arr_typ
    sxzlw__joi = ', '.join(sxzlw__joi)
    sfl__aza = 'def impl():\n'
    nqz__tum = bodo.hiframes.dataframe_impl._gen_init_df(sfl__aza, toty.
        columns, sxzlw__joi, index, ugtv__yrldi)
    df = context.compile_internal(builder, nqz__tum, toty(), [])
    return df


@overload(pd.DataFrame, inline='always', no_unliteral=True)
def pd_dataframe_overload(data=None, index=None, columns=None, dtype=None,
    copy=False):
    if not is_overload_constant_bool(copy):
        raise BodoError(
            "pd.DataFrame(): 'copy' argument should be a constant boolean")
    copy = get_overload_const(copy)
    hdfs__zmqpv, sxzlw__joi, index_arg = _get_df_args(data, index, columns,
        dtype, copy)
    tvdnr__otgv = gen_const_tup(hdfs__zmqpv)
    sfl__aza = (
        'def _init_df(data=None, index=None, columns=None, dtype=None, copy=False):\n'
        )
    sfl__aza += (
        '  return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, {}, {})\n'
        .format(sxzlw__joi, index_arg, tvdnr__otgv))
    ozlqp__onkk = {}
    exec(sfl__aza, {'bodo': bodo, 'np': np}, ozlqp__onkk)
    qrwx__mmknf = ozlqp__onkk['_init_df']
    return qrwx__mmknf


def _get_df_args(data, index, columns, dtype, copy):
    karff__wuani = ''
    if not is_overload_none(dtype):
        karff__wuani = '.astype(dtype)'
    index_is_none = is_overload_none(index)
    index_arg = 'bodo.utils.conversion.convert_to_index(index)'
    if isinstance(data, types.BaseTuple):
        if not data.types[0] == types.StringLiteral('__bodo_tup'):
            raise BodoError('pd.DataFrame tuple input data not supported yet')
        assert len(data.types) % 2 == 1, 'invalid const dict tuple structure'
        yso__aiti = (len(data.types) - 1) // 2
        fpj__vzlrj = [byt__ylqs.literal_value for byt__ylqs in data.types[1
            :yso__aiti + 1]]
        data_val_types = dict(zip(fpj__vzlrj, data.types[yso__aiti + 1:]))
        btnfw__kab = ['data[{}]'.format(i) for i in range(yso__aiti + 1, 2 *
            yso__aiti + 1)]
        data_dict = dict(zip(fpj__vzlrj, btnfw__kab))
        if is_overload_none(index):
            for i, byt__ylqs in enumerate(data.types[yso__aiti + 1:]):
                if isinstance(byt__ylqs, SeriesType):
                    index_arg = (
                        'bodo.hiframes.pd_series_ext.get_series_index(data[{}])'
                        .format(yso__aiti + 1 + i))
                    index_is_none = False
                    break
    elif is_overload_none(data):
        data_dict = {}
        data_val_types = {}
    else:
        if not (isinstance(data, types.Array) and data.ndim == 2):
            raise BodoError(
                'pd.DataFrame() only supports constant dictionary and array input'
                )
        if is_overload_none(columns):
            raise BodoError(
                "pd.DataFrame() 'columns' argument is required when an array is passed as data"
                )
        dmcwg__ubq = '.copy()' if copy else ''
        rqq__dxw = get_overload_const_list(columns)
        yso__aiti = len(rqq__dxw)
        data_val_types = {xcgcs__wgbld: data.copy(ndim=1) for xcgcs__wgbld in
            rqq__dxw}
        btnfw__kab = ['data[:,{}]{}'.format(i, dmcwg__ubq) for i in range(
            yso__aiti)]
        data_dict = dict(zip(rqq__dxw, btnfw__kab))
    if is_overload_none(columns):
        col_names = data_dict.keys()
    else:
        col_names = get_overload_const_list(columns)
    df_len = _get_df_len_from_info(data_dict, data_val_types, col_names,
        index_is_none, index_arg)
    _fill_null_arrays(data_dict, col_names, df_len, dtype)
    if index_is_none:
        if is_overload_none(data):
            index_arg = (
                'bodo.hiframes.pd_index_ext.init_binary_str_index(bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0))'
                )
        else:
            index_arg = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, {}, 1, None)'
                .format(df_len))
    sxzlw__joi = '({},)'.format(', '.join(
        'bodo.utils.conversion.coerce_to_array({}, True, scalar_to_arr_len={}){}'
        .format(data_dict[xcgcs__wgbld], df_len, karff__wuani) for
        xcgcs__wgbld in col_names))
    if len(col_names) == 0:
        sxzlw__joi = '()'
    return col_names, sxzlw__joi, index_arg


def _get_df_len_from_info(data_dict, data_val_types, col_names,
    index_is_none, index_arg):
    df_len = '0'
    for xcgcs__wgbld in col_names:
        if xcgcs__wgbld in data_dict and is_iterable_type(data_val_types[
            xcgcs__wgbld]):
            df_len = 'len({})'.format(data_dict[xcgcs__wgbld])
            break
    if df_len == '0' and not index_is_none:
        df_len = f'len({index_arg})'
    return df_len


def _fill_null_arrays(data_dict, col_names, df_len, dtype):
    if all(xcgcs__wgbld in data_dict for xcgcs__wgbld in col_names):
        return
    if is_overload_none(dtype):
        dtype = 'bodo.string_array_type'
    else:
        dtype = 'bodo.utils.conversion.array_type_from_dtype(dtype)'
    ijpj__cpgq = 'bodo.libs.array_kernels.gen_na_array({}, {})'.format(df_len,
        dtype)
    for xcgcs__wgbld in col_names:
        if xcgcs__wgbld not in data_dict:
            data_dict[xcgcs__wgbld] = ijpj__cpgq


@overload(len)
def df_len_overload(df):
    if not isinstance(df, DataFrameType):
        return
    if len(df.columns) == 0:
        return lambda df: 0

    def impl(df):
        if is_null_pointer(df._meminfo):
            return 0
        return len(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, 0))
    return impl


@infer_global(operator.getitem)
class GetItemTuple(AbstractTemplate):
    key = operator.getitem

    def generic(self, args, kws):
        tup, idx = args
        if not isinstance(tup, types.BaseTuple) or not isinstance(idx,
            types.IntegerLiteral):
            return
        not__qwk = idx.literal_value
        if isinstance(not__qwk, int):
            hwc__bmoxw = tup.types[not__qwk]
        elif isinstance(not__qwk, slice):
            hwc__bmoxw = types.BaseTuple.from_types(tup.types[not__qwk])
        return signature(hwc__bmoxw, *args)


@lower_builtin(operator.getitem, types.BaseTuple, types.IntegerLiteral)
@lower_builtin(operator.getitem, types.BaseTuple, types.SliceLiteral)
def getitem_tuple_lower(context, builder, sig, args):
    qetag__bfzi, idx = sig.args
    idx = idx.literal_value
    tup, imlmh__cmyjk = args
    if isinstance(idx, int):
        if idx < 0:
            idx += len(qetag__bfzi)
        if not 0 <= idx < len(qetag__bfzi):
            raise IndexError('cannot index at %d in %s' % (idx, qetag__bfzi))
        kar__sjpo = builder.extract_value(tup, idx)
    elif isinstance(idx, slice):
        wiycg__ttyug = cgutils.unpack_tuple(builder, tup)[idx]
        kar__sjpo = context.make_tuple(builder, sig.return_type, wiycg__ttyug)
    else:
        raise NotImplementedError('unexpected index %r for %s' % (idx, sig.
            args[0]))
    return impl_ret_borrowed(context, builder, sig.return_type, kar__sjpo)


def join_dummy(left_df, right_df, left_on, right_on, how, suffix_x,
    suffix_y, is_join, indicator, _bodo_na_equal, gen_cond):
    return left_df


@infer_global(join_dummy)
class JoinTyper(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        from bodo.utils.typing import is_overload_str
        assert not kws
        (left_df, right_df, left_on, right_on, ocy__nme, suffix_x, suffix_y,
            is_join, indicator, _bodo_na_equal, xasam__ewku) = args
        left_on = get_overload_const_list(left_on)
        right_on = get_overload_const_list(right_on)
        pocmo__fiwe = set(left_on) & set(right_on)
        bcjot__cdb = set(left_df.columns) & set(right_df.columns)
        rfqw__rntbg = bcjot__cdb - pocmo__fiwe
        yizz__cbtlc = '$_bodo_index_' in left_on
        befe__lec = '$_bodo_index_' in right_on
        how = get_overload_const_str(ocy__nme)
        tdtkh__kkydm = how in {'left', 'outer'}
        lsb__wsqh = how in {'right', 'outer'}
        columns = []
        data = []
        if yizz__cbtlc and not befe__lec and not is_join.literal_value:
            iutm__lrdfj = right_on[0]
            if iutm__lrdfj in left_df.columns:
                columns.append(iutm__lrdfj)
                data.append(right_df.data[right_df.columns.index(iutm__lrdfj)])
        if befe__lec and not yizz__cbtlc and not is_join.literal_value:
            afoa__fruk = left_on[0]
            if afoa__fruk in right_df.columns:
                columns.append(afoa__fruk)
                data.append(left_df.data[left_df.columns.index(afoa__fruk)])
        for lkmi__erkll, kjg__pjc in zip(left_df.data, left_df.columns):
            columns.append(str(kjg__pjc) + suffix_x.literal_value if 
                kjg__pjc in rfqw__rntbg else kjg__pjc)
            if kjg__pjc in pocmo__fiwe:
                data.append(lkmi__erkll)
            else:
                data.append(to_nullable_type(lkmi__erkll) if lsb__wsqh else
                    lkmi__erkll)
        for lkmi__erkll, kjg__pjc in zip(right_df.data, right_df.columns):
            if kjg__pjc not in pocmo__fiwe:
                columns.append(str(kjg__pjc) + suffix_y.literal_value if 
                    kjg__pjc in rfqw__rntbg else kjg__pjc)
                data.append(to_nullable_type(lkmi__erkll) if tdtkh__kkydm else
                    lkmi__erkll)
        urkls__sybj = get_overload_const_bool(indicator)
        if urkls__sybj:
            columns.append('_merge')
            data.append(bodo.CategoricalArrayType(bodo.PDCategoricalDtype((
                'left_only', 'right_only', 'both'), bodo.string_type, False)))
        index_typ = RangeIndexType(types.none)
        if yizz__cbtlc and befe__lec and not is_overload_str(how, 'asof'):
            index_typ = left_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        elif yizz__cbtlc and not befe__lec:
            index_typ = right_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        elif befe__lec and not yizz__cbtlc:
            index_typ = left_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        ppgv__sbqq = DataFrameType(tuple(data), index_typ, tuple(columns))
        return signature(ppgv__sbqq, *args)


JoinTyper._no_unliteral = True


@lower_builtin(join_dummy, types.VarArg(types.Any))
def lower_join_dummy(context, builder, sig, args):
    meuj__jzxdp = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return meuj__jzxdp._getvalue()


@overload(pd.concat, inline='always', no_unliteral=True)
def concat_overload(objs, axis=0, join='outer', join_axes=None,
    ignore_index=False, keys=None, levels=None, names=None,
    verify_integrity=False, sort=None, copy=True):
    axis = get_overload_const_int(axis)
    ignore_index = is_overload_true(ignore_index)
    mxurk__qfc = dict(join=join, join_axes=join_axes, keys=keys, levels=
        levels, names=names, verify_integrity=verify_integrity, sort=sort,
        copy=copy)
    qvz__ssdqw = dict(join='outer', join_axes=None, keys=None, levels=None,
        names=None, verify_integrity=False, sort=None, copy=True)
    check_unsupported_args('pd.concat', mxurk__qfc, qvz__ssdqw)
    sfl__aza = """def impl(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True):
"""
    if axis == 1:
        if not isinstance(objs, types.BaseTuple):
            raise_bodo_error(
                'Only tuple argument for pd.concat(axis=1) expected')
        index = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(objs[0]), 1, None)'
            )
        rja__ywh = 0
        sxzlw__joi = []
        names = []
        for i, fscp__vizy in enumerate(objs.types):
            assert isinstance(fscp__vizy, (SeriesType, DataFrameType))
            if isinstance(fscp__vizy, SeriesType):
                names.append(str(rja__ywh))
                rja__ywh += 1
                sxzlw__joi.append(
                    'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'
                    .format(i))
            else:
                names.extend(fscp__vizy.columns)
                for gbm__rvxkw in range(len(fscp__vizy.data)):
                    sxzlw__joi.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, gbm__rvxkw))
        return bodo.hiframes.dataframe_impl._gen_init_df(sfl__aza, names,
            ', '.join(sxzlw__joi), index)
    assert axis == 0
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        DataFrameType):
        assert all(isinstance(byt__ylqs, DataFrameType) for byt__ylqs in
            objs.types)
        ozy__alu = []
        for df in objs.types:
            ozy__alu.extend(df.columns)
        ozy__alu = list(dict.fromkeys(ozy__alu).keys())
        qzej__nnpdk = {}
        for rja__ywh, xcgcs__wgbld in enumerate(ozy__alu):
            for df in objs.types:
                if xcgcs__wgbld in df.columns:
                    qzej__nnpdk['arr_typ{}'.format(rja__ywh)] = df.data[df.
                        columns.index(xcgcs__wgbld)]
                    break
        assert len(qzej__nnpdk) == len(ozy__alu)
        hzy__vrxyt = []
        for rja__ywh, xcgcs__wgbld in enumerate(ozy__alu):
            args = []
            for i, df in enumerate(objs.types):
                if xcgcs__wgbld in df.columns:
                    wsdq__ntqmp = df.columns.index(xcgcs__wgbld)
                    args.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, wsdq__ntqmp))
                else:
                    args.append(
                        'bodo.libs.array_kernels.gen_na_array(len(objs[{}]), arr_typ{})'
                        .format(i, rja__ywh))
            sfl__aza += ('  A{} = bodo.libs.array_kernels.concat(({},))\n'.
                format(rja__ywh, ', '.join(args)))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(A0), 1, None)'
                )
        else:
            index = (
                """bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)) if len(objs[i].
                columns) > 0)))
        return bodo.hiframes.dataframe_impl._gen_init_df(sfl__aza, ozy__alu,
            ', '.join('A{}'.format(i) for i in range(len(ozy__alu))), index,
            qzej__nnpdk)
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        SeriesType):
        assert all(isinstance(byt__ylqs, SeriesType) for byt__ylqs in objs.
            types)
        sfl__aza += ('  out_arr = bodo.libs.array_kernels.concat(({},))\n'.
            format(', '.join(
            'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'.format(
            i) for i in range(len(objs.types)))))
        if ignore_index:
            sfl__aza += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            sfl__aza += (
                """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)))))
        sfl__aza += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        ozlqp__onkk = {}
        exec(sfl__aza, {'bodo': bodo, 'np': np, 'numba': numba}, ozlqp__onkk)
        return ozlqp__onkk['impl']
    if isinstance(objs, types.List) and isinstance(objs.dtype, DataFrameType):
        df_type = objs.dtype
        for rja__ywh, xcgcs__wgbld in enumerate(df_type.columns):
            sfl__aza += '  arrs{} = []\n'.format(rja__ywh)
            sfl__aza += '  for i in range(len(objs)):\n'
            sfl__aza += '    df = objs[i]\n'
            sfl__aza += (
                """    arrs{0}.append(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0}))
"""
                .format(rja__ywh))
            sfl__aza += (
                '  out_arr{0} = bodo.libs.array_kernels.concat(arrs{0})\n'.
                format(rja__ywh))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr0), 1, None)'
                )
        else:
            sfl__aza += '  arrs_index = []\n'
            sfl__aza += '  for i in range(len(objs)):\n'
            sfl__aza += '    df = objs[i]\n'
            sfl__aza += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
            index = """bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index))
"""
        return bodo.hiframes.dataframe_impl._gen_init_df(sfl__aza, df_type.
            columns, ', '.join('out_arr{}'.format(i) for i in range(len(
            df_type.columns))), index)
    if isinstance(objs, types.List) and isinstance(objs.dtype, SeriesType):
        sfl__aza += '  arrs = []\n'
        sfl__aza += '  for i in range(len(objs)):\n'
        sfl__aza += (
            '    arrs.append(bodo.hiframes.pd_series_ext.get_series_data(objs[i]))\n'
            )
        sfl__aza += '  out_arr = bodo.libs.array_kernels.concat(arrs)\n'
        if ignore_index:
            sfl__aza += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            sfl__aza += '  arrs_index = []\n'
            sfl__aza += '  for i in range(len(objs)):\n'
            sfl__aza += '    S = objs[i]\n'
            sfl__aza += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S)))
"""
            sfl__aza += """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index))
"""
        sfl__aza += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        ozlqp__onkk = {}
        exec(sfl__aza, {'bodo': bodo, 'np': np, 'numba': numba}, ozlqp__onkk)
        return ozlqp__onkk['impl']
    raise BodoError('pd.concat(): input type {} not supported yet'.format(objs)
        )


def sort_values_dummy(df, by, ascending, inplace, na_position):
    return df.sort_values(by, ascending=ascending, inplace=inplace,
        na_position=na_position)


@infer_global(sort_values_dummy)
class SortDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df, by, ascending, inplace, na_position = args
        index = df.index
        if isinstance(index, bodo.hiframes.pd_index_ext.RangeIndexType):
            index = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64)
        iwn__kxgh = df.copy(index=index)
        return signature(iwn__kxgh, *args)


SortDummyTyper._no_unliteral = True


@lower_builtin(sort_values_dummy, types.VarArg(types.Any))
def lower_sort_values_dummy(context, builder, sig, args):
    if sig.return_type == types.none:
        return
    nhcys__dktq = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return nhcys__dktq._getvalue()


def set_parent_dummy(df):
    return df


@infer_global(set_parent_dummy)
class ParentDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df, = args
        hwc__bmoxw = DataFrameType(df.data, df.index, df.columns)
        return signature(hwc__bmoxw, *args)


@lower_builtin(set_parent_dummy, types.VarArg(types.Any))
def lower_set_parent_dummy(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@overload_method(DataFrameType, 'itertuples', inline='always', no_unliteral
    =True)
def itertuples_overload(df, index=True, name='Pandas'):
    mxurk__qfc = dict(index=index, name=name)
    qvz__ssdqw = dict(index=True, name='Pandas')
    check_unsupported_args('DataFrame.itertuples', mxurk__qfc, qvz__ssdqw)

    def _impl(df, index=True, name='Pandas'):
        return bodo.hiframes.pd_dataframe_ext.itertuples_dummy(df)
    return _impl


def itertuples_dummy(df):
    return df


@infer_global(itertuples_dummy)
class ItertuplesDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df, = args
        assert 'Index' not in df.columns
        columns = ('Index',) + df.columns
        qzej__nnpdk = (types.Array(types.int64, 1, 'C'),) + df.data
        xndtt__jlfv = bodo.hiframes.dataframe_impl.DataFrameTupleIterator(
            columns, qzej__nnpdk)
        return signature(xndtt__jlfv, *args)


@lower_builtin(itertuples_dummy, types.VarArg(types.Any))
def lower_itertuples_dummy(context, builder, sig, args):
    nhcys__dktq = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return nhcys__dktq._getvalue()


def query_dummy(df, expr):
    return df.eval(expr)


@infer_global(query_dummy)
class QueryDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(SeriesType(types.bool_, index=RangeIndexType(types
            .none)), *args)


@lower_builtin(query_dummy, types.VarArg(types.Any))
def lower_query_dummy(context, builder, sig, args):
    nhcys__dktq = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return nhcys__dktq._getvalue()


def val_isin_dummy(S, vals):
    return S in vals


def val_notin_dummy(S, vals):
    return S not in vals


@infer_global(val_isin_dummy)
@infer_global(val_notin_dummy)
class ValIsinTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(SeriesType(types.bool_, index=args[0].index), *args)


@lower_builtin(val_isin_dummy, types.VarArg(types.Any))
@lower_builtin(val_notin_dummy, types.VarArg(types.Any))
def lower_val_isin_dummy(context, builder, sig, args):
    nhcys__dktq = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return nhcys__dktq._getvalue()


def gen_pandas_parquet_metadata(df, write_non_range_index_to_metadata,
    write_rangeindex_to_metadata, partition_cols=None):
    dscc__zvc = {}
    dscc__zvc['columns'] = []
    if partition_cols is None:
        partition_cols = []
    for upeqb__aekae, tph__hjnp in zip(df.columns, df.data):
        if upeqb__aekae in partition_cols:
            continue
        if isinstance(tph__hjnp, types.Array) or tph__hjnp == boolean_array:
            wtn__asi = rud__kvyh = tph__hjnp.dtype.name
            if rud__kvyh.startswith('datetime'):
                wtn__asi = 'datetime'
        elif tph__hjnp == string_array_type:
            wtn__asi = 'unicode'
            rud__kvyh = 'object'
        elif tph__hjnp == binary_array_type:
            wtn__asi = 'bytes'
            rud__kvyh = 'object'
        elif isinstance(tph__hjnp, DecimalArrayType):
            wtn__asi = rud__kvyh = 'object'
        elif isinstance(tph__hjnp, IntegerArrayType):
            qtcq__mnt = tph__hjnp.dtype.name
            if qtcq__mnt.startswith('int'):
                wtn__asi = 'Int' + qtcq__mnt[3:]
            elif qtcq__mnt.startswith('uint'):
                wtn__asi = 'UInt' + qtcq__mnt[4:]
            else:
                raise BodoError(
                    'to_parquet(): unknown dtype in nullable Integer column {} {}'
                    .format(upeqb__aekae, tph__hjnp))
            rud__kvyh = tph__hjnp.dtype.name
        elif tph__hjnp == datetime_date_array_type:
            wtn__asi = 'datetime'
            rud__kvyh = 'object'
        elif isinstance(tph__hjnp, (StructArrayType, ArrayItemArrayType)):
            wtn__asi = 'object'
            rud__kvyh = 'object'
        else:
            raise BodoError(
                'to_parquet(): unsupported column type for metadata generation : {} {}'
                .format(upeqb__aekae, tph__hjnp))
        ebzvd__ovtu = {'name': upeqb__aekae, 'field_name': upeqb__aekae,
            'pandas_type': wtn__asi, 'numpy_type': rud__kvyh, 'metadata': None}
        dscc__zvc['columns'].append(ebzvd__ovtu)
    if write_non_range_index_to_metadata:
        if 'none' in df.index.name:
            ozj__szw = '__index_level_0__'
            pnb__emw = None
        else:
            ozj__szw = '%s'
            pnb__emw = '%s'
        dscc__zvc['index_columns'] = [ozj__szw]
        dscc__zvc['columns'].append({'name': pnb__emw, 'field_name':
            ozj__szw, 'pandas_type': df.index.pandas_type_name,
            'numpy_type': df.index.numpy_type_name, 'metadata': None})
    elif write_rangeindex_to_metadata:
        dscc__zvc['index_columns'] = [{'kind': 'range', 'name': '%s',
            'start': '%d', 'stop': '%d', 'step': '%d'}]
    else:
        dscc__zvc['index_columns'] = []
    dscc__zvc['pandas_version'] = pd.__version__
    return dscc__zvc


@overload_method(DataFrameType, 'to_parquet', no_unliteral=True)
def to_parquet_overload(df, fname, engine='auto', compression='snappy',
    index=None, partition_cols=None, _is_parallel=False):
    if not is_overload_none(engine) and get_overload_const_str(engine) not in (
        'auto', 'pyarrow'):
        raise BodoError('DataFrame.to_parquet(): only pyarrow engine supported'
            )
    if not is_overload_none(compression) and get_overload_const_str(compression
        ) not in {'snappy', 'gzip', 'brotli'}:
        raise BodoError('to_parquet(): Unsupported compression: ' + str(
            get_overload_const_str(compression)))
    if not is_overload_none(partition_cols):
        partition_cols = get_overload_const_list(partition_cols)
        mkjle__xbb = []
        for cuq__cptq in partition_cols:
            try:
                idx = df.columns.index(cuq__cptq)
            except ValueError as fphqc__dtlhs:
                raise BodoError(
                    f'Partition column {cuq__cptq} is not in dataframe')
            mkjle__xbb.append(idx)
    else:
        partition_cols = None
    if not is_overload_none(index) and not is_overload_constant_bool(index):
        raise BodoError('to_parquet(): index must be a constant bool or None')
    from bodo.io.parquet_pio import parquet_write_table_cpp, parquet_write_table_partitioned_cpp
    gqox__bcryv = isinstance(df.index, bodo.hiframes.pd_index_ext.
        RangeIndexType)
    iqpmu__rhwr = df.index is not None and (is_overload_true(_is_parallel) or
        not is_overload_true(_is_parallel) and not gqox__bcryv)
    write_non_range_index_to_metadata = is_overload_true(index
        ) or is_overload_none(index) and (not gqox__bcryv or
        is_overload_true(_is_parallel))
    write_rangeindex_to_metadata = is_overload_none(index
        ) and gqox__bcryv and not is_overload_true(_is_parallel)
    lqlw__vqyo = json.dumps(gen_pandas_parquet_metadata(df,
        write_non_range_index_to_metadata, write_rangeindex_to_metadata,
        partition_cols=partition_cols))
    if not is_overload_true(_is_parallel) and gqox__bcryv:
        lqlw__vqyo = lqlw__vqyo.replace('"%d"', '%d')
        if df.index.name == 'RangeIndexType(none)':
            lqlw__vqyo = lqlw__vqyo.replace('"%s"', '%s')
    sxzlw__joi = ', '.join(
        'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
        .format(i) for i in range(len(df.columns)))
    bmrva__lrho = ', '.join('"{}"'.format(upeqb__aekae) for upeqb__aekae in
        df.columns)
    sfl__aza = """def df_to_parquet(df, fname, engine='auto', compression='snappy', index=None, partition_cols=None, _is_parallel=False):
"""
    sfl__aza += '    info_list = [{}]\n'.format(sxzlw__joi)
    sfl__aza += '    table = arr_info_list_to_table(info_list)\n'
    sfl__aza += ('    col_names = array_to_info(str_arr_from_sequence([{}]))\n'
        .format(bmrva__lrho))
    if is_overload_true(index) or is_overload_none(index) and iqpmu__rhwr:
        sfl__aza += """    index_col = array_to_info(index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
        jpi__tgtmi = True
    else:
        sfl__aza += '    index_col = array_to_info(np.empty(0))\n'
        jpi__tgtmi = False
    sfl__aza += '    metadata = """' + lqlw__vqyo + '"""\n'
    sfl__aza += '    if compression is None:\n'
    sfl__aza += "        compression = 'none'\n"
    sfl__aza += '    if df.index.name is not None:\n'
    sfl__aza += '        name_ptr = df.index.name\n'
    sfl__aza += '    else:\n'
    sfl__aza += "        name_ptr = 'null'\n"
    sfl__aza += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel=_is_parallel)
"""
    if partition_cols:
        kkk__jbja = ', '.join(
            f'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype.categories.values)'
             for i in range(len(df.columns)) if isinstance(df.data[i],
            CategoricalArrayType) and i in mkjle__xbb)
        if kkk__jbja:
            sfl__aza += '    cat_info_list = [{}]\n'.format(kkk__jbja)
            sfl__aza += (
                '    cat_table = arr_info_list_to_table(cat_info_list)\n')
        else:
            sfl__aza += '    cat_table = table\n'
        tkl__jwxg = ', '.join('"{}"'.format(upeqb__aekae) for upeqb__aekae in
            df.columns if upeqb__aekae not in partition_cols)
        sfl__aza += (
            '    col_names_no_partitions = array_to_info(str_arr_from_sequence([{}]))\n'
            .format(tkl__jwxg))
        sfl__aza += (
            f'    part_cols_idxs = np.array({mkjle__xbb}, dtype=np.int32)\n')
        sfl__aza += (
            '    parquet_write_table_partitioned_cpp(unicode_to_utf8(fname),\n'
            )
        sfl__aza += """                            table, col_names, col_names_no_partitions, cat_table,
"""
        sfl__aza += (
            '                            part_cols_idxs.ctypes, len(part_cols_idxs),\n'
            )
        sfl__aza += (
            '                            unicode_to_utf8(compression),\n')
        sfl__aza += '                            _is_parallel,\n'
        sfl__aza += (
            '                            unicode_to_utf8(bucket_region))\n')
    elif write_rangeindex_to_metadata:
        sfl__aza += '    parquet_write_table_cpp(unicode_to_utf8(fname),\n'
        sfl__aza += (
            '                            table, col_names, index_col,\n')
        sfl__aza += '                            ' + str(jpi__tgtmi) + ',\n'
        sfl__aza += '                            unicode_to_utf8(metadata),\n'
        sfl__aza += (
            '                            unicode_to_utf8(compression),\n')
        sfl__aza += (
            '                            _is_parallel, 1, df.index.start,\n')
        sfl__aza += (
            '                            df.index.stop, df.index.step,\n')
        sfl__aza += '                            unicode_to_utf8(name_ptr),\n'
        sfl__aza += (
            '                            unicode_to_utf8(bucket_region))\n')
    else:
        sfl__aza += '    parquet_write_table_cpp(unicode_to_utf8(fname),\n'
        sfl__aza += (
            '                            table, col_names, index_col,\n')
        sfl__aza += '                            ' + str(jpi__tgtmi) + ',\n'
        sfl__aza += '                            unicode_to_utf8(metadata),\n'
        sfl__aza += (
            '                            unicode_to_utf8(compression),\n')
        sfl__aza += '                            _is_parallel, 0, 0, 0, 0,\n'
        sfl__aza += '                            unicode_to_utf8(name_ptr),\n'
        sfl__aza += (
            '                            unicode_to_utf8(bucket_region))\n')
    ozlqp__onkk = {}
    exec(sfl__aza, {'np': np, 'bodo': bodo, 'unicode_to_utf8':
        unicode_to_utf8, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'str_arr_from_sequence': str_arr_from_sequence,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'parquet_write_table_partitioned_cpp':
        parquet_write_table_partitioned_cpp, 'index_to_array':
        index_to_array}, ozlqp__onkk)
    cpar__jxlr = ozlqp__onkk['df_to_parquet']
    return cpar__jxlr


def to_sql_exception_guard(df, name, con, schema=None, if_exists='fail',
    index=True, index_label=None, chunksize=None, dtype=None, method=None):
    wzm__uqu = 'all_ok'
    try:
        df.to_sql(name, con, schema, if_exists, index, index_label,
            chunksize, dtype, method)
    except ValueError as ror__rmbhq:
        wzm__uqu = ror__rmbhq.args[0]
    return wzm__uqu


@numba.njit
def to_sql_exception_guard_encaps(df, name, con, schema=None, if_exists=
    'fail', index=True, index_label=None, chunksize=None, dtype=None,
    method=None):
    with numba.objmode(out='unicode_type'):
        out = to_sql_exception_guard(df, name, con, schema, if_exists,
            index, index_label, chunksize, dtype, method)
    return out


@overload_method(DataFrameType, 'to_sql')
def to_sql_overload(df, name, con, schema=None, if_exists='fail', index=
    True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_parallel=False):
    mxurk__qfc = dict(chunksize=chunksize)
    qvz__ssdqw = dict(chunksize=None)
    check_unsupported_args('to_sql', mxurk__qfc, qvz__ssdqw)

    def _impl(df, name, con, schema=None, if_exists='fail', index=True,
        index_label=None, chunksize=None, dtype=None, method=None,
        _is_parallel=False):
        bjz__kpzy = bodo.libs.distributed_api.get_rank()
        wzm__uqu = 'unset'
        if bjz__kpzy != 0:
            if_exists = 'append'
            wzm__uqu = bcast_scalar(wzm__uqu)
        if bjz__kpzy == 0 or _is_parallel and wzm__uqu == 'all_ok':
            wzm__uqu = to_sql_exception_guard_encaps(df, name, con, schema,
                if_exists, index, index_label, chunksize, dtype, method)
        if bjz__kpzy == 0:
            wzm__uqu = bcast_scalar(wzm__uqu)
        if wzm__uqu != 'all_ok':
            print('err_msg=', wzm__uqu)
            raise ValueError('error in to_sql() operation')
    return _impl


@overload_method(DataFrameType, 'to_csv', no_unliteral=True)
def to_csv_overload(df, path_or_buf=None, sep=',', na_rep='', float_format=
    None, columns=None, header=True, index=True, index_label=None, mode='w',
    encoding=None, compression=None, quoting=None, quotechar='"',
    line_terminator=None, chunksize=None, date_format=None, doublequote=
    True, escapechar=None, decimal='.', errors='strict', storage_options=None):
    check_unsupported_args('DataFrame.to_csv', {'encoding': encoding,
        'mode': mode, 'errors': errors, 'storage_options': storage_options},
        {'encoding': None, 'mode': 'w', 'errors': 'strict',
        'storage_options': None})
    if not (is_overload_none(path_or_buf) or is_overload_constant_str(
        path_or_buf) or path_or_buf == string_type):
        raise BodoError(
            "DataFrame.to_csv(): 'path_or_buf' argument should be None or string"
            )
    if not is_overload_none(compression):
        raise BodoError(
            "DataFrame.to_csv(): 'compression' argument supports only None, which is the default in JIT code."
            )
    if is_overload_constant_str(path_or_buf):
        ttdex__geyxx = get_overload_const_str(path_or_buf)
        if ttdex__geyxx.endswith(('.gz', '.bz2', '.zip', '.xz')):
            import warnings
            from bodo.utils.typing import BodoWarning
            warnings.warn(BodoWarning(
                "DataFrame.to_csv(): 'compression' argument defaults to None in JIT code, which is the only supported value."
                ))
    if isinstance(columns, types.List):
        raise BodoError(
            "DataFrame.to_csv(): 'columns' argument must not be list type. Please convert to tuple type."
            )
    if is_overload_none(path_or_buf):

        def _impl(df, path_or_buf=None, sep=',', na_rep='', float_format=
            None, columns=None, header=True, index=True, index_label=None,
            mode='w', encoding=None, compression=None, quoting=None,
            quotechar='"', line_terminator=None, chunksize=None,
            date_format=None, doublequote=True, escapechar=None, decimal=
            '.', errors='strict', storage_options=None):
            with numba.objmode(D='unicode_type'):
                D = df.to_csv(path_or_buf, sep, na_rep, float_format,
                    columns, header, index, index_label, mode, encoding,
                    compression, quoting, quotechar, line_terminator,
                    chunksize, date_format, doublequote, escapechar,
                    decimal, errors, storage_options)
            return D
        return _impl

    def _impl(df, path_or_buf=None, sep=',', na_rep='', float_format=None,
        columns=None, header=True, index=True, index_label=None, mode='w',
        encoding=None, compression=None, quoting=None, quotechar='"',
        line_terminator=None, chunksize=None, date_format=None, doublequote
        =True, escapechar=None, decimal='.', errors='strict',
        storage_options=None):
        with numba.objmode(D='unicode_type'):
            D = df.to_csv(None, sep, na_rep, float_format, columns, header,
                index, index_label, mode, encoding, compression, quoting,
                quotechar, line_terminator, chunksize, date_format,
                doublequote, escapechar, decimal, errors, storage_options)
        bodo.io.fs_io.csv_write(path_or_buf, D)
    return _impl


@overload_method(DataFrameType, 'to_json', no_unliteral=True)
def to_json_overload(df, path_or_buf=None, orient='columns', date_format=
    None, double_precision=10, force_ascii=True, date_unit='ms',
    default_handler=None, lines=False, compression='infer', index=True,
    indent=None):
    if path_or_buf is None or path_or_buf == types.none:

        def _impl(df, path_or_buf=None, orient='columns', date_format=None,
            double_precision=10, force_ascii=True, date_unit='ms',
            default_handler=None, lines=False, compression='infer', index=
            True, indent=None):
            with numba.objmode(D='unicode_type'):
                D = df.to_json(path_or_buf, orient, date_format,
                    double_precision, force_ascii, date_unit,
                    default_handler, lines, compression, index, indent)
            return D
        return _impl

    def _impl(df, path_or_buf=None, orient='columns', date_format=None,
        double_precision=10, force_ascii=True, date_unit='ms',
        default_handler=None, lines=False, compression='infer', index=True,
        indent=None):
        with numba.objmode(D='unicode_type'):
            D = df.to_json(None, orient, date_format, double_precision,
                force_ascii, date_unit, default_handler, lines, compression,
                index, indent)
        bkj__vcc = bodo.io.fs_io.get_s3_bucket_region_njit(path_or_buf,
            parallel=False)
        if lines and orient == 'records':
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, True,
                unicode_to_utf8(bkj__vcc))
            bodo.utils.utils.check_and_propagate_cpp_exception()
        else:
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, False,
                unicode_to_utf8(bkj__vcc))
            bodo.utils.utils.check_and_propagate_cpp_exception()
    return _impl


@overload(pd.get_dummies, inline='always', no_unliteral=True)
def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=
    None, sparse=False, drop_first=False, dtype=None):
    fkxao__sugi = {'prefix': prefix, 'prefix_sep': prefix_sep, 'dummy_na':
        dummy_na, 'columns': columns, 'sparse': sparse, 'drop_first':
        drop_first, 'dtype': dtype}
    vnr__oalmb = {'prefix': None, 'prefix_sep': '_', 'dummy_na': False,
        'columns': None, 'sparse': False, 'drop_first': False, 'dtype': None}
    check_unsupported_args('pd.get_dummies', fkxao__sugi, vnr__oalmb)
    if not categorical_can_construct_dataframe(data):
        raise BodoError(
            'pd.get_dummies() only support categorical data types with explicitly known categories'
            )
    sfl__aza = """def impl(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None,):
"""
    if isinstance(data, SeriesType):
        nymyv__vhu = data.data.dtype.categories
        sfl__aza += (
            '  data_values = bodo.hiframes.pd_series_ext.get_series_data(data)\n'
            )
    else:
        nymyv__vhu = data.dtype.categories
        sfl__aza += '  data_values = data\n'
    yso__aiti = len(nymyv__vhu)
    sfl__aza += """  codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(data_values)
"""
    sfl__aza += '  numba.parfors.parfor.init_prange()\n'
    sfl__aza += '  n = len(data_values)\n'
    for i in range(yso__aiti):
        sfl__aza += '  data_arr_{} = np.empty(n, np.uint8)\n'.format(i)
    sfl__aza += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    sfl__aza += '      if bodo.libs.array_kernels.isna(data_values, i):\n'
    for gbm__rvxkw in range(yso__aiti):
        sfl__aza += '          data_arr_{}[i] = 0\n'.format(gbm__rvxkw)
    sfl__aza += '      else:\n'
    for muaj__thbkl in range(yso__aiti):
        sfl__aza += '          data_arr_{0}[i] = codes[i] == {0}\n'.format(
            muaj__thbkl)
    sxzlw__joi = ', '.join(f'data_arr_{i}' for i in range(yso__aiti))
    index = 'bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)'
    return bodo.hiframes.dataframe_impl._gen_init_df(sfl__aza, nymyv__vhu,
        sxzlw__joi, index)


def categorical_can_construct_dataframe(val):
    if isinstance(val, CategoricalArrayType):
        return val.dtype.categories is not None
    elif isinstance(val, SeriesType) and isinstance(val.data,
        CategoricalArrayType):
        return val.data.dtype.categories is not None
    return False


def handle_inplace_df_type_change(inplace, _bodo_transformed, func_name):
    if is_overload_false(_bodo_transformed
        ) and bodo.transforms.typing_pass.in_partial_typing and (
        is_overload_true(inplace) or not is_overload_constant_bool(inplace)):
        bodo.transforms.typing_pass.typing_transform_required = True
        raise Exception('DataFrame.{}(): transform necessary for inplace'.
            format(func_name))


pd_unsupported = (pd.read_pickle, pd.read_table, pd.read_fwf, pd.
    read_clipboard, pd.ExcelWriter, pd.json_normalize, pd.read_html, pd.
    read_hdf, pd.read_feather, pd.read_orc, pd.read_sas, pd.read_spss, pd.
    read_sql_table, pd.read_sql_query, pd.read_gbq, pd.read_stata, pd.melt,
    pd.pivot, pd.merge_ordered, pd.factorize, pd.wide_to_long, pd.
    bdate_range, pd.period_range, pd.infer_freq, pd.interval_range, pd.eval,
    pd.util.hash_array, pd.util.hash_pandas_object, pd.test)
dataframe_unsupported = {'to_latex', 'from_dict', 'reindex_like', 'pivot',
    'clip', 'slice_shift', 'tz_convert', 'combine', 'convert_dtypes',
    'floordiv', 'eval', 'applymap', 'nlargest', 'to_markdown', 'rmul',
    'pad', 'sparse', 'combine_first', 'kurt', 'at_time', 'mad', 'mask',
    'to_html', 'unstack', 'iteritems', 'between_time', 'mod', 'to_gbq',
    'rank', 'round', 'mode', 'multiply', 'value_counts', 'corrwith',
    'set_axis', 'nsmallest', 'to_dict', 'to_feather', 'cummax', 'to_stata',
    'ne', 'ewm', 'first', 'expanding', 'droplevel', 'truncate', 'asof',
    'pow', 'reorder_levels', 'mul', 'last', 'agg', 'le', 'any', 'xs',
    'explode', 'equals', 'asfreq', 'pop', 'iterrows', 'rename_axis',
    'resample', 'to_xarray', 'items', 'radd', 'tshift', 'rsub', 'align',
    'add', 'squeeze', 'swapaxes', 'to_pickle', 'to_timestamp',
    'interpolate', 'eq', 'bool', 'skew', 'rdiv', 'div', 'sem',
    'tz_localize', 'lt', 'bfill', 'last_valid_index', 'to_records', 'keys',
    'to_clipboard', 'transform', 'dot', 'truediv', 'gt', 'add_prefix',
    'divide', 'lookup', 'infer_objects', 'melt', 'rmod', 'aggregate',
    'from_records', 'rpow', 'to_excel', 'subtract', 'rfloordiv', 'ffill',
    'to_hdf', 'update', 'sub', 'hist', 'ge', 'get', 'all', 'plot',
    'backfill', 'stack', 'where', 'transpose', 'T', 'rtruediv', 'cummin',
    'swaplevel', 'first_valid_index', 'compare', 'boxplot', 'to_period',
    'add_suffix', 'kurtosis', 'reindex', 'at', '__iter__'}
dataframe_unsupported_attrs = 'axes', 'at', 'attrs'


def _install_pd_unsupported():
    for xnnw__uuoxi in pd_unsupported:
        fname = 'pd.' + xnnw__uuoxi.__name__
        overload(xnnw__uuoxi, no_unliteral=True)(create_unsupported_overload
            (fname))


def _install_dataframe_unsupported():
    for lqll__bvlai in dataframe_unsupported_attrs:
        bvf__brw = 'DataFrame.' + lqll__bvlai
        overload_attribute(DataFrameType, lqll__bvlai)(
            create_unsupported_overload(bvf__brw))
    for fname in dataframe_unsupported:
        bvf__brw = 'Dataframe.' + fname
        overload_method(DataFrameType, fname)(create_unsupported_overload(
            bvf__brw))


_install_pd_unsupported()
_install_dataframe_unsupported()
