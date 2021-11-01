"""Support for MultiIndex type of Pandas
"""
import operator
import numba
import pandas as pd
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, register_model, typeof_impl, unbox
from bodo.utils.typing import BodoError, check_unsupported_args, dtype_to_array_type, get_val_type_maybe_str_literal, is_overload_none


class MultiIndexType(types.Type):

    def __init__(self, array_types, names_typ=None, name_typ=None):
        names_typ = (types.none,) * len(array_types
            ) if names_typ is None else names_typ
        name_typ = types.none if name_typ is None else name_typ
        self.array_types = array_types
        self.names_typ = names_typ
        self.name_typ = name_typ
        super(MultiIndexType, self).__init__(name=
            'MultiIndexType({}, {}, {})'.format(array_types, names_typ,
            name_typ))
    ndim = 1

    def copy(self):
        return MultiIndexType(self.array_types, self.names_typ, self.name_typ)

    @property
    def nlevels(self):
        return len(self.array_types)


@register_model(MultiIndexType)
class MultiIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        zndbd__jxhys = [('data', types.Tuple(fe_type.array_types)), (
            'names', types.Tuple(fe_type.names_typ)), ('name', fe_type.
            name_typ)]
        super(MultiIndexModel, self).__init__(dmm, fe_type, zndbd__jxhys)


make_attribute_wrapper(MultiIndexType, 'data', '_data')
make_attribute_wrapper(MultiIndexType, 'names', '_names')
make_attribute_wrapper(MultiIndexType, 'name', '_name')


@typeof_impl.register(pd.MultiIndex)
def typeof_multi_index(val, c):
    array_types = tuple(numba.typeof(val.levels[pubm__ztqkv].values) for
        pubm__ztqkv in range(val.nlevels))
    return MultiIndexType(array_types, tuple(get_val_type_maybe_str_literal
        (hchcm__novkg) for hchcm__novkg in val.names), numba.typeof(val.name))


@box(MultiIndexType)
def box_multi_index(typ, val, c):
    ykf__lwkku = c.context.insert_const_string(c.builder.module, 'pandas')
    lgxg__xjckp = c.pyapi.import_module_noblock(ykf__lwkku)
    rgtad__pxv = c.pyapi.object_getattr_string(lgxg__xjckp, 'MultiIndex')
    xak__qoef = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Tuple(typ.array_types), xak__qoef
        .data)
    data = c.pyapi.from_native_value(types.Tuple(typ.array_types),
        xak__qoef.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Tuple(typ.names_typ), xak__qoef.names
        )
    names = c.pyapi.from_native_value(types.Tuple(typ.names_typ), xak__qoef
        .names, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, xak__qoef.name)
    name = c.pyapi.from_native_value(typ.name_typ, xak__qoef.name, c.
        env_manager)
    sortorder = c.pyapi.make_none()
    bznz__jnux = c.pyapi.call_method(rgtad__pxv, 'from_arrays', (data,
        sortorder, names))
    c.pyapi.object_setattr_string(bznz__jnux, 'name', name)
    c.pyapi.decref(lgxg__xjckp)
    c.pyapi.decref(rgtad__pxv)
    c.context.nrt.decref(c.builder, typ, val)
    return bznz__jnux


@unbox(MultiIndexType)
def unbox_multi_index(typ, val, c):
    hmq__slv = []
    enmx__wbxul = []
    for pubm__ztqkv in range(typ.nlevels):
        nzdf__opf = c.pyapi.unserialize(c.pyapi.serialize_object(pubm__ztqkv))
        qoq__aln = c.pyapi.call_method(val, 'get_level_values', (nzdf__opf,))
        yyl__ibho = c.pyapi.object_getattr_string(qoq__aln, 'values')
        c.pyapi.decref(qoq__aln)
        c.pyapi.decref(nzdf__opf)
        jpjy__zkkz = c.pyapi.to_native_value(typ.array_types[pubm__ztqkv],
            yyl__ibho).value
        hmq__slv.append(jpjy__zkkz)
        enmx__wbxul.append(yyl__ibho)
    if isinstance(types.Tuple(typ.array_types), types.UniTuple):
        data = cgutils.pack_array(c.builder, hmq__slv)
    else:
        data = cgutils.pack_struct(c.builder, hmq__slv)
    upk__lmpy = c.pyapi.object_getattr_string(val, 'names')
    vpmqg__qyzc = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    knau__zknpq = c.pyapi.call_function_objargs(vpmqg__qyzc, (upk__lmpy,))
    names = c.pyapi.to_native_value(types.Tuple(typ.names_typ), knau__zknpq
        ).value
    ewkx__vjbk = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, ewkx__vjbk).value
    xak__qoef = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    xak__qoef.data = data
    xak__qoef.names = names
    xak__qoef.name = name
    for yyl__ibho in enmx__wbxul:
        c.pyapi.decref(yyl__ibho)
    c.pyapi.decref(upk__lmpy)
    c.pyapi.decref(vpmqg__qyzc)
    c.pyapi.decref(knau__zknpq)
    c.pyapi.decref(ewkx__vjbk)
    return NativeValue(xak__qoef._getvalue())


def from_product_error_checking(iterables, sortorder, names):
    qgoo__gfvwl = 'pandas.MultiIndex.from_product'
    plaas__aajcg = dict(sortorder=sortorder)
    hiyz__rkrja = dict(sortorder=None)
    check_unsupported_args(qgoo__gfvwl, plaas__aajcg, hiyz__rkrja)
    if not (is_overload_none(names) or isinstance(names, types.BaseTuple)):
        raise BodoError(f'{qgoo__gfvwl}: names must be None or a tuple.')
    elif not isinstance(iterables, types.BaseTuple):
        raise BodoError(f'{qgoo__gfvwl}: iterables must be a tuple.')
    elif not is_overload_none(names) and len(iterables) != len(names):
        raise BodoError(
            f'{qgoo__gfvwl}: iterables and names must be of the same length.')


def from_product(iterable, sortorder=None, names=None):
    pass


@overload(from_product)
def from_product_overload(iterables, sortorder=None, names=None):
    from_product_error_checking(iterables, sortorder, names)
    array_types = tuple(dtype_to_array_type(iterable.dtype) for iterable in
        iterables)
    if is_overload_none(names):
        names_typ = tuple([types.none] * len(iterables))
    else:
        names_typ = names.types
    gitrn__jwut = MultiIndexType(array_types, names_typ)
    iezqc__btzi = f'from_product_multiindex{numba.core.ir_utils.next_label()}'
    setattr(types, iezqc__btzi, gitrn__jwut)
    xdce__jjdt = f"""
def impl(iterables, sortorder=None, names=None):
    with numba.objmode(mi='{iezqc__btzi}'):
        mi = pd.MultiIndex.from_product(iterables, names=names)
    return mi
"""
    vrba__otc = {}
    exec(xdce__jjdt, globals(), vrba__otc)
    eqezn__pujxn = vrba__otc['impl']
    return eqezn__pujxn


@intrinsic
def init_multi_index(typingctx, data, names, name=None):
    name = types.none if name is None else name
    names = types.Tuple(names.types)

    def codegen(context, builder, signature, args):
        pctd__ofelf, jzyx__hhmuk, swsh__fdxi = args
        fibf__sft = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        fibf__sft.data = pctd__ofelf
        fibf__sft.names = jzyx__hhmuk
        fibf__sft.name = swsh__fdxi
        context.nrt.incref(builder, signature.args[0], pctd__ofelf)
        context.nrt.incref(builder, signature.args[1], jzyx__hhmuk)
        context.nrt.incref(builder, signature.args[2], swsh__fdxi)
        return fibf__sft._getvalue()
    mucpt__katc = MultiIndexType(data.types, names.types, name)
    return mucpt__katc(data, names, name), codegen


@overload(len, no_unliteral=True)
def overload_len_pd_multiindex(A):
    if isinstance(A, MultiIndexType):
        return lambda A: len(A._data[0])


@overload(operator.getitem, no_unliteral=True)
def overload_multi_index_getitem(I, ind):
    if not isinstance(I, MultiIndexType):
        return
    if not isinstance(ind, types.Integer):
        hyhrq__gvzt = len(I.array_types)
        xdce__jjdt = 'def impl(I, ind):\n'
        xdce__jjdt += '  data = I._data\n'
        xdce__jjdt += ('  return init_multi_index(({},), I._names, I._name)\n'
            .format(', '.join(f'data[{pubm__ztqkv}][ind]' for pubm__ztqkv in
            range(hyhrq__gvzt))))
        vrba__otc = {}
        exec(xdce__jjdt, {'init_multi_index': init_multi_index}, vrba__otc)
        eqezn__pujxn = vrba__otc['impl']
        return eqezn__pujxn


@lower_builtin(operator.is_, MultiIndexType, MultiIndexType)
def multi_index_is(context, builder, sig, args):
    tsmj__sfq, owhin__aodx = sig.args
    if tsmj__sfq != owhin__aodx:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._data is b._data and a._names is b._names and a._name is
            b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)
