"""
Class information for DataFrame iterators returned by pd.read_csv. This is used
to handle situations in which pd.read_csv is used to return chunks with separate
read calls instead of just a single read.
"""
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import RefType, impl_ret_borrowed, iternext_impl
from numba.core.typing.templates import signature
from numba.extending import intrinsic, lower_builtin, models, register_model
import bodo
import bodo.ir.connector
import bodo.ir.csv_ext
from bodo import objmode
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.io import csv_cpp
from bodo.ir.csv_ext import _gen_read_csv_objmode, astype
from bodo.utils.transform import gen_const_tup
from bodo.utils.utils import check_java_installation
from bodo.utils.utils import sanitize_varname
ll.add_symbol('update_csv_reader', csv_cpp.update_csv_reader)
ll.add_symbol('initialize_csv_reader', csv_cpp.initialize_csv_reader)


class CSVIteratorType(types.SimpleIteratorType):

    def __init__(self, df_type, out_colnames, out_types, usecols, sep,
        index_ind):
        assert isinstance(df_type, DataFrameType
            ), 'CSVIterator must return a DataFrame'
        qyph__oant = (
            f'CSVIteratorType({df_type}, {out_colnames}, {out_types}, {usecols}, {sep}, {index_ind})'
            )
        super(types.SimpleIteratorType, self).__init__(qyph__oant)
        self._yield_type = df_type
        self._out_colnames = out_colnames
        self._out_types = out_types
        self._usecols = usecols
        self._sep = sep
        self._index_ind = index_ind


@register_model(CSVIteratorType)
class CSVIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        mvzgx__wtrki = [('csv_reader', bodo.ir.connector.stream_reader_type
            ), ('index', types.EphemeralPointer(types.uintp))]
        super(CSVIteratorModel, self).__init__(dmm, fe_type, mvzgx__wtrki)


@lower_builtin('getiter', CSVIteratorType)
def getiter_csv_iterator(context, builder, sig, args):
    ioinw__ongh = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    jgai__orn = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer()])
    uik__srx = cgutils.get_or_insert_function(builder.module, jgai__orn,
        name='initialize_csv_reader')
    builder.call(uik__srx, [ioinw__ongh.csv_reader])
    builder.store(context.get_constant(types.uint64, 0), ioinw__ongh.index)
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', CSVIteratorType)
@iternext_impl(RefType.NEW)
def iternext_csv_iterator(context, builder, sig, args, result):
    [hnk__ibx] = sig.args
    [yft__mzgb] = args
    ioinw__ongh = cgutils.create_struct_proxy(hnk__ibx)(context, builder,
        value=yft__mzgb)
    jgai__orn = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer()])
    uik__srx = cgutils.get_or_insert_function(builder.module, jgai__orn,
        name='update_csv_reader')
    qmo__cfnv = builder.call(uik__srx, [ioinw__ongh.csv_reader])
    result.set_valid(qmo__cfnv)
    with builder.if_then(qmo__cfnv):
        kscb__ccfa = builder.load(ioinw__ongh.index)
        fnqa__zbguc = types.Tuple([sig.return_type.first_type, types.int64])
        werql__iso = gen_read_csv_objmode(sig.args[0])
        elon__vigsd = signature(fnqa__zbguc, bodo.ir.connector.
            stream_reader_type, types.int64)
        mmb__tjaq = context.compile_internal(builder, werql__iso,
            elon__vigsd, [ioinw__ongh.csv_reader, kscb__ccfa])
        mom__ktl, fmkw__dnon = cgutils.unpack_tuple(builder, mmb__tjaq)
        buq__zbb = builder.add(kscb__ccfa, fmkw__dnon, flags=['nsw'])
        builder.store(buq__zbb, ioinw__ongh.index)
        result.yield_(mom__ktl)


@intrinsic
def init_csv_iterator(typingctx, csv_reader, csv_iterator_typeref):

    def codegen(context, builder, signature, args):
        iutab__szx = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        iutab__szx.csv_reader = args[0]
        fvaj__vpuh = context.get_constant(types.uintp, 0)
        iutab__szx.index = cgutils.alloca_once_value(builder, fvaj__vpuh)
        return iutab__szx._getvalue()
    assert isinstance(csv_iterator_typeref, types.TypeRef
        ), 'Initializing a csv iterator requires a typeref'
    avq__mqh = csv_iterator_typeref.instance_type
    sig = signature(avq__mqh, csv_reader, csv_iterator_typeref)
    return sig, codegen


def gen_read_csv_objmode(csv_iterator_type):
    jto__yam = 'def read_csv_objmode(f_reader):\n'
    bxs__rcovj = [sanitize_varname(aoiom__ctu) for aoiom__ctu in
        csv_iterator_type._out_colnames]
    jto__yam += _gen_read_csv_objmode(csv_iterator_type._out_colnames,
        bxs__rcovj, csv_iterator_type._out_types, csv_iterator_type.
        _usecols, csv_iterator_type._sep, parallel=False,
        check_parallel_runtime=True)
    jpo__exhe = bodo.ir.csv_ext._gen_parallel_flag_name(bxs__rcovj)
    tht__bcyv = bxs__rcovj + [jpo__exhe]
    jto__yam += f"  return {', '.join(tht__bcyv)}"
    ubh__jhhsj = globals()
    tfnju__retp = {}
    exec(jto__yam, ubh__jhhsj, tfnju__retp)
    orwta__dmgw = tfnju__retp['read_csv_objmode']
    qld__ldu = numba.njit(orwta__dmgw)
    bodo.ir.csv_ext.compiled_funcs.append(qld__ldu)
    szz__kodz = 'def read_func(reader, local_start):\n'
    szz__kodz += f"  {', '.join(tht__bcyv)} = objmode_func(reader)\n"
    index_ind = csv_iterator_type._index_ind
    if index_ind == -1:
        szz__kodz += f'  local_len = len({bxs__rcovj[0]})\n'
        szz__kodz += '  total_size = local_len\n'
        szz__kodz += f'  if ({jpo__exhe}):\n'
        szz__kodz += """    local_start = local_start + bodo.libs.distributed_api.dist_exscan(local_len, _op)
"""
        szz__kodz += (
            '    total_size = bodo.libs.distributed_api.dist_reduce(local_len, _op)\n'
            )
        vgbne__xlqv = (
            f'bodo.hiframes.pd_index_ext.init_range_index(local_start, local_start + local_len, 1, None)'
            )
        opv__mqj = bxs__rcovj
    else:
        vgbne__xlqv = (
            f'bodo.utils.conversion.convert_to_index({bxs__rcovj[index_ind]}, {csv_iterator_type._out_colnames[index_ind]}:!r)'
            )
        opv__mqj = bxs__rcovj[:index_ind] + bxs__rcovj[index_ind + 1:]
    efw__ksvz = gen_const_tup(csv_iterator_type.yield_type.columns)
    szz__kodz += (
        """  return (bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), {}, {}), total_size)
"""
        .format(', '.join(opv__mqj), vgbne__xlqv, efw__ksvz))
    exec(szz__kodz, {'bodo': bodo, 'objmode_func': qld__ldu, '_op': np.
        int32(bodo.libs.distributed_api.Reduce_Type.Sum.value)}, tfnju__retp)
    return tfnju__retp['read_func']
