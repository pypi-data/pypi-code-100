import enum
import operator
import numba
import numpy as np
import pandas as pd
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.utils.typing import NOT_CONSTANT, BodoError, check_unsupported_args, dtype_to_array_type, get_literal_value, get_overload_const, get_overload_const_bool, is_common_scalar_dtype, is_iterable_type, is_list_like_index_type, is_literal_type, is_overload_constant_bool, is_overload_none, is_overload_true, is_scalar_type, raise_bodo_error


class PDCategoricalDtype(types.Opaque):

    def __init__(self, categories, elem_type, ordered, data=None, int_type=None
        ):
        self.categories = categories
        self.elem_type = elem_type
        self.ordered = ordered
        self.data = _get_cat_index_type(elem_type) if data is None else data
        self.int_type = int_type
        ftz__lws = (
            f'PDCategoricalDtype({self.categories}, {self.elem_type}, {self.ordered}, {self.data}, {self.int_type})'
            )
        super(PDCategoricalDtype, self).__init__(name=ftz__lws)


@typeof_impl.register(pd.CategoricalDtype)
def _typeof_pd_cat_dtype(val, c):
    kisng__xxwgg = val.categories.to_list()
    elem_type = None if len(kisng__xxwgg) == 0 else bodo.typeof(val.
        categories.values).dtype
    int_type = getattr(val, '_int_type', None)
    return PDCategoricalDtype(tuple(kisng__xxwgg), elem_type, val.ordered,
        bodo.typeof(val.categories), int_type)


def _get_cat_index_type(elem_type):
    elem_type = bodo.string_type if elem_type is None else elem_type
    return bodo.utils.typing.get_index_type_from_dtype(elem_type)


@lower_constant(PDCategoricalDtype)
def lower_constant_categorical_type(context, builder, typ, pyval):
    crkd__zdh = context.make_helper(builder, typ)
    crkd__zdh.categories = context.get_constant_generic(builder, bodo.
        typeof(pyval.categories), pyval.categories)
    crkd__zdh.ordered = context.get_constant(types.bool_, pyval.ordered)
    return crkd__zdh._getvalue()


@register_model(PDCategoricalDtype)
class PDCategoricalDtypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        vxdh__vzph = [('categories', fe_type.data), ('ordered', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, vxdh__vzph)


make_attribute_wrapper(PDCategoricalDtype, 'categories', 'categories')
make_attribute_wrapper(PDCategoricalDtype, 'ordered', 'ordered')


@intrinsic
def init_cat_dtype(typingctx, categories_typ, ordered_typ, int_type=None):
    assert bodo.hiframes.pd_index_ext.is_index_type(categories_typ)
    assert is_overload_constant_bool(ordered_typ)
    olf__pif = None if is_overload_none(int_type) else int_type.dtype

    def codegen(context, builder, sig, args):
        categories, ordered, yojzo__xepq = args
        cat_dtype = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        cat_dtype.categories = categories
        context.nrt.incref(builder, sig.args[0], categories)
        context.nrt.incref(builder, sig.args[1], ordered)
        cat_dtype.ordered = ordered
        return cat_dtype._getvalue()
    wiofy__gqx = PDCategoricalDtype(None, categories_typ.dtype,
        is_overload_true(ordered_typ), categories_typ, olf__pif)
    return wiofy__gqx(categories_typ, ordered_typ, int_type), codegen


@unbox(PDCategoricalDtype)
def unbox_cat_dtype(typ, obj, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    weguc__txgds = c.pyapi.object_getattr_string(obj, 'ordered')
    cat_dtype.ordered = c.pyapi.to_native_value(types.bool_, weguc__txgds
        ).value
    c.pyapi.decref(weguc__txgds)
    nfbc__ektkf = c.pyapi.object_getattr_string(obj, 'categories')
    cat_dtype.categories = c.pyapi.to_native_value(typ.data, nfbc__ektkf).value
    c.pyapi.decref(nfbc__ektkf)
    gluu__bbgms = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cat_dtype._getvalue(), is_error=gluu__bbgms)


@box(PDCategoricalDtype)
def box_cat_dtype(typ, val, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    weguc__txgds = c.pyapi.from_native_value(types.bool_, cat_dtype.ordered,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.data, cat_dtype.categories)
    mgp__eypz = c.pyapi.from_native_value(typ.data, cat_dtype.categories, c
        .env_manager)
    qzms__upthm = c.context.insert_const_string(c.builder.module, 'pandas')
    yvxx__uspbo = c.pyapi.import_module_noblock(qzms__upthm)
    iwu__lnlq = c.pyapi.call_method(yvxx__uspbo, 'CategoricalDtype', (
        mgp__eypz, weguc__txgds))
    c.pyapi.decref(weguc__txgds)
    c.pyapi.decref(mgp__eypz)
    c.pyapi.decref(yvxx__uspbo)
    c.context.nrt.decref(c.builder, typ, val)
    return iwu__lnlq


@overload_attribute(PDCategoricalDtype, 'nbytes')
def pd_categorical_nbytes_overload(A):
    return lambda A: A.categories.nbytes + bodo.io.np_io.get_dtype_size(types
        .bool_)


class CategoricalArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        self.dtype = dtype
        super(CategoricalArrayType, self).__init__(name=
            'CategoricalArrayType({})'.format(dtype))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return CategoricalArrayType(self.dtype)


@typeof_impl.register(pd.Categorical)
def _typeof_pd_cat(val, c):
    return CategoricalArrayType(bodo.typeof(val.dtype))


@register_model(CategoricalArrayType)
class CategoricalArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        krvqo__bcy = get_categories_int_type(fe_type.dtype)
        vxdh__vzph = [('dtype', fe_type.dtype), ('codes', types.Array(
            krvqo__bcy, 1, 'C'))]
        super(CategoricalArrayModel, self).__init__(dmm, fe_type, vxdh__vzph)


make_attribute_wrapper(CategoricalArrayType, 'codes', 'codes')
make_attribute_wrapper(CategoricalArrayType, 'dtype', 'dtype')


@unbox(CategoricalArrayType)
def unbox_categorical_array(typ, val, c):
    kouri__svk = c.pyapi.object_getattr_string(val, 'codes')
    dtype = get_categories_int_type(typ.dtype)
    codes = c.pyapi.to_native_value(types.Array(dtype, 1, 'C'), kouri__svk
        ).value
    c.pyapi.decref(kouri__svk)
    iwu__lnlq = c.pyapi.object_getattr_string(val, 'dtype')
    vuyk__orl = c.pyapi.to_native_value(typ.dtype, iwu__lnlq).value
    c.pyapi.decref(iwu__lnlq)
    jczc__pew = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    jczc__pew.codes = codes
    jczc__pew.dtype = vuyk__orl
    return NativeValue(jczc__pew._getvalue())


@lower_constant(CategoricalArrayType)
def lower_constant_categorical_array(context, builder, typ, pyval):
    snpf__mzmi = get_categories_int_type(typ.dtype)
    ding__anp = context.get_constant_generic(builder, types.Array(
        snpf__mzmi, 1, 'C'), pyval.codes)
    cat_dtype = context.get_constant_generic(builder, typ.dtype, pyval.dtype)
    jczc__pew = cgutils.create_struct_proxy(typ)(context, builder)
    jczc__pew.codes = ding__anp
    jczc__pew.dtype = cat_dtype
    return jczc__pew._getvalue()


def get_categories_int_type(cat_dtype):
    dtype = types.int64
    if cat_dtype.int_type is not None:
        return cat_dtype.int_type
    if cat_dtype.categories is None:
        return types.int64
    italp__pranc = len(cat_dtype.categories)
    if italp__pranc < np.iinfo(np.int8).max:
        dtype = types.int8
    elif italp__pranc < np.iinfo(np.int16).max:
        dtype = types.int16
    elif italp__pranc < np.iinfo(np.int32).max:
        dtype = types.int32
    return dtype


@box(CategoricalArrayType)
def box_categorical_array(typ, val, c):
    dtype = typ.dtype
    qzms__upthm = c.context.insert_const_string(c.builder.module, 'pandas')
    yvxx__uspbo = c.pyapi.import_module_noblock(qzms__upthm)
    krvqo__bcy = get_categories_int_type(dtype)
    xwpr__hcg = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    siua__qwwcu = types.Array(krvqo__bcy, 1, 'C')
    c.context.nrt.incref(c.builder, siua__qwwcu, xwpr__hcg.codes)
    kouri__svk = c.pyapi.from_native_value(siua__qwwcu, xwpr__hcg.codes, c.
        env_manager)
    c.context.nrt.incref(c.builder, dtype, xwpr__hcg.dtype)
    iwu__lnlq = c.pyapi.from_native_value(dtype, xwpr__hcg.dtype, c.env_manager
        )
    rwnfy__xrze = c.pyapi.borrow_none()
    ljbky__vjnyf = c.pyapi.object_getattr_string(yvxx__uspbo, 'Categorical')
    tud__mcbd = c.pyapi.call_method(ljbky__vjnyf, 'from_codes', (kouri__svk,
        rwnfy__xrze, rwnfy__xrze, iwu__lnlq))
    c.pyapi.decref(ljbky__vjnyf)
    c.pyapi.decref(kouri__svk)
    c.pyapi.decref(iwu__lnlq)
    c.pyapi.decref(yvxx__uspbo)
    c.context.nrt.decref(c.builder, typ, val)
    return tud__mcbd


def create_cmp_op_overload(op):

    def overload_cat_arr_cmp(A, other):
        if not isinstance(A, CategoricalArrayType):
            return
        if A.dtype.categories and is_literal_type(other) and types.unliteral(
            other) == A.dtype.elem_type:
            val = get_literal_value(other)
            ofxa__gmxex = list(A.dtype.categories).index(val
                ) if val in A.dtype.categories else -2

            def impl_lit(A, other):
                ddwfw__xwvyk = op(bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(A), ofxa__gmxex)
                return ddwfw__xwvyk
            return impl_lit

        def impl(A, other):
            ofxa__gmxex = get_code_for_value(A.dtype, other)
            ddwfw__xwvyk = op(bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A), ofxa__gmxex)
            return ddwfw__xwvyk
        return impl
    return overload_cat_arr_cmp


def _install_cmp_ops():
    for op in [operator.eq, operator.ne]:
        mkx__qbmq = create_cmp_op_overload(op)
        overload(op, inline='always', no_unliteral=True)(mkx__qbmq)


_install_cmp_ops()


@register_jitable
def get_code_for_value(cat_dtype, val):
    xwpr__hcg = cat_dtype.categories
    n = len(xwpr__hcg)
    for fhh__xtxds in range(n):
        if xwpr__hcg[fhh__xtxds] == val:
            return fhh__xtxds
    return -2


@overload_method(CategoricalArrayType, 'astype', inline='always',
    no_unliteral=True)
def overload_cat_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "CategoricalArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    ugn__hcssq = bodo.utils.typing.parse_dtype(dtype, 'CategoricalArray.astype'
        )
    if ugn__hcssq != A.dtype.elem_type:
        raise BodoError(
            f'Converting categorical array {A} to dtype {dtype} not supported yet'
            )
    siua__qwwcu = dtype_to_array_type(ugn__hcssq)

    def impl(A, dtype, copy=True):
        codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(A)
        categories = A.dtype.categories
        n = len(codes)
        ddwfw__xwvyk = bodo.utils.utils.alloc_type(n, siua__qwwcu, (-1,))
        for fhh__xtxds in numba.parfors.parfor.internal_prange(n):
            ptesh__vakr = codes[fhh__xtxds]
            if ptesh__vakr == -1:
                bodo.libs.array_kernels.setna(ddwfw__xwvyk, fhh__xtxds)
                continue
            ddwfw__xwvyk[fhh__xtxds
                ] = bodo.utils.conversion.unbox_if_timestamp(categories[
                ptesh__vakr])
        return ddwfw__xwvyk
    return impl


@overload(pd.api.types.CategoricalDtype, no_unliteral=True)
def cat_overload_dummy(val_list):
    return lambda val_list: 1


@intrinsic
def init_categorical_array(typingctx, codes, cat_dtype=None):
    assert isinstance(codes, types.Array) and isinstance(codes.dtype, types
        .Integer)

    def codegen(context, builder, signature, args):
        lwim__hywlk, vuyk__orl = args
        xwpr__hcg = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        xwpr__hcg.codes = lwim__hywlk
        xwpr__hcg.dtype = vuyk__orl
        context.nrt.incref(builder, signature.args[0], lwim__hywlk)
        context.nrt.incref(builder, signature.args[1], vuyk__orl)
        return xwpr__hcg._getvalue()
    odfuq__fjc = CategoricalArrayType(cat_dtype)
    sig = odfuq__fjc(codes, cat_dtype)
    return sig, codegen


def init_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    yfux__nbz = args[0]
    if equiv_set.has_shape(yfux__nbz):
        return ArrayAnalysis.AnalyzeResult(shape=yfux__nbz, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_init_categorical_array
    ) = init_categorical_array_equiv


def alloc_categorical_array(n, cat_dtype):
    pass


@overload(alloc_categorical_array, no_unliteral=True)
def _alloc_categorical_array(n, cat_dtype):
    krvqo__bcy = get_categories_int_type(cat_dtype)

    def impl(n, cat_dtype):
        codes = np.empty(n, krvqo__bcy)
        return init_categorical_array(codes, cat_dtype)
    return impl


def alloc_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_alloc_categorical_array
    ) = alloc_categorical_array_equiv


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_categorical_arr_codes(A):
    return lambda A: A.codes


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_categorical_array',
    'bodo.hiframes.pd_categorical_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_categorical_arr_codes',
    'bodo.hiframes.pd_categorical_ext'] = alias_ext_dummy_func


@overload_method(CategoricalArrayType, 'copy', no_unliteral=True)
def cat_arr_copy_overload(arr):
    return lambda arr: init_categorical_array(arr.codes.copy(), arr.dtype)


def build_replace_dicts(to_replace, value, categories):
    return dict(), np.empty(len(categories) + 1), 0


@overload(build_replace_dicts, no_unliteral=True)
def _build_replace_dicts(to_replace, value, categories):
    if isinstance(to_replace, types.Number) or to_replace == bodo.string_type:

        def impl(to_replace, value, categories):
            return build_replace_dicts([to_replace], value, categories)
        return impl
    else:

        def impl(to_replace, value, categories):
            n = len(categories)
            bpszi__ptjc = {}
            ding__anp = np.empty(n + 1, np.int64)
            zci__zybq = {}
            dtgl__vwy = []
            ppij__bdt = {}
            for fhh__xtxds in range(n):
                ppij__bdt[categories[fhh__xtxds]] = fhh__xtxds
            for okup__ddmco in to_replace:
                if okup__ddmco != value:
                    if okup__ddmco in ppij__bdt:
                        if value in ppij__bdt:
                            bpszi__ptjc[okup__ddmco] = okup__ddmco
                            mwsc__vfgk = ppij__bdt[okup__ddmco]
                            zci__zybq[mwsc__vfgk] = ppij__bdt[value]
                            dtgl__vwy.append(mwsc__vfgk)
                        else:
                            bpszi__ptjc[okup__ddmco] = value
                            ppij__bdt[value] = ppij__bdt[okup__ddmco]
            ydx__hleav = np.sort(np.array(dtgl__vwy))
            gght__obp = 0
            cpaon__wctbi = []
            for fppk__cerdw in range(-1, n):
                while gght__obp < len(ydx__hleav) and fppk__cerdw > ydx__hleav[
                    gght__obp]:
                    gght__obp += 1
                cpaon__wctbi.append(gght__obp)
            for pwy__myfp in range(-1, n):
                dbcap__egbqb = pwy__myfp
                if pwy__myfp in zci__zybq:
                    dbcap__egbqb = zci__zybq[pwy__myfp]
                ding__anp[pwy__myfp + 1] = dbcap__egbqb - cpaon__wctbi[
                    dbcap__egbqb + 1]
            return bpszi__ptjc, ding__anp, len(ydx__hleav)
        return impl


@numba.njit
def python_build_replace_dicts(to_replace, value, categories):
    return build_replace_dicts(to_replace, value, categories)


@register_jitable
def reassign_codes(new_codes_arr, old_codes_arr, codes_map_arr):
    for fhh__xtxds in range(len(new_codes_arr)):
        new_codes_arr[fhh__xtxds] = codes_map_arr[old_codes_arr[fhh__xtxds] + 1
            ]


@overload_method(CategoricalArrayType, 'replace', inline='always',
    no_unliteral=True)
def overload_replace(arr, to_replace, value):

    def impl(arr, to_replace, value):
        return bodo.hiframes.pd_categorical_ext.cat_replace(arr, to_replace,
            value)
    return impl


def cat_replace(arr, to_replace, value):
    return


@overload(cat_replace, no_unliteral=True)
def cat_replace_overload(arr, to_replace, value):
    xwhs__kwyqd = arr.dtype.ordered
    wafay__lsfd = arr.dtype.elem_type
    bin__azheq = get_overload_const(to_replace)
    ioz__nbkl = get_overload_const(value)
    if (arr.dtype.categories is not None and bin__azheq is not NOT_CONSTANT and
        ioz__nbkl is not NOT_CONSTANT):
        ust__gsih, codes_map_arr, yojzo__xepq = python_build_replace_dicts(
            bin__azheq, ioz__nbkl, arr.dtype.categories)
        if len(ust__gsih) == 0:
            return lambda arr, to_replace, value: arr.copy()
        ruwsd__ghqnx = []
        for javkw__hags in arr.dtype.categories:
            if javkw__hags in ust__gsih:
                rre__ceq = ust__gsih[javkw__hags]
                if rre__ceq != javkw__hags:
                    ruwsd__ghqnx.append(rre__ceq)
            else:
                ruwsd__ghqnx.append(javkw__hags)
        fxpv__tzm = pd.CategoricalDtype(ruwsd__ghqnx, xwhs__kwyqd)

        def impl_dtype(arr, to_replace, value):
            xwpr__hcg = alloc_categorical_array(len(arr.codes), fxpv__tzm)
            reassign_codes(xwpr__hcg.codes, arr.codes, codes_map_arr)
            return xwpr__hcg
        return impl_dtype
    wafay__lsfd = arr.dtype.elem_type
    if wafay__lsfd == types.unicode_type:

        def impl_str(arr, to_replace, value):
            categories = arr.dtype.categories
            bpszi__ptjc, codes_map_arr, knny__dnyq = build_replace_dicts(
                to_replace, value, categories.values)
            if len(bpszi__ptjc) == 0:
                return init_categorical_array(arr.codes.copy().astype(np.
                    int64), init_cat_dtype(categories.copy(), xwhs__kwyqd,
                    None))
            n = len(categories)
            emv__dges = bodo.libs.str_arr_ext.pre_alloc_string_array(n -
                knny__dnyq, -1)
            vvyj__jsvc = 0
            for fppk__cerdw in range(n):
                ncc__rsi = categories[fppk__cerdw]
                if ncc__rsi in bpszi__ptjc:
                    dsrot__eqdo = bpszi__ptjc[ncc__rsi]
                    if dsrot__eqdo != ncc__rsi:
                        emv__dges[vvyj__jsvc] = dsrot__eqdo
                        vvyj__jsvc += 1
                else:
                    emv__dges[vvyj__jsvc] = ncc__rsi
                    vvyj__jsvc += 1
            xwpr__hcg = alloc_categorical_array(len(arr.codes),
                init_cat_dtype(bodo.utils.conversion.index_from_array(
                emv__dges), xwhs__kwyqd, None))
            reassign_codes(xwpr__hcg.codes, arr.codes, codes_map_arr)
            return xwpr__hcg
        return impl_str
    qkzs__kldu = dtype_to_array_type(wafay__lsfd)

    def impl(arr, to_replace, value):
        categories = arr.dtype.categories
        bpszi__ptjc, codes_map_arr, knny__dnyq = build_replace_dicts(to_replace
            , value, categories.values)
        if len(bpszi__ptjc) == 0:
            return init_categorical_array(arr.codes.copy().astype(np.int64),
                init_cat_dtype(categories.copy(), xwhs__kwyqd, None))
        n = len(categories)
        emv__dges = bodo.utils.utils.alloc_type(n - knny__dnyq, qkzs__kldu,
            None)
        vvyj__jsvc = 0
        for fhh__xtxds in range(n):
            ncc__rsi = categories[fhh__xtxds]
            if ncc__rsi in bpszi__ptjc:
                dsrot__eqdo = bpszi__ptjc[ncc__rsi]
                if dsrot__eqdo != ncc__rsi:
                    emv__dges[vvyj__jsvc] = dsrot__eqdo
                    vvyj__jsvc += 1
            else:
                emv__dges[vvyj__jsvc] = ncc__rsi
                vvyj__jsvc += 1
        xwpr__hcg = alloc_categorical_array(len(arr.codes), init_cat_dtype(
            bodo.utils.conversion.index_from_array(emv__dges), xwhs__kwyqd,
            None))
        reassign_codes(xwpr__hcg.codes, arr.codes, codes_map_arr)
        return xwpr__hcg
    return impl


@overload(len, no_unliteral=True)
def overload_cat_arr_len(A):
    if isinstance(A, CategoricalArrayType):
        return lambda A: len(A.codes)


@overload_attribute(CategoricalArrayType, 'shape')
def overload_cat_arr_shape(A):
    return lambda A: (len(A.codes),)


@overload_attribute(CategoricalArrayType, 'ndim')
def overload_cat_arr_ndim(A):
    return lambda A: 1


@overload_attribute(CategoricalArrayType, 'nbytes')
def cat_arr_nbytes_overload(A):
    return lambda A: A.codes.nbytes + A.dtype.nbytes


@register_jitable
def get_label_dict_from_categories(vals):
    povz__sno = dict()
    gddmm__dvcwy = 0
    for fhh__xtxds in range(len(vals)):
        val = vals[fhh__xtxds]
        if val in povz__sno:
            continue
        povz__sno[val] = gddmm__dvcwy
        gddmm__dvcwy += 1
    return povz__sno


@overload(pd.Categorical, no_unliteral=True)
def pd_categorical_overload(values, categories=None, ordered=None, dtype=
    None, fastpath=False):
    lbau__gwsqj = dict(fastpath=fastpath)
    mhj__xgmw = dict(fastpath=False)
    check_unsupported_args('pd.Categorical', lbau__gwsqj, mhj__xgmw)
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):

        def impl_dtype(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, dtype)
        return impl_dtype
    if not is_overload_none(categories):
        hec__lvzg = get_overload_const(categories)
        if hec__lvzg is not NOT_CONSTANT and get_overload_const(ordered
            ) is not NOT_CONSTANT:
            if is_overload_none(ordered):
                wqwah__mcpg = False
            else:
                wqwah__mcpg = get_overload_const_bool(ordered)
            lea__dpw = pd.CategoricalDtype(hec__lvzg, wqwah__mcpg)

            def impl_cats_const(values, categories=None, ordered=None,
                dtype=None, fastpath=False):
                data = bodo.utils.conversion.coerce_to_array(values)
                return bodo.utils.conversion.fix_arr_dtype(data, lea__dpw)
            return impl_cats_const

        def impl_cats(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            ordered = bodo.utils.conversion.false_if_none(ordered)
            data = bodo.utils.conversion.coerce_to_array(values)
            kisng__xxwgg = bodo.utils.conversion.convert_to_index(categories)
            cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(
                kisng__xxwgg, ordered, None)
            return bodo.utils.conversion.fix_arr_dtype(data, cat_dtype)
        return impl_cats
    elif is_overload_none(ordered):

        def impl_auto(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, 'category')
        return impl_auto
    raise BodoError(
        f'pd.Categorical(): argument combination not supported yet: {values}, {categories}, {ordered}, {dtype}'
        )


@overload(operator.getitem, no_unliteral=True)
def categorical_array_getitem(arr, ind):
    if not isinstance(arr, CategoricalArrayType):
        return
    if isinstance(ind, types.Integer):

        def categorical_getitem_impl(arr, ind):
            gbrxl__fipf = arr.codes[ind]
            return arr.dtype.categories[max(gbrxl__fipf, 0)]
        return categorical_getitem_impl
    if is_list_like_index_type(ind) or isinstance(ind, types.SliceType):

        def impl_bool(arr, ind):
            return init_categorical_array(arr.codes[ind], arr.dtype)
        return impl_bool
    raise BodoError(
        f'getitem for CategoricalArrayType with indexing type {ind} not supported.'
        )


class CategoricalMatchingValues(enum.Enum):
    DIFFERENT_TYPES = -1
    DONT_MATCH = 0
    MAY_MATCH = 1
    DO_MATCH = 2


def categorical_arrs_match(arr1, arr2):
    if not (isinstance(arr1, CategoricalArrayType) and isinstance(arr2,
        CategoricalArrayType)):
        return CategoricalMatchingValues.DIFFERENT_TYPES
    if arr1.dtype.categories is None or arr2.dtype.categories is None:
        return CategoricalMatchingValues.MAY_MATCH
    return (CategoricalMatchingValues.DO_MATCH if arr1.dtype.categories ==
        arr2.dtype.categories and arr1.dtype.ordered == arr2.dtype.ordered else
        CategoricalMatchingValues.DONT_MATCH)


@register_jitable
def cat_dtype_equal(dtype1, dtype2):
    if dtype1.ordered != dtype2.ordered or len(dtype1.categories) != len(dtype2
        .categories):
        return False
    arr1 = dtype1.categories.values
    arr2 = dtype2.categories.values
    for fhh__xtxds in range(len(arr1)):
        if arr1[fhh__xtxds] != arr2[fhh__xtxds]:
            return False
    return True


@overload(operator.setitem, no_unliteral=True)
def categorical_array_setitem(arr, ind, val):
    if not isinstance(arr, CategoricalArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    mmhc__ghplr = is_scalar_type(val) and is_common_scalar_dtype([types.
        unliteral(val), arr.dtype.elem_type]) and not (isinstance(arr.dtype
        .elem_type, types.Integer) and isinstance(val, types.Float))
    sew__iejvx = not isinstance(val, CategoricalArrayType
        ) and is_iterable_type(val) and is_common_scalar_dtype([val.dtype,
        arr.dtype.elem_type]) and not (isinstance(arr.dtype.elem_type,
        types.Integer) and isinstance(val.dtype, types.Float))
    phsf__iqp = categorical_arrs_match(arr, val)
    jwdw__ubhu = (
        f"setitem for CategoricalArrayType of dtype {arr.dtype} with indexing type {ind} received an incorrect 'value' type {val}."
        )
    ujowh__vuf = (
        'Cannot set a Categorical with another, without identical categories')
    if isinstance(ind, types.Integer):
        if not mmhc__ghplr:
            raise BodoError(jwdw__ubhu)

        def impl_scalar(arr, ind, val):
            if val not in arr.dtype.categories:
                raise ValueError(
                    'Cannot setitem on a Categorical with a new category, set the categories first'
                    )
            gbrxl__fipf = arr.dtype.categories.get_loc(val)
            arr.codes[ind] = gbrxl__fipf
        return impl_scalar
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if not (mmhc__ghplr or sew__iejvx or phsf__iqp !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(jwdw__ubhu)
        if phsf__iqp == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(ujowh__vuf)
        if mmhc__ghplr:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                xbxdh__zlxy = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for fppk__cerdw in range(n):
                    arr.codes[ind[fppk__cerdw]] = xbxdh__zlxy
            return impl_scalar
        if phsf__iqp == CategoricalMatchingValues.DO_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                n = len(val.codes)
                for fhh__xtxds in range(n):
                    arr.codes[ind[fhh__xtxds]] = val.codes[fhh__xtxds]
            return impl_arr_ind_mask
        if phsf__iqp == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(ujowh__vuf)
                n = len(val.codes)
                for fhh__xtxds in range(n):
                    arr.codes[ind[fhh__xtxds]] = val.codes[fhh__xtxds]
            return impl_arr_ind_mask
        if sew__iejvx:

            def impl_arr_ind_mask_cat_values(arr, ind, val):
                n = len(val)
                categories = arr.dtype.categories
                for fppk__cerdw in range(n):
                    zemc__mmi = bodo.utils.conversion.unbox_if_timestamp(val
                        [fppk__cerdw])
                    if zemc__mmi not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    gbrxl__fipf = categories.get_loc(zemc__mmi)
                    arr.codes[ind[fppk__cerdw]] = gbrxl__fipf
            return impl_arr_ind_mask_cat_values
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if not (mmhc__ghplr or sew__iejvx or phsf__iqp !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(jwdw__ubhu)
        if phsf__iqp == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(ujowh__vuf)
        if mmhc__ghplr:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                xbxdh__zlxy = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for fppk__cerdw in range(n):
                    if ind[fppk__cerdw]:
                        arr.codes[fppk__cerdw] = xbxdh__zlxy
            return impl_scalar
        if phsf__iqp == CategoricalMatchingValues.DO_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                n = len(ind)
                jxyjb__dpk = 0
                for fhh__xtxds in range(n):
                    if ind[fhh__xtxds]:
                        arr.codes[fhh__xtxds] = val.codes[jxyjb__dpk]
                        jxyjb__dpk += 1
            return impl_bool_ind_mask
        if phsf__iqp == CategoricalMatchingValues.MAY_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(ujowh__vuf)
                n = len(ind)
                jxyjb__dpk = 0
                for fhh__xtxds in range(n):
                    if ind[fhh__xtxds]:
                        arr.codes[fhh__xtxds] = val.codes[jxyjb__dpk]
                        jxyjb__dpk += 1
            return impl_bool_ind_mask
        if sew__iejvx:

            def impl_bool_ind_mask_cat_values(arr, ind, val):
                n = len(ind)
                jxyjb__dpk = 0
                categories = arr.dtype.categories
                for fppk__cerdw in range(n):
                    if ind[fppk__cerdw]:
                        zemc__mmi = bodo.utils.conversion.unbox_if_timestamp(
                            val[jxyjb__dpk])
                        if zemc__mmi not in categories:
                            raise ValueError(
                                'Cannot setitem on a Categorical with a new category, set the categories first'
                                )
                        gbrxl__fipf = categories.get_loc(zemc__mmi)
                        arr.codes[fppk__cerdw] = gbrxl__fipf
                        jxyjb__dpk += 1
            return impl_bool_ind_mask_cat_values
    if isinstance(ind, types.SliceType):
        if not (mmhc__ghplr or sew__iejvx or phsf__iqp !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(jwdw__ubhu)
        if phsf__iqp == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(ujowh__vuf)
        if mmhc__ghplr:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                xbxdh__zlxy = arr.dtype.categories.get_loc(val)
                lrom__pwqc = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                for fppk__cerdw in range(lrom__pwqc.start, lrom__pwqc.stop,
                    lrom__pwqc.step):
                    arr.codes[fppk__cerdw] = xbxdh__zlxy
            return impl_scalar
        if phsf__iqp == CategoricalMatchingValues.DO_MATCH:

            def impl_arr(arr, ind, val):
                arr.codes[ind] = val.codes
            return impl_arr
        if phsf__iqp == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(ujowh__vuf)
                arr.codes[ind] = val.codes
            return impl_arr
        if sew__iejvx:

            def impl_slice_cat_values(arr, ind, val):
                categories = arr.dtype.categories
                lrom__pwqc = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                jxyjb__dpk = 0
                for fppk__cerdw in range(lrom__pwqc.start, lrom__pwqc.stop,
                    lrom__pwqc.step):
                    zemc__mmi = bodo.utils.conversion.unbox_if_timestamp(val
                        [jxyjb__dpk])
                    if zemc__mmi not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    gbrxl__fipf = categories.get_loc(zemc__mmi)
                    arr.codes[fppk__cerdw] = gbrxl__fipf
                    jxyjb__dpk += 1
            return impl_slice_cat_values
    raise BodoError(
        f'setitem for CategoricalArrayType with indexing type {ind} not supported.'
        )
