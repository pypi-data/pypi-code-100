import numba
import numpy as np
import pandas as pd
from mpi4py import MPI
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, replace_arg_nodes
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.utils.typing import BodoError
from bodo.utils.utils import check_java_installation
from bodo.utils.utils import sanitize_varname


class CsvReader(ir.Stmt):

    def __init__(self, file_name, df_out, sep, df_colnames, out_vars,
        out_types, usecols, loc, header, compression, nrows, skiprows,
        chunksize):
        self.connector_typ = 'csv'
        self.file_name = file_name
        self.df_out = df_out
        self.sep = sep
        self.df_colnames = df_colnames
        self.out_vars = out_vars
        self.out_types = out_types
        self.usecols = usecols
        self.loc = loc
        self.skiprows = skiprows
        self.nrows = nrows
        self.header = header
        self.compression = compression
        self.chunksize = chunksize

    def __repr__(self):
        return (
            '{} = ReadCsv(file={}, col_names={}, types={}, vars={}, nrows={}, skiprows={}, self.chunksize={})'
            .format(self.df_out, self.file_name, self.df_colnames, self.
            out_types, self.out_vars, self.nrows, self.skiprows, self.
            chunksize))


def check_node_typing(node, typemap):
    quo__uvis = typemap[node.file_name.name]
    if types.unliteral(quo__uvis) != types.unicode_type:
        raise BodoError(
            f"pd.read_csv(): 'filepath_or_buffer' must be a string. Found type: {quo__uvis}."
            , node.file_name.loc)
    if not isinstance(node.skiprows, ir.Const):
        pvgek__bfaes = typemap[node.skiprows.name]
        if isinstance(pvgek__bfaes, types.Dispatcher):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' callable not supported yet.",
                node.file_name.loc)
        elif not isinstance(pvgek__bfaes, types.Integer):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' must be an integer. Found type {pvgek__bfaes}."
                , loc=node.skiprows.loc)
    if not isinstance(node.nrows, ir.Const):
        waod__tpmy = typemap[node.nrows.name]
        if not isinstance(waod__tpmy, types.Integer):
            raise BodoError(
                f"pd.read_csv(): 'nrows' must be an integer. Found type {waod__tpmy}."
                , loc=node.nrows.loc)


import llvmlite.binding as ll
from bodo.io import csv_cpp
ll.add_symbol('csv_file_chunk_reader', csv_cpp.csv_file_chunk_reader)
csv_file_chunk_reader = types.ExternalFunction('csv_file_chunk_reader',
    bodo.ir.connector.stream_reader_type(types.voidptr, types.bool_, types.
    int64, types.int64, types.bool_, types.voidptr, types.voidptr, types.int64)
    )


def remove_dead_csv(csv_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if csv_node.chunksize is not None:
        mol__gvnx = csv_node.out_vars[0]
        if mol__gvnx.name not in lives:
            return None
        return csv_node
    vynng__pjki = []
    pvhrl__wxreh = []
    jfbe__wwwvg = []
    gapr__bxgie = []
    for wyqe__efel, tpc__hha in enumerate(csv_node.out_vars):
        if tpc__hha.name in lives:
            vynng__pjki.append(csv_node.df_colnames[wyqe__efel])
            pvhrl__wxreh.append(csv_node.out_vars[wyqe__efel])
            jfbe__wwwvg.append(csv_node.out_types[wyqe__efel])
            gapr__bxgie.append(csv_node.usecols[wyqe__efel])
    csv_node.df_colnames = vynng__pjki
    csv_node.out_vars = pvhrl__wxreh
    csv_node.out_types = jfbe__wwwvg
    csv_node.usecols = gapr__bxgie
    if len(csv_node.out_vars) == 0:
        return None
    return csv_node


def csv_distributed_run(csv_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if csv_node.chunksize is not None:
        if array_dists is None:
            parallel = False
        else:
            sav__aozmn = array_dists[csv_node.out_vars[0].name]
            parallel = (sav__aozmn == distributed_pass.Distribution.OneD or
                sav__aozmn == distributed_pass.Distribution.OneD_Var)
        aob__ycuxi = 'def csv_iterator_impl(fname, nrows, skiprows):\n'
        aob__ycuxi += (
            f'    reader = _csv_reader_init(fname, nrows, skiprows)\n')
        aob__ycuxi += (
            f'    iterator = init_csv_iterator(reader, csv_iterator_type)\n')
        eyf__lfqpd = {}
        from bodo.io.csv_iterator_ext import init_csv_iterator
        exec(aob__ycuxi, {}, eyf__lfqpd)
        hni__bmaos = eyf__lfqpd['csv_iterator_impl']
        uui__jajt = 'def csv_reader_init(fname, nrows, skiprows):\n'
        uui__jajt += _gen_csv_file_reader_init(parallel, csv_node.header,
            csv_node.compression, csv_node.chunksize)
        uui__jajt += '  return f_reader\n'
        exec(uui__jajt, globals(), eyf__lfqpd)
        wyi__cjm = eyf__lfqpd['csv_reader_init']
        ifg__yupvc = numba.njit(wyi__cjm)
        compiled_funcs.append(ifg__yupvc)
        qrbjs__cbtge = compile_to_numba_ir(hni__bmaos, {'_csv_reader_init':
            ifg__yupvc, 'init_csv_iterator': init_csv_iterator,
            'csv_iterator_type': typemap[csv_node.out_vars[0].name]},
            typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
            types.int64, types.int64), typemap=typemap, calltypes=calltypes
            ).blocks.popitem()[1]
        replace_arg_nodes(qrbjs__cbtge, [csv_node.file_name, csv_node.nrows,
            csv_node.skiprows])
        ohuch__mrj = qrbjs__cbtge.body[:-3]
        ohuch__mrj[-1].target = csv_node.out_vars[0]
        return ohuch__mrj
    parallel = False
    if array_dists is not None:
        parallel = True
        for wwybe__yzukn in csv_node.out_vars:
            if array_dists[wwybe__yzukn.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                wwybe__yzukn.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    dygc__qdshn = len(csv_node.out_vars)
    bnah__mkhny = ', '.join('arr' + str(wyqe__efel) for wyqe__efel in range
        (dygc__qdshn))
    aob__ycuxi = 'def csv_impl(fname, nrows, skiprows):\n'
    aob__ycuxi += (
        f'    ({bnah__mkhny},) = _csv_reader_py(fname, nrows, skiprows)\n')
    eyf__lfqpd = {}
    exec(aob__ycuxi, {}, eyf__lfqpd)
    uoroe__zmgti = eyf__lfqpd['csv_impl']
    rmhf__gix = _gen_csv_reader_py(csv_node.df_colnames, csv_node.out_types,
        csv_node.usecols, csv_node.sep, parallel, csv_node.header, csv_node
        .compression)
    qrbjs__cbtge = compile_to_numba_ir(uoroe__zmgti, {'_csv_reader_py':
        rmhf__gix}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type, types.int64, types.int64), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(qrbjs__cbtge, [csv_node.file_name, csv_node.nrows,
        csv_node.skiprows])
    ohuch__mrj = qrbjs__cbtge.body[:-3]
    for wyqe__efel in range(len(csv_node.out_vars)):
        ohuch__mrj[-len(csv_node.out_vars) + wyqe__efel
            ].target = csv_node.out_vars[wyqe__efel]
    return ohuch__mrj


numba.parfors.array_analysis.array_analysis_extensions[CsvReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[CsvReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[CsvReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[CsvReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[CsvReader] = remove_dead_csv
numba.core.analysis.ir_extension_usedefs[CsvReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[CsvReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[CsvReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[CsvReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[CsvReader] = csv_distributed_run


def _get_dtype_str(t):
    zfyl__zozlo = t.dtype
    if isinstance(zfyl__zozlo, PDCategoricalDtype):
        aadr__cjg = CategoricalArrayType(zfyl__zozlo)
        ixmi__ufhg = 'CategoricalArrayType' + str(ir_utils.next_label())
        setattr(types, ixmi__ufhg, aadr__cjg)
        return ixmi__ufhg
    if zfyl__zozlo == types.NPDatetime('ns'):
        zfyl__zozlo = 'NPDatetime("ns")'
    if t == string_array_type:
        types.string_array_type = string_array_type
        return 'string_array_type'
    if isinstance(t, IntegerArrayType):
        lxb__pbjc = 'int_arr_{}'.format(zfyl__zozlo)
        setattr(types, lxb__pbjc, t)
        return lxb__pbjc
    if t == boolean_array:
        types.boolean_array = boolean_array
        return 'boolean_array'
    if zfyl__zozlo == types.bool_:
        zfyl__zozlo = 'bool_'
    if zfyl__zozlo == datetime_date_type:
        return 'datetime_date_array_type'
    return '{}[::1]'.format(zfyl__zozlo)


def _get_pd_dtype_str(t):
    zfyl__zozlo = t.dtype
    if isinstance(zfyl__zozlo, PDCategoricalDtype):
        return 'pd.CategoricalDtype({})'.format(zfyl__zozlo.categories)
    if zfyl__zozlo == types.NPDatetime('ns'):
        return 'str'
    if t == string_array_type:
        return 'str'
    if isinstance(t, IntegerArrayType):
        return '"{}Int{}"'.format('' if zfyl__zozlo.signed else 'U',
            zfyl__zozlo.bitwidth)
    if t == boolean_array:
        return 'np.bool_'
    return 'np.{}'.format(zfyl__zozlo)


compiled_funcs = []


@numba.njit
def check_nrows_skiprows_value(nrows, skiprows):
    if nrows < -1:
        raise ValueError('pd.read_csv: nrows must be integer >= 0.')
    if skiprows < 0:
        raise ValueError('pd.read_csv: skiprows must be integer >= 0.')


def astype(df, typemap, parallel):
    zumuo__wfhj = ''
    for dbr__vyjbp, ekd__udzsi in typemap.items():
        try:
            df[dbr__vyjbp] = df[dbr__vyjbp].astype(ekd__udzsi, copy=False)
        except TypeError as bogud__rnkik:
            zumuo__wfhj = (
                f"Caught the TypeError '{bogud__rnkik}' on column {dbr__vyjbp}. Consider setting the 'dtype' argument in 'read_csv' or investigate if the data is corrupted."
                )
            break
    ukyg__uplrz = bool(zumuo__wfhj)
    if parallel:
        oecho__sbi = MPI.COMM_WORLD
        ukyg__uplrz = oecho__sbi.allreduce(ukyg__uplrz, op=MPI.LOR)
    if ukyg__uplrz:
        yqnmh__pmfj = 'pd.read_csv(): Bodo could not infer dtypes correctly.'
        if zumuo__wfhj:
            raise TypeError(f'{yqnmh__pmfj}\n{zumuo__wfhj}')
        else:
            raise TypeError(
                f'{yqnmh__pmfj}\nPlease refer to errors on other ranks.')


def _gen_csv_file_reader_init(parallel, header, compression, chunksize):
    zbdsu__wugnb = header == 0
    if compression is None:
        compression = 'uncompressed'
    aob__ycuxi = '  check_nrows_skiprows_value(nrows, skiprows)\n'
    aob__ycuxi += '  check_java_installation(fname)\n'
    aob__ycuxi += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    aob__ycuxi += (
        '  f_reader = bodo.ir.csv_ext.csv_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    aob__ycuxi += (
        """    {}, skiprows, nrows, {}, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), {})
"""
        .format(parallel, zbdsu__wugnb, compression, chunksize))
    aob__ycuxi += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    aob__ycuxi += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    aob__ycuxi += "      raise FileNotFoundError('File does not exist')\n"
    return aob__ycuxi


def _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs, usecols,
    sep, parallel, check_parallel_runtime):
    bjvn__knn = ', '.join(['{}:{}'.format(bktt__rft, _get_pd_dtype_str(t)) for
        bktt__rft, t in zip(usecols, col_typs) if _get_pd_dtype_str(t) ==
        'str'])
    slzwr__omd = ', '.join(['{}:{}'.format(bktt__rft, _get_pd_dtype_str(t)) for
        bktt__rft, t in zip(usecols, col_typs) if _get_pd_dtype_str(t) !=
        'str'])
    dpsr__urw = ', '.join(str(wyqe__efel) for wyqe__efel, t in enumerate(
        col_typs) if t.dtype == types.NPDatetime('ns'))
    xqt__kwx = ', '.join(["{}='{}'".format(jgxof__myl, _get_dtype_str(t)) for
        jgxof__myl, t in zip(sanitized_cnames, col_typs)])
    iqa__wfq = _gen_parallel_flag_name(sanitized_cnames)
    if check_parallel_runtime:
        xqt__kwx += f", {iqa__wfq}='bool_'"
    aob__ycuxi = '  with objmode({}):\n'.format(xqt__kwx)
    aob__ycuxi += '    if f_reader.get_chunk_size() == 0:\n'
    pxbb__qslf = ', '.join(f'{vxy__yzww}' for vxy__yzww in usecols)
    aob__ycuxi += (
        f'      df = pd.DataFrame(columns=[{pxbb__qslf}], dtype=str)\n')
    aob__ycuxi += '    else:\n'
    aob__ycuxi += '      df = pd.read_csv(f_reader,\n'
    aob__ycuxi += '        header=None,\n'
    aob__ycuxi += '        parse_dates=[{}],\n'.format(dpsr__urw)
    aob__ycuxi += '        dtype={{{}}},\n'.format(bjvn__knn)
    aob__ycuxi += '        usecols={}, sep={!r}, low_memory=False)\n'.format(
        usecols, sep)
    aob__ycuxi += '    typemap = {{{}}}\n'.format(slzwr__omd)
    if check_parallel_runtime:
        aob__ycuxi += f'    {iqa__wfq} = f_reader.is_parallel()\n'
    else:
        aob__ycuxi += f'    {iqa__wfq} = {parallel}\n'
    aob__ycuxi += f'    astype(df, typemap, {iqa__wfq})\n'
    for sohkv__okdqj, jgxof__myl in zip(usecols, sanitized_cnames):
        aob__ycuxi += '    {} = df[{}].values\n'.format(jgxof__myl,
            sohkv__okdqj)
    return aob__ycuxi


def _gen_parallel_flag_name(sanitized_cnames):
    iqa__wfq = '_parallel_value'
    while iqa__wfq in sanitized_cnames:
        iqa__wfq = '_' + iqa__wfq
    return iqa__wfq


def _gen_csv_reader_py(col_names, col_typs, usecols, sep, parallel, header,
    compression):
    sanitized_cnames = [sanitize_varname(znwzq__ynzin) for znwzq__ynzin in
        col_names]
    aob__ycuxi = 'def csv_reader_py(fname, nrows, skiprows):\n'
    aob__ycuxi += _gen_csv_file_reader_init(parallel, header, compression, -1)
    aob__ycuxi += _gen_read_csv_objmode(col_names, sanitized_cnames,
        col_typs, usecols, sep, parallel=parallel, check_parallel_runtime=False
        )
    aob__ycuxi += '  return ({},)\n'.format(', '.join(vxy__yzww for
        vxy__yzww in sanitized_cnames))
    sgii__bgw = globals()
    eyf__lfqpd = {}
    exec(aob__ycuxi, sgii__bgw, eyf__lfqpd)
    rmhf__gix = eyf__lfqpd['csv_reader_py']
    ifg__yupvc = numba.njit(rmhf__gix)
    compiled_funcs.append(ifg__yupvc)
    return ifg__yupvc
