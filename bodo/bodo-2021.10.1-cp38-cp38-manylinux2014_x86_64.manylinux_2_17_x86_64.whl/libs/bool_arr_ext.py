"""Nullable boolean array that stores data in Numpy format (1 byte per value)
but nulls are stored in bit arrays (1 bit per value) similar to Arrow's nulls.
Pandas converts boolean array to object when NAs are introduced.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import NativeValue, box, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, type_callable, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs import hstr_ext
from bodo.libs.str_arr_ext import string_array_type
from bodo.utils.typing import is_list_like_index_type
ll.add_symbol('is_bool_array', hstr_ext.is_bool_array)
ll.add_symbol('is_pd_boolean_array', hstr_ext.is_pd_boolean_array)
ll.add_symbol('unbox_bool_array_obj', hstr_ext.unbox_bool_array_obj)
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, is_iterable_type, is_overload_false, is_overload_true, parse_dtype, raise_bodo_error


class BooleanArrayType(types.ArrayCompatible):

    def __init__(self):
        super(BooleanArrayType, self).__init__(name='BooleanArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return types.bool_

    def copy(self):
        return BooleanArrayType()


boolean_array = BooleanArrayType()


@typeof_impl.register(pd.arrays.BooleanArray)
def typeof_boolean_array(val, c):
    return boolean_array


data_type = types.Array(types.bool_, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(BooleanArrayType)
class BooleanArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        lbnqz__xfev = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, lbnqz__xfev)


make_attribute_wrapper(BooleanArrayType, 'data', '_data')
make_attribute_wrapper(BooleanArrayType, 'null_bitmap', '_null_bitmap')


class BooleanDtype(types.Number):

    def __init__(self):
        self.dtype = types.bool_
        super(BooleanDtype, self).__init__('BooleanDtype')


boolean_dtype = BooleanDtype()
register_model(BooleanDtype)(models.OpaqueModel)


@box(BooleanDtype)
def box_boolean_dtype(typ, val, c):
    hsq__fdd = c.context.insert_const_string(c.builder.module, 'pandas')
    hfp__wjx = c.pyapi.import_module_noblock(hsq__fdd)
    yugq__wxz = c.pyapi.call_method(hfp__wjx, 'BooleanDtype', ())
    c.pyapi.decref(hfp__wjx)
    return yugq__wxz


@unbox(BooleanDtype)
def unbox_boolean_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.BooleanDtype)(lambda a, b: boolean_dtype)
type_callable(pd.BooleanDtype)(lambda c: lambda : boolean_dtype)
lower_builtin(pd.BooleanDtype)(lambda c, b, s, a: c.get_dummy_value())


@numba.njit
def gen_full_bitmap(n):
    bry__zgov = n + 7 >> 3
    return np.full(bry__zgov, 255, np.uint8)


def call_func_in_unbox(func, args, arg_typs, c):
    gjj__clw = c.context.typing_context.resolve_value_type(func)
    eqbc__vyd = gjj__clw.get_call_type(c.context.typing_context, arg_typs, {})
    zfh__tbd = c.context.get_function(gjj__clw, eqbc__vyd)
    cgfc__zquy = c.context.call_conv.get_function_type(eqbc__vyd.
        return_type, eqbc__vyd.args)
    mxkbr__cppt = c.builder.module
    rfpl__nhyk = lir.Function(mxkbr__cppt, cgfc__zquy, name=mxkbr__cppt.
        get_unique_name('.func_conv'))
    rfpl__nhyk.linkage = 'internal'
    lsps__rss = lir.IRBuilder(rfpl__nhyk.append_basic_block())
    wjsa__gtftb = c.context.call_conv.decode_arguments(lsps__rss, eqbc__vyd
        .args, rfpl__nhyk)
    hot__gufwq = zfh__tbd(lsps__rss, wjsa__gtftb)
    c.context.call_conv.return_value(lsps__rss, hot__gufwq)
    iyyz__mywc, weemp__pstg = c.context.call_conv.call_function(c.builder,
        rfpl__nhyk, eqbc__vyd.return_type, eqbc__vyd.args, args)
    return weemp__pstg


@unbox(BooleanArrayType)
def unbox_bool_array(typ, obj, c):
    smhb__rru = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(smhb__rru)
    c.pyapi.decref(smhb__rru)
    cgfc__zquy = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    zbdjh__gidv = cgutils.get_or_insert_function(c.builder.module,
        cgfc__zquy, name='is_bool_array')
    cgfc__zquy = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    rfpl__nhyk = cgutils.get_or_insert_function(c.builder.module,
        cgfc__zquy, name='is_pd_boolean_array')
    udcx__nau = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ivjy__blsu = c.builder.call(rfpl__nhyk, [obj])
    yvcy__wgar = c.builder.icmp_unsigned('!=', ivjy__blsu, ivjy__blsu.type(0))
    with c.builder.if_else(yvcy__wgar) as (pd_then, pd_otherwise):
        with pd_then:
            frmv__nipcv = c.pyapi.object_getattr_string(obj, '_data')
            udcx__nau.data = c.pyapi.to_native_value(types.Array(types.
                bool_, 1, 'C'), frmv__nipcv).value
            blsqc__czek = c.pyapi.object_getattr_string(obj, '_mask')
            zyilz__qfx = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), blsqc__czek).value
            bry__zgov = c.builder.udiv(c.builder.add(n, lir.Constant(lir.
                IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
            xstyd__pgc = c.context.make_array(types.Array(types.bool_, 1, 'C')
                )(c.context, c.builder, zyilz__qfx)
            vwk__qpxqy = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(types.uint8, 1, 'C'), [bry__zgov])
            cgfc__zquy = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            rfpl__nhyk = cgutils.get_or_insert_function(c.builder.module,
                cgfc__zquy, name='mask_arr_to_bitmap')
            c.builder.call(rfpl__nhyk, [vwk__qpxqy.data, xstyd__pgc.data, n])
            udcx__nau.null_bitmap = vwk__qpxqy._getvalue()
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), zyilz__qfx)
            c.pyapi.decref(frmv__nipcv)
            c.pyapi.decref(blsqc__czek)
        with pd_otherwise:
            arpi__xvfk = c.builder.call(zbdjh__gidv, [obj])
            mov__ryez = c.builder.icmp_unsigned('!=', arpi__xvfk,
                arpi__xvfk.type(0))
            with c.builder.if_else(mov__ryez) as (then, otherwise):
                with then:
                    udcx__nau.data = c.pyapi.to_native_value(types.Array(
                        types.bool_, 1, 'C'), obj).value
                    udcx__nau.null_bitmap = call_func_in_unbox(gen_full_bitmap,
                        (n,), (types.int64,), c)
                with otherwise:
                    udcx__nau.data = bodo.utils.utils._empty_nd_impl(c.
                        context, c.builder, types.Array(types.bool_, 1, 'C'
                        ), [n])._getvalue()
                    bry__zgov = c.builder.udiv(c.builder.add(n, lir.
                        Constant(lir.IntType(64), 7)), lir.Constant(lir.
                        IntType(64), 8))
                    udcx__nau.null_bitmap = bodo.utils.utils._empty_nd_impl(c
                        .context, c.builder, types.Array(types.uint8, 1,
                        'C'), [bry__zgov])._getvalue()
                    vcig__htb = c.context.make_array(types.Array(types.
                        bool_, 1, 'C'))(c.context, c.builder, udcx__nau.data
                        ).data
                    ilisb__hygit = c.context.make_array(types.Array(types.
                        uint8, 1, 'C'))(c.context, c.builder, udcx__nau.
                        null_bitmap).data
                    cgfc__zquy = lir.FunctionType(lir.VoidType(), [lir.
                        IntType(8).as_pointer(), lir.IntType(8).as_pointer(
                        ), lir.IntType(8).as_pointer(), lir.IntType(64)])
                    rfpl__nhyk = cgutils.get_or_insert_function(c.builder.
                        module, cgfc__zquy, name='unbox_bool_array_obj')
                    c.builder.call(rfpl__nhyk, [obj, vcig__htb,
                        ilisb__hygit, n])
    return NativeValue(udcx__nau._getvalue())


@box(BooleanArrayType)
def box_bool_arr(typ, val, c):
    udcx__nau = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        udcx__nau.data, c.env_manager)
    jot__arf = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, udcx__nau.null_bitmap).data
    smhb__rru = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(smhb__rru)
    hsq__fdd = c.context.insert_const_string(c.builder.module, 'numpy')
    zhk__bxc = c.pyapi.import_module_noblock(hsq__fdd)
    ptp__rkpn = c.pyapi.object_getattr_string(zhk__bxc, 'bool_')
    zyilz__qfx = c.pyapi.call_method(zhk__bxc, 'empty', (smhb__rru, ptp__rkpn))
    zib__pcrln = c.pyapi.object_getattr_string(zyilz__qfx, 'ctypes')
    ntko__qwax = c.pyapi.object_getattr_string(zib__pcrln, 'data')
    dea__tds = c.builder.inttoptr(c.pyapi.long_as_longlong(ntko__qwax), lir
        .IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as loop:
        dkftq__yoivf = loop.index
        txe__xlv = c.builder.lshr(dkftq__yoivf, lir.Constant(lir.IntType(64
            ), 3))
        cgyfy__ord = c.builder.load(cgutils.gep(c.builder, jot__arf, txe__xlv))
        ynfa__ylwdv = c.builder.trunc(c.builder.and_(dkftq__yoivf, lir.
            Constant(lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(cgyfy__ord, ynfa__ylwdv), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        oqexu__pcth = cgutils.gep(c.builder, dea__tds, dkftq__yoivf)
        c.builder.store(val, oqexu__pcth)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        udcx__nau.null_bitmap)
    hsq__fdd = c.context.insert_const_string(c.builder.module, 'pandas')
    hfp__wjx = c.pyapi.import_module_noblock(hsq__fdd)
    tvph__muken = c.pyapi.object_getattr_string(hfp__wjx, 'arrays')
    yugq__wxz = c.pyapi.call_method(tvph__muken, 'BooleanArray', (data,
        zyilz__qfx))
    c.pyapi.decref(hfp__wjx)
    c.pyapi.decref(smhb__rru)
    c.pyapi.decref(zhk__bxc)
    c.pyapi.decref(ptp__rkpn)
    c.pyapi.decref(zib__pcrln)
    c.pyapi.decref(ntko__qwax)
    c.pyapi.decref(tvph__muken)
    c.pyapi.decref(data)
    c.pyapi.decref(zyilz__qfx)
    return yugq__wxz


@lower_constant(BooleanArrayType)
def lower_constant_bool_arr(context, builder, typ, pyval):
    n = len(pyval)
    eha__gsk = np.empty(n, np.bool_)
    xnl__azpxg = np.empty(n + 7 >> 3, np.uint8)
    for dkftq__yoivf, s in enumerate(pyval):
        ogyr__lwtym = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(xnl__azpxg, dkftq__yoivf, int(
            not ogyr__lwtym))
        if not ogyr__lwtym:
            eha__gsk[dkftq__yoivf] = s
    zajrj__mhfl = context.get_constant_generic(builder, data_type, eha__gsk)
    scz__garh = context.get_constant_generic(builder, nulls_type, xnl__azpxg)
    plsi__cxb = context.make_helper(builder, typ)
    plsi__cxb.data = zajrj__mhfl
    plsi__cxb.null_bitmap = scz__garh
    return plsi__cxb._getvalue()


def lower_init_bool_array(context, builder, signature, args):
    lzfhw__uzhbj, kvph__hjqg = args
    udcx__nau = cgutils.create_struct_proxy(signature.return_type)(context,
        builder)
    udcx__nau.data = lzfhw__uzhbj
    udcx__nau.null_bitmap = kvph__hjqg
    context.nrt.incref(builder, signature.args[0], lzfhw__uzhbj)
    context.nrt.incref(builder, signature.args[1], kvph__hjqg)
    return udcx__nau._getvalue()


@intrinsic
def init_bool_array(typingctx, data, null_bitmap=None):
    assert data == types.Array(types.bool_, 1, 'C')
    assert null_bitmap == types.Array(types.uint8, 1, 'C')
    sig = boolean_array(data, null_bitmap)
    return sig, lower_init_bool_array


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_bool_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_bool_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_bool_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    hyvqs__vhtb = args[0]
    if equiv_set.has_shape(hyvqs__vhtb):
        return ArrayAnalysis.AnalyzeResult(shape=hyvqs__vhtb, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_get_bool_arr_data = (
    get_bool_arr_data_equiv)


def init_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    hyvqs__vhtb = args[0]
    if equiv_set.has_shape(hyvqs__vhtb):
        return ArrayAnalysis.AnalyzeResult(shape=hyvqs__vhtb, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_init_bool_array = (
    init_bool_array_equiv)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


def alias_ext_init_bool_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_bool_array',
    'bodo.libs.bool_arr_ext'] = alias_ext_init_bool_array
numba.core.ir_utils.alias_func_extensions['get_bool_arr_data',
    'bodo.libs.bool_arr_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_bool_arr_bitmap',
    'bodo.libs.bool_arr_ext'] = alias_ext_dummy_func


@numba.njit(no_cpython_wrapper=True)
def alloc_bool_array(n):
    eha__gsk = np.empty(n, dtype=np.bool_)
    hwxa__mqxl = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_bool_array(eha__gsk, hwxa__mqxl)


def alloc_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_alloc_bool_array = (
    alloc_bool_array_equiv)


@overload(operator.getitem, no_unliteral=True)
def bool_arr_getitem(A, ind):
    if A != boolean_array:
        return
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda A, ind: A._data[ind]
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            supdl__vkp, idsc__gkbry = array_getitem_bool_index(A, ind)
            return init_bool_array(supdl__vkp, idsc__gkbry)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            supdl__vkp, idsc__gkbry = array_getitem_int_index(A, ind)
            return init_bool_array(supdl__vkp, idsc__gkbry)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            supdl__vkp, idsc__gkbry = array_getitem_slice_index(A, ind)
            return init_bool_array(supdl__vkp, idsc__gkbry)
        return impl_slice
    raise BodoError(
        f'getitem for BooleanArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def bool_arr_setitem(A, idx, val):
    if A != boolean_array:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    fpz__lwo = (
        f"setitem for BooleanArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == types.bool_:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(fpz__lwo)
    if not (is_iterable_type(val) and val.dtype == types.bool_ or types.
        unliteral(val) == types.bool_):
        raise BodoError(fpz__lwo)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, types.Integer):

        def impl_arr_ind_mask(A, idx, val):
            array_setitem_int_index(A, idx, val)
        return impl_arr_ind_mask
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:

        def impl_bool_ind_mask(A, idx, val):
            array_setitem_bool_index(A, idx, val)
        return impl_bool_ind_mask
    if isinstance(idx, types.SliceType):

        def impl_slice_mask(A, idx, val):
            array_setitem_slice_index(A, idx, val)
        return impl_slice_mask
    raise BodoError(
        f'setitem for BooleanArray with indexing type {idx} not supported.')


@overload(len, no_unliteral=True)
def overload_bool_arr_len(A):
    if A == boolean_array:
        return lambda A: len(A._data)


@overload_attribute(BooleanArrayType, 'shape')
def overload_bool_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(BooleanArrayType, 'dtype')
def overload_bool_arr_dtype(A):
    return lambda A: pd.BooleanDtype()


@overload_attribute(BooleanArrayType, 'ndim')
def overload_bool_arr_ndim(A):
    return lambda A: 1


@overload_attribute(BooleanArrayType, 'nbytes')
def bool_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


@overload_method(BooleanArrayType, 'copy', no_unliteral=True)
def overload_bool_arr_copy(A):
    return lambda A: bodo.libs.bool_arr_ext.init_bool_array(bodo.libs.
        bool_arr_ext.get_bool_arr_data(A).copy(), bodo.libs.bool_arr_ext.
        get_bool_arr_bitmap(A).copy())


@overload_method(BooleanArrayType, 'sum', no_unliteral=True, inline='always')
def overload_bool_sum(A):

    def impl(A):
        numba.parfors.parfor.init_prange()
        s = 0
        for dkftq__yoivf in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, dkftq__yoivf):
                val = A[dkftq__yoivf]
            s += val
        return s
    return impl


@overload_method(BooleanArrayType, 'astype', no_unliteral=True)
def overload_bool_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "BooleanArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if dtype == types.bool_:
        if is_overload_false(copy):
            return lambda A, dtype, copy=True: A
        elif is_overload_true(copy):
            return lambda A, dtype, copy=True: A.copy()
        else:

            def impl(A, dtype, copy=True):
                if copy:
                    return A.copy()
                else:
                    return A
            return impl
    nb_dtype = parse_dtype(dtype, 'BooleanArray.astype')
    if isinstance(nb_dtype, types.Float):

        def impl_float(A, dtype, copy=True):
            data = bodo.libs.bool_arr_ext.get_bool_arr_data(A)
            n = len(data)
            fju__tud = np.empty(n, nb_dtype)
            for dkftq__yoivf in numba.parfors.parfor.internal_prange(n):
                fju__tud[dkftq__yoivf] = data[dkftq__yoivf]
                if bodo.libs.array_kernels.isna(A, dkftq__yoivf):
                    fju__tud[dkftq__yoivf] = np.nan
            return fju__tud
        return impl_float
    return (lambda A, dtype, copy=True: bodo.libs.bool_arr_ext.
        get_bool_arr_data(A).astype(nb_dtype))


@overload(str, no_unliteral=True)
def overload_str_bool(val):
    if val == types.bool_:

        def impl(val):
            if val:
                return 'True'
            return 'False'
        return impl


ufunc_aliases = {'equal': 'eq', 'not_equal': 'ne', 'less': 'lt',
    'less_equal': 'le', 'greater': 'gt', 'greater_equal': 'ge'}


def create_op_overload(op, n_inputs):
    uaiol__faw = op.__name__
    uaiol__faw = ufunc_aliases.get(uaiol__faw, uaiol__faw)
    if n_inputs == 1:

        def overload_bool_arr_op_nin_1(A):
            if isinstance(A, BooleanArrayType):
                return bodo.libs.int_arr_ext.get_nullable_array_unary_impl(op,
                    A)
        return overload_bool_arr_op_nin_1
    elif n_inputs == 2:

        def overload_bool_arr_op_nin_2(lhs, rhs):
            if lhs == boolean_array or rhs == boolean_array:
                return bodo.libs.int_arr_ext.get_nullable_array_binary_impl(op,
                    lhs, rhs)
        return overload_bool_arr_op_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for vmag__xjdvd in numba.np.ufunc_db.get_ufuncs():
        fhhrw__ekqw = create_op_overload(vmag__xjdvd, vmag__xjdvd.nin)
        overload(vmag__xjdvd, no_unliteral=True)(fhhrw__ekqw)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod, operator.or_, operator.and_]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        fhhrw__ekqw = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(fhhrw__ekqw)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        fhhrw__ekqw = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(fhhrw__ekqw)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        fhhrw__ekqw = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(fhhrw__ekqw)


_install_unary_ops()


@overload_method(BooleanArrayType, 'unique', no_unliteral=True)
def overload_unique(A):

    def impl_bool_arr(A):
        data = []
        ynfa__ylwdv = []
        jmw__tzye = False
        lgbv__qsr = False
        gnt__lnye = False
        for dkftq__yoivf in range(len(A)):
            if bodo.libs.array_kernels.isna(A, dkftq__yoivf):
                if not jmw__tzye:
                    data.append(False)
                    ynfa__ylwdv.append(False)
                    jmw__tzye = True
                continue
            val = A[dkftq__yoivf]
            if val and not lgbv__qsr:
                data.append(True)
                ynfa__ylwdv.append(True)
                lgbv__qsr = True
            if not val and not gnt__lnye:
                data.append(False)
                ynfa__ylwdv.append(True)
                gnt__lnye = True
            if jmw__tzye and lgbv__qsr and gnt__lnye:
                break
        supdl__vkp = np.array(data)
        n = len(supdl__vkp)
        bry__zgov = 1
        idsc__gkbry = np.empty(bry__zgov, np.uint8)
        for ccdqu__uir in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(idsc__gkbry, ccdqu__uir,
                ynfa__ylwdv[ccdqu__uir])
        return init_bool_array(supdl__vkp, idsc__gkbry)
    return impl_bool_arr


@overload(operator.getitem, no_unliteral=True)
def bool_arr_ind_getitem(A, ind):
    if ind == boolean_array and (isinstance(A, (types.Array, bodo.libs.
        int_arr_ext.IntegerArrayType)) or isinstance(A, bodo.libs.
        struct_arr_ext.StructArrayType) or isinstance(A, bodo.libs.
        array_item_arr_ext.ArrayItemArrayType) or isinstance(A, bodo.libs.
        map_arr_ext.MapArrayType) or A in (string_array_type, bodo.hiframes
        .split_impl.string_array_split_view_type, boolean_array)):
        return lambda A, ind: A[ind._data]


@lower_cast(types.Array(types.bool_, 1, 'C'), boolean_array)
def cast_np_bool_arr_to_bool_arr(context, builder, fromty, toty, val):
    func = lambda A: bodo.libs.bool_arr_ext.init_bool_array(A, np.full(len(
        A) + 7 >> 3, 255, np.uint8))
    yugq__wxz = context.compile_internal(builder, func, toty(fromty), [val])
    return impl_ret_borrowed(context, builder, toty, yugq__wxz)


@overload(operator.setitem, no_unliteral=True)
def overload_np_array_setitem_bool_arr(A, idx, val):
    if isinstance(A, types.Array) and idx == boolean_array:

        def impl(A, idx, val):
            A[idx._data] = val
        return impl


def create_nullable_logical_op_overload(op):
    wmgy__fpx = op == operator.or_

    def bool_array_impl(val1, val2):
        if not is_valid_boolean_array_logical_op(val1, val2):
            return
        dgjfa__jhlyj = bodo.utils.utils.is_array_typ(val1, False)
        lvx__koqwv = bodo.utils.utils.is_array_typ(val2, False)
        amgit__emcfi = 'val1' if dgjfa__jhlyj else 'val2'
        oncn__kjfo = 'def impl(val1, val2):\n'
        oncn__kjfo += f'  n = len({amgit__emcfi})\n'
        oncn__kjfo += (
            '  out_arr = bodo.utils.utils.alloc_type(n, bodo.boolean_array, (-1,))\n'
            )
        oncn__kjfo += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if dgjfa__jhlyj:
            null1 = 'bodo.libs.array_kernels.isna(val1, i)\n'
            pkbjz__hvdwd = 'val1[i]'
        else:
            null1 = 'False\n'
            pkbjz__hvdwd = 'val1'
        if lvx__koqwv:
            null2 = 'bodo.libs.array_kernels.isna(val2, i)\n'
            ynsd__gxa = 'val2[i]'
        else:
            null2 = 'False\n'
            ynsd__gxa = 'val2'
        if wmgy__fpx:
            oncn__kjfo += f"""    result, isna_val = compute_or_body({null1}, {null2}, {pkbjz__hvdwd}, {ynsd__gxa})
"""
        else:
            oncn__kjfo += f"""    result, isna_val = compute_and_body({null1}, {null2}, {pkbjz__hvdwd}, {ynsd__gxa})
"""
        oncn__kjfo += '    out_arr[i] = result\n'
        oncn__kjfo += '    if isna_val:\n'
        oncn__kjfo += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        oncn__kjfo += '      continue\n'
        oncn__kjfo += '  return out_arr\n'
        iboyf__vzvhz = {}
        exec(oncn__kjfo, {'bodo': bodo, 'numba': numba, 'compute_and_body':
            compute_and_body, 'compute_or_body': compute_or_body}, iboyf__vzvhz
            )
        impl = iboyf__vzvhz['impl']
        return impl
    return bool_array_impl


def compute_or_body(null1, null2, val1, val2):
    pass


@overload(compute_or_body)
def overload_compute_or_body(null1, null2, val1, val2):

    def impl(null1, null2, val1, val2):
        if null1 and null2:
            return False, True
        elif null1:
            return val2, val2 == False
        elif null2:
            return val1, val1 == False
        else:
            return val1 | val2, False
    return impl


def compute_and_body(null1, null2, val1, val2):
    pass


@overload(compute_and_body)
def overload_compute_and_body(null1, null2, val1, val2):

    def impl(null1, null2, val1, val2):
        if null1 and null2:
            return False, True
        elif null1:
            return val2, val2 == True
        elif null2:
            return val1, val1 == True
        else:
            return val1 & val2, False
    return impl


def create_boolean_array_logical_lower_impl(op):

    def logical_lower_impl(context, builder, sig, args):
        impl = create_nullable_logical_op_overload(op)(*sig.args)
        return context.compile_internal(builder, impl, sig, args)
    return logical_lower_impl


class BooleanArrayLogicalOperatorTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        if not is_valid_boolean_array_logical_op(args[0], args[1]):
            return
        tma__zqy = boolean_array
        return tma__zqy(*args)


def is_valid_boolean_array_logical_op(typ1, typ2):
    gco__uxfup = (typ1 == bodo.boolean_array or typ2 == bodo.boolean_array
        ) and (bodo.utils.utils.is_array_typ(typ1, False) and typ1.dtype ==
        types.bool_ or typ1 == types.bool_) and (bodo.utils.utils.
        is_array_typ(typ2, False) and typ2.dtype == types.bool_ or typ2 ==
        types.bool_)
    return gco__uxfup


def _install_nullable_logical_lowering():
    for op in (operator.and_, operator.or_):
        wdnph__sgm = create_boolean_array_logical_lower_impl(op)
        infer_global(op)(BooleanArrayLogicalOperatorTemplate)
        for typ1, typ2 in [(boolean_array, boolean_array), (boolean_array,
            types.bool_), (boolean_array, types.Array(types.bool_, 1, 'C'))]:
            lower_builtin(op, typ1, typ2)(wdnph__sgm)
            if typ1 != typ2:
                lower_builtin(op, typ2, typ1)(wdnph__sgm)


_install_nullable_logical_lowering()
