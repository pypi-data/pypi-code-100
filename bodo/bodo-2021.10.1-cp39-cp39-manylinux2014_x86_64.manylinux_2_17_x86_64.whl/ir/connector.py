"""
Common IR extension functions for connectors such as CSV, Parquet and JSON readers.
"""
from collections import defaultdict
import numba
from numba.core import types
from numba.core.ir_utils import replace_vars_inner, visit_vars_inner
from numba.extending import box, models, register_model
from bodo.transforms.distributed_analysis import Distribution
from bodo.utils.utils import debug_prints


def connector_array_analysis(node, equiv_set, typemap, array_analysis):
    lmgi__sra = []
    assert len(node.out_vars) > 0, 'empty {} in array analysis'.format(node
        .connector_typ)
    if node.connector_typ == 'csv' and node.chunksize is not None:
        return [], []
    hbqp__qonko = []
    for wrsdc__wpg in node.out_vars:
        typ = typemap[wrsdc__wpg.name]
        djo__mdbs = array_analysis._gen_shape_call(equiv_set, wrsdc__wpg,
            typ.ndim, None, lmgi__sra)
        equiv_set.insert_equiv(wrsdc__wpg, djo__mdbs)
        hbqp__qonko.append(djo__mdbs[0])
        equiv_set.define(wrsdc__wpg, set())
    if len(hbqp__qonko) > 1:
        equiv_set.insert_equiv(*hbqp__qonko)
    return [], lmgi__sra


def connector_distributed_analysis(node, array_dists):
    from bodo.ir.sql_ext import SqlReader
    if isinstance(node, SqlReader) and node.limit is not None:
        kae__kuok = Distribution.OneD_Var
    else:
        kae__kuok = Distribution.OneD
    for bsh__iwd in node.out_vars:
        if bsh__iwd.name in array_dists:
            kae__kuok = Distribution(min(kae__kuok.value, array_dists[
                bsh__iwd.name].value))
    for bsh__iwd in node.out_vars:
        array_dists[bsh__iwd.name] = kae__kuok


def connector_typeinfer(node, typeinferer):
    for wrsdc__wpg, typ in zip(node.out_vars, node.out_types):
        typeinferer.lock_type(wrsdc__wpg.name, typ, loc=node.loc)


def visit_vars_connector(node, callback, cbdata):
    if debug_prints():
        print('visiting {} vars for:'.format(node.connector_typ), node)
        print('cbdata: ', sorted(cbdata.items()))
    iyg__ufm = []
    for wrsdc__wpg in node.out_vars:
        bznp__cqg = visit_vars_inner(wrsdc__wpg, callback, cbdata)
        iyg__ufm.append(bznp__cqg)
    node.out_vars = iyg__ufm
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = visit_vars_inner(node.file_name, callback, cbdata)
    if node.connector_typ == 'csv':
        node.nrows = visit_vars_inner(node.nrows, callback, cbdata)
        node.skiprows = visit_vars_inner(node.skiprows, callback, cbdata)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for vicxb__dljo in node.filters:
            for xiy__bjlhr in range(len(vicxb__dljo)):
                val = vicxb__dljo[xiy__bjlhr]
                vicxb__dljo[xiy__bjlhr] = val[0], val[1], visit_vars_inner(val
                    [2], callback, cbdata)


def connector_usedefs(node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    def_set.update({bsh__iwd.name for bsh__iwd in node.out_vars})
    if node.connector_typ in ('csv', 'parquet', 'json'):
        use_set.add(node.file_name.name)
    if node.connector_typ == 'csv':
        if isinstance(node.nrows, numba.core.ir.Var):
            use_set.add(node.nrows.name)
        if isinstance(node.skiprows, numba.core.ir.Var):
            use_set.add(node.skiprows.name)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        use_set.update({bsh__iwd[2].name for evy__jgr in node.filters for
            bsh__iwd in evy__jgr})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


def get_copies_connector(node, typemap):
    bas__ovmg = set(bsh__iwd.name for bsh__iwd in node.out_vars)
    return set(), bas__ovmg


def apply_copies_connector(node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    iyg__ufm = []
    for wrsdc__wpg in node.out_vars:
        bznp__cqg = replace_vars_inner(wrsdc__wpg, var_dict)
        iyg__ufm.append(bznp__cqg)
    node.out_vars = iyg__ufm
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = replace_vars_inner(node.file_name, var_dict)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for vicxb__dljo in node.filters:
            for xiy__bjlhr in range(len(vicxb__dljo)):
                val = vicxb__dljo[xiy__bjlhr]
                vicxb__dljo[xiy__bjlhr] = val[0], val[1], replace_vars_inner(
                    val[2], var_dict)
    if node.connector_typ == 'csv':
        node.nrows = replace_vars_inner(node.nrows, var_dict)
        node.skiprows = replace_vars_inner(node.skiprows, var_dict)


def build_connector_definitions(node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for wrsdc__wpg in node.out_vars:
        definitions[wrsdc__wpg.name].append(node)
    return definitions


def generate_filter_map(filters):
    if filters:
        oizpq__nja = []
        rgdge__kvf = [bsh__iwd[2] for evy__jgr in filters for bsh__iwd in
            evy__jgr]
        hosom__ksp = set()
        for qdj__vyci in rgdge__kvf:
            if qdj__vyci.name not in hosom__ksp:
                oizpq__nja.append(qdj__vyci)
            hosom__ksp.add(qdj__vyci.name)
        return {bsh__iwd.name: f'f{xiy__bjlhr}' for xiy__bjlhr, bsh__iwd in
            enumerate(oizpq__nja)}, oizpq__nja
    else:
        return {}, []


class StreamReaderType(types.Opaque):

    def __init__(self):
        super(StreamReaderType, self).__init__(name='StreamReaderType')


stream_reader_type = StreamReaderType()
register_model(StreamReaderType)(models.OpaqueModel)


@box(StreamReaderType)
def box_stream_reader(typ, val, c):
    c.pyapi.incref(val)
    return val
