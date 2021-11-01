"""
Helper functions for transformations.
"""
import itertools
import math
from collections import namedtuple
import numba
import numpy as np
import pandas as pd
from numba.core import ir, ir_utils, types
from numba.core.ir_utils import GuardException, build_definitions, compile_to_numba_ir, compute_cfg_from_blocks, find_callname, find_const, get_definition, guard, mk_unique_var, replace_arg_nodes, require
from numba.core.registry import CPUDispatcher
from numba.core.typing.templates import fold_arguments
import bodo
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.struct_arr_ext import StructArrayType, StructType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoConstUpdatedError, BodoError, can_literalize_type, get_literal_value, get_overload_const_bool, get_overload_const_list, is_literal_type, is_overload_constant_bool
from bodo.utils.utils import is_array_typ, is_assign, is_call, is_expr
ReplaceFunc = namedtuple('ReplaceFunc', ['func', 'arg_types', 'args',
    'glbls', 'inline_bodo_calls', 'run_full_pipeline', 'pre_nodes'])
bodo_types_with_params = {'ArrayItemArrayType', 'CSRMatrixType',
    'CategoricalArrayType', 'CategoricalIndexType', 'DataFrameType',
    'DatetimeIndexType', 'Decimal128Type', 'DecimalArrayType',
    'IntegerArrayType', 'IntervalArrayType', 'IntervalIndexType', 'List',
    'MapArrayType', 'NumericIndexType', 'PDCategoricalDtype',
    'PeriodIndexType', 'RangeIndexType', 'SeriesType', 'StringIndexType',
    'BinaryIndexType', 'StructArrayType', 'TimedeltaIndexType',
    'TupleArrayType'}
no_side_effect_call_tuples = {(int,), (list,), (set,), (dict,), (min,), (
    max,), (abs,), (len,), (bool,), ('ceil', math), ('init_series',
    'pd_series_ext', 'hiframes', bodo), ('get_series_data', 'pd_series_ext',
    'hiframes', bodo), ('get_series_index', 'pd_series_ext', 'hiframes',
    bodo), ('get_series_name', 'pd_series_ext', 'hiframes', bodo), (
    'get_index_data', 'pd_index_ext', 'hiframes', bodo), ('get_index_name',
    'pd_index_ext', 'hiframes', bodo), ('init_binary_str_index',
    'pd_index_ext', 'hiframes', bodo), ('init_numeric_index',
    'pd_index_ext', 'hiframes', bodo), ('init_categorical_index',
    'pd_index_ext', 'hiframes', bodo), ('_dti_val_finalize', 'pd_index_ext',
    'hiframes', bodo), ('init_datetime_index', 'pd_index_ext', 'hiframes',
    bodo), ('init_timedelta_index', 'pd_index_ext', 'hiframes', bodo), (
    'init_range_index', 'pd_index_ext', 'hiframes', bodo), (
    'init_heter_index', 'pd_index_ext', 'hiframes', bodo), (
    'get_int_arr_data', 'int_arr_ext', 'libs', bodo), ('get_int_arr_bitmap',
    'int_arr_ext', 'libs', bodo), ('init_integer_array', 'int_arr_ext',
    'libs', bodo), ('alloc_int_array', 'int_arr_ext', 'libs', bodo), (
    'inplace_eq', 'str_arr_ext', 'libs', bodo), ('get_bool_arr_data',
    'bool_arr_ext', 'libs', bodo), ('get_bool_arr_bitmap', 'bool_arr_ext',
    'libs', bodo), ('init_bool_array', 'bool_arr_ext', 'libs', bodo), (
    'alloc_bool_array', 'bool_arr_ext', 'libs', bodo), (bodo.libs.
    bool_arr_ext.compute_or_body,), (bodo.libs.bool_arr_ext.
    compute_and_body,), ('alloc_datetime_date_array', 'datetime_date_ext',
    'hiframes', bodo), ('alloc_datetime_timedelta_array',
    'datetime_timedelta_ext', 'hiframes', bodo), ('cat_replace',
    'pd_categorical_ext', 'hiframes', bodo), ('init_categorical_array',
    'pd_categorical_ext', 'hiframes', bodo), ('alloc_categorical_array',
    'pd_categorical_ext', 'hiframes', bodo), ('get_categorical_arr_codes',
    'pd_categorical_ext', 'hiframes', bodo), ('_sum_handle_nan',
    'series_kernels', 'hiframes', bodo), ('_box_cat_val', 'series_kernels',
    'hiframes', bodo), ('_mean_handle_nan', 'series_kernels', 'hiframes',
    bodo), ('_var_handle_mincount', 'series_kernels', 'hiframes', bodo), (
    '_handle_nan_count', 'series_kernels', 'hiframes', bodo), (
    '_handle_nan_count_ddof', 'series_kernels', 'hiframes', bodo), (
    'dist_return', 'distributed_api', 'libs', bodo), ('init_dataframe',
    'pd_dataframe_ext', 'hiframes', bodo), ('get_dataframe_data',
    'pd_dataframe_ext', 'hiframes', bodo), ('get_dataframe_index',
    'pd_dataframe_ext', 'hiframes', bodo), ('init_rolling',
    'pd_rolling_ext', 'hiframes', bodo), ('init_groupby', 'pd_groupby_ext',
    'hiframes', bodo), ('calc_nitems', 'array_kernels', 'libs', bodo), (
    'concat', 'array_kernels', 'libs', bodo), ('unique', 'array_kernels',
    'libs', bodo), ('nunique', 'array_kernels', 'libs', bodo), ('quantile',
    'array_kernels', 'libs', bodo), ('explode', 'array_kernels', 'libs',
    bodo), ('str_arr_from_sequence', 'str_arr_ext', 'libs', bodo), (
    'parse_datetime_str', 'pd_timestamp_ext', 'hiframes', bodo), (
    'integer_to_dt64', 'pd_timestamp_ext', 'hiframes', bodo), (
    'dt64_to_integer', 'pd_timestamp_ext', 'hiframes', bodo), (
    'timedelta64_to_integer', 'pd_timestamp_ext', 'hiframes', bodo), (
    'integer_to_timedelta64', 'pd_timestamp_ext', 'hiframes', bodo), (
    'npy_datetimestruct_to_datetime', 'pd_timestamp_ext', 'hiframes', bodo),
    ('isna', 'array_kernels', 'libs', bodo), ('copy',), (
    'from_iterable_impl', 'typing', 'utils', bodo), ('chain', itertools), (
    'groupby',), ('rolling',), (pd.CategoricalDtype,), (bodo.hiframes.
    pd_categorical_ext.get_code_for_value,), ('asarray', np), ('int32', np),
    ('int64', np), ('float64', np), ('float32', np), ('bool_', np), ('full',
    np), ('round', np), ('isnan', np), ('isnat', np), ('internal_prange',
    'parfor', numba), ('internal_prange', 'parfor', 'parfors', numba), (
    'empty_inferred', 'ndarray', 'unsafe', numba), ('_slice_span',
    'unicode', numba), ('_normalize_slice', 'unicode', numba), (
    'init_session_builder', 'pyspark_ext', 'libs', bodo), ('init_session',
    'pyspark_ext', 'libs', bodo), ('init_spark_df', 'pyspark_ext', 'libs',
    bodo), ('h5size', 'h5_api', 'io', bodo), ('pre_alloc_struct_array',
    'struct_arr_ext', 'libs', bodo), (bodo.libs.struct_arr_ext.
    pre_alloc_struct_array,), ('pre_alloc_tuple_array', 'tuple_arr_ext',
    'libs', bodo), (bodo.libs.tuple_arr_ext.pre_alloc_tuple_array,), (
    'pre_alloc_array_item_array', 'array_item_arr_ext', 'libs', bodo), (
    bodo.libs.array_item_arr_ext.pre_alloc_array_item_array,), (
    'dist_reduce', 'distributed_api', 'libs', bodo), (bodo.libs.
    distributed_api.dist_reduce,), ('pre_alloc_string_array', 'str_arr_ext',
    'libs', bodo), (bodo.libs.str_arr_ext.pre_alloc_string_array,), (
    'pre_alloc_binary_array', 'binary_arr_ext', 'libs', bodo), (bodo.libs.
    binary_arr_ext.pre_alloc_binary_array,), ('prange', bodo), (bodo.prange
    ,), ('objmode', bodo), (bodo.objmode,)}


def remove_hiframes(rhs, lives, call_list):
    fqg__jjl = tuple(call_list)
    if fqg__jjl in no_side_effect_call_tuples:
        return True
    if len(call_list) == 4 and call_list[1:] == ['conversion', 'utils', bodo]:
        return True
    if len(call_list) == 2 and call_list[0] == 'copy':
        return True
    if call_list == ['h5read', 'h5_api', 'io', bodo] and rhs.args[5
        ].name not in lives:
        return True
    if call_list == ['move_str_binary_arr_payload', 'str_arr_ext', 'libs', bodo
        ] and rhs.args[0].name not in lives:
        return True
    if call_list == ['setna', 'array_kernels', 'libs', bodo] and rhs.args[0
        ].name not in lives:
        return True
    if len(fqg__jjl) == 1 and tuple in getattr(fqg__jjl[0], '__mro__', ()):
        return True
    return False


numba.core.ir_utils.remove_call_handlers.append(remove_hiframes)


def compile_func_single_block(func, args, ret_var, typing_info=None,
    extra_globals=None, infer_types=True, run_untyped_pass=False, flags=
    None, replace_globals=True):
    jicc__wxgn = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd, 'math':
        math}
    if extra_globals is not None:
        jicc__wxgn.update(extra_globals)
    if not replace_globals:
        jicc__wxgn = func.__globals__
    loc = ir.Loc('', 0)
    if ret_var:
        loc = ret_var.loc
    if typing_info and infer_types:
        loc = typing_info.curr_loc
        f_ir = compile_to_numba_ir(func, jicc__wxgn, typingctx=typing_info.
            typingctx, targetctx=typing_info.targetctx, arg_typs=tuple(
            typing_info.typemap[qmfin__pdju.name] for qmfin__pdju in args),
            typemap=typing_info.typemap, calltypes=typing_info.calltypes)
    else:
        f_ir = compile_to_numba_ir(func, jicc__wxgn)
    assert len(f_ir.blocks
        ) == 1, 'only single block functions supported in compile_func_single_block()'
    if run_untyped_pass:
        ruq__uih = tuple(typing_info.typemap[qmfin__pdju.name] for
            qmfin__pdju in args)
        mtx__jqaq = bodo.transforms.untyped_pass.UntypedPass(f_ir,
            typing_info.typingctx, ruq__uih, {}, {}, flags)
        mtx__jqaq.run()
    ueak__kghhp = f_ir.blocks.popitem()[1]
    replace_arg_nodes(ueak__kghhp, args)
    qzul__sit = ueak__kghhp.body[:-2]
    update_locs(qzul__sit[len(args):], loc)
    for stmt in qzul__sit[:len(args)]:
        stmt.target.loc = loc
    if ret_var is not None:
        yskv__oyg = ueak__kghhp.body[-2]
        assert is_assign(yskv__oyg) and is_expr(yskv__oyg.value, 'cast')
        fzs__bqdh = yskv__oyg.value.value
        qzul__sit.append(ir.Assign(fzs__bqdh, ret_var, loc))
    return qzul__sit


def update_locs(node_list, loc):
    for stmt in node_list:
        stmt.loc = loc
        for ntdg__xsfd in stmt.list_vars():
            ntdg__xsfd.loc = loc
        if is_assign(stmt):
            stmt.value.loc = loc


def get_stmt_defs(stmt):
    if is_assign(stmt):
        return set([stmt.target.name])
    if type(stmt) in numba.core.analysis.ir_extension_usedefs:
        xyfj__lnazz = numba.core.analysis.ir_extension_usedefs[type(stmt)]
        kyhlx__bflt, hxzd__newzy = xyfj__lnazz(stmt)
        return hxzd__newzy
    return set()


def get_const_value(var, func_ir, err_msg, typemap=None, arg_types=None,
    file_info=None):
    if hasattr(var, 'loc'):
        loc = var.loc
    else:
        loc = None
    try:
        bppl__tonla = get_const_value_inner(func_ir, var, arg_types,
            typemap, file_info=file_info)
        if isinstance(bppl__tonla, ir.UndefinedType):
            pswwv__csvi = func_ir.get_definition(var.name).name
            raise BodoError(f"name '{pswwv__csvi}' is not defined", loc=loc)
    except GuardException as ebwj__fxwei:
        raise BodoError(err_msg, loc=loc)
    return bppl__tonla


def get_const_value_inner(func_ir, var, arg_types=None, typemap=None,
    updated_containers=None, file_info=None, pyobject_to_literal=False):
    require(isinstance(var, ir.Var))
    qbuq__lblsm = get_definition(func_ir, var)
    ezxe__cfylz = None
    if typemap is not None:
        ezxe__cfylz = typemap.get(var.name, None)
    if isinstance(qbuq__lblsm, ir.Arg) and arg_types is not None:
        ezxe__cfylz = arg_types[qbuq__lblsm.index]
    if updated_containers and var.name in updated_containers:
        raise BodoConstUpdatedError(
            f"variable '{var.name}' is updated inplace using '{updated_containers[var.name]}'"
            )
    if is_literal_type(ezxe__cfylz):
        return get_literal_value(ezxe__cfylz)
    if isinstance(qbuq__lblsm, (ir.Const, ir.Global, ir.FreeVar)):
        bppl__tonla = qbuq__lblsm.value
        return bppl__tonla
    if isinstance(qbuq__lblsm, ir.Arg) and can_literalize_type(ezxe__cfylz,
        pyobject_to_literal):
        raise numba.core.errors.ForceLiteralArg({qbuq__lblsm.index}, loc=
            var.loc, file_infos={qbuq__lblsm.index: file_info} if file_info
             is not None else None)
    if is_expr(qbuq__lblsm, 'binop'):
        yfpa__rrbi = get_const_value_inner(func_ir, qbuq__lblsm.lhs,
            arg_types, typemap, updated_containers)
        nlcc__kkn = get_const_value_inner(func_ir, qbuq__lblsm.rhs,
            arg_types, typemap, updated_containers)
        return qbuq__lblsm.fn(yfpa__rrbi, nlcc__kkn)
    if is_expr(qbuq__lblsm, 'unary'):
        bppl__tonla = get_const_value_inner(func_ir, qbuq__lblsm.value,
            arg_types, typemap, updated_containers)
        return qbuq__lblsm.fn(bppl__tonla)
    if is_expr(qbuq__lblsm, 'getattr') and typemap:
        diut__geebc = typemap.get(qbuq__lblsm.value.name, None)
        if isinstance(diut__geebc, bodo.hiframes.pd_dataframe_ext.DataFrameType
            ) and qbuq__lblsm.attr == 'columns':
            return pd.Index(diut__geebc.columns)
        if isinstance(diut__geebc, types.SliceType):
            zermp__gdqrl = get_definition(func_ir, qbuq__lblsm.value)
            require(is_call(zermp__gdqrl))
            rxt__tpo = find_callname(func_ir, zermp__gdqrl)
            bwa__qglqj = False
            if rxt__tpo == ('_normalize_slice', 'numba.cpython.unicode'):
                require(qbuq__lblsm.attr in ('start', 'step'))
                zermp__gdqrl = get_definition(func_ir, zermp__gdqrl.args[0])
                bwa__qglqj = True
            require(find_callname(func_ir, zermp__gdqrl) == ('slice',
                'builtins'))
            if len(zermp__gdqrl.args) == 1:
                if qbuq__lblsm.attr == 'start':
                    return 0
                if qbuq__lblsm.attr == 'step':
                    return 1
                require(qbuq__lblsm.attr == 'stop')
                return get_const_value_inner(func_ir, zermp__gdqrl.args[0],
                    arg_types, typemap, updated_containers)
            if qbuq__lblsm.attr == 'start':
                bppl__tonla = get_const_value_inner(func_ir, zermp__gdqrl.
                    args[0], arg_types, typemap, updated_containers)
                if bppl__tonla is None:
                    bppl__tonla = 0
                if bwa__qglqj:
                    require(bppl__tonla == 0)
                return bppl__tonla
            if qbuq__lblsm.attr == 'stop':
                assert not bwa__qglqj
                return get_const_value_inner(func_ir, zermp__gdqrl.args[1],
                    arg_types, typemap, updated_containers)
            require(qbuq__lblsm.attr == 'step')
            if len(zermp__gdqrl.args) == 2:
                return 1
            else:
                bppl__tonla = get_const_value_inner(func_ir, zermp__gdqrl.
                    args[2], arg_types, typemap, updated_containers)
                if bppl__tonla is None:
                    bppl__tonla = 1
                if bwa__qglqj:
                    require(bppl__tonla == 1)
                return bppl__tonla
    if is_expr(qbuq__lblsm, 'getattr'):
        return getattr(get_const_value_inner(func_ir, qbuq__lblsm.value,
            arg_types, typemap, updated_containers), qbuq__lblsm.attr)
    if is_expr(qbuq__lblsm, 'getitem'):
        value = get_const_value_inner(func_ir, qbuq__lblsm.value, arg_types,
            typemap, updated_containers)
        index = get_const_value_inner(func_ir, qbuq__lblsm.index, arg_types,
            typemap, updated_containers)
        return value[index]
    mcal__ysa = guard(find_callname, func_ir, qbuq__lblsm, typemap)
    if mcal__ysa is not None and len(mcal__ysa) == 2 and mcal__ysa[0
        ] == 'keys' and isinstance(mcal__ysa[1], ir.Var):
        pyei__cuz = qbuq__lblsm.func
        qbuq__lblsm = get_definition(func_ir, mcal__ysa[1])
        rtr__gce = mcal__ysa[1].name
        if updated_containers and rtr__gce in updated_containers:
            raise BodoConstUpdatedError(
                "variable '{}' is updated inplace using '{}'".format(
                rtr__gce, updated_containers[rtr__gce]))
        require(is_expr(qbuq__lblsm, 'build_map'))
        vals = [ntdg__xsfd[0] for ntdg__xsfd in qbuq__lblsm.items]
        ret__ykub = guard(get_definition, func_ir, pyei__cuz)
        assert isinstance(ret__ykub, ir.Expr) and ret__ykub.attr == 'keys'
        ret__ykub.attr = 'copy'
        return [get_const_value_inner(func_ir, ntdg__xsfd, arg_types,
            typemap, updated_containers) for ntdg__xsfd in vals]
    if is_expr(qbuq__lblsm, 'build_map'):
        return {get_const_value_inner(func_ir, ntdg__xsfd[0], arg_types,
            typemap, updated_containers): get_const_value_inner(func_ir,
            ntdg__xsfd[1], arg_types, typemap, updated_containers) for
            ntdg__xsfd in qbuq__lblsm.items}
    if is_expr(qbuq__lblsm, 'build_tuple'):
        return tuple(get_const_value_inner(func_ir, ntdg__xsfd, arg_types,
            typemap, updated_containers) for ntdg__xsfd in qbuq__lblsm.items)
    if is_expr(qbuq__lblsm, 'build_list'):
        return [get_const_value_inner(func_ir, ntdg__xsfd, arg_types,
            typemap, updated_containers) for ntdg__xsfd in qbuq__lblsm.items]
    if is_expr(qbuq__lblsm, 'build_set'):
        return {get_const_value_inner(func_ir, ntdg__xsfd, arg_types,
            typemap, updated_containers) for ntdg__xsfd in qbuq__lblsm.items}
    if mcal__ysa == ('list', 'builtins'):
        values = get_const_value_inner(func_ir, qbuq__lblsm.args[0],
            arg_types, typemap, updated_containers)
        if isinstance(values, set):
            values = sorted(values)
        return list(values)
    if mcal__ysa == ('set', 'builtins'):
        return set(get_const_value_inner(func_ir, qbuq__lblsm.args[0],
            arg_types, typemap, updated_containers))
    if mcal__ysa == ('range', 'builtins') and len(qbuq__lblsm.args) == 1:
        return range(get_const_value_inner(func_ir, qbuq__lblsm.args[0],
            arg_types, typemap, updated_containers))
    if mcal__ysa == ('slice', 'builtins'):
        return slice(*tuple(get_const_value_inner(func_ir, ntdg__xsfd,
            arg_types, typemap, updated_containers) for ntdg__xsfd in
            qbuq__lblsm.args))
    if mcal__ysa == ('str', 'builtins'):
        return str(get_const_value_inner(func_ir, qbuq__lblsm.args[0],
            arg_types, typemap, updated_containers))
    if mcal__ysa == ('bool', 'builtins'):
        return bool(get_const_value_inner(func_ir, qbuq__lblsm.args[0],
            arg_types, typemap, updated_containers))
    if mcal__ysa == ('format', 'builtins'):
        qmfin__pdju = get_const_value_inner(func_ir, qbuq__lblsm.args[0],
            arg_types, typemap, updated_containers)
        beu__fjprn = get_const_value_inner(func_ir, qbuq__lblsm.args[1],
            arg_types, typemap, updated_containers) if len(qbuq__lblsm.args
            ) > 1 else ''
        return format(qmfin__pdju, beu__fjprn)
    if mcal__ysa in (('init_binary_str_index', 'bodo.hiframes.pd_index_ext'
        ), ('init_numeric_index', 'bodo.hiframes.pd_index_ext'), (
        'init_categorical_index', 'bodo.hiframes.pd_index_ext'), (
        'init_datetime_index', 'bodo.hiframes.pd_index_ext'), (
        'init_timedelta_index', 'bodo.hiframes.pd_index_ext'), (
        'init_heter_index', 'bodo.hiframes.pd_index_ext')):
        return pd.Index(get_const_value_inner(func_ir, qbuq__lblsm.args[0],
            arg_types, typemap, updated_containers))
    if mcal__ysa == ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'):
        return np.array(get_const_value_inner(func_ir, qbuq__lblsm.args[0],
            arg_types, typemap, updated_containers))
    if mcal__ysa == ('init_range_index', 'bodo.hiframes.pd_index_ext'):
        return pd.RangeIndex(get_const_value_inner(func_ir, qbuq__lblsm.
            args[0], arg_types, typemap, updated_containers),
            get_const_value_inner(func_ir, qbuq__lblsm.args[1], arg_types,
            typemap, updated_containers), get_const_value_inner(func_ir,
            qbuq__lblsm.args[2], arg_types, typemap, updated_containers))
    if mcal__ysa == ('len', 'builtins') and typemap and isinstance(typemap.
        get(qbuq__lblsm.args[0].name, None), types.BaseTuple):
        return len(typemap[qbuq__lblsm.args[0].name])
    if mcal__ysa == ('len', 'builtins'):
        bqxse__udxhl = guard(get_definition, func_ir, qbuq__lblsm.args[0])
        if isinstance(bqxse__udxhl, ir.Expr) and bqxse__udxhl.op in (
            'build_tuple', 'build_list', 'build_set', 'build_map'):
            return len(bqxse__udxhl.items)
        return len(get_const_value_inner(func_ir, qbuq__lblsm.args[0],
            arg_types, typemap, updated_containers))
    if mcal__ysa == ('CategoricalDtype', 'pandas'):
        kws = dict(qbuq__lblsm.kws)
        arm__omn = get_call_expr_arg('CategoricalDtype', qbuq__lblsm.args,
            kws, 0, 'categories', '')
        lfo__lvdok = get_call_expr_arg('CategoricalDtype', qbuq__lblsm.args,
            kws, 1, 'ordered', False)
        if lfo__lvdok is not False:
            lfo__lvdok = get_const_value_inner(func_ir, lfo__lvdok,
                arg_types, typemap, updated_containers)
        if arm__omn == '':
            arm__omn = None
        else:
            arm__omn = get_const_value_inner(func_ir, arm__omn, arg_types,
                typemap, updated_containers)
        return pd.CategoricalDtype(arm__omn, lfo__lvdok)
    if mcal__ysa == ('dtype', 'numpy'):
        return np.dtype(get_const_value_inner(func_ir, qbuq__lblsm.args[0],
            arg_types, typemap, updated_containers))
    if mcal__ysa is not None and len(mcal__ysa) == 2 and mcal__ysa[1
        ] == 'pandas' and mcal__ysa[0] in ('Int8Dtype', 'Int16Dtype',
        'Int32Dtype', 'Int64Dtype', 'UInt8Dtype', 'UInt16Dtype',
        'UInt32Dtype', 'UInt64Dtype'):
        return getattr(pd, mcal__ysa[0])()
    if mcal__ysa is not None and len(mcal__ysa) == 2 and isinstance(mcal__ysa
        [1], ir.Var):
        bppl__tonla = get_const_value_inner(func_ir, mcal__ysa[1],
            arg_types, typemap, updated_containers)
        args = [get_const_value_inner(func_ir, ntdg__xsfd, arg_types,
            typemap, updated_containers) for ntdg__xsfd in qbuq__lblsm.args]
        kws = {zcxc__dlwno[0]: get_const_value_inner(func_ir, zcxc__dlwno[1
            ], arg_types, typemap, updated_containers) for zcxc__dlwno in
            qbuq__lblsm.kws}
        return getattr(bppl__tonla, mcal__ysa[0])(*args, **kws)
    if mcal__ysa is not None and len(mcal__ysa) == 2 and mcal__ysa[1
        ] == 'bodo' and mcal__ysa[0] in bodo_types_with_params:
        args = tuple(get_const_value_inner(func_ir, ntdg__xsfd, arg_types,
            typemap, updated_containers) for ntdg__xsfd in qbuq__lblsm.args)
        kwargs = {pswwv__csvi: get_const_value_inner(func_ir, ntdg__xsfd,
            arg_types, typemap, updated_containers) for pswwv__csvi,
            ntdg__xsfd in dict(qbuq__lblsm.kws).items()}
        return getattr(bodo, mcal__ysa[0])(*args, **kwargs)
    raise GuardException('Constant value not found')


def fold_argument_types(pysig, args, kws):

    def normal_handler(index, param, value):
        return value

    def default_handler(index, param, default):
        return types.Omitted(default)

    def stararg_handler(index, param, values):
        return types.StarArgTuple(values)
    args = fold_arguments(pysig, args, kws, normal_handler, default_handler,
        stararg_handler)
    return args


def get_const_func_output_type(func, arg_types, kw_types, typing_context,
    target_context, is_udf=True):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
    py_func = None
    if isinstance(func, types.MakeFunctionLiteral):
        giyix__vuyx = func.literal_value.code
        cqutq__nub = {'np': np, 'pd': pd, 'numba': numba, 'bodo': bodo}
        if hasattr(func.literal_value, 'globals'):
            cqutq__nub = func.literal_value.globals
        f_ir = numba.core.ir_utils.get_ir_of_code(cqutq__nub, giyix__vuyx)
        fix_struct_return(f_ir)
        typemap, vkuj__pqxi, tjkw__rjm, vyph__zzia = (numba.core.
            typed_passes.type_inference_stage(typing_context,
            target_context, f_ir, arg_types, None))
    elif isinstance(func, bodo.utils.typing.FunctionLiteral):
        py_func = func.literal_value
        f_ir, typemap, tjkw__rjm, vkuj__pqxi = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    elif isinstance(func, CPUDispatcher):
        py_func = func.py_func
        f_ir, typemap, tjkw__rjm, vkuj__pqxi = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    else:
        if not isinstance(func, types.Dispatcher):
            if isinstance(func, types.Function):
                raise BodoError(
                    f'Bodo does not support built-in functions yet, {func}')
            else:
                raise BodoError(f'Function type expected, not {func}')
        py_func = func.dispatcher.py_func
        f_ir, typemap, tjkw__rjm, vkuj__pqxi = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    if is_udf and isinstance(vkuj__pqxi, types.DictType):
        iamqb__dpn = guard(get_struct_keynames, f_ir, typemap)
        if iamqb__dpn is not None:
            vkuj__pqxi = StructType((vkuj__pqxi.value_type,) * len(
                iamqb__dpn), iamqb__dpn)
    if is_udf and isinstance(vkuj__pqxi, (SeriesType, HeterogeneousSeriesType)
        ):
        fgr__bnwu = numba.core.registry.cpu_target.typing_context
        zowc__ifwa = numba.core.registry.cpu_target.target_context
        iipsq__gjlm = bodo.transforms.series_pass.SeriesPass(f_ir,
            fgr__bnwu, zowc__ifwa, typemap, tjkw__rjm, {})
        iipsq__gjlm.run()
        iipsq__gjlm.run()
        iipsq__gjlm.run()
        teln__ccrs = compute_cfg_from_blocks(f_ir.blocks)
        ututr__jhhj = [guard(_get_const_series_info, f_ir.blocks[
            szvkn__eilb], f_ir, typemap) for szvkn__eilb in teln__ccrs.
            exit_points() if isinstance(f_ir.blocks[szvkn__eilb].body[-1],
            ir.Return)]
        if None in ututr__jhhj or len(pd.Series(ututr__jhhj).unique()) != 1:
            vkuj__pqxi.const_info = None
        else:
            vkuj__pqxi.const_info = ututr__jhhj[0]
    return vkuj__pqxi


def _get_const_series_info(block, f_ir, typemap):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType
    assert isinstance(block.body[-1], ir.Return)
    eeume__mrfop = block.body[-1].value
    ngxs__bfv = get_definition(f_ir, eeume__mrfop)
    require(is_expr(ngxs__bfv, 'cast'))
    ngxs__bfv = get_definition(f_ir, ngxs__bfv.value)
    require(is_call(ngxs__bfv) and find_callname(f_ir, ngxs__bfv) == (
        'init_series', 'bodo.hiframes.pd_series_ext'))
    bmvnh__ycafz = ngxs__bfv.args[1]
    qiiq__sptz = tuple(get_const_value_inner(f_ir, bmvnh__ycafz, typemap=
        typemap))
    if isinstance(typemap[eeume__mrfop.name], HeterogeneousSeriesType):
        return len(typemap[eeume__mrfop.name].data), qiiq__sptz
    vtkbc__gzuo = ngxs__bfv.args[0]
    hnph__qlxt = get_definition(f_ir, vtkbc__gzuo)
    if is_call(hnph__qlxt) and bodo.utils.utils.is_alloc_callname(*
        find_callname(f_ir, hnph__qlxt)):
        bfkco__piik = hnph__qlxt.args[0]
        ynmzs__ggfvh = get_const_value_inner(f_ir, bfkco__piik, typemap=typemap
            )
        return ynmzs__ggfvh, qiiq__sptz
    if is_call(hnph__qlxt) and find_callname(f_ir, hnph__qlxt) in [(
        'asarray', 'numpy'), ('str_arr_from_sequence', 'bodo.libs.str_arr_ext')
        ]:
        vtkbc__gzuo = hnph__qlxt.args[0]
        hnph__qlxt = get_definition(f_ir, vtkbc__gzuo)
    require(is_expr(hnph__qlxt, 'build_tuple') or is_expr(hnph__qlxt,
        'build_list'))
    return len(hnph__qlxt.items), qiiq__sptz


def extract_keyvals_from_struct_map(f_ir, build_map, loc, scope, typemap=None):
    wuwry__omyg = []
    bflfe__ubf = []
    values = []
    for fyb__ocbyt, ntdg__xsfd in build_map.items:
        yhxb__hxl = find_const(f_ir, fyb__ocbyt)
        require(isinstance(yhxb__hxl, str))
        bflfe__ubf.append(yhxb__hxl)
        wuwry__omyg.append(fyb__ocbyt)
        values.append(ntdg__xsfd)
    ygiat__fger = ir.Var(scope, mk_unique_var('val_tup'), loc)
    mzqrw__ejtws = ir.Assign(ir.Expr.build_tuple(values, loc), ygiat__fger, loc
        )
    f_ir._definitions[ygiat__fger.name] = [mzqrw__ejtws.value]
    nwo__eabic = ir.Var(scope, mk_unique_var('key_tup'), loc)
    fxnb__lue = ir.Assign(ir.Expr.build_tuple(wuwry__omyg, loc), nwo__eabic,
        loc)
    f_ir._definitions[nwo__eabic.name] = [fxnb__lue.value]
    if typemap is not None:
        typemap[ygiat__fger.name] = types.Tuple([typemap[ntdg__xsfd.name] for
            ntdg__xsfd in values])
        typemap[nwo__eabic.name] = types.Tuple([typemap[ntdg__xsfd.name] for
            ntdg__xsfd in wuwry__omyg])
    return bflfe__ubf, ygiat__fger, mzqrw__ejtws, nwo__eabic, fxnb__lue


def _replace_const_map_return(f_ir, block, label):
    require(isinstance(block.body[-1], ir.Return))
    wjlf__lgryl = block.body[-1].value
    ztif__moays = guard(get_definition, f_ir, wjlf__lgryl)
    require(is_expr(ztif__moays, 'cast'))
    ngxs__bfv = guard(get_definition, f_ir, ztif__moays.value)
    require(is_expr(ngxs__bfv, 'build_map'))
    require(len(ngxs__bfv.items) > 0)
    loc = block.loc
    scope = block.scope
    bflfe__ubf, ygiat__fger, mzqrw__ejtws, nwo__eabic, fxnb__lue = (
        extract_keyvals_from_struct_map(f_ir, ngxs__bfv, loc, scope))
    mqydn__lztq = ir.Var(scope, mk_unique_var('conv_call'), loc)
    piiof__vjvaw = ir.Assign(ir.Global('struct_if_heter_dict', bodo.utils.
        conversion.struct_if_heter_dict, loc), mqydn__lztq, loc)
    f_ir._definitions[mqydn__lztq.name] = [piiof__vjvaw.value]
    gawj__qber = ir.Var(scope, mk_unique_var('struct_val'), loc)
    ajps__mqn = ir.Assign(ir.Expr.call(mqydn__lztq, [ygiat__fger,
        nwo__eabic], {}, loc), gawj__qber, loc)
    f_ir._definitions[gawj__qber.name] = [ajps__mqn.value]
    ztif__moays.value = gawj__qber
    ngxs__bfv.items = [(fyb__ocbyt, fyb__ocbyt) for fyb__ocbyt, vyph__zzia in
        ngxs__bfv.items]
    block.body = block.body[:-2] + [mzqrw__ejtws, fxnb__lue, piiof__vjvaw,
        ajps__mqn] + block.body[-2:]
    return tuple(bflfe__ubf)


def get_struct_keynames(f_ir, typemap):
    teln__ccrs = compute_cfg_from_blocks(f_ir.blocks)
    actum__dnhrr = list(teln__ccrs.exit_points())[0]
    block = f_ir.blocks[actum__dnhrr]
    require(isinstance(block.body[-1], ir.Return))
    wjlf__lgryl = block.body[-1].value
    ztif__moays = guard(get_definition, f_ir, wjlf__lgryl)
    require(is_expr(ztif__moays, 'cast'))
    ngxs__bfv = guard(get_definition, f_ir, ztif__moays.value)
    require(is_call(ngxs__bfv) and find_callname(f_ir, ngxs__bfv) == (
        'struct_if_heter_dict', 'bodo.utils.conversion'))
    return get_overload_const_list(typemap[ngxs__bfv.args[1].name])


def fix_struct_return(f_ir):
    ntq__nbv = None
    teln__ccrs = compute_cfg_from_blocks(f_ir.blocks)
    for actum__dnhrr in teln__ccrs.exit_points():
        ntq__nbv = guard(_replace_const_map_return, f_ir, f_ir.blocks[
            actum__dnhrr], actum__dnhrr)
    return ntq__nbv


def update_node_list_definitions(node_list, func_ir):
    loc = ir.Loc('', 0)
    eyd__qayr = ir.Block(ir.Scope(None, loc), loc)
    eyd__qayr.body = node_list
    build_definitions({(0): eyd__qayr}, func_ir._definitions)
    return


NESTED_TUP_SENTINEL = '$BODO_NESTED_TUP'


def gen_const_val_str(c):
    if isinstance(c, tuple):
        return "'{}{}', ".format(NESTED_TUP_SENTINEL, len(c)) + ', '.join(
            gen_const_val_str(ntdg__xsfd) for ntdg__xsfd in c)
    if isinstance(c, str):
        return "'{}'".format(c)
    if isinstance(c, (pd.Timestamp, pd.Timedelta, float)):
        return "'{}'".format(c)
    return str(c)


def gen_const_tup(vals):
    kwszl__jroxx = ', '.join(gen_const_val_str(c) for c in vals)
    return '({}{})'.format(kwszl__jroxx, ',' if len(vals) == 1 else '')


def get_const_tup_vals(c_typ):
    vals = get_overload_const_list(c_typ)
    return _get_original_nested_tups(vals)


def _get_original_nested_tups(vals):
    for dbc__wyjh in range(len(vals) - 1, -1, -1):
        ntdg__xsfd = vals[dbc__wyjh]
        if isinstance(ntdg__xsfd, str) and ntdg__xsfd.startswith(
            NESTED_TUP_SENTINEL):
            imzw__novwe = int(ntdg__xsfd[len(NESTED_TUP_SENTINEL):])
            return _get_original_nested_tups(tuple(vals[:dbc__wyjh]) + (
                tuple(vals[dbc__wyjh + 1:dbc__wyjh + imzw__novwe + 1]),) +
                tuple(vals[dbc__wyjh + imzw__novwe + 1:]))
    return tuple(vals)


def get_call_expr_arg(f_name, args, kws, arg_no, arg_name, default=None,
    err_msg=None, use_default=False):
    qmfin__pdju = None
    if len(args) > arg_no:
        qmfin__pdju = args[arg_no]
        if arg_name in kws:
            err_msg = (
                f"{f_name}() got multiple values for argument '{arg_name}'")
            raise BodoError(err_msg)
    elif arg_name in kws:
        qmfin__pdju = kws[arg_name]
    if qmfin__pdju is None:
        if use_default or default is not None:
            return default
        if err_msg is None:
            err_msg = "{} requires '{}' argument".format(f_name, arg_name)
        raise BodoError(err_msg)
    return qmfin__pdju


def set_call_expr_arg(var, args, kws, arg_no, arg_name):
    if len(args) > arg_no:
        args[arg_no] = var
    elif arg_name in kws:
        kws[arg_name] = var
    else:
        raise BodoError('cannot set call argument since does not exist')


def avoid_udf_inline(py_func, arg_types, kw_types):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    f_ir = numba.core.compiler.run_frontend(py_func, inline_closures=True)
    if '_bodo_inline' in kw_types and is_overload_constant_bool(kw_types[
        '_bodo_inline']):
        return not get_overload_const_bool(kw_types['_bodo_inline'])
    if any(isinstance(t, DataFrameType) for t in arg_types + tuple(kw_types
        .values())):
        return True
    for block in f_ir.blocks.values():
        if isinstance(block.body[-1], (ir.Raise, ir.StaticRaise)):
            return True
        for stmt in block.body:
            if isinstance(stmt, ir.EnterWith):
                return True
    return False


def replace_func(pass_info, func, args, const=False, pre_nodes=None,
    extra_globals=None, pysig=None, kws=None, inline_bodo_calls=False,
    run_full_pipeline=False):
    jicc__wxgn = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd}
    if extra_globals is not None:
        jicc__wxgn.update(extra_globals)
    func.__globals__.update(jicc__wxgn)
    if pysig is not None:
        pre_nodes = [] if pre_nodes is None else pre_nodes
        scope = next(iter(pass_info.func_ir.blocks.values())).scope
        loc = scope.loc

        def normal_handler(index, param, default):
            return default

        def default_handler(index, param, default):
            eshm__zyxh = ir.Var(scope, mk_unique_var('defaults'), loc)
            try:
                pass_info.typemap[eshm__zyxh.name] = types.literal(default)
            except:
                pass_info.typemap[eshm__zyxh.name] = numba.typeof(default)
            jvaf__olvuy = ir.Assign(ir.Const(default, loc), eshm__zyxh, loc)
            pre_nodes.append(jvaf__olvuy)
            return eshm__zyxh
        args = numba.core.typing.fold_arguments(pysig, args, kws,
            normal_handler, default_handler, normal_handler)
    ruq__uih = tuple(pass_info.typemap[ntdg__xsfd.name] for ntdg__xsfd in args)
    if const:
        zlaoj__pqwb = []
        for dbc__wyjh, qmfin__pdju in enumerate(args):
            bppl__tonla = guard(find_const, pass_info.func_ir, qmfin__pdju)
            if bppl__tonla:
                zlaoj__pqwb.append(types.literal(bppl__tonla))
            else:
                zlaoj__pqwb.append(ruq__uih[dbc__wyjh])
        ruq__uih = tuple(zlaoj__pqwb)
    return ReplaceFunc(func, ruq__uih, args, jicc__wxgn, inline_bodo_calls,
        run_full_pipeline, pre_nodes)


def is_var_size_item_array_type(t):
    assert is_array_typ(t, False)
    return t == string_array_type or isinstance(t, ArrayItemArrayType
        ) or isinstance(t, StructArrayType) and any(
        is_var_size_item_array_type(tqv__zyk) for tqv__zyk in t.data)


def gen_init_varsize_alloc_sizes(t):
    if t == string_array_type:
        cxthh__mtfs = 'num_chars_{}'.format(ir_utils.next_label())
        return f'  {cxthh__mtfs} = 0\n', (cxthh__mtfs,)
    if isinstance(t, ArrayItemArrayType):
        ndale__dcrg, tqab__lkw = gen_init_varsize_alloc_sizes(t.dtype)
        cxthh__mtfs = 'num_items_{}'.format(ir_utils.next_label())
        return f'  {cxthh__mtfs} = 0\n' + ndale__dcrg, (cxthh__mtfs,
            ) + tqab__lkw
    return '', ()


def gen_varsize_item_sizes(t, item, var_names):
    if t == string_array_type:
        return '    {} += bodo.libs.str_arr_ext.get_utf8_size({})\n'.format(
            var_names[0], item)
    if isinstance(t, ArrayItemArrayType):
        return '    {} += len({})\n'.format(var_names[0], item
            ) + gen_varsize_array_counts(t.dtype, item, var_names[1:])
    return ''


def gen_varsize_array_counts(t, item, var_names):
    if t == string_array_type:
        return ('    {} += bodo.libs.str_arr_ext.get_num_total_chars({})\n'
            .format(var_names[0], item))
    return ''


def get_type_alloc_counts(t):
    if isinstance(t, (StructArrayType, TupleArrayType)):
        return 1 + sum(get_type_alloc_counts(tqv__zyk.dtype) for tqv__zyk in
            t.data)
    if isinstance(t, ArrayItemArrayType) or t == string_array_type:
        return 1 + get_type_alloc_counts(t.dtype)
    if isinstance(t, MapArrayType):
        return get_type_alloc_counts(t.key_arr_type) + get_type_alloc_counts(t
            .value_arr_type)
    if bodo.utils.utils.is_array_typ(t, False) or t == bodo.string_type:
        return 1
    if isinstance(t, StructType):
        return sum(get_type_alloc_counts(tqv__zyk) for tqv__zyk in t.data)
    if isinstance(t, types.BaseTuple):
        return sum(get_type_alloc_counts(tqv__zyk) for tqv__zyk in t.types)
    return 0


def find_udf_str_name(obj_dtype, func_name, typing_context, caller_name):
    byji__djne = typing_context.resolve_getattr(obj_dtype, func_name)
    if byji__djne is None:
        hnh__ppw = types.misc.Module(np)
        try:
            byji__djne = typing_context.resolve_getattr(hnh__ppw, func_name)
        except AttributeError as ebwj__fxwei:
            byji__djne = None
        if byji__djne is None:
            raise BodoError(
                f"{caller_name}(): No Pandas method or Numpy function found with the name '{func_name}'."
                )
    return byji__djne


def get_udf_str_return_type(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    byji__djne = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(byji__djne, types.BoundFunction):
        if axis is not None:
            hbw__rxjr = byji__djne.get_call_type(typing_context, (), {
                'axis': axis})
        else:
            hbw__rxjr = byji__djne.get_call_type(typing_context, (), {})
        return hbw__rxjr.return_type
    else:
        if bodo.utils.typing.is_numpy_ufunc(byji__djne):
            hbw__rxjr = byji__djne.get_call_type(typing_context, (obj_dtype
                ,), {})
            return hbw__rxjr.return_type
        raise BodoError(
            f"{caller_name}(): Only Pandas methods and np.ufunc are supported as string literals. '{func_name}' not supported."
            )


def get_pandas_method_str_impl(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    byji__djne = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(byji__djne, types.BoundFunction):
        cgcmx__nfpd = byji__djne.template
        if axis is not None:
            return cgcmx__nfpd._overload_func(obj_dtype, axis=axis)
        else:
            return cgcmx__nfpd._overload_func(obj_dtype)
    return None


def dict_to_const_keys_var_values_lists(dict_var, func_ir, arg_types,
    typemap, updated_containers, require_const_map, label):
    require(isinstance(dict_var, ir.Var))
    ngx__lvtjj = get_definition(func_ir, dict_var)
    require(isinstance(ngx__lvtjj, ir.Expr))
    require(ngx__lvtjj.op == 'build_map')
    zyi__eph = ngx__lvtjj.items
    wuwry__omyg = []
    values = []
    kalk__veax = False
    for dbc__wyjh in range(len(zyi__eph)):
        tirbs__jbgev, value = zyi__eph[dbc__wyjh]
        try:
            cuhsi__znq = get_const_value_inner(func_ir, tirbs__jbgev,
                arg_types, typemap, updated_containers)
            wuwry__omyg.append(cuhsi__znq)
            values.append(value)
        except GuardException as ebwj__fxwei:
            require_const_map[tirbs__jbgev] = label
            kalk__veax = True
    if kalk__veax:
        raise GuardException
    return wuwry__omyg, values
