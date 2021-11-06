from enum import Enum
import pickle
import inspect
import importlib
from collections import OrderedDict

from PySide2 import QtCore
from PySide2.QtCore import Qt, QModelIndex, QMimeData, QByteArray
from PySide2.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide2.QtWidgets import QApplication

from sknrf.model.base import AbstractModel
from sknrf.model.runtime import RuntimeModel

__author__ = 'dtbespal'
icon_map = {"package": ":/PNG/green/32/circled_p.png",
            "module": ":/PNG/cyan/32/circled_m.png",
            "class": ":/PNG/blue/32/circled_c.png",
            "static_method": ":/PNG/violet/32/circled_s.png",
            "function": ":/PNG/magenta/32/circled_f.png",
            "method": ":/PNG/red/32/circled_m.png",
            "property": ":/PNG/orange/32/circled_p.png",
            "attribute": ":/PNG/yellow/32/circled_a.png"}


class ActionItemDataType(Enum):
    """Data type of the python object stored inside the ActionItemDataRole.ObjectRole of an ActionItem.
    """
    Module = 0
    Class = 1
    Object = 2
    Function = 3
    Method = 4


class ActionItemDataRole(Enum):
    """Data role of data stored in an ActionItem.
    """
    DisplayRole = int(Qt.DisplayRole)
    UserRole = int(Qt.UserRole)
    IconRole = 33
    ObjectRole = 34
    TypeRole = 35
    CodeRole = 36
    ModuleRole = 37


class ActionItem(QStandardItem):
    """Action Item that can be added to ActionItemModel.

    A QStandardItem that contains the following additional ItemDataRoles:

        * ActionItemDataRole.IconRole: A filename string
        * ActionItemDataRole.ObjectRole: A Python Object
        * ActionItemDataRole.TypeRole: A ActionItemDataType indicating the Pyhton object datatype.
        * ActionItemDataRole.CodeRole: A string list of Python code in the format
            [["line[1]_return_var", "line[1]_function_call"],
            ["line[2]_return_var", "line[2]_function_call"],
            ...
            ["line[n]_return_var", "line[n]_function_call"]]
        * ActionItemDataRole.ModuleRole: The Python module object that defines the Python object

    Parameters
    ----------
    icon_filename : str
        Icon Filename eg.) ":/PNG/32/function.png".
    text : str
        The text stored in the Qt.DisplayRole.
    py_object : object
        A Python object.
    type_ : ActionItemDataType
        ActionItemDataType of the Python object.
    py_code : list
        A string list of python code in the format shown above.
    py_module : object
        A python module object.

    """
    def __init__(self, icon_filename="", text="", edit="", type_=ActionItemDataType.Module,
                 py_object=None, py_code="", py_module=None):
        super(ActionItem, self).__init__(QIcon(icon_filename), text)
        edit = edit if len(edit) > 0 else text
        self._icon_filename = None
        self._action_type = None
        self._py_object = None
        self._py_code = None
        self._py_module = None
        self.setData(icon_filename, ActionItemDataRole.IconRole)
        self.setData(text, ActionItemDataRole.DisplayRole)
        self.setData(edit, ActionItemDataRole.UserRole)
        self.setData(type_, ActionItemDataRole.TypeRole)
        self.setData(py_object, ActionItemDataRole.ObjectRole)
        self.setData(py_code, ActionItemDataRole.CodeRole)
        self.setData(py_module, ActionItemDataRole.ModuleRole)

    def __getstate__(self, state={}):
        # Automatically save selected object ATTRIBUTES
        state = self.__dict__.copy()
        # ### Manually save selected object PROPERTIES here ###
        state.pop("_py_module")
        state["text"] = self.data(ActionItemDataRole.DisplayRole)
        state["edit"] = self.data(ActionItemDataRole.UserRole)
        return state

    def __setstate__(self, state):
        self.__init__(state["_icon_filename"], state["text"], state["edit"],
                      state["_action_type"], state["_py_object"], state["_py_code"])
        # ### Manually load saved object ATTRIBUTES and PROPERTIES here ###
        if self._action_type == ActionItemDataType.Module:
            self._py_module = importlib.import_module(state["edit"])

    def data(self, role=Qt.DisplayRole):
        """Returns the data stored in an Action Item that matches the provided role.

        Parameters
        ----------
        role : ActionItemDataRole
            The desired data stored inside the Action Item

        """
        try:
            role = ActionItemDataRole(role)
        except ValueError:
            return super(ActionItem, self).data(role)
        if role == ActionItemDataRole.DisplayRole:
            return super(ActionItem, self).data(role.value)
        if role == ActionItemDataRole.UserRole:
            return super(ActionItem, self).data(role.value)
        if role == ActionItemDataRole.IconRole:
            return self._icon_filename
        if role == ActionItemDataRole.ObjectRole:
            return self._py_object
        if role == ActionItemDataRole.TypeRole:
            return self._action_type
        if role == ActionItemDataRole.CodeRole:
            return self._py_code
        if role == ActionItemDataRole.ModuleRole:
            return self._py_module

    def setData(self, value, role=Qt.DisplayRole):
        """Sets the data stored in an Action Item that matches the provided role.

        Parameters
        ----------
        role : ActionItemDataRole
            The desired data stored inside the Action

        """
        try:
            role = ActionItemDataRole(role)
        except ValueError:
            return super(ActionItem, self).setData(value, role)
        if role == ActionItemDataRole.DisplayRole and isinstance(value, str):
            super(ActionItem, self).setData(value, role.value)
            return True
        if role == ActionItemDataRole.UserRole and isinstance(value, str):
            super(ActionItem, self).setData(value, role.value)
            return True
        if role == ActionItemDataRole.IconRole and isinstance(value, str):
            self.setIcon(QIcon(value))
            self._icon_filename = value
            return True
        if role == ActionItemDataRole.ObjectRole:
            self._py_object = value
            return True
        if role == ActionItemDataRole.TypeRole and isinstance(value, ActionItemDataType):
            self._action_type = value
            return True
        if role == ActionItemDataRole.CodeRole and isinstance(value, list):
            self._py_code = value
            return True
        if role == ActionItemDataRole.ModuleRole and inspect.ismodule(value):
            self._py_module = value
            return True
        return False


class ActionItemModel(QStandardItemModel):
    """Action Item Model that represents all model data stored in a QAbstractItemView.

    A QStandardItem Model that also supports the following MIME data type:

        * "action/item": A ActionItem object.

    Parameters
    ----------
    parent : QAbstractItemView
        The parent view object.

    """
    def __init__(self, parent=None):
        super(ActionItemModel, self).__init__(parent=parent)

    def __getstate__(self, state={}):
        # Automatically save selected object ATTRIBUTES
        if self.__class__ == ActionItemModel:
            state = self.__dict__.copy()
        # ### Manually save selected object PROPERTIES here ###
        items = [None]*self.rowCount()
        for index in range(self.rowCount()):
            items[index] = self.item(index)
        state["items"] = items
        del state["rowsInserted"]
        del state["dataChanged"]
        del state["rowsRemoved"]
        return state

    def __setstate__(self, state):
        if self.__class__ == ActionItemModel:
            self.__init__()
        # ### Manually load saved object ATTRIBUTES and PROPERTIES here ###
        for item in state["items"]:
            self.appendRow(item)

    def supportedDropActions(self, *args, **kwargs):
        """Virtual method that defines the allowed Qt.DropActions.
        """
        return Qt.CopyAction | Qt.MoveAction

    def flags(self, index):
        """Virtual method that defines the enabled Qt.ItemFlags.
        """
        default_flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled
        if index.isValid():
            return Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | default_flags
        else:
            return Qt.ItemIsDropEnabled | default_flags

    def mimeTypes(self):
        """Virtual method that defines the supported MIME data types.
        """
        return ["action/item"]

    def mimeData(self, index):
        """Returns the MIME Data object of the desired model index.

        Parameters
        ----------
        index : QModelIndex
            The desired model index.

        """
        if isinstance(index, QModelIndex):
            mime_data = QMimeData()
            item = self.itemFromIndex(index)
            mime_data.setData("action/item", QByteArray(pickle.dumps(item)))
            return mime_data


class SequencerSideModel(AbstractModel):

    def __new__(cls, model=OrderedDict()):
        self = super(SequencerSideModel, cls).__new__(cls)
        return self

    def __init__(self, model=OrderedDict()):
        super(SequencerSideModel, self).__init__()
        self._package_map = model

    def __getstate__(self, state={}):
        state = super(SequencerSideModel, self).__getstate__(state=state)
        # ### Manually save selected object PROPERTIES here ###
        state['_package_map'] = self._package_map
        return state

    def __setstate__(self, state):
        super(SequencerSideModel, self).__setstate__(state)
        # ### Manually load saved object ATTRIBUTES and PROPERTIES here ###
        self._package_map = state['_package_map']

    def __info__(self):
        """ Initializes the display information of a device and stores information in self.info.
        """
        super(SequencerSideModel, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###

    def package_map(self):
        return self._package_map


class SequencerModel(AbstractModel):
    """The model definition of the Sequencer Menu.

    Model definition that contains:

        * import_model: The model for the ImportListView.
        * variable_modee: The model for the VariableTableWidget
        * sequence_model: The model for the SequenceTreeView

    """
    def __new__(cls):
        self = super(SequencerModel, cls).__new__(cls)
        return self

    def __init__(self):
        super(SequencerModel, self).__init__()
        self._import_model = ActionItemModel()
        self._variable_model = ActionItemModel()
        self._sequence_model = ActionItemModel()

    def __getstate__(self, state={}):
        state = super(SequencerModel, self).__getstate__(state=state)
        # ### Manually save selected object PROPERTIES here ###
        state['_import_model'] = self._import_model
        state['_variable_model'] = self._variable_model
        state['_sequence_model'] = self._sequence_model
        return state

    def __setstate__(self, state):
        super(SequencerModel, self).__setstate__(state)
        # ### Manually load saved object ATTRIBUTES and PROPERTIES here ###
        self._import_model = state['_import_model']
        self._variable_model = state['_variable_model']
        self._sequence_model = state['_sequence_model']

    def __info__(self):
        """ Initializes the display information of a device and stores information in self.info.
        """
        super(SequencerModel, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###

    def import_model(self):
        return self._import_model

    def variable_model(self):
        return self._variable_model

    def sequence_model(self):
        return self._sequence_model


class AbstractSequencerRuntimeModel(RuntimeModel):

    def __new__(cls, locals_={}):
        self = super(AbstractSequencerRuntimeModel, cls).__new__(cls)
        return self

    def __init__(self, locals_={}):
        super(AbstractSequencerRuntimeModel, self).__init__()
        self._locals = locals_

    def connect_signals(self):
        for k, v in self._locals.items():
            if isinstance(v, RuntimeModel):
                v.error.connect(self.error_handler)
                v.init_request.connect(self.initialize)
                v.update_request.connect(self.update)
                v.close_request.connect(self.close)

    def disconnect_signals(self):
        main_thread = QApplication.instance().thread()
        for k, v in self._locals.items():
            if isinstance(v, AbstractModel):
                v.moveToThread(main_thread)
            if isinstance(v, RuntimeModel):
                try:
                    v.error.disconnect()
                    v.init_request.disconnect()
                    v.update_request.disconnect()
                    v.close_request.disconnect()
                except RuntimeError:
                    pass

    @QtCore.Slot(object)
    def initialize(self, model):
        self.init_request.emit(model)

    @QtCore.Slot(object)
    def update(self, model=None, batch_index=-1):
        self.update_request.emit(model, batch_index)

    @QtCore.Slot(object)
    def close(self, model):
        self.close_request.emit(model)

    def error_handler(self, message):
        self.error.emit(message)


