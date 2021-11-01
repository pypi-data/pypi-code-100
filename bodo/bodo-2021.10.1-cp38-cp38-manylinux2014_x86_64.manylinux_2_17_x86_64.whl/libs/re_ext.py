"""Support re module using object mode of Numba
"""
import operator
import re
import numba
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import NativeValue, box, intrinsic, lower_builtin, lower_cast, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
from bodo.libs.str_ext import string_type
from bodo.utils.typing import gen_objmode_func_overload, gen_objmode_method_overload, get_overload_const_str, is_overload_constant_str
_dummy_pat = '_BODO_DUMMY_PATTERN_'
Pattern = type(re.compile(_dummy_pat))
Match = type(re.match(_dummy_pat, _dummy_pat))


class RePatternType(types.Opaque):

    def __init__(self, pat_const=None):
        self.pat_const = pat_const
        super(RePatternType, self).__init__(name='RePatternType({})'.format
            (pat_const))


re_pattern_type = RePatternType()
types.re_pattern_type = re_pattern_type
register_model(RePatternType)(models.OpaqueModel)


@typeof_impl.register(Pattern)
def typeof_re_pattern(val, c):
    return re_pattern_type


@box(RePatternType)
def box_re_pattern(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(RePatternType)
def unbox_re_pattern(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


class ReMatchType(types.Type):

    def __init__(self):
        super(ReMatchType, self).__init__(name='ReMatchType')


re_match_type = ReMatchType()
types.re_match_type = re_match_type
types.list_str_type = types.List(string_type)
register_model(ReMatchType)(models.OpaqueModel)


@typeof_impl.register(Match)
def typeof_re_match(val, c):
    return re_match_type


@box(ReMatchType)
def box_re_match(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(ReMatchType)
def unbox_re_match(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@lower_cast(ReMatchType, types.Boolean)
def cast_match_obj_bool(context, builder, fromty, toty, val):
    out = cgutils.alloca_once_value(builder, context.get_constant(types.
        bool_, True))
    xlcbg__cfbcn = context.get_python_api(builder)
    mona__meo = builder.icmp_signed('==', val, xlcbg__cfbcn.borrow_none())
    with builder.if_then(mona__meo):
        builder.store(context.get_constant(types.bool_, False), out)
    return builder.load(out)


@intrinsic
def match_obj_is_none(typingctx, match_typ=None):
    assert match_typ == re_match_type

    def codegen(context, builder, sig, args):
        return cast_match_obj_bool(context, builder, re_match_type, types.
            bool_, args[0])
    return types.bool_(match_typ), codegen


@overload(bool)
def overload_bool_re_match(val):
    if val == re_match_type:
        return lambda val: match_obj_is_none(val)


@lower_builtin(operator.is_, ReMatchType, types.NoneType)
def lower_match_is_none(context, builder, sig, args):
    hvfp__ujb = args[0]
    return builder.not_(cast_match_obj_bool(context, builder, sig.args[0],
        sig.args[1], hvfp__ujb))


gen_objmode_func_overload(re.search, 're_match_type')
gen_objmode_func_overload(re.match, 're_match_type')
gen_objmode_func_overload(re.fullmatch, 're_match_type')
gen_objmode_func_overload(re.split, 'list_str_type')
gen_objmode_func_overload(re.sub, 'unicode_type')
gen_objmode_func_overload(re.escape, 'unicode_type')


@overload(re.findall, no_unliteral=True)
def overload_re_findall(pattern, string, flags=0):

    def _re_findall_impl(pattern, string, flags=0):
        with numba.objmode(m='list_str_type'):
            m = re.findall(pattern, string, flags)
        return m
    return _re_findall_impl


@overload(re.subn, no_unliteral=True)
def overload_re_subn(pattern, repl, string, count=0, flags=0):

    def _re_subn_impl(pattern, repl, string, count=0, flags=0):
        with numba.objmode(m='unicode_type', s='int64'):
            m, s = re.subn(pattern, repl, string, count, flags)
        return m, s
    return _re_subn_impl


@overload(re.purge, no_unliteral=True)
def overload_re_purge():

    def _re_purge_impl():
        with numba.objmode():
            re.purge()
        return
    return _re_purge_impl


@intrinsic
def init_const_pattern(typingctx, pat, pat_const=None):
    fedj__yaax = get_overload_const_str(pat_const)

    def codegen(context, builder, sig, args):
        return impl_ret_borrowed(context, builder, sig.return_type, args[0])
    return RePatternType(fedj__yaax)(pat, pat_const), codegen


@overload(re.compile, no_unliteral=True)
def re_compile_overload(pattern, flags=0):
    if is_overload_constant_str(pattern):
        pat_const = get_overload_const_str(pattern)

        def _re_compile_const_impl(pattern, flags=0):
            with numba.objmode(pat='re_pattern_type'):
                pat = re.compile(pattern, flags)
            return init_const_pattern(pat, pat_const)
        return _re_compile_const_impl

    def _re_compile_impl(pattern, flags=0):
        with numba.objmode(pat='re_pattern_type'):
            pat = re.compile(pattern, flags)
        return pat
    return _re_compile_impl


gen_objmode_method_overload(RePatternType, 'search', re.Pattern.search,
    're_match_type')
gen_objmode_method_overload(RePatternType, 'match', re.Pattern.match,
    're_match_type')
gen_objmode_method_overload(RePatternType, 'fullmatch', re.Pattern.
    fullmatch, 're_match_type')
gen_objmode_method_overload(RePatternType, 'split', re.Pattern.split,
    'list_str_type')
gen_objmode_method_overload(RePatternType, 'sub', re.Pattern.sub,
    'unicode_type')


@overload_method(RePatternType, 'findall', no_unliteral=True)
def overload_pat_findall(p, string, pos=0, endpos=9223372036854775807):
    if p.pat_const:
        zwe__emt = re.compile(p.pat_const).groups
        typ = types.List(string_type)
        if zwe__emt > 1:
            typ = types.List(types.Tuple([string_type] * zwe__emt))
        ditlt__ilql = 'list_tup_str_{}'.format(numba.core.ir_utils.next_label()
            )
        setattr(types, ditlt__ilql, typ)
        eojw__bzk = (
            """
def _pat_findall_const_impl(
    p, string, pos=0, endpos=9223372036854775807
):  # pragma: no cover
    with numba.objmode(m="{}"):
        m = p.findall(string, pos, endpos)
    return m
"""
            .format(ditlt__ilql))
        kzu__aulr = {}
        exec(eojw__bzk, globals(), kzu__aulr)
        zalw__qku = kzu__aulr['_pat_findall_const_impl']
        return zalw__qku

    def _pat_findall_impl(p, string, pos=0, endpos=9223372036854775807):
        with numba.objmode(m='list_str_type'):
            m = p.findall(string, pos, endpos)
        if p.groups > 1:
            raise ValueError(
                "pattern string should be constant for 'findall' with multiple groups"
                )
        return m
    return _pat_findall_impl


@overload_method(RePatternType, 'subn', no_unliteral=True)
def re_subn_overload(p, repl, string, count=0):

    def _re_subn_impl(p, repl, string, count=0):
        with numba.objmode(out='unicode_type', s='int64'):
            out, s = p.subn(repl, string, count)
        return out, s
    return _re_subn_impl


@overload_attribute(RePatternType, 'flags')
def overload_pattern_flags(p):

    def _pat_flags_impl(p):
        with numba.objmode(flags='int64'):
            flags = p.flags
        return flags
    return _pat_flags_impl


@overload_attribute(RePatternType, 'groups')
def overload_pattern_groups(p):

    def _pat_groups_impl(p):
        with numba.objmode(groups='int64'):
            groups = p.groups
        return groups
    return _pat_groups_impl


@overload_attribute(RePatternType, 'groupindex')
def overload_pattern_groupindex(p):
    types.dict_string_int = types.DictType(string_type, types.int64)

    def _pat_groupindex_impl(p):
        with numba.objmode(d='dict_string_int'):
            ins__uayy = dict(p.groupindex)
            d = numba.typed.Dict.empty(key_type=numba.core.types.
                unicode_type, value_type=numba.int64)
            d.update(ins__uayy)
        return d
    return _pat_groupindex_impl


@overload_attribute(RePatternType, 'pattern')
def overload_pattern_pattern(p):

    def _pat_pattern_impl(p):
        with numba.objmode(pattern='unicode_type'):
            pattern = p.pattern
        return pattern
    return _pat_pattern_impl


gen_objmode_method_overload(ReMatchType, 'expand', re.Match.expand,
    'unicode_type')


@overload_method(ReMatchType, 'group', no_unliteral=True)
def overload_match_group(m, *args):
    if len(args) == 1 and isinstance(args[0], (types.StarArgTuple, types.
        StarArgUniTuple)):
        args = args[0].types
    if len(args) == 0:

        def _match_group_impl_zero(m, *args):
            with numba.objmode(out='unicode_type'):
                out = m.group()
            return out
        return _match_group_impl_zero
    if len(args) == 1:

        def _match_group_impl_one(m, *args):
            axn__awgra = args[0]
            with numba.objmode(out='unicode_type'):
                out = m.group(axn__awgra)
            return out
        return _match_group_impl_one
    rsd__ilpx = 'tuple_str_{}'.format(len(args))
    setattr(types, rsd__ilpx, types.Tuple([string_type] * len(args)))
    zac__cknr = ', '.join('group{}'.format(xzb__rxlgf + 1) for xzb__rxlgf in
        range(len(args)))
    eojw__bzk = 'def _match_group_impl(m, *args):\n'
    eojw__bzk += '  ({}) = args\n'.format(zac__cknr)
    eojw__bzk += "  with numba.objmode(out='{}'):\n".format(rsd__ilpx)
    eojw__bzk += '    out = m.group({})\n'.format(zac__cknr)
    eojw__bzk += '  return out\n'
    kzu__aulr = {}
    exec(eojw__bzk, globals(), kzu__aulr)
    zalw__qku = kzu__aulr['_match_group_impl']
    return zalw__qku


@overload(operator.getitem, no_unliteral=True)
def overload_match_getitem(m, ind):
    if m == re_match_type:
        return lambda m, ind: m.group(ind)


@overload_method(ReMatchType, 'groups', no_unliteral=True)
def overload_match_groups(m, default=None):

    def _match_groups_impl(m, default=None):
        with numba.objmode(out='list_str_type'):
            out = list(m.groups(default))
        return out
    return _match_groups_impl


@overload_method(ReMatchType, 'groupdict', no_unliteral=True)
def overload_match_groupdict(m, default=None):
    types.dict_string_string = types.DictType(string_type, string_type)

    def _match_groupdict_impl(m, default=None):
        with numba.objmode(d='dict_string_string'):
            out = m.groupdict(default)
            d = numba.typed.Dict.empty(key_type=numba.core.types.
                unicode_type, value_type=numba.core.types.unicode_type)
            d.update(out)
        return d
    return _match_groupdict_impl


gen_objmode_method_overload(ReMatchType, 'start', re.Match.start, 'int64')
gen_objmode_method_overload(ReMatchType, 'end', re.Match.end, 'int64')


@overload_method(ReMatchType, 'span', no_unliteral=True)
def overload_match_span(m, group=0):
    types.tuple_int64_2 = types.Tuple([types.int64, types.int64])

    def _match_span_impl(m, group=0):
        with numba.objmode(out='tuple_int64_2'):
            out = m.span(group)
        return out
    return _match_span_impl


@overload_attribute(ReMatchType, 'pos')
def overload_match_pos(p):

    def _match_pos_impl(p):
        with numba.objmode(pos='int64'):
            pos = p.pos
        return pos
    return _match_pos_impl


@overload_attribute(ReMatchType, 'endpos')
def overload_match_endpos(p):

    def _match_endpos_impl(p):
        with numba.objmode(endpos='int64'):
            endpos = p.endpos
        return endpos
    return _match_endpos_impl


@overload_attribute(ReMatchType, 'lastindex')
def overload_match_lastindex(p):

    def _match_lastindex_impl(p):
        with numba.objmode(lastindex='int64'):
            lastindex = p.lastindex
        return lastindex
    return _match_lastindex_impl


@overload_attribute(ReMatchType, 'lastgroup')
def overload_match_lastgroup(p):

    def _match_lastgroup_impl(p):
        with numba.objmode(lastgroup='unicode_type'):
            lastgroup = p.lastgroup
        return lastgroup
    return _match_lastgroup_impl


@overload_attribute(ReMatchType, 're')
def overload_match_re(m):

    def _match_re_impl(m):
        with numba.objmode(m_re='re_pattern_type'):
            m_re = m.re
        return m_re
    return _match_re_impl


@overload_attribute(ReMatchType, 'string')
def overload_match_string(m):

    def _match_string_impl(m):
        with numba.objmode(out='unicode_type'):
            out = m.string
        return out
    return _match_string_impl
