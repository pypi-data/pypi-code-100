"""
Analysis and transformation for HDF5 support.
"""
import types as pytypes
import numba
from numba.core import ir, types
from numba.core.ir_utils import compile_to_numba_ir, find_callname, find_const, get_definition, guard, replace_arg_nodes, require
import bodo
import bodo.io
from bodo.utils.transform import get_const_value_inner


class H5_IO:

    def __init__(self, func_ir, _locals, flags, arg_types):
        self.func_ir = func_ir
        self.locals = _locals
        self.flags = flags
        self.arg_types = arg_types

    def handle_possible_h5_read(self, assign, lhs, rhs):
        mxrz__jqw = self._get_h5_type(lhs, rhs)
        if mxrz__jqw is not None:
            qcxk__hrtx = str(mxrz__jqw.dtype)
            vhcgk__tbdl = 'def _h5_read_impl(dset, index):\n'
            vhcgk__tbdl += (
                "  arr = bodo.io.h5_api.h5_read_dummy(dset, {}, '{}', index)\n"
                .format(mxrz__jqw.ndim, qcxk__hrtx))
            esxdc__cicr = {}
            exec(vhcgk__tbdl, {}, esxdc__cicr)
            jmov__yefym = esxdc__cicr['_h5_read_impl']
            dahr__obrib = compile_to_numba_ir(jmov__yefym, {'bodo': bodo}
                ).blocks.popitem()[1]
            ekp__qbj = rhs.index if rhs.op == 'getitem' else rhs.index_var
            replace_arg_nodes(dahr__obrib, [rhs.value, ekp__qbj])
            loaj__wvmd = dahr__obrib.body[:-3]
            loaj__wvmd[-1].target = assign.target
            return loaj__wvmd
        return None

    def _get_h5_type(self, lhs, rhs):
        mxrz__jqw = self._get_h5_type_locals(lhs)
        if mxrz__jqw is not None:
            return mxrz__jqw
        return guard(self._infer_h5_typ, rhs)

    def _infer_h5_typ(self, rhs):
        require(rhs.op in ('getitem', 'static_getitem'))
        ekp__qbj = rhs.index if rhs.op == 'getitem' else rhs.index_var
        jndm__dprja = guard(find_const, self.func_ir, ekp__qbj)
        require(not isinstance(jndm__dprja, str))
        val_def = rhs
        obj_name_list = []
        while True:
            val_def = get_definition(self.func_ir, val_def.value)
            require(isinstance(val_def, ir.Expr))
            if val_def.op == 'call':
                return self._get_h5_type_file(val_def, obj_name_list)
            require(val_def.op in ('getitem', 'static_getitem'))
            ndz__qlpq = (val_def.index if val_def.op == 'getitem' else
                val_def.index_var)
            nwy__rqggu = get_const_value_inner(self.func_ir, ndz__qlpq,
                arg_types=self.arg_types)
            obj_name_list.append(nwy__rqggu)

    def _get_h5_type_file(self, val_def, obj_name_list):
        require(len(obj_name_list) > 0)
        require(find_callname(self.func_ir, val_def) == ('File', 'h5py'))
        require(len(val_def.args) > 0)
        ydlp__swrdu = get_const_value_inner(self.func_ir, val_def.args[0],
            arg_types=self.arg_types)
        obj_name_list.reverse()
        import h5py
        dkn__gjzjo = h5py.File(ydlp__swrdu, 'r')
        fdho__pwuwz = dkn__gjzjo
        for nwy__rqggu in obj_name_list:
            fdho__pwuwz = fdho__pwuwz[nwy__rqggu]
        require(isinstance(fdho__pwuwz, h5py.Dataset))
        ozp__xqjdo = len(fdho__pwuwz.shape)
        wfig__bgml = numba.np.numpy_support.from_dtype(fdho__pwuwz.dtype)
        dkn__gjzjo.close()
        return types.Array(wfig__bgml, ozp__xqjdo, 'C')

    def _get_h5_type_locals(self, varname):
        ocxpt__iiu = self.locals.pop(varname, None)
        if ocxpt__iiu is None and varname is not None:
            ocxpt__iiu = self.flags.h5_types.get(varname, None)
        return ocxpt__iiu
