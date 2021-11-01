"""IR node for the parquet data access"""
import numba
from numba.core import ir, ir_utils, typeinfer
import bodo
import bodo.ir.connector
from bodo.transforms import distributed_analysis


class ParquetReader(ir.Stmt):

    def __init__(self, file_name, df_out, col_names, col_indices, out_types,
        out_vars, loc, partition_names=None, storage_options=None):
        self.connector_typ = 'parquet'
        self.file_name = file_name
        self.df_out = df_out
        self.col_names = col_names
        self.col_indices = col_indices
        self.out_types = out_types
        self.out_vars = out_vars
        self.loc = loc
        self.partition_names = partition_names
        self.filters = None
        self.storage_options = storage_options

    def __repr__(self):
        return '({}) = ReadParquet({}, {}, {}, {}, {}, {}, {}, {})'.format(self
            .df_out, self.file_name.name, self.col_names, self.col_indices,
            self.out_types, self.out_vars, self.partition_names, self.
            filters, self.storage_options)


def remove_dead_pq(pq_node, lives_no_aliases, lives, arg_aliases, alias_map,
    func_ir, typemap):
    eekef__uay = []
    sxo__apxlw = []
    yyzdu__fnpq = []
    vij__bquf = []
    for jik__hsyr, qbu__nmao in enumerate(pq_node.out_vars):
        if qbu__nmao.name in lives:
            eekef__uay.append(pq_node.col_names[jik__hsyr])
            sxo__apxlw.append(pq_node.out_vars[jik__hsyr])
            yyzdu__fnpq.append(pq_node.out_types[jik__hsyr])
            vij__bquf.append(pq_node.col_indices[jik__hsyr])
    pq_node.col_names = eekef__uay
    pq_node.out_vars = sxo__apxlw
    pq_node.out_types = yyzdu__fnpq
    pq_node.col_indices = vij__bquf
    if len(pq_node.out_vars) == 0:
        return None
    return pq_node


numba.parfors.array_analysis.array_analysis_extensions[ParquetReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[ParquetReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[ParquetReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[ParquetReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[ParquetReader] = remove_dead_pq
numba.core.analysis.ir_extension_usedefs[ParquetReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[ParquetReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[ParquetReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[ParquetReader
    ] = bodo.ir.connector.build_connector_definitions
