"""
Support for Series.str methods
"""
import operator
import re
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_index_ext import StringIndexType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.split_impl import get_split_view_data_ptr, get_split_view_index, string_array_split_view_type
from bodo.libs.array import get_search_regex
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.str_arr_ext import get_utf8_size, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import str_findall_count
from bodo.utils.typing import BodoError, create_unsupported_overload, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_const_str_len, is_list_like_index_type, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_list, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true, raise_bodo_error


class SeriesStrMethodType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        hdxp__nqho = 'SeriesStrMethodType({})'.format(stype)
        super(SeriesStrMethodType, self).__init__(hdxp__nqho)


@register_model(SeriesStrMethodType)
class SeriesStrModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        exiee__zjcgu = [('obj', fe_type.stype)]
        super(SeriesStrModel, self).__init__(dmm, fe_type, exiee__zjcgu)


make_attribute_wrapper(SeriesStrMethodType, 'obj', '_obj')


@intrinsic
def init_series_str_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        talwq__ziqr, = args
        czn__myzb = signature.return_type
        cte__kykc = cgutils.create_struct_proxy(czn__myzb)(context, builder)
        cte__kykc.obj = talwq__ziqr
        context.nrt.incref(builder, signature.args[0], talwq__ziqr)
        return cte__kykc._getvalue()
    return SeriesStrMethodType(obj)(obj), codegen


def str_arg_check(func_name, arg_name, arg):
    if not isinstance(arg, types.UnicodeType) and not is_overload_constant_str(
        arg):
        raise_bodo_error(
            "Series.str.{}(): parameter '{}' expected a string object, not {}"
            .format(func_name, arg_name, arg))


def int_arg_check(func_name, arg_name, arg):
    if not isinstance(arg, types.Integer) and not is_overload_constant_int(arg
        ):
        raise BodoError(
            "Series.str.{}(): parameter '{}' expected an int object, not {}"
            .format(func_name, arg_name, arg))


def not_supported_arg_check(func_name, arg_name, arg, defval):
    if arg_name == 'na':
        if not isinstance(arg, types.Omitted) and (not isinstance(arg,
            float) or not np.isnan(arg)):
            raise BodoError(
                "Series.str.{}(): parameter '{}' is not supported, default: np.nan"
                .format(func_name, arg_name))
    elif not isinstance(arg, types.Omitted) and arg != defval:
        raise BodoError(
            "Series.str.{}(): parameter '{}' is not supported, default: {}"
            .format(func_name, arg_name, defval))


def common_validate_padding(func_name, width, fillchar):
    if is_overload_constant_str(fillchar):
        if get_overload_const_str_len(fillchar) != 1:
            raise BodoError(
                'Series.str.{}(): fillchar must be a character, not str'.
                format(func_name))
    elif not isinstance(fillchar, types.UnicodeType):
        raise BodoError('Series.str.{}(): fillchar must be a character, not {}'
            .format(func_name, fillchar))
    int_arg_check(func_name, 'width', width)


@overload_attribute(SeriesType, 'str')
def overload_series_str(S):
    if not isinstance(S, SeriesType) or not (S.data in (string_array_type,
        string_array_split_view_type) or isinstance(S.data, ArrayItemArrayType)
        ):
        raise_bodo_error(
            'Series.str: input should be a series of string or arrays')
    return lambda S: bodo.hiframes.series_str_impl.init_series_str_method(S)


@overload_method(SeriesStrMethodType, 'len', inline='always', no_unliteral=True
    )
def overload_str_method_len(S_str):

    def impl(S_str):
        S = S_str._obj
        hrz__vbpt = bodo.hiframes.pd_series_ext.get_series_data(S)
        kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
        hdxp__nqho = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(hrz__vbpt)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)
        for i in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(hrz__vbpt, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = len(hrz__vbpt[i])
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kjm__fhkkx,
            hdxp__nqho)
    return impl


@overload_method(SeriesStrMethodType, 'split', inline='always',
    no_unliteral=True)
def overload_str_method_split(S_str, pat=None, n=-1, expand=False):
    if not is_overload_none(pat):
        str_arg_check('split', 'pat', pat)
    int_arg_check('split', 'n', n)
    not_supported_arg_check('split', 'expand', expand, False)
    if is_overload_constant_str(pat) and len(get_overload_const_str(pat)
        ) == 1 and get_overload_const_str(pat).isascii(
        ) and is_overload_constant_int(n) and get_overload_const_int(n) == -1:

        def _str_split_view_impl(S_str, pat=None, n=-1, expand=False):
            S = S_str._obj
            hrz__vbpt = bodo.hiframes.pd_series_ext.get_series_data(S)
            kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
            hdxp__nqho = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.hiframes.split_impl.compute_split_view(hrz__vbpt,
                pat)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                kjm__fhkkx, hdxp__nqho)
        return _str_split_view_impl

    def _str_split_impl(S_str, pat=None, n=-1, expand=False):
        S = S_str._obj
        hrz__vbpt = bodo.hiframes.pd_series_ext.get_series_data(S)
        kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
        hdxp__nqho = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.str_ext.str_split(hrz__vbpt, pat, n)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kjm__fhkkx,
            hdxp__nqho)
    return _str_split_impl


@overload_method(SeriesStrMethodType, 'get', no_unliteral=True)
def overload_str_method_get(S_str, i):
    gppbi__wnaiu = S_str.stype.data
    if (gppbi__wnaiu != string_array_split_view_type and gppbi__wnaiu !=
        string_array_type) and not isinstance(gppbi__wnaiu, ArrayItemArrayType
        ):
        raise_bodo_error(
            'Series.str.get(): only supports input type of Series(array(item)) and Series(str)'
            )
    int_arg_check('get', 'i', i)
    if isinstance(gppbi__wnaiu, ArrayItemArrayType):

        def _str_get_array_impl(S_str, i):
            S = S_str._obj
            hrz__vbpt = bodo.hiframes.pd_series_ext.get_series_data(S)
            kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
            hdxp__nqho = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.array_kernels.get(hrz__vbpt, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                kjm__fhkkx, hdxp__nqho)
        return _str_get_array_impl
    if gppbi__wnaiu == string_array_split_view_type:

        def _str_get_split_impl(S_str, i):
            S = S_str._obj
            hrz__vbpt = bodo.hiframes.pd_series_ext.get_series_data(S)
            kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
            hdxp__nqho = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            n = len(hrz__vbpt)
            vzfbx__twbkx = 0
            for bqyp__evu in numba.parfors.parfor.internal_prange(n):
                jyqh__qws, jyqh__qws, docsn__abov = get_split_view_index(
                    hrz__vbpt, bqyp__evu, i)
                vzfbx__twbkx += docsn__abov
            numba.parfors.parfor.init_prange()
            out_arr = pre_alloc_string_array(n, vzfbx__twbkx)
            for hauj__pkeb in numba.parfors.parfor.internal_prange(n):
                afgk__gtlqe, efcqz__vvq, docsn__abov = get_split_view_index(
                    hrz__vbpt, hauj__pkeb, i)
                if afgk__gtlqe == 0:
                    bodo.libs.array_kernels.setna(out_arr, hauj__pkeb)
                    iwsro__pkxft = get_split_view_data_ptr(hrz__vbpt, 0)
                else:
                    bodo.libs.str_arr_ext.str_arr_set_not_na(out_arr,
                        hauj__pkeb)
                    iwsro__pkxft = get_split_view_data_ptr(hrz__vbpt,
                        efcqz__vvq)
                bodo.libs.str_arr_ext.setitem_str_arr_ptr(out_arr,
                    hauj__pkeb, iwsro__pkxft, docsn__abov)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                kjm__fhkkx, hdxp__nqho)
        return _str_get_split_impl

    def _str_get_impl(S_str, i):
        S = S_str._obj
        hrz__vbpt = bodo.hiframes.pd_series_ext.get_series_data(S)
        kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
        hdxp__nqho = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(hrz__vbpt)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(n, -1)
        for hauj__pkeb in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(hrz__vbpt, hauj__pkeb) or not len(
                hrz__vbpt[hauj__pkeb]) > i >= -len(hrz__vbpt[hauj__pkeb]):
                out_arr[hauj__pkeb] = ''
                bodo.libs.array_kernels.setna(out_arr, hauj__pkeb)
            else:
                out_arr[hauj__pkeb] = hrz__vbpt[hauj__pkeb][i]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kjm__fhkkx,
            hdxp__nqho)
    return _str_get_impl


@overload_method(SeriesStrMethodType, 'join', inline='always', no_unliteral
    =True)
def overload_str_method_join(S_str, sep):
    gppbi__wnaiu = S_str.stype.data
    if (gppbi__wnaiu != string_array_split_view_type and gppbi__wnaiu !=
        ArrayItemArrayType(string_array_type) and gppbi__wnaiu !=
        string_array_type):
        raise_bodo_error(
            'Series.str.join(): only supports input type of Series(list(str)) and Series(str)'
            )
    str_arg_check('join', 'sep', sep)

    def impl(S_str, sep):
        S = S_str._obj
        mkjig__dxo = bodo.hiframes.pd_series_ext.get_series_data(S)
        hdxp__nqho = bodo.hiframes.pd_series_ext.get_series_name(S)
        kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        n = len(mkjig__dxo)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
        for hauj__pkeb in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(mkjig__dxo, hauj__pkeb):
                out_arr[hauj__pkeb] = ''
                bodo.libs.array_kernels.setna(out_arr, hauj__pkeb)
            else:
                secen__cgbug = mkjig__dxo[hauj__pkeb]
                out_arr[hauj__pkeb] = sep.join(secen__cgbug)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kjm__fhkkx,
            hdxp__nqho)
    return impl


@overload_method(SeriesStrMethodType, 'replace', inline='always',
    no_unliteral=True)
def overload_str_method_replace(S_str, pat, repl, n=-1, case=None, flags=0,
    regex=True):
    not_supported_arg_check('replace', 'n', n, -1)
    not_supported_arg_check('replace', 'case', case, None)
    str_arg_check('replace', 'pat', pat)
    str_arg_check('replace', 'repl', repl)
    int_arg_check('replace', 'flags', flags)
    if is_overload_true(regex):

        def _str_replace_regex_impl(S_str, pat, repl, n=-1, case=None,
            flags=0, regex=True):
            S = S_str._obj
            hrz__vbpt = bodo.hiframes.pd_series_ext.get_series_data(S)
            kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
            hdxp__nqho = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            nyb__ldsl = re.compile(pat, flags)
            hnvsl__kmk = len(hrz__vbpt)
            out_arr = pre_alloc_string_array(hnvsl__kmk, -1)
            for hauj__pkeb in numba.parfors.parfor.internal_prange(hnvsl__kmk):
                if bodo.libs.array_kernels.isna(hrz__vbpt, hauj__pkeb):
                    out_arr[hauj__pkeb] = ''
                    bodo.libs.array_kernels.setna(out_arr, hauj__pkeb)
                    continue
                out_arr[hauj__pkeb] = nyb__ldsl.sub(repl, hrz__vbpt[hauj__pkeb]
                    )
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                kjm__fhkkx, hdxp__nqho)
        return _str_replace_regex_impl
    if not is_overload_false(regex):
        raise BodoError('Series.str.replace(): regex argument should be bool')

    def _str_replace_noregex_impl(S_str, pat, repl, n=-1, case=None, flags=
        0, regex=True):
        S = S_str._obj
        hrz__vbpt = bodo.hiframes.pd_series_ext.get_series_data(S)
        kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
        hdxp__nqho = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        hnvsl__kmk = len(hrz__vbpt)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(hnvsl__kmk, -1)
        for hauj__pkeb in numba.parfors.parfor.internal_prange(hnvsl__kmk):
            if bodo.libs.array_kernels.isna(hrz__vbpt, hauj__pkeb):
                out_arr[hauj__pkeb] = ''
                bodo.libs.array_kernels.setna(out_arr, hauj__pkeb)
                continue
            out_arr[hauj__pkeb] = hrz__vbpt[hauj__pkeb].replace(pat, repl)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kjm__fhkkx,
            hdxp__nqho)
    return _str_replace_noregex_impl


@numba.njit
def series_contains_regex(S, pat, case, flags, na, regex):
    with numba.objmode(out_arr=bodo.boolean_array):
        out_arr = S.array._str_contains(pat, case, flags, na, regex)
    return out_arr


def is_regex_unsupported(pat):
    cbls__xcs = ['(?a', '(?i', '(?L', '(?m', '(?s', '(?u', '(?x', '(?#']
    if is_overload_constant_str(pat):
        if isinstance(pat, types.StringLiteral):
            pat = pat.literal_value
        return any([(tzlac__neyq in pat) for tzlac__neyq in cbls__xcs])
    else:
        return True


@overload_method(SeriesStrMethodType, 'contains', no_unliteral=True)
def overload_str_method_contains(S_str, pat, case=True, flags=0, na=np.nan,
    regex=True):
    not_supported_arg_check('contains', 'na', na, np.nan)
    str_arg_check('contains', 'pat', pat)
    int_arg_check('contains', 'flags', flags)
    if not is_overload_constant_bool(regex):
        raise BodoError(
            "Series.str.contains(): 'regex' argument should be a constant boolean"
            )
    if not is_overload_constant_bool(case):
        raise BodoError(
            "Series.str.contains(): 'case' argument should be a constant boolean"
            )
    reje__itik = re.IGNORECASE.value
    oge__ssxwl = 'def impl(\n'
    oge__ssxwl += '    S_str, pat, case=True, flags=0, na=np.nan, regex=True\n'
    oge__ssxwl += '):\n'
    oge__ssxwl += '  S = S_str._obj\n'
    oge__ssxwl += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    oge__ssxwl += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    oge__ssxwl += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    oge__ssxwl += '  l = len(arr)\n'
    oge__ssxwl += '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    if is_overload_true(regex):
        if is_regex_unsupported(pat) or flags:
            oge__ssxwl += """  out_arr = bodo.hiframes.series_str_impl.series_contains_regex(S, pat, case, flags, na, regex)
"""
        else:
            oge__ssxwl += """  get_search_regex(arr, case, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    else:
        oge__ssxwl += '  numba.parfors.parfor.init_prange()\n'
        if is_overload_false(case):
            oge__ssxwl += '  upper_pat = pat.upper()\n'
        oge__ssxwl += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        oge__ssxwl += '      if bodo.libs.array_kernels.isna(arr, i):\n'
        oge__ssxwl += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        oge__ssxwl += '      else: \n'
        if is_overload_true(case):
            oge__ssxwl += '          out_arr[i] = pat in arr[i]\n'
        else:
            oge__ssxwl += (
                '          out_arr[i] = upper_pat in arr[i].upper()\n')
    oge__ssxwl += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    yvy__lecfw = {}
    exec(oge__ssxwl, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': reje__itik, 'get_search_regex':
        get_search_regex}, yvy__lecfw)
    impl = yvy__lecfw['impl']
    return impl


@overload_method(SeriesStrMethodType, 'count', inline='always',
    no_unliteral=True)
def overload_str_method_count(S_str, pat, flags=0):
    str_arg_check('count', 'pat', pat)
    int_arg_check('count', 'flags', flags)

    def impl(S_str, pat, flags=0):
        S = S_str._obj
        mkjig__dxo = bodo.hiframes.pd_series_ext.get_series_data(S)
        hdxp__nqho = bodo.hiframes.pd_series_ext.get_series_name(S)
        kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
        nyb__ldsl = re.compile(pat, flags)
        numba.parfors.parfor.init_prange()
        hnvsl__kmk = len(mkjig__dxo)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(hnvsl__kmk, np.int64)
        for i in numba.parfors.parfor.internal_prange(hnvsl__kmk):
            if bodo.libs.array_kernels.isna(mkjig__dxo, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = str_findall_count(nyb__ldsl, mkjig__dxo[i])
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kjm__fhkkx,
            hdxp__nqho)
    return impl


@overload_method(SeriesStrMethodType, 'find', inline='always', no_unliteral
    =True)
def overload_str_method_find(S_str, sub, start=0, end=None):
    str_arg_check('find', 'sub', sub)
    int_arg_check('find', 'start', start)
    if not is_overload_none(end):
        int_arg_check('find', 'end', end)

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        mkjig__dxo = bodo.hiframes.pd_series_ext.get_series_data(S)
        hdxp__nqho = bodo.hiframes.pd_series_ext.get_series_name(S)
        kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        hnvsl__kmk = len(mkjig__dxo)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(hnvsl__kmk, np.int64)
        for i in numba.parfors.parfor.internal_prange(hnvsl__kmk):
            if bodo.libs.array_kernels.isna(mkjig__dxo, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = mkjig__dxo[i].find(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kjm__fhkkx,
            hdxp__nqho)
    return impl


@overload_method(SeriesStrMethodType, 'rfind', inline='always',
    no_unliteral=True)
def overload_str_method_rfind(S_str, sub, start=0, end=None):
    str_arg_check('rfind', 'sub', sub)
    if start != 0:
        int_arg_check('rfind', 'start', start)
    if not is_overload_none(end):
        int_arg_check('rfind', 'end', end)

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        mkjig__dxo = bodo.hiframes.pd_series_ext.get_series_data(S)
        hdxp__nqho = bodo.hiframes.pd_series_ext.get_series_name(S)
        kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        hnvsl__kmk = len(mkjig__dxo)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(hnvsl__kmk, np.int64)
        for i in numba.parfors.parfor.internal_prange(hnvsl__kmk):
            if bodo.libs.array_kernels.isna(mkjig__dxo, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = mkjig__dxo[i].rfind(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kjm__fhkkx,
            hdxp__nqho)
    return impl


@overload_method(SeriesStrMethodType, 'center', inline='always',
    no_unliteral=True)
def overload_str_method_center(S_str, width, fillchar=' '):
    common_validate_padding('center', width, fillchar)

    def impl(S_str, width, fillchar=' '):
        S = S_str._obj
        mkjig__dxo = bodo.hiframes.pd_series_ext.get_series_data(S)
        hdxp__nqho = bodo.hiframes.pd_series_ext.get_series_name(S)
        kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        hnvsl__kmk = len(mkjig__dxo)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(hnvsl__kmk, -1)
        for hauj__pkeb in numba.parfors.parfor.internal_prange(hnvsl__kmk):
            if bodo.libs.array_kernels.isna(mkjig__dxo, hauj__pkeb):
                out_arr[hauj__pkeb] = ''
                bodo.libs.array_kernels.setna(out_arr, hauj__pkeb)
            else:
                out_arr[hauj__pkeb] = mkjig__dxo[hauj__pkeb].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kjm__fhkkx,
            hdxp__nqho)
    return impl


@overload_method(SeriesStrMethodType, 'slice_replace', inline='always',
    no_unliteral=True)
def overload_str_method_slice_replace(S_str, start=0, stop=None, repl=''):
    int_arg_check('slice_replace', 'start', start)
    if not is_overload_none(stop):
        int_arg_check('slice_replace', 'stop', stop)
    str_arg_check('slice_replace', 'repl', repl)

    def impl(S_str, start=0, stop=None, repl=''):
        S = S_str._obj
        mkjig__dxo = bodo.hiframes.pd_series_ext.get_series_data(S)
        hdxp__nqho = bodo.hiframes.pd_series_ext.get_series_name(S)
        kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        hnvsl__kmk = len(mkjig__dxo)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(hnvsl__kmk, -1)
        for hauj__pkeb in numba.parfors.parfor.internal_prange(hnvsl__kmk):
            if bodo.libs.array_kernels.isna(mkjig__dxo, hauj__pkeb):
                bodo.libs.array_kernels.setna(out_arr, hauj__pkeb)
            else:
                if stop is not None:
                    mrpj__fxtik = mkjig__dxo[hauj__pkeb][stop:]
                else:
                    mrpj__fxtik = ''
                out_arr[hauj__pkeb] = mkjig__dxo[hauj__pkeb][:start
                    ] + repl + mrpj__fxtik
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kjm__fhkkx,
            hdxp__nqho)
    return impl


@overload_method(SeriesStrMethodType, 'repeat', inline='always',
    no_unliteral=True)
def overload_str_method_repeat(S_str, repeats):
    if isinstance(repeats, types.Integer) or is_overload_constant_int(repeats):

        def impl(S_str, repeats):
            S = S_str._obj
            mkjig__dxo = bodo.hiframes.pd_series_ext.get_series_data(S)
            hdxp__nqho = bodo.hiframes.pd_series_ext.get_series_name(S)
            kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
            numba.parfors.parfor.init_prange()
            hnvsl__kmk = len(mkjig__dxo)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(hnvsl__kmk,
                -1)
            for hauj__pkeb in numba.parfors.parfor.internal_prange(hnvsl__kmk):
                if bodo.libs.array_kernels.isna(mkjig__dxo, hauj__pkeb):
                    bodo.libs.array_kernels.setna(out_arr, hauj__pkeb)
                else:
                    out_arr[hauj__pkeb] = mkjig__dxo[hauj__pkeb] * repeats
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                kjm__fhkkx, hdxp__nqho)
        return impl
    elif is_overload_constant_list(repeats):
        hubl__mabm = get_overload_const_list(repeats)
        wlbkc__usrv = all([isinstance(zgg__eax, int) for zgg__eax in
            hubl__mabm])
    elif is_list_like_index_type(repeats) and isinstance(repeats.dtype,
        types.Integer):
        wlbkc__usrv = True
    else:
        wlbkc__usrv = False
    if wlbkc__usrv:

        def impl(S_str, repeats):
            S = S_str._obj
            mkjig__dxo = bodo.hiframes.pd_series_ext.get_series_data(S)
            hdxp__nqho = bodo.hiframes.pd_series_ext.get_series_name(S)
            kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
            uwb__lkzi = bodo.utils.conversion.coerce_to_array(repeats)
            numba.parfors.parfor.init_prange()
            hnvsl__kmk = len(mkjig__dxo)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(hnvsl__kmk,
                -1)
            for hauj__pkeb in numba.parfors.parfor.internal_prange(hnvsl__kmk):
                if bodo.libs.array_kernels.isna(mkjig__dxo, hauj__pkeb):
                    bodo.libs.array_kernels.setna(out_arr, hauj__pkeb)
                else:
                    out_arr[hauj__pkeb] = mkjig__dxo[hauj__pkeb] * uwb__lkzi[
                        hauj__pkeb]
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                kjm__fhkkx, hdxp__nqho)
        return impl
    else:
        raise BodoError(
            'Series.str.repeat(): repeats argument must either be an integer or a sequence of integers'
            )


@overload_method(SeriesStrMethodType, 'ljust', inline='always',
    no_unliteral=True)
def overload_str_method_ljust(S_str, width, fillchar=' '):
    common_validate_padding('ljust', width, fillchar)

    def impl(S_str, width, fillchar=' '):
        S = S_str._obj
        mkjig__dxo = bodo.hiframes.pd_series_ext.get_series_data(S)
        hdxp__nqho = bodo.hiframes.pd_series_ext.get_series_name(S)
        kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        hnvsl__kmk = len(mkjig__dxo)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(hnvsl__kmk, -1)
        for hauj__pkeb in numba.parfors.parfor.internal_prange(hnvsl__kmk):
            if bodo.libs.array_kernels.isna(mkjig__dxo, hauj__pkeb):
                out_arr[hauj__pkeb] = ''
                bodo.libs.array_kernels.setna(out_arr, hauj__pkeb)
            else:
                out_arr[hauj__pkeb] = mkjig__dxo[hauj__pkeb].ljust(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kjm__fhkkx,
            hdxp__nqho)
    return impl


@overload_method(SeriesStrMethodType, 'rjust', inline='always',
    no_unliteral=True)
def overload_str_method_rjust(S_str, width, fillchar=' '):
    common_validate_padding('rjust', width, fillchar)

    def impl(S_str, width, fillchar=' '):
        S = S_str._obj
        mkjig__dxo = bodo.hiframes.pd_series_ext.get_series_data(S)
        hdxp__nqho = bodo.hiframes.pd_series_ext.get_series_name(S)
        kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        hnvsl__kmk = len(mkjig__dxo)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(hnvsl__kmk, -1)
        for hauj__pkeb in numba.parfors.parfor.internal_prange(hnvsl__kmk):
            if bodo.libs.array_kernels.isna(mkjig__dxo, hauj__pkeb):
                out_arr[hauj__pkeb] = ''
                bodo.libs.array_kernels.setna(out_arr, hauj__pkeb)
            else:
                out_arr[hauj__pkeb] = mkjig__dxo[hauj__pkeb].rjust(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kjm__fhkkx,
            hdxp__nqho)
    return impl


@overload_method(SeriesStrMethodType, 'pad', no_unliteral=True)
def overload_str_method_pad(S_str, width, side='left', fillchar=' '):
    common_validate_padding('pad', width, fillchar)
    if is_overload_constant_str(side):
        if get_overload_const_str(side) not in ['left', 'right', 'both']:
            raise BodoError('Series.str.pad(): Invalid Side')
    else:
        raise BodoError('Series.str.pad(): Invalid Side')

    def impl(S_str, width, side='left', fillchar=' '):
        S = S_str._obj
        mkjig__dxo = bodo.hiframes.pd_series_ext.get_series_data(S)
        hdxp__nqho = bodo.hiframes.pd_series_ext.get_series_name(S)
        kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        hnvsl__kmk = len(mkjig__dxo)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(hnvsl__kmk, -1)
        for hauj__pkeb in numba.parfors.parfor.internal_prange(hnvsl__kmk):
            if bodo.libs.array_kernels.isna(mkjig__dxo, hauj__pkeb):
                out_arr[hauj__pkeb] = ''
                bodo.libs.array_kernels.setna(out_arr, hauj__pkeb)
            elif side == 'left':
                out_arr[hauj__pkeb] = mkjig__dxo[hauj__pkeb].rjust(width,
                    fillchar)
            elif side == 'right':
                out_arr[hauj__pkeb] = mkjig__dxo[hauj__pkeb].ljust(width,
                    fillchar)
            elif side == 'both':
                out_arr[hauj__pkeb] = mkjig__dxo[hauj__pkeb].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kjm__fhkkx,
            hdxp__nqho)
    return impl


@overload_method(SeriesStrMethodType, 'zfill', inline='always',
    no_unliteral=True)
def overload_str_method_zfill(S_str, width):
    int_arg_check('zfill', 'width', width)

    def impl(S_str, width):
        S = S_str._obj
        mkjig__dxo = bodo.hiframes.pd_series_ext.get_series_data(S)
        hdxp__nqho = bodo.hiframes.pd_series_ext.get_series_name(S)
        kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        hnvsl__kmk = len(mkjig__dxo)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(hnvsl__kmk, -1)
        for hauj__pkeb in numba.parfors.parfor.internal_prange(hnvsl__kmk):
            if bodo.libs.array_kernels.isna(mkjig__dxo, hauj__pkeb):
                out_arr[hauj__pkeb] = ''
                bodo.libs.array_kernels.setna(out_arr, hauj__pkeb)
            else:
                out_arr[hauj__pkeb] = mkjig__dxo[hauj__pkeb].zfill(width)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kjm__fhkkx,
            hdxp__nqho)
    return impl


@overload_method(SeriesStrMethodType, 'slice', no_unliteral=True)
def overload_str_method_slice(S_str, start=None, stop=None, step=None):
    if not is_overload_none(start):
        int_arg_check('slice', 'start', start)
    if not is_overload_none(stop):
        int_arg_check('slice', 'stop', stop)
    if not is_overload_none(step):
        int_arg_check('slice', 'step', step)

    def impl(S_str, start=None, stop=None, step=None):
        S = S_str._obj
        mkjig__dxo = bodo.hiframes.pd_series_ext.get_series_data(S)
        hdxp__nqho = bodo.hiframes.pd_series_ext.get_series_name(S)
        kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        hnvsl__kmk = len(mkjig__dxo)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(hnvsl__kmk, -1)
        for hauj__pkeb in numba.parfors.parfor.internal_prange(hnvsl__kmk):
            if bodo.libs.array_kernels.isna(mkjig__dxo, hauj__pkeb):
                out_arr[hauj__pkeb] = ''
                bodo.libs.array_kernels.setna(out_arr, hauj__pkeb)
            else:
                out_arr[hauj__pkeb] = mkjig__dxo[hauj__pkeb][start:stop:step]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kjm__fhkkx,
            hdxp__nqho)
    return impl


@overload_method(SeriesStrMethodType, 'startswith', inline='always',
    no_unliteral=True)
def overload_str_method_startswith(S_str, pat, na=np.nan):
    not_supported_arg_check('startswith', 'na', na, np.nan)
    str_arg_check('startswith', 'pat', pat)

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        mkjig__dxo = bodo.hiframes.pd_series_ext.get_series_data(S)
        hdxp__nqho = bodo.hiframes.pd_series_ext.get_series_name(S)
        kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        hnvsl__kmk = len(mkjig__dxo)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(hnvsl__kmk)
        for i in numba.parfors.parfor.internal_prange(hnvsl__kmk):
            if bodo.libs.array_kernels.isna(mkjig__dxo, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = mkjig__dxo[i].startswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kjm__fhkkx,
            hdxp__nqho)
    return impl


@overload_method(SeriesStrMethodType, 'endswith', inline='always',
    no_unliteral=True)
def overload_str_method_endswith(S_str, pat, na=np.nan):
    not_supported_arg_check('endswith', 'na', na, np.nan)
    str_arg_check('endswith', 'pat', pat)

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        mkjig__dxo = bodo.hiframes.pd_series_ext.get_series_data(S)
        hdxp__nqho = bodo.hiframes.pd_series_ext.get_series_name(S)
        kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        hnvsl__kmk = len(mkjig__dxo)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(hnvsl__kmk)
        for i in numba.parfors.parfor.internal_prange(hnvsl__kmk):
            if bodo.libs.array_kernels.isna(mkjig__dxo, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = mkjig__dxo[i].endswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, kjm__fhkkx,
            hdxp__nqho)
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_str_method_getitem(S_str, ind):
    if not isinstance(S_str, SeriesStrMethodType):
        return
    if not isinstance(types.unliteral(ind), (types.SliceType, types.Integer)):
        raise BodoError(
            'index input to Series.str[] should be a slice or an integer')
    if isinstance(ind, types.SliceType):
        return lambda S_str, ind: S_str.slice(ind.start, ind.stop, ind.step)
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda S_str, ind: S_str.get(ind)


@overload_method(SeriesStrMethodType, 'extract', inline='always',
    no_unliteral=True)
def overload_str_method_extract(S_str, pat, flags=0, expand=True):
    if not is_overload_constant_bool(expand):
        raise BodoError(
            "Series.str.extract(): 'expand' argument should be a constant bool"
            )
    kijcm__kyrfv, regex = _get_column_names_from_regex(pat, flags, 'extract')
    lcih__mhk = len(kijcm__kyrfv)
    oge__ssxwl = 'def impl(S_str, pat, flags=0, expand=True):\n'
    oge__ssxwl += '  regex = re.compile(pat, flags=flags)\n'
    oge__ssxwl += '  S = S_str._obj\n'
    oge__ssxwl += (
        '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    oge__ssxwl += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    oge__ssxwl += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    oge__ssxwl += '  numba.parfors.parfor.init_prange()\n'
    oge__ssxwl += '  n = len(str_arr)\n'
    for i in range(lcih__mhk):
        oge__ssxwl += (
            '  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)\n'
            .format(i))
    oge__ssxwl += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    oge__ssxwl += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
    for i in range(lcih__mhk):
        oge__ssxwl += "          out_arr_{}[j] = ''\n".format(i)
        oge__ssxwl += (
            '          bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
            format(i))
    oge__ssxwl += '      else:\n'
    oge__ssxwl += '          m = regex.search(str_arr[j])\n'
    oge__ssxwl += '          if m:\n'
    oge__ssxwl += '            g = m.groups()\n'
    for i in range(lcih__mhk):
        oge__ssxwl += '            out_arr_{0}[j] = g[{0}]\n'.format(i)
    oge__ssxwl += '          else:\n'
    for i in range(lcih__mhk):
        oge__ssxwl += "            out_arr_{}[j] = ''\n".format(i)
        oge__ssxwl += (
            '            bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
            format(i))
    if is_overload_false(expand) and regex.groups == 1:
        hdxp__nqho = "'{}'".format(list(regex.groupindex.keys()).pop()) if len(
            regex.groupindex.keys()) > 0 else 'name'
        oge__ssxwl += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr_0, index, {})\n'
            .format(hdxp__nqho))
        yvy__lecfw = {}
        exec(oge__ssxwl, {'re': re, 'bodo': bodo, 'numba': numba,
            'get_utf8_size': get_utf8_size}, yvy__lecfw)
        impl = yvy__lecfw['impl']
        return impl
    ejg__qye = ', '.join('out_arr_{}'.format(i) for i in range(lcih__mhk))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(oge__ssxwl,
        kijcm__kyrfv, ejg__qye, 'index', extra_globals={'get_utf8_size':
        get_utf8_size, 're': re})
    return impl


@overload_method(SeriesStrMethodType, 'extractall', inline='always',
    no_unliteral=True)
def overload_str_method_extractall(S_str, pat, flags=0, expand=True):
    kijcm__kyrfv, jyqh__qws = _get_column_names_from_regex(pat, flags,
        'extractall')
    lcih__mhk = len(kijcm__kyrfv)
    ofqv__fhrpx = isinstance(S_str.stype.index, StringIndexType)
    oge__ssxwl = 'def impl(S_str, pat, flags=0, expand=True):\n'
    oge__ssxwl += '  regex = re.compile(pat, flags=flags)\n'
    oge__ssxwl += '  S = S_str._obj\n'
    oge__ssxwl += (
        '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    oge__ssxwl += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    oge__ssxwl += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    oge__ssxwl += '  index_arr = bodo.utils.conversion.index_to_array(index)\n'
    oge__ssxwl += (
        '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n')
    oge__ssxwl += '  numba.parfors.parfor.init_prange()\n'
    oge__ssxwl += '  n = len(str_arr)\n'
    oge__ssxwl += '  out_n_l = [0]\n'
    for i in range(lcih__mhk):
        oge__ssxwl += '  num_chars_{} = 0\n'.format(i)
    if ofqv__fhrpx:
        oge__ssxwl += '  index_num_chars = 0\n'
    oge__ssxwl += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    if ofqv__fhrpx:
        oge__ssxwl += '      index_num_chars += get_utf8_size(index_arr[i])\n'
    oge__ssxwl += '      if bodo.libs.array_kernels.isna(str_arr, i):\n'
    oge__ssxwl += '          continue\n'
    oge__ssxwl += '      m = regex.findall(str_arr[i])\n'
    oge__ssxwl += '      out_n_l[0] += len(m)\n'
    for i in range(lcih__mhk):
        oge__ssxwl += '      l_{} = 0\n'.format(i)
    oge__ssxwl += '      for s in m:\n'
    for i in range(lcih__mhk):
        oge__ssxwl += '        l_{} += get_utf8_size(s{})\n'.format(i, 
            '[{}]'.format(i) if lcih__mhk > 1 else '')
    for i in range(lcih__mhk):
        oge__ssxwl += '      num_chars_{0} += l_{0}\n'.format(i)
    oge__ssxwl += (
        '  out_n = bodo.libs.distributed_api.local_alloc_size(out_n_l[0], str_arr)\n'
        )
    for i in range(lcih__mhk):
        oge__ssxwl += (
            """  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, num_chars_{0})
"""
            .format(i))
    if ofqv__fhrpx:
        oge__ssxwl += """  out_ind_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, index_num_chars)
"""
    else:
        oge__ssxwl += '  out_ind_arr = np.empty(out_n, index_arr.dtype)\n'
    oge__ssxwl += '  out_match_arr = np.empty(out_n, np.int64)\n'
    oge__ssxwl += '  out_ind = 0\n'
    oge__ssxwl += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    oge__ssxwl += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
    oge__ssxwl += '          continue\n'
    oge__ssxwl += '      m = regex.findall(str_arr[j])\n'
    oge__ssxwl += '      for k, s in enumerate(m):\n'
    for i in range(lcih__mhk):
        oge__ssxwl += (
            '        bodo.libs.distributed_api.set_arr_local(out_arr_{}, out_ind, s{})\n'
            .format(i, '[{}]'.format(i) if lcih__mhk > 1 else ''))
    oge__ssxwl += """        bodo.libs.distributed_api.set_arr_local(out_ind_arr, out_ind, index_arr[j])
"""
    oge__ssxwl += (
        '        bodo.libs.distributed_api.set_arr_local(out_match_arr, out_ind, k)\n'
        )
    oge__ssxwl += '        out_ind += 1\n'
    oge__ssxwl += (
        '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n')
    oge__ssxwl += "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n"
    ejg__qye = ', '.join('out_arr_{}'.format(i) for i in range(lcih__mhk))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(oge__ssxwl,
        kijcm__kyrfv, ejg__qye, 'out_index', extra_globals={'get_utf8_size':
        get_utf8_size, 're': re})
    return impl


def _get_column_names_from_regex(pat, flags, func_name):
    if not is_overload_constant_str(pat):
        raise BodoError(
            "Series.str.{}(): 'pat' argument should be a constant string".
            format(func_name))
    if not is_overload_constant_int(flags):
        raise BodoError(
            "Series.str.{}(): 'flags' argument should be a constant int".
            format(func_name))
    pat = get_overload_const_str(pat)
    flags = get_overload_const_int(flags)
    regex = re.compile(pat, flags=flags)
    if regex.groups == 0:
        raise BodoError(
            'Series.str.{}(): pattern {} contains no capture groups'.format
            (func_name, pat))
    eot__tev = dict(zip(regex.groupindex.values(), regex.groupindex.keys()))
    kijcm__kyrfv = [eot__tev.get(1 + i, i) for i in range(regex.groups)]
    return kijcm__kyrfv, regex


def create_str2str_methods_overload(func_name):
    if func_name in ['lstrip', 'rstrip', 'strip']:
        oge__ssxwl = 'def f(S_str, to_strip=None):\n'
    else:
        oge__ssxwl = 'def f(S_str):\n'
    oge__ssxwl += '    S = S_str._obj\n'
    oge__ssxwl += (
        '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    oge__ssxwl += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    oge__ssxwl += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    oge__ssxwl += '    numba.parfors.parfor.init_prange()\n'
    oge__ssxwl += '    n = len(str_arr)\n'
    if func_name in ('capitalize', 'lower', 'swapcase', 'title', 'upper'):
        oge__ssxwl += '    num_chars = num_total_chars(str_arr)\n'
    else:
        oge__ssxwl += '    num_chars = -1\n'
    oge__ssxwl += (
        '    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, num_chars)\n'
        )
    oge__ssxwl += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    oge__ssxwl += '        if bodo.libs.array_kernels.isna(str_arr, j):\n'
    oge__ssxwl += '            out_arr[j] = ""\n'
    oge__ssxwl += '            bodo.libs.array_kernels.setna(out_arr, j)\n'
    oge__ssxwl += '        else:\n'
    if func_name in ['lstrip', 'rstrip', 'strip']:
        oge__ssxwl += ('            out_arr[j] = str_arr[j].{}(to_strip)\n'
            .format(func_name))
    else:
        oge__ssxwl += '            out_arr[j] = str_arr[j].{}()\n'.format(
            func_name)
    oge__ssxwl += (
        '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    yvy__lecfw = {}
    exec(oge__ssxwl, {'bodo': bodo, 'numba': numba, 'num_total_chars': bodo
        .libs.str_arr_ext.num_total_chars, 'get_utf8_size': bodo.libs.
        str_arr_ext.get_utf8_size}, yvy__lecfw)
    apj__epuv = yvy__lecfw['f']
    if func_name in ['lstrip', 'rstrip', 'strip']:

        def overload_strip_method(S_str, to_strip=None):
            return apj__epuv
        return overload_strip_method
    else:

        def overload_str2str_methods(S_str):
            return apj__epuv
        return overload_str2str_methods


def create_str2bool_methods_overload(func_name):

    def overload_str2bool_methods(S_str):
        oge__ssxwl = 'def f(S_str):\n'
        oge__ssxwl += '    S = S_str._obj\n'
        oge__ssxwl += (
            '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        oge__ssxwl += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        oge__ssxwl += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        oge__ssxwl += '    numba.parfors.parfor.init_prange()\n'
        oge__ssxwl += '    l = len(str_arr)\n'
        oge__ssxwl += (
            '    out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n')
        oge__ssxwl += '    for i in numba.parfors.parfor.internal_prange(l):\n'
        oge__ssxwl += '        if bodo.libs.array_kernels.isna(str_arr, i):\n'
        oge__ssxwl += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
        oge__ssxwl += '        else:\n'
        oge__ssxwl += ('            out_arr[i] = np.bool_(str_arr[i].{}())\n'
            .format(func_name))
        oge__ssxwl += '    return bodo.hiframes.pd_series_ext.init_series(\n'
        oge__ssxwl += '      out_arr,index, name)\n'
        yvy__lecfw = {}
        exec(oge__ssxwl, {'bodo': bodo, 'numba': numba, 'np': np}, yvy__lecfw)
        apj__epuv = yvy__lecfw['f']
        return apj__epuv
    return overload_str2bool_methods


def _install_str2str_methods():
    for fpg__msvl in bodo.hiframes.pd_series_ext.str2str_methods:
        cwz__zzvj = create_str2str_methods_overload(fpg__msvl)
        overload_method(SeriesStrMethodType, fpg__msvl, inline='always',
            no_unliteral=True)(cwz__zzvj)


def _install_str2bool_methods():
    for fpg__msvl in bodo.hiframes.pd_series_ext.str2bool_methods:
        cwz__zzvj = create_str2bool_methods_overload(fpg__msvl)
        overload_method(SeriesStrMethodType, fpg__msvl, inline='always',
            no_unliteral=True)(cwz__zzvj)


_install_str2str_methods()
_install_str2bool_methods()


@overload_attribute(SeriesType, 'cat')
def overload_series_cat(s):
    if not isinstance(s.dtype, bodo.hiframes.pd_categorical_ext.
        PDCategoricalDtype):
        raise BodoError('Can only use .cat accessor with categorical values.')
    return lambda s: bodo.hiframes.series_str_impl.init_series_cat_method(s)


class SeriesCatMethodType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        hdxp__nqho = 'SeriesCatMethodType({})'.format(stype)
        super(SeriesCatMethodType, self).__init__(hdxp__nqho)


@register_model(SeriesCatMethodType)
class SeriesCatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        exiee__zjcgu = [('obj', fe_type.stype)]
        super(SeriesCatModel, self).__init__(dmm, fe_type, exiee__zjcgu)


make_attribute_wrapper(SeriesCatMethodType, 'obj', '_obj')


@intrinsic
def init_series_cat_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        talwq__ziqr, = args
        rtvbp__rlqjx = signature.return_type
        wmli__sdzkg = cgutils.create_struct_proxy(rtvbp__rlqjx)(context,
            builder)
        wmli__sdzkg.obj = talwq__ziqr
        context.nrt.incref(builder, signature.args[0], talwq__ziqr)
        return wmli__sdzkg._getvalue()
    return SeriesCatMethodType(obj)(obj), codegen


@overload_attribute(SeriesCatMethodType, 'codes')
def series_cat_codes_overload(S_dt):

    def impl(S_dt):
        S = S_dt._obj
        hrz__vbpt = bodo.hiframes.pd_series_ext.get_series_data(S)
        kjm__fhkkx = bodo.hiframes.pd_series_ext.get_series_index(S)
        hdxp__nqho = None
        return bodo.hiframes.pd_series_ext.init_series(bodo.hiframes.
            pd_categorical_ext.get_categorical_arr_codes(hrz__vbpt),
            kjm__fhkkx, hdxp__nqho)
    return impl


unsupported_str_methods = {'casefold', 'cat', 'decode', 'encode', 'findall',
    'fullmatch', 'get_dummies', 'index', 'match', 'normalize', 'partition',
    'repeat', 'rindex', 'rpartition', 'rsplit', 'slice_replace',
    'translate', 'wrap'}


def _install_strseries_unsupported():
    for lwc__flh in unsupported_str_methods:
        gni__bxdw = 'Series.str.' + lwc__flh
        overload_method(SeriesStrMethodType, lwc__flh)(
            create_unsupported_overload(gni__bxdw))


_install_strseries_unsupported()
