"""IR node for the join and merge"""
from collections import defaultdict
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba import generated_jit
from numba.core import cgutils, ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, next_label, replace_arg_nodes, replace_vars_inner, visit_vars_inner
from numba.extending import intrinsic, overload
import bodo
from bodo.libs.array import arr_info_list_to_table, array_to_info, compute_node_partition_by_hash, delete_table, delete_table_decref_arrays, hash_join_table, info_from_table, info_to_array
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType
from bodo.libs.str_arr_ext import copy_str_arr_slice, cp_str_list_to_array, get_bit_bitmap, get_null_bitmap_ptr, get_str_arr_item_length, get_str_arr_item_ptr, get_utf8_size, getitem_str_offset, num_total_chars, pre_alloc_string_array, set_bit_to, str_copy_ptr, string_array_type, to_list_if_immutable_arr
from bodo.libs.str_ext import string_type
from bodo.libs.timsort import getitem_arr_tup, setitem_arr_tup
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.utils.shuffle import _get_data_tup, _get_keys_tup, alloc_pre_shuffle_metadata, alltoallv_tup, finalize_shuffle_meta, getitem_arr_tup_single, update_shuffle_meta
from bodo.utils.typing import BodoError, dtype_to_array_type, find_common_np_dtype, is_dtype_nullable, is_nullable_type, to_nullable_type
from bodo.utils.utils import alloc_arr_tup, debug_prints, is_null_pointer
join_gen_cond_cfunc = {}
join_gen_cond_cfunc_addr = {}


@intrinsic
def add_join_gen_cond_cfunc_sym(typingctx, func, sym):

    def codegen(context, builder, signature, args):
        sino__dhfz = func.signature
        smajb__xft = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(64)])
        ijnvs__lryg = cgutils.get_or_insert_function(builder.module,
            smajb__xft, sym._literal_value)
        builder.call(ijnvs__lryg, [context.get_constant_null(sino__dhfz.
            args[0]), context.get_constant_null(sino__dhfz.args[1]),
            context.get_constant_null(sino__dhfz.args[2]), context.
            get_constant_null(sino__dhfz.args[3]), context.
            get_constant_null(sino__dhfz.args[4]), context.
            get_constant_null(sino__dhfz.args[5]), context.get_constant(
            types.int64, 0), context.get_constant(types.int64, 0)])
        context.add_linking_libs([join_gen_cond_cfunc[sym._literal_value].
            _library])
        return
    return types.none(func, sym), codegen


@numba.jit
def get_join_cond_addr(name):
    with numba.objmode(addr='int64'):
        addr = join_gen_cond_cfunc_addr[name]
    return addr


class Join(ir.Stmt):

    def __init__(self, df_out, left_df, right_df, left_keys, right_keys,
        out_data_vars, left_vars, right_vars, how, suffix_x, suffix_y, loc,
        is_left, is_right, is_join, left_index, right_index, indicator,
        is_na_equal, gen_cond_expr):
        self.df_out = df_out
        self.left_df = left_df
        self.right_df = right_df
        self.left_keys = left_keys
        self.right_keys = right_keys
        self.out_data_vars = out_data_vars
        self.left_vars = left_vars
        self.right_vars = right_vars
        self.how = how
        self.suffix_x = suffix_x
        self.suffix_y = suffix_y
        self.loc = loc
        self.is_left = is_left
        self.is_right = is_right
        self.is_join = is_join
        self.left_index = left_index
        self.right_index = right_index
        self.indicator = indicator
        self.is_na_equal = is_na_equal
        self.gen_cond_expr = gen_cond_expr
        self.left_cond_cols = set(kamu__luhzl for kamu__luhzl in left_vars.
            keys() if f'(left.{kamu__luhzl})' in gen_cond_expr)
        self.right_cond_cols = set(kamu__luhzl for kamu__luhzl in
            right_vars.keys() if f'(right.{kamu__luhzl})' in gen_cond_expr)
        bvxr__dox = set(left_keys) & set(right_keys)
        iji__tgc = set(left_vars.keys()) & set(right_vars.keys())
        snvvs__ntas = iji__tgc - bvxr__dox
        vect_same_key = []
        n_keys = len(left_keys)
        for wbjm__qrqp in range(n_keys):
            dsal__ljc = left_keys[wbjm__qrqp]
            xlpmb__rtfit = right_keys[wbjm__qrqp]
            vect_same_key.append(dsal__ljc == xlpmb__rtfit)
        self.vect_same_key = vect_same_key
        self.column_origins = {(str(kamu__luhzl) + suffix_x if kamu__luhzl in
            snvvs__ntas else kamu__luhzl): ('left', kamu__luhzl) for
            kamu__luhzl in left_vars.keys()}
        self.column_origins.update({(str(kamu__luhzl) + suffix_y if 
            kamu__luhzl in snvvs__ntas else kamu__luhzl): ('right',
            kamu__luhzl) for kamu__luhzl in right_vars.keys()})
        if '$_bodo_index_' in snvvs__ntas:
            snvvs__ntas.remove('$_bodo_index_')
        self.add_suffix = snvvs__ntas

    def __repr__(self):
        ibfzo__yix = ''
        for kamu__luhzl, ydivy__kxke in self.out_data_vars.items():
            ibfzo__yix += "'{}':{}, ".format(kamu__luhzl, ydivy__kxke.name)
        fug__neg = '{}{{{}}}'.format(self.df_out, ibfzo__yix)
        ada__powr = ''
        for kamu__luhzl, ydivy__kxke in self.left_vars.items():
            ada__powr += "'{}':{}, ".format(kamu__luhzl, ydivy__kxke.name)
        wyc__exr = '{}{{{}}}'.format(self.left_df, ada__powr)
        ada__powr = ''
        for kamu__luhzl, ydivy__kxke in self.right_vars.items():
            ada__powr += "'{}':{}, ".format(kamu__luhzl, ydivy__kxke.name)
        kdghg__xpzy = '{}{{{}}}'.format(self.right_df, ada__powr)
        return 'join [{}={}]: {} , {}, {}'.format(self.left_keys, self.
            right_keys, fug__neg, wyc__exr, kdghg__xpzy)


def join_array_analysis(join_node, equiv_set, typemap, array_analysis):
    tuspv__nejxz = []
    assert len(join_node.out_data_vars) > 0, 'empty join in array analysis'
    tva__neik = []
    ftvvx__iera = list(join_node.left_vars.values())
    for sbm__slce in ftvvx__iera:
        gixxc__sijku = typemap[sbm__slce.name]
        omuwg__ljvq = equiv_set.get_shape(sbm__slce)
        if omuwg__ljvq:
            tva__neik.append(omuwg__ljvq[0])
    if len(tva__neik) > 1:
        equiv_set.insert_equiv(*tva__neik)
    tva__neik = []
    ftvvx__iera = list(join_node.right_vars.values())
    for sbm__slce in ftvvx__iera:
        gixxc__sijku = typemap[sbm__slce.name]
        omuwg__ljvq = equiv_set.get_shape(sbm__slce)
        if omuwg__ljvq:
            tva__neik.append(omuwg__ljvq[0])
    if len(tva__neik) > 1:
        equiv_set.insert_equiv(*tva__neik)
    tva__neik = []
    for sbm__slce in join_node.out_data_vars.values():
        gixxc__sijku = typemap[sbm__slce.name]
        mwc__uaww = array_analysis._gen_shape_call(equiv_set, sbm__slce,
            gixxc__sijku.ndim, None, tuspv__nejxz)
        equiv_set.insert_equiv(sbm__slce, mwc__uaww)
        tva__neik.append(mwc__uaww[0])
        equiv_set.define(sbm__slce, set())
    if len(tva__neik) > 1:
        equiv_set.insert_equiv(*tva__neik)
    return [], tuspv__nejxz


numba.parfors.array_analysis.array_analysis_extensions[Join
    ] = join_array_analysis


def join_distributed_analysis(join_node, array_dists):
    xkilh__ndo = Distribution.OneD
    fokl__tckw = Distribution.OneD
    for sbm__slce in join_node.left_vars.values():
        xkilh__ndo = Distribution(min(xkilh__ndo.value, array_dists[
            sbm__slce.name].value))
    for sbm__slce in join_node.right_vars.values():
        fokl__tckw = Distribution(min(fokl__tckw.value, array_dists[
            sbm__slce.name].value))
    wwzua__mcyhn = Distribution.OneD_Var
    for sbm__slce in join_node.out_data_vars.values():
        if sbm__slce.name in array_dists:
            wwzua__mcyhn = Distribution(min(wwzua__mcyhn.value, array_dists
                [sbm__slce.name].value))
    ewyn__eujl = Distribution(min(wwzua__mcyhn.value, xkilh__ndo.value))
    wtf__zjdbg = Distribution(min(wwzua__mcyhn.value, fokl__tckw.value))
    wwzua__mcyhn = Distribution(max(ewyn__eujl.value, wtf__zjdbg.value))
    for sbm__slce in join_node.out_data_vars.values():
        array_dists[sbm__slce.name] = wwzua__mcyhn
    if wwzua__mcyhn != Distribution.OneD_Var:
        xkilh__ndo = wwzua__mcyhn
        fokl__tckw = wwzua__mcyhn
    for sbm__slce in join_node.left_vars.values():
        array_dists[sbm__slce.name] = xkilh__ndo
    for sbm__slce in join_node.right_vars.values():
        array_dists[sbm__slce.name] = fokl__tckw
    return


distributed_analysis.distributed_analysis_extensions[Join
    ] = join_distributed_analysis


def join_typeinfer(join_node, typeinferer):
    bvxr__dox = set(join_node.left_keys) & set(join_node.right_keys)
    iji__tgc = set(join_node.left_vars.keys()) & set(join_node.right_vars.
        keys())
    snvvs__ntas = iji__tgc - bvxr__dox
    for puyc__ppy, ypch__cagm in join_node.out_data_vars.items():
        if join_node.indicator and puyc__ppy == '_merge':
            continue
        if not puyc__ppy in join_node.column_origins:
            raise BodoError('join(): The variable ' + puyc__ppy +
                ' is absent from the output')
        zcl__nqb = join_node.column_origins[puyc__ppy]
        if zcl__nqb[0] == 'left':
            sbm__slce = join_node.left_vars[zcl__nqb[1]]
        else:
            sbm__slce = join_node.right_vars[zcl__nqb[1]]
        typeinferer.constraints.append(typeinfer.Propagate(dst=ypch__cagm.
            name, src=sbm__slce.name, loc=join_node.loc))
    return


typeinfer.typeinfer_extensions[Join] = join_typeinfer


def visit_vars_join(join_node, callback, cbdata):
    if debug_prints():
        print('visiting join vars for:', join_node)
        print('cbdata: ', sorted(cbdata.items()))
    for qsqkx__nct in list(join_node.left_vars.keys()):
        join_node.left_vars[qsqkx__nct] = visit_vars_inner(join_node.
            left_vars[qsqkx__nct], callback, cbdata)
    for qsqkx__nct in list(join_node.right_vars.keys()):
        join_node.right_vars[qsqkx__nct] = visit_vars_inner(join_node.
            right_vars[qsqkx__nct], callback, cbdata)
    for qsqkx__nct in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[qsqkx__nct] = visit_vars_inner(join_node.
            out_data_vars[qsqkx__nct], callback, cbdata)


ir_utils.visit_vars_extensions[Join] = visit_vars_join


def remove_dead_join(join_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    gzw__wijjs = []
    kjsl__uidki = True
    for qsqkx__nct, sbm__slce in join_node.out_data_vars.items():
        if sbm__slce.name in lives:
            kjsl__uidki = False
            continue
        if qsqkx__nct == '$_bodo_index_':
            continue
        if join_node.indicator and qsqkx__nct == '_merge':
            gzw__wijjs.append('_merge')
            join_node.indicator = False
            continue
        nar__fosw, nmm__qogsm = join_node.column_origins[qsqkx__nct]
        if (nar__fosw == 'left' and nmm__qogsm not in join_node.left_keys and
            nmm__qogsm not in join_node.left_cond_cols):
            join_node.left_vars.pop(nmm__qogsm)
            gzw__wijjs.append(qsqkx__nct)
        if (nar__fosw == 'right' and nmm__qogsm not in join_node.right_keys and
            nmm__qogsm not in join_node.right_cond_cols):
            join_node.right_vars.pop(nmm__qogsm)
            gzw__wijjs.append(qsqkx__nct)
    for cname in gzw__wijjs:
        join_node.out_data_vars.pop(cname)
    if kjsl__uidki:
        return None
    return join_node


ir_utils.remove_dead_extensions[Join] = remove_dead_join


def join_usedefs(join_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({ydivy__kxke.name for ydivy__kxke in join_node.left_vars
        .values()})
    use_set.update({ydivy__kxke.name for ydivy__kxke in join_node.
        right_vars.values()})
    def_set.update({ydivy__kxke.name for ydivy__kxke in join_node.
        out_data_vars.values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Join] = join_usedefs


def get_copies_join(join_node, typemap):
    wesev__fbllp = set(ydivy__kxke.name for ydivy__kxke in join_node.
        out_data_vars.values())
    return set(), wesev__fbllp


ir_utils.copy_propagate_extensions[Join] = get_copies_join


def apply_copies_join(join_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for qsqkx__nct in list(join_node.left_vars.keys()):
        join_node.left_vars[qsqkx__nct] = replace_vars_inner(join_node.
            left_vars[qsqkx__nct], var_dict)
    for qsqkx__nct in list(join_node.right_vars.keys()):
        join_node.right_vars[qsqkx__nct] = replace_vars_inner(join_node.
            right_vars[qsqkx__nct], var_dict)
    for qsqkx__nct in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[qsqkx__nct] = replace_vars_inner(join_node.
            out_data_vars[qsqkx__nct], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Join] = apply_copies_join


def build_join_definitions(join_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for sbm__slce in join_node.out_data_vars.values():
        definitions[sbm__slce.name].append(join_node)
    return definitions


ir_utils.build_defs_extensions[Join] = build_join_definitions


def join_distributed_run(join_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    left_parallel, right_parallel = False, False
    if array_dists is not None:
        left_parallel, right_parallel = _get_table_parallel_flags(join_node,
            array_dists)
    n_keys = len(join_node.left_keys)
    doxox__kdwu = tuple(join_node.left_vars[kamu__luhzl] for kamu__luhzl in
        join_node.left_keys)
    donb__qht = tuple(join_node.right_vars[kamu__luhzl] for kamu__luhzl in
        join_node.right_keys)
    ezozm__fsn = tuple(join_node.left_vars.keys())
    zkycs__wuz = tuple(join_node.right_vars.keys())
    wcb__xlfl = ()
    jug__suta = ()
    optional_column = False
    if (join_node.left_index and not join_node.right_index and not
        join_node.is_join):
        msq__idvpn = join_node.right_keys[0]
        if msq__idvpn in ezozm__fsn:
            jug__suta = msq__idvpn,
            wcb__xlfl = join_node.right_vars[msq__idvpn],
            optional_column = True
    if (join_node.right_index and not join_node.left_index and not
        join_node.is_join):
        msq__idvpn = join_node.left_keys[0]
        if msq__idvpn in zkycs__wuz:
            jug__suta = msq__idvpn,
            wcb__xlfl = join_node.left_vars[msq__idvpn],
            optional_column = True
    ifr__rkars = tuple(join_node.out_data_vars[cname] for cname in jug__suta)
    imr__teyu = tuple(ydivy__kxke for davy__clysk, ydivy__kxke in sorted(
        join_node.left_vars.items(), key=lambda a: str(a[0])) if 
        davy__clysk not in join_node.left_keys)
    xpwlq__syrup = tuple(ydivy__kxke for davy__clysk, ydivy__kxke in sorted
        (join_node.right_vars.items(), key=lambda a: str(a[0])) if 
        davy__clysk not in join_node.right_keys)
    fdjyd__gxbzy = (wcb__xlfl + doxox__kdwu + donb__qht + imr__teyu +
        xpwlq__syrup)
    lfbns__har = tuple(typemap[ydivy__kxke.name] for ydivy__kxke in
        fdjyd__gxbzy)
    lalp__mkn = tuple('opti_c' + str(i) for i in range(len(wcb__xlfl)))
    left_other_names = tuple('t1_c' + str(i) for i in range(len(imr__teyu)))
    right_other_names = tuple('t2_c' + str(i) for i in range(len(xpwlq__syrup))
        )
    left_other_types = tuple([typemap[kamu__luhzl.name] for kamu__luhzl in
        imr__teyu])
    right_other_types = tuple([typemap[kamu__luhzl.name] for kamu__luhzl in
        xpwlq__syrup])
    left_key_names = tuple('t1_key' + str(i) for i in range(n_keys))
    right_key_names = tuple('t2_key' + str(i) for i in range(n_keys))
    glbs = {}
    loc = join_node.loc
    func_text = 'def f({}{}, {},{}{}{}):\n'.format('{},'.format(lalp__mkn[0
        ]) if len(lalp__mkn) == 1 else '', ','.join(left_key_names), ','.
        join(right_key_names), ','.join(left_other_names), ',' if len(
        left_other_names) != 0 else '', ','.join(right_other_names))
    left_key_types = tuple(typemap[ydivy__kxke.name] for ydivy__kxke in
        doxox__kdwu)
    right_key_types = tuple(typemap[ydivy__kxke.name] for ydivy__kxke in
        donb__qht)
    for i in range(n_keys):
        glbs[f'key_type_{i}'] = _match_join_key_types(left_key_types[i],
            right_key_types[i], loc)
    func_text += '    t1_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({left_key_names[i]}, key_type_{i})' for i in
        range(n_keys)))
    func_text += '    t2_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({right_key_names[i]}, key_type_{i})' for
        i in range(n_keys)))
    func_text += '    data_left = ({}{})\n'.format(','.join(
        left_other_names), ',' if len(left_other_names) != 0 else '')
    func_text += '    data_right = ({}{})\n'.format(','.join(
        right_other_names), ',' if len(right_other_names) != 0 else '')
    rbe__its = []
    for cname in join_node.left_keys:
        if cname in join_node.add_suffix:
            sckw__tyx = str(cname) + join_node.suffix_x
        else:
            sckw__tyx = cname
        assert sckw__tyx in join_node.out_data_vars
        rbe__its.append(join_node.out_data_vars[sckw__tyx])
    for i, cname in enumerate(join_node.right_keys):
        if not join_node.vect_same_key[i] and not join_node.is_join:
            if cname in join_node.add_suffix:
                sckw__tyx = str(cname) + join_node.suffix_y
            else:
                sckw__tyx = cname
            assert sckw__tyx in join_node.out_data_vars
            rbe__its.append(join_node.out_data_vars[sckw__tyx])

    def _get_out_col_var(cname, is_left):
        if cname in join_node.add_suffix:
            if is_left:
                sckw__tyx = str(cname) + join_node.suffix_x
            else:
                sckw__tyx = str(cname) + join_node.suffix_y
        else:
            sckw__tyx = cname
        return join_node.out_data_vars[sckw__tyx]
    dyens__abjz = ifr__rkars + tuple(rbe__its)
    dyens__abjz += tuple(_get_out_col_var(davy__clysk, True) for 
        davy__clysk, ydivy__kxke in sorted(join_node.left_vars.items(), key
        =lambda a: str(a[0])) if davy__clysk not in join_node.left_keys)
    dyens__abjz += tuple(_get_out_col_var(davy__clysk, False) for 
        davy__clysk, ydivy__kxke in sorted(join_node.right_vars.items(),
        key=lambda a: str(a[0])) if davy__clysk not in join_node.right_keys)
    if join_node.indicator:
        dyens__abjz += _get_out_col_var('_merge', False),
    nbry__ijxo = [('t3_c' + str(i)) for i in range(len(dyens__abjz))]
    general_cond_cfunc, left_col_nums, right_col_nums = (
        _gen_general_cond_cfunc(join_node, typemap))
    if join_node.how == 'asof':
        if left_parallel or right_parallel:
            assert left_parallel and right_parallel
            func_text += """    t2_keys, data_right = parallel_asof_comm(t1_keys, t2_keys, data_right)
"""
        func_text += """    out_t1_keys, out_t2_keys, out_data_left, out_data_right = bodo.ir.join.local_merge_asof(t1_keys, t2_keys, data_left, data_right)
"""
    else:
        func_text += _gen_local_hash_join(optional_column, left_key_names,
            right_key_names, left_key_types, right_key_types,
            left_other_names, right_other_names, left_other_types,
            right_other_types, join_node.vect_same_key, join_node.is_left,
            join_node.is_right, join_node.is_join, left_parallel,
            right_parallel, glbs, [typemap[ydivy__kxke.name] for
            ydivy__kxke in dyens__abjz], join_node.loc, join_node.indicator,
            join_node.is_na_equal, general_cond_cfunc, left_col_nums,
            right_col_nums)
    if join_node.how == 'asof':
        for i in range(len(left_other_names)):
            func_text += '    left_{} = out_data_left[{}]\n'.format(i, i)
        for i in range(len(right_other_names)):
            func_text += '    right_{} = out_data_right[{}]\n'.format(i, i)
        for i in range(n_keys):
            func_text += f'    t1_keys_{i} = out_t1_keys[{i}]\n'
        for i in range(n_keys):
            func_text += f'    t2_keys_{i} = out_t2_keys[{i}]\n'
    idx = 0
    if optional_column:
        func_text += f'    {nbry__ijxo[idx]} = opti_0\n'
        idx += 1
    for i in range(n_keys):
        func_text += f'    {nbry__ijxo[idx]} = t1_keys_{i}\n'
        idx += 1
    for i in range(n_keys):
        if not join_node.vect_same_key[i] and not join_node.is_join:
            func_text += f'    {nbry__ijxo[idx]} = t2_keys_{i}\n'
            idx += 1
    for i in range(len(left_other_names)):
        func_text += f'    {nbry__ijxo[idx]} = left_{i}\n'
        idx += 1
    for i in range(len(right_other_names)):
        func_text += f'    {nbry__ijxo[idx]} = right_{i}\n'
        idx += 1
    if join_node.indicator:
        func_text += f'    {nbry__ijxo[idx]} = indicator_col\n'
        idx += 1
    smxta__dmay = {}
    exec(func_text, {}, smxta__dmay)
    kvgm__exj = smxta__dmay['f']
    glbs.update({'bodo': bodo, 'np': np, 'pd': pd,
        'to_list_if_immutable_arr': to_list_if_immutable_arr,
        'cp_str_list_to_array': cp_str_list_to_array, 'parallel_asof_comm':
        parallel_asof_comm, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'hash_join_table':
        hash_join_table, 'info_from_table': info_from_table,
        'info_to_array': info_to_array, 'delete_table': delete_table,
        'delete_table_decref_arrays': delete_table_decref_arrays,
        'add_join_gen_cond_cfunc_sym': add_join_gen_cond_cfunc_sym,
        'get_join_cond_addr': get_join_cond_addr})
    if general_cond_cfunc:
        glbs.update({'general_cond_cfunc': general_cond_cfunc})
    pdzv__pca = compile_to_numba_ir(kvgm__exj, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=lfbns__har, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(pdzv__pca, fdjyd__gxbzy)
    jsfo__riy = pdzv__pca.body[:-3]
    for i in range(len(dyens__abjz)):
        jsfo__riy[-len(dyens__abjz) + i].target = dyens__abjz[i]
    return jsfo__riy


distributed_pass.distributed_run_extensions[Join] = join_distributed_run


def _gen_general_cond_cfunc(join_node, typemap):
    expr = join_node.gen_cond_expr
    if not expr:
        return None, [], []
    toerp__vkvpv = next_label()
    fbk__yoh = _get_col_to_ind(join_node.left_keys, join_node.left_vars)
    lulk__ebknm = _get_col_to_ind(join_node.right_keys, join_node.right_vars)
    table_getitem_funcs = {'bodo': bodo, 'numba': numba, 'is_null_pointer':
        is_null_pointer}
    na_check_name = 'NOT_NA'
    func_text = f"""def bodo_join_gen_cond{toerp__vkvpv}(left_table, right_table, left_data1, right_data1, left_null_bitmap, right_null_bitmap, left_ind, right_ind):
"""
    func_text += '  if is_null_pointer(left_table):\n'
    func_text += '    return False\n'
    expr, func_text, left_col_nums = _replace_column_accesses(expr,
        fbk__yoh, typemap, join_node.left_vars, table_getitem_funcs,
        func_text, 'left', len(join_node.left_keys), na_check_name)
    expr, func_text, right_col_nums = _replace_column_accesses(expr,
        lulk__ebknm, typemap, join_node.right_vars, table_getitem_funcs,
        func_text, 'right', len(join_node.right_keys), na_check_name)
    func_text += f'  return {expr}'
    smxta__dmay = {}
    exec(func_text, table_getitem_funcs, smxta__dmay)
    uzx__mpdi = smxta__dmay[f'bodo_join_gen_cond{toerp__vkvpv}']
    zdmh__ibwra = types.bool_(types.voidptr, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.int64, types.int64)
    iaim__ibrc = numba.cfunc(zdmh__ibwra, nopython=True)(uzx__mpdi)
    join_gen_cond_cfunc[iaim__ibrc.native_name] = iaim__ibrc
    join_gen_cond_cfunc_addr[iaim__ibrc.native_name] = iaim__ibrc.address
    return iaim__ibrc, left_col_nums, right_col_nums


def _replace_column_accesses(expr, col_to_ind, typemap, col_vars,
    table_getitem_funcs, func_text, table_name, n_keys, na_check_name):
    wjjrv__ksq = []
    for kamu__luhzl, doibl__fendr in col_to_ind.items():
        cname = f'({table_name}.{kamu__luhzl})'
        if cname not in expr:
            continue
        klpg__sgoq = f'getitem_{table_name}_val_{doibl__fendr}'
        lgs__qsrer = f'_bodo_{table_name}_val_{doibl__fendr}'
        nkeo__mzjr = typemap[col_vars[kamu__luhzl].name].dtype
        if nkeo__mzjr == types.unicode_type:
            func_text += f"""  {lgs__qsrer}, {lgs__qsrer}_size = {klpg__sgoq}({table_name}_table, {table_name}_ind)
"""
            func_text += f"""  {lgs__qsrer} = bodo.libs.str_arr_ext.decode_utf8({lgs__qsrer}, {lgs__qsrer}_size)
"""
        else:
            func_text += (
                f'  {lgs__qsrer} = {klpg__sgoq}({table_name}_data1, {table_name}_ind)\n'
                )
        table_getitem_funcs[klpg__sgoq
            ] = bodo.libs.array._gen_row_access_intrinsic(nkeo__mzjr,
            doibl__fendr)
        expr = expr.replace(cname, lgs__qsrer)
        neg__rykau = f'({na_check_name}.{table_name}.{kamu__luhzl})'
        if neg__rykau in expr:
            ssyel__zpo = typemap[col_vars[kamu__luhzl].name]
            thx__nsn = f'nacheck_{table_name}_val_{doibl__fendr}'
            rzqyt__grif = f'_bodo_isna_{table_name}_val_{doibl__fendr}'
            if isinstance(ssyel__zpo, bodo.libs.int_arr_ext.IntegerArrayType
                ) or ssyel__zpo in [bodo.libs.bool_arr_ext.boolean_array,
                bodo.libs.str_arr_ext.string_array_type]:
                func_text += f"""  {rzqyt__grif} = {thx__nsn}({table_name}_null_bitmap, {table_name}_ind)
"""
            else:
                func_text += (
                    f'  {rzqyt__grif} = {thx__nsn}({table_name}_data1, {table_name}_ind)\n'
                    )
            table_getitem_funcs[thx__nsn
                ] = bodo.libs.array._gen_row_na_check_intrinsic(ssyel__zpo,
                doibl__fendr)
            expr = expr.replace(neg__rykau, rzqyt__grif)
        if doibl__fendr >= n_keys:
            wjjrv__ksq.append(doibl__fendr)
    return expr, func_text, wjjrv__ksq


def _get_col_to_ind(key_names, col_vars):
    n_keys = len(key_names)
    col_to_ind = {kamu__luhzl: i for i, kamu__luhzl in enumerate(key_names)}
    i = n_keys
    for kamu__luhzl in sorted(col_vars, key=lambda a: str(a)):
        if kamu__luhzl in key_names:
            continue
        col_to_ind[kamu__luhzl] = i
        i += 1
    return col_to_ind


def _match_join_key_types(t1, t2, loc):
    if t1 == t2:
        return t1
    try:
        arr = dtype_to_array_type(find_common_np_dtype([t1, t2]))
        return to_nullable_type(arr) if is_nullable_type(t1
            ) or is_nullable_type(t2) else arr
    except:
        raise BodoError(f'Join key types {t1} and {t2} do not match', loc=loc)


def _get_table_parallel_flags(join_node, array_dists):
    xwmd__ijzm = (distributed_pass.Distribution.OneD, distributed_pass.
        Distribution.OneD_Var)
    left_parallel = all(array_dists[ydivy__kxke.name] in xwmd__ijzm for
        ydivy__kxke in join_node.left_vars.values())
    right_parallel = all(array_dists[ydivy__kxke.name] in xwmd__ijzm for
        ydivy__kxke in join_node.right_vars.values())
    if not left_parallel:
        assert not any(array_dists[ydivy__kxke.name] in xwmd__ijzm for
            ydivy__kxke in join_node.left_vars.values())
    if not right_parallel:
        assert not any(array_dists[ydivy__kxke.name] in xwmd__ijzm for
            ydivy__kxke in join_node.right_vars.values())
    if left_parallel or right_parallel:
        assert all(array_dists[ydivy__kxke.name] in xwmd__ijzm for
            ydivy__kxke in join_node.out_data_vars.values())
    return left_parallel, right_parallel


def _gen_local_hash_join(optional_column, left_key_names, right_key_names,
    left_key_types, right_key_types, left_other_names, right_other_names,
    left_other_types, right_other_types, vect_same_key, is_left, is_right,
    is_join, left_parallel, right_parallel, glbs, out_types, loc, indicator,
    is_na_equal, general_cond_cfunc, left_col_nums, right_col_nums):

    def needs_typechange(in_type, need_nullable, is_same_key):
        return isinstance(in_type, types.Array) and not is_dtype_nullable(
            in_type.dtype) and need_nullable and not is_same_key
    staru__limoe = []
    for i in range(len(left_key_names)):
        kmrhb__poxmk = _match_join_key_types(left_key_types[i],
            right_key_types[i], loc)
        staru__limoe.append(needs_typechange(kmrhb__poxmk, is_right,
            vect_same_key[i]))
    for i in range(len(left_other_names)):
        staru__limoe.append(needs_typechange(left_other_types[i], is_right,
            False))
    for i in range(len(right_key_names)):
        if not vect_same_key[i] and not is_join:
            kmrhb__poxmk = _match_join_key_types(left_key_types[i],
                right_key_types[i], loc)
            staru__limoe.append(needs_typechange(kmrhb__poxmk, is_left, False))
    for i in range(len(right_other_names)):
        staru__limoe.append(needs_typechange(right_other_types[i], is_left,
            False))

    def get_out_type(idx, in_type, in_name, need_nullable, is_same_key):
        if isinstance(in_type, types.Array) and not is_dtype_nullable(in_type
            .dtype) and need_nullable and not is_same_key:
            if isinstance(in_type.dtype, types.Integer):
                whqfu__vundx = IntDtype(in_type.dtype).name
                assert whqfu__vundx.endswith('Dtype()')
                whqfu__vundx = whqfu__vundx[:-7]
                ihck__atncn = f"""    typ_{idx} = bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype="{whqfu__vundx}"))
"""
                ibu__zbd = f'typ_{idx}'
            else:
                assert in_type.dtype == types.bool_, 'unexpected non-nullable type in join'
                ihck__atncn = (
                    f'    typ_{idx} = bodo.libs.bool_arr_ext.alloc_bool_array(1)\n'
                    )
                ibu__zbd = f'typ_{idx}'
        else:
            ihck__atncn = ''
            ibu__zbd = in_name
        return ihck__atncn, ibu__zbd
    n_keys = len(left_key_names)
    func_text = '    # beginning of _gen_local_hash_join\n'
    bbbr__jhm = []
    for i in range(n_keys):
        bbbr__jhm.append('t1_keys[{}]'.format(i))
    for i in range(len(left_other_names)):
        bbbr__jhm.append('data_left[{}]'.format(i))
    func_text += '    info_list_total_l = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in bbbr__jhm))
    func_text += '    table_left = arr_info_list_to_table(info_list_total_l)\n'
    rmq__lfz = []
    for i in range(n_keys):
        rmq__lfz.append('t2_keys[{}]'.format(i))
    for i in range(len(right_other_names)):
        rmq__lfz.append('data_right[{}]'.format(i))
    func_text += '    info_list_total_r = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in rmq__lfz))
    func_text += (
        '    table_right = arr_info_list_to_table(info_list_total_r)\n')
    func_text += '    vect_same_key = np.array([{}])\n'.format(','.join('1' if
        loby__csyof else '0' for loby__csyof in vect_same_key))
    func_text += '    vect_need_typechange = np.array([{}])\n'.format(','.
        join('1' if loby__csyof else '0' for loby__csyof in staru__limoe))
    func_text += f"""    left_table_cond_columns = np.array({left_col_nums if len(left_col_nums) > 0 else [-1]}, dtype=np.int64)
"""
    func_text += f"""    right_table_cond_columns = np.array({right_col_nums if len(right_col_nums) > 0 else [-1]}, dtype=np.int64)
"""
    if general_cond_cfunc:
        func_text += f"""    cfunc_cond = add_join_gen_cond_cfunc_sym(general_cond_cfunc, '{general_cond_cfunc.native_name}')
"""
        func_text += (
            f"    cfunc_cond = get_join_cond_addr('{general_cond_cfunc.native_name}')\n"
            )
    else:
        func_text += '    cfunc_cond = 0\n'
    func_text += (
        """    out_table = hash_join_table(table_left, table_right, {}, {}, {}, {}, {}, vect_same_key.ctypes, vect_need_typechange.ctypes, {}, {}, {}, {}, {}, {}, cfunc_cond, left_table_cond_columns.ctypes, {}, right_table_cond_columns.ctypes, {})
"""
        .format(left_parallel, right_parallel, n_keys, len(left_other_names
        ), len(right_other_names), is_left, is_right, is_join,
        optional_column, indicator, is_na_equal, len(left_col_nums), len(
        right_col_nums)))
    func_text += '    delete_table(table_left)\n'
    func_text += '    delete_table(table_right)\n'
    idx = 0
    if optional_column:
        func_text += (
            f'    opti_0 = info_to_array(info_from_table(out_table, {idx}), opti_c0)\n'
            )
        idx += 1
    for i, vjb__lkkt in enumerate(left_key_names):
        kmrhb__poxmk = _match_join_key_types(left_key_types[i],
            right_key_types[i], loc)
        ypxg__lprgh = get_out_type(idx, kmrhb__poxmk, f't1_keys[{i}]',
            is_right, vect_same_key[i])
        func_text += ypxg__lprgh[0]
        glbs[f'out_type_{idx}'] = out_types[idx]
        if kmrhb__poxmk != left_key_types[i]:
            func_text += f"""    t1_keys_{i} = bodo.utils.utils.astype(info_to_array(info_from_table(out_table, {idx}), {ypxg__lprgh[1]}), out_type_{idx})
"""
        else:
            func_text += f"""    t1_keys_{i} = info_to_array(info_from_table(out_table, {idx}), {ypxg__lprgh[1]})
"""
        idx += 1
    for i, vjb__lkkt in enumerate(left_other_names):
        ypxg__lprgh = get_out_type(idx, left_other_types[i], vjb__lkkt,
            is_right, False)
        func_text += ypxg__lprgh[0]
        func_text += (
            '    left_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(i, idx, ypxg__lprgh[1]))
        idx += 1
    for i, vjb__lkkt in enumerate(right_key_names):
        if not vect_same_key[i] and not is_join:
            kmrhb__poxmk = _match_join_key_types(left_key_types[i],
                right_key_types[i], loc)
            ypxg__lprgh = get_out_type(idx, kmrhb__poxmk, f't2_keys[{i}]',
                is_left, False)
            func_text += ypxg__lprgh[0]
            glbs[f'out_type_{idx}'] = out_types[idx - len(left_other_names)]
            if kmrhb__poxmk != right_key_types[i]:
                func_text += f"""    t2_keys_{i} = bodo.utils.utils.astype(info_to_array(info_from_table(out_table, {idx}), {ypxg__lprgh[1]}), out_type_{idx})
"""
            else:
                func_text += f"""    t2_keys_{i} = info_to_array(info_from_table(out_table, {idx}), {ypxg__lprgh[1]})
"""
            idx += 1
    for i, vjb__lkkt in enumerate(right_other_names):
        ypxg__lprgh = get_out_type(idx, right_other_types[i], vjb__lkkt,
            is_left, False)
        func_text += ypxg__lprgh[0]
        func_text += (
            '    right_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(i, idx, ypxg__lprgh[1]))
        idx += 1
    if indicator:
        func_text += f"""    typ_{idx} = pd.Categorical(values=['both'], categories=('left_only', 'right_only', 'both'))
"""
        func_text += f"""    indicator_col = info_to_array(info_from_table(out_table, {idx}), typ_{idx})
"""
        idx += 1
    func_text += '    delete_table(out_table)\n'
    return func_text


def parallel_join_impl(key_arrs, data):
    mbeno__ijz = bodo.libs.distributed_api.get_size()
    pqsh__mqbwc = alloc_pre_shuffle_metadata(key_arrs, data, mbeno__ijz, False)
    davy__clysk = len(key_arrs[0])
    rsbo__oia = np.empty(davy__clysk, np.int32)
    mwjge__byxjx = arr_info_list_to_table([array_to_info(key_arrs[0])])
    qfgq__epsl = 1
    vzla__fpq = compute_node_partition_by_hash(mwjge__byxjx, qfgq__epsl,
        mbeno__ijz)
    xbfp__izsei = np.empty(1, np.int32)
    mxxry__sljcx = info_to_array(info_from_table(vzla__fpq, 0), xbfp__izsei)
    delete_table(vzla__fpq)
    delete_table(mwjge__byxjx)
    for i in range(davy__clysk):
        val = getitem_arr_tup_single(key_arrs, i)
        node_id = mxxry__sljcx[i]
        rsbo__oia[i] = node_id
        update_shuffle_meta(pqsh__mqbwc, node_id, i, key_arrs, data, False)
    shuffle_meta = finalize_shuffle_meta(key_arrs, data, pqsh__mqbwc,
        mbeno__ijz, False)
    for i in range(davy__clysk):
        node_id = rsbo__oia[i]
        write_send_buff(shuffle_meta, node_id, i, key_arrs, data)
        shuffle_meta.tmp_offset[node_id] += 1
    kobp__hmow = alltoallv_tup(key_arrs + data, shuffle_meta, key_arrs)
    rbe__its = _get_keys_tup(kobp__hmow, key_arrs)
    uom__fww = _get_data_tup(kobp__hmow, key_arrs)
    return rbe__its, uom__fww


@generated_jit(nopython=True, cache=True)
def parallel_shuffle(key_arrs, data):
    return parallel_join_impl


@numba.njit
def parallel_asof_comm(left_key_arrs, right_key_arrs, right_data):
    mbeno__ijz = bodo.libs.distributed_api.get_size()
    dhjun__hmebx = np.empty(mbeno__ijz, left_key_arrs[0].dtype)
    osg__cuhlt = np.empty(mbeno__ijz, left_key_arrs[0].dtype)
    bodo.libs.distributed_api.allgather(dhjun__hmebx, left_key_arrs[0][0])
    bodo.libs.distributed_api.allgather(osg__cuhlt, left_key_arrs[0][-1])
    ubj__rrby = np.zeros(mbeno__ijz, np.int32)
    uyzt__hpbr = np.zeros(mbeno__ijz, np.int32)
    nzlj__fzovl = np.zeros(mbeno__ijz, np.int32)
    jsa__jhoem = right_key_arrs[0][0]
    fda__vtspv = right_key_arrs[0][-1]
    rwhb__bro = -1
    i = 0
    while i < mbeno__ijz - 1 and osg__cuhlt[i] < jsa__jhoem:
        i += 1
    while i < mbeno__ijz and dhjun__hmebx[i] <= fda__vtspv:
        rwhb__bro, nnx__jcsi = _count_overlap(right_key_arrs[0],
            dhjun__hmebx[i], osg__cuhlt[i])
        if rwhb__bro != 0:
            rwhb__bro -= 1
            nnx__jcsi += 1
        ubj__rrby[i] = nnx__jcsi
        uyzt__hpbr[i] = rwhb__bro
        i += 1
    while i < mbeno__ijz:
        ubj__rrby[i] = 1
        uyzt__hpbr[i] = len(right_key_arrs[0]) - 1
        i += 1
    bodo.libs.distributed_api.alltoall(ubj__rrby, nzlj__fzovl, 1)
    fao__vnx = nzlj__fzovl.sum()
    tgwzc__ylpv = np.empty(fao__vnx, right_key_arrs[0].dtype)
    hby__gwjz = alloc_arr_tup(fao__vnx, right_data)
    uabqs__hjlg = bodo.ir.join.calc_disp(nzlj__fzovl)
    bodo.libs.distributed_api.alltoallv(right_key_arrs[0], tgwzc__ylpv,
        ubj__rrby, nzlj__fzovl, uyzt__hpbr, uabqs__hjlg)
    bodo.libs.distributed_api.alltoallv_tup(right_data, hby__gwjz,
        ubj__rrby, nzlj__fzovl, uyzt__hpbr, uabqs__hjlg)
    return (tgwzc__ylpv,), hby__gwjz


@numba.njit
def _count_overlap(r_key_arr, start, end):
    nnx__jcsi = 0
    rwhb__bro = 0
    jqh__evj = 0
    while jqh__evj < len(r_key_arr) and r_key_arr[jqh__evj] < start:
        rwhb__bro += 1
        jqh__evj += 1
    while jqh__evj < len(r_key_arr) and start <= r_key_arr[jqh__evj] <= end:
        jqh__evj += 1
        nnx__jcsi += 1
    return rwhb__bro, nnx__jcsi


def write_send_buff(shuffle_meta, node_id, i, key_arrs, data):
    return i


@overload(write_send_buff, no_unliteral=True)
def write_data_buff_overload(meta, node_id, i, key_arrs, data):
    func_text = 'def f(meta, node_id, i, key_arrs, data):\n'
    func_text += (
        '  w_ind = meta.send_disp[node_id] + meta.tmp_offset[node_id]\n')
    n_keys = len(key_arrs.types)
    for i, gixxc__sijku in enumerate(key_arrs.types + data.types):
        arr = 'key_arrs[{}]'.format(i) if i < n_keys else 'data[{}]'.format(
            i - n_keys)
        if not gixxc__sijku in (string_type, string_array_type,
            binary_array_type, bytes_type):
            func_text += '  meta.send_buff_tup[{}][w_ind] = {}[i]\n'.format(i,
                arr)
        else:
            func_text += ('  n_chars_{} = get_str_arr_item_length({}, i)\n'
                .format(i, arr))
            func_text += ('  meta.send_arr_lens_tup[{}][w_ind] = n_chars_{}\n'
                .format(i, i))
            if i >= n_keys:
                func_text += (
                    """  out_bitmap = meta.send_arr_nulls_tup[{}][meta.send_disp_nulls[node_id]:].ctypes
"""
                    .format(i))
                func_text += (
                    '  bit_val = get_bit_bitmap(get_null_bitmap_ptr(data[{}]), i)\n'
                    .format(i - n_keys))
                func_text += (
                    '  set_bit_to(out_bitmap, meta.tmp_offset[node_id], bit_val)\n'
                    )
            func_text += (
                """  indc_{} = meta.send_disp_char_tup[{}][node_id] + meta.tmp_offset_char_tup[{}][node_id]
"""
                .format(i, i, i))
            func_text += ('  item_ptr_{} = get_str_arr_item_ptr({}, i)\n'.
                format(i, arr))
            func_text += (
                """  str_copy_ptr(meta.send_arr_chars_tup[{}], indc_{}, item_ptr_{}, n_chars_{})
"""
                .format(i, i, i, i))
            func_text += (
                '  meta.tmp_offset_char_tup[{}][node_id] += n_chars_{}\n'.
                format(i, i))
    func_text += '  return w_ind\n'
    smxta__dmay = {}
    exec(func_text, {'str_copy_ptr': str_copy_ptr, 'get_null_bitmap_ptr':
        get_null_bitmap_ptr, 'get_bit_bitmap': get_bit_bitmap, 'set_bit_to':
        set_bit_to, 'get_str_arr_item_length': get_str_arr_item_length,
        'get_str_arr_item_ptr': get_str_arr_item_ptr}, smxta__dmay)
    lqb__blg = smxta__dmay['f']
    return lqb__blg


import llvmlite.binding as ll
from bodo.libs import hdist
ll.add_symbol('c_alltoallv', hdist.c_alltoallv)


@numba.njit
def calc_disp(arr):
    brlk__tli = np.empty_like(arr)
    brlk__tli[0] = 0
    for i in range(1, len(arr)):
        brlk__tli[i] = brlk__tli[i - 1] + arr[i - 1]
    return brlk__tli


def ensure_capacity(arr, new_size):
    zoci__kxied = arr
    cgvw__wri = len(arr)
    if cgvw__wri < new_size:
        rkcc__yfa = 2 * cgvw__wri
        zoci__kxied = bodo.utils.utils.alloc_type(rkcc__yfa, arr)
        zoci__kxied[:cgvw__wri] = arr
    return zoci__kxied


@overload(ensure_capacity, no_unliteral=True)
def ensure_capacity_overload(arr, new_size):
    if isinstance(arr, types.Array) or arr == boolean_array:
        return ensure_capacity
    assert isinstance(arr, types.BaseTuple)
    nnx__jcsi = arr.count
    func_text = 'def f(arr, new_size):\n'
    func_text += '  return ({}{})\n'.format(','.join([
        'ensure_capacity(arr[{}], new_size)'.format(i) for i in range(
        nnx__jcsi)]), ',' if nnx__jcsi == 1 else '')
    smxta__dmay = {}
    exec(func_text, {'ensure_capacity': ensure_capacity}, smxta__dmay)
    utcmo__ahs = smxta__dmay['f']
    return utcmo__ahs


@numba.njit
def ensure_capacity_str(arr, new_size, n_chars):
    zoci__kxied = arr
    cgvw__wri = len(arr)
    uutm__rasi = num_total_chars(arr)
    hrixx__mqyev = getitem_str_offset(arr, new_size - 1) + n_chars
    if cgvw__wri < new_size or hrixx__mqyev > uutm__rasi:
        rkcc__yfa = int(2 * cgvw__wri if cgvw__wri < new_size else cgvw__wri)
        eek__fkvur = int(2 * uutm__rasi + n_chars if hrixx__mqyev >
            uutm__rasi else uutm__rasi)
        zoci__kxied = pre_alloc_string_array(rkcc__yfa, eek__fkvur)
        copy_str_arr_slice(zoci__kxied, arr, new_size - 1)
    return zoci__kxied


def trim_arr_tup(data, new_size):
    return data


@overload(trim_arr_tup, no_unliteral=True)
def trim_arr_tup_overload(data, new_size):
    assert isinstance(data, types.BaseTuple)
    nnx__jcsi = data.count
    func_text = 'def f(data, new_size):\n'
    func_text += '  return ({}{})\n'.format(','.join([
        'trim_arr(data[{}], new_size)'.format(i) for i in range(nnx__jcsi)]
        ), ',' if nnx__jcsi == 1 else '')
    smxta__dmay = {}
    exec(func_text, {'trim_arr': trim_arr}, smxta__dmay)
    utcmo__ahs = smxta__dmay['f']
    return utcmo__ahs


def copy_elem_buff(arr, ind, val):
    zoci__kxied = ensure_capacity(arr, ind + 1)
    zoci__kxied[ind] = val
    return zoci__kxied


@overload(copy_elem_buff, no_unliteral=True)
def copy_elem_buff_overload(arr, ind, val):
    if isinstance(arr, types.Array) or arr == boolean_array:
        return copy_elem_buff
    assert arr == string_array_type

    def copy_elem_buff_str(arr, ind, val):
        zoci__kxied = ensure_capacity_str(arr, ind + 1, get_utf8_size(val))
        zoci__kxied[ind] = val
        return zoci__kxied
    return copy_elem_buff_str


def copy_elem_buff_tup(arr, ind, val):
    return arr


@overload(copy_elem_buff_tup, no_unliteral=True)
def copy_elem_buff_tup_overload(data, ind, val):
    assert isinstance(data, types.BaseTuple)
    nnx__jcsi = data.count
    func_text = 'def f(data, ind, val):\n'
    for i in range(nnx__jcsi):
        func_text += ('  arr_{} = copy_elem_buff(data[{}], ind, val[{}])\n'
            .format(i, i, i))
    func_text += '  return ({}{})\n'.format(','.join(['arr_{}'.format(i) for
        i in range(nnx__jcsi)]), ',' if nnx__jcsi == 1 else '')
    smxta__dmay = {}
    exec(func_text, {'copy_elem_buff': copy_elem_buff}, smxta__dmay)
    dpt__trl = smxta__dmay['f']
    return dpt__trl


def trim_arr(arr, size):
    return arr[:size]


@overload(trim_arr, no_unliteral=True)
def trim_arr_overload(arr, size):
    if isinstance(arr, types.Array) or arr == boolean_array:
        return trim_arr
    assert arr == string_array_type

    def trim_arr_str(arr, size):
        zoci__kxied = pre_alloc_string_array(size, np.int64(
            getitem_str_offset(arr, size)))
        copy_str_arr_slice(zoci__kxied, arr, size)
        return zoci__kxied
    return trim_arr_str


def setnan_elem_buff(arr, ind):
    zoci__kxied = ensure_capacity(arr, ind + 1)
    bodo.libs.array_kernels.setna(zoci__kxied, ind)
    return zoci__kxied


@overload(setnan_elem_buff, no_unliteral=True)
def setnan_elem_buff_overload(arr, ind):
    if isinstance(arr, types.Array) or arr == boolean_array:
        return setnan_elem_buff
    assert arr == string_array_type

    def setnan_elem_buff_str(arr, ind):
        zoci__kxied = ensure_capacity_str(arr, ind + 1, 0)
        zoci__kxied[ind] = ''
        bodo.libs.array_kernels.setna(zoci__kxied, ind)
        return zoci__kxied
    return setnan_elem_buff_str


def setnan_elem_buff_tup(arr, ind):
    return arr


@overload(setnan_elem_buff_tup, no_unliteral=True)
def setnan_elem_buff_tup_overload(data, ind):
    assert isinstance(data, types.BaseTuple)
    nnx__jcsi = data.count
    func_text = 'def f(data, ind):\n'
    for i in range(nnx__jcsi):
        func_text += '  arr_{} = setnan_elem_buff(data[{}], ind)\n'.format(i, i
            )
    func_text += '  return ({}{})\n'.format(','.join(['arr_{}'.format(i) for
        i in range(nnx__jcsi)]), ',' if nnx__jcsi == 1 else '')
    smxta__dmay = {}
    exec(func_text, {'setnan_elem_buff': setnan_elem_buff}, smxta__dmay)
    dpt__trl = smxta__dmay['f']
    return dpt__trl


@generated_jit(nopython=True, cache=True)
def _check_ind_if_hashed(right_keys, r_ind, l_key):
    if right_keys == types.Tuple((types.intp[::1],)):
        return lambda right_keys, r_ind, l_key: r_ind

    def _impl(right_keys, r_ind, l_key):
        jbua__satc = getitem_arr_tup(right_keys, r_ind)
        if jbua__satc != l_key:
            return -1
        return r_ind
    return _impl


@numba.njit
def local_merge_asof(left_keys, right_keys, data_left, data_right):
    qplky__zbfim = len(left_keys[0])
    xoy__tselc = len(right_keys[0])
    oymtt__ufxbn = alloc_arr_tup(qplky__zbfim, left_keys)
    jrtbx__ztgre = alloc_arr_tup(qplky__zbfim, right_keys)
    eihlu__smtz = alloc_arr_tup(qplky__zbfim, data_left)
    hwtqv__chxzx = alloc_arr_tup(qplky__zbfim, data_right)
    cmvo__vhoj = 0
    dcw__ero = 0
    for cmvo__vhoj in range(qplky__zbfim):
        if dcw__ero < 0:
            dcw__ero = 0
        while dcw__ero < xoy__tselc and getitem_arr_tup(right_keys, dcw__ero
            ) <= getitem_arr_tup(left_keys, cmvo__vhoj):
            dcw__ero += 1
        dcw__ero -= 1
        setitem_arr_tup(oymtt__ufxbn, cmvo__vhoj, getitem_arr_tup(left_keys,
            cmvo__vhoj))
        setitem_arr_tup(eihlu__smtz, cmvo__vhoj, getitem_arr_tup(data_left,
            cmvo__vhoj))
        if dcw__ero >= 0:
            setitem_arr_tup(jrtbx__ztgre, cmvo__vhoj, getitem_arr_tup(
                right_keys, dcw__ero))
            setitem_arr_tup(hwtqv__chxzx, cmvo__vhoj, getitem_arr_tup(
                data_right, dcw__ero))
        else:
            bodo.libs.array_kernels.setna_tup(jrtbx__ztgre, cmvo__vhoj)
            bodo.libs.array_kernels.setna_tup(hwtqv__chxzx, cmvo__vhoj)
    return oymtt__ufxbn, jrtbx__ztgre, eihlu__smtz, hwtqv__chxzx


def copy_arr_tup(arrs):
    return tuple(a.copy() for a in arrs)


@overload(copy_arr_tup, no_unliteral=True)
def copy_arr_tup_overload(arrs):
    nnx__jcsi = arrs.count
    func_text = 'def f(arrs):\n'
    func_text += '  return ({},)\n'.format(','.join('arrs[{}].copy()'.
        format(i) for i in range(nnx__jcsi)))
    smxta__dmay = {}
    exec(func_text, {}, smxta__dmay)
    impl = smxta__dmay['f']
    return impl


def get_nan_bits(arr, ind):
    return 0


@overload(get_nan_bits, no_unliteral=True)
def overload_get_nan_bits(arr, ind):
    if arr == string_array_type:

        def impl_str(arr, ind):
            psla__hvd = get_null_bitmap_ptr(arr)
            return get_bit_bitmap(psla__hvd, ind)
        return impl_str
    if isinstance(arr, IntegerArrayType) or arr == boolean_array:

        def impl(arr, ind):
            return bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr.
                _null_bitmap, ind)
        return impl
    return lambda arr, ind: False


def get_nan_bits_tup(arr_tup, ind):
    return tuple(get_nan_bits(arr, ind) for arr in arr_tup)


@overload(get_nan_bits_tup, no_unliteral=True)
def overload_get_nan_bits_tup(arr_tup, ind):
    nnx__jcsi = arr_tup.count
    func_text = 'def f(arr_tup, ind):\n'
    func_text += '  return ({}{})\n'.format(','.join([
        'get_nan_bits(arr_tup[{}], ind)'.format(i) for i in range(nnx__jcsi
        )]), ',' if nnx__jcsi == 1 else '')
    smxta__dmay = {}
    exec(func_text, {'get_nan_bits': get_nan_bits}, smxta__dmay)
    impl = smxta__dmay['f']
    return impl


def set_nan_bits(arr, ind, na_val):
    return 0


@overload(set_nan_bits, no_unliteral=True)
def overload_set_nan_bits(arr, ind, na_val):
    if arr == string_array_type:

        def impl_str(arr, ind, na_val):
            psla__hvd = get_null_bitmap_ptr(arr)
            set_bit_to(psla__hvd, ind, na_val)
        return impl_str
    if isinstance(arr, IntegerArrayType) or arr == boolean_array:

        def impl(arr, ind, na_val):
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, na_val)
        return impl
    return lambda arr, ind, na_val: None


def set_nan_bits_tup(arr_tup, ind, na_val):
    return tuple(set_nan_bits(arr, ind, na_val) for arr in arr_tup)


@overload(set_nan_bits_tup, no_unliteral=True)
def overload_set_nan_bits_tup(arr_tup, ind, na_val):
    nnx__jcsi = arr_tup.count
    func_text = 'def f(arr_tup, ind, na_val):\n'
    for i in range(nnx__jcsi):
        func_text += '  set_nan_bits(arr_tup[{}], ind, na_val[{}])\n'.format(i,
            i)
    func_text += '  return\n'
    smxta__dmay = {}
    exec(func_text, {'set_nan_bits': set_nan_bits}, smxta__dmay)
    impl = smxta__dmay['f']
    return impl
