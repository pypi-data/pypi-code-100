"""IR node for the data sorting"""
from collections import defaultdict
import numba
import numpy as np
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, mk_unique_var, replace_arg_nodes, replace_vars_inner, visit_vars_inner
import bodo
import bodo.libs.timsort
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_table, delete_table_decref_arrays, info_from_table, info_to_array, sort_values_table
from bodo.libs.str_arr_ext import cp_str_list_to_array, to_list_if_immutable_arr
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.utils.utils import debug_prints, gen_getitem
MIN_SAMPLES = 1000000
samplePointsPerPartitionHint = 20
MPI_ROOT = 0


class Sort(ir.Stmt):

    def __init__(self, df_in, df_out, key_arrs, out_key_arrs, df_in_vars,
        df_out_vars, inplace, loc, ascending_list=True, na_position='last'):
        self.df_in = df_in
        self.df_out = df_out
        self.key_arrs = key_arrs
        self.out_key_arrs = out_key_arrs
        self.df_in_vars = df_in_vars
        self.df_out_vars = df_out_vars
        self.inplace = inplace
        if isinstance(na_position, str):
            if na_position == 'last':
                self.na_position_b = (True,) * len(key_arrs)
            else:
                self.na_position_b = (False,) * len(key_arrs)
        else:
            self.na_position_b = tuple([(True if ygtdm__avd == 'last' else 
                False) for ygtdm__avd in na_position])
        if isinstance(ascending_list, bool):
            ascending_list = (ascending_list,) * len(key_arrs)
        self.ascending_list = ascending_list
        self.loc = loc

    def __repr__(self):
        aodzk__nxj = ''
        for zzvw__wvuxb, veqjf__gyj in self.df_in_vars.items():
            aodzk__nxj += "'{}':{}, ".format(zzvw__wvuxb, veqjf__gyj.name)
        tmtez__gfy = '{}{{{}}}'.format(self.df_in, aodzk__nxj)
        fga__vmnm = ''
        for zzvw__wvuxb, veqjf__gyj in self.df_out_vars.items():
            fga__vmnm += "'{}':{}, ".format(zzvw__wvuxb, veqjf__gyj.name)
        drgbs__auwgz = '{}{{{}}}'.format(self.df_out, fga__vmnm)
        return 'sort: [key: {}] {} [key: {}] {}'.format(', '.join(
            veqjf__gyj.name for veqjf__gyj in self.key_arrs), tmtez__gfy,
            ', '.join(veqjf__gyj.name for veqjf__gyj in self.out_key_arrs),
            drgbs__auwgz)


def sort_array_analysis(sort_node, equiv_set, typemap, array_analysis):
    sfg__eny = []
    oicb__uvk = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    for dftrm__mslvq in oicb__uvk:
        zaaa__pbof = equiv_set.get_shape(dftrm__mslvq)
        if zaaa__pbof is not None:
            sfg__eny.append(zaaa__pbof[0])
    if len(sfg__eny) > 1:
        equiv_set.insert_equiv(*sfg__eny)
    qkwrf__rpo = []
    sfg__eny = []
    lbde__ilhuv = sort_node.out_key_arrs + list(sort_node.df_out_vars.values())
    for dftrm__mslvq in lbde__ilhuv:
        pwoth__otzi = typemap[dftrm__mslvq.name]
        mfi__omf = array_analysis._gen_shape_call(equiv_set, dftrm__mslvq,
            pwoth__otzi.ndim, None, qkwrf__rpo)
        equiv_set.insert_equiv(dftrm__mslvq, mfi__omf)
        sfg__eny.append(mfi__omf[0])
        equiv_set.define(dftrm__mslvq, set())
    if len(sfg__eny) > 1:
        equiv_set.insert_equiv(*sfg__eny)
    return [], qkwrf__rpo


numba.parfors.array_analysis.array_analysis_extensions[Sort
    ] = sort_array_analysis


def sort_distributed_analysis(sort_node, array_dists):
    oicb__uvk = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    pekl__wrs = sort_node.out_key_arrs + list(sort_node.df_out_vars.values())
    luie__rgf = Distribution.OneD
    for dftrm__mslvq in oicb__uvk:
        luie__rgf = Distribution(min(luie__rgf.value, array_dists[
            dftrm__mslvq.name].value))
    nxp__ofr = Distribution(min(luie__rgf.value, Distribution.OneD_Var.value))
    for dftrm__mslvq in pekl__wrs:
        if dftrm__mslvq.name in array_dists:
            nxp__ofr = Distribution(min(nxp__ofr.value, array_dists[
                dftrm__mslvq.name].value))
    if nxp__ofr != Distribution.OneD_Var:
        luie__rgf = nxp__ofr
    for dftrm__mslvq in oicb__uvk:
        array_dists[dftrm__mslvq.name] = luie__rgf
    for dftrm__mslvq in pekl__wrs:
        array_dists[dftrm__mslvq.name] = nxp__ofr
    return


distributed_analysis.distributed_analysis_extensions[Sort
    ] = sort_distributed_analysis


def sort_typeinfer(sort_node, typeinferer):
    for jtq__dlkv, pau__rkv in zip(sort_node.key_arrs, sort_node.out_key_arrs):
        typeinferer.constraints.append(typeinfer.Propagate(dst=pau__rkv.
            name, src=jtq__dlkv.name, loc=sort_node.loc))
    for nppj__irni, dftrm__mslvq in sort_node.df_in_vars.items():
        epu__hhcdx = sort_node.df_out_vars[nppj__irni]
        typeinferer.constraints.append(typeinfer.Propagate(dst=epu__hhcdx.
            name, src=dftrm__mslvq.name, loc=sort_node.loc))
    return


typeinfer.typeinfer_extensions[Sort] = sort_typeinfer


def build_sort_definitions(sort_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    if not sort_node.inplace:
        for dftrm__mslvq in (sort_node.out_key_arrs + list(sort_node.
            df_out_vars.values())):
            definitions[dftrm__mslvq.name].append(sort_node)
    return definitions


ir_utils.build_defs_extensions[Sort] = build_sort_definitions


def visit_vars_sort(sort_node, callback, cbdata):
    if debug_prints():
        print('visiting sort vars for:', sort_node)
        print('cbdata: ', sorted(cbdata.items()))
    for irdl__wumu in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[irdl__wumu] = visit_vars_inner(sort_node.
            key_arrs[irdl__wumu], callback, cbdata)
        sort_node.out_key_arrs[irdl__wumu] = visit_vars_inner(sort_node.
            out_key_arrs[irdl__wumu], callback, cbdata)
    for nppj__irni in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[nppj__irni] = visit_vars_inner(sort_node.
            df_in_vars[nppj__irni], callback, cbdata)
    for nppj__irni in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[nppj__irni] = visit_vars_inner(sort_node.
            df_out_vars[nppj__irni], callback, cbdata)


ir_utils.visit_vars_extensions[Sort] = visit_vars_sort


def remove_dead_sort(sort_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    hqr__fjee = []
    for nppj__irni, dftrm__mslvq in sort_node.df_out_vars.items():
        if dftrm__mslvq.name not in lives:
            hqr__fjee.append(nppj__irni)
    for lyfk__ekcbw in hqr__fjee:
        sort_node.df_in_vars.pop(lyfk__ekcbw)
        sort_node.df_out_vars.pop(lyfk__ekcbw)
    if len(sort_node.df_out_vars) == 0 and all(veqjf__gyj.name not in lives for
        veqjf__gyj in sort_node.out_key_arrs):
        return None
    return sort_node


ir_utils.remove_dead_extensions[Sort] = remove_dead_sort


def sort_usedefs(sort_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({veqjf__gyj.name for veqjf__gyj in sort_node.key_arrs})
    use_set.update({veqjf__gyj.name for veqjf__gyj in sort_node.df_in_vars.
        values()})
    if not sort_node.inplace:
        def_set.update({veqjf__gyj.name for veqjf__gyj in sort_node.
            out_key_arrs})
        def_set.update({veqjf__gyj.name for veqjf__gyj in sort_node.
            df_out_vars.values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Sort] = sort_usedefs


def get_copies_sort(sort_node, typemap):
    dhhfo__rqdcf = set()
    if not sort_node.inplace:
        dhhfo__rqdcf = set(veqjf__gyj.name for veqjf__gyj in sort_node.
            df_out_vars.values())
        dhhfo__rqdcf.update({veqjf__gyj.name for veqjf__gyj in sort_node.
            out_key_arrs})
    return set(), dhhfo__rqdcf


ir_utils.copy_propagate_extensions[Sort] = get_copies_sort


def apply_copies_sort(sort_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for irdl__wumu in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[irdl__wumu] = replace_vars_inner(sort_node.
            key_arrs[irdl__wumu], var_dict)
        sort_node.out_key_arrs[irdl__wumu] = replace_vars_inner(sort_node.
            out_key_arrs[irdl__wumu], var_dict)
    for nppj__irni in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[nppj__irni] = replace_vars_inner(sort_node.
            df_in_vars[nppj__irni], var_dict)
    for nppj__irni in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[nppj__irni] = replace_vars_inner(sort_node.
            df_out_vars[nppj__irni], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Sort] = apply_copies_sort


def sort_distributed_run(sort_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    stwn__uej = False
    snuqt__fjbqv = list(sort_node.df_in_vars.values())
    lbde__ilhuv = list(sort_node.df_out_vars.values())
    if array_dists is not None:
        stwn__uej = True
        for veqjf__gyj in (sort_node.key_arrs + sort_node.out_key_arrs +
            snuqt__fjbqv + lbde__ilhuv):
            if array_dists[veqjf__gyj.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                veqjf__gyj.name] != distributed_pass.Distribution.OneD_Var:
                stwn__uej = False
    loc = sort_node.loc
    bvt__setf = sort_node.key_arrs[0].scope
    nodes = []
    key_arrs = sort_node.key_arrs
    if not sort_node.inplace:
        jnty__lytb = []
        for veqjf__gyj in key_arrs:
            thefd__porb = _copy_array_nodes(veqjf__gyj, nodes, typingctx,
                targetctx, typemap, calltypes)
            jnty__lytb.append(thefd__porb)
        key_arrs = jnty__lytb
        ymc__jal = []
        for veqjf__gyj in snuqt__fjbqv:
            gvw__zrtrh = _copy_array_nodes(veqjf__gyj, nodes, typingctx,
                targetctx, typemap, calltypes)
            ymc__jal.append(gvw__zrtrh)
        snuqt__fjbqv = ymc__jal
    key_name_args = [('key' + str(irdl__wumu)) for irdl__wumu in range(len(
        key_arrs))]
    rhsah__pjuqr = ', '.join(key_name_args)
    col_name_args = [('c' + str(irdl__wumu)) for irdl__wumu in range(len(
        snuqt__fjbqv))]
    smvv__hru = ', '.join(col_name_args)
    ufdp__rbdbm = 'def f({}, {}):\n'.format(rhsah__pjuqr, smvv__hru)
    ufdp__rbdbm += get_sort_cpp_section(key_name_args, col_name_args,
        sort_node.ascending_list, sort_node.na_position_b, stwn__uej)
    ufdp__rbdbm += '  return key_arrs, data\n'
    jvryp__rudv = {}
    exec(ufdp__rbdbm, {}, jvryp__rudv)
    kbv__okyb = jvryp__rudv['f']
    ttq__rfful = types.Tuple([typemap[veqjf__gyj.name] for veqjf__gyj in
        key_arrs])
    opkop__uxpo = types.Tuple([typemap[veqjf__gyj.name] for veqjf__gyj in
        snuqt__fjbqv])
    ynocc__hap = compile_to_numba_ir(kbv__okyb, {'bodo': bodo, 'np': np,
        'to_list_if_immutable_arr': to_list_if_immutable_arr,
        'cp_str_list_to_array': cp_str_list_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'sort_values_table':
        sort_values_table, 'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=tuple(list(ttq__rfful.types) + list(opkop__uxpo
        .types)), typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(ynocc__hap, key_arrs + snuqt__fjbqv)
    nodes += ynocc__hap.body[:-2]
    wgd__ffap = nodes[-1].target
    mrna__gzud = ir.Var(bvt__setf, mk_unique_var('key_data'), loc)
    typemap[mrna__gzud.name] = ttq__rfful
    gen_getitem(mrna__gzud, wgd__ffap, 0, calltypes, nodes)
    kjrsr__qhgfk = ir.Var(bvt__setf, mk_unique_var('sort_data'), loc)
    typemap[kjrsr__qhgfk.name] = opkop__uxpo
    gen_getitem(kjrsr__qhgfk, wgd__ffap, 1, calltypes, nodes)
    for irdl__wumu, var in enumerate(sort_node.out_key_arrs):
        gen_getitem(var, mrna__gzud, irdl__wumu, calltypes, nodes)
    for irdl__wumu, var in enumerate(lbde__ilhuv):
        gen_getitem(var, kjrsr__qhgfk, irdl__wumu, calltypes, nodes)
    return nodes


distributed_pass.distributed_run_extensions[Sort] = sort_distributed_run


def _copy_array_nodes(var, nodes, typingctx, targetctx, typemap, calltypes):

    def _impl(arr):
        return arr.copy()
    ynocc__hap = compile_to_numba_ir(_impl, {}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(typemap[var.name],), typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(ynocc__hap, [var])
    nodes += ynocc__hap.body[:-2]
    return nodes[-1].target


def get_sort_cpp_section(key_name_args, col_name_args, ascending_list,
    na_position_b, parallel_b):
    lwhpa__kjm = len(key_name_args)
    xbv__lhx = ['array_to_info({})'.format(qmlz__asqk) for qmlz__asqk in
        key_name_args] + ['array_to_info({})'.format(qmlz__asqk) for
        qmlz__asqk in col_name_args]
    ufdp__rbdbm = '  info_list_total = [{}]\n'.format(','.join(xbv__lhx))
    ufdp__rbdbm += '  table_total = arr_info_list_to_table(info_list_total)\n'
    ufdp__rbdbm += '  vect_ascending = np.array([{}])\n'.format(','.join(
        '1' if qqjul__fahc else '0' for qqjul__fahc in ascending_list))
    ufdp__rbdbm += '  na_position = np.array([{}])\n'.format(','.join('1' if
        qqjul__fahc else '0' for qqjul__fahc in na_position_b))
    ufdp__rbdbm += (
        """  out_table = sort_values_table(table_total, {}, vect_ascending.ctypes, na_position.ctypes, {})
"""
        .format(lwhpa__kjm, parallel_b))
    xhf__klgxl = 0
    xuem__otyj = []
    for qmlz__asqk in key_name_args:
        xuem__otyj.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(xhf__klgxl, qmlz__asqk))
        xhf__klgxl += 1
    ufdp__rbdbm += '  key_arrs = ({},)\n'.format(','.join(xuem__otyj))
    jkt__poc = []
    for qmlz__asqk in col_name_args:
        jkt__poc.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(xhf__klgxl, qmlz__asqk))
        xhf__klgxl += 1
    if len(jkt__poc) > 0:
        ufdp__rbdbm += '  data = ({},)\n'.format(','.join(jkt__poc))
    else:
        ufdp__rbdbm += '  data = ()\n'
    ufdp__rbdbm += '  delete_table(out_table)\n'
    ufdp__rbdbm += '  delete_table(table_total)\n'
    return ufdp__rbdbm
