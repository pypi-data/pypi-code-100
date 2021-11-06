import importlib
import inspect
import logging
import pkgutil
import sys

from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QColor
from PySide2.QtWidgets import QDialog, QMessageBox, QFrame, QAbstractItemView, QHeaderView, QTableWidgetItem

from sknrf.settings import Settings
from sknrf.model import transform as transform_pkg
from sknrf.model.transform.base import AbstractTransform
from sknrf.view.desktop.base import BusyFrame
from sknrf.view.desktop.sideview.base import AbstractSideView
from sknrf.view.desktop.transform.QTransformDialog import Ui_transformDialog
from sknrf.view.desktop.transform.QTransformFrame import Ui_transformFrame
from sknrf.icons.transforms_rc import *

from sknrf.widget.propertybrowser.view.enums import DISPLAY
from sknrf.widget.propertybrowser.view import BrowserCol, QtBrowserItem

logger = logging.getLogger(__name__)


class TransformDialog(QDialog, Ui_transformDialog):

    selected_transform = QtCore.Signal()

    def __init__(self, transform_package, parent=None, model=None):
        super(TransformDialog, self).__init__(parent=parent)
        self.setupUi(self)

        self.transform_package = transform_package
        self.transform_map = {}
        self.update_transform_map()
        transform_list = list(self.transform_map.keys())
        self.transformComboBox.addItems(transform_list)

        self.value_manager_map, self.value_factory_map = None, None
        self._model = None

        if model is None:
            model = AbstractTransform("unknown", (1,))
        self.connect_signals()
        self.transformTable.property_browser.display = DISPLAY.PUBLIC
        self.transformTable.property_browser.setAttributes([BrowserCol.UNIT, BrowserCol.PKAVG, BrowserCol.FORMAT])
        self.transformTable.property_browser.set_update(self.update,  **{"value": True})
        self.set_model(model)

    def connect_signals(self, *args, **kwargs):
        self.transformComboBox.currentIndexChanged[str].connect(self.select_transform)

    def disconnect_signals(self, *args, **kwargs):
        self.transformComboBox.currentIndexChanged[str].disconnect(self.select_transform)

    def update_transform_map(self):
        """Updates the transform list based on the contents of the transform_package folder.
        """
        transform_map = {}
        package = self.transform_package
        base_class = AbstractTransform
        for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__,
                                                              prefix=package.__name__+'.',
                                                              onerror=lambda x: None):
            module = importlib.import_module(modname)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) \
                        and not inspect.isabstract(obj) \
                        and base_class in inspect.getmro(obj)\
                        and not name.startswith("_"):
                    transform_map[name] = module
        self.transform_map = transform_map

    def model(self):
        return self._model

    def set_model(self, model):
        self.disconnect_signals()

        self._model = model
        combo = self.transformComboBox
        combo.setCurrentIndex(combo.findText(self._model.__class__.__name__))
        img = QPixmap(model._preview_filename).scaled(400, 200, Qt.KeepAspectRatio)
        self.previewLabel.setPixmap(img)
        property_browser = self.transformTable.property_browser
        property_browser.set_model(self._model)
        self.connect_signals()

    def select_transform(self, transform_name):
        driver = getattr(self.transform_map[transform_name], transform_name)
        with BusyFrame(self.transformTable, self.selected_transform,  "Selecting Transform..."):
            try:
                model = driver()
            except Exception:
                logger.error('An error occured while loading the transform: %s.' \
                                           % (transform_name,), exc_info=True)
                QMessageBox.critical(self, 'Unable to select transform',
                                           'An error occured while loading the transform: %s.' \
                                           % (transform_name,))
                combo = self.transformComboBox
                combo.setCurrentIndex(combo.findText(self.transform_package.default_transform.__name__))
            else:
                self.set_model(model)
            finally:
                self.selected_transform.emit()

    def reject(self):
        self._model = None
        super(TransformDialog, self).reject()

    def update(self, value=False):
        super(TransformDialog, self).update()
        all_ = not(value)

        if value or all_:
            self.transformTable.property_browser.render()


class TransformSideView(QFrame, AbstractSideView, Ui_transformFrame):

    def __init__(self, parent=None, model=None):
        super(TransformSideView, self).__init__(parent=parent)
        self.setupUi(self)
        self.transformTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.transformTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.transformTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self._model = []
        if model is None:
            model = []

        self.connect_signals()
        self.set_model(model)

    def connect_signals(self):
        self.addButton.clicked.connect(self.add_transform)
        self.removeButton.clicked.connect(self.remove_transform)
        self.upButton.clicked.connect(self.shift_transform_up)
        self.downButton.clicked.connect(self.shift_transform_down)
        self.transformTable.currentCellChanged.connect(self.current_changed)

    def disconnect_signals(self):
        self.addButton.clicked.disconnect(self.add_transform)
        self.removeButton.clicked.disconnect(self.remove_transform)
        self.upButton.clicked.disconnect(self.shift_transform_up)
        self.downButton.clicked.disconnect(self.shift_transform_down)
        self.transformTable.currentCellChanged.disconnect(self.current_changed)

    def set_model(self, model):
        self.disconnect_signals()
        super(TransformSideView, self).set_model(model)
        self.transformTable.clear()
        for col in reversed(range(self.transformTable.columnCount())):
            self.transformTable.removeColumn(col)
        for row in reversed(range(self.transformTable.rowCount())):
            self.transformTable.removeRow(row)
        self.transformTable.insertColumn(0)
        item = QTableWidgetItem()
        item.setText("Calkits")
        self.transformTable.setHorizontalHeaderItem(0, item)
        for port_num in range(Settings().num_ports):
            port_num += 1
            self.transformTable.insertColumn(port_num)
            item = QTableWidgetItem()
            item.setText("Port %s" % str(port_num))
            self.transformTable.setHorizontalHeaderItem(port_num, item)
        self.current_changed(-1, -1, -1, -1)
        row = 0
        transforms = self._model.device_model().transforms
        for transform in transforms:
            self.transformTable.insertRow(row)
            for col in range(self.transformTable.columnCount()):
                item = QTableWidgetItem()
                if col in transform.ports:
                    item.setText(transform.name)
                    item.setBackground(QColor(transform.color()))
                    self.transformTable.setItem(row, col, item)
                else:
                    item.setBackground(QColor(Settings().color_map["white"]))
                    self.transformTable.setItem(row, col, item)
            row += 1
        self._model.device_model().stimulus()
        self.transformTable.selectRow(row-1)
        self.connect_signals()

    def add_transform(self):
        dialog = TransformDialog(transform_pkg, parent=self, model=None)
        transforms = self._model.device_model().transforms
        if dialog.exec_():
            transform = dialog.model()
            transform.name = transforms.mangle(transform.name)
            if transform:
                row = self.transformTable.currentRow()
                self.transformTable.insertRow(row+1)
                for col in range(self.transformTable.columnCount()):
                    item = QTableWidgetItem()
                    if col in transform.ports:
                        item.setText(transform.name)
                        item.setBackground(QColor(transform.color()))
                        self.transformTable.setItem(row+1, col, item)
                    else:
                        item.setBackground(QColor(Settings().color_map["white"]))
                        self.transformTable.setItem(row+1, col, item)
                transforms.insert(row+1, transform.name, transform)
                self.transformTable.selectRow(row+1)
                self._model.device_model().stimulus()
                self.update_window()

    def remove_transform(self):
        row = self.transformTable.currentRow()
        self._model.device_model().transforms[row].release()
        del self._model.device_model().transforms[row]
        self.transformTable.removeRow(row)
        self._model.device_model().stimulus()
        if row > 0:
            self.transformTable.selectRow(row - 1)
            self.update_window()

    def shift_transform_up(self):
        row = self.transformTable.currentRow()
        transforms = self._model.device_model().transforms
        if row > 0:
            for col in range(self.transformTable.columnCount()):
                first_item = self.transformTable.takeItem(row-1, col)
                second_item = self.transformTable.takeItem(row, col)
                self.transformTable.setItem(row-1, col, second_item)
                self.transformTable.setItem(row, col, first_item)
            temp = transforms[row-1]
            transforms[row-1] = transforms[row]
            transforms[row] = temp
            self.transformTable.selectRow(row - 1)
            self._model.device_model().stimulus()
            self.update_window()

    def shift_transform_down(self):
        row = self.transformTable.currentRow()
        transforms = self._model.device_model().transforms
        if row < self.transformTable.rowCount()-1:
            for col in range(self.transformTable.columnCount()):
                second_item = self.transformTable.takeItem(row+1, col)
                first_item = self.transformTable.takeItem(row, col)
                self.transformTable.setItem(row+1, col, first_item)
                self.transformTable.setItem(row, col, second_item)
            temp = transforms[row+1]
            transforms[row+1] = transforms[row]
            transforms[row] = temp
            self.transformTable.selectRow(row + 1)
            self._model.device_model().stimulus()
            self.update_window()

    def keyPressEvent(self, event):
        super(TransformSideView, self).keyPressEvent(event)
        if event.key() == Qt.Key_Delete:
            self.remove_transform()

    def current_changed(self, current_row, current_col, previous_row, previous_col):
        if current_row < 0:
            self.removeButton.setEnabled(False)
            self.infoButton.setEnabled(False)
            self.upButton.setEnabled(False)
            self.downButton.setEnabled(False)
            return
        self.removeButton.setEnabled(True)
        self.infoButton.setEnabled(True)
        self.upButton.setEnabled(current_row > 0)
        self.downButton.setEnabled(current_row < self.transformTable.rowCount() - 1)

    def update(self, table=False):
        super(TransformSideView, self).update()
        all_ = not (table)

        if table or all_:
            self.set_model(self._model)
            self.current_changed(self.transformTable.currentRow(), self.transformTable.currentColumn(), 0, 0)


if __name__ == "__main__":
    from PySide2.QtWidgets import QApplication
    app = QApplication(sys.argv)
    Settings().t_step = 1e-9
    Settings().t_stop = 10e-9
    form = TransformSideView()
    form.show()
    app.exec_()