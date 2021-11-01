import os
import warnings
from collections import defaultdict
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from numba.core import ir, types
from numba.core.ir_utils import compile_to_numba_ir, get_definition, guard, mk_unique_var, replace_arg_nodes
from numba.extending import NativeValue, intrinsic, models, overload, register_model, unbox
from pyarrow import null
import bodo
import bodo.ir.parquet_ext
import bodo.utils.tracing as tracing
from bodo.hiframes.datetime_date_ext import datetime_date_array_type, datetime_date_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.io.fs_io import get_hdfs_fs, get_s3_fs_from_path
from bodo.libs.array import delete_table, info_from_table, info_to_array, table_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.distributed_api import get_end, get_start
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.transforms import distributed_pass
from bodo.utils.transform import get_const_value
from bodo.utils.typing import BodoError, BodoWarning, FileInfo, get_overload_const_str, get_overload_constant_dict
from bodo.utils.utils import check_and_propagate_cpp_exception, numba_to_c_type, sanitize_varname
use_nullable_int_arr = True
from urllib.parse import urlparse
import bodo.io.pa_parquet


class ParquetPredicateType(types.Type):

    def __init__(self):
        super(ParquetPredicateType, self).__init__(name=
            'ParquetPredicateType()')


parquet_predicate_type = ParquetPredicateType()
types.parquet_predicate_type = parquet_predicate_type
register_model(ParquetPredicateType)(models.OpaqueModel)


@unbox(ParquetPredicateType)
def unbox_parquet_predicate_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


class StorageOptionsDictType(types.Opaque):

    def __init__(self):
        super(StorageOptionsDictType, self).__init__(name=
            'StorageOptionsDictType')


storage_options_dict_type = StorageOptionsDictType()
types.storage_options_dict_type = storage_options_dict_type
register_model(StorageOptionsDictType)(models.OpaqueModel)


@unbox(StorageOptionsDictType)
def unbox_storage_options_dict_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


class ParquetFileInfo(FileInfo):

    def __init__(self, columns, storage_options=None):
        self.columns = columns
        self.storage_options = storage_options

    def get_schema(self, fname):
        try:
            return parquet_file_schema(fname, selected_columns=self.columns,
                storage_options=self.storage_options)
        except OSError as zdx__ueeo:
            if 'non-file path' in str(zdx__ueeo):
                raise FileNotFoundError(str(zdx__ueeo))
            raise


class ParquetHandler:

    def __init__(self, func_ir, typingctx, args, _locals):
        self.func_ir = func_ir
        self.typingctx = typingctx
        self.args = args
        self.locals = _locals

    def gen_parquet_read(self, file_name, lhs, columns, storage_options=None):
        hhxj__bwc = lhs.scope
        rbqw__zlzwa = lhs.loc
        hvfi__qjr = None
        if lhs.name in self.locals:
            hvfi__qjr = self.locals[lhs.name]
            self.locals.pop(lhs.name)
        wdl__jqa = {}
        if lhs.name + ':convert' in self.locals:
            wdl__jqa = self.locals[lhs.name + ':convert']
            self.locals.pop(lhs.name + ':convert')
        if hvfi__qjr is None:
            sluwb__woi = (
                'Parquet schema not available. Either path argument should be constant for Bodo to look at the file at compile time or schema should be provided. For more information, see: https://docs.bodo.ai/latest/source/programming_with_bodo/file_io.html#non-constant-filepaths'
                )
            pmzm__ues = get_const_value(file_name, self.func_ir, sluwb__woi,
                arg_types=self.args, file_info=ParquetFileInfo(columns,
                storage_options=storage_options))
            jybd__pjxo = False
            urwf__sbry = guard(get_definition, self.func_ir, file_name)
            if isinstance(urwf__sbry, ir.Arg):
                typ = self.args[urwf__sbry.index]
                if isinstance(typ, types.FilenameType):
                    (col_names, fteqm__htbl, osax__isf, col_indices,
                        partition_names) = typ.schema
                    jybd__pjxo = True
            if not jybd__pjxo:
                (col_names, fteqm__htbl, osax__isf, col_indices,
                    partition_names) = (parquet_file_schema(pmzm__ues,
                    columns, storage_options=storage_options))
        else:
            pzb__hxmyz = list(hvfi__qjr.keys())
            wjlko__dri = [meq__fxn for meq__fxn in hvfi__qjr.values()]
            osax__isf = 'index' if 'index' in pzb__hxmyz else None
            if columns is None:
                selected_columns = pzb__hxmyz
            else:
                selected_columns = columns
            col_indices = [pzb__hxmyz.index(c) for c in selected_columns]
            fteqm__htbl = [wjlko__dri[pzb__hxmyz.index(c)] for c in
                selected_columns]
            col_names = selected_columns
            osax__isf = osax__isf if osax__isf in col_names else None
            partition_names = []
        for tcc__qmql, c in enumerate(col_names):
            if c in wdl__jqa:
                fteqm__htbl[tcc__qmql] = wdl__jqa[c]
        svsvd__yrh = [ir.Var(hhxj__bwc, mk_unique_var(c), rbqw__zlzwa) for
            c in col_names]
        hpk__ycp = [bodo.ir.parquet_ext.ParquetReader(file_name, lhs.name,
            col_names, col_indices, fteqm__htbl, svsvd__yrh, rbqw__zlzwa,
            partition_names, storage_options)]
        return col_names, svsvd__yrh, osax__isf, hpk__ycp


def pq_distributed_run(pq_node, array_dists, typemap, calltypes, typingctx,
    targetctx, meta_head_only_info=None):
    puhr__alnuj = len(pq_node.out_vars)
    extra_args = ''
    filter_str = 'None'
    yalvi__hwmna, yzubw__dmt = bodo.ir.connector.generate_filter_map(pq_node
        .filters)
    extra_args = ', '.join(yalvi__hwmna.values())
    if yalvi__hwmna:
        filter_str = '[{}]'.format(', '.join('[{}]'.format(', '.join(
            f"('{vfawu__lbbm[0]}', '{vfawu__lbbm[1]}', {yalvi__hwmna[vfawu__lbbm[2].name]})"
             for vfawu__lbbm in ssiiz__clq)) for ssiiz__clq in pq_node.filters)
            )
        extra_args = ', '.join(yalvi__hwmna.values())
    fwl__rls = ', '.join(f'out{tcc__qmql}' for tcc__qmql in range(puhr__alnuj))
    qksoq__jkzjb = f'def pq_impl(fname, {extra_args}):\n'
    qksoq__jkzjb += (
        f'    (total_rows, {fwl__rls},) = _pq_reader_py(fname, {extra_args})\n'
        )
    tpzw__duh = {}
    exec(qksoq__jkzjb, {}, tpzw__duh)
    engog__ykxh = tpzw__duh['pq_impl']
    parallel = []
    if array_dists is not None:
        parallel = [c for c, vfawu__lbbm in zip(pq_node.col_names, pq_node.
            out_vars) if array_dists[vfawu__lbbm.name] in (distributed_pass
            .Distribution.OneD, distributed_pass.Distribution.OneD_Var)]
    fqggn__rbie = _gen_pq_reader_py(pq_node.col_names, pq_node.col_indices,
        pq_node.out_types, pq_node.storage_options, pq_node.partition_names,
        filter_str, extra_args, typingctx, targetctx, parallel,
        meta_head_only_info)
    diolp__wqyc = (string_type,) + tuple(typemap[vfawu__lbbm.name] for
        vfawu__lbbm in yzubw__dmt)
    qyjl__vltc = compile_to_numba_ir(engog__ykxh, {'_pq_reader_py':
        fqggn__rbie}, typingctx=typingctx, targetctx=targetctx, arg_typs=
        diolp__wqyc, typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(qyjl__vltc, [pq_node.file_name] + yzubw__dmt)
    hpk__ycp = qyjl__vltc.body[:-3]
    if meta_head_only_info:
        hpk__ycp[-1 - puhr__alnuj].target = meta_head_only_info[1]
    for tcc__qmql in range(puhr__alnuj):
        hpk__ycp[tcc__qmql - puhr__alnuj].target = pq_node.out_vars[tcc__qmql]
    return hpk__ycp


distributed_pass.distributed_run_extensions[bodo.ir.parquet_ext.ParquetReader
    ] = pq_distributed_run


def get_filters_pyobject(filters, vars):
    pass


@overload(get_filters_pyobject, no_unliteral=True)
def overload_get_filters_pyobject(filter_str, var_tup):
    yzc__nyjrn = get_overload_const_str(filter_str)
    kpehs__forkh = ', '.join(f'f{tcc__qmql}' for tcc__qmql in range(len(
        var_tup)))
    qksoq__jkzjb = 'def impl(filter_str, var_tup):\n'
    if len(var_tup):
        qksoq__jkzjb += f'  {kpehs__forkh}, = var_tup\n'
    qksoq__jkzjb += (
        "  with numba.objmode(filters_py='parquet_predicate_type'):\n")
    qksoq__jkzjb += f'    filters_py = {yzc__nyjrn}\n'
    qksoq__jkzjb += '  return filters_py\n'
    tpzw__duh = {}
    exec(qksoq__jkzjb, globals(), tpzw__duh)
    return tpzw__duh['impl']


def get_storage_options_pyobject(storage_options):
    pass


@overload(get_storage_options_pyobject, no_unliteral=True)
def overload_get_storage_options_pyobject(storage_options):
    wqlru__irdcl = get_overload_constant_dict(storage_options)
    qksoq__jkzjb = 'def impl(storage_options):\n'
    qksoq__jkzjb += (
        "  with numba.objmode(storage_options_py='storage_options_dict_type'):\n"
        )
    qksoq__jkzjb += f'    storage_options_py = {str(wqlru__irdcl)}\n'
    qksoq__jkzjb += '  return storage_options_py\n'
    tpzw__duh = {}
    exec(qksoq__jkzjb, globals(), tpzw__duh)
    return tpzw__duh['impl']


def _gen_pq_reader_py(col_names, col_indices, out_types, storage_options,
    partition_names, filter_str, extra_args, typingctx, targetctx, parallel,
    meta_head_only_info):
    if len(parallel) > 0:
        assert col_names == parallel
    is_parallel = len(parallel) > 0
    lbh__oqftj = ',' if extra_args else ''
    qksoq__jkzjb = f'def pq_reader_py(fname,{extra_args}):\n'
    qksoq__jkzjb += (
        f"    ev = bodo.utils.tracing.Event('read_parquet', {is_parallel})\n")
    qksoq__jkzjb += "    ev.add_attribute('fname', fname)\n"
    qksoq__jkzjb += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={is_parallel})
"""
    qksoq__jkzjb += f"""    filters = get_filters_pyobject("{filter_str}", ({extra_args}{lbh__oqftj}))
"""
    storage_options['bodo_dummy'] = 'dummy'
    qksoq__jkzjb += f"""    storage_options_py = get_storage_options_pyobject({str(storage_options)})
"""
    uhn__jzlsk = -1
    if meta_head_only_info and meta_head_only_info[0] is not None:
        uhn__jzlsk = meta_head_only_info[0]
    ieve__awdut = [sanitize_varname(c) for c in col_names]
    partition_names = [sanitize_varname(c) for c in partition_names]
    ceklr__twol = {}
    for ljmx__cfsa, ypk__nbhql in zip(col_indices, out_types):
        ceklr__twol[f'col_{ljmx__cfsa}_type'] = ypk__nbhql
    wzpeb__dizny = sorted([ljmx__cfsa for pfnu__jsv, ljmx__cfsa in zip(
        ieve__awdut, col_indices) if pfnu__jsv not in partition_names])

    def is_nullable(typ):
        return bodo.utils.utils.is_array_typ(typ, False) and not isinstance(typ
            , types.Array)
    fdzgm__djc = [int(is_nullable(out_types[col_indices.index(ljmx__cfsa)])
        ) for ljmx__cfsa in wzpeb__dizny]
    idwn__wpgh = []
    caeld__xod = []
    zhnks__idihq = []
    for tcc__qmql, ptn__icb in enumerate(partition_names):
        try:
            jym__ucxj = ieve__awdut.index(ptn__icb)
        except ValueError as lvug__udkzx:
            continue
        idwn__wpgh.append(ptn__icb)
        caeld__xod.append(tcc__qmql)
        dlp__llec = out_types[jym__ucxj].dtype
        srybg__uswvd = (bodo.hiframes.pd_categorical_ext.
            get_categories_int_type(dlp__llec))
        zhnks__idihq.append(numba_to_c_type(srybg__uswvd))
    qksoq__jkzjb += f'    total_rows_np = np.array([0], dtype=np.int64)\n'
    if len(caeld__xod) > 0:
        qksoq__jkzjb += f"""    out_table = pq_read(unicode_to_utf8(fname), {is_parallel}, unicode_to_utf8(bucket_region), filters, storage_options_py, {uhn__jzlsk}, np.array({wzpeb__dizny}, dtype=np.int32).ctypes, {len(wzpeb__dizny)}, np.array({fdzgm__djc}, dtype=np.int32).ctypes, np.array({caeld__xod}, dtype=np.int32).ctypes, np.array({zhnks__idihq}, dtype=np.int32).ctypes, {len(caeld__xod)}, total_rows_np.ctypes)
"""
    else:
        qksoq__jkzjb += f"""    out_table = pq_read(unicode_to_utf8(fname), {is_parallel}, unicode_to_utf8(bucket_region), filters, storage_options_py, {uhn__jzlsk}, np.array({wzpeb__dizny}, dtype=np.int32).ctypes, {len(wzpeb__dizny)}, np.array({fdzgm__djc}, dtype=np.int32).ctypes, 0, 0, 0, total_rows_np.ctypes)
"""
    qksoq__jkzjb += '    check_and_propagate_cpp_exception()\n'
    for tcc__qmql, ljmx__cfsa in enumerate(wzpeb__dizny):
        pfnu__jsv = ieve__awdut[col_indices.index(ljmx__cfsa)]
        qksoq__jkzjb += f"""    {pfnu__jsv} = info_to_array(info_from_table(out_table, {tcc__qmql}), col_{ljmx__cfsa}_type)
"""
    for tcc__qmql, pfnu__jsv in enumerate(idwn__wpgh):
        ljmx__cfsa = col_indices[ieve__awdut.index(pfnu__jsv)]
        qksoq__jkzjb += f"""    {pfnu__jsv} = info_to_array(info_from_table(out_table, {tcc__qmql + len(wzpeb__dizny)}), col_{ljmx__cfsa}_type)
"""
    qksoq__jkzjb += '    delete_table(out_table)\n'
    qksoq__jkzjb += f'    total_rows = total_rows_np[0]\n'
    qksoq__jkzjb += f'    ev.finalize()\n'
    qksoq__jkzjb += '    return (total_rows, {},)\n'.format(', '.join(
        ieve__awdut))
    tpzw__duh = {}
    acezx__vdq = {'info_to_array': info_to_array, 'info_from_table':
        info_from_table, 'delete_table': delete_table,
        'check_and_propagate_cpp_exception':
        check_and_propagate_cpp_exception, 'pq_read': _pq_read,
        'unicode_to_utf8': unicode_to_utf8, 'get_filters_pyobject':
        get_filters_pyobject, 'get_storage_options_pyobject':
        get_storage_options_pyobject, 'np': np, 'pd': pd, 'bodo': bodo}
    acezx__vdq.update(ceklr__twol)
    exec(qksoq__jkzjb, acezx__vdq, tpzw__duh)
    fqggn__rbie = tpzw__duh['pq_reader_py']
    sxbd__uwjcb = numba.njit(fqggn__rbie, no_cpython_wrapper=True)
    return sxbd__uwjcb


def _get_numba_typ_from_pa_typ(pa_typ, is_index, nullable_from_metadata,
    category_info):
    import pyarrow as pa
    if isinstance(pa_typ.type, pa.ListType):
        return ArrayItemArrayType(_get_numba_typ_from_pa_typ(pa_typ.type.
            value_field, is_index, nullable_from_metadata, category_info))
    if isinstance(pa_typ.type, pa.StructType):
        tkl__vqbij = []
        yxj__ewmrx = []
        for mkxth__vxdxc in pa_typ.flatten():
            yxj__ewmrx.append(mkxth__vxdxc.name.split('.')[-1])
            tkl__vqbij.append(_get_numba_typ_from_pa_typ(mkxth__vxdxc,
                is_index, nullable_from_metadata, category_info))
        return StructArrayType(tuple(tkl__vqbij), tuple(yxj__ewmrx))
    if isinstance(pa_typ.type, pa.Decimal128Type):
        return DecimalArrayType(pa_typ.type.precision, pa_typ.type.scale)
    xmh__hri = {pa.bool_(): types.bool_, pa.int8(): types.int8, pa.int16():
        types.int16, pa.int32(): types.int32, pa.int64(): types.int64, pa.
        uint8(): types.uint8, pa.uint16(): types.uint16, pa.uint32(): types
        .uint32, pa.uint64(): types.uint64, pa.float32(): types.float32, pa
        .float64(): types.float64, pa.string(): string_type, pa.binary():
        bytes_type, pa.date32(): datetime_date_type, pa.date64(): types.
        NPDatetime('ns'), pa.timestamp('ns'): types.NPDatetime('ns'), pa.
        timestamp('us'): types.NPDatetime('ns'), pa.timestamp('ms'): types.
        NPDatetime('ns'), pa.timestamp('s'): types.NPDatetime('ns'), null():
        string_type}
    if isinstance(pa_typ.type, pa.DictionaryType):
        if pa_typ.type.value_type != pa.string():
            raise BodoError(
                f'Parquet Categorical data type should be string, not {pa_typ.type.value_type}'
                )
        mtnmn__rqg = xmh__hri[pa_typ.type.index_type]
        qmxfc__wkb = PDCategoricalDtype(category_info[pa_typ.name], bodo.
            string_type, pa_typ.type.ordered, int_type=mtnmn__rqg)
        return CategoricalArrayType(qmxfc__wkb)
    if pa_typ.type not in xmh__hri:
        raise BodoError('Arrow data type {} not supported yet'.format(
            pa_typ.type))
    mxm__qkcr = xmh__hri[pa_typ.type]
    if mxm__qkcr == datetime_date_type:
        return datetime_date_array_type
    if mxm__qkcr == bytes_type:
        return binary_array_type
    cwah__eaypx = (string_array_type if mxm__qkcr == string_type else types
        .Array(mxm__qkcr, 1, 'C'))
    if mxm__qkcr == types.bool_:
        cwah__eaypx = boolean_array
    if nullable_from_metadata is not None:
        tkh__fjp = nullable_from_metadata
    else:
        tkh__fjp = use_nullable_int_arr
    if tkh__fjp and not is_index and isinstance(mxm__qkcr, types.Integer
        ) and pa_typ.nullable:
        cwah__eaypx = IntegerArrayType(mxm__qkcr)
    return cwah__eaypx


def get_parquet_dataset(fpath, get_row_counts=True, filters=None,
    storage_options=None, read_categories=False, is_parallel=False):
    if get_row_counts:
        xmeo__qvc = tracing.Event('get_parquet_dataset')
    import pyarrow as pa
    import pyarrow.parquet as pq
    from mpi4py import MPI
    msw__jmuy = MPI.COMM_WORLD
    fpath = fpath.rstrip('/')
    if fpath.startswith('gs://'):
        fpath = fpath[:1] + 'c' + fpath[1:]
    if fpath.startswith('gcs://'):
        try:
            import gcsfs
        except ImportError as lvug__udkzx:
            vmmi__exds = """Couldn't import gcsfs, which is required for Google cloud access. gcsfs can be installed by calling 'conda install -c conda-forge gcsfs'.
"""
            raise BodoError(vmmi__exds)
    if fpath.startswith('http://'):
        try:
            import fsspec
        except ImportError as lvug__udkzx:
            vmmi__exds = """Couldn't import fsspec, which is required for http access. fsspec can be installed by calling 'conda install -c conda-forge fsspec'.
"""
    mwbc__voe = []

    def getfs(parallel=False):
        if len(mwbc__voe) == 1:
            return mwbc__voe[0]
        if fpath.startswith('s3://'):
            mwbc__voe.append(get_s3_fs_from_path(fpath, parallel=parallel,
                storage_options=storage_options))
        elif fpath.startswith('gcs://'):
            kba__lee = gcsfs.GCSFileSystem(token=None)
            mwbc__voe.append(kba__lee)
        elif fpath.startswith('http://'):
            mwbc__voe.append(fsspec.filesystem('http'))
        elif fpath.startswith('hdfs://') or fpath.startswith('abfs://'
            ) or fpath.startswith('abfss://'):
            mwbc__voe.append(get_hdfs_fs(fpath))
        else:
            mwbc__voe.append(None)
        return mwbc__voe[0]
    rqka__rzvww = bodo.parquet_validate_schema
    if get_row_counts or rqka__rzvww:
        obbiu__hjsrq = getfs(parallel=True)
    if bodo.get_rank() == 0:
        mco__whmd = 1
        xnt__vkt = os.cpu_count()
        if xnt__vkt is not None and xnt__vkt > 1:
            mco__whmd = xnt__vkt // 2
        try:
            if get_row_counts:
                tjapq__uaov = tracing.Event('pq.ParquetDataset',
                    is_parallel=False)
            zos__gjrn = pa.io_thread_count()
            pa.set_io_thread_count(mco__whmd)
            fzu__neduw = pq.ParquetDataset(fpath, filesystem=getfs(),
                filters=filters, use_legacy_dataset=True, validate_schema=
                False, metadata_nthreads=mco__whmd)
            pa.set_io_thread_count(zos__gjrn)
            if get_row_counts:
                tjapq__uaov.finalize()
            zwt__hvyvs = bodo.io.pa_parquet.get_dataset_schema(fzu__neduw)
            fzu__neduw._metadata.fs = None
        except Exception as zdx__ueeo:
            msw__jmuy.bcast(zdx__ueeo)
            raise BodoError(
                f'error from pyarrow: {type(zdx__ueeo).__name__}: {str(zdx__ueeo)}\n'
                )
        if get_row_counts:
            bffih__qwfls = tracing.Event('bcast dataset')
        msw__jmuy.bcast(fzu__neduw)
        msw__jmuy.bcast(zwt__hvyvs)
    else:
        if get_row_counts:
            bffih__qwfls = tracing.Event('bcast dataset')
        fzu__neduw = msw__jmuy.bcast(None)
        if isinstance(fzu__neduw, Exception):
            nrci__nfg = fzu__neduw
            raise BodoError(
                f'error from pyarrow: {type(nrci__nfg).__name__}: {str(nrci__nfg)}\n'
                )
        zwt__hvyvs = msw__jmuy.bcast(None)
    if get_row_counts:
        bffih__qwfls.finalize()
    fzu__neduw._bodo_total_rows = 0
    if get_row_counts or rqka__rzvww:
        if get_row_counts:
            cgyxg__hbm = tracing.Event('get_row_counts')
        num_pieces = len(fzu__neduw.pieces)
        start = get_start(num_pieces, bodo.get_size(), bodo.get_rank())
        elyun__yiic = get_end(num_pieces, bodo.get_size(), bodo.get_rank())
        mth__lizck = 0
        bmz__cxu = 0
        addg__hsu = []
        crcm__khxg = True
        fzu__neduw._metadata.fs = getfs()
        for czp__gyuaj in fzu__neduw.pieces[start:elyun__yiic]:
            ruhwu__pxzxz = czp__gyuaj.get_metadata()
            if get_row_counts:
                addg__hsu.append(ruhwu__pxzxz.num_rows)
                mth__lizck += ruhwu__pxzxz.num_rows
                bmz__cxu += ruhwu__pxzxz.num_row_groups
            if rqka__rzvww:
                ffqzd__btn = ruhwu__pxzxz.schema.to_arrow_schema()
                if zwt__hvyvs != ffqzd__btn:
                    print('Schema in {!s} was different. \n{!s}\n\nvs\n\n{!s}'
                        .format(czp__gyuaj, ffqzd__btn, zwt__hvyvs))
                    crcm__khxg = False
                    break
        if rqka__rzvww:
            crcm__khxg = msw__jmuy.allreduce(crcm__khxg, op=MPI.LAND)
            if not crcm__khxg:
                raise BodoError("Schema in parquet files don't match")
        if get_row_counts:
            fzu__neduw._bodo_total_rows = msw__jmuy.allreduce(mth__lizck,
                op=MPI.SUM)
            emfea__log = msw__jmuy.allreduce(bmz__cxu, op=MPI.SUM)
            if is_parallel and bodo.get_rank(
                ) == 0 and emfea__log < bodo.get_size():
                warnings.warn(BodoWarning(
                    f"""Total number of row groups in parquet dataset {fpath} ({emfea__log}) is too small for effective IO parallelization.
For best performance the number of row groups should be greater than the number of workers ({bodo.get_size()})
"""
                    ))
            mlzoj__mjwl = msw__jmuy.allgather(addg__hsu)
            for tcc__qmql, bhmz__daj in enumerate([skg__cktt for kvdi__tpr in
                mlzoj__mjwl for skg__cktt in kvdi__tpr]):
                fzu__neduw.pieces[tcc__qmql]._bodo_num_rows = bhmz__daj
            cgyxg__hbm.add_attribute('total_num_row_groups', emfea__log)
            cgyxg__hbm.finalize()
    xkzp__glng = urlparse(fpath)
    fzu__neduw._prefix = ''
    if xkzp__glng.scheme in ['hdfs']:
        nsn__yth = f'{xkzp__glng.scheme}://{xkzp__glng.netloc}'
        if len(fzu__neduw.pieces) > 0:
            jloo__cayg = fzu__neduw.pieces[0]
            if not jloo__cayg.path.startswith(nsn__yth):
                fzu__neduw._prefix = nsn__yth
    if read_categories:
        _add_categories_to_pq_dataset(fzu__neduw)
    if get_row_counts:
        xmeo__qvc.finalize()
    return fzu__neduw


def _add_categories_to_pq_dataset(pq_dataset):
    import pyarrow as pa
    from mpi4py import MPI
    if len(pq_dataset.pieces) < 1:
        raise BodoError(
            'No pieces found in Parquet dataset. Cannot get read categorical values'
            )
    dkmp__ngnk = pq_dataset.schema.to_arrow_schema()
    svefu__dnmix = [c for c in dkmp__ngnk.names if isinstance(dkmp__ngnk.
        field(c).type, pa.DictionaryType)]
    if len(svefu__dnmix) == 0:
        pq_dataset._category_info = {}
        return
    msw__jmuy = MPI.COMM_WORLD
    if bodo.get_rank() == 0:
        try:
            gfqyx__tfdeg = pq_dataset.pieces[0].open()
            uuz__vumh = gfqyx__tfdeg.read_row_group(0, svefu__dnmix)
            category_info = {c: tuple(uuz__vumh.column(c).chunk(0).
                dictionary.to_pylist()) for c in svefu__dnmix}
            del gfqyx__tfdeg, uuz__vumh
        except Exception as zdx__ueeo:
            msw__jmuy.bcast(zdx__ueeo)
            raise zdx__ueeo
        msw__jmuy.bcast(category_info)
    else:
        category_info = msw__jmuy.bcast(None)
        if isinstance(category_info, Exception):
            nrci__nfg = category_info
            raise nrci__nfg
    pq_dataset._category_info = category_info


def get_pandas_metadata(schema, num_pieces):
    osax__isf = None
    nullable_from_metadata = defaultdict(lambda : None)
    sfm__psa = b'pandas'
    if schema.metadata is not None and sfm__psa in schema.metadata:
        import json
        skq__zxbf = json.loads(schema.metadata[sfm__psa].decode('utf8'))
        bbnyu__cmgzu = len(skq__zxbf['index_columns'])
        if bbnyu__cmgzu > 1:
            raise BodoError('read_parquet: MultiIndex not supported yet')
        osax__isf = skq__zxbf['index_columns'][0] if bbnyu__cmgzu else None
        if not isinstance(osax__isf, str) and (not isinstance(osax__isf,
            dict) or num_pieces != 1):
            osax__isf = None
        for haxsz__qdqg in skq__zxbf['columns']:
            vxpix__bgewi = haxsz__qdqg['name']
            if haxsz__qdqg['pandas_type'].startswith('int'
                ) and vxpix__bgewi is not None:
                if haxsz__qdqg['numpy_type'].startswith('Int'):
                    nullable_from_metadata[vxpix__bgewi] = True
                else:
                    nullable_from_metadata[vxpix__bgewi] = False
    return osax__isf, nullable_from_metadata


def parquet_file_schema(file_name, selected_columns, storage_options=None):
    col_names = []
    fteqm__htbl = []
    pq_dataset = get_parquet_dataset(file_name, get_row_counts=False,
        storage_options=storage_options, read_categories=True)
    partition_names = [] if pq_dataset.partitions is None else [pq_dataset.
        partitions.levels[tcc__qmql].name for tcc__qmql in range(len(
        pq_dataset.partitions.partition_names))]
    dkmp__ngnk = pq_dataset.schema.to_arrow_schema()
    num_pieces = len(pq_dataset.pieces)
    col_names = dkmp__ngnk.names
    osax__isf, nullable_from_metadata = get_pandas_metadata(dkmp__ngnk,
        num_pieces)
    wjlko__dri = [_get_numba_typ_from_pa_typ(dkmp__ngnk.field(c), c ==
        osax__isf, nullable_from_metadata[c], pq_dataset._category_info) for
        c in col_names]
    if partition_names:
        col_names += partition_names
        wjlko__dri += [_get_partition_cat_dtype(pq_dataset.partitions.
            levels[tcc__qmql]) for tcc__qmql in range(len(partition_names))]
    if selected_columns is None:
        selected_columns = col_names
    for c in selected_columns:
        if c not in col_names:
            raise BodoError('Selected column {} not in Parquet file schema'
                .format(c))
    if osax__isf and not isinstance(osax__isf, dict
        ) and osax__isf not in selected_columns:
        selected_columns.append(osax__isf)
    col_indices = [col_names.index(c) for c in selected_columns]
    fteqm__htbl = [wjlko__dri[col_names.index(c)] for c in selected_columns]
    col_names = selected_columns
    return col_names, fteqm__htbl, osax__isf, col_indices, partition_names


def _get_partition_cat_dtype(part_set):
    wwlt__ooay = part_set.dictionary.to_pandas()
    mss__krro = bodo.typeof(wwlt__ooay).dtype
    qmxfc__wkb = PDCategoricalDtype(tuple(wwlt__ooay), mss__krro, False)
    return CategoricalArrayType(qmxfc__wkb)


_pq_read = types.ExternalFunction('pq_read', table_type(types.voidptr,
    types.boolean, types.voidptr, parquet_predicate_type,
    storage_options_dict_type, types.int64, types.voidptr, types.int32,
    types.voidptr, types.voidptr, types.voidptr, types.int32, types.voidptr))
from llvmlite import ir as lir
from numba.core import cgutils
if bodo.utils.utils.has_pyarrow():
    from bodo.io import arrow_cpp
    ll.add_symbol('pq_read', arrow_cpp.pq_read)
    ll.add_symbol('pq_write', arrow_cpp.pq_write)
    ll.add_symbol('pq_write_partitioned', arrow_cpp.pq_write_partitioned)


@intrinsic
def parquet_write_table_cpp(typingctx, filename_t, table_t, col_names_t,
    index_t, write_index, metadata_t, compression_t, is_parallel_t,
    write_range_index, start, stop, step, name, bucket_region):

    def codegen(context, builder, sig, args):
        lud__xtc = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(32), lir.IntType(32),
            lir.IntType(32), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer()])
        yxds__zbmy = cgutils.get_or_insert_function(builder.module,
            lud__xtc, name='pq_write')
        builder.call(yxds__zbmy, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, table_t, col_names_t, index_t, types.
        boolean, types.voidptr, types.voidptr, types.boolean, types.boolean,
        types.int32, types.int32, types.int32, types.voidptr, types.voidptr
        ), codegen


@intrinsic
def parquet_write_table_partitioned_cpp(typingctx, filename_t, data_table_t,
    col_names_t, col_names_no_partitions_t, cat_table_t, part_col_idxs_t,
    num_part_col_t, compression_t, is_parallel_t, bucket_region):

    def codegen(context, builder, sig, args):
        lud__xtc = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer()])
        yxds__zbmy = cgutils.get_or_insert_function(builder.module,
            lud__xtc, name='pq_write_partitioned')
        builder.call(yxds__zbmy, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, data_table_t, col_names_t,
        col_names_no_partitions_t, cat_table_t, types.voidptr, types.int32,
        types.voidptr, types.boolean, types.voidptr), codegen
