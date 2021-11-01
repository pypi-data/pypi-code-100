"""
Numba monkey patches to fix issues related to Bodo. Should be imported before any
other module in bodo package.
"""
import copy
import functools
import hashlib
import inspect
import itertools
import operator
import os
import re
import sys
import textwrap
import traceback
import types as pytypes
import warnings
from collections import OrderedDict
from collections.abc import Sequence
from contextlib import ExitStack
import numba
import numba.core.inline_closurecall
import numba.np.linalg
from numba.core import analysis, cgutils, errors, ir, ir_utils, types
from numba.core.errors import ForceLiteralArg, LiteralTypingError, TypingError
from numba.core.ir_utils import GuardException, _create_function_from_code_obj, analysis, build_definitions, find_callname, guard, has_no_side_effect, mk_unique_var, remove_dead_extensions, replace_vars_inner, require, visit_vars_extensions, visit_vars_inner
from numba.core.types import literal
from numba.core.types.functions import _bt_as_lines, _ResolutionFailures, _termcolor, _unlit_non_poison
from numba.core.typing.templates import AbstractTemplate, Signature, _EmptyImplementationEntry, _inline_info, _OverloadAttributeTemplate, infer_global, signature
from numba.core.typing.typeof import Purpose, typeof
from numba.experimental.jitclass import base as jitclass_base
from numba.experimental.jitclass import decorators as jitclass_decorators
from numba.extending import NativeValue, lower_builtin, typeof_impl
from numba.parfors.parfor import get_expr_args
_check_numba_change = False
numba.core.typing.templates._IntrinsicTemplate.prefer_literal = True


def run_frontend(func, inline_closures=False, emit_dels=False):
    tgzm__avdyr = numba.core.bytecode.FunctionIdentity.from_function(func)
    usew__nskz = numba.core.interpreter.Interpreter(tgzm__avdyr)
    zgzcy__avw = numba.core.bytecode.ByteCode(func_id=tgzm__avdyr)
    func_ir = usew__nskz.interpret(zgzcy__avw)
    if inline_closures:
        from numba.core.inline_closurecall import InlineClosureCallPass


        class DummyPipeline:

            def __init__(self, f_ir):
                self.state = numba.core.compiler.StateDict()
                self.state.typingctx = None
                self.state.targetctx = None
                self.state.args = None
                self.state.func_ir = f_ir
                self.state.typemap = None
                self.state.return_type = None
                self.state.calltypes = None
        numba.core.rewrites.rewrite_registry.apply('before-inference',
            DummyPipeline(func_ir).state)
        skct__yzvrc = InlineClosureCallPass(func_ir, numba.core.cpu.
            ParallelOptions(False), {}, False)
        skct__yzvrc.run()
    ttar__cmjon = numba.core.postproc.PostProcessor(func_ir)
    ttar__cmjon.run(emit_dels)
    return func_ir


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.run_frontend)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8c2477a793b2c08d56430997880974ac12c5570e69c9e54d37d694b322ea18b6':
        warnings.warn('numba.core.compiler.run_frontend has changed')
numba.core.compiler.run_frontend = run_frontend


def visit_vars_stmt(stmt, callback, cbdata):
    for t, bhyn__clmm in visit_vars_extensions.items():
        if isinstance(stmt, t):
            bhyn__clmm(stmt, callback, cbdata)
            return
    if isinstance(stmt, ir.Assign):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Arg):
        stmt.name = visit_vars_inner(stmt.name, callback, cbdata)
    elif isinstance(stmt, ir.Return):
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Raise):
        stmt.exception = visit_vars_inner(stmt.exception, callback, cbdata)
    elif isinstance(stmt, ir.Branch):
        stmt.cond = visit_vars_inner(stmt.cond, callback, cbdata)
    elif isinstance(stmt, ir.Jump):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
    elif isinstance(stmt, ir.Del):
        var = ir.Var(None, stmt.value, stmt.loc)
        var = visit_vars_inner(var, callback, cbdata)
        stmt.value = var.name
    elif isinstance(stmt, ir.DelAttr):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.attr = visit_vars_inner(stmt.attr, callback, cbdata)
    elif isinstance(stmt, ir.SetAttr):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.attr = visit_vars_inner(stmt.attr, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.DelItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index = visit_vars_inner(stmt.index, callback, cbdata)
    elif isinstance(stmt, ir.StaticSetItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index_var = visit_vars_inner(stmt.index_var, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.SetItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index = visit_vars_inner(stmt.index, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Print):
        stmt.args = [visit_vars_inner(x, callback, cbdata) for x in stmt.args]
        stmt.vararg = visit_vars_inner(stmt.vararg, callback, cbdata)
    else:
        pass
    return


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.visit_vars_stmt)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '52b7b645ba65c35f3cf564f936e113261db16a2dff1e80fbee2459af58844117':
        warnings.warn('numba.core.ir_utils.visit_vars_stmt has changed')
numba.core.ir_utils.visit_vars_stmt = visit_vars_stmt
old_run_pass = numba.core.typed_passes.InlineOverloads.run_pass


def InlineOverloads_run_pass(self, state):
    import bodo
    bodo.compiler.bodo_overload_inline_pass(state.func_ir, state.typingctx,
        state.targetctx, state.typemap, state.calltypes)
    return old_run_pass(self, state)


numba.core.typed_passes.InlineOverloads.run_pass = InlineOverloads_run_pass
from numba.core.ir_utils import _add_alias, alias_analysis_extensions, alias_func_extensions
_immutable_type_class = (types.Number, types.scalars._NPDatetimeBase, types
    .iterators.RangeType, types.UnicodeType)


def is_immutable_type(var, typemap):
    if typemap is None or var not in typemap:
        return False
    typ = typemap[var]
    if isinstance(typ, _immutable_type_class):
        return True
    if isinstance(typ, types.BaseTuple) and all(isinstance(t,
        _immutable_type_class) for t in typ.types):
        return True
    return False


def find_potential_aliases(blocks, args, typemap, func_ir, alias_map=None,
    arg_aliases=None):
    if alias_map is None:
        alias_map = {}
    if arg_aliases is None:
        arg_aliases = set(a for a in args if not is_immutable_type(a, typemap))
    func_ir._definitions = build_definitions(func_ir.blocks)
    nqivp__esl = ['ravel', 'transpose', 'reshape']
    for ewv__fpu in blocks.values():
        for lzejo__ajx in ewv__fpu.body:
            if type(lzejo__ajx) in alias_analysis_extensions:
                bhyn__clmm = alias_analysis_extensions[type(lzejo__ajx)]
                bhyn__clmm(lzejo__ajx, args, typemap, func_ir, alias_map,
                    arg_aliases)
            if isinstance(lzejo__ajx, ir.Assign):
                ree__fdej = lzejo__ajx.value
                lhs = lzejo__ajx.target.name
                if is_immutable_type(lhs, typemap):
                    continue
                if isinstance(ree__fdej, ir.Var) and lhs != ree__fdej.name:
                    _add_alias(lhs, ree__fdej.name, alias_map, arg_aliases)
                if isinstance(ree__fdej, ir.Expr) and (ree__fdej.op ==
                    'cast' or ree__fdej.op in ['getitem', 'static_getitem']):
                    _add_alias(lhs, ree__fdej.value.name, alias_map,
                        arg_aliases)
                if isinstance(ree__fdej, ir.Expr
                    ) and ree__fdej.op == 'getattr' and ree__fdej.attr in ['T',
                    'ctypes', 'flat']:
                    _add_alias(lhs, ree__fdej.value.name, alias_map,
                        arg_aliases)
                if isinstance(ree__fdej, ir.Expr
                    ) and ree__fdej.op == 'getattr' and ree__fdej.attr not in [
                    'shape'] and ree__fdej.value.name in arg_aliases:
                    _add_alias(lhs, ree__fdej.value.name, alias_map,
                        arg_aliases)
                if isinstance(ree__fdej, ir.Expr
                    ) and ree__fdej.op == 'getattr' and ree__fdej.attr in (
                    'loc', 'iloc', 'iat', '_obj', 'obj', 'codes', '_df'):
                    _add_alias(lhs, ree__fdej.value.name, alias_map,
                        arg_aliases)
                if isinstance(ree__fdej, ir.Expr) and ree__fdej.op in (
                    'build_tuple', 'build_list', 'build_set'
                    ) and not is_immutable_type(lhs, typemap):
                    for ojxhs__sdmzi in ree__fdej.items:
                        _add_alias(lhs, ojxhs__sdmzi.name, alias_map,
                            arg_aliases)
                if isinstance(ree__fdej, ir.Expr) and ree__fdej.op == 'call':
                    mhzk__ctci = guard(find_callname, func_ir, ree__fdej,
                        typemap)
                    if mhzk__ctci is None:
                        continue
                    htfmh__nbmac, yipjy__oqhpp = mhzk__ctci
                    if mhzk__ctci in alias_func_extensions:
                        mqv__iuz = alias_func_extensions[mhzk__ctci]
                        mqv__iuz(lhs, ree__fdej.args, alias_map, arg_aliases)
                    if yipjy__oqhpp == 'numpy' and htfmh__nbmac in nqivp__esl:
                        _add_alias(lhs, ree__fdej.args[0].name, alias_map,
                            arg_aliases)
                    if isinstance(yipjy__oqhpp, ir.Var
                        ) and htfmh__nbmac in nqivp__esl:
                        _add_alias(lhs, yipjy__oqhpp.name, alias_map,
                            arg_aliases)
    ujvni__vsj = copy.deepcopy(alias_map)
    for ojxhs__sdmzi in ujvni__vsj:
        for wny__mfg in ujvni__vsj[ojxhs__sdmzi]:
            alias_map[ojxhs__sdmzi] |= alias_map[wny__mfg]
        for wny__mfg in ujvni__vsj[ojxhs__sdmzi]:
            alias_map[wny__mfg] = alias_map[ojxhs__sdmzi]
    return alias_map, arg_aliases


if _check_numba_change:
    lines = inspect.getsource(ir_utils.find_potential_aliases)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '2b17b56512a6b9c95e7c6c072bb2e16f681fe2e8e4b8cb7b9fc7ac83133361a1':
        warnings.warn('ir_utils.find_potential_aliases has changed')
ir_utils.find_potential_aliases = find_potential_aliases
if _check_numba_change:
    lines = inspect.getsource(ir_utils.dead_code_elimination)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '40a8626300a1a17523944ec7842b093c91258bbc60844bbd72191a35a4c366bf':
        warnings.warn('ir_utils.dead_code_elimination has changed')


def mini_dce(func_ir, typemap=None, alias_map=None, arg_aliases=None):
    from numba.core.analysis import compute_cfg_from_blocks, compute_live_map, compute_use_defs
    ortv__vhncd = compute_cfg_from_blocks(func_ir.blocks)
    ylfe__aqv = compute_use_defs(func_ir.blocks)
    usznl__oqy = compute_live_map(ortv__vhncd, func_ir.blocks, ylfe__aqv.
        usemap, ylfe__aqv.defmap)
    for xcfs__qona, block in func_ir.blocks.items():
        lives = {ojxhs__sdmzi.name for ojxhs__sdmzi in block.terminator.
            list_vars()}
        for fqzyg__zqu, whmz__qit in ortv__vhncd.successors(xcfs__qona):
            lives |= usznl__oqy[fqzyg__zqu]
        clv__drzh = [block.terminator]
        for stmt in reversed(block.body[:-1]):
            if isinstance(stmt, ir.Assign):
                lhs = stmt.target
                maxxs__sjsm = stmt.value
                if lhs.name not in lives:
                    if isinstance(maxxs__sjsm, ir.Expr
                        ) and maxxs__sjsm.op == 'make_function':
                        continue
                    if isinstance(maxxs__sjsm, ir.Expr
                        ) and maxxs__sjsm.op == 'getattr':
                        continue
                    if isinstance(maxxs__sjsm, ir.Const):
                        continue
                    if typemap and isinstance(typemap.get(lhs, None), types
                        .Function):
                        continue
                if isinstance(maxxs__sjsm, ir.Var
                    ) and lhs.name == maxxs__sjsm.name:
                    continue
            if isinstance(stmt, ir.Del):
                if stmt.value not in lives:
                    continue
            if type(stmt) in analysis.ir_extension_usedefs:
                hfq__jeie = analysis.ir_extension_usedefs[type(stmt)]
                fmg__gyye, jxp__kdtys = hfq__jeie(stmt)
                lives -= jxp__kdtys
                lives |= fmg__gyye
            else:
                lives |= {ojxhs__sdmzi.name for ojxhs__sdmzi in stmt.
                    list_vars()}
                if isinstance(stmt, ir.Assign):
                    lives.remove(lhs.name)
            clv__drzh.append(stmt)
        clv__drzh.reverse()
        block.body = clv__drzh


ir_utils.dead_code_elimination = mini_dce
numba.core.typed_passes.dead_code_elimination = mini_dce
numba.core.inline_closurecall.dead_code_elimination = mini_dce
from numba.core.cpu_options import InlineOptions


def make_overload_template(func, overload_func, jit_options, strict, inline,
    prefer_literal=False, **kwargs):
    cwxco__fag = getattr(func, '__name__', str(func))
    fxxa__cbxe = 'OverloadTemplate_%s' % (cwxco__fag,)
    no_unliteral = kwargs.pop('no_unliteral', False)
    base = numba.core.typing.templates._OverloadFunctionTemplate
    jrbw__ajrr = dict(key=func, _overload_func=staticmethod(overload_func),
        _impl_cache={}, _compiled_overloads={}, _jit_options=jit_options,
        _strict=strict, _inline=staticmethod(InlineOptions(inline)),
        _inline_overloads={}, prefer_literal=prefer_literal, _no_unliteral=
        no_unliteral, metadata=kwargs)
    return type(base)(fxxa__cbxe, (base,), jrbw__ajrr)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        make_overload_template)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '7f6974584cb10e49995b652827540cc6732e497c0b9f8231b44fd83fcc1c0a83':
        warnings.warn(
            'numba.core.typing.templates.make_overload_template has changed')
numba.core.typing.templates.make_overload_template = make_overload_template


def _resolve(self, typ, attr):
    if self._attr != attr:
        return None
    if isinstance(typ, types.TypeRef):
        assert typ == self.key
    else:
        assert isinstance(typ, self.key)


    class MethodTemplate(AbstractTemplate):
        key = self.key, attr
        _inline = self._inline
        _no_unliteral = getattr(self, '_no_unliteral', False)
        _overload_func = staticmethod(self._overload_func)
        _inline_overloads = self._inline_overloads
        prefer_literal = self.prefer_literal

        def generic(_, args, kws):
            args = (typ,) + tuple(args)
            fnty = self._get_function_type(self.context, typ)
            sig = self._get_signature(self.context, fnty, args, kws)
            sig = sig.replace(pysig=numba.core.utils.pysignature(self.
                _overload_func))
            for ytbe__cixtz in fnty.templates:
                self._inline_overloads.update(ytbe__cixtz._inline_overloads)
            if sig is not None:
                return sig.as_method()
    return types.BoundFunction(MethodTemplate, typ)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadMethodTemplate._resolve)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'ce8e0935dc939d0867ef969e1ed2975adb3533a58a4133fcc90ae13c4418e4d6':
        warnings.warn(
            'numba.core.typing.templates._OverloadMethodTemplate._resolve has changed'
            )
numba.core.typing.templates._OverloadMethodTemplate._resolve = _resolve


def make_overload_attribute_template(typ, attr, overload_func, inline,
    prefer_literal=False, base=_OverloadAttributeTemplate, **kwargs):
    assert isinstance(typ, types.Type) or issubclass(typ, types.Type)
    fxxa__cbxe = 'OverloadAttributeTemplate_%s_%s' % (typ, attr)
    no_unliteral = kwargs.pop('no_unliteral', False)
    jrbw__ajrr = dict(key=typ, _attr=attr, _impl_cache={}, _inline=
        staticmethod(InlineOptions(inline)), _inline_overloads={},
        _no_unliteral=no_unliteral, _overload_func=staticmethod(
        overload_func), prefer_literal=prefer_literal, metadata=kwargs)
    obj = type(base)(fxxa__cbxe, (base,), jrbw__ajrr)
    return obj


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        make_overload_attribute_template)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f066c38c482d6cf8bf5735a529c3264118ba9b52264b24e58aad12a6b1960f5d':
        warnings.warn(
            'numba.core.typing.templates.make_overload_attribute_template has changed'
            )
numba.core.typing.templates.make_overload_attribute_template = (
    make_overload_attribute_template)


def generic(self, args, kws):
    from numba.core.typed_passes import PreLowerStripPhis
    isg__lvcp, dysy__zkb = self._get_impl(args, kws)
    if isg__lvcp is None:
        return
    nxhh__slvy = types.Dispatcher(isg__lvcp)
    if not self._inline.is_never_inline:
        from numba.core import compiler, typed_passes
        from numba.core.inline_closurecall import InlineWorker
        mgkkr__jwao = isg__lvcp._compiler
        fzsa__kwr = compiler.Flags()
        eoz__ekuhg = mgkkr__jwao.targetdescr.typing_context
        uxvrh__dzn = mgkkr__jwao.targetdescr.target_context
        vjdt__hjn = mgkkr__jwao.pipeline_class(eoz__ekuhg, uxvrh__dzn, None,
            None, None, fzsa__kwr, None)
        jco__prjv = InlineWorker(eoz__ekuhg, uxvrh__dzn, mgkkr__jwao.locals,
            vjdt__hjn, fzsa__kwr, None)
        xtamz__yll = nxhh__slvy.dispatcher.get_call_template
        ytbe__cixtz, nhln__evknp, tqvhl__ivvt, kws = xtamz__yll(dysy__zkb, kws)
        if tqvhl__ivvt in self._inline_overloads:
            return self._inline_overloads[tqvhl__ivvt]['iinfo'].signature
        ir = jco__prjv.run_untyped_passes(nxhh__slvy.dispatcher.py_func,
            enable_ssa=True)
        typemap, ggse__iuqg, calltypes, _ = typed_passes.type_inference_stage(
            self.context, uxvrh__dzn, ir, tqvhl__ivvt, None)
        ir = PreLowerStripPhis()._strip_phi_nodes(ir)
        ir._definitions = numba.core.ir_utils.build_definitions(ir.blocks)
        sig = Signature(ggse__iuqg, tqvhl__ivvt, None)
        self._inline_overloads[sig.args] = {'folded_args': tqvhl__ivvt}
        hifs__dlf = _EmptyImplementationEntry('always inlined')
        self._compiled_overloads[sig.args] = hifs__dlf
        if not self._inline.is_always_inline:
            sig = nxhh__slvy.get_call_type(self.context, dysy__zkb, kws)
            self._compiled_overloads[sig.args] = nxhh__slvy.get_overload(sig)
        yaxw__ibk = _inline_info(ir, typemap, calltypes, sig)
        self._inline_overloads[sig.args] = {'folded_args': tqvhl__ivvt,
            'iinfo': yaxw__ibk}
    else:
        sig = nxhh__slvy.get_call_type(self.context, dysy__zkb, kws)
        if sig is None:
            return None
        self._compiled_overloads[sig.args] = nxhh__slvy.get_overload(sig)
    return sig


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadFunctionTemplate.generic)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5d453a6d0215ebf0bab1279ff59eb0040b34938623be99142ce20acc09cdeb64':
        warnings.warn(
            'numba.core.typing.templates._OverloadFunctionTemplate.generic has changed'
            )
numba.core.typing.templates._OverloadFunctionTemplate.generic = generic


def bound_function(template_key, no_unliteral=False):

    def wrapper(method_resolver):

        @functools.wraps(method_resolver)
        def attribute_resolver(self, ty):


            class MethodTemplate(AbstractTemplate):
                key = template_key

                def generic(_, args, kws):
                    sig = method_resolver(self, ty, args, kws)
                    if sig is not None and sig.recvr is None:
                        sig = sig.replace(recvr=ty)
                    return sig
            MethodTemplate._no_unliteral = no_unliteral
            return types.BoundFunction(MethodTemplate, ty)
        return attribute_resolver
    return wrapper


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.bound_function)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a2feefe64eae6a15c56affc47bf0c1d04461f9566913442d539452b397103322':
        warnings.warn('numba.core.typing.templates.bound_function has changed')
numba.core.typing.templates.bound_function = bound_function


def get_call_type(self, context, args, kws):
    from numba.core.target_extension import get_local_target, target_registry
    hhtm__huax = [True, False]
    eytcn__xhb = [False, True]
    ljmjv__zgpd = _ResolutionFailures(context, self, args, kws, depth=self.
        _depth)
    huj__wfnp = get_local_target(context)
    tgwt__jvc = 'generic'
    meiim__wyad = []
    for aodwv__gkpe, kkg__xgokq in enumerate(self.templates):
        lszz__vqkgb = kkg__xgokq.metadata.get('target', tgwt__jvc)
        if lszz__vqkgb is not None:
            sry__rxd = target_registry[lszz__vqkgb]
            if huj__wfnp.inherits_from(sry__rxd):
                meiim__wyad.append((kkg__xgokq, sry__rxd, aodwv__gkpe))

    def key(x):
        return huj__wfnp.__mro__.index(x[1])
    wnnvk__etvol = [x[0] for x in sorted(meiim__wyad, key=key)]
    if not wnnvk__etvol:
        msg = (
            f"Function resolution cannot find any matches for function '{self.key[0]}' for the current target: '{huj__wfnp}'."
            )
        raise errors.UnsupportedError(msg)
    self._depth += 1
    for kkg__xgokq in wnnvk__etvol:
        nawc__ydlb = kkg__xgokq(context)
        iyo__xaaa = hhtm__huax if nawc__ydlb.prefer_literal else eytcn__xhb
        iyo__xaaa = [True] if getattr(nawc__ydlb, '_no_unliteral', False
            ) else iyo__xaaa
        for maqm__szcpi in iyo__xaaa:
            try:
                if maqm__szcpi:
                    sig = nawc__ydlb.apply(args, kws)
                else:
                    hyn__ookm = tuple([_unlit_non_poison(a) for a in args])
                    doejx__zxlq = {mifa__owd: _unlit_non_poison(
                        ojxhs__sdmzi) for mifa__owd, ojxhs__sdmzi in kws.
                        items()}
                    sig = nawc__ydlb.apply(hyn__ookm, doejx__zxlq)
            except Exception as e:
                sig = None
                ljmjv__zgpd.add_error(nawc__ydlb, False, e, maqm__szcpi)
            else:
                if sig is not None:
                    self._impl_keys[sig.args] = nawc__ydlb.get_impl_key(sig)
                    self._depth -= 1
                    return sig
                else:
                    yodxu__qcl = getattr(nawc__ydlb, 'cases', None)
                    if yodxu__qcl is not None:
                        msg = 'No match for registered cases:\n%s'
                        msg = msg % '\n'.join(' * {}'.format(x) for x in
                            yodxu__qcl)
                    else:
                        msg = 'No match.'
                    ljmjv__zgpd.add_error(nawc__ydlb, True, msg, maqm__szcpi)
    ljmjv__zgpd.raise_error()


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.BaseFunction.
        get_call_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'bec97de8c8b943243f111ca58d0afd705bbb30b0807b055b5da36bede5159abb':
        warnings.warn(
            'numba.core.types.functions.BaseFunction.get_call_type has changed'
            )
numba.core.types.functions.BaseFunction.get_call_type = get_call_type
bodo_typing_error_info = """
This is often caused by the use of unsupported features or typing issues.
See https://docs.bodo.ai/
"""


def get_call_type2(self, context, args, kws):
    ytbe__cixtz = self.template(context)
    bizb__fnq = None
    aflvz__gydbj = None
    wqlw__utaz = None
    iyo__xaaa = [True, False] if ytbe__cixtz.prefer_literal else [False, True]
    iyo__xaaa = [True] if getattr(ytbe__cixtz, '_no_unliteral', False
        ) else iyo__xaaa
    for maqm__szcpi in iyo__xaaa:
        if maqm__szcpi:
            try:
                wqlw__utaz = ytbe__cixtz.apply(args, kws)
            except Exception as qti__red:
                if isinstance(qti__red, errors.ForceLiteralArg):
                    raise qti__red
                bizb__fnq = qti__red
                wqlw__utaz = None
            else:
                break
        else:
            hqs__ekl = tuple([_unlit_non_poison(a) for a in args])
            wdtly__sek = {mifa__owd: _unlit_non_poison(ojxhs__sdmzi) for 
                mifa__owd, ojxhs__sdmzi in kws.items()}
            rcwaz__ogfps = hqs__ekl == args and kws == wdtly__sek
            if not rcwaz__ogfps and wqlw__utaz is None:
                try:
                    wqlw__utaz = ytbe__cixtz.apply(hqs__ekl, wdtly__sek)
                except Exception as qti__red:
                    if isinstance(qti__red, errors.ForceLiteralArg):
                        if ytbe__cixtz.prefer_literal:
                            raise qti__red
                    aflvz__gydbj = qti__red
                else:
                    break
    if wqlw__utaz is None and (aflvz__gydbj is not None or bizb__fnq is not
        None):
        wasl__dhs = '- Resolution failure for {} arguments:\n{}\n'
        xwmgq__xdqf = _termcolor.highlight(wasl__dhs)
        if numba.core.config.DEVELOPER_MODE:
            anwn__liif = ' ' * 4

            def add_bt(error):
                if isinstance(error, BaseException):
                    yjr__ggue = traceback.format_exception(type(error),
                        error, error.__traceback__)
                else:
                    yjr__ggue = ['']
                zvpa__ymnoj = '\n{}'.format(2 * anwn__liif)
                dfzpi__wtzyz = _termcolor.reset(zvpa__ymnoj + zvpa__ymnoj.
                    join(_bt_as_lines(yjr__ggue)))
                return _termcolor.reset(dfzpi__wtzyz)
        else:
            add_bt = lambda X: ''

        def nested_msg(literalness, e):
            utu__gmn = str(e)
            utu__gmn = utu__gmn if utu__gmn else str(repr(e)) + add_bt(e)
            pfieh__yuudi = errors.TypingError(textwrap.dedent(utu__gmn))
            return xwmgq__xdqf.format(literalness, str(pfieh__yuudi))
        import bodo
        if isinstance(bizb__fnq, bodo.utils.typing.BodoError):
            raise bizb__fnq
        if numba.core.config.DEVELOPER_MODE:
            raise errors.TypingError(nested_msg('literal', bizb__fnq) +
                nested_msg('non-literal', aflvz__gydbj))
        else:
            msg = 'Compilation error for '
            if isinstance(self.this, bodo.hiframes.pd_dataframe_ext.
                DataFrameType):
                msg += 'DataFrame.'
            elif isinstance(self.this, bodo.hiframes.pd_series_ext.SeriesType):
                msg += 'Series.'
            msg += f'{self.typing_key[1]}().{bodo_typing_error_info}'
            raise errors.TypingError(msg)
    return wqlw__utaz


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.BoundFunction.
        get_call_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5427d7ba522b97a4e34745587365b1eacb7b9641229649a02737f944e150bfba':
        warnings.warn(
            'numba.core.types.functions.BoundFunction.get_call_type has changed'
            )
numba.core.types.functions.BoundFunction.get_call_type = get_call_type2


def string_from_string_and_size(self, string, size):
    from llvmlite.llvmpy.core import Type
    fnty = Type.function(self.pyobj, [self.cstring, self.py_ssize_t])
    htfmh__nbmac = 'PyUnicode_FromStringAndSize'
    fn = self._get_function(fnty, name=htfmh__nbmac)
    return self.builder.call(fn, [string, size])


numba.core.pythonapi.PythonAPI.string_from_string_and_size = (
    string_from_string_and_size)


def _compile_for_args(self, *args, **kws):
    assert not kws
    self._compilation_chain_init_hook()
    import bodo

    def error_rewrite(e, issue_type):
        if numba.core.config.SHOW_HELP:
            cyf__bkpur = errors.error_extras[issue_type]
            e.patch_message('\n'.join((str(e).rstrip(), cyf__bkpur)))
        if numba.core.config.FULL_TRACEBACKS:
            raise e
        else:
            raise e.with_traceback(None)
    jgbj__gswt = []
    for a in args:
        if isinstance(a, numba.core.dispatcher.OmittedArg):
            jgbj__gswt.append(types.Omitted(a.value))
        else:
            jgbj__gswt.append(self.typeof_pyval(a))
    qusmo__ixosr = None
    try:
        error = None
        qusmo__ixosr = self.compile(tuple(jgbj__gswt))
    except errors.ForceLiteralArg as e:
        ekdb__aalls = [i for i in e.requested_args if isinstance(args[i],
            types.Literal) and not isinstance(args[i], types.LiteralStrKeyDict)
            ]
        if ekdb__aalls:
            eayy__tuwn = """Repeated literal typing request.
{}.
This is likely caused by an error in typing. Please see nested and suppressed exceptions."""
            exo__ziof = ', '.join('Arg #{} is {}'.format(i, args[i]) for i in
                sorted(ekdb__aalls))
            raise errors.CompilerError(eayy__tuwn.format(exo__ziof))
        dysy__zkb = []
        try:
            for i, ojxhs__sdmzi in enumerate(args):
                if i in e.requested_args:
                    if i in e.file_infos:
                        dysy__zkb.append(types.FilenameType(args[i], e.
                            file_infos[i]))
                    else:
                        dysy__zkb.append(types.literal(args[i]))
                else:
                    dysy__zkb.append(args[i])
            args = dysy__zkb
        except (OSError, FileNotFoundError) as hkp__jfmi:
            error = FileNotFoundError(str(hkp__jfmi) + '\n' + e.loc.
                strformat() + '\n')
        except bodo.utils.typing.BodoError as e:
            error = bodo.utils.typing.BodoError(str(e))
        if error is None:
            try:
                qusmo__ixosr = self._compile_for_args(*args)
            except TypingError as e:
                error = errors.TypingError(str(e))
            except bodo.utils.typing.BodoError as e:
                error = bodo.utils.typing.BodoError(str(e))
    except errors.TypingError as e:
        pmrxl__hgief = []
        for i, rvyxa__sohz in enumerate(args):
            val = rvyxa__sohz.value if isinstance(rvyxa__sohz, numba.core.
                dispatcher.OmittedArg) else rvyxa__sohz
            try:
                xkw__dunl = typeof(val, Purpose.argument)
            except ValueError as kly__guk:
                pmrxl__hgief.append((i, str(kly__guk)))
            else:
                if xkw__dunl is None:
                    pmrxl__hgief.append((i,
                        f'cannot determine Numba type of value {val}'))
        if pmrxl__hgief:
            pnz__uea = '\n'.join(f'- argument {i}: {mwqy__aze}' for i,
                mwqy__aze in pmrxl__hgief)
            msg = f"""{str(e).rstrip()} 

This error may have been caused by the following argument(s):
{pnz__uea}
"""
            e.patch_message(msg)
        if not numba.core.config.DEVELOPER_MODE:
            if bodo_typing_error_info not in e.msg:
                zrub__mdgmt = ['Failed in nopython mode pipeline',
                    'Failed in bodo mode pipeline', 'numba', 'Overload',
                    'lowering']
                ndln__lwrc = False
                for ziluv__vxcjn in zrub__mdgmt:
                    if ziluv__vxcjn in e.msg:
                        msg = 'Compilation error. '
                        msg += f'{bodo_typing_error_info}'
                        ndln__lwrc = True
                        break
                if not ndln__lwrc:
                    msg = f'{str(e)}'
                msg += '\n' + e.loc.strformat() + '\n'
                e.patch_message(msg)
        error_rewrite(e, 'typing')
    except errors.UnsupportedError as e:
        error_rewrite(e, 'unsupported_error')
    except (errors.NotDefinedError, errors.RedefinedError, errors.
        VerificationError) as e:
        error_rewrite(e, 'interpreter')
    except errors.ConstantInferenceError as e:
        error_rewrite(e, 'constant_inference')
    except bodo.utils.typing.BodoError as e:
        error = bodo.utils.typing.BodoError(str(e))
    except Exception as e:
        if numba.core.config.SHOW_HELP:
            if hasattr(e, 'patch_message'):
                cyf__bkpur = errors.error_extras['reportable']
                e.patch_message('\n'.join((str(e).rstrip(), cyf__bkpur)))
        raise e
    finally:
        self._types_active_call = []
        del args
        if error:
            raise error
    return qusmo__ixosr


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher._DispatcherBase.
        _compile_for_args)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5cdfbf0b13a528abf9f0408e70f67207a03e81d610c26b1acab5b2dc1f79bf06':
        warnings.warn(
            'numba.core.dispatcher._DispatcherBase._compile_for_args has changed'
            )
numba.core.dispatcher._DispatcherBase._compile_for_args = _compile_for_args


def resolve_gb_agg_funcs(cres):
    from bodo.ir.aggregate import gb_agg_cfunc_addr
    for awzz__byu in cres.library._codegen._engine._defined_symbols:
        if awzz__byu.startswith('cfunc'
            ) and 'get_agg_udf_addr' not in awzz__byu and (
            'bodo_gb_udf_update_local' in awzz__byu or 
            'bodo_gb_udf_combine' in awzz__byu or 'bodo_gb_udf_eval' in
            awzz__byu or 'bodo_gb_apply_general_udfs' in awzz__byu):
            gb_agg_cfunc_addr[awzz__byu
                ] = cres.library.get_pointer_to_function(awzz__byu)


def resolve_join_general_cond_funcs(cres):
    from bodo.ir.join import join_gen_cond_cfunc_addr
    for awzz__byu in cres.library._codegen._engine._defined_symbols:
        if awzz__byu.startswith('cfunc') and ('get_join_cond_addr' not in
            awzz__byu or 'bodo_join_gen_cond' in awzz__byu):
            join_gen_cond_cfunc_addr[awzz__byu
                ] = cres.library.get_pointer_to_function(awzz__byu)


def compile(self, sig):
    import numba.core.event as ev
    from numba.core import sigutils
    from numba.core.compiler_lock import global_compiler_lock
    isg__lvcp = self._get_dispatcher_for_current_target()
    if isg__lvcp is not self:
        return isg__lvcp.compile(sig)
    with ExitStack() as scope:
        cres = None

        def cb_compiler(dur):
            if cres is not None:
                self._callback_add_compiler_timer(dur, cres)

        def cb_llvm(dur):
            if cres is not None:
                self._callback_add_llvm_timer(dur, cres)
        scope.enter_context(ev.install_timer('numba:compiler_lock',
            cb_compiler))
        scope.enter_context(ev.install_timer('numba:llvm_lock', cb_llvm))
        scope.enter_context(global_compiler_lock)
        if not self._can_compile:
            raise RuntimeError('compilation disabled')
        with self._compiling_counter:
            args, ggse__iuqg = sigutils.normalize_signature(sig)
            xhap__xivz = self.overloads.get(tuple(args))
            if xhap__xivz is not None:
                return xhap__xivz.entry_point
            cres = self._cache.load_overload(sig, self.targetctx)
            if cres is not None:
                resolve_gb_agg_funcs(cres)
                resolve_join_general_cond_funcs(cres)
                self._cache_hits[sig] += 1
                if not cres.objectmode:
                    self.targetctx.insert_user_function(cres.entry_point,
                        cres.fndesc, [cres.library])
                self.add_overload(cres)
                return cres.entry_point
            self._cache_misses[sig] += 1
            vpc__iuzq = dict(dispatcher=self, args=args, return_type=ggse__iuqg
                )
            with ev.trigger_event('numba:compile', data=vpc__iuzq):
                try:
                    cres = self._compiler.compile(args, ggse__iuqg)
                except errors.ForceLiteralArg as e:

                    def folded(args, kws):
                        return self._compiler.fold_argument_types(args, kws)[1]
                    raise e.bind_fold_arguments(folded)
                self.add_overload(cres)
            self._cache.save_overload(sig, cres)
            return cres.entry_point


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.Dispatcher.compile)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '934ec993577ea3b1c7dd2181ac02728abf8559fd42c17062cc821541b092ff8f':
        warnings.warn('numba.core.dispatcher.Dispatcher.compile has changed')
numba.core.dispatcher.Dispatcher.compile = compile


def _get_module_for_linking(self):
    import llvmlite.binding as ll
    self._ensure_finalized()
    if self._shared_module is not None:
        return self._shared_module
    kszn__xqdsc = self._final_module
    qrbme__jlzqm = []
    qlmd__yahgd = 0
    for fn in kszn__xqdsc.functions:
        qlmd__yahgd += 1
        if not fn.is_declaration and fn.linkage == ll.Linkage.external:
            if 'get_agg_udf_addr' not in fn.name:
                if 'bodo_gb_udf_update_local' in fn.name:
                    continue
                if 'bodo_gb_udf_combine' in fn.name:
                    continue
                if 'bodo_gb_udf_eval' in fn.name:
                    continue
                if 'bodo_gb_apply_general_udfs' in fn.name:
                    continue
            if 'get_join_cond_addr' not in fn.name:
                if 'bodo_join_gen_cond' in fn.name:
                    continue
            qrbme__jlzqm.append(fn.name)
    if qlmd__yahgd == 0:
        raise RuntimeError(
            'library unfit for linking: no available functions in %s' % (self,)
            )
    if qrbme__jlzqm:
        kszn__xqdsc = kszn__xqdsc.clone()
        for fxxa__cbxe in qrbme__jlzqm:
            kszn__xqdsc.get_function(fxxa__cbxe).linkage = 'linkonce_odr'
    self._shared_module = kszn__xqdsc
    return kszn__xqdsc


if _check_numba_change:
    lines = inspect.getsource(numba.core.codegen.CPUCodeLibrary.
        _get_module_for_linking)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '56dde0e0555b5ec85b93b97c81821bce60784515a1fbf99e4542e92d02ff0a73':
        warnings.warn(
            'numba.core.codegen.CPUCodeLibrary._get_module_for_linking has changed'
            )
numba.core.codegen.CPUCodeLibrary._get_module_for_linking = (
    _get_module_for_linking)


def propagate(self, typeinfer):
    import bodo
    errors = []
    for qhxb__vaow in self.constraints:
        loc = qhxb__vaow.loc
        with typeinfer.warnings.catch_warnings(filename=loc.filename,
            lineno=loc.line):
            try:
                qhxb__vaow(typeinfer)
            except numba.core.errors.ForceLiteralArg as e:
                errors.append(e)
            except numba.core.errors.TypingError as e:
                numba.core.typeinfer._logger.debug('captured error', exc_info=e
                    )
                azygy__rdm = numba.core.errors.TypingError(str(e), loc=
                    qhxb__vaow.loc, highlighting=False)
                errors.append(numba.core.utils.chain_exception(azygy__rdm, e))
            except bodo.utils.typing.BodoError as e:
                if loc not in e.locs_in_msg:
                    errors.append(bodo.utils.typing.BodoError(str(e.msg) +
                        '\n' + loc.strformat() + '\n', locs_in_msg=e.
                        locs_in_msg + [loc]))
                else:
                    errors.append(bodo.utils.typing.BodoError(e.msg,
                        locs_in_msg=e.locs_in_msg))
            except Exception as e:
                numba.core.typeinfer._logger.debug('captured error', exc_info=e
                    )
                msg = (
                    'Internal error at {con}.\n{err}\nEnable logging at debug level for details.'
                    )
                azygy__rdm = numba.core.errors.TypingError(msg.format(con=
                    qhxb__vaow, err=str(e)), loc=qhxb__vaow.loc,
                    highlighting=False)
                errors.append(numba.core.utils.chain_exception(azygy__rdm, e))
    return errors


if _check_numba_change:
    lines = inspect.getsource(numba.core.typeinfer.ConstraintNetwork.propagate)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '2c204df4d8c58da7c86e0abbab48a7a7863ee3cbe8d2ba89f617d4f580b622e9':
        warnings.warn(
            'numba.core.typeinfer.ConstraintNetwork.propagate has changed')
numba.core.typeinfer.ConstraintNetwork.propagate = propagate


def raise_error(self):
    import bodo
    for ulguy__wyva in self._failures.values():
        for phf__tahim in ulguy__wyva:
            if isinstance(phf__tahim.error, ForceLiteralArg):
                raise phf__tahim.error
            if isinstance(phf__tahim.error, bodo.utils.typing.BodoError):
                raise phf__tahim.error
    raise TypingError(self.format())


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.
        _ResolutionFailures.raise_error)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '84b89430f5c8b46cfc684804e6037f00a0f170005cd128ad245551787b2568ea':
        warnings.warn(
            'numba.core.types.functions._ResolutionFailures.raise_error has changed'
            )
numba.core.types.functions._ResolutionFailures.raise_error = raise_error


def bodo_remove_dead_block(block, lives, call_table, arg_aliases, alias_map,
    alias_set, func_ir, typemap):
    from bodo.transforms.distributed_pass import saved_array_analysis
    from bodo.utils.utils import is_array_typ, is_expr
    vfvt__ghugh = False
    clv__drzh = [block.terminator]
    for stmt in reversed(block.body[:-1]):
        hpg__mcd = set()
        cnol__pjw = lives & alias_set
        for ojxhs__sdmzi in cnol__pjw:
            hpg__mcd |= alias_map[ojxhs__sdmzi]
        lives_n_aliases = lives | hpg__mcd | arg_aliases
        if type(stmt) in remove_dead_extensions:
            bhyn__clmm = remove_dead_extensions[type(stmt)]
            stmt = bhyn__clmm(stmt, lives, lives_n_aliases, arg_aliases,
                alias_map, func_ir, typemap)
            if stmt is None:
                vfvt__ghugh = True
                continue
        if isinstance(stmt, ir.Assign):
            lhs = stmt.target
            maxxs__sjsm = stmt.value
            if lhs.name not in lives and has_no_side_effect(maxxs__sjsm,
                lives_n_aliases, call_table):
                vfvt__ghugh = True
                continue
            if saved_array_analysis and lhs.name in lives and is_expr(
                maxxs__sjsm, 'getattr'
                ) and maxxs__sjsm.attr == 'shape' and is_array_typ(typemap[
                maxxs__sjsm.value.name]
                ) and maxxs__sjsm.value.name not in lives:
                iofr__zql = {ojxhs__sdmzi: mifa__owd for mifa__owd,
                    ojxhs__sdmzi in func_ir.blocks.items()}
                if block in iofr__zql:
                    xcfs__qona = iofr__zql[block]
                    fiqx__duhlb = saved_array_analysis.get_equiv_set(xcfs__qona
                        )
                    ypnm__xqvx = fiqx__duhlb.get_equiv_set(maxxs__sjsm.value)
                    if ypnm__xqvx is not None:
                        for ojxhs__sdmzi in ypnm__xqvx:
                            if ojxhs__sdmzi.endswith('#0'):
                                ojxhs__sdmzi = ojxhs__sdmzi[:-2]
                            if ojxhs__sdmzi in typemap and is_array_typ(typemap
                                [ojxhs__sdmzi]) and ojxhs__sdmzi in lives:
                                maxxs__sjsm.value = ir.Var(maxxs__sjsm.
                                    value.scope, ojxhs__sdmzi, maxxs__sjsm.
                                    value.loc)
                                vfvt__ghugh = True
                                break
            if isinstance(maxxs__sjsm, ir.Var
                ) and lhs.name == maxxs__sjsm.name:
                vfvt__ghugh = True
                continue
        if isinstance(stmt, ir.Del):
            if stmt.value not in lives:
                vfvt__ghugh = True
                continue
        if isinstance(stmt, ir.SetItem):
            fxxa__cbxe = stmt.target.name
            if fxxa__cbxe not in lives_n_aliases:
                continue
        if type(stmt) in analysis.ir_extension_usedefs:
            hfq__jeie = analysis.ir_extension_usedefs[type(stmt)]
            fmg__gyye, jxp__kdtys = hfq__jeie(stmt)
            lives -= jxp__kdtys
            lives |= fmg__gyye
        else:
            lives |= {ojxhs__sdmzi.name for ojxhs__sdmzi in stmt.list_vars()}
            if isinstance(stmt, ir.Assign):
                icysc__hgxp = set()
                if isinstance(maxxs__sjsm, ir.Expr):
                    icysc__hgxp = {ojxhs__sdmzi.name for ojxhs__sdmzi in
                        maxxs__sjsm.list_vars()}
                if lhs.name not in icysc__hgxp:
                    lives.remove(lhs.name)
        clv__drzh.append(stmt)
    clv__drzh.reverse()
    block.body = clv__drzh
    return vfvt__ghugh


ir_utils.remove_dead_block = bodo_remove_dead_block


@infer_global(set)
class SetBuiltin(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if args:
            wlrx__emzaa, = args
            if isinstance(wlrx__emzaa, types.IterableType):
                dtype = wlrx__emzaa.iterator_type.yield_type
                if isinstance(dtype, types.Hashable
                    ) or dtype == numba.core.types.unicode_type:
                    return signature(types.Set(dtype), wlrx__emzaa)
        else:
            return signature(types.Set(types.undefined))


def Set__init__(self, dtype, reflected=False):
    assert isinstance(dtype, (types.Hashable, types.Undefined)
        ) or dtype == numba.core.types.unicode_type
    self.dtype = dtype
    self.reflected = reflected
    pnqtb__khdjf = 'reflected set' if reflected else 'set'
    fxxa__cbxe = '%s(%s)' % (pnqtb__khdjf, self.dtype)
    super(types.Set, self).__init__(name=fxxa__cbxe)


types.Set.__init__ = Set__init__


@lower_builtin(operator.eq, types.UnicodeType, types.UnicodeType)
def eq_str(context, builder, sig, args):
    func = numba.cpython.unicode.unicode_eq(*sig.args)
    return context.compile_internal(builder, func, sig, args)


numba.parfors.parfor.push_call_vars = (lambda blocks, saved_globals,
    saved_getattrs, typemap, nested=False: None)


def maybe_literal(value):
    if isinstance(value, (list, dict, pytypes.FunctionType)):
        return
    try:
        return literal(value)
    except LiteralTypingError as zwsnc__vldr:
        return


if _check_numba_change:
    lines = inspect.getsource(types.maybe_literal)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8fb2fd93acf214b28e33e37d19dc2f7290a42792ec59b650553ac278854b5081':
        warnings.warn('types.maybe_literal has changed')
types.maybe_literal = maybe_literal
types.misc.maybe_literal = maybe_literal


def CacheImpl__init__(self, py_func):
    self._lineno = py_func.__code__.co_firstlineno
    try:
        zobbh__psbz = py_func.__qualname__
    except AttributeError as zwsnc__vldr:
        zobbh__psbz = py_func.__name__
    enx__mbpp = inspect.getfile(py_func)
    for cls in self._locator_classes:
        trj__grfus = cls.from_function(py_func, enx__mbpp)
        if trj__grfus is not None:
            break
    else:
        raise RuntimeError(
            'cannot cache function %r: no locator available for file %r' %
            (zobbh__psbz, enx__mbpp))
    self._locator = trj__grfus
    joo__dhvky = inspect.getfile(py_func)
    cjoae__nnf = os.path.splitext(os.path.basename(joo__dhvky))[0]
    if enx__mbpp.startswith('<ipython-'):
        luec__qne = re.sub('(ipython-input)(-\\d+)(-[0-9a-fA-F]+)',
            '\\1\\3', cjoae__nnf, count=1)
        if luec__qne == cjoae__nnf:
            warnings.warn(
                'Did not recognize ipython module name syntax. Caching might not work'
                )
        cjoae__nnf = luec__qne
    rgn__vvfzc = '%s.%s' % (cjoae__nnf, zobbh__psbz)
    yusz__wiz = getattr(sys, 'abiflags', '')
    self._filename_base = self.get_filename_base(rgn__vvfzc, yusz__wiz)


if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheImpl.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b46d298146e3844e9eaeef29d36f5165ba4796c270ca50d2b35f9fcdc0fa032a':
        warnings.warn('numba.core.caching._CacheImpl.__init__ has changed')
numba.core.caching._CacheImpl.__init__ = CacheImpl__init__


def _analyze_broadcast(self, scope, equiv_set, loc, args, fn):
    from numba.parfors.array_analysis import ArrayAnalysis
    jfvvl__bjrfp = list(filter(lambda a: self._istuple(a.name), args))
    if len(jfvvl__bjrfp) == 2 and fn.__name__ == 'add':
        nivkj__iho = self.typemap[jfvvl__bjrfp[0].name]
        onjq__krm = self.typemap[jfvvl__bjrfp[1].name]
        if nivkj__iho.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                jfvvl__bjrfp[1]))
        if onjq__krm.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                jfvvl__bjrfp[0]))
        try:
            hjlgy__xhv = [equiv_set.get_shape(x) for x in jfvvl__bjrfp]
            if None in hjlgy__xhv:
                return None
            tlars__obqcq = sum(hjlgy__xhv, ())
            return ArrayAnalysis.AnalyzeResult(shape=tlars__obqcq)
        except GuardException as zwsnc__vldr:
            return None
    ysney__wthx = list(filter(lambda a: self._isarray(a.name), args))
    require(len(ysney__wthx) > 0)
    yvkdl__wwlsf = [x.name for x in ysney__wthx]
    gkpu__dsl = [self.typemap[x.name].ndim for x in ysney__wthx]
    tqz__hrn = max(gkpu__dsl)
    require(tqz__hrn > 0)
    hjlgy__xhv = [equiv_set.get_shape(x) for x in ysney__wthx]
    if any(a is None for a in hjlgy__xhv):
        return ArrayAnalysis.AnalyzeResult(shape=ysney__wthx[0], pre=self.
            _call_assert_equiv(scope, loc, equiv_set, ysney__wthx))
    return self._broadcast_assert_shapes(scope, equiv_set, loc, hjlgy__xhv,
        yvkdl__wwlsf)


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.array_analysis.ArrayAnalysis.
        _analyze_broadcast)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '6c91fec038f56111338ea2b08f5f0e7f61ebdab1c81fb811fe26658cc354e40f':
        warnings.warn(
            'numba.parfors.array_analysis.ArrayAnalysis._analyze_broadcast has changed'
            )
numba.parfors.array_analysis.ArrayAnalysis._analyze_broadcast = (
    _analyze_broadcast)


def convert_code_obj_to_function(code_obj, caller_ir):
    import bodo
    gmb__wswzp = code_obj.code
    qteu__bfd = len(gmb__wswzp.co_freevars)
    ozi__knqj = gmb__wswzp.co_freevars
    if code_obj.closure is not None:
        assert isinstance(code_obj.closure, ir.Var)
        spsiz__myzf, ttmik__monw = ir_utils.find_build_sequence(caller_ir,
            code_obj.closure)
        assert ttmik__monw == 'build_tuple'
        ozi__knqj = [ojxhs__sdmzi.name for ojxhs__sdmzi in spsiz__myzf]
    pyzp__awl = caller_ir.func_id.func.__globals__
    try:
        pyzp__awl = getattr(code_obj, 'globals', pyzp__awl)
    except KeyError as zwsnc__vldr:
        pass
    msg = (
        "Inner function is using non-constant variable '{}' from outer function. Please pass as argument if possible. See https://docs.bodo.ai/latest/source/pandas.html#user-defined-functions-udfs"
        )
    hcpx__gkiu = []
    for x in ozi__knqj:
        try:
            snms__keyrh = caller_ir.get_definition(x)
        except KeyError as zwsnc__vldr:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
        from numba.core.registry import CPUDispatcher
        if isinstance(snms__keyrh, (ir.Const, ir.Global, ir.FreeVar)):
            val = snms__keyrh.value
            if isinstance(val, str):
                val = "'{}'".format(val)
            if isinstance(val, pytypes.FunctionType):
                cwxco__fag = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                pyzp__awl[cwxco__fag] = numba.njit(val)
                val = cwxco__fag
            if isinstance(val, CPUDispatcher):
                cwxco__fag = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                pyzp__awl[cwxco__fag] = val
                val = cwxco__fag
            hcpx__gkiu.append(val)
        elif isinstance(snms__keyrh, ir.Expr
            ) and snms__keyrh.op == 'make_function':
            hudur__ifo = convert_code_obj_to_function(snms__keyrh, caller_ir)
            cwxco__fag = ir_utils.mk_unique_var('nested_func').replace('.', '_'
                )
            pyzp__awl[cwxco__fag] = numba.njit(hudur__ifo)
            hcpx__gkiu.append(cwxco__fag)
        else:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
    tqhps__aktw = '\n'.join([('  c_%d = %s' % (i, x)) for i, x in enumerate
        (hcpx__gkiu)])
    kfl__tuc = ','.join([('c_%d' % i) for i in range(qteu__bfd)])
    eej__qppjd = list(gmb__wswzp.co_varnames)
    tsb__uqtl = 0
    nxpsy__xrv = gmb__wswzp.co_argcount
    lpam__xahnh = caller_ir.get_definition(code_obj.defaults)
    if lpam__xahnh is not None:
        if isinstance(lpam__xahnh, tuple):
            itir__kub = [caller_ir.get_definition(x).value for x in lpam__xahnh
                ]
            fmfvk__ijl = tuple(itir__kub)
        else:
            itir__kub = [caller_ir.get_definition(x).value for x in
                lpam__xahnh.items]
            fmfvk__ijl = tuple(itir__kub)
        tsb__uqtl = len(fmfvk__ijl)
    qmmhl__abgyb = nxpsy__xrv - tsb__uqtl
    trmng__tdkr = ','.join([('%s' % eej__qppjd[i]) for i in range(
        qmmhl__abgyb)])
    if tsb__uqtl:
        bzw__eogfo = [('%s = %s' % (eej__qppjd[i + qmmhl__abgyb],
            fmfvk__ijl[i])) for i in range(tsb__uqtl)]
        trmng__tdkr += ', '
        trmng__tdkr += ', '.join(bzw__eogfo)
    return _create_function_from_code_obj(gmb__wswzp, tqhps__aktw,
        trmng__tdkr, kfl__tuc, pyzp__awl)


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.convert_code_obj_to_function)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b6b51a980f1952532f128fc20653b836a3d45ceb93add91fa14acd54901444d7':
        warnings.warn(
            'numba.core.ir_utils.convert_code_obj_to_function has changed')
numba.core.ir_utils.convert_code_obj_to_function = convert_code_obj_to_function
numba.core.untyped_passes.convert_code_obj_to_function = (
    convert_code_obj_to_function)


def passmanager_run(self, state):
    from numba.core.compiler import _EarlyPipelineCompletion
    if not self.finalized:
        raise RuntimeError('Cannot run non-finalised pipeline')
    from numba.core.compiler_machinery import CompilerPass, _pass_registry
    import bodo
    for pycb__dcylc, (tsadm__iqdd, iudlt__dra) in enumerate(self.passes):
        try:
            numba.core.tracing.event('-- %s' % iudlt__dra)
            yugo__dcwid = _pass_registry.get(tsadm__iqdd).pass_inst
            if isinstance(yugo__dcwid, CompilerPass):
                self._runPass(pycb__dcylc, yugo__dcwid, state)
            else:
                raise BaseException('Legacy pass in use')
        except _EarlyPipelineCompletion as e:
            raise e
        except bodo.utils.typing.BodoError as e:
            raise
        except Exception as e:
            if numba.core.config.DEVELOPER_MODE:
                msg = 'Failed in %s mode pipeline (step: %s)' % (self.
                    pipeline_name, iudlt__dra)
                uwz__bdhk = self._patch_error(msg, e)
                raise uwz__bdhk
            else:
                raise e


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler_machinery.PassManager.run)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5d21271317cfa1bdcec1cc71973d80df0ffd7126c4608eeef4ad676bbff8f0d3':
        warnings.warn(
            'numba.core.compiler_machinery.PassManager.run has changed')
numba.core.compiler_machinery.PassManager.run = passmanager_run
if _check_numba_change:
    lines = inspect.getsource(numba.np.ufunc.parallel._launch_threads)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '3d7e5889ad7dcd2b1ff0389cf37df400855e0b0b25b956927073b49015298736':
        warnings.warn('numba.np.ufunc.parallel._launch_threads has changed')
numba.np.ufunc.parallel._launch_threads = lambda : None


def get_reduce_nodes(reduction_node, nodes, func_ir):
    dab__swn = None
    jxp__kdtys = {}

    def lookup(var, varonly=True):
        val = jxp__kdtys.get(var.name, None)
        if isinstance(val, ir.Var):
            return lookup(val)
        else:
            return var if varonly or val is None else val
    fxxa__cbxe = reduction_node.name
    qncnv__edwlc = reduction_node.unversioned_name
    for i, stmt in enumerate(nodes):
        lhs = stmt.target
        maxxs__sjsm = stmt.value
        jxp__kdtys[lhs.name] = maxxs__sjsm
        if isinstance(maxxs__sjsm, ir.Var) and maxxs__sjsm.name in jxp__kdtys:
            maxxs__sjsm = lookup(maxxs__sjsm)
        if isinstance(maxxs__sjsm, ir.Expr):
            tjucm__mbish = set(lookup(ojxhs__sdmzi, True).name for
                ojxhs__sdmzi in maxxs__sjsm.list_vars())
            if fxxa__cbxe in tjucm__mbish:
                args = [(x.name, lookup(x, True)) for x in get_expr_args(
                    maxxs__sjsm)]
                aan__xwee = [x for x, xxcem__rmjv in args if xxcem__rmjv.
                    name != fxxa__cbxe]
                args = [(x, xxcem__rmjv) for x, xxcem__rmjv in args if x !=
                    xxcem__rmjv.name]
                gsa__oscd = dict(args)
                if len(aan__xwee) == 1:
                    gsa__oscd[aan__xwee[0]] = ir.Var(lhs.scope, fxxa__cbxe +
                        '#init', lhs.loc)
                replace_vars_inner(maxxs__sjsm, gsa__oscd)
                dab__swn = nodes[i:]
                break
    return dab__swn


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_reduce_nodes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a05b52aff9cb02e595a510cd34e973857303a71097fc5530567cb70ca183ef3b':
        warnings.warn('numba.parfors.parfor.get_reduce_nodes has changed')
numba.parfors.parfor.get_reduce_nodes = get_reduce_nodes


def _can_reorder_stmts(stmt, next_stmt, func_ir, call_table, alias_map,
    arg_aliases):
    from numba.parfors.parfor import Parfor, expand_aliases, is_assert_equiv
    if isinstance(stmt, Parfor) and not isinstance(next_stmt, Parfor
        ) and not isinstance(next_stmt, ir.Print) and (not isinstance(
        next_stmt, ir.Assign) or has_no_side_effect(next_stmt.value, set(),
        call_table) or guard(is_assert_equiv, func_ir, next_stmt.value)):
        nillo__lnq = expand_aliases({ojxhs__sdmzi.name for ojxhs__sdmzi in
            stmt.list_vars()}, alias_map, arg_aliases)
        ksle__ivmqh = expand_aliases(get_parfor_writes(stmt, func_ir),
            alias_map, arg_aliases)
        khzc__rdib = expand_aliases({ojxhs__sdmzi.name for ojxhs__sdmzi in
            next_stmt.list_vars()}, alias_map, arg_aliases)
        sofn__yldy = expand_aliases(get_stmt_writes(next_stmt, func_ir),
            alias_map, arg_aliases)
        if len(ksle__ivmqh & khzc__rdib | sofn__yldy & nillo__lnq) == 0:
            return True
    return False


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor._can_reorder_stmts)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '18caa9a01b21ab92b4f79f164cfdbc8574f15ea29deedf7bafdf9b0e755d777c':
        warnings.warn('numba.parfors.parfor._can_reorder_stmts has changed')
numba.parfors.parfor._can_reorder_stmts = _can_reorder_stmts


def get_parfor_writes(parfor, func_ir):
    from numba.parfors.parfor import Parfor
    assert isinstance(parfor, Parfor)
    ltg__ekekm = set()
    blocks = parfor.loop_body.copy()
    blocks[-1] = parfor.init_block
    for block in blocks.values():
        for stmt in block.body:
            ltg__ekekm.update(get_stmt_writes(stmt, func_ir))
            if isinstance(stmt, Parfor):
                ltg__ekekm.update(get_parfor_writes(stmt, func_ir))
    return ltg__ekekm


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_parfor_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a7b29cd76832b6f6f1f2d2397ec0678c1409b57a6eab588bffd344b775b1546f':
        warnings.warn('numba.parfors.parfor.get_parfor_writes has changed')


def get_stmt_writes(stmt, func_ir):
    import bodo
    from bodo.utils.utils import is_call_assign
    ltg__ekekm = set()
    if isinstance(stmt, (ir.Assign, ir.SetItem, ir.StaticSetItem)):
        ltg__ekekm.add(stmt.target.name)
    if isinstance(stmt, bodo.ir.aggregate.Aggregate):
        ltg__ekekm = {ojxhs__sdmzi.name for ojxhs__sdmzi in stmt.
            df_out_vars.values()}
        if stmt.out_key_vars is not None:
            ltg__ekekm.update({ojxhs__sdmzi.name for ojxhs__sdmzi in stmt.
                out_key_vars})
    if isinstance(stmt, (bodo.ir.csv_ext.CsvReader, bodo.ir.parquet_ext.
        ParquetReader)):
        ltg__ekekm = {ojxhs__sdmzi.name for ojxhs__sdmzi in stmt.out_vars}
    if isinstance(stmt, bodo.ir.join.Join):
        ltg__ekekm = {ojxhs__sdmzi.name for ojxhs__sdmzi in stmt.
            out_data_vars.values()}
    if isinstance(stmt, bodo.ir.sort.Sort):
        if not stmt.inplace:
            ltg__ekekm.update({ojxhs__sdmzi.name for ojxhs__sdmzi in stmt.
                out_key_arrs})
            ltg__ekekm.update({ojxhs__sdmzi.name for ojxhs__sdmzi in stmt.
                df_out_vars.values()})
    if is_call_assign(stmt):
        mhzk__ctci = guard(find_callname, func_ir, stmt.value)
        if mhzk__ctci in (('setitem_str_arr_ptr', 'bodo.libs.str_arr_ext'),
            ('setna', 'bodo.libs.array_kernels'), (
            'str_arr_item_to_numeric', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_int_to_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_NA_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_set_not_na', 'bodo.libs.str_arr_ext'), (
            'set_bit_to_arr', 'bodo.libs.int_arr_ext')):
            ltg__ekekm.add(stmt.value.args[0].name)
    return ltg__ekekm


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.get_stmt_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1a7a80b64c9a0eb27e99dc8eaae187bde379d4da0b74c84fbf87296d87939974':
        warnings.warn('numba.core.ir_utils.get_stmt_writes has changed')


def patch_message(self, new_message):
    self.msg = new_message
    self.args = (new_message,) + self.args[1:]


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.NumbaError.patch_message)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'ed189a428a7305837e76573596d767b6e840e99f75c05af6941192e0214fa899':
        warnings.warn('numba.core.errors.NumbaError.patch_message has changed')
numba.core.errors.NumbaError.patch_message = patch_message


def add_context(self, msg):
    if numba.core.config.DEVELOPER_MODE:
        self.contexts.append(msg)
        bhyn__clmm = _termcolor.errmsg('{0}') + _termcolor.filename(
            'During: {1}')
        wsvqi__sgcxv = bhyn__clmm.format(self, msg)
        self.args = wsvqi__sgcxv,
    else:
        bhyn__clmm = _termcolor.errmsg('{0}')
        wsvqi__sgcxv = bhyn__clmm.format(self)
        self.args = wsvqi__sgcxv,
    return self


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.NumbaError.add_context)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '6a388d87788f8432c2152ac55ca9acaa94dbc3b55be973b2cf22dd4ee7179ab8':
        warnings.warn('numba.core.errors.NumbaError.add_context has changed')
numba.core.errors.NumbaError.add_context = add_context


def _get_dist_spec_from_options(spec, **options):
    from bodo.transforms.distributed_analysis import Distribution
    dist_spec = {}
    if 'distributed' in options:
        for sfy__cru in options['distributed']:
            dist_spec[sfy__cru] = Distribution.OneD_Var
    if 'distributed_block' in options:
        for sfy__cru in options['distributed_block']:
            dist_spec[sfy__cru] = Distribution.OneD
    return dist_spec


def register_class_type(cls, spec, class_ctor, builder, **options):
    import typing as pt
    from numba.core.typing.asnumbatype import as_numba_type
    import bodo
    dist_spec = _get_dist_spec_from_options(spec, **options)
    assfs__hgnin = options.get('returns_maybe_distributed', True)
    if spec is None:
        spec = OrderedDict()
    elif isinstance(spec, Sequence):
        spec = OrderedDict(spec)
    for attr, asmfz__edozn in pt.get_type_hints(cls).items():
        if attr not in spec:
            spec[attr] = as_numba_type(asmfz__edozn)
    jitclass_base._validate_spec(spec)
    spec = jitclass_base._fix_up_private_attr(cls.__name__, spec)
    hzge__uys = {}
    for anwv__jqzoa in reversed(inspect.getmro(cls)):
        hzge__uys.update(anwv__jqzoa.__dict__)
    lupx__opof, acyt__acfso, ajcd__fsmd, pcypq__heyks = {}, {}, {}, {}
    for mifa__owd, ojxhs__sdmzi in hzge__uys.items():
        if isinstance(ojxhs__sdmzi, pytypes.FunctionType):
            lupx__opof[mifa__owd] = ojxhs__sdmzi
        elif isinstance(ojxhs__sdmzi, property):
            acyt__acfso[mifa__owd] = ojxhs__sdmzi
        elif isinstance(ojxhs__sdmzi, staticmethod):
            ajcd__fsmd[mifa__owd] = ojxhs__sdmzi
        else:
            pcypq__heyks[mifa__owd] = ojxhs__sdmzi
    oqj__uklt = (set(lupx__opof) | set(acyt__acfso) | set(ajcd__fsmd)) & set(
        spec)
    if oqj__uklt:
        raise NameError('name shadowing: {0}'.format(', '.join(oqj__uklt)))
    lwhz__atpt = pcypq__heyks.pop('__doc__', '')
    jitclass_base._drop_ignored_attrs(pcypq__heyks)
    if pcypq__heyks:
        msg = 'class members are not yet supported: {0}'
        ypbvx__pzk = ', '.join(pcypq__heyks.keys())
        raise TypeError(msg.format(ypbvx__pzk))
    for mifa__owd, ojxhs__sdmzi in acyt__acfso.items():
        if ojxhs__sdmzi.fdel is not None:
            raise TypeError('deleter is not supported: {0}'.format(mifa__owd))
    jit_methods = {mifa__owd: bodo.jit(returns_maybe_distributed=
        assfs__hgnin)(ojxhs__sdmzi) for mifa__owd, ojxhs__sdmzi in
        lupx__opof.items()}
    jit_props = {}
    for mifa__owd, ojxhs__sdmzi in acyt__acfso.items():
        jrbw__ajrr = {}
        if ojxhs__sdmzi.fget:
            jrbw__ajrr['get'] = bodo.jit(ojxhs__sdmzi.fget)
        if ojxhs__sdmzi.fset:
            jrbw__ajrr['set'] = bodo.jit(ojxhs__sdmzi.fset)
        jit_props[mifa__owd] = jrbw__ajrr
    jit_static_methods = {mifa__owd: bodo.jit(ojxhs__sdmzi.__func__) for 
        mifa__owd, ojxhs__sdmzi in ajcd__fsmd.items()}
    kfyu__ezei = class_ctor(cls, jitclass_base.ConstructorTemplate, spec,
        jit_methods, jit_props, jit_static_methods, dist_spec)
    gvoa__aneop = dict(class_type=kfyu__ezei, __doc__=lwhz__atpt)
    gvoa__aneop.update(jit_static_methods)
    cls = jitclass_base.JitClassType(cls.__name__, (cls,), gvoa__aneop)
    typingctx = numba.core.registry.cpu_target.typing_context
    typingctx.insert_global(cls, kfyu__ezei)
    kkft__hee = numba.core.registry.cpu_target.target_context
    builder(kfyu__ezei, typingctx, kkft__hee).register()
    as_numba_type.register(cls, kfyu__ezei.instance_type)
    return cls


if _check_numba_change:
    lines = inspect.getsource(jitclass_base.register_class_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '005e6e2e89a47f77a19ba86305565050d4dbc2412fc4717395adf2da348671a9':
        warnings.warn('jitclass_base.register_class_type has changed')
jitclass_base.register_class_type = register_class_type


def ClassType__init__(self, class_def, ctor_template_cls, struct,
    jit_methods, jit_props, jit_static_methods, dist_spec=None):
    if dist_spec is None:
        dist_spec = {}
    self.class_name = class_def.__name__
    self.class_doc = class_def.__doc__
    self._ctor_template_class = ctor_template_cls
    self.jit_methods = jit_methods
    self.jit_props = jit_props
    self.jit_static_methods = jit_static_methods
    self.struct = struct
    self.dist_spec = dist_spec
    kdeh__xsgu = ','.join('{0}:{1}'.format(mifa__owd, ojxhs__sdmzi) for 
        mifa__owd, ojxhs__sdmzi in struct.items())
    hok__zhrr = ','.join('{0}:{1}'.format(mifa__owd, ojxhs__sdmzi) for 
        mifa__owd, ojxhs__sdmzi in dist_spec.items())
    fxxa__cbxe = '{0}.{1}#{2:x}<{3}><{4}>'.format(self.name_prefix, self.
        class_name, id(self), kdeh__xsgu, hok__zhrr)
    super(types.misc.ClassType, self).__init__(fxxa__cbxe)


if _check_numba_change:
    lines = inspect.getsource(types.misc.ClassType.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '2b848ea82946c88f540e81f93ba95dfa7cd66045d944152a337fe2fc43451c30':
        warnings.warn('types.misc.ClassType.__init__ has changed')
types.misc.ClassType.__init__ = ClassType__init__


def jitclass(cls_or_spec=None, spec=None, **options):
    if cls_or_spec is not None and spec is None and not isinstance(cls_or_spec,
        type):
        spec = cls_or_spec
        cls_or_spec = None

    def wrap(cls):
        if numba.core.config.DISABLE_JIT:
            return cls
        else:
            from numba.experimental.jitclass.base import ClassBuilder
            return register_class_type(cls, spec, types.ClassType,
                ClassBuilder, **options)
    if cls_or_spec is None:
        return wrap
    else:
        return wrap(cls_or_spec)


if _check_numba_change:
    lines = inspect.getsource(jitclass_decorators.jitclass)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '265f1953ee5881d1a5d90238d3c932cd300732e41495657e65bf51e59f7f4af5':
        warnings.warn('jitclass_decorators.jitclass has changed')


def CallConstraint_resolve(self, typeinfer, typevars, fnty):
    assert fnty
    context = typeinfer.context
    edjb__oyed = numba.core.typeinfer.fold_arg_vars(typevars, self.args,
        self.vararg, self.kws)
    if edjb__oyed is None:
        return
    gar__nbwz, iwgo__nczju = edjb__oyed
    for a in itertools.chain(gar__nbwz, iwgo__nczju.values()):
        if not a.is_precise() and not isinstance(a, types.Array):
            return
    if isinstance(fnty, types.TypeRef):
        fnty = fnty.instance_type
    try:
        sig = typeinfer.resolve_call(fnty, gar__nbwz, iwgo__nczju)
    except ForceLiteralArg as e:
        fjx__sau = (fnty.this,) + tuple(self.args) if isinstance(fnty,
            types.BoundFunction) else self.args
        folded = e.fold_arguments(fjx__sau, self.kws)
        seoe__iroqf = set()
        zshj__pvq = set()
        znwe__kfvd = {}
        for pycb__dcylc in e.requested_args:
            odof__qlmg = typeinfer.func_ir.get_definition(folded[pycb__dcylc])
            if isinstance(odof__qlmg, ir.Arg):
                seoe__iroqf.add(odof__qlmg.index)
                if odof__qlmg.index in e.file_infos:
                    znwe__kfvd[odof__qlmg.index] = e.file_infos[odof__qlmg.
                        index]
            else:
                zshj__pvq.add(pycb__dcylc)
        if zshj__pvq:
            raise TypingError('Cannot request literal type.', loc=self.loc)
        elif seoe__iroqf:
            raise ForceLiteralArg(seoe__iroqf, loc=self.loc, file_infos=
                znwe__kfvd)
    if sig is None:
        lhrq__twjm = 'Invalid use of {0} with parameters ({1})'
        args = [str(a) for a in gar__nbwz]
        args += [('%s=%s' % (mifa__owd, ojxhs__sdmzi)) for mifa__owd,
            ojxhs__sdmzi in sorted(iwgo__nczju.items())]
        nsjd__nkppg = lhrq__twjm.format(fnty, ', '.join(map(str, args)))
        xco__pefrj = context.explain_function_type(fnty)
        msg = '\n'.join([nsjd__nkppg, xco__pefrj])
        raise TypingError(msg)
    typeinfer.add_type(self.target, sig.return_type, loc=self.loc)
    if isinstance(fnty, types.BoundFunction
        ) and sig.recvr is not None and sig.recvr != fnty.this:
        zgh__eirn = context.unify_pairs(sig.recvr, fnty.this)
        if zgh__eirn is None and fnty.this.is_precise(
            ) and sig.recvr.is_precise():
            msg = 'Cannot refine type {} to {}'.format(sig.recvr, fnty.this)
            raise TypingError(msg, loc=self.loc)
        if zgh__eirn is not None and zgh__eirn.is_precise():
            tqoxh__goec = fnty.copy(this=zgh__eirn)
            typeinfer.propagate_refined_type(self.func, tqoxh__goec)
    if not sig.return_type.is_precise():
        nwunx__utjd = typevars[self.target]
        if nwunx__utjd.defined:
            ubh__fzm = nwunx__utjd.getone()
            if context.unify_pairs(ubh__fzm, sig.return_type) == ubh__fzm:
                sig = sig.replace(return_type=ubh__fzm)
    self.signature = sig
    self._add_refine_map(typeinfer, typevars, sig)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typeinfer.CallConstraint.resolve)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c78cd8ffc64b836a6a2ddf0362d481b52b9d380c5249920a87ff4da052ce081f':
        warnings.warn('numba.core.typeinfer.CallConstraint.resolve has changed'
            )
numba.core.typeinfer.CallConstraint.resolve = CallConstraint_resolve


def ForceLiteralArg__init__(self, arg_indices, fold_arguments=None, loc=
    None, file_infos=None):
    super(ForceLiteralArg, self).__init__(
        'Pseudo-exception to force literal arguments in the dispatcher',
        loc=loc)
    self.requested_args = frozenset(arg_indices)
    self.fold_arguments = fold_arguments
    if file_infos is None:
        self.file_infos = {}
    else:
        self.file_infos = file_infos


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b241d5e36a4cf7f4c73a7ad3238693612926606c7a278cad1978070b82fb55ef':
        warnings.warn('numba.core.errors.ForceLiteralArg.__init__ has changed')
numba.core.errors.ForceLiteralArg.__init__ = ForceLiteralArg__init__


def ForceLiteralArg_bind_fold_arguments(self, fold_arguments):
    e = ForceLiteralArg(self.requested_args, fold_arguments, loc=self.loc,
        file_infos=self.file_infos)
    return numba.core.utils.chain_exception(e, self)


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.
        bind_fold_arguments)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1e93cca558f7c604a47214a8f2ec33ee994104cb3e5051166f16d7cc9315141d':
        warnings.warn(
            'numba.core.errors.ForceLiteralArg.bind_fold_arguments has changed'
            )
numba.core.errors.ForceLiteralArg.bind_fold_arguments = (
    ForceLiteralArg_bind_fold_arguments)


def ForceLiteralArg_combine(self, other):
    if not isinstance(other, ForceLiteralArg):
        eayy__tuwn = '*other* must be a {} but got a {} instead'
        raise TypeError(eayy__tuwn.format(ForceLiteralArg, type(other)))
    return ForceLiteralArg(self.requested_args | other.requested_args, {**
        self.file_infos, **other.file_infos})


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.combine)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '49bf06612776f5d755c1c7d1c5eb91831a57665a8fed88b5651935f3bf33e899':
        warnings.warn('numba.core.errors.ForceLiteralArg.combine has changed')
numba.core.errors.ForceLiteralArg.combine = ForceLiteralArg_combine


def _get_global_type(self, gv):
    from bodo.utils.typing import FunctionLiteral
    ty = self._lookup_global(gv)
    if ty is not None:
        return ty
    if isinstance(gv, pytypes.ModuleType):
        return types.Module(gv)
    if isinstance(gv, pytypes.FunctionType):
        return FunctionLiteral(gv)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.context.BaseContext.
        _get_global_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8ffe6b81175d1eecd62a37639b5005514b4477d88f35f5b5395041ac8c945a4a':
        warnings.warn(
            'numba.core.typing.context.BaseContext._get_global_type has changed'
            )
numba.core.typing.context.BaseContext._get_global_type = _get_global_type


def _legalize_args(self, func_ir, args, kwargs, loc, func_globals,
    func_closures):
    from numba.core import sigutils
    from bodo.utils.transform import get_const_value_inner
    if args:
        raise errors.CompilerError(
            "objectmode context doesn't take any positional arguments")
    ffwp__kvyn = {}

    def report_error(varname, msg, loc):
        raise errors.CompilerError(
            f'Error handling objmode argument {varname!r}. {msg}', loc=loc)
    for mifa__owd, ojxhs__sdmzi in kwargs.items():
        ukyn__wztfw = None
        try:
            affzu__bro = ir.Var(ir.Scope(None, loc), ir_utils.mk_unique_var
                ('dummy'), loc)
            func_ir._definitions[affzu__bro.name] = [ojxhs__sdmzi]
            ukyn__wztfw = get_const_value_inner(func_ir, affzu__bro)
            func_ir._definitions.pop(affzu__bro.name)
            if isinstance(ukyn__wztfw, str):
                ukyn__wztfw = sigutils._parse_signature_string(ukyn__wztfw)
            assert isinstance(ukyn__wztfw, types.Type)
            ffwp__kvyn[mifa__owd] = ukyn__wztfw
        except:
            msg = (
                'The value must be a compile-time constant either as a non-local variable or an expression that refers to a Bodo type.'
                )
            if isinstance(ukyn__wztfw, ir.UndefinedType):
                msg = f'not defined.'
                if isinstance(ojxhs__sdmzi, ir.Global):
                    msg = f'Global {ojxhs__sdmzi.name!r} is not defined.'
                if isinstance(ojxhs__sdmzi, ir.FreeVar):
                    msg = f'Freevar {ojxhs__sdmzi.name!r} is not defined.'
            if isinstance(ojxhs__sdmzi, ir.Expr
                ) and ojxhs__sdmzi.op == 'getattr':
                msg = 'Getattr cannot be resolved at compile-time.'
            report_error(varname=mifa__owd, msg=msg, loc=loc)
    for fxxa__cbxe, typ in ffwp__kvyn.items():
        self._legalize_arg_type(fxxa__cbxe, typ, loc)
    return ffwp__kvyn


if _check_numba_change:
    lines = inspect.getsource(numba.core.withcontexts._ObjModeContextType.
        _legalize_args)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '867c9ba7f1bcf438be56c38e26906bb551f59a99f853a9f68b71208b107c880e':
        warnings.warn(
            'numba.core.withcontexts._ObjModeContextType._legalize_args has changed'
            )
numba.core.withcontexts._ObjModeContextType._legalize_args = _legalize_args


def op_FORMAT_VALUE_byteflow(self, state, inst):
    fzsa__kwr = inst.arg
    if fzsa__kwr & 3 != 0:
        msg = 'str/repr/ascii conversion in f-strings not supported yet'
        raise errors.UnsupportedError(msg, loc=self.get_debug_loc(inst.lineno))
    format_spec = None
    if fzsa__kwr & 4 == 4:
        format_spec = state.pop()
    value = state.pop()
    fmtvar = state.make_temp()
    res = state.make_temp()
    state.append(inst, value=value, res=res, fmtvar=fmtvar, format_spec=
        format_spec)
    state.push(res)


def op_BUILD_STRING_byteflow(self, state, inst):
    vbsx__wugq = inst.arg
    assert vbsx__wugq > 0, 'invalid BUILD_STRING count'
    strings = list(reversed([state.pop() for _ in range(vbsx__wugq)]))
    tmps = [state.make_temp() for _ in range(vbsx__wugq - 1)]
    state.append(inst, strings=strings, tmps=tmps)
    state.push(tmps[-1])


numba.core.byteflow.TraceRunner.op_FORMAT_VALUE = op_FORMAT_VALUE_byteflow
numba.core.byteflow.TraceRunner.op_BUILD_STRING = op_BUILD_STRING_byteflow


def op_FORMAT_VALUE_interpreter(self, inst, value, res, fmtvar, format_spec):
    value = self.get(value)
    sxfm__fmpe = ir.Global('format', format, loc=self.loc)
    self.store(value=sxfm__fmpe, name=fmtvar)
    args = (value, self.get(format_spec)) if format_spec else (value,)
    cwoq__nxs = ir.Expr.call(self.get(fmtvar), args, (), loc=self.loc)
    self.store(value=cwoq__nxs, name=res)


def op_BUILD_STRING_interpreter(self, inst, strings, tmps):
    vbsx__wugq = inst.arg
    assert vbsx__wugq > 0, 'invalid BUILD_STRING count'
    rqt__dzdmf = self.get(strings[0])
    for other, brla__ciely in zip(strings[1:], tmps):
        other = self.get(other)
        ree__fdej = ir.Expr.binop(operator.add, lhs=rqt__dzdmf, rhs=other,
            loc=self.loc)
        self.store(ree__fdej, brla__ciely)
        rqt__dzdmf = self.get(brla__ciely)


numba.core.interpreter.Interpreter.op_FORMAT_VALUE = (
    op_FORMAT_VALUE_interpreter)
numba.core.interpreter.Interpreter.op_BUILD_STRING = (
    op_BUILD_STRING_interpreter)


def object_hasattr_string(self, obj, attr):
    from llvmlite.llvmpy.core import Type
    dft__zvzxg = self.context.insert_const_string(self.module, attr)
    fnty = Type.function(Type.int(), [self.pyobj, self.cstring])
    fn = self._get_function(fnty, name='PyObject_HasAttrString')
    return self.builder.call(fn, [obj, dft__zvzxg])


numba.core.pythonapi.PythonAPI.object_hasattr_string = object_hasattr_string


@typeof_impl.register(dict)
def _typeof_dict(val, c):
    if len(val) == 0:
        raise ValueError('Cannot type empty dict')
    mifa__owd, ojxhs__sdmzi = next(iter(val.items()))
    syaif__qvw = typeof_impl(mifa__owd, c)
    ofbwy__easyt = typeof_impl(ojxhs__sdmzi, c)
    if syaif__qvw is None or ofbwy__easyt is None:
        raise ValueError(
            f'Cannot type dict element type {type(mifa__owd)}, {type(ojxhs__sdmzi)}'
            )
    return types.DictType(syaif__qvw, ofbwy__easyt)


def unbox_dicttype(typ, val, c):
    from llvmlite import ir as lir
    from numba.typed import dictobject
    from numba.typed.typeddict import Dict
    context = c.context
    jiga__oalym = cgutils.alloca_once_value(c.builder, val)
    eqq__dmd = c.pyapi.object_hasattr_string(val, '_opaque')
    mcpso__wdhry = c.builder.icmp_unsigned('==', eqq__dmd, lir.Constant(
        eqq__dmd.type, 0))
    zsa__pww = typ.key_type
    bsmus__gmlb = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(zsa__pww, bsmus__gmlb)

    def copy_dict(out_dict, in_dict):
        for mifa__owd, ojxhs__sdmzi in in_dict.items():
            out_dict[mifa__owd] = ojxhs__sdmzi
    with c.builder.if_then(mcpso__wdhry):
        vth__dqah = c.pyapi.unserialize(c.pyapi.serialize_object(make_dict))
        snbpt__ntc = c.pyapi.call_function_objargs(vth__dqah, [])
        toonx__imr = c.pyapi.unserialize(c.pyapi.serialize_object(copy_dict))
        c.pyapi.call_function_objargs(toonx__imr, [snbpt__ntc, val])
        c.builder.store(snbpt__ntc, jiga__oalym)
    val = c.builder.load(jiga__oalym)
    lrk__cwpx = c.pyapi.unserialize(c.pyapi.serialize_object(Dict))
    sbctw__eiw = c.pyapi.object_type(val)
    kbg__wxql = c.builder.icmp_unsigned('==', sbctw__eiw, lrk__cwpx)
    with c.builder.if_else(kbg__wxql) as (then, orelse):
        with then:
            dnpe__bula = c.pyapi.object_getattr_string(val, '_opaque')
            azfhk__vtr = types.MemInfoPointer(types.voidptr)
            nedbf__rdx = c.unbox(azfhk__vtr, dnpe__bula)
            mi = nedbf__rdx.value
            jgbj__gswt = azfhk__vtr, typeof(typ)

            def convert(mi, typ):
                return dictobject._from_meminfo(mi, typ)
            sig = signature(typ, *jgbj__gswt)
            aek__tmmk = context.get_constant_null(jgbj__gswt[1])
            args = mi, aek__tmmk
            odu__hfojw, fgw__dsng = c.pyapi.call_jit_code(convert, sig, args)
            c.context.nrt.decref(c.builder, typ, fgw__dsng)
            c.pyapi.decref(dnpe__bula)
            wiprz__hycvp = c.builder.basic_block
        with orelse:
            c.pyapi.err_format('PyExc_TypeError',
                "can't unbox a %S as a %S", sbctw__eiw, lrk__cwpx)
            scfpw__buym = c.builder.basic_block
    zwztx__ukpvk = c.builder.phi(fgw__dsng.type)
    ziz__crpm = c.builder.phi(odu__hfojw.type)
    zwztx__ukpvk.add_incoming(fgw__dsng, wiprz__hycvp)
    zwztx__ukpvk.add_incoming(fgw__dsng.type(None), scfpw__buym)
    ziz__crpm.add_incoming(odu__hfojw, wiprz__hycvp)
    ziz__crpm.add_incoming(cgutils.true_bit, scfpw__buym)
    c.pyapi.decref(lrk__cwpx)
    c.pyapi.decref(sbctw__eiw)
    with c.builder.if_then(mcpso__wdhry):
        c.pyapi.decref(val)
    return NativeValue(zwztx__ukpvk, is_error=ziz__crpm)


import numba.typed.typeddict
if _check_numba_change:
    lines = inspect.getsource(numba.core.pythonapi._unboxers.functions[
        numba.core.types.DictType])
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5f6f183b94dc57838538c668a54c2476576c85d8553843f3219f5162c61e7816':
        warnings.warn('unbox_dicttype has changed')
numba.core.pythonapi._unboxers.functions[types.DictType] = unbox_dicttype


def mk_alloc(typingctx, typemap, calltypes, lhs, size_var, dtype, scope,
    loc, lhs_typ):
    import numpy
    from numba.core.ir_utils import convert_size_to_var, get_np_ufunc_typ, mk_unique_var
    wqlw__utaz = []
    hrgcr__aknar = 1
    cjm__qhhr = types.intp
    if isinstance(size_var, tuple):
        if len(size_var) == 1:
            size_var = size_var[0]
            size_var = convert_size_to_var(size_var, typemap, scope, loc,
                wqlw__utaz)
        else:
            hrgcr__aknar = len(size_var)
            voakk__rck = ir.Var(scope, mk_unique_var('$tuple_var'), loc)
            if typemap:
                typemap[voakk__rck.name] = types.containers.UniTuple(types.
                    intp, hrgcr__aknar)
            zgw__wavbe = [convert_size_to_var(jxw__ttlp, typemap, scope,
                loc, wqlw__utaz) for jxw__ttlp in size_var]
            rdvj__pmu = ir.Expr.build_tuple(zgw__wavbe, loc)
            well__nbe = ir.Assign(rdvj__pmu, voakk__rck, loc)
            wqlw__utaz.append(well__nbe)
            size_var = voakk__rck
            cjm__qhhr = types.containers.UniTuple(types.intp, hrgcr__aknar)
    lssa__wtwp = ir.Var(scope, mk_unique_var('$np_g_var'), loc)
    if typemap:
        typemap[lssa__wtwp.name] = types.misc.Module(numpy)
    bln__vjao = ir.Global('np', numpy, loc)
    swd__rcld = ir.Assign(bln__vjao, lssa__wtwp, loc)
    uhzj__wwec = ir.Expr.getattr(lssa__wtwp, 'empty', loc)
    ghd__nykut = ir.Var(scope, mk_unique_var('$empty_attr_attr'), loc)
    if typemap:
        typemap[ghd__nykut.name] = get_np_ufunc_typ(numpy.empty)
    adynj__tfpz = ir.Assign(uhzj__wwec, ghd__nykut, loc)
    nsycv__xdxvx = str(dtype)
    mbx__vixb = ir.Var(scope, mk_unique_var('$np_typ_var'), loc)
    if typemap:
        typemap[mbx__vixb.name] = types.functions.NumberClass(dtype)
    if isinstance(dtype, (types.NPDatetime, types.NPTimedelta)
        ) and dtype.unit != '':
        swwxr__qamr = ir.Const(nsycv__xdxvx, loc)
        pqdoe__ztsmo = ir.Assign(swwxr__qamr, mbx__vixb, loc)
    else:
        if nsycv__xdxvx == 'bool':
            nsycv__xdxvx = 'bool_'
        paiua__ovv = ir.Expr.getattr(lssa__wtwp, nsycv__xdxvx, loc)
        pqdoe__ztsmo = ir.Assign(paiua__ovv, mbx__vixb, loc)
    vkk__fjzk = ir.Expr.call(ghd__nykut, [size_var, mbx__vixb], (), loc)
    if calltypes:
        eva__wxli = typemap[ghd__nykut.name].get_call_type(typingctx, [
            cjm__qhhr, types.functions.NumberClass(dtype)], {})
        eva__wxli._return_type = lhs_typ.copy(layout='C'
            ) if lhs_typ.layout == 'F' else lhs_typ
        calltypes[vkk__fjzk] = eva__wxli
    if lhs_typ.layout == 'F':
        lrz__vvqd = lhs_typ.copy(layout='C')
        peo__rtjk = ir.Var(scope, mk_unique_var('$empty_c_var'), loc)
        if typemap:
            typemap[peo__rtjk.name] = lhs_typ.copy(layout='C')
        tdlmu__dacjn = ir.Assign(vkk__fjzk, peo__rtjk, loc)
        ahgrz__khkuj = ir.Expr.getattr(lssa__wtwp, 'asfortranarray', loc)
        ivh__rpaku = ir.Var(scope, mk_unique_var('$asfortran_array_attr'), loc)
        if typemap:
            typemap[ivh__rpaku.name] = get_np_ufunc_typ(numpy.asfortranarray)
        njlfb__gqqiw = ir.Assign(ahgrz__khkuj, ivh__rpaku, loc)
        tvzwx__lvrhs = ir.Expr.call(ivh__rpaku, [peo__rtjk], (), loc)
        if calltypes:
            calltypes[tvzwx__lvrhs] = typemap[ivh__rpaku.name].get_call_type(
                typingctx, [lrz__vvqd], {})
        wrxlv__jdute = ir.Assign(tvzwx__lvrhs, lhs, loc)
        wqlw__utaz.extend([swd__rcld, adynj__tfpz, pqdoe__ztsmo,
            tdlmu__dacjn, njlfb__gqqiw, wrxlv__jdute])
    else:
        kohu__cfyed = ir.Assign(vkk__fjzk, lhs, loc)
        wqlw__utaz.extend([swd__rcld, adynj__tfpz, pqdoe__ztsmo, kohu__cfyed])
    return wqlw__utaz


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.mk_alloc)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'ee194e9b4637c385a32a8eadd998a665d29a1f787e0e1f46b160ea2dcabd3b26':
        warnings.warn('mk_alloc has changed')
numba.core.ir_utils.mk_alloc = mk_alloc
numba.parfors.parfor.mk_alloc = mk_alloc


def inline_ir(self, caller_ir, block, i, callee_ir, callee_freevars,
    arg_typs=None):
    from numba.core.inline_closurecall import _add_definitions, _debug_dump, _get_all_scopes, _get_callee_args, _replace_args_with, _replace_returns, add_offset_to_labels, find_topo_order, next_label, replace_vars, simplify_CFG

    def copy_ir(the_ir):
        mcyko__mbalx = the_ir.copy()
        mcyko__mbalx.blocks = {}
        for megd__bbgmw, block in the_ir.blocks.items():
            utapj__jtc = copy.deepcopy(the_ir.blocks[megd__bbgmw])
            utapj__jtc.body = []
            for stmt in the_ir.blocks[megd__bbgmw].body:
                sgo__xini = copy.deepcopy(stmt)
                utapj__jtc.body.append(sgo__xini)
            mcyko__mbalx.blocks[megd__bbgmw] = utapj__jtc
        return mcyko__mbalx
    callee_ir = copy_ir(callee_ir)
    if self.validator is not None:
        self.validator(callee_ir)
    jodn__efzcm = callee_ir.copy()
    scope = block.scope
    lzejo__ajx = block.body[i]
    mvpw__wau = lzejo__ajx.value
    sbn__nuwv = callee_ir.blocks
    zcnl__xlz = max(ir_utils._the_max_label.next(), max(caller_ir.blocks.
        keys()))
    sbn__nuwv = add_offset_to_labels(sbn__nuwv, zcnl__xlz + 1)
    sbn__nuwv = simplify_CFG(sbn__nuwv)
    callee_ir.blocks = sbn__nuwv
    ien__raunh = min(sbn__nuwv.keys())
    zcnl__xlz = max(sbn__nuwv.keys())
    ir_utils._the_max_label.update(zcnl__xlz)
    self.debug_print('After relabel')
    _debug_dump(callee_ir)
    vzgp__kogc = _get_all_scopes(sbn__nuwv)
    self.debug_print('callee_scopes = ', vzgp__kogc)
    assert len(vzgp__kogc) == 1
    qgcz__hmij = vzgp__kogc[0]
    xkz__oiz = {}
    for var in qgcz__hmij.localvars._con.values():
        if not var.name in callee_freevars:
            oiibj__tpt = scope.redefine(mk_unique_var(var.name), loc=var.loc)
            xkz__oiz[var.name] = oiibj__tpt
    self.debug_print('var_dict = ', xkz__oiz)
    replace_vars(sbn__nuwv, xkz__oiz)
    self.debug_print('After local var rename')
    _debug_dump(callee_ir)
    zla__miqar = callee_ir.func_id.func
    args = _get_callee_args(mvpw__wau, zla__miqar, block.body[i].loc, caller_ir
        )
    if self._permit_update_type_and_call_maps:
        if arg_typs is None:
            raise TypeError('arg_typs should have a value not None')
        self.update_type_and_call_maps(callee_ir, arg_typs)
        sbn__nuwv = callee_ir.blocks
    self.debug_print('After arguments rename: ')
    _debug_dump(callee_ir)
    _replace_args_with(sbn__nuwv, args)
    kauh__ouc = []
    utapj__jtc = ir.Block(scope, block.loc)
    utapj__jtc.body = block.body[i + 1:]
    hqtdw__fad = next_label()
    caller_ir.blocks[hqtdw__fad] = utapj__jtc
    kauh__ouc.append((hqtdw__fad, utapj__jtc))
    block.body = block.body[:i]
    block.body.append(ir.Jump(ien__raunh, lzejo__ajx.loc))
    ouxp__gsxsw = find_topo_order(sbn__nuwv)
    _replace_returns(sbn__nuwv, lzejo__ajx.target, hqtdw__fad)
    if (lzejo__ajx.target.name in caller_ir._definitions and mvpw__wau in
        caller_ir._definitions[lzejo__ajx.target.name]):
        caller_ir._definitions[lzejo__ajx.target.name].remove(mvpw__wau)
    for xcfs__qona in ouxp__gsxsw:
        block = sbn__nuwv[xcfs__qona]
        block.scope = scope
        _add_definitions(caller_ir, block)
        caller_ir.blocks[xcfs__qona] = block
        kauh__ouc.append((xcfs__qona, block))
    self.debug_print('After merge in')
    _debug_dump(caller_ir)
    return jodn__efzcm, sbn__nuwv, xkz__oiz, kauh__ouc


if _check_numba_change:
    lines = inspect.getsource(numba.core.inline_closurecall.InlineWorker.
        inline_ir)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '9a06c2daf1ac4db26d0d6c02a85c3e661909d8190b9ae354283e1631c9693d20':
        warnings.warn('inline_ir has changed')
numba.core.inline_closurecall.InlineWorker.inline_ir = inline_ir


def ufunc_find_matching_loop(ufunc, arg_types):
    import numpy as np
    from numba.np import npdatetime_helpers
    from numba.np.numpy_support import UFuncLoopSpec, as_dtype, from_dtype, ufunc_can_cast
    qzl__ggxt = arg_types[:ufunc.nin]
    yeufb__qna = arg_types[ufunc.nin:]
    assert len(qzl__ggxt) == ufunc.nin
    try:
        bnd__qiy = [as_dtype(x) for x in qzl__ggxt]
    except NotImplementedError as zwsnc__vldr:
        return None
    try:
        dmj__qkz = [as_dtype(x) for x in yeufb__qna]
    except NotImplementedError as zwsnc__vldr:
        return None
    ojojc__dmuk = any(czft__trw.kind in 'iu' for czft__trw in bnd__qiy
        ) and any(czft__trw.kind in 'cf' for czft__trw in bnd__qiy)

    def choose_types(numba_types, ufunc_letters):
        assert len(ufunc_letters) >= len(numba_types)
        types = [(xkw__dunl if nkyya__kyb in 'mM' else from_dtype(np.dtype(
            nkyya__kyb))) for xkw__dunl, nkyya__kyb in zip(numba_types,
            ufunc_letters)]
        types += [from_dtype(np.dtype(nkyya__kyb)) for nkyya__kyb in
            ufunc_letters[len(numba_types):]]
        return types

    def set_output_dt_units(inputs, outputs, ufunc_inputs):

        def make_specific(outputs, unit):
            acxl__xria = []
            for wqlw__utaz in outputs:
                if isinstance(wqlw__utaz, types.NPTimedelta
                    ) and wqlw__utaz.unit == '':
                    acxl__xria.append(types.NPTimedelta(unit))
                else:
                    acxl__xria.append(wqlw__utaz)
            return acxl__xria

        def make_datetime_specific(outputs, dt_unit, td_unit):
            acxl__xria = []
            for wqlw__utaz in outputs:
                if isinstance(wqlw__utaz, types.NPDatetime
                    ) and wqlw__utaz.unit == '':
                    unit = npdatetime_helpers.combine_datetime_timedelta_units(
                        dt_unit, td_unit)
                    acxl__xria.append(types.NPDatetime(unit))
                else:
                    acxl__xria.append(wqlw__utaz)
            return acxl__xria
        if ufunc_inputs == 'mm':
            if all(ejjb__dafl.unit == inputs[0].unit for ejjb__dafl in inputs):
                unit = inputs[0].unit
                acxl__xria = make_specific(outputs, unit)
            else:
                return outputs
            return acxl__xria
        elif ufunc_inputs == 'mM':
            td_unit = inputs[0].unit
            dt_unit = inputs[1].unit
            return make_datetime_specific(outputs, dt_unit, td_unit)
        elif ufunc_inputs == 'Mm':
            dt_unit = inputs[0].unit
            td_unit = inputs[1].unit
            return make_datetime_specific(outputs, dt_unit, td_unit)
        elif ufunc_inputs[0] == 'm':
            unit = inputs[0].unit
            acxl__xria = make_specific(outputs, unit)
            return acxl__xria
    for ftgc__gqiyy in ufunc.types:
        ufunc_inputs = ftgc__gqiyy[:ufunc.nin]
        ludx__nmric = ftgc__gqiyy[-ufunc.nout:] if ufunc.nout else []
        if 'O' in ufunc_inputs:
            continue
        yctl__zqspf = True
        for eofp__vtu, ehkou__ldd in zip(bnd__qiy, ufunc_inputs):
            if eofp__vtu.char in 'mM' or ehkou__ldd in 'mM':
                if eofp__vtu.char != ehkou__ldd:
                    yctl__zqspf = False
                    break
            elif not ufunc_can_cast(eofp__vtu.char, ehkou__ldd, ojojc__dmuk,
                'safe'):
                yctl__zqspf = False
                break
        if yctl__zqspf:
            for eofp__vtu, ehkou__ldd in zip(dmj__qkz, ludx__nmric):
                if eofp__vtu.char not in 'mM' and not ufunc_can_cast(ehkou__ldd
                    , eofp__vtu.char, ojojc__dmuk, 'same_kind'):
                    yctl__zqspf = False
                    break
        if yctl__zqspf:
            try:
                inputs = choose_types(qzl__ggxt, ufunc_inputs)
                outputs = choose_types(yeufb__qna, ludx__nmric)
                if ufunc_inputs[0] == 'm' or ufunc_inputs == 'Mm':
                    outputs = set_output_dt_units(inputs, outputs, ufunc_inputs
                        )
            except NotImplementedError as zwsnc__vldr:
                continue
            else:
                return UFuncLoopSpec(inputs, outputs, ftgc__gqiyy)
    return None


if _check_numba_change:
    lines = inspect.getsource(numba.np.numpy_support.ufunc_find_matching_loop)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '31d1c4f9c2fb0dd0642bc3717e64f79a846e0dc5fdeecd36392cf546e4d7d85b':
        warnings.warn('ufunc_find_matching_loop has changed')
numba.np.numpy_support.ufunc_find_matching_loop = ufunc_find_matching_loop
numba.core.typing.npydecl.ufunc_find_matching_loop = ufunc_find_matching_loop
numba.np.ufunc.gufunc.ufunc_find_matching_loop = ufunc_find_matching_loop
import numba.np.npyimpl
numba.np.npyimpl.ufunc_find_matching_loop = ufunc_find_matching_loop


def resolve_number___call__(self, classty):
    import numpy as np
    from numba.core.typing.templates import make_callable_template
    ty = classty.instance_type

    def typer(val):
        if isinstance(val, (types.BaseTuple, types.Sequence)):
            fnty = self.context.resolve_value_type(np.array)
            sig = fnty.get_call_type(self.context, (val, types.DType(ty)), {})
            return sig.return_type
        elif isinstance(val, (types.Number, types.Boolean)):
            return ty
        elif val == types.unicode_type:
            return ty
        elif val in [types.NPDatetime('ns'), types.NPTimedelta('ns')]:
            return ty
        elif isinstance(val, types.Array
            ) and val.ndim == 0 and val.dtype == ty:
            return ty
        else:
            msg = f'Casting {val} to {ty} directly is unsupported.'
            if isinstance(val, types.Array):
                msg += f" Try doing '<array>.astype(np.{ty})' instead"
            raise errors.TypingError(msg)
    return types.Function(make_callable_template(key=ty, typer=typer))


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.builtins.
        NumberClassAttribute.resolve___call__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '6708eb64f6df62710ebaaed6232f324a8ffb0e176e14a9ffa65d7f0e12380c2d':
        warnings.warn('Number Class resolve___call__ has changed')
numba.core.typing.builtins.NumberClassAttribute.resolve___call__ = (
    resolve_number___call__)


def on_assign(self, states, assign):
    if assign.target.name == states['varname']:
        scope = states['scope']
        pmpf__kbpwl = states['defmap']
        if len(pmpf__kbpwl) == 0:
            xtk__hht = assign.target
            numba.core.ssa._logger.debug('first assign: %s', xtk__hht)
            if xtk__hht.name not in scope.localvars:
                xtk__hht = scope.define(assign.target.name, loc=assign.loc)
        else:
            xtk__hht = scope.redefine(assign.target.name, loc=assign.loc)
        assign = ir.Assign(target=xtk__hht, value=assign.value, loc=assign.loc)
        pmpf__kbpwl[states['label']].append(assign)
    return assign


if _check_numba_change:
    lines = inspect.getsource(numba.core.ssa._FreshVarHandler.on_assign)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '922c4f9807455f81600b794bbab36f9c6edfecfa83fda877bf85f465db7865e8':
        warnings.warn('_FreshVarHandler on_assign has changed')
numba.core.ssa._FreshVarHandler.on_assign = on_assign


def get_np_ufunc_typ_lst(func):
    from numba.core import typing
    iib__ltc = []
    for mifa__owd, ojxhs__sdmzi in typing.npydecl.registry.globals:
        if mifa__owd == func:
            iib__ltc.append(ojxhs__sdmzi)
    for mifa__owd, ojxhs__sdmzi in typing.templates.builtin_registry.globals:
        if mifa__owd == func:
            iib__ltc.append(ojxhs__sdmzi)
    if len(iib__ltc) == 0:
        raise RuntimeError('type for func ', func, ' not found')
    return iib__ltc


def canonicalize_array_math(func_ir, typemap, calltypes, typingctx):
    import numpy
    from numba.core.ir_utils import arr_math, find_topo_order, mk_unique_var
    blocks = func_ir.blocks
    zxj__uyh = {}
    ouxp__gsxsw = find_topo_order(blocks)
    xrak__tfkg = {}
    for xcfs__qona in ouxp__gsxsw:
        block = blocks[xcfs__qona]
        clv__drzh = []
        for stmt in block.body:
            if isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr):
                lhs = stmt.target.name
                maxxs__sjsm = stmt.value
                if (maxxs__sjsm.op == 'getattr' and maxxs__sjsm.attr in
                    arr_math and isinstance(typemap[maxxs__sjsm.value.name],
                    types.npytypes.Array)):
                    maxxs__sjsm = stmt.value
                    luih__gssbh = maxxs__sjsm.value
                    zxj__uyh[lhs] = luih__gssbh
                    scope = luih__gssbh.scope
                    loc = luih__gssbh.loc
                    lssa__wtwp = ir.Var(scope, mk_unique_var('$np_g_var'), loc)
                    typemap[lssa__wtwp.name] = types.misc.Module(numpy)
                    bln__vjao = ir.Global('np', numpy, loc)
                    swd__rcld = ir.Assign(bln__vjao, lssa__wtwp, loc)
                    maxxs__sjsm.value = lssa__wtwp
                    clv__drzh.append(swd__rcld)
                    func_ir._definitions[lssa__wtwp.name] = [bln__vjao]
                    func = getattr(numpy, maxxs__sjsm.attr)
                    gwsaq__immcg = get_np_ufunc_typ_lst(func)
                    xrak__tfkg[lhs] = gwsaq__immcg
                if (maxxs__sjsm.op == 'call' and maxxs__sjsm.func.name in
                    zxj__uyh):
                    luih__gssbh = zxj__uyh[maxxs__sjsm.func.name]
                    qxx__fin = calltypes.pop(maxxs__sjsm)
                    iqd__lciyx = qxx__fin.args[:len(maxxs__sjsm.args)]
                    pyt__bqzx = {fxxa__cbxe: typemap[ojxhs__sdmzi.name] for
                        fxxa__cbxe, ojxhs__sdmzi in maxxs__sjsm.kws}
                    qlhyd__ylrps = xrak__tfkg[maxxs__sjsm.func.name]
                    xbrd__zbxwq = None
                    for mfnk__rlzr in qlhyd__ylrps:
                        try:
                            xbrd__zbxwq = mfnk__rlzr.get_call_type(typingctx,
                                [typemap[luih__gssbh.name]] + list(
                                iqd__lciyx), pyt__bqzx)
                            typemap.pop(maxxs__sjsm.func.name)
                            typemap[maxxs__sjsm.func.name] = mfnk__rlzr
                            calltypes[maxxs__sjsm] = xbrd__zbxwq
                            break
                        except Exception as zwsnc__vldr:
                            pass
                    if xbrd__zbxwq is None:
                        raise TypeError(
                            f'No valid template found for {maxxs__sjsm.func.name}'
                            )
                    maxxs__sjsm.args = [luih__gssbh] + maxxs__sjsm.args
            clv__drzh.append(stmt)
        block.body = clv__drzh


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.canonicalize_array_math)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b2200e9100613631cc554f4b640bc1181ba7cea0ece83630122d15b86941be2e':
        warnings.warn('canonicalize_array_math has changed')
numba.core.ir_utils.canonicalize_array_math = canonicalize_array_math
numba.parfors.parfor.canonicalize_array_math = canonicalize_array_math
numba.core.inline_closurecall.canonicalize_array_math = canonicalize_array_math


def _Numpy_Rules_ufunc_handle_inputs(cls, ufunc, args, kws):
    aibbo__gxisw = ufunc.nin
    bbkvr__azvx = ufunc.nout
    qmmhl__abgyb = ufunc.nargs
    assert qmmhl__abgyb == aibbo__gxisw + bbkvr__azvx
    if len(args) < aibbo__gxisw:
        msg = "ufunc '{0}': not enough arguments ({1} found, {2} required)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args),
            aibbo__gxisw))
    if len(args) > qmmhl__abgyb:
        msg = "ufunc '{0}': too many arguments ({1} found, {2} maximum)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args),
            qmmhl__abgyb))
    args = [(a.as_array if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else a) for a in args]
    iwfnw__zxdvt = [(a.ndim if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else 0) for a in args]
    hrgcr__aknar = max(iwfnw__zxdvt)
    wfpe__anlm = args[aibbo__gxisw:]
    if not all(itir__kub == hrgcr__aknar for itir__kub in iwfnw__zxdvt[
        aibbo__gxisw:]):
        msg = "ufunc '{0}' called with unsuitable explicit output arrays."
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(isinstance(otaw__iitte, types.ArrayCompatible) and not
        isinstance(otaw__iitte, types.Bytes) for otaw__iitte in wfpe__anlm):
        msg = "ufunc '{0}' called with an explicit output that is not an array"
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(otaw__iitte.mutable for otaw__iitte in wfpe__anlm):
        msg = "ufunc '{0}' called with an explicit output that is read-only"
        raise TypingError(msg=msg.format(ufunc.__name__))
    evn__zyat = [(x.dtype if isinstance(x, types.ArrayCompatible) and not
        isinstance(x, types.Bytes) else x) for x in args]
    qfrcs__gcg = None
    if hrgcr__aknar > 0 and len(wfpe__anlm) < ufunc.nout:
        qfrcs__gcg = 'C'
        yrek__seay = [(x.layout if isinstance(x, types.ArrayCompatible) and
            not isinstance(x, types.Bytes) else '') for x in args]
        if 'C' not in yrek__seay and 'F' in yrek__seay:
            qfrcs__gcg = 'F'
    return evn__zyat, wfpe__anlm, hrgcr__aknar, qfrcs__gcg


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.npydecl.Numpy_rules_ufunc.
        _handle_inputs)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4b97c64ad9c3d50e082538795054f35cf6d2fe962c3ca40e8377a4601b344d5c':
        warnings.warn('Numpy_rules_ufunc._handle_inputs has changed')
numba.core.typing.npydecl.Numpy_rules_ufunc._handle_inputs = (
    _Numpy_Rules_ufunc_handle_inputs)
numba.np.ufunc.dufunc.npydecl.Numpy_rules_ufunc._handle_inputs = (
    _Numpy_Rules_ufunc_handle_inputs)


@classmethod
def _IPythonCacheLocator_from_function(cls, py_func, py_file):
    if not (py_file.startswith('<ipython-') or os.path.basename(os.path.
        dirname(py_file)).startswith('ipykernel_')):
        return
    self = cls(py_func, py_file)
    try:
        self.ensure_cache_path()
    except OSError as zwsnc__vldr:
        return
    return self


if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._IPythonCacheLocator.
        from_function)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'd1bcb594c7da469542b6c5c78730d30a8df03f69f92fb965a84382b4d58c32dc':
        warnings.warn('_IPythonCacheLocator from_function has changed')
numba.core.caching._IPythonCacheLocator.from_function = (
    _IPythonCacheLocator_from_function)


def DictType__init__(self, keyty, valty, initial_value=None):
    from numba.types import DictType, InitialValue, NoneType, Optional, Tuple, TypeRef, unliteral
    assert not isinstance(keyty, TypeRef)
    assert not isinstance(valty, TypeRef)
    keyty = unliteral(keyty)
    valty = unliteral(valty)
    if isinstance(keyty, (Optional, NoneType)):
        qqgxx__gvhe = 'Dict.key_type cannot be of type {}'
        raise TypingError(qqgxx__gvhe.format(keyty))
    if isinstance(valty, (Optional, NoneType)):
        qqgxx__gvhe = 'Dict.value_type cannot be of type {}'
        raise TypingError(qqgxx__gvhe.format(valty))
    self.key_type = keyty
    self.value_type = valty
    self.keyvalue_type = Tuple([keyty, valty])
    fxxa__cbxe = '{}[{},{}]<iv={}>'.format(self.__class__.__name__, keyty,
        valty, initial_value)
    super(DictType, self).__init__(fxxa__cbxe)
    InitialValue.__init__(self, initial_value)


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.containers.DictType.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '475acd71224bd51526750343246e064ff071320c0d10c17b8b8ac81d5070d094':
        warnings.warn('DictType.__init__ has changed')
numba.core.types.containers.DictType.__init__ = DictType__init__


def _legalize_arg_types(self, args):
    for i, a in enumerate(args, start=1):
        if isinstance(a, types.Dispatcher):
            msg = (
                'Does not support function type inputs into with-context for arg {}'
                )
            raise errors.TypingError(msg.format(i))


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.ObjModeLiftedWith.
        _legalize_arg_types)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4793f44ebc7da8843e8f298e08cd8a5428b4b84b89fd9d5c650273fdb8fee5ee':
        warnings.warn('ObjModeLiftedWith._legalize_arg_types has changed')
numba.core.dispatcher.ObjModeLiftedWith._legalize_arg_types = (
    _legalize_arg_types)


def Omitted__init__(self, value):
    self._value = value
    try:
        hash(value)
        self._value_key = value
    except Exception as zwsnc__vldr:
        self._value_key = id(value)
    super(types.Omitted, self).__init__('omitted(default=%r)' % (value,))


@property
def Omitted_key(self):
    return type(self._value), self._value_key


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.misc.Omitted.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4ee9f821c8bd45d9c27396a1046fb5e2d9456b308c260c0b56af9a322feaa817':
        warnings.warn('Omitted __init__ has changed')
numba.core.types.misc.Omitted.__init__ = Omitted__init__
numba.core.types.misc.Omitted.key = Omitted_key


def _overload_template_get_impl(self, args, kws):
    zxxb__ttbf = self.context, tuple(args), tuple(kws.items())
    try:
        tmxx__idd, args = self._impl_cache[zxxb__ttbf]
        return tmxx__idd, args
    except KeyError as zwsnc__vldr:
        pass
    tmxx__idd, args = self._build_impl(zxxb__ttbf, args, kws)
    return tmxx__idd, args


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadFunctionTemplate._get_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'fc53b28d15fb9a6694afcfa33a85f7e448b874aa7c040e2ac71f71a3c78f60df':
        warnings.warn('_OverloadFunctionTemplate _get_impl has changed')
numba.core.typing.templates._OverloadFunctionTemplate._get_impl = (
    _overload_template_get_impl)


def remove_dead_parfor(parfor, lives, lives_n_aliases, arg_aliases,
    alias_map, func_ir, typemap):
    from numba.core.analysis import compute_cfg_from_blocks, compute_live_map, compute_use_defs
    from numba.core.ir_utils import find_topo_order
    from numba.parfors.parfor import _add_liveness_return_block, _update_parfor_get_setitems, dummy_return_in_loop_body, get_index_var, remove_dead_parfor_recursive, simplify_parfor_body_CFG
    with dummy_return_in_loop_body(parfor.loop_body):
        dzlzq__cye = find_topo_order(parfor.loop_body)
    fxzdo__nnc = dzlzq__cye[0]
    jnug__yuwzj = {}
    _update_parfor_get_setitems(parfor.loop_body[fxzdo__nnc].body, parfor.
        index_var, alias_map, jnug__yuwzj, lives_n_aliases)
    jbm__ynctj = set(jnug__yuwzj.keys())
    for npk__dbnyt in dzlzq__cye:
        if npk__dbnyt == fxzdo__nnc:
            continue
        for stmt in parfor.loop_body[npk__dbnyt].body:
            if (isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.
                Expr) and stmt.value.op == 'getitem' and stmt.value.index.
                name == parfor.index_var.name):
                continue
            bec__qud = set(ojxhs__sdmzi.name for ojxhs__sdmzi in stmt.
                list_vars())
            ewovy__bsnmf = bec__qud & jbm__ynctj
            for a in ewovy__bsnmf:
                jnug__yuwzj.pop(a, None)
    for npk__dbnyt in dzlzq__cye:
        if npk__dbnyt == fxzdo__nnc:
            continue
        block = parfor.loop_body[npk__dbnyt]
        uwhqk__blhj = jnug__yuwzj.copy()
        _update_parfor_get_setitems(block.body, parfor.index_var, alias_map,
            uwhqk__blhj, lives_n_aliases)
    blocks = parfor.loop_body.copy()
    skwi__cbtkv = max(blocks.keys())
    ngah__tggf, voakk__rck = _add_liveness_return_block(blocks,
        lives_n_aliases, typemap)
    rcee__bwubj = ir.Jump(ngah__tggf, ir.Loc('parfors_dummy', -1))
    blocks[skwi__cbtkv].body.append(rcee__bwubj)
    ortv__vhncd = compute_cfg_from_blocks(blocks)
    ylfe__aqv = compute_use_defs(blocks)
    usznl__oqy = compute_live_map(ortv__vhncd, blocks, ylfe__aqv.usemap,
        ylfe__aqv.defmap)
    alias_set = set(alias_map.keys())
    for xcfs__qona, block in blocks.items():
        clv__drzh = []
        wjfa__euuc = {ojxhs__sdmzi.name for ojxhs__sdmzi in block.
            terminator.list_vars()}
        for fqzyg__zqu, whmz__qit in ortv__vhncd.successors(xcfs__qona):
            wjfa__euuc |= usznl__oqy[fqzyg__zqu]
        for stmt in reversed(block.body):
            hpg__mcd = wjfa__euuc & alias_set
            for ojxhs__sdmzi in hpg__mcd:
                wjfa__euuc |= alias_map[ojxhs__sdmzi]
            if (isinstance(stmt, (ir.StaticSetItem, ir.SetItem)) and 
                get_index_var(stmt).name == parfor.index_var.name and stmt.
                target.name not in wjfa__euuc and stmt.target.name not in
                arg_aliases):
                continue
            elif isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
                ) and stmt.value.op == 'call':
                mhzk__ctci = guard(find_callname, func_ir, stmt.value)
                if mhzk__ctci == ('setna', 'bodo.libs.array_kernels'
                    ) and stmt.value.args[0
                    ].name not in wjfa__euuc and stmt.value.args[0
                    ].name not in arg_aliases:
                    continue
            wjfa__euuc |= {ojxhs__sdmzi.name for ojxhs__sdmzi in stmt.
                list_vars()}
            clv__drzh.append(stmt)
        clv__drzh.reverse()
        block.body = clv__drzh
    typemap.pop(voakk__rck.name)
    blocks[skwi__cbtkv].body.pop()

    def trim_empty_parfor_branches(parfor):
        ihl__cwc = False
        blocks = parfor.loop_body.copy()
        for xcfs__qona, block in blocks.items():
            if len(block.body):
                ruz__zxljk = block.body[-1]
                if isinstance(ruz__zxljk, ir.Branch):
                    if len(blocks[ruz__zxljk.truebr].body) == 1 and len(blocks
                        [ruz__zxljk.falsebr].body) == 1:
                        nnd__lajq = blocks[ruz__zxljk.truebr].body[0]
                        dmudn__ravtd = blocks[ruz__zxljk.falsebr].body[0]
                        if isinstance(nnd__lajq, ir.Jump) and isinstance(
                            dmudn__ravtd, ir.Jump
                            ) and nnd__lajq.target == dmudn__ravtd.target:
                            parfor.loop_body[xcfs__qona].body[-1] = ir.Jump(
                                nnd__lajq.target, ruz__zxljk.loc)
                            ihl__cwc = True
                    elif len(blocks[ruz__zxljk.truebr].body) == 1:
                        nnd__lajq = blocks[ruz__zxljk.truebr].body[0]
                        if isinstance(nnd__lajq, ir.Jump
                            ) and nnd__lajq.target == ruz__zxljk.falsebr:
                            parfor.loop_body[xcfs__qona].body[-1] = ir.Jump(
                                nnd__lajq.target, ruz__zxljk.loc)
                            ihl__cwc = True
                    elif len(blocks[ruz__zxljk.falsebr].body) == 1:
                        dmudn__ravtd = blocks[ruz__zxljk.falsebr].body[0]
                        if isinstance(dmudn__ravtd, ir.Jump
                            ) and dmudn__ravtd.target == ruz__zxljk.truebr:
                            parfor.loop_body[xcfs__qona].body[-1] = ir.Jump(
                                dmudn__ravtd.target, ruz__zxljk.loc)
                            ihl__cwc = True
        return ihl__cwc
    ihl__cwc = True
    while ihl__cwc:
        """
        Process parfor body recursively.
        Note that this is the only place in this function that uses the
        argument lives instead of lives_n_aliases.  The former does not
        include the aliases of live variables but only the live variable
        names themselves.  See a comment in this function for how that
        is used.
        """
        remove_dead_parfor_recursive(parfor, lives, arg_aliases, alias_map,
            func_ir, typemap)
        simplify_parfor_body_CFG(func_ir.blocks)
        ihl__cwc = trim_empty_parfor_branches(parfor)
    nysxh__elox = len(parfor.init_block.body) == 0
    for block in parfor.loop_body.values():
        nysxh__elox &= len(block.body) == 0
    if nysxh__elox:
        return None
    return parfor


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.remove_dead_parfor)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1c9b008a7ead13e988e1efe67618d8f87f0b9f3d092cc2cd6bfcd806b1fdb859':
        warnings.warn('remove_dead_parfor has changed')
numba.parfors.parfor.remove_dead_parfor = remove_dead_parfor
numba.core.ir_utils.remove_dead_extensions[numba.parfors.parfor.Parfor
    ] = remove_dead_parfor


def simplify_parfor_body_CFG(blocks):
    from numba.core.analysis import compute_cfg_from_blocks
    from numba.core.ir_utils import simplify_CFG
    from numba.parfors.parfor import Parfor
    farkv__cbmz = 0
    for block in blocks.values():
        for stmt in block.body:
            if isinstance(stmt, Parfor):
                farkv__cbmz += 1
                parfor = stmt
                ssfga__zhkt = parfor.loop_body[max(parfor.loop_body.keys())]
                scope = ssfga__zhkt.scope
                loc = ir.Loc('parfors_dummy', -1)
                prb__okcz = ir.Var(scope, mk_unique_var('$const'), loc)
                ssfga__zhkt.body.append(ir.Assign(ir.Const(0, loc),
                    prb__okcz, loc))
                ssfga__zhkt.body.append(ir.Return(prb__okcz, loc))
                ortv__vhncd = compute_cfg_from_blocks(parfor.loop_body)
                for lmq__wtlu in ortv__vhncd.dead_nodes():
                    del parfor.loop_body[lmq__wtlu]
                parfor.loop_body = simplify_CFG(parfor.loop_body)
                ssfga__zhkt = parfor.loop_body[max(parfor.loop_body.keys())]
                ssfga__zhkt.body.pop()
                ssfga__zhkt.body.pop()
                simplify_parfor_body_CFG(parfor.loop_body)
    return farkv__cbmz


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.simplify_parfor_body_CFG)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '437ae96a5e8ec64a2b69a4f23ba8402a1d170262a5400aa0aa7bfe59e03bf726':
        warnings.warn('simplify_parfor_body_CFG has changed')
numba.parfors.parfor.simplify_parfor_body_CFG = simplify_parfor_body_CFG
