"""CSR Matrix data type implementation for scipy.sparse.csr_matrix
"""
import operator
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
import bodo
from bodo.utils.typing import BodoError


class CSRMatrixType(types.ArrayCompatible):
    ndim = 2

    def __init__(self, dtype, idx_dtype):
        self.dtype = dtype
        self.idx_dtype = idx_dtype
        super(CSRMatrixType, self).__init__(name=
            f'CSRMatrixType({dtype}, {idx_dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    def copy(self):
        return CSRMatrixType(self.dtype, self.idx_dtype)


@register_model(CSRMatrixType)
class CSRMatrixModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        hkhm__jrkjv = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'indices', types.Array(fe_type.idx_dtype, 1, 'C')), ('indptr',
            types.Array(fe_type.idx_dtype, 1, 'C')), ('shape', types.
            UniTuple(types.int64, 2))]
        models.StructModel.__init__(self, dmm, fe_type, hkhm__jrkjv)


make_attribute_wrapper(CSRMatrixType, 'data', 'data')
make_attribute_wrapper(CSRMatrixType, 'indices', 'indices')
make_attribute_wrapper(CSRMatrixType, 'indptr', 'indptr')
make_attribute_wrapper(CSRMatrixType, 'shape', 'shape')


@intrinsic
def init_csr_matrix(typingctx, data_t, indices_t, indptr_t, shape_t=None):
    assert isinstance(data_t, types.Array)
    assert isinstance(indices_t, types.Array) and isinstance(indices_t.
        dtype, types.Integer)
    assert indices_t == indptr_t

    def codegen(context, builder, signature, args):
        uzcrn__ria, pgmzx__tex, qmen__ohd, vhb__wwq = args
        upfky__qxvp = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        upfky__qxvp.data = uzcrn__ria
        upfky__qxvp.indices = pgmzx__tex
        upfky__qxvp.indptr = qmen__ohd
        upfky__qxvp.shape = vhb__wwq
        context.nrt.incref(builder, signature.args[0], uzcrn__ria)
        context.nrt.incref(builder, signature.args[1], pgmzx__tex)
        context.nrt.incref(builder, signature.args[2], qmen__ohd)
        return upfky__qxvp._getvalue()
    dvxt__vct = CSRMatrixType(data_t.dtype, indices_t.dtype)
    lpejy__zmq = dvxt__vct(data_t, indices_t, indptr_t, types.UniTuple(
        types.int64, 2))
    return lpejy__zmq, codegen


if bodo.utils.utils.has_scipy():
    import scipy.sparse

    @typeof_impl.register(scipy.sparse.csr_matrix)
    def _typeof_csr_matrix(val, c):
        dtype = numba.from_dtype(val.dtype)
        idx_dtype = numba.from_dtype(val.indices.dtype)
        return CSRMatrixType(dtype, idx_dtype)


@unbox(CSRMatrixType)
def unbox_csr_matrix(typ, val, c):
    upfky__qxvp = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    sxdj__xir = c.pyapi.object_getattr_string(val, 'data')
    pvcc__rze = c.pyapi.object_getattr_string(val, 'indices')
    vkgd__fqynu = c.pyapi.object_getattr_string(val, 'indptr')
    nmap__zbba = c.pyapi.object_getattr_string(val, 'shape')
    upfky__qxvp.data = c.pyapi.to_native_value(types.Array(typ.dtype, 1,
        'C'), sxdj__xir).value
    upfky__qxvp.indices = c.pyapi.to_native_value(types.Array(typ.idx_dtype,
        1, 'C'), pvcc__rze).value
    upfky__qxvp.indptr = c.pyapi.to_native_value(types.Array(typ.idx_dtype,
        1, 'C'), vkgd__fqynu).value
    upfky__qxvp.shape = c.pyapi.to_native_value(types.UniTuple(types.int64,
        2), nmap__zbba).value
    c.pyapi.decref(sxdj__xir)
    c.pyapi.decref(pvcc__rze)
    c.pyapi.decref(vkgd__fqynu)
    c.pyapi.decref(nmap__zbba)
    yog__guqw = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(upfky__qxvp._getvalue(), is_error=yog__guqw)


@box(CSRMatrixType)
def box_csr_matrix(typ, val, c):
    eat__ive = c.context.insert_const_string(c.builder.module, 'scipy.sparse')
    vivu__hvg = c.pyapi.import_module_noblock(eat__ive)
    upfky__qxvp = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Array(typ.dtype, 1, 'C'),
        upfky__qxvp.data)
    sxdj__xir = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        upfky__qxvp.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        upfky__qxvp.indices)
    pvcc__rze = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1, 'C'
        ), upfky__qxvp.indices, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        upfky__qxvp.indptr)
    vkgd__fqynu = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1,
        'C'), upfky__qxvp.indptr, c.env_manager)
    nmap__zbba = c.pyapi.from_native_value(types.UniTuple(types.int64, 2),
        upfky__qxvp.shape, c.env_manager)
    gqae__zys = c.pyapi.tuple_pack([sxdj__xir, pvcc__rze, vkgd__fqynu])
    yfuo__ipr = c.pyapi.call_method(vivu__hvg, 'csr_matrix', (gqae__zys,
        nmap__zbba))
    c.pyapi.decref(gqae__zys)
    c.pyapi.decref(sxdj__xir)
    c.pyapi.decref(pvcc__rze)
    c.pyapi.decref(vkgd__fqynu)
    c.pyapi.decref(nmap__zbba)
    c.pyapi.decref(vivu__hvg)
    c.context.nrt.decref(c.builder, typ, val)
    return yfuo__ipr


@overload(len, no_unliteral=True)
def overload_csr_matrix_len(A):
    if isinstance(A, CSRMatrixType):
        return lambda A: A.shape[0]


@overload_attribute(CSRMatrixType, 'ndim')
def overload_csr_matrix_ndim(A):
    return lambda A: 2


@overload_method(CSRMatrixType, 'copy', no_unliteral=True)
def overload_csr_matrix_copy(A):

    def copy_impl(A):
        return init_csr_matrix(A.data.copy(), A.indices.copy(), A.indptr.
            copy(), A.shape)
    return copy_impl


@overload(operator.getitem, no_unliteral=True)
def csr_matrix_getitem(A, idx):
    if not isinstance(A, CSRMatrixType):
        return
    jvllf__izeur = A.dtype
    yocn__njwms = A.idx_dtype
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):

        def impl(A, idx):
            stfm__hluk, vlbi__fzr = A.shape
            yfbkn__nzxs = numba.cpython.unicode._normalize_slice(idx[0],
                stfm__hluk)
            byxer__lbk = numba.cpython.unicode._normalize_slice(idx[1],
                vlbi__fzr)
            if yfbkn__nzxs.step != 1 or byxer__lbk.step != 1:
                raise ValueError(
                    'CSR matrix slice getitem only supports step=1 currently')
            djt__aydop = yfbkn__nzxs.start
            fwtay__eagau = yfbkn__nzxs.stop
            xdn__ozmh = byxer__lbk.start
            fbpzz__iiz = byxer__lbk.stop
            hriqk__mecb = A.indptr
            iwamc__lsic = A.indices
            rcvo__fsp = A.data
            udmge__ygeu = fwtay__eagau - djt__aydop
            eef__bvw = fbpzz__iiz - xdn__ozmh
            ynhpk__gip = 0
            cnb__pxmch = 0
            for obh__doxjc in range(udmge__ygeu):
                vds__mmymw = hriqk__mecb[djt__aydop + obh__doxjc]
                qoq__wbza = hriqk__mecb[djt__aydop + obh__doxjc + 1]
                for kxgbw__deyp in range(vds__mmymw, qoq__wbza):
                    if iwamc__lsic[kxgbw__deyp] >= xdn__ozmh and iwamc__lsic[
                        kxgbw__deyp] < fbpzz__iiz:
                        ynhpk__gip += 1
            wxxek__ismr = np.empty(udmge__ygeu + 1, yocn__njwms)
            cgkn__zfwh = np.empty(ynhpk__gip, yocn__njwms)
            peqys__kyt = np.empty(ynhpk__gip, jvllf__izeur)
            wxxek__ismr[0] = 0
            for obh__doxjc in range(udmge__ygeu):
                vds__mmymw = hriqk__mecb[djt__aydop + obh__doxjc]
                qoq__wbza = hriqk__mecb[djt__aydop + obh__doxjc + 1]
                for kxgbw__deyp in range(vds__mmymw, qoq__wbza):
                    if iwamc__lsic[kxgbw__deyp] >= xdn__ozmh and iwamc__lsic[
                        kxgbw__deyp] < fbpzz__iiz:
                        cgkn__zfwh[cnb__pxmch] = iwamc__lsic[kxgbw__deyp
                            ] - xdn__ozmh
                        peqys__kyt[cnb__pxmch] = rcvo__fsp[kxgbw__deyp]
                        cnb__pxmch += 1
                wxxek__ismr[obh__doxjc + 1] = cnb__pxmch
            return init_csr_matrix(peqys__kyt, cgkn__zfwh, wxxek__ismr, (
                udmge__ygeu, eef__bvw))
        return impl
    raise BodoError(
        f'getitem for CSR matrix with index type {idx} not supported yet.')
