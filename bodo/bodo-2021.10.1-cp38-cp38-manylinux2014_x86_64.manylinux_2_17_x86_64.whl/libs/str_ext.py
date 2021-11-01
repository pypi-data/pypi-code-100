import operator
import re
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.typing.templates import AbstractTemplate, AttributeTemplate, bound_function, infer_getattr, infer_global, signature
from numba.extending import intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, register_jitable, register_model
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs import hstr_ext
from bodo.utils.typing import get_overload_const_int, get_overload_const_str, is_overload_constant_int, is_overload_constant_str


def unliteral_all(args):
    return tuple(types.unliteral(a) for a in args)


ll.add_symbol('del_str', hstr_ext.del_str)
ll.add_symbol('unicode_to_utf8', hstr_ext.unicode_to_utf8)
ll.add_symbol('memcmp', hstr_ext.memcmp)
ll.add_symbol('int_to_hex', hstr_ext.int_to_hex)
string_type = types.unicode_type


@numba.njit
def contains_regex(e, in_str):
    with numba.objmode(res='bool_'):
        res = bool(e.search(in_str))
    return res


@numba.generated_jit
def str_findall_count(regex, in_str):

    def _str_findall_count_impl(regex, in_str):
        with numba.objmode(res='int64'):
            res = len(regex.findall(in_str))
        return res
    return _str_findall_count_impl


utf8_str_type = types.ArrayCTypes(types.Array(types.uint8, 1, 'C'))


@intrinsic
def unicode_to_utf8_and_len(typingctx, str_typ=None):
    assert str_typ in (string_type, types.Optional(string_type)) or isinstance(
        str_typ, types.StringLiteral)
    tst__tan = types.Tuple([utf8_str_type, types.int64])

    def codegen(context, builder, sig, args):
        ylyg__kxxm, = args
        hxiqa__odpn = cgutils.create_struct_proxy(string_type)(context,
            builder, value=ylyg__kxxm)
        nbcgi__kdgeb = cgutils.create_struct_proxy(utf8_str_type)(context,
            builder)
        yag__sagvl = cgutils.create_struct_proxy(tst__tan)(context, builder)
        is_ascii = builder.icmp_unsigned('==', hxiqa__odpn.is_ascii, lir.
            Constant(hxiqa__odpn.is_ascii.type, 1))
        with builder.if_else(is_ascii) as (then, orelse):
            with then:
                context.nrt.incref(builder, string_type, ylyg__kxxm)
                nbcgi__kdgeb.data = hxiqa__odpn.data
                nbcgi__kdgeb.meminfo = hxiqa__odpn.meminfo
                yag__sagvl.f1 = hxiqa__odpn.length
            with orelse:
                fws__afo = lir.FunctionType(lir.IntType(64), [lir.IntType(8
                    ).as_pointer(), lir.IntType(8).as_pointer(), lir.
                    IntType(64), lir.IntType(32)])
                mbcz__rjzac = cgutils.get_or_insert_function(builder.module,
                    fws__afo, name='unicode_to_utf8')
                mdu__mdg = context.get_constant_null(types.voidptr)
                owgg__zkvw = builder.call(mbcz__rjzac, [mdu__mdg,
                    hxiqa__odpn.data, hxiqa__odpn.length, hxiqa__odpn.kind])
                yag__sagvl.f1 = owgg__zkvw
                oer__azsvv = builder.add(owgg__zkvw, lir.Constant(lir.
                    IntType(64), 1))
                nbcgi__kdgeb.meminfo = context.nrt.meminfo_alloc_aligned(
                    builder, size=oer__azsvv, align=32)
                nbcgi__kdgeb.data = context.nrt.meminfo_data(builder,
                    nbcgi__kdgeb.meminfo)
                builder.call(mbcz__rjzac, [nbcgi__kdgeb.data, hxiqa__odpn.
                    data, hxiqa__odpn.length, hxiqa__odpn.kind])
                builder.store(lir.Constant(lir.IntType(8), 0), builder.gep(
                    nbcgi__kdgeb.data, [owgg__zkvw]))
        yag__sagvl.f0 = nbcgi__kdgeb._getvalue()
        return yag__sagvl._getvalue()
    return tst__tan(string_type), codegen


def unicode_to_utf8(s):
    return s


@overload(unicode_to_utf8)
def overload_unicode_to_utf8(s):
    return lambda s: unicode_to_utf8_and_len(s)[0]


@overload(max)
def overload_builtin_max(lhs, rhs):
    if lhs == types.unicode_type and rhs == types.unicode_type:

        def impl(lhs, rhs):
            return lhs if lhs > rhs else rhs
        return impl


@overload(min)
def overload_builtin_min(lhs, rhs):
    if lhs == types.unicode_type and rhs == types.unicode_type:

        def impl(lhs, rhs):
            return lhs if lhs < rhs else rhs
        return impl


@intrinsic
def memcmp(typingctx, dest_t, src_t, count_t=None):

    def codegen(context, builder, sig, args):
        fws__afo = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
        eqee__rvf = cgutils.get_or_insert_function(builder.module, fws__afo,
            name='memcmp')
        return builder.call(eqee__rvf, args)
    return types.int32(types.voidptr, types.voidptr, types.intp), codegen


def int_to_str_len(n):
    return len(str(n))


@overload(int_to_str_len)
def overload_int_to_str_len(n):
    oeukt__alna = n(10)

    def impl(n):
        if n == 0:
            return 1
        jnuov__lzct = 0
        if n < 0:
            n = -n
            jnuov__lzct += 1
        while n > 0:
            n = n // oeukt__alna
            jnuov__lzct += 1
        return jnuov__lzct
    return impl


class StdStringType(types.Opaque):

    def __init__(self):
        super(StdStringType, self).__init__(name='StdStringType')


std_str_type = StdStringType()
register_model(StdStringType)(models.OpaqueModel)
del_str = types.ExternalFunction('del_str', types.void(std_str_type))
get_c_str = types.ExternalFunction('get_c_str', types.voidptr(std_str_type))
dummy_use = numba.njit(lambda a: None)


@overload(int)
def int_str_overload(in_str, base=10):
    if in_str == string_type:
        if is_overload_constant_int(base) and get_overload_const_int(base
            ) == 10:

            def _str_to_int_impl(in_str, base=10):
                val = _str_to_int64(in_str._data, in_str._length)
                dummy_use(in_str)
                return val
            return _str_to_int_impl

        def _str_to_int_base_impl(in_str, base=10):
            val = _str_to_int64_base(in_str._data, in_str._length, base)
            dummy_use(in_str)
            return val
        return _str_to_int_base_impl


@infer_global(float)
class StrToFloat(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        [tdwjx__kwata] = args
        if isinstance(tdwjx__kwata, StdStringType):
            return signature(types.float64, tdwjx__kwata)
        if tdwjx__kwata == string_type:
            return signature(types.float64, tdwjx__kwata)


ll.add_symbol('init_string_const', hstr_ext.init_string_const)
ll.add_symbol('get_c_str', hstr_ext.get_c_str)
ll.add_symbol('str_to_int64', hstr_ext.str_to_int64)
ll.add_symbol('str_to_uint64', hstr_ext.str_to_uint64)
ll.add_symbol('str_to_int64_base', hstr_ext.str_to_int64_base)
ll.add_symbol('str_to_float64', hstr_ext.str_to_float64)
ll.add_symbol('str_to_float32', hstr_ext.str_to_float32)
ll.add_symbol('get_str_len', hstr_ext.get_str_len)
ll.add_symbol('str_from_float32', hstr_ext.str_from_float32)
ll.add_symbol('str_from_float64', hstr_ext.str_from_float64)
get_std_str_len = types.ExternalFunction('get_str_len', signature(types.
    intp, std_str_type))
init_string_from_chars = types.ExternalFunction('init_string_const',
    std_str_type(types.voidptr, types.intp))
_str_to_int64 = types.ExternalFunction('str_to_int64', signature(types.
    int64, types.voidptr, types.int64))
_str_to_uint64 = types.ExternalFunction('str_to_uint64', signature(types.
    uint64, types.voidptr, types.int64))
_str_to_int64_base = types.ExternalFunction('str_to_int64_base', signature(
    types.int64, types.voidptr, types.int64, types.int64))


def gen_unicode_to_std_str(context, builder, unicode_val):
    hxiqa__odpn = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    fws__afo = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType(8
        ).as_pointer(), lir.IntType(64)])
    ltpvf__afb = cgutils.get_or_insert_function(builder.module, fws__afo,
        name='init_string_const')
    return builder.call(ltpvf__afb, [hxiqa__odpn.data, hxiqa__odpn.length])


def gen_std_str_to_unicode(context, builder, std_str_val, del_str=False):
    kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

    def _std_str_to_unicode(std_str):
        length = bodo.libs.str_ext.get_std_str_len(std_str)
        lubq__vjdai = numba.cpython.unicode._empty_string(kind, length, 1)
        bodo.libs.str_arr_ext._memcpy(lubq__vjdai._data, bodo.libs.str_ext.
            get_c_str(std_str), length, 1)
        if del_str:
            bodo.libs.str_ext.del_str(std_str)
        return lubq__vjdai
    val = context.compile_internal(builder, _std_str_to_unicode,
        string_type(bodo.libs.str_ext.std_str_type), [std_str_val])
    return val


def gen_get_unicode_chars(context, builder, unicode_val):
    hxiqa__odpn = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    return hxiqa__odpn.data


@intrinsic
def unicode_to_std_str(typingctx, unicode_t=None):

    def codegen(context, builder, sig, args):
        return gen_unicode_to_std_str(context, builder, args[0])
    return std_str_type(string_type), codegen


@intrinsic
def std_str_to_unicode(typingctx, unicode_t=None):

    def codegen(context, builder, sig, args):
        return gen_std_str_to_unicode(context, builder, args[0], True)
    return string_type(std_str_type), codegen


class RandomAccessStringArrayType(types.ArrayCompatible):

    def __init__(self):
        super(RandomAccessStringArrayType, self).__init__(name=
            'RandomAccessStringArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_type

    def copy(self):
        RandomAccessStringArrayType()


random_access_string_array = RandomAccessStringArrayType()


@register_model(RandomAccessStringArrayType)
class RandomAccessStringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        sitn__qxh = [('data', types.List(string_type))]
        models.StructModel.__init__(self, dmm, fe_type, sitn__qxh)


make_attribute_wrapper(RandomAccessStringArrayType, 'data', '_data')


@intrinsic
def alloc_random_access_string_array(typingctx, n_t=None):

    def codegen(context, builder, sig, args):
        uxgb__ccaog, = args
        dlp__sax = types.List(string_type)
        ppcl__mvo = numba.cpython.listobj.ListInstance.allocate(context,
            builder, dlp__sax, uxgb__ccaog)
        ppcl__mvo.size = uxgb__ccaog
        pmun__pkw = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        pmun__pkw.data = ppcl__mvo.value
        return pmun__pkw._getvalue()
    return random_access_string_array(types.intp), codegen


@overload(operator.getitem, no_unliteral=True)
def random_access_str_arr_getitem(A, ind):
    if A != random_access_string_array:
        return
    if isinstance(ind, types.Integer):
        return lambda A, ind: A._data[ind]


@overload(operator.setitem)
def random_access_str_arr_setitem(A, idx, val):
    if A != random_access_string_array:
        return
    if isinstance(idx, types.Integer):
        assert val == string_type

        def impl_scalar(A, idx, val):
            A._data[idx] = val
        return impl_scalar


@overload(len, no_unliteral=True)
def overload_str_arr_len(A):
    if A == random_access_string_array:
        return lambda A: len(A._data)


@overload_attribute(RandomAccessStringArrayType, 'shape')
def overload_str_arr_shape(A):
    return lambda A: (len(A._data),)


def alloc_random_access_str_arr_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_libs_str_ext_alloc_random_access_string_array
    ) = alloc_random_access_str_arr_equiv
str_from_float32 = types.ExternalFunction('str_from_float32', types.void(
    types.voidptr, types.float32))
str_from_float64 = types.ExternalFunction('str_from_float64', types.void(
    types.voidptr, types.float64))


def float_to_str(s, v):
    pass


@overload(float_to_str)
def float_to_str_overload(s, v):
    assert isinstance(v, types.Float)
    if v == types.float32:
        return lambda s, v: str_from_float32(s._data, v)
    return lambda s, v: str_from_float64(s._data, v)


@overload(str)
def float_str_overload(v):
    if isinstance(v, types.Float):
        kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(v):
            if v == 0:
                return '0.0'
            rcqtd__vjn = 0
            wjerx__tjkl = v
            if wjerx__tjkl < 0:
                rcqtd__vjn = 1
                wjerx__tjkl = -wjerx__tjkl
            if wjerx__tjkl < 1:
                yrvb__fymi = 1
            else:
                yrvb__fymi = 1 + int(np.floor(np.log10(wjerx__tjkl)))
            length = rcqtd__vjn + yrvb__fymi + 1 + 6
            s = numba.cpython.unicode._malloc_string(kind, 1, length, True)
            float_to_str(s, v)
            return s
        return impl


@overload(format, no_unliteral=True)
def overload_format(value, format_spec=''):
    if is_overload_constant_str(format_spec) and get_overload_const_str(
        format_spec) == '':

        def impl_fast(value, format_spec=''):
            return str(value)
        return impl_fast

    def impl(value, format_spec=''):
        with numba.objmode(res='string'):
            res = format(value, format_spec)
        return res
    return impl


@lower_cast(StdStringType, types.float64)
def cast_str_to_float64(context, builder, fromty, toty, val):
    fws__afo = lir.FunctionType(lir.DoubleType(), [lir.IntType(8).as_pointer()]
        )
    ltpvf__afb = cgutils.get_or_insert_function(builder.module, fws__afo,
        name='str_to_float64')
    return builder.call(ltpvf__afb, (val,))


@lower_cast(StdStringType, types.float32)
def cast_str_to_float32(context, builder, fromty, toty, val):
    fws__afo = lir.FunctionType(lir.FloatType(), [lir.IntType(8).as_pointer()])
    ltpvf__afb = cgutils.get_or_insert_function(builder.module, fws__afo,
        name='str_to_float32')
    return builder.call(ltpvf__afb, (val,))


@lower_cast(string_type, types.float64)
def cast_unicode_str_to_float64(context, builder, fromty, toty, val):
    std_str = gen_unicode_to_std_str(context, builder, val)
    return cast_str_to_float64(context, builder, std_str_type, toty, std_str)


@lower_cast(string_type, types.float32)
def cast_unicode_str_to_float32(context, builder, fromty, toty, val):
    std_str = gen_unicode_to_std_str(context, builder, val)
    return cast_str_to_float32(context, builder, std_str_type, toty, std_str)


@lower_cast(string_type, types.int64)
@lower_cast(string_type, types.int32)
@lower_cast(string_type, types.int16)
@lower_cast(string_type, types.int8)
def cast_unicode_str_to_int64(context, builder, fromty, toty, val):
    hxiqa__odpn = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    fws__afo = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(8)
        .as_pointer(), lir.IntType(64)])
    ltpvf__afb = cgutils.get_or_insert_function(builder.module, fws__afo,
        name='str_to_int64')
    return builder.call(ltpvf__afb, (hxiqa__odpn.data, hxiqa__odpn.length))


@lower_cast(string_type, types.uint64)
@lower_cast(string_type, types.uint32)
@lower_cast(string_type, types.uint16)
@lower_cast(string_type, types.uint8)
def cast_unicode_str_to_uint64(context, builder, fromty, toty, val):
    hxiqa__odpn = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    fws__afo = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(8)
        .as_pointer(), lir.IntType(64)])
    ltpvf__afb = cgutils.get_or_insert_function(builder.module, fws__afo,
        name='str_to_uint64')
    return builder.call(ltpvf__afb, (hxiqa__odpn.data, hxiqa__odpn.length))


@infer_getattr
class StringAttribute(AttributeTemplate):
    key = types.UnicodeType

    @bound_function('str.format', no_unliteral=True)
    def resolve_format(self, string_typ, args, kws):
        kws = dict(kws)
        amhrg__snzee = ', '.join('e{}'.format(nqa__vvkym) for nqa__vvkym in
            range(len(args)))
        if amhrg__snzee:
            amhrg__snzee += ', '
        fjg__qyi = ', '.join("{} = ''".format(a) for a in kws.keys())
        lvgwo__cnyki = f'def format_stub(string, {amhrg__snzee} {fjg__qyi}):\n'
        lvgwo__cnyki += '    pass\n'
        rhf__pddic = {}
        exec(lvgwo__cnyki, {}, rhf__pddic)
        ygaw__yvko = rhf__pddic['format_stub']
        txu__iikk = numba.core.utils.pysignature(ygaw__yvko)
        bnabu__vhioh = (string_typ,) + args + tuple(kws.values())
        return signature(string_typ, bnabu__vhioh).replace(pysig=txu__iikk)


@numba.njit(cache=True)
def str_split(arr, pat, n):
    iucc__bit = pat is not None and len(pat) > 1
    if iucc__bit:
        axd__crhbj = re.compile(pat)
        if n == -1:
            n = 0
    elif n == 0:
        n = -1
    ppcl__mvo = len(arr)
    kniyu__cxsuy = 0
    tdbgd__xkcx = 0
    for nqa__vvkym in numba.parfors.parfor.internal_prange(ppcl__mvo):
        if bodo.libs.array_kernels.isna(arr, nqa__vvkym):
            continue
        if iucc__bit:
            owupo__yaekr = axd__crhbj.split(arr[nqa__vvkym], maxsplit=n)
        elif pat == '':
            owupo__yaekr = [''] + list(arr[nqa__vvkym]) + ['']
        else:
            owupo__yaekr = arr[nqa__vvkym].split(pat, n)
        kniyu__cxsuy += len(owupo__yaekr)
        for s in owupo__yaekr:
            tdbgd__xkcx += bodo.libs.str_arr_ext.get_utf8_size(s)
    isb__cif = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        ppcl__mvo, (kniyu__cxsuy, tdbgd__xkcx), bodo.libs.str_arr_ext.
        string_array_type)
    zvre__ejy = bodo.libs.array_item_arr_ext.get_offsets(isb__cif)
    tqzvh__qwl = bodo.libs.array_item_arr_ext.get_null_bitmap(isb__cif)
    nct__xahjr = bodo.libs.array_item_arr_ext.get_data(isb__cif)
    wtsc__lhu = 0
    for vskx__vwz in numba.parfors.parfor.internal_prange(ppcl__mvo):
        zvre__ejy[vskx__vwz] = wtsc__lhu
        if bodo.libs.array_kernels.isna(arr, vskx__vwz):
            bodo.libs.int_arr_ext.set_bit_to_arr(tqzvh__qwl, vskx__vwz, 0)
            continue
        bodo.libs.int_arr_ext.set_bit_to_arr(tqzvh__qwl, vskx__vwz, 1)
        if iucc__bit:
            owupo__yaekr = axd__crhbj.split(arr[vskx__vwz], maxsplit=n)
        elif pat == '':
            owupo__yaekr = [''] + list(arr[vskx__vwz]) + ['']
        else:
            owupo__yaekr = arr[vskx__vwz].split(pat, n)
        fjd__bdbj = len(owupo__yaekr)
        for rhs__obzlq in range(fjd__bdbj):
            s = owupo__yaekr[rhs__obzlq]
            nct__xahjr[wtsc__lhu] = s
            wtsc__lhu += 1
    zvre__ejy[ppcl__mvo] = wtsc__lhu
    return isb__cif


@overload(hex)
def overload_hex(x):
    if isinstance(x, types.Integer):
        kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(x):
            x = np.int64(x)
            if x < 0:
                mkhl__aareg = '-0x'
                x = x * -1
            else:
                mkhl__aareg = '0x'
            x = np.uint64(x)
            if x == 0:
                cvu__chqpv = 1
            else:
                cvu__chqpv = fast_ceil_log2(x + 1)
                cvu__chqpv = (cvu__chqpv + 3) // 4
            length = len(mkhl__aareg) + cvu__chqpv
            output = numba.cpython.unicode._empty_string(kind, length, 1)
            bodo.libs.str_arr_ext._memcpy(output._data, mkhl__aareg._data,
                len(mkhl__aareg), 1)
            int_to_hex(output, cvu__chqpv, len(mkhl__aareg), x)
            return output
        return impl


@register_jitable
def fast_ceil_log2(x):
    kmgqj__bqbe = 0 if x & x - 1 == 0 else 1
    tyw__lrsso = [np.uint64(18446744069414584320), np.uint64(4294901760),
        np.uint64(65280), np.uint64(240), np.uint64(12), np.uint64(2)]
    eonfs__rzrzx = 32
    for nqa__vvkym in range(len(tyw__lrsso)):
        swbsk__siibm = 0 if x & tyw__lrsso[nqa__vvkym] == 0 else eonfs__rzrzx
        kmgqj__bqbe = kmgqj__bqbe + swbsk__siibm
        x = x >> swbsk__siibm
        eonfs__rzrzx = eonfs__rzrzx >> 1
    return kmgqj__bqbe


@intrinsic
def int_to_hex(typingctx, output, out_len, header_len, int_val):

    def codegen(context, builder, sig, args):
        output, out_len, header_len, int_val = args
        olgys__glr = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=output)
        fws__afo = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(64)])
        wmafv__nvq = cgutils.get_or_insert_function(builder.module,
            fws__afo, name='int_to_hex')
        hnik__olt = builder.inttoptr(builder.add(builder.ptrtoint(
            olgys__glr.data, lir.IntType(64)), header_len), lir.IntType(8).
            as_pointer())
        builder.call(wmafv__nvq, (hnik__olt, out_len, int_val))
    return types.void(output, out_len, header_len, int_val), codegen


def alloc_empty_bytes_or_string_data(typ, kind, length, is_ascii=0):
    pass


@overload(alloc_empty_bytes_or_string_data)
def overload_alloc_empty_bytes_or_string_data(typ, kind, length, is_ascii=0):
    typ = typ.instance_type if isinstance(typ, types.TypeRef) else typ
    if typ == bodo.bytes_type:
        return lambda typ, kind, length, is_ascii=0: np.empty(length, np.uint8)
    if typ == string_type:
        return (lambda typ, kind, length, is_ascii=0: numba.cpython.unicode
            ._empty_string(kind, length, is_ascii))
    raise BodoError(
        f'Internal Error: Expected Bytes or String type, found {typ}')


def get_unicode_or_numpy_data(val):
    pass


@overload(get_unicode_or_numpy_data)
def overload_get_unicode_or_numpy_data(val):
    if val == string_type:
        return lambda val: val._data
    if isinstance(val, types.Array):
        return lambda val: val.ctypes
    raise BodoError(
        f'Internal Error: Expected String or Numpy Array, found {val}')
