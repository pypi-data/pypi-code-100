"""
==================================================
Equation (:mod:`sknrf.model.dataviewer.equation`)
==================================================

This module stores custom post-measurement calculations inside a dataset.

See Also
--------
sknrf.model.dataviewer.dataset.DatagroupModel, sknrf.model.dataviewer.dataset.DatasetModel

"""

import re
import logging

from PySide2 import QtCore
from PySide2.QtCore import Qt, QAbstractTableModel
import torch as th
import tables as tb
from tables.node import NotLoggedMixin
from toposort import toposort_flatten

__author__ = 'dtbespal'
logger = logging.getLogger(__name__)


dtype_atom_map = {
    th.uint8:             tb.UInt8Atom(),
    th.int8:              tb.Int8Atom(),
    th.int16:             tb.Int16Atom(),
    th.short:             tb.Int16Atom(),
    th.int32:             tb.Int32Atom(),
    th.int:               tb.Int32Atom(),
    th.int64:             tb.Int64Atom(),
    th.long:              tb.Int64Atom(),
    th.float16:           tb.Float16Atom(),
    th.half:              tb.Float16Atom(),
    th.float32:           tb.Float32Atom(),
    th.float:             tb.Float32Atom(),
    th.float64:           tb.Float64Atom(),
    th.double:            tb.Float64Atom(),
    th.complex64:         tb.ComplexAtom(itemsize=8),
    th.complex128:        tb.ComplexAtom(itemsize=16),
}


class SignalArray(NotLoggedMixin, tb.Group):
    """PyTables database representation of a Signal

    Parameters
    ----------
    parentnode : tables.File
        Reference to the parent node inside the database.
    name : str
        Database node name.
    obj : Signal_like
         Reference to a Signal object to be stored in the database.
    title : str
        Title of the node inside the database.
    new : bool
        Create new node in database if True.

    """
    _c_classid = 'SIGNALARRAY'

    # _c_classId = previous_api_property('_c_classid')

    def __init__(self, parentnode, name, obj=None, title='', new=False, filters=None, byteorder=None, _log=True, _atom=None):
        super(SignalArray, self).__init__(parentnode, name, title=title, new=new, filters=filters, _log=_log)
        if new:
            self._v_attrs.type = obj.__class__.__name__
            tb.CArray(self, 'data',
                      atom=dtype_atom_map[obj.dtype], shape=list(obj.shape), title=title, filters=filters, byteorder=byteorder, _log=_log)
            self[...] = obj.detach().numpy()

    def copy(self):
        return self.__getitem__(Ellipsis)

    def __setitem__(self, key, value):
        self.data.__setitem__(key, value)

    def __getitem__(self, keys):
        return th.as_tensor(self.data.__getitem__(keys))

    def _g_create(self):
        return super(SignalArray, self)._g_create()

    def _g_open(self):
        return super(SignalArray, self)._g_open()

    def _g_copy(self, newparent, newname, recursive, _log=True, **kwargs):
        return super(SignalArray, self)._g_copy(newparent, newname, recursive, _log=_log, **kwargs)


class DatasetEquationModel(object):
    """Dataset Equation Model

    A temporary dataset attribute defined by:
        * A string name
        * A string expression in terms of current dataset attributes that evaluates to a value using the built-in eval() function.

    Parameters
    ----------
    dataset : DatasetModel
        Reference to the current dataset.
    name : str
        Name of the dataset equation.

    """
    _eval_order = []
    _eval_map = {}

    def __init__(self, dataset, name="Untitled"):
        super(DatasetEquationModel, self).__init__()
        index = 1
        self.name = name
        while dataset.__contains__(self.name):
            self.name = name + str(index)
            index += 1
        self.eqn = "0"
        self._eqn = "0"
        self.is_valid = False
        self.eval(dataset, eqn=self.eqn)

    def eval(self, dataset, eqn=""):
        """Evaluate the Dataset Equation expression based on attributes in the current dataset

        Parameters
        ----------
        dataset : str
            Reference to the current dataset.
        eqn : str
            A string expression in terms of current dataset attributes that evaluates to a value using the built-in eval() function.

        """
        if eqn:
            if "__" in eqn:
                raise ValueError("Invalid equation character sequence")
            _eqn = eqn
            eqn_refs = re.findall(r"\.(\w+)", _eqn)
            for eqn_ref in eqn_refs:
                if '[' not in eqn_ref:
                    _eqn = _eqn.replace(eqn_ref, eqn_ref + "[...]")
            _eqn, _ = re.subn(r"\.(\w+)((?=\[.+\]))", r"dataset.\1\2", _eqn)
            self.eqn, self._eqn = eqn, _eqn
            DatasetEquationModel._eval_map[self.name] = set(re.findall(r"\.(\w+)", self.eqn))
            DatasetEquationModel._eval_order = toposort_flatten(DatasetEquationModel._eval_map)
        try:
            r_val = eval(self._eqn, {'__builtins__': {}}, {"dataset": dataset})
            if isinstance(r_val, (tb.array.Array, SignalArray)):
                raise TypeError("Database Equation cannot be accessed without indexation.")
        except (SyntaxError, TypeError, NameError, AttributeError, ValueError):
            self.is_valid = False
            logger.error("Invalid Equation: %s = %s", self.name, self.eqn, exc_info=True)
            raise
        else:
            self.is_valid = True
            if not isinstance(r_val, th.Tensor):
                r_val = th.as_tensor(r_val)
            if len(r_val.shape) == 0:
                r_val = r_val.unsqueeze(0)
            return r_val


class EquationTableModel(QAbstractTableModel):
    """The equation table Model.

        Parameters
        ----------
        root : OrderedDict
            The dictionary of items that populate the equation table.
    """
    def __init__(self, root, parent=None):
        super(EquationTableModel, self).__init__(parent)
        self.header = ["Variable", "Shape", "Unit"]
        self._root = root
        self._num_rows = 0
        self._num_cols = 3
        self._selected_row = 0
        self._selected_name = ""
        self._selected_value = None
        self._selected_shape = tuple()
        self._selected_unit = ""
        self._row_key_map = {}
        self.shape_map = dict.fromkeys(tuple(root.keys()), "")
        self.unit_map = dict.fromkeys(tuple(root.keys()), "")
        for k, v in self._root.items():
            if hasattr(v, "data"):
                self._row_key_map[self._num_rows] = k
                self.shape_map[k] = v[...].shape
                self.unit_map[k] = ""
                self._num_rows += 1

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def rowCount(self, parent):
        return self._num_rows

    def columnCount(self, parent):
        return self._num_cols

    def selected(self):
        """
            Returns
            -------
            ndarray
                The selected dictionary value based on the selected row.
        """
        return self._selected_row, self._selected_name, self._selected_value, self._selected_shape, self._selected_unit

    @QtCore.Slot(int)
    def set_selected(self, index):
        """ Set the selected dictionary value

            Parameters
            ----------
            index : QtCore.QModelIndex
                The table row to be selected.
        """
        index = index.row()
        self._selected_row = index
        self._selected_name = self._row_key_map[index]
        self._selected_value = self._root[self._row_key_map[index]]
        self._selected_shape = self.shape_map[self._row_key_map[index]]
        self._selected_unit = self.unit_map[self._row_key_map[index]]

    def data(self, index, role=Qt.DisplayRole):
        """ Get the table data.

            Parameters
            ----------
            index : QtCore.QModelIndex
                The table index to get.
            role : Qt.DisplayRole, optional
                The requested data role to get.

            Returns
            -------
            QtCore.QVariant :
                The return type is determined by the data role.

        """
        if not index.isValid():
            return None
        row, col = index.row(), index.column()
        if role == Qt.DisplayRole:
            key = self._row_key_map[row]
            if col == 0:
                return key
            elif col == 1:
                return str(self.shape_map[key])
            elif col == 2:
                return self.unit_map[key]
        else:
            return None

