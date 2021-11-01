"""
Implementation of pd.read_sql in BODO.
We piggyback on the pandas implementation. Future plan is to have a faster
version for this task.
"""
import numba
import numpy as np
import pandas as pd
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, replace_arg_nodes
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.ir.csv_ext import _get_dtype_str
from bodo.libs.array import delete_table, info_from_table, info_to_array, table_type
from bodo.libs.distributed_api import bcast, bcast_scalar
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.utils.typing import BodoError
from bodo.utils.utils import check_and_propagate_cpp_exception, sanitize_varname
MPI_ROOT = 0


class SqlReader(ir.Stmt):

    def __init__(self, sql_request, connection, df_out, df_colnames,
        out_vars, out_types, converted_colnames, db_type, loc):
        self.connector_typ = 'sql'
        self.sql_request = sql_request
        self.connection = connection
        self.df_out = df_out
        self.df_colnames = df_colnames
        self.out_vars = out_vars
        self.out_types = out_types
        self.converted_colnames = converted_colnames
        self.loc = loc
        self.limit = req_limit(sql_request)
        self.db_type = db_type
        self.filters = None

    def __repr__(self):
        return (
            '{} = ReadSql(sql_request={}, connection={}, col_names={}, types={}, vars={}, limit={})'
            .format(self.df_out, self.sql_request, self.connection, self.
            df_colnames, self.out_types, self.out_vars, self.limit))


def remove_dead_sql(sql_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    slmmg__bdo = []
    ojpk__rjfyw = []
    noxg__hnub = []
    for iwkj__jjud, pjd__uzbu in enumerate(sql_node.out_vars):
        if pjd__uzbu.name in lives:
            slmmg__bdo.append(sql_node.df_colnames[iwkj__jjud])
            ojpk__rjfyw.append(sql_node.out_vars[iwkj__jjud])
            noxg__hnub.append(sql_node.out_types[iwkj__jjud])
    sql_node.df_colnames = slmmg__bdo
    sql_node.out_vars = ojpk__rjfyw
    sql_node.out_types = noxg__hnub
    if len(sql_node.out_vars) == 0:
        return None
    return sql_node


def sql_distributed_run(sql_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    parallel = False
    if array_dists is not None:
        parallel = True
        for maxvp__tot in sql_node.out_vars:
            if array_dists[maxvp__tot.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                maxvp__tot.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    utvw__nyczq = len(sql_node.out_vars)
    qay__ohqhu = ', '.join('arr' + str(iwkj__jjud) for iwkj__jjud in range(
        utvw__nyczq))
    bmxc__xkrdl, cpszv__reenl = bodo.ir.connector.generate_filter_map(sql_node
        .filters)
    bpat__hyeb = ', '.join(bmxc__xkrdl.values())
    esq__nyg = f'def sql_impl(sql_request, conn, {bpat__hyeb}):\n'
    if sql_node.filters:
        bsloe__cth = []
        for thedb__zwb in sql_node.filters:
            mmj__swwqk = [' '.join(['(', huv__msh[0], huv__msh[1], '{' +
                bmxc__xkrdl[huv__msh[2].name] + '}', ')']) for huv__msh in
                thedb__zwb]
            bsloe__cth.append(' ( ' + ' AND '.join(mmj__swwqk) + ' ) ')
        jttds__jnk = ' WHERE ' + ' OR '.join(bsloe__cth)
        for iwkj__jjud, oab__bbkgo in enumerate(bmxc__xkrdl.values()):
            esq__nyg += f'    {oab__bbkgo} = get_sql_literal({oab__bbkgo})\n'
        esq__nyg += f'    sql_request = f"{{sql_request}} {jttds__jnk}"\n'
    esq__nyg += '    ({},) = _sql_reader_py(sql_request, conn)\n'.format(
        qay__ohqhu)
    dlrsb__xklb = {}
    exec(esq__nyg, {}, dlrsb__xklb)
    uad__axjc = dlrsb__xklb['sql_impl']
    odb__zlil = _gen_sql_reader_py(sql_node.df_colnames, sql_node.out_types,
        typingctx, targetctx, sql_node.db_type, sql_node.limit, parallel)
    flut__eay = compile_to_numba_ir(uad__axjc, {'_sql_reader_py': odb__zlil,
        'bcast_scalar': bcast_scalar, 'bcast': bcast, 'get_sql_literal':
        _get_snowflake_sql_literal}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=(string_type, string_type) + tuple(typemap[
        maxvp__tot.name] for maxvp__tot in cpszv__reenl), typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    if sql_node.db_type == 'snowflake':
        vfxl__pppz = [(mycby__julx.upper() if mycby__julx in sql_node.
            converted_colnames else mycby__julx) for mycby__julx in
            sql_node.df_colnames]
        fwd__iopzi = ', '.join([f'"{mycby__julx}"' for mycby__julx in
            vfxl__pppz])
    else:
        fwd__iopzi = ', '.join(sql_node.df_colnames)
    xuju__wzun = ('SELECT ' + fwd__iopzi + ' FROM (' + sql_node.sql_request +
        ') as TEMP')
    replace_arg_nodes(flut__eay, [ir.Const(xuju__wzun, sql_node.loc), ir.
        Const(sql_node.connection, sql_node.loc)] + cpszv__reenl)
    cpbqq__abjn = flut__eay.body[:-3]
    for iwkj__jjud in range(len(sql_node.out_vars)):
        cpbqq__abjn[-len(sql_node.out_vars) + iwkj__jjud
            ].target = sql_node.out_vars[iwkj__jjud]
    return cpbqq__abjn


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal(filter_value):
    jiay__skbd = types.unliteral(filter_value)
    if jiay__skbd == types.unicode_type:
        return lambda filter_value: f'$${filter_value}$$'
    elif isinstance(jiay__skbd, (types.Integer, types.Float)
        ) or filter_value == types.bool_:
        return lambda filter_value: str(filter_value)
    elif jiay__skbd == bodo.pd_timestamp_type:

        def impl(filter_value):
            blzg__csavs = filter_value.nanosecond
            ixaos__hda = ''
            if blzg__csavs < 10:
                ixaos__hda = '00'
            elif blzg__csavs < 100:
                ixaos__hda = '0'
            return (
                f"timestamp '{filter_value.strftime('%Y-%m-%d %H:%M:%S.%f')}{ixaos__hda}{blzg__csavs}'"
                )
        return impl
    elif jiay__skbd == bodo.datetime_date_type:
        return (lambda filter_value:
            f"date '{filter_value.strftime('%Y-%m-%d')}'")
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported type {jiay__skbd} used in filter pushdown.'
            )


numba.parfors.array_analysis.array_analysis_extensions[SqlReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[SqlReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[SqlReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[SqlReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[SqlReader] = remove_dead_sql
numba.core.analysis.ir_extension_usedefs[SqlReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[SqlReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[SqlReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[SqlReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[SqlReader] = sql_distributed_run
compiled_funcs = []


@numba.njit
def sqlalchemy_check():
    with numba.objmode():
        sqlalchemy_check_()


def sqlalchemy_check_():
    try:
        import sqlalchemy
    except ImportError as jbgb__agp:
        dqpcw__faey = (
            "Using URI string without sqlalchemy installed. sqlalchemy can be installed by calling 'conda install -c conda-forge sqlalchemy'."
            )
        raise BodoError(dqpcw__faey)


def req_limit(sql_request):
    import re
    clu__ybbrz = re.compile('LIMIT\\s+(\\d+)\\s*$', re.IGNORECASE)
    sufl__dlbag = clu__ybbrz.search(sql_request)
    if sufl__dlbag:
        return int(sufl__dlbag.group(1))
    else:
        return None


def _gen_sql_reader_py(col_names, col_typs, typingctx, targetctx, db_type,
    limit, parallel):
    mqbys__zsgpr = [sanitize_varname(ijpt__jkw) for ijpt__jkw in col_names]
    vwl__bzzr = ["{}='{}'".format(nfpim__khj, _get_dtype_str(jar__yyfh)) for
        nfpim__khj, jar__yyfh in zip(mqbys__zsgpr, col_typs)]
    if bodo.sql_access_method == 'multiple_access_by_block':
        esq__nyg = 'def sql_reader_py(sql_request,conn):\n'
        esq__nyg += '  sqlalchemy_check()\n'
        esq__nyg += '  rank = bodo.libs.distributed_api.get_rank()\n'
        esq__nyg += '  n_pes = bodo.libs.distributed_api.get_size()\n'
        esq__nyg += '  with objmode({}):\n'.format(', '.join(vwl__bzzr))
        esq__nyg += '    list_df_block = []\n'
        esq__nyg += '    block_size = 50000\n'
        esq__nyg += '    iter = 0\n'
        esq__nyg += '    while(True):\n'
        esq__nyg += '      offset = (iter * n_pes + rank) * block_size\n'
        esq__nyg += """      sql_cons = 'select * from (' + sql_request + ') x LIMIT ' + str(block_size) + ' OFFSET ' + str(offset)
"""
        esq__nyg += '      df_block = pd.read_sql(sql_cons, conn)\n'
        esq__nyg += '      if df_block.size == 0:\n'
        esq__nyg += '        break\n'
        esq__nyg += '      list_df_block.append(df_block)\n'
        esq__nyg += '      iter += 1\n'
        esq__nyg += '    df_ret = pd.concat(list_df_block)\n'
        for nfpim__khj, eyuf__nbe in zip(mqbys__zsgpr, col_names):
            esq__nyg += "    {} = df_ret['{}'].values\n".format(nfpim__khj,
                eyuf__nbe)
        esq__nyg += '  return ({},)\n'.format(', '.join(fbhi__vcoiv for
            fbhi__vcoiv in mqbys__zsgpr))
    if bodo.sql_access_method == 'multiple_access_nb_row_first':
        esq__nyg = 'def sql_reader_py(sql_request, conn):\n'
        if db_type == 'snowflake':
            hzu__njs = {}
            for iwkj__jjud, isg__epm in enumerate(col_typs):
                hzu__njs[f'col_{iwkj__jjud}_type'] = isg__epm
            esq__nyg += (
                f"  ev = bodo.utils.tracing.Event('read_snowflake', {parallel})\n"
                )

            def is_nullable(typ):
                return bodo.utils.utils.is_array_typ(typ, False
                    ) and not isinstance(typ, types.Array)
            sqbh__naj = [int(is_nullable(isg__epm)) for isg__epm in col_typs]
            esq__nyg += f"""  out_table = snowflake_read(unicode_to_utf8(sql_request), unicode_to_utf8(conn), {parallel}, {len(col_names)}, np.array({sqbh__naj}, dtype=np.int32).ctypes)
"""
            esq__nyg += '  check_and_propagate_cpp_exception()\n'
            for iwkj__jjud, edmgs__fkpj in enumerate(mqbys__zsgpr):
                esq__nyg += f"""  {edmgs__fkpj} = info_to_array(info_from_table(out_table, {iwkj__jjud}), col_{iwkj__jjud}_type)
"""
            esq__nyg += '  delete_table(out_table)\n'
            esq__nyg += f'  ev.finalize()\n'
        else:
            esq__nyg += '  sqlalchemy_check()\n'
            if parallel:
                esq__nyg += '  rank = bodo.libs.distributed_api.get_rank()\n'
                if limit is not None:
                    esq__nyg += f'  nb_row = {limit}\n'
                else:
                    esq__nyg += '  with objmode(nb_row="int64"):\n'
                    esq__nyg += f'     if rank == {MPI_ROOT}:\n'
                    esq__nyg += """         sql_cons = 'select count(*) from (' + sql_request + ') x'
"""
                    esq__nyg += (
                        '         frame = pd.read_sql(sql_cons, conn)\n')
                    esq__nyg += '         nb_row = frame.iat[0,0]\n'
                    esq__nyg += '     else:\n'
                    esq__nyg += '         nb_row = 0\n'
                    esq__nyg += '  nb_row = bcast_scalar(nb_row)\n'
                esq__nyg += '  with objmode({}):\n'.format(', '.join(vwl__bzzr)
                    )
                esq__nyg += """    offset, limit = bodo.libs.distributed_api.get_start_count(nb_row)
"""
                esq__nyg += f"""    sql_cons = 'select {', '.join(col_names)} from (' + sql_request + ') x LIMIT ' + str(limit) + ' OFFSET ' + str(offset)
"""
                esq__nyg += '    df_ret = pd.read_sql(sql_cons, conn)\n'
            else:
                esq__nyg += '  with objmode({}):\n'.format(', '.join(vwl__bzzr)
                    )
                esq__nyg += '    df_ret = pd.read_sql(sql_request, conn)\n'
            for nfpim__khj, eyuf__nbe in zip(mqbys__zsgpr, col_names):
                esq__nyg += "    {} = df_ret['{}'].values\n".format(nfpim__khj,
                    eyuf__nbe)
        esq__nyg += '  return ({},)\n'.format(', '.join(fbhi__vcoiv for
            fbhi__vcoiv in mqbys__zsgpr))
    slfsb__dnptp = {'bodo': bodo}
    if db_type == 'snowflake':
        slfsb__dnptp.update(hzu__njs)
        slfsb__dnptp.update({'np': np, 'unicode_to_utf8': unicode_to_utf8,
            'check_and_propagate_cpp_exception':
            check_and_propagate_cpp_exception, 'snowflake_read':
            _snowflake_read, 'info_to_array': info_to_array,
            'info_from_table': info_from_table, 'delete_table': delete_table})
    else:
        slfsb__dnptp.update({'sqlalchemy_check': sqlalchemy_check, 'pd': pd,
            'objmode': objmode, 'bcast_scalar': bcast_scalar})
    dlrsb__xklb = {}
    exec(esq__nyg, slfsb__dnptp, dlrsb__xklb)
    odb__zlil = dlrsb__xklb['sql_reader_py']
    bvcpb__gxgnp = numba.njit(odb__zlil)
    compiled_funcs.append(bvcpb__gxgnp)
    return bvcpb__gxgnp


_snowflake_read = types.ExternalFunction('snowflake_read', table_type(types
    .voidptr, types.voidptr, types.boolean, types.int64, types.voidptr))
import llvmlite.binding as ll
from bodo.io import arrow_cpp
ll.add_symbol('snowflake_read', arrow_cpp.snowflake_read)
