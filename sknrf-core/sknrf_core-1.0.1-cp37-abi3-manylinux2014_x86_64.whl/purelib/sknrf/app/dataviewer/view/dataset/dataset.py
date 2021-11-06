import re

from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtGui import QTextCursor
from PySide2.QtWidgets import QDialog, QMessageBox, QFrame, QTextEdit, QCompleter

from sknrf.app.dataviewer.model.equation import DatasetEquationModel
from sknrf.utilities import numeric
from sknrf.app.dataviewer.view.equation.QDatasetEquationFrame import Ui_datasetEquationFrame
from sknrf.app.dataviewer.view.equation.QEquationDialog import Ui_equationDialog
from sknrf.widget.propertybrowser.view.base import PropertyScrollArea
from sknrf.widget.propertybrowser.view.enums import DISPLAY

from sknrf.widget.propertybrowser.view import BrowserCol, QtBrowserItem

__author__ = 'dtbespal'


class EquationLineEdit(QTextEdit):

    editingFinished = QtCore.Signal()

    def __init__(self, parent=None):
        super(EquationLineEdit, self).__init__(parent=parent)
        self._completer = None

    def completer(self):
        return self._completer

    def setCompleter(self, completer):
        if self._completer:
            self._completer.disconnect(self)
        if not completer:
            return
        completer.setWidget(self)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.activated.connect(self.insertCompletion)
        self._completer = completer

    def keyPressEvent(self, event):
        if self._completer and self._completer.popup().isVisible():
            if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
                event.ignore()
                return
        is_shortcut = (event.modifiers() &  Qt.ControlModifier) and event.key() == Qt.Key_E  # CTRL + E
        if not self._completer or  not is_shortcut:
            super(EquationLineEdit, self).keyPressEvent(event)
        eqn = self.toPlainText()
        match = re.findall(r"(\.\w*)", eqn)
        if len(match) and eqn.endswith(match[-1]):
            self._completer.setCompletionPrefix(match[-1])
            self._completer.complete()
        elif self._completer.popup().isVisible():
            self._completer.popup().hide()

    def focusInEvent(self, event):
        if self._completer:
            self._completer.setWidget(self)
        super(EquationLineEdit, self).focusInEvent(event)

    def focusOutEvent(self, event):
        super(EquationLineEdit, self).focusOutEvent(event)
        self.editingFinished.emit()

    def insertCompletion(self, completion):
        if self._completer.widget() is not self:
            return
        tc = self.textCursor()
        extra = len(completion) - len(self._completer.completionPrefix())
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[-extra::])
        self.setTextCursor(tc)


class EquationDialog(QDialog, Ui_equationDialog):
    def __init__(self, equation, dataset, parent=None):
        super(EquationDialog, self).__init__(parent=parent)
        self.setupUi(self)
        self.equationLineEdit = EquationLineEdit(self.equationFrame)
        self.gridLayout.addWidget(self.equationLineEdit, 1, 1, 1, 1)
        self.equation = equation
        self._eqn = ""
        self.dataset = dataset
        self._value = None
        self._name_is_valid = False
        self._equation_is_valid = False
        self._unit_is_valid = False
        self._equation_names = list(self.dataset._v_children.keys())
        try:
            self._equation_names.remove(self.equation.name)
        except ValueError:
            self._new_equation = True
        else:
            self._new_equation = False
        self._equation_handles = ['.{0}'.format(i) for i in self._equation_names]

        self.nameLineEdit.setText(self.equation.name)
        self.equationLineEdit.setText(self.equation.eqn)
        completer = QCompleter(self._equation_handles)
        self.equationLineEdit.setCompleter(completer)
        self.unitLineEdit.setText("")

        self.name_edit_finished()
        self.equation_edit_finished()
        self.unit_edit_finished()
        self.connect_signals()

    def connect_signals(self):
        self.nameLineEdit.editingFinished.connect(self.name_edit_finished)
        self.equationLineEdit.editingFinished.connect(self.equation_edit_finished)
        self.unitLineEdit.editingFinished.connect(self.unit_edit_finished)

    def disconnect_signals(self):
        self.nameLineEdit.editingFinished.disconnect(self.name_edit_finished)
        self.equationLineEdit.editingFinished.disconnect(self.equation_edit_finished)
        self.unitLineEdit.editingFinished.disconnect(self.unit_edit_finished)

    def name_edit_finished(self):
        name = self.nameLineEdit.text()

        if name in self._equation_names:
            self.nameLineEdit.setStyleSheet("border: 3px solid red")
            self._name_is_valid = False
        else:
            if not self._new_equation:
                self.dataset.rename(self.equation.name, name)
            self.nameLineEdit.setStyleSheet("")
            self.equation.name = name
            self._name_is_valid = True

    def equation_edit_finished(self):
        try:
            self._value = self.equation.eval(self.dataset, eqn=self.equationLineEdit.toPlainText())
        except (SyntaxError, TypeError, NameError, AttributeError, ValueError) as e:
            self.equationLineEdit.setStyleSheet("border: 3px solid red")
            self._equation_is_valid = False
            QMessageBox.critical(self, 'Dataset Equation Error',
                                       "Invalid Equation: %s = %s\n%s: %s"\
                                       % (self.equation.name, self.equation.eqn, str(type(e)), str(e)))
        else:
            self.equationLineEdit.setStyleSheet("")
            self._equation_is_valid = True

    def unit_edit_finished(self):
        unit = self.unitLineEdit.text()
        if len(unit) and unit[0] in list(numeric.STR2NUM_SCALE.keys()):
            self.unitLineEdit.setStyleSheet("border: 3px solid red")
            self._unit_is_valid = False
        else:
            self.unitLineEdit.setStyleSheet("")
            self._unit_is_valid = True

    def accept(self):
        if self.focusWidget() == self.nameLineEdit:
            self.name_edit_finished()
        elif self.focusWidget() == self.equationLineEdit:
            self.equation_edit_finished()
        elif self.focusWidget() == self.unitLineEdit:
            self.unit_edit_finished()
        if self._name_is_valid and self._equation_is_valid and self._unit_is_valid:
            if hasattr(self.dataset, self.equation.name):
                self.dataset.set_equation(self.equation.name, self._value)
            else:
                self.dataset.add(self.equation.name, self._value)
            self.done(QDialog.DialogCode.Accepted)


class DatasetEquationView(QFrame, Ui_datasetEquationFrame):
    """Interactive control over dataset equation.

    The default equations (v, i, z for each port) in the selected dataset model are displayed and cannot be modified.

    Additional user-defined equations can be added using the following actions:
        * Add an "Untitled" equation to the dataset.
        * Remove an existing equation (the default equations cannot be removed).
        * Change the order of the equation display

        Args:
            model (DatasetModel): A Dataset Model containing the dataset equations to be displayed.

        Keyword Args:
            parent (QWidget): Parent GUI container
    """
    def __init__(self, model, parent=None):
        super(DatasetEquationView, self).__init__(parent)
        self.setupUi(self)
        self._model = None
        self._equation_map = dict()

        self.connect_signals()
        self.propertyTable.property_browser.display = DISPLAY.PUBLIC
        self.propertyTable.property_browser.setAttributes([BrowserCol.UNIT, BrowserCol.PKAVG, BrowserCol.FORMAT])
        self.propertyTable.property_browser.set_update(self.update, **{"value": True})
        self.set_model(model)

    def connect_signals(self):
        self.addButton.clicked.connect(self.add_equation)
        self.removeButton.clicked.connect(self.remove_equation)
        self.infoButton.clicked.connect(self.equation_settings)
        self.upButton.clicked.connect(self.shift_equation_up)
        self.downButton.clicked.connect(self.shift_equation_down)

    def disconnect_signals(self):
        self.addButton.clicked.disconnect(self.add_equation)
        self.removeButton.clicked.disconnect(self.remove_equation)
        self.infoButton.clicked.disconnect(self.equation_settings)
        self.upButton.clicked.disconnect(self.shift_equation_up)
        self.downButton.clicked.disconnect(self.shift_equation_down)

    def model(self):
        return self._model

    def set_model(self, model):
        self._model = model
        property_browser = self.propertyTable.property_browser
        property_browser.set_model(self._model)
        self.update()

    def set_equation(self, property_, equation_str):
        name = property_.propertyName()
        try:
            value = self._equation_map[name].eval(self._model, eqn=equation_str)
        except (SyntaxError, NameError, AttributeError, ValueError) as e:
            value = 0
            QMessageBox.critical(self, 'Dataset Equation Error',
                                       "Invalid Equation: %s = %s\n%s: %s"\
                                       % (name, equation_str, str(type(e)), e.message))
        finally:
            self._model.set_equation(name, value)
            self.update()

    def add_equation(self):
        equation = DatasetEquationModel(self._model)
        dialog = EquationDialog(equation, self._model, parent=self)
        if dialog.exec_():
            name = equation.name
            value = getattr(self._model, name)
            self._equation_map[name] = equation
            property_ = PropertyBrowser._add_property(self.propertyTable.property_browser._manager_map, self.propertyTable.property_browser._model, name, value, has_info=False)
            browser_item = self.propertyTable.property_browser.currentItem()
            if browser_item and not browser_item.parent():
                self.propertyTable.property_browser.insertProperty(property_, browser_item.property())
            else:
                self.propertyTable.property_browser.insertProperty(property_, None)
            self.update()

    def remove_equation(self):
        browser_item = self.propertyTable.property_browser.currentItem()
        if browser_item and not browser_item.parent():
            name = browser_item.property().propertyName()
            try:
                self._model.remove(name)
            except AttributeError:
                QMessageBox.critical(self, 'Dataset Equation Error', "Unable to remove equation: %s" % (name, ))
            else:
                self.propertyTable.property_browser.removeProperty(browser_item.property())

    def equation_settings(self):
        browser_item = self.propertyTable.property_browser.currentItem()
        if browser_item and not browser_item.parent():
            property_ = browser_item.property()
            name = property_.propertyName()
            if name in self._model._v_attrs.signal_lock:
                QMessageBox.critical(self, 'Dataset Equation Error',
                                           'Unable to modify locked signals.\n')
            else:
                equation = self._equation_map[name]
                dialog = EquationDialog(equation, self._model, parent=self)
                if dialog.exec_():
                    if equation.name != name:
                        self._equation_map.pop(name)
                        name = equation.name
                        property_.setPropertyName(name)
                    self._equation_map[name] = equation
                    self.update()

    def shift_equation_up(self):
        browser_item = self.propertyTable.property_browser.currentItem()
        if browser_item and not browser_item.parent():
            browser_items = self.propertyTable.property_browser.topLevelItems()
            current_index = browser_items.index(browser_item)
            is_expanded = self.propertyTable.property_browser.isExpanded(browser_item)
            property_ = browser_item.property()
            if current_index > 1:
                previous_property = browser_items[current_index-2].property()
            else:
                previous_property = None
            self.propertyTable.property_browser.removeProperty(property_)
            browser_item = self.propertyTable.property_browser.insertProperty(property_, previous_property)
            self.propertyTable.property_browser.setExpanded(browser_item, is_expanded)
            self.propertyTable.property_browser.setCurrentItem(browser_item)

    def shift_equation_down(self):
        browser_item = self.propertyTable.property_browser.currentItem()
        if browser_item and not browser_item.parent():
            browser_items = self.propertyTable.property_browser.topLevelItems()
            current_index = browser_items.index(browser_item)
            is_expanded = self.propertyTable.property_browser.isExpanded(browser_item)
            property_ = browser_item.property()
            if current_index < len(browser_items)-1:
                next_property = browser_items[current_index+1].property()
                self.propertyTable.property_browser.removeProperty(property_)
                browser_item = self.propertyTable.property_browser.insertProperty(property_, next_property)
                self.propertyTable.property_browser.setExpanded(browser_item, is_expanded)
                self.propertyTable.property_browser.setCurrentItem(browser_item)

    def keyPressEvent(self, event):
        super(DatasetEquationView, self).keyPressEvent(event)
        if event.key() == Qt.Key_Delete:
            self.remove_equation()

    def update(self, value=False):
        super(DatasetEquationView, self).update()
        all_ = not value

        if value or all_:
            for name in DatasetEquationModel._eval_order:
                self._model.set_equation(name, self._equation_map[name].eval(self._model))
            # self.propertyTable.property_browser.render()


class DatasetView:

    def __init__(self):
        self.dataset_tree = 0
        self.info_table = 0

    @property
    def current_dataset_group(self):
        return ""

    @property
    def current_dataset(self):
        return ""

    def dataset_tree_item_selected(self):
        pass
