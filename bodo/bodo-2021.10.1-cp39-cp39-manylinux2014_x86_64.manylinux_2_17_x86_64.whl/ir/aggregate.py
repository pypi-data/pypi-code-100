"""IR node for the groupby, pivot and cross_tabulation"""
import ctypes
import operator
import types as pytypes
from collections import defaultdict, namedtuple
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, compiler, ir, ir_utils, types
from numba.core.analysis import compute_use_defs
from numba.core.ir_utils import build_definitions, compile_to_numba_ir, find_callname, find_const, find_topo_order, get_definition, get_ir_of_code, get_name_var_table, guard, is_getitem, mk_unique_var, next_label, remove_dels, replace_arg_nodes, replace_var_names, replace_vars_inner, visit_vars_inner
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, lower_builtin, overload
from numba.parfors.parfor import Parfor, unwrap_parfor_blocks, wrap_parfor_blocks
import bodo
from bodo.hiframes.datetime_date_ext import DatetimeDateArrayType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.libs.array import arr_info_list_to_table, array_to_info, compute_node_partition_by_hash, delete_info_decref_array, delete_table, delete_table_decref_arrays, groupby_and_aggregate, info_from_table, info_to_array, pivot_groupby_and_aggregate
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, pre_alloc_array_item_array
from bodo.libs.binary_arr_ext import BinaryArrayType, pre_alloc_binary_array
from bodo.libs.bool_arr_ext import BooleanArrayType
from bodo.libs.decimal_arr_ext import DecimalArrayType, alloc_decimal_array
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.utils.transform import get_call_expr_arg
from bodo.utils.typing import BodoError, get_literal_value, get_overload_const_func, get_overload_const_str, get_overload_constant_dict, is_overload_constant_dict, is_overload_constant_str, list_cumulative
from bodo.utils.utils import debug_prints, incref, is_assign, is_call_assign, is_expr, is_null_pointer, is_var_assign, sanitize_varname, unliteral_all
gb_agg_cfunc = {}
gb_agg_cfunc_addr = {}


@intrinsic
def add_agg_cfunc_sym(typingctx, func, sym):

    def codegen(context, builder, signature, args):
        sig = func.signature
        if sig == types.none(types.voidptr):
            snc__sov = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer()])
            qjhj__ruj = cgutils.get_or_insert_function(builder.module,
                snc__sov, sym._literal_value)
            builder.call(qjhj__ruj, [context.get_constant_null(sig.args[0])])
        elif sig == types.none(types.int64, types.voidptr, types.voidptr):
            snc__sov = lir.FunctionType(lir.VoidType(), [lir.IntType(64),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
            qjhj__ruj = cgutils.get_or_insert_function(builder.module,
                snc__sov, sym._literal_value)
            builder.call(qjhj__ruj, [context.get_constant(types.int64, 0),
                context.get_constant_null(sig.args[1]), context.
                get_constant_null(sig.args[2])])
        else:
            snc__sov = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64).
                as_pointer()])
            qjhj__ruj = cgutils.get_or_insert_function(builder.module,
                snc__sov, sym._literal_value)
            builder.call(qjhj__ruj, [context.get_constant_null(sig.args[0]),
                context.get_constant_null(sig.args[1]), context.
                get_constant_null(sig.args[2])])
        context.add_linking_libs([gb_agg_cfunc[sym._literal_value]._library])
        return
    return types.none(func, sym), codegen


@numba.jit
def get_agg_udf_addr(name):
    with numba.objmode(addr='int64'):
        addr = gb_agg_cfunc_addr[name]
    return addr


class AggUDFStruct(object):

    def __init__(self, regular_udf_funcs=None, general_udf_funcs=None):
        assert regular_udf_funcs is not None or general_udf_funcs is not None
        self.regular_udfs = False
        self.general_udfs = False
        self.regular_udf_cfuncs = None
        self.general_udf_cfunc = None
        if regular_udf_funcs is not None:
            (self.var_typs, self.init_func, self.update_all_func, self.
                combine_all_func, self.eval_all_func) = regular_udf_funcs
            self.regular_udfs = True
        if general_udf_funcs is not None:
            self.general_udf_funcs = general_udf_funcs
            self.general_udfs = True

    def set_regular_cfuncs(self, update_cb, combine_cb, eval_cb):
        assert self.regular_udfs and self.regular_udf_cfuncs is None
        self.regular_udf_cfuncs = [update_cb, combine_cb, eval_cb]

    def set_general_cfunc(self, general_udf_cb):
        assert self.general_udfs and self.general_udf_cfunc is None
        self.general_udf_cfunc = general_udf_cb


AggFuncStruct = namedtuple('AggFuncStruct', ['func', 'ftype'])
supported_agg_funcs = ['no_op', 'transform', 'size', 'shift', 'sum',
    'count', 'nunique', 'median', 'cumsum', 'cumprod', 'cummin', 'cummax',
    'mean', 'min', 'max', 'prod', 'first', 'last', 'idxmin', 'idxmax',
    'var', 'std', 'udf', 'gen_udf']
supported_transform_funcs = ['no_op', 'sum', 'count', 'nunique', 'median',
    'mean', 'min', 'max', 'prod', 'first', 'last', 'var', 'std']


def get_agg_func(func_ir, func_name, rhs, series_type=None, typemap=None):
    if func_name == 'no_op':
        raise BodoError('Unknown aggregation function used in groupby.')
    if series_type is None:
        series_type = SeriesType(types.float64)
    if func_name in {'var', 'std'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 3
        func.ncols_post_shuffle = 4
        return func
    if func_name in {'first', 'last'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        return func
    if func_name in {'idxmin', 'idxmax'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 2
        func.ncols_post_shuffle = 2
        return func
    if func_name in supported_agg_funcs[:-8]:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        zgys__vpdtc = True
        tnigi__mxp = 1
        if isinstance(rhs, ir.Expr):
            for aofa__ozwwz in rhs.kws:
                if func_name in list_cumulative:
                    if aofa__ozwwz[0] == 'skipna':
                        zgys__vpdtc = guard(find_const, func_ir, aofa__ozwwz[1]
                            )
                        if not isinstance(zgys__vpdtc, bool):
                            raise BodoError(
                                'For {} argument of skipna should be a boolean'
                                .format(func_name))
                if func_name == 'nunique':
                    if aofa__ozwwz[0] == 'dropna':
                        zgys__vpdtc = guard(find_const, func_ir, aofa__ozwwz[1]
                            )
                        if not isinstance(zgys__vpdtc, bool):
                            raise BodoError(
                                'argument of dropna to nunique should be a boolean'
                                )
        if func_name == 'shift' and (len(rhs.args) > 0 or len(rhs.kws) > 0):
            tnigi__mxp = get_call_expr_arg('shift', rhs.args, dict(rhs.kws),
                0, 'periods', tnigi__mxp)
            tnigi__mxp = guard(find_const, func_ir, tnigi__mxp)
        func.skipdropna = zgys__vpdtc
        func.periods = tnigi__mxp
        if func_name == 'transform':
            kws = dict(rhs.kws)
            nnzpm__fqvo = get_call_expr_arg(func_name, rhs.args, kws, 0,
                'func', '')
            hkc__lwx = typemap[nnzpm__fqvo.name]
            lpmz__tdbz = None
            if isinstance(hkc__lwx, str):
                lpmz__tdbz = hkc__lwx
            elif is_overload_constant_str(hkc__lwx):
                lpmz__tdbz = get_overload_const_str(hkc__lwx)
            elif bodo.utils.typing.is_builtin_function(hkc__lwx):
                lpmz__tdbz = bodo.utils.typing.get_builtin_function_name(
                    hkc__lwx)
            if lpmz__tdbz not in bodo.ir.aggregate.supported_transform_funcs[:
                ]:
                raise BodoError(f'unsupported transform function {lpmz__tdbz}')
            func.transform_func = supported_agg_funcs.index(lpmz__tdbz)
        else:
            func.transform_func = supported_agg_funcs.index('no_op')
        return func
    assert func_name in ['agg', 'aggregate']
    assert typemap is not None
    kws = dict(rhs.kws)
    nnzpm__fqvo = get_call_expr_arg(func_name, rhs.args, kws, 0, 'func', '')
    if nnzpm__fqvo == '':
        hkc__lwx = types.none
    else:
        hkc__lwx = typemap[nnzpm__fqvo.name]
    if is_overload_constant_dict(hkc__lwx):
        tbkim__pah = get_overload_constant_dict(hkc__lwx)
        sttj__dmnk = [get_agg_func_udf(func_ir, f_val, rhs, series_type,
            typemap) for f_val in tbkim__pah.values()]
        return sttj__dmnk
    if hkc__lwx == types.none:
        return [get_agg_func_udf(func_ir, get_literal_value(typemap[f_val.
            name])[1], rhs, series_type, typemap) for f_val in kws.values()]
    if isinstance(hkc__lwx, types.BaseTuple):
        sttj__dmnk = []
        ect__mbq = 0
        for t in hkc__lwx.types:
            if is_overload_constant_str(t):
                func_name = get_overload_const_str(t)
                sttj__dmnk.append(get_agg_func(func_ir, func_name, rhs,
                    series_type, typemap))
            else:
                assert typemap is not None, 'typemap is required for agg UDF handling'
                func = _get_const_agg_func(t, func_ir)
                func.ftype = 'udf'
                func.fname = _get_udf_name(func)
                if func.fname == '<lambda>':
                    func.fname = '<lambda_' + str(ect__mbq) + '>'
                    ect__mbq += 1
                sttj__dmnk.append(func)
        return [sttj__dmnk]
    if is_overload_constant_str(hkc__lwx):
        func_name = get_overload_const_str(hkc__lwx)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(hkc__lwx):
        func_name = bodo.utils.typing.get_builtin_function_name(hkc__lwx)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    assert typemap is not None, 'typemap is required for agg UDF handling'
    func = _get_const_agg_func(typemap[rhs.args[0].name], func_ir)
    func.ftype = 'udf'
    func.fname = _get_udf_name(func)
    return func


def get_agg_func_udf(func_ir, f_val, rhs, series_type, typemap):
    if isinstance(f_val, str):
        return get_agg_func(func_ir, f_val, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(f_val):
        func_name = bodo.utils.typing.get_builtin_function_name(f_val)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if isinstance(f_val, (tuple, list)):
        ect__mbq = 0
        vcoc__ydyzx = []
        for ovfec__tcq in f_val:
            func = get_agg_func_udf(func_ir, ovfec__tcq, rhs, series_type,
                typemap)
            if func.fname == '<lambda>' and len(f_val) > 1:
                func.fname = f'<lambda_{ect__mbq}>'
                ect__mbq += 1
            vcoc__ydyzx.append(func)
        return vcoc__ydyzx
    else:
        assert is_expr(f_val, 'make_function') or isinstance(f_val, (numba.
            core.registry.CPUDispatcher, types.Dispatcher))
        assert typemap is not None, 'typemap is required for agg UDF handling'
        func = _get_const_agg_func(f_val, func_ir)
        func.ftype = 'udf'
        func.fname = _get_udf_name(func)
        return func


def _get_udf_name(func):
    code = func.code if hasattr(func, 'code') else func.__code__
    lpmz__tdbz = code.co_name
    return lpmz__tdbz


def _get_const_agg_func(func_typ, func_ir):
    agg_func = get_overload_const_func(func_typ, func_ir)
    if is_expr(agg_func, 'make_function'):

        def agg_func_wrapper(A):
            return A
        agg_func_wrapper.__code__ = agg_func.code
        agg_func = agg_func_wrapper
        return agg_func
    return agg_func


@infer_global(type)
class TypeDt64(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if len(args) == 1 and isinstance(args[0], (types.NPDatetime, types.
            NPTimedelta)):
            lla__qdjj = types.DType(args[0])
            return signature(lla__qdjj, *args)


@numba.njit(no_cpython_wrapper=True)
def _var_combine(ssqdm_a, mean_a, nobs_a, ssqdm_b, mean_b, nobs_b):
    tgehi__bttp = nobs_a + nobs_b
    quorb__rjzs = (nobs_a * mean_a + nobs_b * mean_b) / tgehi__bttp
    edrly__lbgug = mean_b - mean_a
    vrd__ibz = (ssqdm_a + ssqdm_b + edrly__lbgug * edrly__lbgug * nobs_a *
        nobs_b / tgehi__bttp)
    return vrd__ibz, quorb__rjzs, tgehi__bttp


def __special_combine(*args):
    return


@infer_global(__special_combine)
class SpecialCombineTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.void, *unliteral_all(args))


@lower_builtin(__special_combine, types.VarArg(types.Any))
def lower_special_combine(context, builder, sig, args):
    return context.get_dummy_value()


class Aggregate(ir.Stmt):

    def __init__(self, df_out, df_in, key_names, gb_info_in, gb_info_out,
        out_key_vars, df_out_vars, df_in_vars, key_arrs, input_has_index,
        same_index, return_key, loc, func_name, dropna=True, pivot_arr=None,
        pivot_values=None, is_crosstab=False):
        self.df_out = df_out
        self.df_in = df_in
        self.key_names = key_names
        self.gb_info_in = gb_info_in
        self.gb_info_out = gb_info_out
        self.out_key_vars = out_key_vars
        self.df_out_vars = df_out_vars
        self.df_in_vars = df_in_vars
        self.key_arrs = key_arrs
        self.input_has_index = input_has_index
        self.same_index = same_index
        self.return_key = return_key
        self.loc = loc
        self.func_name = func_name
        self.dropna = dropna
        self.pivot_arr = pivot_arr
        self.pivot_values = pivot_values
        self.is_crosstab = is_crosstab

    def __repr__(self):
        uya__yqc = ''
        for apgz__iqlaq, v in self.df_out_vars.items():
            uya__yqc += "'{}':{}, ".format(apgz__iqlaq, v.name)
        maic__entxt = '{}{{{}}}'.format(self.df_out, uya__yqc)
        ymwkb__fms = ''
        for apgz__iqlaq, v in self.df_in_vars.items():
            ymwkb__fms += "'{}':{}, ".format(apgz__iqlaq, v.name)
        lrbxu__mfs = '{}{{{}}}'.format(self.df_in, ymwkb__fms)
        mym__dakaf = 'pivot {}:{}'.format(self.pivot_arr.name, self.
            pivot_values) if self.pivot_arr is not None else ''
        key_names = ','.join(self.key_names)
        xpmoq__kfcus = ','.join([v.name for v in self.key_arrs])
        return 'aggregate: {} = {} [key: {}:{}] {}'.format(maic__entxt,
            lrbxu__mfs, key_names, xpmoq__kfcus, mym__dakaf)

    def remove_out_col(self, out_col_name):
        self.df_out_vars.pop(out_col_name)
        xaubt__npsqu, frzv__bmon = self.gb_info_out.pop(out_col_name)
        if xaubt__npsqu is None and not self.is_crosstab:
            return
        xcfv__nuemh = self.gb_info_in[xaubt__npsqu]
        if self.pivot_arr is not None:
            self.pivot_values.remove(out_col_name)
            for i, (func, uya__yqc) in enumerate(xcfv__nuemh):
                try:
                    uya__yqc.remove(out_col_name)
                    if len(uya__yqc) == 0:
                        xcfv__nuemh.pop(i)
                        break
                except ValueError as zhwc__svcy:
                    continue
        else:
            for i, (func, taycn__ktidk) in enumerate(xcfv__nuemh):
                if taycn__ktidk == out_col_name:
                    xcfv__nuemh.pop(i)
                    break
        if len(xcfv__nuemh) == 0:
            self.gb_info_in.pop(xaubt__npsqu)
            self.df_in_vars.pop(xaubt__npsqu)


def aggregate_usedefs(aggregate_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({v.name for v in aggregate_node.key_arrs})
    use_set.update({v.name for v in aggregate_node.df_in_vars.values()})
    if aggregate_node.pivot_arr is not None:
        use_set.add(aggregate_node.pivot_arr.name)
    def_set.update({v.name for v in aggregate_node.df_out_vars.values()})
    if aggregate_node.out_key_vars is not None:
        def_set.update({v.name for v in aggregate_node.out_key_vars})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Aggregate] = aggregate_usedefs


def remove_dead_aggregate(aggregate_node, lives_no_aliases, lives,
    arg_aliases, alias_map, func_ir, typemap):
    jzh__tkfa = [akm__dfdnj for akm__dfdnj, jfxa__okjn in aggregate_node.
        df_out_vars.items() if jfxa__okjn.name not in lives]
    for flruc__xuhy in jzh__tkfa:
        aggregate_node.remove_out_col(flruc__xuhy)
    out_key_vars = aggregate_node.out_key_vars
    if out_key_vars is not None and all(v.name not in lives for v in
        out_key_vars):
        aggregate_node.out_key_vars = None
    if len(aggregate_node.df_out_vars
        ) == 0 and aggregate_node.out_key_vars is None:
        return None
    return aggregate_node


ir_utils.remove_dead_extensions[Aggregate] = remove_dead_aggregate


def get_copies_aggregate(aggregate_node, typemap):
    zhvcl__myjft = set(v.name for v in aggregate_node.df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        zhvcl__myjft.update({v.name for v in aggregate_node.out_key_vars})
    return set(), zhvcl__myjft


ir_utils.copy_propagate_extensions[Aggregate] = get_copies_aggregate


def apply_copies_aggregate(aggregate_node, var_dict, name_var_table,
    typemap, calltypes, save_copies):
    for i in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[i] = replace_vars_inner(aggregate_node.
            key_arrs[i], var_dict)
    for akm__dfdnj in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[akm__dfdnj] = replace_vars_inner(
            aggregate_node.df_in_vars[akm__dfdnj], var_dict)
    for akm__dfdnj in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[akm__dfdnj] = replace_vars_inner(
            aggregate_node.df_out_vars[akm__dfdnj], var_dict)
    if aggregate_node.out_key_vars is not None:
        for i in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[i] = replace_vars_inner(aggregate_node
                .out_key_vars[i], var_dict)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = replace_vars_inner(aggregate_node.
            pivot_arr, var_dict)


ir_utils.apply_copy_propagate_extensions[Aggregate] = apply_copies_aggregate


def visit_vars_aggregate(aggregate_node, callback, cbdata):
    if debug_prints():
        print('visiting aggregate vars for:', aggregate_node)
        print('cbdata: ', sorted(cbdata.items()))
    for i in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[i] = visit_vars_inner(aggregate_node.
            key_arrs[i], callback, cbdata)
    for akm__dfdnj in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[akm__dfdnj] = visit_vars_inner(aggregate_node
            .df_in_vars[akm__dfdnj], callback, cbdata)
    for akm__dfdnj in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[akm__dfdnj] = visit_vars_inner(
            aggregate_node.df_out_vars[akm__dfdnj], callback, cbdata)
    if aggregate_node.out_key_vars is not None:
        for i in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[i] = visit_vars_inner(aggregate_node
                .out_key_vars[i], callback, cbdata)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = visit_vars_inner(aggregate_node.
            pivot_arr, callback, cbdata)


ir_utils.visit_vars_extensions[Aggregate] = visit_vars_aggregate


def aggregate_array_analysis(aggregate_node, equiv_set, typemap, array_analysis
    ):
    assert len(aggregate_node.df_out_vars
        ) > 0 or aggregate_node.out_key_vars is not None or aggregate_node.is_crosstab, 'empty aggregate in array analysis'
    udmju__vbh = []
    for qipnr__bspk in aggregate_node.key_arrs:
        fjoso__qruzq = equiv_set.get_shape(qipnr__bspk)
        if fjoso__qruzq:
            udmju__vbh.append(fjoso__qruzq[0])
    if aggregate_node.pivot_arr is not None:
        fjoso__qruzq = equiv_set.get_shape(aggregate_node.pivot_arr)
        if fjoso__qruzq:
            udmju__vbh.append(fjoso__qruzq[0])
    for jfxa__okjn in aggregate_node.df_in_vars.values():
        fjoso__qruzq = equiv_set.get_shape(jfxa__okjn)
        if fjoso__qruzq:
            udmju__vbh.append(fjoso__qruzq[0])
    if len(udmju__vbh) > 1:
        equiv_set.insert_equiv(*udmju__vbh)
    mmmw__gqtnh = []
    udmju__vbh = []
    eudvo__clt = list(aggregate_node.df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        eudvo__clt.extend(aggregate_node.out_key_vars)
    for jfxa__okjn in eudvo__clt:
        rcir__cgw = typemap[jfxa__okjn.name]
        zlcfm__lcg = array_analysis._gen_shape_call(equiv_set, jfxa__okjn,
            rcir__cgw.ndim, None, mmmw__gqtnh)
        equiv_set.insert_equiv(jfxa__okjn, zlcfm__lcg)
        udmju__vbh.append(zlcfm__lcg[0])
        equiv_set.define(jfxa__okjn, set())
    if len(udmju__vbh) > 1:
        equiv_set.insert_equiv(*udmju__vbh)
    return [], mmmw__gqtnh


numba.parfors.array_analysis.array_analysis_extensions[Aggregate
    ] = aggregate_array_analysis


def aggregate_distributed_analysis(aggregate_node, array_dists):
    idnn__zbaj = Distribution.OneD
    for jfxa__okjn in aggregate_node.df_in_vars.values():
        idnn__zbaj = Distribution(min(idnn__zbaj.value, array_dists[
            jfxa__okjn.name].value))
    for qipnr__bspk in aggregate_node.key_arrs:
        idnn__zbaj = Distribution(min(idnn__zbaj.value, array_dists[
            qipnr__bspk.name].value))
    if aggregate_node.pivot_arr is not None:
        idnn__zbaj = Distribution(min(idnn__zbaj.value, array_dists[
            aggregate_node.pivot_arr.name].value))
        array_dists[aggregate_node.pivot_arr.name] = idnn__zbaj
    for jfxa__okjn in aggregate_node.df_in_vars.values():
        array_dists[jfxa__okjn.name] = idnn__zbaj
    for qipnr__bspk in aggregate_node.key_arrs:
        array_dists[qipnr__bspk.name] = idnn__zbaj
    qnfig__ohw = Distribution.OneD_Var
    for jfxa__okjn in aggregate_node.df_out_vars.values():
        if jfxa__okjn.name in array_dists:
            qnfig__ohw = Distribution(min(qnfig__ohw.value, array_dists[
                jfxa__okjn.name].value))
    if aggregate_node.out_key_vars is not None:
        for jfxa__okjn in aggregate_node.out_key_vars:
            if jfxa__okjn.name in array_dists:
                qnfig__ohw = Distribution(min(qnfig__ohw.value, array_dists
                    [jfxa__okjn.name].value))
    qnfig__ohw = Distribution(min(qnfig__ohw.value, idnn__zbaj.value))
    for jfxa__okjn in aggregate_node.df_out_vars.values():
        array_dists[jfxa__okjn.name] = qnfig__ohw
    if aggregate_node.out_key_vars is not None:
        for irrk__sbkn in aggregate_node.out_key_vars:
            array_dists[irrk__sbkn.name] = qnfig__ohw
    if qnfig__ohw != Distribution.OneD_Var:
        for qipnr__bspk in aggregate_node.key_arrs:
            array_dists[qipnr__bspk.name] = qnfig__ohw
        if aggregate_node.pivot_arr is not None:
            array_dists[aggregate_node.pivot_arr.name] = qnfig__ohw
        for jfxa__okjn in aggregate_node.df_in_vars.values():
            array_dists[jfxa__okjn.name] = qnfig__ohw


distributed_analysis.distributed_analysis_extensions[Aggregate
    ] = aggregate_distributed_analysis


def build_agg_definitions(agg_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for jfxa__okjn in agg_node.df_out_vars.values():
        definitions[jfxa__okjn.name].append(agg_node)
    if agg_node.out_key_vars is not None:
        for irrk__sbkn in agg_node.out_key_vars:
            definitions[irrk__sbkn.name].append(agg_node)
    return definitions


ir_utils.build_defs_extensions[Aggregate] = build_agg_definitions


def __update_redvars():
    pass


@infer_global(__update_redvars)
class UpdateDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.void, *args)


def __combine_redvars():
    pass


@infer_global(__combine_redvars)
class CombineDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.void, *args)


def __eval_res():
    pass


@infer_global(__eval_res)
class EvalDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(args[0].dtype, *args)


def agg_distributed_run(agg_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    parallel = False
    if array_dists is not None:
        parallel = True
        for v in (list(agg_node.df_in_vars.values()) + list(agg_node.
            df_out_vars.values()) + agg_node.key_arrs):
            if array_dists[v.name
                ] != distributed_pass.Distribution.OneD and array_dists[v.name
                ] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    coki__iekx = tuple(typemap[v.name] for v in agg_node.key_arrs)
    wteh__rjsf = [v for vfqdm__kxp, v in agg_node.df_in_vars.items()]
    xspoa__xujg = [v for vfqdm__kxp, v in agg_node.df_out_vars.items()]
    in_col_typs = []
    sttj__dmnk = []
    if agg_node.pivot_arr is not None:
        for xaubt__npsqu, xcfv__nuemh in agg_node.gb_info_in.items():
            for func, frzv__bmon in xcfv__nuemh:
                if xaubt__npsqu is not None:
                    in_col_typs.append(typemap[agg_node.df_in_vars[
                        xaubt__npsqu].name])
                sttj__dmnk.append(func)
    else:
        for xaubt__npsqu, func in agg_node.gb_info_out.values():
            if xaubt__npsqu is not None:
                in_col_typs.append(typemap[agg_node.df_in_vars[xaubt__npsqu
                    ].name])
            sttj__dmnk.append(func)
    out_col_typs = tuple(typemap[v.name] for v in xspoa__xujg)
    pivot_typ = types.none if agg_node.pivot_arr is None else typemap[agg_node
        .pivot_arr.name]
    arg_typs = tuple(coki__iekx + tuple(typemap[v.name] for v in wteh__rjsf
        ) + (pivot_typ,))
    hjrv__frna = {'bodo': bodo, 'np': np, 'dt64_dtype': np.dtype(
        'datetime64[ns]'), 'td64_dtype': np.dtype('timedelta64[ns]')}
    for i, in_col_typ in enumerate(in_col_typs):
        if isinstance(in_col_typ, bodo.CategoricalArrayType):
            hjrv__frna.update({f'in_cat_dtype_{i}': in_col_typ})
    for i, axtt__yxkrw in enumerate(out_col_typs):
        if isinstance(axtt__yxkrw, bodo.CategoricalArrayType):
            hjrv__frna.update({f'out_cat_dtype_{i}': axtt__yxkrw})
    udf_func_struct = get_udf_func_struct(sttj__dmnk, agg_node.
        input_has_index, in_col_typs, out_col_typs, typingctx, targetctx,
        pivot_typ, agg_node.pivot_values, agg_node.is_crosstab)
    srr__dhcl = gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs,
        parallel, udf_func_struct)
    hjrv__frna.update({'pd': pd, 'pre_alloc_string_array':
        pre_alloc_string_array, 'pre_alloc_binary_array':
        pre_alloc_binary_array, 'pre_alloc_array_item_array':
        pre_alloc_array_item_array, 'string_array_type': string_array_type,
        'alloc_decimal_array': alloc_decimal_array, 'array_to_info':
        array_to_info, 'arr_info_list_to_table': arr_info_list_to_table,
        'coerce_to_array': bodo.utils.conversion.coerce_to_array,
        'groupby_and_aggregate': groupby_and_aggregate,
        'pivot_groupby_and_aggregate': pivot_groupby_and_aggregate,
        'compute_node_partition_by_hash': compute_node_partition_by_hash,
        'info_from_table': info_from_table, 'info_to_array': info_to_array,
        'delete_info_decref_array': delete_info_decref_array,
        'delete_table': delete_table, 'add_agg_cfunc_sym':
        add_agg_cfunc_sym, 'get_agg_udf_addr': get_agg_udf_addr,
        'delete_table_decref_arrays': delete_table_decref_arrays})
    if udf_func_struct is not None:
        if udf_func_struct.regular_udfs:
            hjrv__frna.update({'__update_redvars': udf_func_struct.
                update_all_func, '__init_func': udf_func_struct.init_func,
                '__combine_redvars': udf_func_struct.combine_all_func,
                '__eval_res': udf_func_struct.eval_all_func,
                'cpp_cb_update': udf_func_struct.regular_udf_cfuncs[0],
                'cpp_cb_combine': udf_func_struct.regular_udf_cfuncs[1],
                'cpp_cb_eval': udf_func_struct.regular_udf_cfuncs[2]})
        if udf_func_struct.general_udfs:
            hjrv__frna.update({'cpp_cb_general': udf_func_struct.
                general_udf_cfunc})
    fkh__iwu = compile_to_numba_ir(srr__dhcl, hjrv__frna, typingctx=
        typingctx, targetctx=targetctx, arg_typs=arg_typs, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    hhb__afyno = []
    if agg_node.pivot_arr is None:
        ksxa__bogf = agg_node.key_arrs[0].scope
        loc = agg_node.loc
        ayw__ijb = ir.Var(ksxa__bogf, mk_unique_var('dummy_none'), loc)
        typemap[ayw__ijb.name] = types.none
        hhb__afyno.append(ir.Assign(ir.Const(None, loc), ayw__ijb, loc))
        wteh__rjsf.append(ayw__ijb)
    else:
        wteh__rjsf.append(agg_node.pivot_arr)
    replace_arg_nodes(fkh__iwu, agg_node.key_arrs + wteh__rjsf)
    uxsi__oxg = fkh__iwu.body[-3]
    assert is_assign(uxsi__oxg) and isinstance(uxsi__oxg.value, ir.Expr
        ) and uxsi__oxg.value.op == 'build_tuple'
    hhb__afyno += fkh__iwu.body[:-3]
    eudvo__clt = list(agg_node.df_out_vars.values())
    if agg_node.out_key_vars is not None:
        eudvo__clt += agg_node.out_key_vars
    for i, plqyz__lxgr in enumerate(eudvo__clt):
        kay__ekag = uxsi__oxg.value.items[i]
        hhb__afyno.append(ir.Assign(kay__ekag, plqyz__lxgr, plqyz__lxgr.loc))
    return hhb__afyno


distributed_pass.distributed_run_extensions[Aggregate] = agg_distributed_run


def get_numba_set(dtype):
    pass


@infer_global(get_numba_set)
class GetNumbaSetTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        arr = args[0]
        dtype = types.Tuple([t.dtype for t in arr.types]) if isinstance(arr,
            types.BaseTuple) else arr.dtype
        if isinstance(arr, types.BaseTuple) and len(arr.types) == 1:
            dtype = arr.types[0].dtype
        return signature(types.Set(dtype), *args)


@lower_builtin(get_numba_set, types.Any)
def lower_get_numba_set(context, builder, sig, args):
    return numba.cpython.setobj.set_empty_constructor(context, builder, sig,
        args)


@infer_global(bool)
class BoolNoneTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        pgbom__bhr = args[0]
        if pgbom__bhr == types.none:
            return signature(types.boolean, *args)


@lower_builtin(bool, types.none)
def lower_column_mean_impl(context, builder, sig, args):
    myzcb__ieaf = context.compile_internal(builder, lambda a: False, sig, args)
    return myzcb__ieaf


def setitem_array_with_str(arr, i, v):
    return


@overload(setitem_array_with_str)
def setitem_array_with_str_overload(arr, i, val):
    if arr == string_array_type:

        def setitem_str_arr(arr, i, val):
            arr[i] = val
        return setitem_str_arr
    if val == string_type:
        return lambda arr, i, val: None

    def setitem_impl(arr, i, val):
        arr[i] = val
    return setitem_impl


def _gen_dummy_alloc(t, colnum=0, is_input=False):
    if isinstance(t, IntegerArrayType):
        ycpb__rwsp = IntDtype(t.dtype).name
        assert ycpb__rwsp.endswith('Dtype()')
        ycpb__rwsp = ycpb__rwsp[:-7]
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype='{ycpb__rwsp}'))"
            )
    elif isinstance(t, BooleanArrayType):
        return (
            'bodo.libs.bool_arr_ext.init_bool_array(np.empty(0, np.bool_), np.empty(0, np.uint8))'
            )
    elif isinstance(t, StringArrayType):
        return 'pre_alloc_string_array(1, 1)'
    elif isinstance(t, BinaryArrayType):
        return 'pre_alloc_binary_array(1, 1)'
    elif t == ArrayItemArrayType(string_array_type):
        return 'pre_alloc_array_item_array(1, (1, 1), string_array_type)'
    elif isinstance(t, DecimalArrayType):
        return 'alloc_decimal_array(1, {}, {})'.format(t.precision, t.scale)
    elif isinstance(t, DatetimeDateArrayType):
        return (
            'bodo.hiframes.datetime_date_ext.init_datetime_date_array(np.empty(1, np.int64), np.empty(1, np.uint8))'
            )
    elif isinstance(t, bodo.CategoricalArrayType):
        if t.dtype.categories is None:
            raise BodoError(
                'Groupby agg operations on Categorical types require constant categories'
                )
        dfx__oel = 'in' if is_input else 'out'
        return f'bodo.utils.utils.alloc_type(1, {dfx__oel}_cat_dtype_{colnum})'
    else:
        return 'np.empty(1, {})'.format(_get_np_dtype(t.dtype))


def _get_np_dtype(t):
    if t == types.bool_:
        return 'np.bool_'
    if t == types.NPDatetime('ns'):
        return 'dt64_dtype'
    if t == types.NPTimedelta('ns'):
        return 'td64_dtype'
    return 'np.{}'.format(t)


def gen_update_cb(udf_func_struct, allfuncs, n_keys, data_in_typs_,
    out_data_typs, do_combine, func_idx_to_in_col, label_suffix):
    xlfs__dmxa = udf_func_struct.var_typs
    dcpse__yygsz = len(xlfs__dmxa)
    kdfo__gyn = (
        'def bodo_gb_udf_update_local{}(in_table, out_table, row_to_group):\n'
        .format(label_suffix))
    kdfo__gyn += '    if is_null_pointer(in_table):\n'
    kdfo__gyn += '        return\n'
    kdfo__gyn += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in xlfs__dmxa]), 
        ',' if len(xlfs__dmxa) == 1 else '')
    gggzu__uwcy = n_keys
    jmw__mcd = []
    redvar_offsets = []
    xxh__aynyk = []
    if do_combine:
        for i, ovfec__tcq in enumerate(allfuncs):
            if ovfec__tcq.ftype != 'udf':
                gggzu__uwcy += ovfec__tcq.ncols_pre_shuffle
            else:
                redvar_offsets += list(range(gggzu__uwcy, gggzu__uwcy +
                    ovfec__tcq.n_redvars))
                gggzu__uwcy += ovfec__tcq.n_redvars
                xxh__aynyk.append(data_in_typs_[func_idx_to_in_col[i]])
                jmw__mcd.append(func_idx_to_in_col[i] + n_keys)
    else:
        for i, ovfec__tcq in enumerate(allfuncs):
            if ovfec__tcq.ftype != 'udf':
                gggzu__uwcy += ovfec__tcq.ncols_post_shuffle
            else:
                redvar_offsets += list(range(gggzu__uwcy + 1, gggzu__uwcy +
                    1 + ovfec__tcq.n_redvars))
                gggzu__uwcy += ovfec__tcq.n_redvars + 1
                xxh__aynyk.append(data_in_typs_[func_idx_to_in_col[i]])
                jmw__mcd.append(func_idx_to_in_col[i] + n_keys)
    assert len(redvar_offsets) == dcpse__yygsz
    wdpwu__znfh = len(xxh__aynyk)
    uxj__afme = []
    for i, t in enumerate(xxh__aynyk):
        uxj__afme.append(_gen_dummy_alloc(t, i, True))
    kdfo__gyn += '    data_in_dummy = ({}{})\n'.format(','.join(uxj__afme),
        ',' if len(xxh__aynyk) == 1 else '')
    kdfo__gyn += """
    # initialize redvar cols
"""
    kdfo__gyn += '    init_vals = __init_func()\n'
    for i in range(dcpse__yygsz):
        kdfo__gyn += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(i, redvar_offsets[i], i))
        kdfo__gyn += '    incref(redvar_arr_{})\n'.format(i)
        kdfo__gyn += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(i, i)
    kdfo__gyn += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(i) for i in range(dcpse__yygsz)]), ',' if dcpse__yygsz == 1 else
        '')
    kdfo__gyn += '\n'
    for i in range(wdpwu__znfh):
        kdfo__gyn += (
            """    data_in_{} = info_to_array(info_from_table(in_table, {}), data_in_dummy[{}])
"""
            .format(i, jmw__mcd[i], i))
        kdfo__gyn += '    incref(data_in_{})\n'.format(i)
    kdfo__gyn += '    data_in = ({}{})\n'.format(','.join(['data_in_{}'.
        format(i) for i in range(wdpwu__znfh)]), ',' if wdpwu__znfh == 1 else
        '')
    kdfo__gyn += '\n'
    kdfo__gyn += '    for i in range(len(data_in_0)):\n'
    kdfo__gyn += '        w_ind = row_to_group[i]\n'
    kdfo__gyn += '        if w_ind != -1:\n'
    kdfo__gyn += (
        '            __update_redvars(redvars, data_in, w_ind, i, pivot_arr=None)\n'
        )
    uynll__ztei = {}
    exec(kdfo__gyn, {'bodo': bodo, 'np': np, 'pd': pd, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table, 'incref': incref,
        'pre_alloc_string_array': pre_alloc_string_array, '__init_func':
        udf_func_struct.init_func, '__update_redvars': udf_func_struct.
        update_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, uynll__ztei)
    return uynll__ztei['bodo_gb_udf_update_local{}'.format(label_suffix)]


def gen_combine_cb(udf_func_struct, allfuncs, n_keys, out_data_typs,
    label_suffix):
    xlfs__dmxa = udf_func_struct.var_typs
    dcpse__yygsz = len(xlfs__dmxa)
    kdfo__gyn = (
        'def bodo_gb_udf_combine{}(in_table, out_table, row_to_group):\n'.
        format(label_suffix))
    kdfo__gyn += '    if is_null_pointer(in_table):\n'
    kdfo__gyn += '        return\n'
    kdfo__gyn += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in xlfs__dmxa]), 
        ',' if len(xlfs__dmxa) == 1 else '')
    ayhd__tkloq = n_keys
    xwzeh__uqyf = n_keys
    grhq__jhc = []
    ompq__wfbhr = []
    for ovfec__tcq in allfuncs:
        if ovfec__tcq.ftype != 'udf':
            ayhd__tkloq += ovfec__tcq.ncols_pre_shuffle
            xwzeh__uqyf += ovfec__tcq.ncols_post_shuffle
        else:
            grhq__jhc += list(range(ayhd__tkloq, ayhd__tkloq + ovfec__tcq.
                n_redvars))
            ompq__wfbhr += list(range(xwzeh__uqyf + 1, xwzeh__uqyf + 1 +
                ovfec__tcq.n_redvars))
            ayhd__tkloq += ovfec__tcq.n_redvars
            xwzeh__uqyf += 1 + ovfec__tcq.n_redvars
    assert len(grhq__jhc) == dcpse__yygsz
    kdfo__gyn += """
    # initialize redvar cols
"""
    kdfo__gyn += '    init_vals = __init_func()\n'
    for i in range(dcpse__yygsz):
        kdfo__gyn += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(i, ompq__wfbhr[i], i))
        kdfo__gyn += '    incref(redvar_arr_{})\n'.format(i)
        kdfo__gyn += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(i, i)
    kdfo__gyn += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(i) for i in range(dcpse__yygsz)]), ',' if dcpse__yygsz == 1 else
        '')
    kdfo__gyn += '\n'
    for i in range(dcpse__yygsz):
        kdfo__gyn += (
            """    recv_redvar_arr_{} = info_to_array(info_from_table(in_table, {}), data_redvar_dummy[{}])
"""
            .format(i, grhq__jhc[i], i))
        kdfo__gyn += '    incref(recv_redvar_arr_{})\n'.format(i)
    kdfo__gyn += '    recv_redvars = ({}{})\n'.format(','.join([
        'recv_redvar_arr_{}'.format(i) for i in range(dcpse__yygsz)]), ',' if
        dcpse__yygsz == 1 else '')
    kdfo__gyn += '\n'
    if dcpse__yygsz:
        kdfo__gyn += '    for i in range(len(recv_redvar_arr_0)):\n'
        kdfo__gyn += '        w_ind = row_to_group[i]\n'
        kdfo__gyn += (
            '        __combine_redvars(redvars, recv_redvars, w_ind, i, pivot_arr=None)\n'
            )
    uynll__ztei = {}
    exec(kdfo__gyn, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__init_func':
        udf_func_struct.init_func, '__combine_redvars': udf_func_struct.
        combine_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, uynll__ztei)
    return uynll__ztei['bodo_gb_udf_combine{}'.format(label_suffix)]


def gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_data_typs_, label_suffix
    ):
    xlfs__dmxa = udf_func_struct.var_typs
    dcpse__yygsz = len(xlfs__dmxa)
    gggzu__uwcy = n_keys
    redvar_offsets = []
    rfkfq__pzax = []
    out_data_typs = []
    for i, ovfec__tcq in enumerate(allfuncs):
        if ovfec__tcq.ftype != 'udf':
            gggzu__uwcy += ovfec__tcq.ncols_post_shuffle
        else:
            rfkfq__pzax.append(gggzu__uwcy)
            redvar_offsets += list(range(gggzu__uwcy + 1, gggzu__uwcy + 1 +
                ovfec__tcq.n_redvars))
            gggzu__uwcy += 1 + ovfec__tcq.n_redvars
            out_data_typs.append(out_data_typs_[i])
    assert len(redvar_offsets) == dcpse__yygsz
    wdpwu__znfh = len(out_data_typs)
    kdfo__gyn = 'def bodo_gb_udf_eval{}(table):\n'.format(label_suffix)
    kdfo__gyn += '    if is_null_pointer(table):\n'
    kdfo__gyn += '        return\n'
    kdfo__gyn += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in xlfs__dmxa]), 
        ',' if len(xlfs__dmxa) == 1 else '')
    kdfo__gyn += '    out_data_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t.dtype)) for t in
        out_data_typs]), ',' if len(out_data_typs) == 1 else '')
    for i in range(dcpse__yygsz):
        kdfo__gyn += (
            """    redvar_arr_{} = info_to_array(info_from_table(table, {}), data_redvar_dummy[{}])
"""
            .format(i, redvar_offsets[i], i))
        kdfo__gyn += '    incref(redvar_arr_{})\n'.format(i)
    kdfo__gyn += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(i) for i in range(dcpse__yygsz)]), ',' if dcpse__yygsz == 1 else
        '')
    kdfo__gyn += '\n'
    for i in range(wdpwu__znfh):
        kdfo__gyn += (
            """    data_out_{} = info_to_array(info_from_table(table, {}), out_data_dummy[{}])
"""
            .format(i, rfkfq__pzax[i], i))
        kdfo__gyn += '    incref(data_out_{})\n'.format(i)
    kdfo__gyn += '    data_out = ({}{})\n'.format(','.join(['data_out_{}'.
        format(i) for i in range(wdpwu__znfh)]), ',' if wdpwu__znfh == 1 else
        '')
    kdfo__gyn += '\n'
    kdfo__gyn += '    for i in range(len(data_out_0)):\n'
    kdfo__gyn += '        __eval_res(redvars, data_out, i)\n'
    uynll__ztei = {}
    exec(kdfo__gyn, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__eval_res':
        udf_func_struct.eval_all_func, 'is_null_pointer': is_null_pointer,
        'dt64_dtype': np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, uynll__ztei)
    return uynll__ztei['bodo_gb_udf_eval{}'.format(label_suffix)]


def gen_general_udf_cb(udf_func_struct, allfuncs, n_keys, in_col_typs,
    out_col_typs, func_idx_to_in_col, label_suffix):
    gggzu__uwcy = n_keys
    mjn__dza = []
    for i, ovfec__tcq in enumerate(allfuncs):
        if ovfec__tcq.ftype == 'gen_udf':
            mjn__dza.append(gggzu__uwcy)
            gggzu__uwcy += 1
        elif ovfec__tcq.ftype != 'udf':
            gggzu__uwcy += ovfec__tcq.ncols_post_shuffle
        else:
            gggzu__uwcy += ovfec__tcq.n_redvars + 1
    kdfo__gyn = (
        'def bodo_gb_apply_general_udfs{}(num_groups, in_table, out_table):\n'
        .format(label_suffix))
    kdfo__gyn += '    if num_groups == 0:\n'
    kdfo__gyn += '        return\n'
    for i, func in enumerate(udf_func_struct.general_udf_funcs):
        kdfo__gyn += '    # col {}\n'.format(i)
        kdfo__gyn += (
            """    out_col = info_to_array(info_from_table(out_table, {}), out_col_{}_typ)
"""
            .format(mjn__dza[i], i))
        kdfo__gyn += '    incref(out_col)\n'
        kdfo__gyn += '    for j in range(num_groups):\n'
        kdfo__gyn += (
            """        in_col = info_to_array(info_from_table(in_table, {}*num_groups + j), in_col_{}_typ)
"""
            .format(i, i))
        kdfo__gyn += '        incref(in_col)\n'
        kdfo__gyn += (
            '        out_col[j] = func_{}(pd.Series(in_col))  # func returns scalar\n'
            .format(i))
    hjrv__frna = {'pd': pd, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref}
    tztim__yti = 0
    for i, func in enumerate(allfuncs):
        if func.ftype != 'gen_udf':
            continue
        func = udf_func_struct.general_udf_funcs[tztim__yti]
        hjrv__frna['func_{}'.format(tztim__yti)] = func
        hjrv__frna['in_col_{}_typ'.format(tztim__yti)] = in_col_typs[
            func_idx_to_in_col[i]]
        hjrv__frna['out_col_{}_typ'.format(tztim__yti)] = out_col_typs[i]
        tztim__yti += 1
    uynll__ztei = {}
    exec(kdfo__gyn, hjrv__frna, uynll__ztei)
    ovfec__tcq = uynll__ztei['bodo_gb_apply_general_udfs{}'.format(
        label_suffix)]
    ihid__dcz = types.void(types.int64, types.voidptr, types.voidptr)
    return numba.cfunc(ihid__dcz, nopython=True)(ovfec__tcq)


def gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs, parallel,
    udf_func_struct):
    hgd__rpfd = agg_node.pivot_arr is not None
    if agg_node.same_index:
        assert agg_node.input_has_index
    if agg_node.pivot_values is None:
        wmoi__lge = 1
    else:
        wmoi__lge = len(agg_node.pivot_values)
    sqtpi__thn = tuple('key_' + sanitize_varname(apgz__iqlaq) for
        apgz__iqlaq in agg_node.key_names)
    lzkgy__khso = {apgz__iqlaq: 'in_{}'.format(sanitize_varname(apgz__iqlaq
        )) for apgz__iqlaq in agg_node.gb_info_in.keys() if apgz__iqlaq is not
        None}
    yfxh__xei = {apgz__iqlaq: ('out_' + sanitize_varname(apgz__iqlaq)) for
        apgz__iqlaq in agg_node.gb_info_out.keys()}
    n_keys = len(agg_node.key_names)
    avj__lgqzv = ', '.join(sqtpi__thn)
    mua__jcx = ', '.join(lzkgy__khso.values())
    if mua__jcx != '':
        mua__jcx = ', ' + mua__jcx
    kdfo__gyn = 'def agg_top({}{}{}, pivot_arr):\n'.format(avj__lgqzv,
        mua__jcx, ', index_arg' if agg_node.input_has_index else '')
    if hgd__rpfd:
        zbt__gjghs = []
        for xaubt__npsqu, xcfv__nuemh in agg_node.gb_info_in.items():
            if xaubt__npsqu is not None:
                for func, frzv__bmon in xcfv__nuemh:
                    zbt__gjghs.append(lzkgy__khso[xaubt__npsqu])
    else:
        zbt__gjghs = tuple(lzkgy__khso[xaubt__npsqu] for xaubt__npsqu,
            frzv__bmon in agg_node.gb_info_out.values() if xaubt__npsqu is not
            None)
    wbcb__xpcr = sqtpi__thn + tuple(zbt__gjghs)
    kdfo__gyn += '    info_list = [{}{}{}]\n'.format(', '.join(
        'array_to_info({})'.format(a) for a in wbcb__xpcr), 
        ', array_to_info(index_arg)' if agg_node.input_has_index else '', 
        ', array_to_info(pivot_arr)' if agg_node.is_crosstab else '')
    kdfo__gyn += '    table = arr_info_list_to_table(info_list)\n'
    for i, apgz__iqlaq in enumerate(agg_node.gb_info_out.keys()):
        lmem__rmcry = yfxh__xei[apgz__iqlaq] + '_dummy'
        axtt__yxkrw = out_col_typs[i]
        xaubt__npsqu, func = agg_node.gb_info_out[apgz__iqlaq]
        if isinstance(func, pytypes.SimpleNamespace) and func.fname in ['min',
            'max', 'shift'] and isinstance(axtt__yxkrw, bodo.
            CategoricalArrayType):
            kdfo__gyn += '    {} = {}\n'.format(lmem__rmcry, lzkgy__khso[
                xaubt__npsqu])
        else:
            kdfo__gyn += '    {} = {}\n'.format(lmem__rmcry,
                _gen_dummy_alloc(axtt__yxkrw, i, False))
    do_combine = parallel
    allfuncs = []
    dsbi__frd = []
    func_idx_to_in_col = []
    qgby__ukilu = []
    zgys__vpdtc = False
    mcb__iyjjq = 1
    sqtmo__tmidv = 0
    oqi__sje = 0
    if not hgd__rpfd:
        sttj__dmnk = [func for frzv__bmon, func in agg_node.gb_info_out.
            values()]
    else:
        sttj__dmnk = [func for func, frzv__bmon in xcfv__nuemh for
            xcfv__nuemh in agg_node.gb_info_in.values()]
    for lwh__fhuf, func in enumerate(sttj__dmnk):
        dsbi__frd.append(len(allfuncs))
        if func.ftype in {'median', 'nunique'}:
            do_combine = False
        if func.ftype in list_cumulative:
            sqtmo__tmidv += 1
        if hasattr(func, 'skipdropna'):
            zgys__vpdtc = func.skipdropna
        if func.ftype == 'shift':
            mcb__iyjjq = func.periods
            do_combine = False
        if func.ftype in {'transform'}:
            oqi__sje = func.transform_func
            do_combine = False
        allfuncs.append(func)
        func_idx_to_in_col.append(lwh__fhuf)
        if func.ftype == 'udf':
            qgby__ukilu.append(func.n_redvars)
        elif func.ftype == 'gen_udf':
            qgby__ukilu.append(0)
            do_combine = False
    dsbi__frd.append(len(allfuncs))
    if agg_node.is_crosstab:
        assert len(agg_node.gb_info_out
            ) == wmoi__lge, 'invalid number of groupby outputs for pivot'
    else:
        assert len(agg_node.gb_info_out) == len(allfuncs
            ) * wmoi__lge, 'invalid number of groupby outputs'
    if sqtmo__tmidv > 0:
        if sqtmo__tmidv != len(allfuncs):
            raise BodoError(
                f'{agg_node.func_name}(): Cannot mix cumulative operations with other aggregation functions'
                , loc=agg_node.loc)
        do_combine = False
    if udf_func_struct is not None:
        atgej__ffprj = next_label()
        if udf_func_struct.regular_udfs:
            ihid__dcz = types.void(types.voidptr, types.voidptr, types.
                CPointer(types.int64))
            tmk__nesu = numba.cfunc(ihid__dcz, nopython=True)(gen_update_cb
                (udf_func_struct, allfuncs, n_keys, in_col_typs,
                out_col_typs, do_combine, func_idx_to_in_col, atgej__ffprj))
            hpznm__dgjw = numba.cfunc(ihid__dcz, nopython=True)(gen_combine_cb
                (udf_func_struct, allfuncs, n_keys, out_col_typs, atgej__ffprj)
                )
            gqcx__nnph = numba.cfunc('void(voidptr)', nopython=True)(
                gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_col_typs,
                atgej__ffprj))
            udf_func_struct.set_regular_cfuncs(tmk__nesu, hpznm__dgjw,
                gqcx__nnph)
            for jnfqy__oykc in udf_func_struct.regular_udf_cfuncs:
                gb_agg_cfunc[jnfqy__oykc.native_name] = jnfqy__oykc
                gb_agg_cfunc_addr[jnfqy__oykc.native_name
                    ] = jnfqy__oykc.address
        if udf_func_struct.general_udfs:
            iha__ygp = gen_general_udf_cb(udf_func_struct, allfuncs, n_keys,
                in_col_typs, out_col_typs, func_idx_to_in_col, atgej__ffprj)
            udf_func_struct.set_general_cfunc(iha__ygp)
        biy__dek = []
        jck__npiqy = 0
        i = 0
        for lmem__rmcry, ovfec__tcq in zip(yfxh__xei.values(), allfuncs):
            if ovfec__tcq.ftype in ('udf', 'gen_udf'):
                biy__dek.append(lmem__rmcry + '_dummy')
                for gcnvl__elme in range(jck__npiqy, jck__npiqy +
                    qgby__ukilu[i]):
                    biy__dek.append('data_redvar_dummy_' + str(gcnvl__elme))
                jck__npiqy += qgby__ukilu[i]
                i += 1
        if udf_func_struct.regular_udfs:
            xlfs__dmxa = udf_func_struct.var_typs
            for i, t in enumerate(xlfs__dmxa):
                kdfo__gyn += ('    data_redvar_dummy_{} = np.empty(1, {})\n'
                    .format(i, _get_np_dtype(t)))
        kdfo__gyn += '    out_info_list_dummy = [{}]\n'.format(', '.join(
            'array_to_info({})'.format(a) for a in biy__dek))
        kdfo__gyn += (
            '    udf_table_dummy = arr_info_list_to_table(out_info_list_dummy)\n'
            )
        if udf_func_struct.regular_udfs:
            kdfo__gyn += "    add_agg_cfunc_sym(cpp_cb_update, '{}')\n".format(
                tmk__nesu.native_name)
            kdfo__gyn += ("    add_agg_cfunc_sym(cpp_cb_combine, '{}')\n".
                format(hpznm__dgjw.native_name))
            kdfo__gyn += "    add_agg_cfunc_sym(cpp_cb_eval, '{}')\n".format(
                gqcx__nnph.native_name)
            kdfo__gyn += ("    cpp_cb_update_addr = get_agg_udf_addr('{}')\n"
                .format(tmk__nesu.native_name))
            kdfo__gyn += ("    cpp_cb_combine_addr = get_agg_udf_addr('{}')\n"
                .format(hpznm__dgjw.native_name))
            kdfo__gyn += ("    cpp_cb_eval_addr = get_agg_udf_addr('{}')\n"
                .format(gqcx__nnph.native_name))
        else:
            kdfo__gyn += '    cpp_cb_update_addr = 0\n'
            kdfo__gyn += '    cpp_cb_combine_addr = 0\n'
            kdfo__gyn += '    cpp_cb_eval_addr = 0\n'
        if udf_func_struct.general_udfs:
            jnfqy__oykc = udf_func_struct.general_udf_cfunc
            gb_agg_cfunc[jnfqy__oykc.native_name] = jnfqy__oykc
            gb_agg_cfunc_addr[jnfqy__oykc.native_name] = jnfqy__oykc.address
            kdfo__gyn += ("    add_agg_cfunc_sym(cpp_cb_general, '{}')\n".
                format(jnfqy__oykc.native_name))
            kdfo__gyn += ("    cpp_cb_general_addr = get_agg_udf_addr('{}')\n"
                .format(jnfqy__oykc.native_name))
        else:
            kdfo__gyn += '    cpp_cb_general_addr = 0\n'
    else:
        kdfo__gyn += (
            '    udf_table_dummy = arr_info_list_to_table([array_to_info(np.empty(1))])\n'
            )
        kdfo__gyn += '    cpp_cb_update_addr = 0\n'
        kdfo__gyn += '    cpp_cb_combine_addr = 0\n'
        kdfo__gyn += '    cpp_cb_eval_addr = 0\n'
        kdfo__gyn += '    cpp_cb_general_addr = 0\n'
    kdfo__gyn += '    ftypes = np.array([{}, 0], dtype=np.int32)\n'.format(', '
        .join([str(supported_agg_funcs.index(ovfec__tcq.ftype)) for
        ovfec__tcq in allfuncs] + ['0']))
    kdfo__gyn += '    func_offsets = np.array({}, dtype=np.int32)\n'.format(str
        (dsbi__frd))
    if len(qgby__ukilu) > 0:
        kdfo__gyn += '    udf_ncols = np.array({}, dtype=np.int32)\n'.format(
            str(qgby__ukilu))
    else:
        kdfo__gyn += '    udf_ncols = np.array([0], np.int32)\n'
    if hgd__rpfd:
        kdfo__gyn += '    arr_type = coerce_to_array({})\n'.format(agg_node
            .pivot_values)
        kdfo__gyn += '    arr_info = array_to_info(arr_type)\n'
        kdfo__gyn += (
            '    dispatch_table = arr_info_list_to_table([arr_info])\n')
        kdfo__gyn += '    pivot_info = array_to_info(pivot_arr)\n'
        kdfo__gyn += (
            '    dispatch_info = arr_info_list_to_table([pivot_info])\n')
        kdfo__gyn += (
            """    out_table = pivot_groupby_and_aggregate(table, {}, dispatch_table, dispatch_info, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel, agg_node.
            is_crosstab, zgys__vpdtc, agg_node.return_key, agg_node.same_index)
            )
        kdfo__gyn += '    delete_info_decref_array(pivot_info)\n'
        kdfo__gyn += '    delete_info_decref_array(arr_info)\n'
    else:
        kdfo__gyn += (
            """    out_table = groupby_and_aggregate(table, {}, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, cpp_cb_general_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel, zgys__vpdtc,
            mcb__iyjjq, oqi__sje, agg_node.return_key, agg_node.same_index,
            agg_node.dropna))
    abre__reuwu = 0
    if agg_node.return_key:
        for i, bjq__ujd in enumerate(sqtpi__thn):
            kdfo__gyn += (
                '    {} = info_to_array(info_from_table(out_table, {}), {})\n'
                .format(bjq__ujd, abre__reuwu, bjq__ujd))
            abre__reuwu += 1
    for lmem__rmcry in yfxh__xei.values():
        kdfo__gyn += (
            '    {} = info_to_array(info_from_table(out_table, {}), {})\n'.
            format(lmem__rmcry, abre__reuwu, lmem__rmcry + '_dummy'))
        abre__reuwu += 1
    if agg_node.same_index:
        kdfo__gyn += (
            """    out_index_arg = info_to_array(info_from_table(out_table, {}), index_arg)
"""
            .format(abre__reuwu))
        abre__reuwu += 1
    kdfo__gyn += (
        f"    ev_clean = bodo.utils.tracing.Event('tables_clean_up', {parallel})\n"
        )
    kdfo__gyn += '    delete_table_decref_arrays(table)\n'
    kdfo__gyn += '    delete_table_decref_arrays(udf_table_dummy)\n'
    kdfo__gyn += '    delete_table(out_table)\n'
    kdfo__gyn += f'    ev_clean.finalize()\n'
    mrl__xxmev = tuple(yfxh__xei.values())
    if agg_node.return_key:
        mrl__xxmev += tuple(sqtpi__thn)
    kdfo__gyn += '    return ({},{})\n'.format(', '.join(mrl__xxmev), 
        ' out_index_arg,' if agg_node.same_index else '')
    uynll__ztei = {}
    exec(kdfo__gyn, {}, uynll__ztei)
    psft__yzn = uynll__ztei['agg_top']
    return psft__yzn


def compile_to_optimized_ir(func, arg_typs, typingctx, targetctx):
    code = func.code if hasattr(func, 'code') else func.__code__
    closure = func.closure if hasattr(func, 'closure') else func.__closure__
    f_ir = get_ir_of_code(func.__globals__, code)
    replace_closures(f_ir, closure, code)
    for block in f_ir.blocks.values():
        for prz__cde in block.body:
            if is_call_assign(prz__cde) and find_callname(f_ir, prz__cde.value
                ) == ('len', 'builtins') and prz__cde.value.args[0
                ].name == f_ir.arg_names[0]:
                sxgs__zttdf = get_definition(f_ir, prz__cde.value.func)
                sxgs__zttdf.name = 'dummy_agg_count'
                sxgs__zttdf.value = dummy_agg_count
    yfic__pmnot = get_name_var_table(f_ir.blocks)
    gmdvz__fponr = {}
    for name, frzv__bmon in yfic__pmnot.items():
        gmdvz__fponr[name] = mk_unique_var(name)
    replace_var_names(f_ir.blocks, gmdvz__fponr)
    f_ir._definitions = build_definitions(f_ir.blocks)
    assert f_ir.arg_count == 1, 'agg function should have one input'
    pys__pyq = numba.core.compiler.Flags()
    pys__pyq.nrt = True
    yheeh__orvw = bodo.transforms.untyped_pass.UntypedPass(f_ir, typingctx,
        arg_typs, {}, {}, pys__pyq)
    yheeh__orvw.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    typemap, fiwe__nuc, calltypes, frzv__bmon = (numba.core.typed_passes.
        type_inference_stage(typingctx, targetctx, f_ir, arg_typs, None))
    mbe__ymfqd = numba.core.cpu.ParallelOptions(True)
    targetctx = numba.core.cpu.CPUContext(typingctx)
    dgonj__ovsn = namedtuple('DummyPipeline', ['typingctx', 'targetctx',
        'args', 'func_ir', 'typemap', 'return_type', 'calltypes',
        'type_annotation', 'locals', 'flags', 'pipeline'])
    evgjf__dflm = namedtuple('TypeAnnotation', ['typemap', 'calltypes'])
    agtpt__vpds = evgjf__dflm(typemap, calltypes)
    pm = dgonj__ovsn(typingctx, targetctx, None, f_ir, typemap, fiwe__nuc,
        calltypes, agtpt__vpds, {}, pys__pyq, None)
    gybgq__tfwqt = (numba.core.compiler.DefaultPassBuilder.
        define_untyped_pipeline(pm))
    pm = dgonj__ovsn(typingctx, targetctx, None, f_ir, typemap, fiwe__nuc,
        calltypes, agtpt__vpds, {}, pys__pyq, gybgq__tfwqt)
    cfvx__zulz = numba.core.typed_passes.InlineOverloads()
    cfvx__zulz.run_pass(pm)
    kzixx__gouv = bodo.transforms.series_pass.SeriesPass(f_ir, typingctx,
        targetctx, typemap, calltypes, {}, False)
    kzixx__gouv.run()
    for block in f_ir.blocks.values():
        for prz__cde in block.body:
            if is_assign(prz__cde) and isinstance(prz__cde.value, (ir.Arg,
                ir.Var)) and isinstance(typemap[prz__cde.target.name],
                SeriesType):
                rcir__cgw = typemap.pop(prz__cde.target.name)
                typemap[prz__cde.target.name] = rcir__cgw.data
            if is_call_assign(prz__cde) and find_callname(f_ir, prz__cde.value
                ) == ('get_series_data', 'bodo.hiframes.pd_series_ext'):
                f_ir._definitions[prz__cde.target.name].remove(prz__cde.value)
                prz__cde.value = prz__cde.value.args[0]
                f_ir._definitions[prz__cde.target.name].append(prz__cde.value)
            if is_call_assign(prz__cde) and find_callname(f_ir, prz__cde.value
                ) == ('isna', 'bodo.libs.array_kernels'):
                f_ir._definitions[prz__cde.target.name].remove(prz__cde.value)
                prz__cde.value = ir.Const(False, prz__cde.loc)
                f_ir._definitions[prz__cde.target.name].append(prz__cde.value)
            if is_call_assign(prz__cde) and find_callname(f_ir, prz__cde.value
                ) == ('setna', 'bodo.libs.array_kernels'):
                f_ir._definitions[prz__cde.target.name].remove(prz__cde.value)
                prz__cde.value = ir.Const(False, prz__cde.loc)
                f_ir._definitions[prz__cde.target.name].append(prz__cde.value)
    bodo.transforms.untyped_pass.remove_dead_branches(f_ir)
    khuc__hvq = numba.parfors.parfor.PreParforPass(f_ir, typemap, calltypes,
        typingctx, targetctx, mbe__ymfqd)
    khuc__hvq.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    rmtm__cweeg = numba.core.compiler.StateDict()
    rmtm__cweeg.func_ir = f_ir
    rmtm__cweeg.typemap = typemap
    rmtm__cweeg.calltypes = calltypes
    rmtm__cweeg.typingctx = typingctx
    rmtm__cweeg.targetctx = targetctx
    rmtm__cweeg.return_type = fiwe__nuc
    numba.core.rewrites.rewrite_registry.apply('after-inference', rmtm__cweeg)
    xsijm__wtbom = numba.parfors.parfor.ParforPass(f_ir, typemap, calltypes,
        fiwe__nuc, typingctx, targetctx, mbe__ymfqd, pys__pyq, {})
    xsijm__wtbom.run()
    remove_dels(f_ir.blocks)
    numba.parfors.parfor.maximize_fusion(f_ir, f_ir.blocks, typemap, False)
    return f_ir, pm


def replace_closures(f_ir, closure, code):
    if closure:
        closure = f_ir.get_definition(closure)
        if isinstance(closure, tuple):
            fudl__jtrz = ctypes.pythonapi.PyCell_Get
            fudl__jtrz.restype = ctypes.py_object
            fudl__jtrz.argtypes = ctypes.py_object,
            tbkim__pah = tuple(fudl__jtrz(rrvn__ajoay) for rrvn__ajoay in
                closure)
        else:
            assert isinstance(closure, ir.Expr) and closure.op == 'build_tuple'
            tbkim__pah = closure.items
        assert len(code.co_freevars) == len(tbkim__pah)
        numba.core.inline_closurecall._replace_freevars(f_ir.blocks, tbkim__pah
            )


class RegularUDFGenerator(object):

    def __init__(self, in_col_types, out_col_types, pivot_typ, pivot_values,
        is_crosstab, typingctx, targetctx):
        self.in_col_types = in_col_types
        self.out_col_types = out_col_types
        self.pivot_typ = pivot_typ
        self.pivot_values = pivot_values
        self.is_crosstab = is_crosstab
        self.typingctx = typingctx
        self.targetctx = targetctx
        self.all_reduce_vars = []
        self.all_vartypes = []
        self.all_init_nodes = []
        self.all_eval_funcs = []
        self.all_update_funcs = []
        self.all_combine_funcs = []
        self.curr_offset = 0
        self.redvar_offsets = [0]

    def add_udf(self, in_col_typ, func):
        bobc__grmyr = SeriesType(in_col_typ.dtype, in_col_typ, None,
            string_type)
        f_ir, pm = compile_to_optimized_ir(func, (bobc__grmyr,), self.
            typingctx, self.targetctx)
        f_ir._definitions = build_definitions(f_ir.blocks)
        assert len(f_ir.blocks
            ) == 1 and 0 in f_ir.blocks, 'only simple functions with one block supported for aggregation'
        block = f_ir.blocks[0]
        pmjs__gvedi, arr_var = _rm_arg_agg_block(block, pm.typemap)
        yti__sll = -1
        for i, prz__cde in enumerate(pmjs__gvedi):
            if isinstance(prz__cde, numba.parfors.parfor.Parfor):
                assert yti__sll == -1, 'only one parfor for aggregation function'
                yti__sll = i
        parfor = None
        if yti__sll != -1:
            parfor = pmjs__gvedi[yti__sll]
            remove_dels(parfor.loop_body)
            remove_dels({(0): parfor.init_block})
        init_nodes = []
        if parfor:
            init_nodes = pmjs__gvedi[:yti__sll] + parfor.init_block.body
        eval_nodes = pmjs__gvedi[yti__sll + 1:]
        redvars = []
        var_to_redvar = {}
        if parfor:
            redvars, var_to_redvar = get_parfor_reductions(parfor, parfor.
                params, pm.calltypes)
        func.ncols_pre_shuffle = len(redvars)
        func.ncols_post_shuffle = len(redvars) + 1
        func.n_redvars = len(redvars)
        reduce_vars = [0] * len(redvars)
        for prz__cde in init_nodes:
            if is_assign(prz__cde) and prz__cde.target.name in redvars:
                ind = redvars.index(prz__cde.target.name)
                reduce_vars[ind] = prz__cde.target
        var_types = [pm.typemap[v] for v in redvars]
        ecs__gyky = gen_combine_func(f_ir, parfor, redvars, var_to_redvar,
            var_types, arr_var, pm, self.typingctx, self.targetctx)
        init_nodes = _mv_read_only_init_vars(init_nodes, parfor, eval_nodes)
        xkxso__yowvf = gen_update_func(parfor, redvars, var_to_redvar,
            var_types, arr_var, in_col_typ, pm, self.typingctx, self.targetctx)
        qqu__tzuzw = gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types,
            pm, self.typingctx, self.targetctx)
        self.all_reduce_vars += reduce_vars
        self.all_vartypes += var_types
        self.all_init_nodes += init_nodes
        self.all_eval_funcs.append(qqu__tzuzw)
        self.all_update_funcs.append(xkxso__yowvf)
        self.all_combine_funcs.append(ecs__gyky)
        self.curr_offset += len(redvars)
        self.redvar_offsets.append(self.curr_offset)

    def gen_all_func(self):
        if len(self.all_update_funcs) == 0:
            return None
        self.all_vartypes = self.all_vartypes * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_vartypes
        self.all_reduce_vars = self.all_reduce_vars * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_reduce_vars
        plgj__qklo = gen_init_func(self.all_init_nodes, self.
            all_reduce_vars, self.all_vartypes, self.typingctx, self.targetctx)
        scu__wgqv = gen_all_update_func(self.all_update_funcs, self.
            all_vartypes, self.in_col_types, self.redvar_offsets, self.
            typingctx, self.targetctx, self.pivot_typ, self.pivot_values,
            self.is_crosstab)
        zvjdw__jkfu = gen_all_combine_func(self.all_combine_funcs, self.
            all_vartypes, self.redvar_offsets, self.typingctx, self.
            targetctx, self.pivot_typ, self.pivot_values)
        dph__jnr = gen_all_eval_func(self.all_eval_funcs, self.all_vartypes,
            self.redvar_offsets, self.out_col_types, self.typingctx, self.
            targetctx, self.pivot_values)
        return self.all_vartypes, plgj__qklo, scu__wgqv, zvjdw__jkfu, dph__jnr


class GeneralUDFGenerator(object):

    def __init__(self):
        self.funcs = []

    def add_udf(self, func):
        self.funcs.append(bodo.jit(distributed=False)(func))
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        func.n_redvars = 0

    def gen_all_func(self):
        if len(self.funcs) > 0:
            return self.funcs
        else:
            return None


def get_udf_func_struct(agg_func, input_has_index, in_col_types,
    out_col_types, typingctx, targetctx, pivot_typ, pivot_values, is_crosstab):
    if is_crosstab and len(in_col_types) == 0:
        in_col_types = [types.Array(types.intp, 1, 'C')]
    kau__quvi = []
    for t, ovfec__tcq in zip(in_col_types, agg_func):
        kau__quvi.append((t, ovfec__tcq))
    xkc__oue = RegularUDFGenerator(in_col_types, out_col_types, pivot_typ,
        pivot_values, is_crosstab, typingctx, targetctx)
    xrrwo__aviia = GeneralUDFGenerator()
    for in_col_typ, func in kau__quvi:
        if func.ftype not in ('udf', 'gen_udf'):
            continue
        try:
            xkc__oue.add_udf(in_col_typ, func)
        except:
            xrrwo__aviia.add_udf(func)
            func.ftype = 'gen_udf'
    regular_udf_funcs = xkc__oue.gen_all_func()
    general_udf_funcs = xrrwo__aviia.gen_all_func()
    if regular_udf_funcs is not None or general_udf_funcs is not None:
        return AggUDFStruct(regular_udf_funcs, general_udf_funcs)
    else:
        return None


def _mv_read_only_init_vars(init_nodes, parfor, eval_nodes):
    if not parfor:
        return init_nodes
    ljul__hts = compute_use_defs(parfor.loop_body)
    ypfd__yyr = set()
    for kusj__ufhd in ljul__hts.usemap.values():
        ypfd__yyr |= kusj__ufhd
    aofl__fhim = set()
    for kusj__ufhd in ljul__hts.defmap.values():
        aofl__fhim |= kusj__ufhd
    amqvf__ydjhz = ir.Block(ir.Scope(None, parfor.loc), parfor.loc)
    amqvf__ydjhz.body = eval_nodes
    xymtf__jdkud = compute_use_defs({(0): amqvf__ydjhz})
    zad__sit = xymtf__jdkud.usemap[0]
    ohcw__mzm = set()
    eyjr__dvjl = []
    gmbh__jac = []
    for prz__cde in reversed(init_nodes):
        gxi__brtmk = {v.name for v in prz__cde.list_vars()}
        if is_assign(prz__cde):
            v = prz__cde.target.name
            gxi__brtmk.remove(v)
            if (v in ypfd__yyr and v not in ohcw__mzm and v not in zad__sit and
                v not in aofl__fhim):
                gmbh__jac.append(prz__cde)
                ypfd__yyr |= gxi__brtmk
                aofl__fhim.add(v)
                continue
        ohcw__mzm |= gxi__brtmk
        eyjr__dvjl.append(prz__cde)
    gmbh__jac.reverse()
    eyjr__dvjl.reverse()
    nzx__qdsp = min(parfor.loop_body.keys())
    lnrua__ynanf = parfor.loop_body[nzx__qdsp]
    lnrua__ynanf.body = gmbh__jac + lnrua__ynanf.body
    return eyjr__dvjl


def gen_init_func(init_nodes, reduce_vars, var_types, typingctx, targetctx):
    wtwld__fdep = (numba.parfors.parfor.max_checker, numba.parfors.parfor.
        min_checker, numba.parfors.parfor.argmax_checker, numba.parfors.
        parfor.argmin_checker)
    wjptj__qcnh = set()
    vali__xbl = []
    for prz__cde in init_nodes:
        if is_assign(prz__cde) and isinstance(prz__cde.value, ir.Global
            ) and isinstance(prz__cde.value.value, pytypes.FunctionType
            ) and prz__cde.value.value in wtwld__fdep:
            wjptj__qcnh.add(prz__cde.target.name)
        elif is_call_assign(prz__cde
            ) and prz__cde.value.func.name in wjptj__qcnh:
            pass
        else:
            vali__xbl.append(prz__cde)
    init_nodes = vali__xbl
    hjxsd__ppm = types.Tuple(var_types)
    kmw__ghe = lambda : None
    f_ir = compile_to_numba_ir(kmw__ghe, {})
    block = list(f_ir.blocks.values())[0]
    loc = block.loc
    txqhw__heanx = ir.Var(block.scope, mk_unique_var('init_tup'), loc)
    ypbc__obom = ir.Assign(ir.Expr.build_tuple(reduce_vars, loc),
        txqhw__heanx, loc)
    block.body = block.body[-2:]
    block.body = init_nodes + [ypbc__obom] + block.body
    block.body[-2].value.value = txqhw__heanx
    vhd__yafn = compiler.compile_ir(typingctx, targetctx, f_ir, (),
        hjxsd__ppm, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    nouke__gvcm = numba.core.target_extension.dispatcher_registry[cpu_target](
        kmw__ghe)
    nouke__gvcm.add_overload(vhd__yafn)
    return nouke__gvcm


def gen_all_update_func(update_funcs, reduce_var_types, in_col_types,
    redvar_offsets, typingctx, targetctx, pivot_typ, pivot_values, is_crosstab
    ):
    ndoku__jxayz = len(update_funcs)
    sqz__jlk = len(in_col_types)
    if pivot_values is not None:
        assert sqz__jlk == 1
    kdfo__gyn = (
        'def update_all_f(redvar_arrs, data_in, w_ind, i, pivot_arr):\n')
    if pivot_values is not None:
        gcwyr__ajin = redvar_offsets[sqz__jlk]
        kdfo__gyn += '  pv = pivot_arr[i]\n'
        for gcnvl__elme, nln__jfyd in enumerate(pivot_values):
            ixld__vat = 'el' if gcnvl__elme != 0 else ''
            kdfo__gyn += "  {}if pv == '{}':\n".format(ixld__vat, nln__jfyd)
            ibw__dyy = gcwyr__ajin * gcnvl__elme
            mpnei__geyao = ', '.join(['redvar_arrs[{}][w_ind]'.format(i) for
                i in range(ibw__dyy + redvar_offsets[0], ibw__dyy +
                redvar_offsets[1])])
            zphfs__okaa = 'data_in[0][i]'
            if is_crosstab:
                zphfs__okaa = '0'
            kdfo__gyn += '    {} = update_vars_0({}, {})\n'.format(mpnei__geyao
                , mpnei__geyao, zphfs__okaa)
    else:
        for gcnvl__elme in range(ndoku__jxayz):
            mpnei__geyao = ', '.join(['redvar_arrs[{}][w_ind]'.format(i) for
                i in range(redvar_offsets[gcnvl__elme], redvar_offsets[
                gcnvl__elme + 1])])
            if mpnei__geyao:
                kdfo__gyn += ('  {} = update_vars_{}({},  data_in[{}][i])\n'
                    .format(mpnei__geyao, gcnvl__elme, mpnei__geyao, 0 if 
                    sqz__jlk == 1 else gcnvl__elme))
    kdfo__gyn += '  return\n'
    hjrv__frna = {}
    for i, ovfec__tcq in enumerate(update_funcs):
        hjrv__frna['update_vars_{}'.format(i)] = ovfec__tcq
    uynll__ztei = {}
    exec(kdfo__gyn, hjrv__frna, uynll__ztei)
    elqj__ybtrw = uynll__ztei['update_all_f']
    return numba.njit(no_cpython_wrapper=True)(elqj__ybtrw)


def gen_all_combine_func(combine_funcs, reduce_var_types, redvar_offsets,
    typingctx, targetctx, pivot_typ, pivot_values):
    qvmqy__kov = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types]
        )
    arg_typs = qvmqy__kov, qvmqy__kov, types.intp, types.intp, pivot_typ
    yfulq__yfcad = len(redvar_offsets) - 1
    gcwyr__ajin = redvar_offsets[yfulq__yfcad]
    kdfo__gyn = (
        'def combine_all_f(redvar_arrs, recv_arrs, w_ind, i, pivot_arr):\n')
    if pivot_values is not None:
        assert yfulq__yfcad == 1
        for tndsy__lay in range(len(pivot_values)):
            ibw__dyy = gcwyr__ajin * tndsy__lay
            mpnei__geyao = ', '.join(['redvar_arrs[{}][w_ind]'.format(i) for
                i in range(ibw__dyy + redvar_offsets[0], ibw__dyy +
                redvar_offsets[1])])
            jfl__uuly = ', '.join(['recv_arrs[{}][i]'.format(i) for i in
                range(ibw__dyy + redvar_offsets[0], ibw__dyy +
                redvar_offsets[1])])
            kdfo__gyn += '  {} = combine_vars_0({}, {})\n'.format(mpnei__geyao,
                mpnei__geyao, jfl__uuly)
    else:
        for gcnvl__elme in range(yfulq__yfcad):
            mpnei__geyao = ', '.join(['redvar_arrs[{}][w_ind]'.format(i) for
                i in range(redvar_offsets[gcnvl__elme], redvar_offsets[
                gcnvl__elme + 1])])
            jfl__uuly = ', '.join(['recv_arrs[{}][i]'.format(i) for i in
                range(redvar_offsets[gcnvl__elme], redvar_offsets[
                gcnvl__elme + 1])])
            if jfl__uuly:
                kdfo__gyn += '  {} = combine_vars_{}({}, {})\n'.format(
                    mpnei__geyao, gcnvl__elme, mpnei__geyao, jfl__uuly)
    kdfo__gyn += '  return\n'
    hjrv__frna = {}
    for i, ovfec__tcq in enumerate(combine_funcs):
        hjrv__frna['combine_vars_{}'.format(i)] = ovfec__tcq
    uynll__ztei = {}
    exec(kdfo__gyn, hjrv__frna, uynll__ztei)
    jngjz__oiqcn = uynll__ztei['combine_all_f']
    f_ir = compile_to_numba_ir(jngjz__oiqcn, hjrv__frna)
    zvjdw__jkfu = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        types.none, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    nouke__gvcm = numba.core.target_extension.dispatcher_registry[cpu_target](
        jngjz__oiqcn)
    nouke__gvcm.add_overload(zvjdw__jkfu)
    return nouke__gvcm


def gen_all_eval_func(eval_funcs, reduce_var_types, redvar_offsets,
    out_col_typs, typingctx, targetctx, pivot_values):
    qvmqy__kov = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types]
        )
    out_col_typs = types.Tuple(out_col_typs)
    yfulq__yfcad = len(redvar_offsets) - 1
    gcwyr__ajin = redvar_offsets[yfulq__yfcad]
    kdfo__gyn = 'def eval_all_f(redvar_arrs, out_arrs, j):\n'
    if pivot_values is not None:
        assert yfulq__yfcad == 1
        for gcnvl__elme in range(len(pivot_values)):
            ibw__dyy = gcwyr__ajin * gcnvl__elme
            mpnei__geyao = ', '.join(['redvar_arrs[{}][j]'.format(i) for i in
                range(ibw__dyy + redvar_offsets[0], ibw__dyy +
                redvar_offsets[1])])
            kdfo__gyn += '  out_arrs[{}][j] = eval_vars_0({})\n'.format(
                gcnvl__elme, mpnei__geyao)
    else:
        for gcnvl__elme in range(yfulq__yfcad):
            mpnei__geyao = ', '.join(['redvar_arrs[{}][j]'.format(i) for i in
                range(redvar_offsets[gcnvl__elme], redvar_offsets[
                gcnvl__elme + 1])])
            kdfo__gyn += '  out_arrs[{}][j] = eval_vars_{}({})\n'.format(
                gcnvl__elme, gcnvl__elme, mpnei__geyao)
    kdfo__gyn += '  return\n'
    hjrv__frna = {}
    for i, ovfec__tcq in enumerate(eval_funcs):
        hjrv__frna['eval_vars_{}'.format(i)] = ovfec__tcq
    uynll__ztei = {}
    exec(kdfo__gyn, hjrv__frna, uynll__ztei)
    newr__npaxv = uynll__ztei['eval_all_f']
    return numba.njit(no_cpython_wrapper=True)(newr__npaxv)


def gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types, pm, typingctx,
    targetctx):
    fcpr__avzyu = len(var_types)
    med__fbz = [f'in{i}' for i in range(fcpr__avzyu)]
    hjxsd__ppm = types.unliteral(pm.typemap[eval_nodes[-1].value.name])
    vxrf__ejex = hjxsd__ppm(0)
    kdfo__gyn = 'def agg_eval({}):\n return _zero\n'.format(', '.join(med__fbz)
        )
    uynll__ztei = {}
    exec(kdfo__gyn, {'_zero': vxrf__ejex}, uynll__ztei)
    uqgmr__cmajl = uynll__ztei['agg_eval']
    arg_typs = tuple(var_types)
    f_ir = compile_to_numba_ir(uqgmr__cmajl, {'numba': numba, 'bodo': bodo,
        'np': np, '_zero': vxrf__ejex}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.
        calltypes)
    block = list(f_ir.blocks.values())[0]
    shwx__qot = []
    for i, v in enumerate(reduce_vars):
        shwx__qot.append(ir.Assign(block.body[i].target, v, v.loc))
        for ecrz__cgjj in v.versioned_names:
            shwx__qot.append(ir.Assign(v, ir.Var(v.scope, ecrz__cgjj, v.loc
                ), v.loc))
    block.body = block.body[:fcpr__avzyu] + shwx__qot + eval_nodes
    qqu__tzuzw = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        hjxsd__ppm, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    nouke__gvcm = numba.core.target_extension.dispatcher_registry[cpu_target](
        uqgmr__cmajl)
    nouke__gvcm.add_overload(qqu__tzuzw)
    return nouke__gvcm


def gen_combine_func(f_ir, parfor, redvars, var_to_redvar, var_types,
    arr_var, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda : ())
    fcpr__avzyu = len(redvars)
    xokpl__cay = [f'v{i}' for i in range(fcpr__avzyu)]
    med__fbz = [f'in{i}' for i in range(fcpr__avzyu)]
    kdfo__gyn = 'def agg_combine({}):\n'.format(', '.join(xokpl__cay +
        med__fbz))
    lmip__oiqq = wrap_parfor_blocks(parfor)
    hoa__oet = find_topo_order(lmip__oiqq)
    hoa__oet = hoa__oet[1:]
    unwrap_parfor_blocks(parfor)
    bxetr__lwkm = {}
    emqly__iiih = []
    for cjg__qvr in hoa__oet:
        jxuf__lac = parfor.loop_body[cjg__qvr]
        for prz__cde in jxuf__lac.body:
            if is_call_assign(prz__cde) and guard(find_callname, f_ir,
                prz__cde.value) == ('__special_combine', 'bodo.ir.aggregate'):
                args = prz__cde.value.args
                helds__gxlkf = []
                bymz__esuk = []
                for v in args[:-1]:
                    ind = redvars.index(v.name)
                    emqly__iiih.append(ind)
                    helds__gxlkf.append('v{}'.format(ind))
                    bymz__esuk.append('in{}'.format(ind))
                tdzu__jktkj = '__special_combine__{}'.format(len(bxetr__lwkm))
                kdfo__gyn += '    ({},) = {}({})\n'.format(', '.join(
                    helds__gxlkf), tdzu__jktkj, ', '.join(helds__gxlkf +
                    bymz__esuk))
                iqnbq__cuef = ir.Expr.call(args[-1], [], (), jxuf__lac.loc)
                jpwl__yiwc = guard(find_callname, f_ir, iqnbq__cuef)
                assert jpwl__yiwc == ('_var_combine', 'bodo.ir.aggregate')
                jpwl__yiwc = bodo.ir.aggregate._var_combine
                bxetr__lwkm[tdzu__jktkj] = jpwl__yiwc
            if is_assign(prz__cde) and prz__cde.target.name in redvars:
                etvj__pgvg = prz__cde.target.name
                ind = redvars.index(etvj__pgvg)
                if ind in emqly__iiih:
                    continue
                if len(f_ir._definitions[etvj__pgvg]) == 2:
                    var_def = f_ir._definitions[etvj__pgvg][0]
                    kdfo__gyn += _match_reduce_def(var_def, f_ir, ind)
                    var_def = f_ir._definitions[etvj__pgvg][1]
                    kdfo__gyn += _match_reduce_def(var_def, f_ir, ind)
    kdfo__gyn += '    return {}'.format(', '.join(['v{}'.format(i) for i in
        range(fcpr__avzyu)]))
    uynll__ztei = {}
    exec(kdfo__gyn, {}, uynll__ztei)
    oioi__lmfqz = uynll__ztei['agg_combine']
    arg_typs = tuple(2 * var_types)
    hjrv__frna = {'numba': numba, 'bodo': bodo, 'np': np}
    hjrv__frna.update(bxetr__lwkm)
    f_ir = compile_to_numba_ir(oioi__lmfqz, hjrv__frna, typingctx=typingctx,
        targetctx=targetctx, arg_typs=arg_typs, typemap=pm.typemap,
        calltypes=pm.calltypes)
    block = list(f_ir.blocks.values())[0]
    hjxsd__ppm = pm.typemap[block.body[-1].value.name]
    ecs__gyky = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        hjxsd__ppm, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    nouke__gvcm = numba.core.target_extension.dispatcher_registry[cpu_target](
        oioi__lmfqz)
    nouke__gvcm.add_overload(ecs__gyky)
    return nouke__gvcm


def _match_reduce_def(var_def, f_ir, ind):
    kdfo__gyn = ''
    while isinstance(var_def, ir.Var):
        var_def = guard(get_definition, f_ir, var_def)
    if isinstance(var_def, ir.Expr
        ) and var_def.op == 'inplace_binop' and var_def.fn in ('+=',
        operator.iadd):
        kdfo__gyn = '    v{} += in{}\n'.format(ind, ind)
    if isinstance(var_def, ir.Expr) and var_def.op == 'call':
        vijc__cjb = guard(find_callname, f_ir, var_def)
        if vijc__cjb == ('min', 'builtins'):
            kdfo__gyn = '    v{} = min(v{}, in{})\n'.format(ind, ind, ind)
        if vijc__cjb == ('max', 'builtins'):
            kdfo__gyn = '    v{} = max(v{}, in{})\n'.format(ind, ind, ind)
    return kdfo__gyn


def gen_update_func(parfor, redvars, var_to_redvar, var_types, arr_var,
    in_col_typ, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda A: ())
    fcpr__avzyu = len(redvars)
    luf__hyiy = 1
    ocwd__hnf = []
    for i in range(luf__hyiy):
        pwfk__qca = ir.Var(arr_var.scope, f'$input{i}', arr_var.loc)
        ocwd__hnf.append(pwfk__qca)
    uti__bvjg = parfor.loop_nests[0].index_variable
    nxy__chjy = [0] * fcpr__avzyu
    for jxuf__lac in parfor.loop_body.values():
        cxpbw__zmm = []
        for prz__cde in jxuf__lac.body:
            if is_var_assign(prz__cde
                ) and prz__cde.value.name == uti__bvjg.name:
                continue
            if is_getitem(prz__cde
                ) and prz__cde.value.value.name == arr_var.name:
                prz__cde.value = ocwd__hnf[0]
            if is_call_assign(prz__cde) and guard(find_callname, pm.func_ir,
                prz__cde.value) == ('isna', 'bodo.libs.array_kernels'
                ) and prz__cde.value.args[0].name == arr_var.name:
                prz__cde.value = ir.Const(False, prz__cde.target.loc)
            if is_assign(prz__cde) and prz__cde.target.name in redvars:
                ind = redvars.index(prz__cde.target.name)
                nxy__chjy[ind] = prz__cde.target
            cxpbw__zmm.append(prz__cde)
        jxuf__lac.body = cxpbw__zmm
    xokpl__cay = ['v{}'.format(i) for i in range(fcpr__avzyu)]
    med__fbz = ['in{}'.format(i) for i in range(luf__hyiy)]
    kdfo__gyn = 'def agg_update({}):\n'.format(', '.join(xokpl__cay + med__fbz)
        )
    kdfo__gyn += '    __update_redvars()\n'
    kdfo__gyn += '    return {}'.format(', '.join(['v{}'.format(i) for i in
        range(fcpr__avzyu)]))
    uynll__ztei = {}
    exec(kdfo__gyn, {}, uynll__ztei)
    irpey__tgf = uynll__ztei['agg_update']
    arg_typs = tuple(var_types + [in_col_typ.dtype] * luf__hyiy)
    f_ir = compile_to_numba_ir(irpey__tgf, {'__update_redvars':
        __update_redvars}, typingctx=typingctx, targetctx=targetctx,
        arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.calltypes)
    f_ir._definitions = build_definitions(f_ir.blocks)
    eozxx__ufaq = f_ir.blocks.popitem()[1].body
    hjxsd__ppm = pm.typemap[eozxx__ufaq[-1].value.name]
    lmip__oiqq = wrap_parfor_blocks(parfor)
    hoa__oet = find_topo_order(lmip__oiqq)
    hoa__oet = hoa__oet[1:]
    unwrap_parfor_blocks(parfor)
    f_ir.blocks = parfor.loop_body
    lnrua__ynanf = f_ir.blocks[hoa__oet[0]]
    cpo__yewe = f_ir.blocks[hoa__oet[-1]]
    bsl__jth = eozxx__ufaq[:fcpr__avzyu + luf__hyiy]
    if fcpr__avzyu > 1:
        hng__aofm = eozxx__ufaq[-3:]
        assert is_assign(hng__aofm[0]) and isinstance(hng__aofm[0].value,
            ir.Expr) and hng__aofm[0].value.op == 'build_tuple'
    else:
        hng__aofm = eozxx__ufaq[-2:]
    for i in range(fcpr__avzyu):
        dkrf__ghjx = eozxx__ufaq[i].target
        slik__qls = ir.Assign(dkrf__ghjx, nxy__chjy[i], dkrf__ghjx.loc)
        bsl__jth.append(slik__qls)
    for i in range(fcpr__avzyu, fcpr__avzyu + luf__hyiy):
        dkrf__ghjx = eozxx__ufaq[i].target
        slik__qls = ir.Assign(dkrf__ghjx, ocwd__hnf[i - fcpr__avzyu],
            dkrf__ghjx.loc)
        bsl__jth.append(slik__qls)
    lnrua__ynanf.body = bsl__jth + lnrua__ynanf.body
    dhehj__vcqi = []
    for i in range(fcpr__avzyu):
        dkrf__ghjx = eozxx__ufaq[i].target
        slik__qls = ir.Assign(nxy__chjy[i], dkrf__ghjx, dkrf__ghjx.loc)
        dhehj__vcqi.append(slik__qls)
    cpo__yewe.body += dhehj__vcqi + hng__aofm
    ofpvo__nht = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        hjxsd__ppm, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    nouke__gvcm = numba.core.target_extension.dispatcher_registry[cpu_target](
        irpey__tgf)
    nouke__gvcm.add_overload(ofpvo__nht)
    return nouke__gvcm


def _rm_arg_agg_block(block, typemap):
    pmjs__gvedi = []
    arr_var = None
    for i, prz__cde in enumerate(block.body):
        if is_assign(prz__cde) and isinstance(prz__cde.value, ir.Arg):
            arr_var = prz__cde.target
            xiclp__wecbp = typemap[arr_var.name]
            if not isinstance(xiclp__wecbp, types.ArrayCompatible):
                pmjs__gvedi += block.body[i + 1:]
                break
            nunql__xwyp = block.body[i + 1]
            assert is_assign(nunql__xwyp) and isinstance(nunql__xwyp.value,
                ir.Expr
                ) and nunql__xwyp.value.op == 'getattr' and nunql__xwyp.value.attr == 'shape' and nunql__xwyp.value.value.name == arr_var.name
            iobsq__cvde = nunql__xwyp.target
            hza__bugo = block.body[i + 2]
            assert is_assign(hza__bugo) and isinstance(hza__bugo.value, ir.Expr
                ) and hza__bugo.value.op == 'static_getitem' and hza__bugo.value.value.name == iobsq__cvde.name
            pmjs__gvedi += block.body[i + 3:]
            break
        pmjs__gvedi.append(prz__cde)
    return pmjs__gvedi, arr_var


def get_parfor_reductions(parfor, parfor_params, calltypes, reduce_varnames
    =None, param_uses=None, var_to_param=None):
    if reduce_varnames is None:
        reduce_varnames = []
    if param_uses is None:
        param_uses = defaultdict(list)
    if var_to_param is None:
        var_to_param = {}
    lmip__oiqq = wrap_parfor_blocks(parfor)
    hoa__oet = find_topo_order(lmip__oiqq)
    hoa__oet = hoa__oet[1:]
    unwrap_parfor_blocks(parfor)
    for cjg__qvr in reversed(hoa__oet):
        for prz__cde in reversed(parfor.loop_body[cjg__qvr].body):
            if isinstance(prz__cde, ir.Assign) and (prz__cde.target.name in
                parfor_params or prz__cde.target.name in var_to_param):
                zkvp__qxvi = prz__cde.target.name
                rhs = prz__cde.value
                xwuoi__xhk = (zkvp__qxvi if zkvp__qxvi in parfor_params else
                    var_to_param[zkvp__qxvi])
                vce__ubbr = []
                if isinstance(rhs, ir.Var):
                    vce__ubbr = [rhs.name]
                elif isinstance(rhs, ir.Expr):
                    vce__ubbr = [v.name for v in prz__cde.value.list_vars()]
                param_uses[xwuoi__xhk].extend(vce__ubbr)
                for v in vce__ubbr:
                    var_to_param[v] = xwuoi__xhk
            if isinstance(prz__cde, Parfor):
                get_parfor_reductions(prz__cde, parfor_params, calltypes,
                    reduce_varnames, param_uses, var_to_param)
    for bkrhu__eub, vce__ubbr in param_uses.items():
        if bkrhu__eub in vce__ubbr and bkrhu__eub not in reduce_varnames:
            reduce_varnames.append(bkrhu__eub)
    return reduce_varnames, var_to_param


@numba.extending.register_jitable
def dummy_agg_count(A):
    return len(A)
