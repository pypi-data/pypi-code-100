import numba
import numpy as np
import pandas as pd
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, replace_arg_nodes
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.utils.utils import check_java_installation
from bodo.utils.utils import sanitize_varname


class JsonReader(ir.Stmt):

    def __init__(self, df_out, loc, out_vars, out_types, file_name,
        df_colnames, orient, convert_dates, precise_float, lines, compression):
        self.connector_typ = 'json'
        self.df_out = df_out
        self.loc = loc
        self.out_vars = out_vars
        self.out_types = out_types
        self.file_name = file_name
        self.df_colnames = df_colnames
        self.orient = orient
        self.convert_dates = convert_dates
        self.precise_float = precise_float
        self.lines = lines
        self.compression = compression

    def __repr__(self):
        return ('{} = ReadJson(file={}, col_names={}, types={}, vars={})'.
            format(self.df_out, self.file_name, self.df_colnames, self.
            out_types, self.out_vars))


import llvmlite.binding as ll
from bodo.io import json_cpp
ll.add_symbol('json_file_chunk_reader', json_cpp.json_file_chunk_reader)
json_file_chunk_reader = types.ExternalFunction('json_file_chunk_reader',
    bodo.ir.connector.stream_reader_type(types.voidptr, types.bool_, types.
    bool_, types.int64, types.voidptr, types.voidptr))


def remove_dead_json(json_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    tqz__snna = []
    xid__atot = []
    mgybv__jrgug = []
    for vyljr__jzkrc, pdkdt__okhn in enumerate(json_node.out_vars):
        if pdkdt__okhn.name in lives:
            tqz__snna.append(json_node.df_colnames[vyljr__jzkrc])
            xid__atot.append(json_node.out_vars[vyljr__jzkrc])
            mgybv__jrgug.append(json_node.out_types[vyljr__jzkrc])
    json_node.df_colnames = tqz__snna
    json_node.out_vars = xid__atot
    json_node.out_types = mgybv__jrgug
    if len(json_node.out_vars) == 0:
        return None
    return json_node


def json_distributed_run(json_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    parallel = False
    if array_dists is not None:
        parallel = True
        for qykwt__wlro in json_node.out_vars:
            if array_dists[qykwt__wlro.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                qykwt__wlro.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    uxy__lzyf = len(json_node.out_vars)
    cylut__zikvl = ', '.join('arr' + str(vyljr__jzkrc) for vyljr__jzkrc in
        range(uxy__lzyf))
    ted__apcz = 'def json_impl(fname):\n'
    ted__apcz += '    ({},) = _json_reader_py(fname)\n'.format(cylut__zikvl)
    oxkwm__ancdv = {}
    exec(ted__apcz, {}, oxkwm__ancdv)
    ssf__wuhvs = oxkwm__ancdv['json_impl']
    snt__lae = _gen_json_reader_py(json_node.df_colnames, json_node.
        out_types, typingctx, targetctx, parallel, json_node.orient,
        json_node.convert_dates, json_node.precise_float, json_node.lines,
        json_node.compression)
    gbdcc__qeiu = compile_to_numba_ir(ssf__wuhvs, {'_json_reader_py':
        snt__lae}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type,), typemap=typemap, calltypes=calltypes).blocks.popitem()[1
        ]
    replace_arg_nodes(gbdcc__qeiu, [json_node.file_name])
    ema__bkfnp = gbdcc__qeiu.body[:-3]
    for vyljr__jzkrc in range(len(json_node.out_vars)):
        ema__bkfnp[-len(json_node.out_vars) + vyljr__jzkrc
            ].target = json_node.out_vars[vyljr__jzkrc]
    return ema__bkfnp


numba.parfors.array_analysis.array_analysis_extensions[JsonReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[JsonReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[JsonReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[JsonReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[JsonReader] = remove_dead_json
numba.core.analysis.ir_extension_usedefs[JsonReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[JsonReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[JsonReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[JsonReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[JsonReader] = json_distributed_run
compiled_funcs = []


def _gen_json_reader_py(col_names, col_typs, typingctx, targetctx, parallel,
    orient, convert_dates, precise_float, lines, compression):
    nyv__hlxm = [sanitize_varname(ata__kklyu) for ata__kklyu in col_names]
    cke__hvvsh = ', '.join(str(vyljr__jzkrc) for vyljr__jzkrc, jrw__wmrfu in
        enumerate(col_typs) if jrw__wmrfu.dtype == types.NPDatetime('ns'))
    nzysj__warl = ', '.join(["{}='{}'".format(vuyhs__kdein, bodo.ir.csv_ext
        ._get_dtype_str(jrw__wmrfu)) for vuyhs__kdein, jrw__wmrfu in zip(
        nyv__hlxm, col_typs)])
    deubs__zmhw = ', '.join(["'{}':{}".format(owubl__stwt, bodo.ir.csv_ext.
        _get_pd_dtype_str(jrw__wmrfu)) for owubl__stwt, jrw__wmrfu in zip(
        col_names, col_typs)])
    if compression is None:
        compression = 'uncompressed'
    ted__apcz = 'def json_reader_py(fname):\n'
    ted__apcz += '  check_java_installation(fname)\n'
    ted__apcz += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    ted__apcz += (
        '  f_reader = bodo.ir.json_ext.json_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    ted__apcz += (
        """    {}, {}, -1, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region) )
"""
        .format(lines, parallel, compression))
    ted__apcz += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    ted__apcz += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    ted__apcz += "      raise FileNotFoundError('File does not exist')\n"
    ted__apcz += '  with objmode({}):\n'.format(nzysj__warl)
    ted__apcz += "    df = pd.read_json(f_reader, orient='{}',\n".format(orient
        )
    ted__apcz += '       convert_dates = {}, \n'.format(convert_dates)
    ted__apcz += '       precise_float={}, \n'.format(precise_float)
    ted__apcz += '       lines={}, \n'.format(lines)
    ted__apcz += '       dtype={{{}}},\n'.format(deubs__zmhw)
    ted__apcz += '       )\n'
    for vuyhs__kdein, owubl__stwt in zip(nyv__hlxm, col_names):
        ted__apcz += '    if len(df) > 0:\n'
        ted__apcz += "        {} = df['{}'].values\n".format(vuyhs__kdein,
            owubl__stwt)
        ted__apcz += '    else:\n'
        ted__apcz += '        {} = np.array([])\n'.format(vuyhs__kdein)
    ted__apcz += '  return ({},)\n'.format(', '.join(fwlqh__uxv for
        fwlqh__uxv in nyv__hlxm))
    wmbb__djkqf = globals()
    oxkwm__ancdv = {}
    exec(ted__apcz, wmbb__djkqf, oxkwm__ancdv)
    snt__lae = oxkwm__ancdv['json_reader_py']
    dbk__fhh = numba.njit(snt__lae)
    compiled_funcs.append(dbk__fhh)
    return dbk__fhh
