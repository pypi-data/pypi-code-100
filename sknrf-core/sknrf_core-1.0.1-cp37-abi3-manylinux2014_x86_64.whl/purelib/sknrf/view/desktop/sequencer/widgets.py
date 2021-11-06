import inspect
from inspect import Signature, Parameter
import importlib
import pkgutil
import pickle
from collections import OrderedDict
import weakref
from warnings import warn

from PySide2.QtCore import Qt, QPoint, QRect
from PySide2.QtGui import QDrag, QPixmap, QPainter
from PySide2.QtWidgets import QApplication, QDialog, QMessageBox, QLabel, QLineEdit, QListView, QTreeView
from PySide2.QtWidgets import QGridLayout, QCompleter

from sknrf.model.base import AbstractModel
from sknrf.model.sequencer.base import icon_map
from sknrf.model.sequencer.base import ActionItemDataType, ActionItemDataRole, ActionItem, ActionItemModel
from sknrf.view.desktop.sequencer.code import LineNumberArea
from sknrf.view.desktop.sequencer.QObjectDialog import Ui_objectDialog
from sknrf.widget.propertybrowser.view.base import TreePropertyBrowser
from sknrf.utilities.numeric import camel2underscore, Info
from sknrf.icons import red_32_rc, green_32_rc

from sknrf.widget.propertybrowser.view import BrowserCol

from sknrf.widget.propertybrowser.view import QtBrowserItem

__author__ = 'dtbespal'


class SequencerState(object):
    """Store the current state of the Sequencer Menu.
    """
    module = None
    variable = None
    variable_name = ""
    action = None
    is_valid_code = False


class ObjectDialog(QDialog, Ui_objectDialog):
    """Class object/function object argument entry dialog.

    Interactive entry dialog for class object/function object argument specification that displays the following information:
        Module: Parent module name (Read-Only)
        Return: Object/return variable name
        Argument_Name[1]: Argument_Value[1]
        Argument_Name[2]: Argument_Value[2]
        ...
        Argument_Name[n]: Argument_Value[n]

    Parameters
    ----------
    obj : object
        A class object or function object.
    globals : dict
        A dictionary containing the global variable namespace for eval/exec commands.
    locals : dict
        A dictionary containing the local variable namespace for eval/exec commands.
    parent : QWidget
        Parent GUI container.

    """
    def __init__(self, obj, parent=None, globals_=globals(), locals_=locals(), existing_arguments=()):
        super(ObjectDialog, self).__init__(parent=parent)
        self.setupUi(self)
        self.gbl = QGridLayout(self.argumentFrame)
        self.obj = obj
        self.variables = locals_
        self.signature = inspect.signature(obj)
        self.return_argument_text = ""
        self._hidden_arguments = ['cls', 'self']
        self.arguments_text = [""]*len(self.signature.parameters)
        self.arguments = [None]*len(self.signature.parameters)
        completer = QCompleter(list(self.variables.keys()))
        completer.setCaseSensitivity(Qt.CaseSensitive)
        self.reserved_names = list(self.variables.keys()) + list(globals_.keys())

        self.moduleLineEdit.setText(SequencerState.module.__name__)
        annotation = self.signature.return_annotation
        if annotation != Signature.empty:
            self.returnLineEdit.setPlaceholderText(str(annotation))
        elif inspect.isclass(self.obj):
            self.set_return_argument_text(camel2underscore(self.obj.__name__))
            self.returnLineEdit.setText(self.return_argument_text)
            self.returnLineEdit.setPlaceholderText("< class " + self.obj.__name__ + ">")
        else:
            self.returnFrame.hide()

        y = 0
        for parameter in self.signature.parameters.values():
            if parameter.name in self._hidden_arguments:
                del self.arguments_text[y]
                del self.arguments[y]
            else:
                label = QLabel(parameter.name)
                edit = QLineEdit()
                edit.setCompleter(completer)
                if parameter.kind == Parameter.VAR_POSITIONAL: # *args
                    default = ()
                elif parameter.kind == Parameter.VAR_KEYWORD: # **kwargs
                    default = {}
                else:  # POSITIONAL_OR_KEYWORD
                    default = parameter.default if parameter.default != Parameter.empty else ""
                default_str = "'"+default+"'" if isinstance(parameter.default, str) else str(default)
                existing_str = existing_arguments[y] if len(existing_arguments) > y else ""
                self.arguments_text[y] = existing_str if len(existing_str) else default_str
                self.arguments[y] = None if len(existing_str) else default
                edit.setText(self.arguments_text[y])
                if parameter.annotation != Parameter.empty:
                    edit.setPlaceholderText(str(parameter.annotation))
                self.gbl.addWidget(label, y, 0, 1, 1)
                self.gbl.addWidget(edit, y, 1, 1, 1)
                y += 1
        if y == 0:
            self.argumentFrame.hide()

        self.connect_signals()

    def connect_signals(self):
        self.returnLineEdit.editingFinished.connect(self.return_edit_finished)
        for line_edit in self.argumentFrame.findChildren(QLineEdit):
            line_edit.editingFinished.connect(self.argument_edit_finished)

    def disconnect_signals(self):
        self.returnLineEdit.editingFinished.disconnect(self.return_edit_finished)
        for line_edit in self.argumentFrame.findChildren(QLineEdit):
            line_edit.editingFinished.disconnect(self.argument_edit_finished)

    def argument_edit_finished(self):
        """Evaluates the function arguments to determine if the user input is valid.
        """
        index = 0
        for line_edit in self.argumentFrame.findChildren(QLineEdit):
            if self.sender() is line_edit:
                text = line_edit.text()
                try:
                    value = eval(text, globals(), self.variables)
                except AttributeError:
                    line_edit.setText(self.arguments_text[index])
                    QMessageBox.critical(self, 'Argument Entry Error',
                                               "Unknown argument entry")
                except ValueError:
                    line_edit.setText(self.arguments_text[index])
                    QMessageBox.critical(self, 'Argument Entry Error',
                                               "Invalid argument entry")
                else:
                    self.arguments_text[index] = text
                    self.arguments[index] = value
            index += 1

    def set_return_argument_text(self, return_argument_text):
        index = 1
        self.return_argument_text = return_argument_text
        while self.return_argument_text in self.reserved_names:
            self.return_argument_text = return_argument_text + str(index)
            index += 1

    def return_edit_finished(self):
        """Stores the name of the return variable.
        """
        self.set_return_argument_text(self.returnLineEdit.text())
        self.returnLineEdit.setText(self.return_argument_text)

    def accept(self):
        """Sets the DialogCode to Accepted and returns to the main window provided if all arguments have a specified value.
        """
        is_valid = True
        if self.returnLineEdit.isVisible() and not self.returnLineEdit.text():
            is_valid = False
        for line_edit in self.argumentFrame.findChildren(QLineEdit):
            if not line_edit.text():
                line_edit.setStyleSheet("border: 3px solid red")
                is_valid = False
            else:
                line_edit.setStyleSheet("")
        if is_valid:
            self.done(QDialog.DialogCode.Accepted)


class ActionTreeView(QTreeView):
    """A tree view containing all actions that can be performed in the Sequencer Menu.

    A list of all sequencer actions is automatically populated from the defined top-level package. The tree model is populated
    by all objects that inherit AbstractModel. The Action Tree is displayed in the following format:

        * Module
            * Class
                * Method
                * Class Method
                * Static Method
            * Function

    ActionItems from the ActionTreeView can be dragged & dropped into other QAbstractItemView objects.

    Parameters
    ----------
    model : ActionItemModel
        The model.
    package : dict
        A top-level package containing actions that populate the tree.
    parent : QWidget
        Parent GUI container.

    """
    def __init__(self, parent=None, model=None, package=None, base_class=AbstractModel, enable_methods=True):
        super(ActionTreeView, self).__init__(parent)
        self._package = package
        self._base_class = base_class
        self._enable_methods = enable_methods
        self._info_edit = None
        self.drag_start_position = QPoint(0, 0)
        if not model:
            model = ActionItemModel(self)
        self.setModel(model)
        self.set_package(package)
        self.connect_signals()

    def connect_signals(self):
        pass

    def disconnect_signals(self):
        pass

    def set_package(self, package):
        """Sets the top-level package containing actions and re-populates the tree model.
        """
        if package:
            self._package = package
            self.update()

    def set_info_edit(self, info_edit):
        """Sets a reference to the info_edit widget.
        """
        self._info_edit = info_edit

    def mousePressEvent(self, event):
        super(ActionTreeView, self).mousePressEvent(event)
        if not (event.buttons() and Qt.LeftButton):  # if not left button
            return
        self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        super(ActionTreeView, self).mouseMoveEvent(event)
        if not (event.buttons() and Qt.LeftButton):  # if not left button
            return
        if not self.currentIndex():  # if no item selected
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mime_data = self.model().mimeData(self.currentIndex())
        drag.setMimeData(mime_data)
        drag.start(Qt.CopyAction)

    def currentChanged(self, current, previous):
        """Updates the info edit widget with documentation from the current selected item.

        Parameters
        ----------
        current : ActionItem
            current selected item
        previous : ActionItem
            previous selected item

        """
        super(ActionTreeView, self).currentChanged(current, previous)
        item = self.model().itemFromIndex(current)
        if item and self._info_edit:
            action_type = item.data(ActionItemDataRole.TypeRole.value)
            obj = None
            if action_type == ActionItemDataType.Module:
                obj = item.data(ActionItemDataRole.ModuleRole.value)
            elif action_type == ActionItemDataType.Class or action_type == ActionItemDataType.Function:
                obj = item.data(ActionItemDataRole.ObjectRole.value)
            elif action_type == ActionItemDataType.Method:
                obj = getattr(item.data(ActionItemDataRole.ObjectRole.value), item.data(ActionItemDataRole.UserRole))
            doc_text = str(inspect.getdoc(obj))
            doc_text = '<html><b><font size="3">' + obj.__name__ + "</font></b><br><br>" + doc_text + "</html>"
            self._info_edit.setText(doc_text.replace("\n", "<br>"))

    def update(self):
        """Updates the ActionItemTree model with all the action items found inside the specified package.
        """
        module_map = {}
        package = self._package
        base_class = self._base_class
        model = self.model()
        model.clear()

        for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__,
                                                              prefix=package.__name__+'.',
                                                              onerror=lambda x: None):
            module = importlib.import_module(modname)
            sep = module.__name__.rfind(".")
            pkg = importlib.import_module(module.__name__[0:sep])
            if (not hasattr(pkg, "__all__") or module.__name__[sep + 1:] in pkg.__all__) \
                    and not module.__name__[sep + 1:].startswith("_") \
                    and not module.__name__[sep + 1:].startswith("test"):
                if module not in module_map:
                    py_code = [["", "from " + module.__name__[0:sep] + " import " + module.__name__[sep+1:]]]
                    item = ActionItem(icon_map["module"], module.__name__, module.__name__,
                                      ActionItemDataType.Module, None, py_code, module)
                # item = module_map[module]
                    for member_name, member_obj in inspect.getmembers(module):
                        if inspect.isclass(member_obj) \
                                and base_class in inspect.getmro(member_obj) \
                                and member_obj.__init__.__code__.co_name == 'exported_function' \
                                and not member_name.startswith("_") \
                                and not member_name.startswith("Abstract") \
                                and inspect.getmodule(member_obj) == module:
                            py_code = [["", module.__name__[sep+1:] + "." + member_obj.__name__]]
                            sub_item = ActionItem(icon_map["class"], member_obj.__name__ , member_obj.__name__,
                                                  ActionItemDataType.Class, member_obj, py_code)
                            item.appendRow(sub_item)
                            if self._enable_methods:
                                for method_name, method_obj in inspect.getmembers(member_obj):
                                    if inspect.isfunction(method_obj) and method_name[0] != "_" \
                                        and method_obj.__code__.co_name == 'exported_function':
                                        if isinstance(method_obj, staticmethod):
                                            py_code = [["", module.__name__[sep+1:] + "." + member_name + "." + method_obj.__name__ + "()"]]
                                            sub_sub_item = ActionItem(icon_map["static_method"], method_name, method_name,
                                                                      ActionItemDataType.Method, member_obj, py_code)
                                        elif isinstance(method_obj, classmethod):
                                            py_code = [["", module.__name__[sep+1:] + "." + member_name + "." + method_obj.__name__ + "()"]]
                                            sub_sub_item = ActionItem(icon_map["method"], method_name, method_name,
                                                                      ActionItemDataType.Method, member_obj, py_code)
                                        else:
                                            py_code = [["", method_obj.__name__ + "()"]]
                                            sub_sub_item = ActionItem(icon_map["method"], method_name, method_name,
                                                                      ActionItemDataType.Method, member_obj, py_code)
                                        sub_item.appendRow(sub_sub_item)
                        elif inspect.isfunction(member_obj) \
                                and member_obj.__code__.co_name == 'exported_function' \
                                and not member_name.startswith("_") \
                                and not member_name.startswith("Abstract") \
                                and inspect.getmodule(member_obj) == module:
                            py_code = [["", module.__name__[sep+1:] + "." + member_obj.__name__]]
                            sub_item = ActionItem(icon_map["function"], member_obj.__name__, member_obj.__name__,
                                                  ActionItemDataType.Function, member_obj, py_code)

                            item.appendRow(sub_item)
                    module_map[module] = item
                    if item.rowCount():
                        model.appendRow(item)


class ImportListView(QListView):
    """A list view containing all imported modules in the Sequencer Menu.

    Parameters
    ----------
    model : ActionItemModel
        The model.
    parent : QWidget
        Parent GUI container.

    """

    def __init__(self, parent=None, model=None):
        super(ImportListView, self).__init__(parent)
        self._parent = None
        self.drag_start_position = QPoint(0, 0)
        if not model:
            model = ActionItemModel(self)
        self.setModel(model)

    def set_parent(self, parent):
        """Sets the parent widget.

        Parameters
        ----------
        parent : QWidget
            Parent GUI container.

        """
        self._parent = weakref.proxy(parent)

    def mousePressEvent(self, event):
        super(ImportListView, self).mousePressEvent(event)
        if not (event.buttons() and Qt.LeftButton):  # if not left button
            return
        self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        super(ImportListView, self).mouseMoveEvent(event)
        if not (event.buttons() and Qt.LeftButton):  # if not left button
            return
        if not self.currentIndex():  # if no item selected
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = self.model().mimeData(self.currentIndex())
        drag.setMimeData(mime_data)
        drag.start(Qt.MoveAction)

    def keyPressEvent(self, event):
        super(ImportListView, self).keyPressEvent(event)
        if event.key() == Qt.Key_Delete:
            item = self.model().itemFromIndex(self.currentIndex())
            text = item.data(ActionItemDataRole.UserRole)
            variable_model = self._parent.sequencerFrame.variableTableWidget.action_model()
            for index in range(variable_model.rowCount()):
                obj = variable_model.item(index).data(ActionItemDataRole.ObjectRole)
                if inspect.getmodule(obj).__name__ == text:
                    QMessageBox.critical(self, 'Unable to remove module',
                                               'Unable to remove module.\n' +
                                               'An existing variable depends on the selected module.')
                    return
            sequence_model = self._parent.sequencerFrame.sequenceTreeView.model()
            for index in range(sequence_model.rowCount()):
                obj = sequence_model.item(index).data(ActionItemDataRole.ObjectRole)
                if inspect.getmodule(obj).__name__ == text:
                    QMessageBox.critical(self, 'Unable to remove module',
                                               'Unable to remove module.\n' +
                                               'An existing action depends on the selected module.')
                    return
            self.model().removeRow(self.currentIndex().row())

    def dragEnterEvent(self, event):
        # super(ImportListView, self).dragEnterEvent(event) accepts everything
        if event.source() == self and event.possibleActions() & Qt.MoveAction:
            event.acceptProposedAction()
        elif event.possibleActions() & Qt.CopyAction:
            item = pickle.loads(event.mimeData().data("action/item").data())
            if item.data(ActionItemDataRole.TypeRole) == ActionItemDataType.Module:
                event.acceptProposedAction()

    def dropEvent(self, event):
        # super(ImportListView, self).dropEvent(event)  # causes seg fault
        if event.dropAction() == Qt.CopyAction:
            row = self.indexAt(event.pos()).row()
            item = pickle.loads(event.mimeData().data("action/item").data())
            if self.model().findItems(item.data(ActionItemDataRole.UserRole)):
                QMessageBox.critical(self, 'Duplicate Entry in "Imports" list',
                                           'Duplicate Entry in "Imports" list.')
                return
            if row >= 0:
                self.model().insertRow(row, item)
                self.setCurrentIndex(self.model().index(row, 0))
            else:
                self.model().appendRow(item)
                self.setCurrentIndex(self.model().index(self.model().rowCount()-1, 0))
        else:
            destination_row = self.indexAt(event.pos()).row()
            if destination_row < 0:
                destination_row = self.model().rowCount() - 1
            source_row = self.currentIndex().row()
            moved_item = self.model().takeItem(source_row)
            self.model().removeRow(source_row)
            self.model().insertRow(destination_row, moved_item)
            self.setCurrentIndex(self.model().index(destination_row, 0))

    def currentChanged(self, current, previous):
        """Updates the Sequencer State with the current selected module.

        Parameters
        ----------
        current : ActionItem
            current selected item
        previous : ActionItem
            previous selected item

        """
        super(ImportListView, self).currentChanged(current, previous)
        item = self.model().itemFromIndex(current)
        try:
            SequencerState.module = item.data(ActionItemDataRole.ModuleRole)
        except AttributeError:
            SequencerState.module = None


class VariableTableWidget(TreePropertyBrowser):
    """A PropertyBrowser containing all declared variables in the Sequencer Menu.

    Parameters
    ----------
    model : ActionItemModel
        The model.
    parent : QWidget
        Parent GUI container.

    """
    def __init__(self, parent=None, model=None):
        super(VariableTableWidget, self).__init__(parent)
        self._parent = None
        self.setAcceptDrops(True)
        self._edit_enabled = True
        if not model:
            model = ActionItemModel(self)
        self._action_model = model
        self._model = OrderedDict()
        self.connect_signals()
        self.set_model(model)

    def connect_signals(self):
        super(VariableTableWidget, self).connect_signals()
        self.currentItemChanged.connect(self.set_current_object)

    def disconnect_signals(self):
        super(VariableTableWidget, self).disconnect_signals()
        self.currentItemChanged.disconnect(self.set_current_object)

    def set_parent(self, parent):
        """Sets the parent widget.

        Parameters
        ----------
        parent : QWidget
            Parent GUI container.

        """
        self._parent = weakref.proxy(parent)

    def model(self):
        """Gets the ActionItemModel.

        Returns
        -------
        OrderedDict
            The model.

        """
        return self._model

    def set_model(self, model, expanded=False):
        """Sets the model.

        Parameters
        ----------
        model : ActionItemModel
            The model.

        """
        _model = {}
        for row in range(model.rowCount()):
            name = model.item(row).data(ActionItemDataRole.UserRole)
            _model[name] = model.item(row).data(ActionItemDataRole.ObjectRole.value)
        if _model is not None:
            self.disconnect_signals()
            self.clear()
            self._model = _model
            self._action_model = model
            property_ = self.add_property("model", _model)
            property_.setPropertyName(_model.__class__.__name__)
            item = self.addProperty(property_)
            if isinstance(item, QtBrowserItem):
                for child_item in item.children():
                    self.setExpanded(child_item, expanded)
            self.connect_signals()

    def action_model(self):
        """Gets the PropertyBrowser model

        Returns
        -------
        ActionItemModel
            The model.

        """
        return self._action_model

    def clear(self):
        """Clears the Model.
        """
        super(VariableTableWidget, self).clear()
        self.property_values_map.clear()
        self._model.clear()
        self._action_model.clear()

    def slot_set_value(self, property_, value, model=False):
        """Sets an attribute value of the current selected variable.

        Parameters
        ----------
        property_ : QtProperty
            Current selected variable attribute.
        value : object
            new value.

        """
        if self._edit_enabled and SequencerState.variable:
            item = self._action_model.findItems(SequencerState.variable_name)[0]
            name = property_.propertyName()
            py_code = item.data(ActionItemDataRole.CodeRole)
            code_changed = False
            for py_sub_code in py_code:
                if py_sub_code[0] == SequencerState.variable_name + "." + name:
                    py_sub_code[1] = str(value)
                    code_changed = True
            if not code_changed:
                py_sub_code = [SequencerState.variable_name + "." + name, str(value)]
                py_code.append(py_sub_code)
            item.setData(py_code, ActionItemDataRole.CodeRole)
            super().slot_set_value(property_, value, model=self.model())

    def slot_set_range(self, property_, min_, max_, model=None):
        """Sets an attribute min/max range of the current selected variable.

        Parameters
        ----------
        property_ : QtProperty
            Current selected variable attribute.
        min_ : float
            minimum value.
        max_ : float
            maximum value.

        """
        if self._edit_enabled and SequencerState.variable:
            super().slot_set_range(property_, min_, max_, model=SequencerState.variable)

    def slot_set_pk_avg(self, property_, pk_avg, model=None):
        """Sets an attribute pk/average display value of the current selected variable.

        Parameters
        ----------
        property_ : QtProperty
            Current selected variable attribute.
        pk_avg : PkAvg
            Pk or Avg.

        """
        if self._edit_enabled and SequencerState.variable:
            super().slot_set_pk_avg(property_, pk_avg, model=SequencerState.variable)

    def slot_set_check(self, property_, display, model=None):
        """Sets an attribute check value of the current selected variable.

        Parameters
        ----------
        property_: QtProperty
            Current selected variable attribute.
        check : bool
            The user-defined check-box value.

        """
        if self._edit_enabled and SequencerState.variable:
            super().set_check(property_, display, model=SequencerState.variable)

    def keyPressEvent(self, event):
        super(VariableTableWidget, self).keyPressEvent(event)
        if event.key() == Qt.Key_Delete:
            browser_item = self.currentItem()
            if browser_item and not browser_item.parent():
                name = browser_item.property().propertyName()
                item = self._action_model.findItems(name)
                if not item:
                    raise KeyError("No Item with text %s, found in VariableTreeWidget", name)
                obj = item[0].data(ActionItemDataRole.ObjectRole)
                sequence_model = self._parent.sequencerFrame.sequenceTreeView.model()
                for index in range(sequence_model.rowCount()):
                    py_object = sequence_model.item(index).data(ActionItemDataRole.ObjectRole)
                    if py_object == obj:
                        QMessageBox.critical(self, 'Unable to remove variable',
                                                   'Unable to remove variable.\n' +
                                                   'An existing action depends on the selected variable.')
                        return
                self.action_model().removeRow(item[0].row())
                self._model.pop(name)
                self.removeProperty(browser_item.property())
                self._parent.update(preview=True)

    def dragEnterEvent(self, event):
        if event.possibleActions() & Qt.CopyAction:
            item = pickle.loads(event.mimeData().data("action/item").data())
            if item.data(ActionItemDataRole.TypeRole) == ActionItemDataType.Class:
                event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        super(VariableTableWidget, self).dropEvent(event)
        if event.dropAction() & Qt.CopyAction:
            row = self.action_model().rowCount()
            item = pickle.loads(event.mimeData().data("action/item").data())
            class_obj = item.data(ActionItemDataRole.ObjectRole)
            if SequencerState.module != inspect.getmodule(class_obj):
                QMessageBox.critical(self, 'Incorrect module selection in "Imports" list',
                                           'Module of dropped class is not selected in "Imports" List.\n' +
                                           'Please select the correct module in the "Imports" list.')
                return
            import_model = self._parent.sequencerFrame.importListView.model()
            locals_dict = {}
            for index in range(import_model.rowCount()):
                full_name = import_model.item(index).data(ActionItemDataRole.UserRole)
                locals_dict[full_name[full_name.rfind('.')+1:]] = None
            locals_dict.update(self.model())
            dialog = ObjectDialog(class_obj, parent=self, locals_=locals_dict)
            if dialog.exec_():
                name = dialog.return_argument_text
                obj = class_obj(*dialog.arguments)
                info = obj.info if hasattr(obj, "info") else Info("untitled", write=True, check=True)
                py_code = item.data(ActionItemDataRole.CodeRole)
                py_code[0][0] = name
                py_code[0][1] += "(" + ", ".join(dialog.arguments_text) + ")"
                item.setData(name, ActionItemDataRole.DisplayRole)
                item.setData(name, ActionItemDataRole.UserRole)
                item.setData(obj, ActionItemDataRole.ObjectRole)
                item.setData(py_code, ActionItemDataRole.CodeRole)
                item.setData(ActionItemDataType.Object, ActionItemDataRole.TypeRole)
                self._model[name] = obj
                self._edit_enabled = False
                try:
                    property_ = self.add_property(name, obj, info, self.properties()[0])
                finally:
                    self._edit_enabled = True
                browser_item = self.items(property_)[0]
                if isinstance(browser_item, QtBrowserItem):
                    self.setCurrentItem(browser_item)
                    self.setExpanded(browser_item, False)
                if row >= 0:
                    self.action_model().insertRow(row, item)
                else:
                    self.action_model().appendRow(item)
                self._parent.update(preview=True)

    def set_current_object(self, browser_item):
        """Updates the Sequencer State with the current selected variable.

        Parameters
        ----------
        current : QtBrowserItem
            current selected item

        """
        try:
            while browser_item.parent():
                child_item = browser_item
                browser_item = browser_item.parent()
            browser_item = child_item
        except AttributeError:
            SequencerState.variable = None
            SequencerState.variable_name = ""
        else:
            name = browser_item.property().propertyName()
            SequencerState.variable = self._model[name]
            SequencerState.variable_name = name

    def update(self, frame=None):
        """Updates the variable property browser.

        If sequencer is running (and a breakpoint is reached), the local variables in the current frame are displayed, otherwise the property browser only contains the variables that were manually declared by the user.

        Parameters
        ----------
        frame : frame
            Current frame provided by the debugger.

        """
        super(VariableTableWidget, self).update()
        if frame:
            try:
                self._edit_enabled = False
                model = frame.f_locals.items()
                for k, v in model:
                    if k not in self._model and k[0] != '_':
                        type_found = False
                        for type_, manager in self._id_manager_map.items():
                            if isinstance(v, type_):
                                manager = self._id_manager_map[type_]
                                property_ = manager.addProperty(k)
                                manager.set_value(property_, v)
                                item = self.addProperty(property_)
                                self.setExpanded(item, False)
                                type_found = True
                                break
                        if not type_found:
                            warn("Unsupported type: %s, found in %s.%s" % (type(v), type(model), k))
            finally:
                self._edit_enabled = True
        self.render()


class SequenceTreeView(QTreeView):
    """A Tree View containing all defined function calls in the Sequencer Menu.

    Parameters
    ----------
    model : ActionItemModel
        The model.
    parent : QWidget
        Parent GUI container.

    """
    def __init__(self, parent=None, model=None):
        super(SequenceTreeView, self).__init__(parent)
        self._parent = None
        self._breakpoint_radius = self.fontMetrics().height()
        self._gap_width = 3
        self._line_number_area = LineNumberArea(self)
        self._breakpoints = set()
        self.breakpoint_offset = 0
        self._active_breakpoint = -1
        self.drag_start_position = QPoint(0, 0)
        if not model:
            model = ActionItemModel(self)
        self.setModel(model)

    def set_parent(self, parent):
        """Sets the parent widget.

        Parameters
        ----------
        parent : QWidget
            Parent GUI container.

        """
        self._parent = weakref.proxy(parent)

    def connect_signals(self, *args, **kwargs):
        self.updateRequest.connect_signals(self.update_line_number_area)

    def disconnect_signals(self, *args, **kwargs):
        self.updateRequest.disconnect_signals(self.update_line_number_area)

    def breakpoints(self):
        """Gets the breakpoint list.

        Returns
        -------
        set
            A list of breakpoint line numbers.

        """
        return self._breakpoints

    def set_breakpoints(self, breakpoints):
        """Sets the breakpoint list.

        Parameters
        ----------
        breakpoints : set
            A list of breakpoint line numbers.

        """
        self._breakpoints = breakpoints
        self._line_number_area.repaint()

    def active_breakpoint(self):
        """Gets the active breakpoint.

        Returns
        -------
        int
            The active breakpoint line number.

        """
        return self._active_breakpoint

    def set_active_breakpoint(self, active_breakpoint):
        """Sets the active breakpoint.

        Parameters
        ----------
        active_breakpoint : int
            The active breakpoint line number.

        """
        self._active_breakpoint = active_breakpoint
        self._line_number_area.repaint()

    def clicked_break_points(self, position):
        """Adds line number closest to position to the breakpoints list.

        Parameters
        ----------
        position : QPoint
            position in the line_number_area where a breakpoint was selected.

        """
        row = self.indexAt(position + QPoint(50, 0)).row()
        if row in self._breakpoints:
            self._breakpoints.remove(row)
        else:
            self._breakpoints.add(row)
        self._line_number_area.repaint()

    def update_line_number_area(self, rect, dy):
        """Updates the line_number_area when the content Scroll Area changes.

        Parameters
        ----------
        rect : QRect
            The rectangle that defines the viewport of the Scroll Area

        """
        if dy:
            self._line_number_area.scroll(0, dy)
        else:
            self._line_number_area.update(0, rect.y(), self._line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def update_line_number_area_width(self, new_block_count):
        self.setContentsMargins(self.line_number_area_width(), 0, 0, 0)

    def line_number_area_width(self):
        return self._gap_width + self._breakpoint_radius + self._gap_width

    def line_number_paint_event(self, event):
        """Paints the line numbers, selected breakpoints, and active breakpoint.
        """
        painter = QPainter(self._line_number_area)
        painter.fillRect(event.rect(), Qt.lightGray)

        index = self.indexAt(self.rect().topLeft())
        row = index.row()
        top = int(self.visualRect(index).top())
        bottom = top + int(self.rowHeight(index))
        radius = self._breakpoint_radius
        gap = self._gap_width
        source_rect = QRect(0, 0, 32, 32)
        while index.isValid() and top <= event.rect().bottom():
            if bottom >= event.rect().top():
                if row in self._breakpoints:
                    rect = QRect(self._line_number_area.width() - radius - gap, top, 2*radius, 2*radius)
                    painter.drawPixmap(rect, QPixmap(":PNG/32/red/form_oval.png"), source_rect)
                if row == self._active_breakpoint:
                    rect = QRect(self._line_number_area.width() - radius - gap, top, 2*radius, 2*radius)
                    painter.drawPixmap(rect, QPixmap(":PNG/32/green/arrow-right.png"), source_rect)
            index = self.indexBelow(index)
            top = bottom
            bottom = top + int(self.rowHeight(index))
            row += 1

    def mousePressEvent(self, event):
        super(SequenceTreeView, self).mousePressEvent(event)
        if not (event.buttons() and Qt.LeftButton):  # if not left button
            return
        self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        super(SequenceTreeView, self).mouseMoveEvent(event)
        if not (event.buttons() and Qt.LeftButton):  # if not left button
            return
        if not self.currentIndex():  # if no item selected
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = self.model().mimeData(self.currentIndex())
        drag.setMimeData(mime_data)
        drag.start(Qt.MoveAction)

    def mouseDoubleClickEvent(self, event):
        super(SequenceTreeView, self).mouseDoubleClickEvent(event)
        if not (event.buttons() and Qt.LeftButton):  # if not left button
            return
        if not self.currentIndex():  # if no item selected
            return
        row = self.indexAt(event.pos()).row()
        item = self.model().itemFromIndex(self.currentIndex())
        member_obj = item.data(ActionItemDataRole.ObjectRole)
        py_code = item.data(ActionItemDataRole.CodeRole)
        method_name = item.data(ActionItemDataRole.UserRole)
        if inspect.isroutine(member_obj):
            func_obj = member_obj
        else:
            func_obj = getattr(item.data(ActionItemDataRole.ObjectRole), method_name)

        import_model = self._parent.sequencerFrame.importListView.model()
        variable_model = self._parent.sequencerFrame.variableTableWidget.model()
        locals_dict = {}
        for index in range(import_model.rowCount()):
            full_name = import_model.item(index).data(ActionItemDataRole.UserRole)
            locals_dict[full_name[full_name.rfind('.')+1:]] = None
        locals_dict.update(variable_model)
        bracket = py_code[0][1].find("(")
        existing_arguments = py_code[0][1][bracket+1:-1].split(", ")
        dialog = ObjectDialog(func_obj, parent=self, locals_=locals_dict, existing_arguments=existing_arguments)
        if dialog.exec_():
            py_code[0][0] = dialog.return_argument_text
            py_code[0][1] = py_code[0][1][0:bracket] + "(" + ", ".join(dialog.arguments_text) + ")"
            item.setData(py_code, ActionItemDataRole.CodeRole)
            self.model().setItem(row, item)

    def keyPressEvent(self, event):
        super(SequenceTreeView, self).keyPressEvent(event)
        if event.key() == Qt.Key_Delete:
            item = self.model().itemFromIndex(self.currentIndex())
            if item:
                row = self.currentIndex().row()
                breakpoints = self.breakpoints()
                self.model().removeRow(self.currentIndex().row())
                if row in breakpoints:
                    breakpoints.remove(row)
                self.set_breakpoints(set(breakpoint - 1 for breakpoint in breakpoints if breakpoint > row))

    def dragEnterEvent(self, event):
        # super(SequenceTreeView, self).dragEnterEvent(event) accepts everything
        if event.source() == self and event.possibleActions() & Qt.MoveAction:
            event.acceptProposedAction()
        elif event.possibleActions() & Qt.CopyAction:
            item = pickle.loads(event.mimeData().data("action/item").data())
            role = item.data(ActionItemDataRole.TypeRole)
            if role == ActionItemDataType.Method or role == ActionItemDataType.Function:
                event.acceptProposedAction()

    def dropEvent(self, event):
        # super(SequenceTreeView, self).dropEvent(event) causes seg fault
        if event.dropAction() == Qt.CopyAction:
            row = self.indexAt(event.pos()).row()
            item = pickle.loads(event.mimeData().data("action/item").data())
            member_obj = item.data(ActionItemDataRole.ObjectRole)
            py_code = item.data(ActionItemDataRole.CodeRole)
            if inspect.isclass(member_obj):  # Method, Static Method, Class Method
                method_name = item.data(ActionItemDataRole.UserRole)
                method_obj = getattr(member_obj, method_name)
                if isinstance(method_obj, staticmethod):
                    py_code[0][1] = member_obj.__name__ + "." + py_code[0][1]
                else:  # Method
                    if SequencerState.variable.__class__ != member_obj:
                        QMessageBox.critical(self, 'Incorrect variable selection in "Variables" list',
                                                   'Object of dropped method is not selected in "Variables" List.\n' +
                                                   'Please select the correct object in the "Variables" list.')
                        return
                    py_code[0][1] = SequencerState.variable_name + "." + py_code[0][1]
                    item.setData(SequencerState.variable, ActionItemDataRole.ObjectRole)
                item.setData(py_code[0][1], ActionItemDataRole.DisplayRole)
                item.setData(method_name, ActionItemDataRole.UserRole)
                func_obj = getattr(item.data(ActionItemDataRole.ObjectRole), method_name)
            else:  # Function
                func_obj = member_obj
            import_model = self._parent.sequencerFrame.importListView.model()
            variable_model = self._parent.sequencerFrame.variableTableWidget.model()
            locals_dict = {}
            for index in range(import_model.rowCount()):
                full_name = import_model.item(index).data(ActionItemDataRole.UserRole)
                locals_dict[full_name[full_name.rfind('.')+1:]] = None
            locals_dict.update(variable_model)
            dialog = ObjectDialog(func_obj, parent=self, locals_=locals_dict)
            if dialog.exec_():
                py_code[0][0] = dialog.return_argument_text
                bracket = py_code[0][1].find("(")
                py_code[0][1] = py_code[0][1][0:bracket] + "(" + ", ".join(dialog.arguments_text) + ")"
                item.setData(py_code, ActionItemDataRole.CodeRole)
                if row >= 0:
                    self.model().insertRow(row, item)
                    self.setCurrentIndex(self.model().index(row, 0))
                else:
                    self.model().appendRow(item)
                    self.setCurrentIndex(self.model().index(self.model().rowCount()-1, 0))
        else:
            destination_row = self.indexAt(event.pos()).row()
            if destination_row < 0:
                destination_row = self.model().rowCount() - 1
            source_row = self.currentIndex().row()
            moved_item = self.model().takeItem(source_row)
            self.model().removeRow(source_row)
            self.model().insertRow(destination_row, moved_item)
            self.setCurrentIndex(self.model().index(destination_row, 0))

    def resizeEvent(self, event):
        super(SequenceTreeView, self).resizeEvent(event)

        cr = self.contentsRect()
        self._line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))
