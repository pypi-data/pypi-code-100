"""
Defines Bodo's compiler pipeline.
"""
import os
import warnings
from collections import namedtuple
import numba
from numba.core import ir, ir_utils
from numba.core.compiler import DefaultPassBuilder
from numba.core.compiler_machinery import AnalysisPass, FunctionPass, register_pass
from numba.core.inline_closurecall import inline_closure_call
from numba.core.ir_utils import build_definitions, find_callname, get_definition, guard
from numba.core.registry import CPUDispatcher
from numba.core.typed_passes import DumpParforDiagnostics, InlineOverloads, NopythonTypeInference, ParforPass, PreParforPass
from numba.core.untyped_passes import MakeFunctionToJitFunction, ReconstructSSA, WithLifting
import bodo
import bodo.libs
import bodo.libs.array_kernels
import bodo.libs.int_arr_ext
import bodo.libs.re_ext
import bodo.libs.spark_extra
import bodo.transforms
import bodo.transforms.series_pass
import bodo.transforms.untyped_pass
from bodo.transforms.series_pass import SeriesPass
from bodo.transforms.typing_pass import BodoTypeInference
from bodo.transforms.untyped_pass import UntypedPass
from bodo.utils.utils import is_assign, is_call_assign, is_expr
_is_sklearn_supported_version = False
_max_sklearn_version = 0, 24, 2
_max_sklearn_ver_str = '.'.join(str(x) for x in _max_sklearn_version)
try:
    import re
    import sklearn
    import bodo.libs.sklearn_ext
    regex = re.compile('(\\d+)\\.(\\d+)\\..*(\\d+)')
    sklearn_version = sklearn.__version__
    m = regex.match(sklearn_version)
    if m:
        ver = tuple(map(int, m.groups()))
        if ver <= _max_sklearn_version:
            _is_sklearn_supported_version = True
except ImportError as gic__wgt:
    pass
_matplotlib_installed = False
try:
    import matplotlib
    import bodo.libs.matplotlib_ext
    _matplotlib_installed = True
except ImportError as gic__wgt:
    pass
_pyspark_installed = False
try:
    import pyspark
    import pyspark.sql.functions
    import bodo.libs.pyspark_ext
    bodo.utils.transform.no_side_effect_call_tuples.update({('col', pyspark
        .sql.functions), (pyspark.sql.functions.col,), ('sum', pyspark.sql.
        functions), (pyspark.sql.functions.sum,)})
    _pyspark_installed = True
except ImportError as gic__wgt:
    pass
import bodo.hiframes.dataframe_indexing
import bodo.hiframes.datetime_datetime_ext
import bodo.hiframes.datetime_timedelta_ext
try:
    import xgboost
    import bodo.libs.xgb_ext
except ImportError as gic__wgt:
    pass
import bodo.io
import bodo.utils
import bodo.utils.typing
if bodo.utils.utils.has_supported_h5py():
    from bodo.io import h5
numba.core.config.DISABLE_PERFORMANCE_WARNINGS = 1
from numba.core.errors import NumbaExperimentalFeatureWarning, NumbaPendingDeprecationWarning
warnings.simplefilter('ignore', category=NumbaExperimentalFeatureWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)
inline_all_calls = False


class BodoCompiler(numba.core.compiler.CompilerBase):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=True,
            inline_calls_pass=inline_all_calls)

    def _create_bodo_pipeline(self, distributed=True, inline_calls_pass=
        False, udf_pipeline=False):
        vdnv__ocd = 'bodo' if distributed else 'bodo_seq'
        vdnv__ocd = vdnv__ocd + '_inline' if inline_calls_pass else vdnv__ocd
        pm = DefaultPassBuilder.define_nopython_pipeline(self.state, vdnv__ocd)
        if inline_calls_pass:
            pm.add_pass_after(InlinePass, WithLifting)
        if udf_pipeline:
            pm.add_pass_after(ConvertCallsUDFPass, WithLifting)
        add_pass_before(pm, BodoUntypedPass, ReconstructSSA)
        replace_pass(pm, BodoTypeInference, NopythonTypeInference)
        remove_pass(pm, MakeFunctionToJitFunction)
        add_pass_before(pm, BodoSeriesPass, PreParforPass)
        if distributed:
            pm.add_pass_after(BodoDistributedPass, ParforPass)
        else:
            pm.add_pass_after(LowerParforSeq, ParforPass)
            pm.add_pass_after(LowerBodoIRExtSeq, LowerParforSeq)
        pm.add_pass_after(BodoDumpDistDiagnosticsPass, DumpParforDiagnostics)
        pm.finalize()
        return [pm]


def add_pass_before(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for sgghf__wdf, (x, qnl__dkf) in enumerate(pm.passes):
        if x == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.insert(sgghf__wdf, (pass_cls, str(pass_cls)))
    pm._finalized = False


def replace_pass(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for sgghf__wdf, (x, qnl__dkf) in enumerate(pm.passes):
        if x == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes[sgghf__wdf] = pass_cls, str(pass_cls)
    pm._finalized = False


def remove_pass(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for sgghf__wdf, (x, qnl__dkf) in enumerate(pm.passes):
        if x == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.pop(sgghf__wdf)
    pm._finalized = False


@register_pass(mutates_CFG=True, analysis_only=False)
class InlinePass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        inline_calls(state.func_ir, state.locals)
        state.func_ir.blocks = ir_utils.simplify_CFG(state.func_ir.blocks)
        return True


def _convert_bodo_dispatcher_to_udf(rhs, func_ir):
    rhh__dsy = guard(get_definition, func_ir, rhs.func)
    if isinstance(rhh__dsy, (ir.Global, ir.FreeVar, ir.Const)):
        pxe__yvqv = rhh__dsy.value
    else:
        ysnx__dwofm = guard(find_callname, func_ir, rhs)
        if not (ysnx__dwofm and isinstance(ysnx__dwofm[0], str) and
            isinstance(ysnx__dwofm[1], str)):
            return
        func_name, func_mod = ysnx__dwofm
        try:
            import importlib
            uot__afepv = importlib.import_module(func_mod)
            pxe__yvqv = getattr(uot__afepv, func_name)
        except:
            return
    if isinstance(pxe__yvqv, CPUDispatcher) and issubclass(pxe__yvqv.
        _compiler.pipeline_class, BodoCompiler
        ) and pxe__yvqv._compiler.pipeline_class != BodoCompilerUDF:
        pxe__yvqv._compiler.pipeline_class = BodoCompilerUDF


@register_pass(mutates_CFG=True, analysis_only=False)
class ConvertCallsUDFPass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        for block in state.func_ir.blocks.values():
            for rbp__hqc in block.body:
                if is_call_assign(rbp__hqc):
                    _convert_bodo_dispatcher_to_udf(rbp__hqc.value, state.
                        func_ir)
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoUntypedPass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        iimr__ohq = UntypedPass(state.func_ir, state.typingctx, state.args,
            state.locals, state.metadata, state.flags)
        iimr__ohq.run()
        return True


def _update_definitions(func_ir, node_list):
    aukmc__zwew = ir.Loc('', 0)
    wgxa__gpoan = ir.Block(ir.Scope(None, aukmc__zwew), aukmc__zwew)
    wgxa__gpoan.body = node_list
    build_definitions({(0): wgxa__gpoan}, func_ir._definitions)


_series_inline_attrs = {'values', 'shape', 'size', 'empty', 'name', 'index',
    'dtype'}
_series_no_inline_methods = {'to_list', 'tolist', 'rolling', 'to_csv',
    'count', 'fillna', 'to_dict', 'map', 'apply', 'pipe', 'combine'}
_series_method_alias = {'isnull': 'isna', 'product': 'prod', 'kurtosis':
    'kurt', 'is_monotonic': 'is_monotonic_increasing', 'notnull': 'notna'}
_dataframe_no_inline_methods = {'apply', 'itertuples', 'pipe', 'to_parquet',
    'to_sql', 'to_csv', 'to_json', 'assign', 'to_string', 'query', 'rolling'}
TypingInfo = namedtuple('TypingInfo', ['typingctx', 'targetctx', 'typemap',
    'calltypes', 'curr_loc'])


def _inline_bodo_getattr(stmt, rhs, rhs_type, new_body, func_ir, typingctx,
    targetctx, typemap, calltypes):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.utils.transform import compile_func_single_block
    if isinstance(rhs_type, SeriesType) and rhs.attr in _series_inline_attrs:
        breqv__qqmd = 'overload_series_' + rhs.attr
        ibs__cbbz = getattr(bodo.hiframes.series_impl, breqv__qqmd)
    if isinstance(rhs_type, DataFrameType) and rhs.attr in ('index', 'columns'
        ):
        breqv__qqmd = 'overload_dataframe_' + rhs.attr
        ibs__cbbz = getattr(bodo.hiframes.dataframe_impl, breqv__qqmd)
    else:
        return False
    func_ir._definitions[stmt.target.name].remove(rhs)
    kltsw__mtpp = ibs__cbbz(rhs_type)
    cqylr__ykey = TypingInfo(typingctx, targetctx, typemap, calltypes, stmt.loc
        )
    xkpm__rurd = compile_func_single_block(kltsw__mtpp, (rhs.value,), stmt.
        target, cqylr__ykey)
    _update_definitions(func_ir, xkpm__rurd)
    new_body += xkpm__rurd
    return True


def _inline_bodo_call(rhs, i, func_mod, func_name, pass_info, new_body,
    block, typingctx, targetctx, calltypes, work_list):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.utils.transform import replace_func, update_locs
    func_ir = pass_info.func_ir
    typemap = pass_info.typemap
    if isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        SeriesType) and func_name not in _series_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        if (func_name in bodo.hiframes.series_impl.explicit_binop_funcs or 
            func_name.startswith('r') and func_name[1:] in bodo.hiframes.
            series_impl.explicit_binop_funcs):
            return False
        rhs.args.insert(0, func_mod)
        srbdk__jzm = tuple(typemap[lea__pzcdy.name] for lea__pzcdy in rhs.args)
        tpprm__gqr = {vdnv__ocd: typemap[lea__pzcdy.name] for vdnv__ocd,
            lea__pzcdy in dict(rhs.kws).items()}
        kltsw__mtpp = getattr(bodo.hiframes.series_impl, 'overload_series_' +
            func_name)(*srbdk__jzm, **tpprm__gqr)
    elif isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        DataFrameType) and func_name not in _dataframe_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        rhs.args.insert(0, func_mod)
        srbdk__jzm = tuple(typemap[lea__pzcdy.name] for lea__pzcdy in rhs.args)
        tpprm__gqr = {vdnv__ocd: typemap[lea__pzcdy.name] for vdnv__ocd,
            lea__pzcdy in dict(rhs.kws).items()}
        kltsw__mtpp = getattr(bodo.hiframes.dataframe_impl, 
            'overload_dataframe_' + func_name)(*srbdk__jzm, **tpprm__gqr)
    else:
        return False
    qwlvq__xzfjo = replace_func(pass_info, kltsw__mtpp, rhs.args, pysig=
        numba.core.utils.pysignature(kltsw__mtpp), kws=dict(rhs.kws))
    block.body = new_body + block.body[i:]
    awur__ovwy, qnl__dkf = inline_closure_call(func_ir, qwlvq__xzfjo.glbls,
        block, len(new_body), qwlvq__xzfjo.func, typingctx=typingctx,
        targetctx=targetctx, arg_typs=qwlvq__xzfjo.arg_types, typemap=
        typemap, calltypes=calltypes, work_list=work_list)
    for lbsyq__mvj in awur__ovwy.values():
        lbsyq__mvj.loc = rhs.loc
        update_locs(lbsyq__mvj.body, rhs.loc)
    return True


def bodo_overload_inline_pass(func_ir, typingctx, targetctx, typemap, calltypes
    ):
    najmu__qgzuc = namedtuple('PassInfo', ['func_ir', 'typemap'])
    pass_info = najmu__qgzuc(func_ir, typemap)
    etcpr__swz = func_ir.blocks
    work_list = list((wsda__ufxz, etcpr__swz[wsda__ufxz]) for wsda__ufxz in
        reversed(etcpr__swz.keys()))
    while work_list:
        qejz__kggq, block = work_list.pop()
        new_body = []
        owgm__usou = False
        for i, stmt in enumerate(block.body):
            if is_assign(stmt) and is_expr(stmt.value, 'getattr'):
                rhs = stmt.value
                rhs_type = typemap[rhs.value.name]
                if _inline_bodo_getattr(stmt, rhs, rhs_type, new_body,
                    func_ir, typingctx, targetctx, typemap, calltypes):
                    continue
            if is_call_assign(stmt):
                rhs = stmt.value
                ysnx__dwofm = guard(find_callname, func_ir, rhs, typemap)
                if ysnx__dwofm is None:
                    new_body.append(stmt)
                    continue
                func_name, func_mod = ysnx__dwofm
                if _inline_bodo_call(rhs, i, func_mod, func_name, pass_info,
                    new_body, block, typingctx, targetctx, calltypes, work_list
                    ):
                    owgm__usou = True
                    break
            new_body.append(stmt)
        if not owgm__usou:
            etcpr__swz[qejz__kggq].body = new_body
    func_ir.blocks = ir_utils.simplify_CFG(func_ir.blocks)


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoDistributedPass(FunctionPass):
    _name = 'bodo_distributed_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        from bodo.transforms.distributed_pass import DistributedPass
        hlyug__jif = DistributedPass(state.func_ir, state.typingctx, state.
            targetctx, state.type_annotation.typemap, state.type_annotation
            .calltypes, state.return_type, state.metadata, state.flags)
        state.return_type = hlyug__jif.run()
        state.type_annotation.blocks = state.func_ir.blocks
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoSeriesPass(FunctionPass):
    _name = 'bodo_series_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        beky__fwek = SeriesPass(state.func_ir, state.typingctx, state.
            targetctx, state.type_annotation.typemap, state.type_annotation
            .calltypes, state.locals)
        beky__fwek.run()
        beky__fwek.run()
        beky__fwek.run()
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoDumpDistDiagnosticsPass(AnalysisPass):
    _name = 'bodo_dump_diagnostics_pass'

    def __init__(self):
        AnalysisPass.__init__(self)

    def run_pass(self, state):
        jllm__ngjlu = 0
        gzgp__alsbw = 'BODO_DISTRIBUTED_DIAGNOSTICS'
        try:
            jllm__ngjlu = int(os.environ[gzgp__alsbw])
        except:
            pass
        if jllm__ngjlu > 0 and 'distributed_diagnostics' in state.metadata:
            state.metadata['distributed_diagnostics'].dump(jllm__ngjlu,
                state.metadata)
        return True


class BodoCompilerSeq(BodoCompiler):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=False,
            inline_calls_pass=inline_all_calls)


class BodoCompilerUDF(BodoCompiler):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=False, udf_pipeline=True)


@register_pass(mutates_CFG=False, analysis_only=True)
class LowerParforSeq(FunctionPass):
    _name = 'bodo_lower_parfor_seq_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        bodo.transforms.distributed_pass.lower_parfor_sequential(state.
            typingctx, state.func_ir, state.typemap, state.calltypes, state
            .metadata)
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class LowerBodoIRExtSeq(FunctionPass):
    _name = 'bodo_lower_ir_ext_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        from bodo.transforms.distributed_pass import distributed_run_extensions
        for block in state.func_ir.blocks.values():
            new_body = []
            for rbp__hqc in block.body:
                if type(rbp__hqc) in distributed_run_extensions:
                    piwr__jna = distributed_run_extensions[type(rbp__hqc)]
                    ccmni__mjsfj = piwr__jna(rbp__hqc, None, state.typemap,
                        state.calltypes, state.typingctx, state.targetctx)
                    new_body += ccmni__mjsfj
                elif is_call_assign(rbp__hqc):
                    rhs = rbp__hqc.value
                    ysnx__dwofm = guard(find_callname, state.func_ir, rhs)
                    if ysnx__dwofm == ('gatherv', 'bodo') or ysnx__dwofm == (
                        'allgatherv', 'bodo'):
                        rbp__hqc.value = rhs.args[0]
                    new_body.append(rbp__hqc)
                else:
                    new_body.append(rbp__hqc)
            block.body = new_body
        state.type_annotation.blocks = state.func_ir.blocks
        return True


def inline_calls(func_ir, _locals, work_list=None, typingctx=None,
    targetctx=None, typemap=None, calltypes=None):
    if work_list is None:
        work_list = list(func_ir.blocks.items())
    zmz__uge = set()
    while work_list:
        qejz__kggq, block = work_list.pop()
        zmz__uge.add(qejz__kggq)
        for i, fzmxo__tqk in enumerate(block.body):
            if isinstance(fzmxo__tqk, ir.Assign):
                jrxv__gjmy = fzmxo__tqk.value
                if isinstance(jrxv__gjmy, ir.Expr) and jrxv__gjmy.op == 'call':
                    rhh__dsy = guard(get_definition, func_ir, jrxv__gjmy.func)
                    if isinstance(rhh__dsy, (ir.Global, ir.FreeVar)
                        ) and isinstance(rhh__dsy.value, CPUDispatcher
                        ) and issubclass(rhh__dsy.value._compiler.
                        pipeline_class, BodoCompiler):
                        weuq__qqjg = rhh__dsy.value.py_func
                        arg_types = None
                        if typingctx:
                            atv__tkqyc = dict(jrxv__gjmy.kws)
                            bhrvs__qext = tuple(typemap[lea__pzcdy.name] for
                                lea__pzcdy in jrxv__gjmy.args)
                            fbck__werx = {qryog__kolg: typemap[lea__pzcdy.
                                name] for qryog__kolg, lea__pzcdy in
                                atv__tkqyc.items()}
                            qnl__dkf, arg_types = (rhh__dsy.value.
                                fold_argument_types(bhrvs__qext, fbck__werx))
                        qnl__dkf, lwbr__asg = inline_closure_call(func_ir,
                            weuq__qqjg.__globals__, block, i, weuq__qqjg,
                            typingctx=typingctx, targetctx=targetctx,
                            arg_typs=arg_types, typemap=typemap, calltypes=
                            calltypes, work_list=work_list)
                        _locals.update((lwbr__asg[qryog__kolg].name,
                            lea__pzcdy) for qryog__kolg, lea__pzcdy in
                            rhh__dsy.value.locals.items() if qryog__kolg in
                            lwbr__asg)
                        break
    return zmz__uge


def udf_jit(signature_or_function=None, **options):
    tzuva__fsqg = {'comprehension': True, 'setitem': False, 'inplace_binop':
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    return numba.njit(signature_or_function, parallel=tzuva__fsqg,
        pipeline_class=bodo.compiler.BodoCompilerUDF, **options)


def is_udf_call(func_type):
    return isinstance(func_type, numba.core.types.Dispatcher
        ) and func_type.dispatcher._compiler.pipeline_class == BodoCompilerUDF


def is_user_dispatcher(func_type):
    return isinstance(func_type, numba.core.types.functions.ObjModeDispatcher
        ) or isinstance(func_type, numba.core.types.Dispatcher) and issubclass(
        func_type.dispatcher._compiler.pipeline_class, BodoCompiler)


@register_pass(mutates_CFG=False, analysis_only=True)
class DummyCR(FunctionPass):
    _name = 'bodo_dummy_cr'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        state.cr = (state.func_ir, state.typemap, state.calltypes, state.
            return_type)
        return True


def remove_passes_after(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for sgghf__wdf, (x, qnl__dkf) in enumerate(pm.passes):
        if x == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes = pm.passes[:sgghf__wdf + 1]
    pm._finalized = False


class TyperCompiler(BodoCompiler):

    def define_pipelines(self):
        [pm] = self._create_bodo_pipeline()
        remove_passes_after(pm, InlineOverloads)
        pm.add_pass_after(DummyCR, InlineOverloads)
        pm.finalize()
        return [pm]


def get_func_type_info(func, arg_types, kw_types):
    typingctx = numba.core.registry.cpu_target.typing_context
    targetctx = numba.core.registry.cpu_target.target_context
    weid__kaxb = None
    rquv__wtrrh = None
    _locals = {}
    udd__eju = numba.core.utils.pysignature(func)
    args = bodo.utils.transform.fold_argument_types(udd__eju, arg_types,
        kw_types)
    rehmz__qlu = numba.core.compiler.Flags()
    naxex__mzsre = {'comprehension': True, 'setitem': False,
        'inplace_binop': False, 'reduction': True, 'numpy': True, 'stencil':
        False, 'fusion': True}
    cfly__idtv = {'nopython': True, 'boundscheck': False, 'parallel':
        naxex__mzsre}
    numba.core.registry.cpu_target.options.parse_as_flags(rehmz__qlu,
        cfly__idtv)
    src__tic = TyperCompiler(typingctx, targetctx, weid__kaxb, args,
        rquv__wtrrh, rehmz__qlu, _locals)
    return src__tic.compile_extra(func)
