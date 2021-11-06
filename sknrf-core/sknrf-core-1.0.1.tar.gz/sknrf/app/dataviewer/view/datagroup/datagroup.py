import importlib
import os
import logging
from collections import OrderedDict

from PySide2 import QtCore
from PySide2.QtCore import Qt, QModelIndex
from PySide2.QtWidgets import QFileDialog, QTreeView, QFrame

from sknrf.settings import Settings
from sknrf.app.dataviewer.model.dataset import DatagroupModel, DatasetModel
from sknrf.app.dataviewer.model.mdif import MDIF
from sknrf.app.dataviewer.model.snp import SNP
from sknrf.app.dataviewer.model.mat import MAT
from sknrf.app.dataviewer.model.spl import SPL
from sknrf.app.dataviewer.model.lpc import LPC
from sknrf.app.dataviewer.model.dataset import DatagroupTreeModel
from sknrf.utilities.error import delta_abs, delta_rel, delta_ratio

from sknrf.app.dataviewer.view.datagroup.QDatagroupFrame import Ui_datagroupFrame

logger = logging.getLogger()


class DatagroupTreeView(QTreeView):

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Delete:
            self.model().removeRows()(e.row())


class DatagroupFrame(QFrame, Ui_datagroupFrame):

    datasetChanged = QtCore.Signal(object)
    def __init__(self, parent=None):
        super(DatagroupFrame, self).__init__(parent=parent)
        self.setupUi(self)

        self._parent = None
        self._datagroup_model = OrderedDict()
        self._import_module_name = ""
        self._import_module = None
        self._import_func = self.nop
        self._datagroup_filename = ""
        self._dataset = None
        self._dataset_marker = ""

        model = DatagroupTreeModel(parent=self)
        self.datagroupTreeView.setModel(model)

    def connect_signals(self):
        self.importLineEdit.returnPressed.connect(self.set_import_module)
        self.importLineEdit.editingFinished.connect(self.update)
        self.importBrowseButton.clicked.connect(self.load_import_module)
        self.datagroupLineEdit.returnPressed.connect(self.set_datagroup_filename)
        self.datagroupLineEdit.editingFinished.connect(self.update)
        self.datagroupBrowseButton.clicked.connect(self.load_datagroup)
        self.datagroupTreeView.clicked.connect(self.set_dataset)

        self.absPushButton.clicked.connect(self.delta_abs)
        self.relPushButton.clicked.connect(self.delta_rel)
        self.ratioPushButton.clicked.connect(self.delta_ratio)
        self.customPushButton.clicked.connect(self.delta_custom)

    def disconnect_signals(self):
        self.importLineEdit.returnPressed.disconnect()
        self.importLineEdit.editingFinished.disconnect()
        self.importBrowseButton.clicked.disconnect()
        self.datagroupLineEdit.returnPressed.disconnect()
        self.datagroupLineEdit.editingFinished.disconnect()
        self.datagroupBrowseButton.clicked.disconnect()
        self.datagroupTreeView.clicked.disconnect()

        self.absPushButton.clicked.disconnect()
        self.relPushButton.clicked.disconnect()
        self.ratioPushButton.clicked.disconnect()
        self.customPushButton.clicked.disconnect()

    @QtCore.Slot()
    def load_import_module(self):
        """ Load the import module that computes pre-defined equations.

            The import module must implement a function called "import_datagroup".
        """
        selected_filter = "Python Files (*.py)"
        filename, filter_ = QFileDialog.getOpenFileName(self, 'Load Import Script', '', filter=selected_filter)
        if filename:
            filename = filename.replace("/", os.sep)
            filename = filename.replace(Settings().root + os.sep, "sknrf" + os.sep)
            filename = filename.replace(".py", "")
            filename = filename.replace(os.sep, ".")
            self.set_import_module(filename)

    @QtCore.Slot()
    def set_import_module(self, module_name=""):
        if not module_name:
            module_name = self.importLineEdit.text()
        try:
            self._import_module = importlib.import_module(module_name)
        except ImportError as e:
            logger.error("Import module could not be loaded")
            raise e
        else:
            if "import_datagroup" in self._import_module.__dict__:
                self._import_func = self._import_module.import_datagroup
                self.importLineEdit.setText(module_name)
                self._import_module_name = module_name
            else:
                logger.error('Import module does not define "import_datagroup()')
                raise AttributeError('Import module does not define "import_datagroup()')

    @QtCore.Slot()
    def load_datagroup(self):
        """Load a datagroup from a file.
        """
        selected_filter = "HDF Files (*.h5);;" + \
                          "MAT Files (*.mat);;" + \
                          "MDIF Files (*.mdf);;" + \
                          "S-Parameters (*.s1p *.s2p *.s3p *.s4p);;" + \
                          "SPL (*.lp);;" + \
                          "LPC (*.lpc, *.lpcwave)"
        filename, filter_ = QFileDialog.getOpenFileName(self, 'Load Datagroup', '', filter=selected_filter)
        if filename:
            self.set_datagroup_filename(filename, filter_=filter_)

    @QtCore.Slot()
    def set_datagroup_filename(self, filename="", filter_="HDF Files (*.h5)"):
        if not filename:
            filename = self.datagroupLineEdit.text()
        try:
            if filter_ == "HDF Files (*.h5)":
                datagroup = DatagroupModel(filename, 'r+')
            elif filter_ == "MAT Files (.mat)":
                datagroup = MAT.import_datagroup(filename)
            elif filter_ == "MDIF Files (*.mdf)":
                datagroup = MDIF.import_datagroup(filename)
            elif filter_ == "S-Parameters (*.s1p *.s2p *.s3p *.s4p)":
                datagroup = SNP.import_datagroup(filename)
            elif filter_ == "SPL (*.lp)":
                datagroup = SPL.import_datagroup(filename)
            elif filter_ == "LPC (*.lpc, *.lpcwave)":
                datagroup = LPC.import_datagroup(filename)
            else:
                logger.error("Unrecognized File Format: %s", filter_)
                raise IOError("Unrecognized File Format: %s", filter_)
        except WindowsError:
            logger.error('Unable to import file: %s', filename)
            raise
        _, name = os.path.split(filename)
        name, _ = os.path.splitext(name)
        datagroup.enable_undo()
        self._import_func(datagroup)
        self._datagroup_filename = filename
        self.datagroupLineEdit.setText(filename)
        self.datagroupTreeView.model().appendRow(name, datagroup, self._datagroup_model)

    @QtCore.Slot(QModelIndex)
    def set_dataset(self, index):
        self.datagroupTreeView.model().set_selected(self.datagroupTreeView.selectedIndexes())
        _, datasets, dataset_markers = self.datagroupTreeView.model().selected()
        if len(datasets):
            self._dataset, self._dataset_marker = datasets[0], dataset_markers[0]
            self.diffGroupBox.setEnabled(len(datasets) == 2)
            self.absPushButton.setEnabled(len(datasets) == 2)
            self.relPushButton.setEnabled(len(datasets) == 2)
            self.ratioPushButton.setEnabled(len(datasets) == 2)
            self.customPushButton.setEnabled("diff" in self._import_module.__dict__)
            self.diffGroupBox.repaint()
            self.datasetChanged.emit(self._dataset)

    @QtCore.Slot()
    def delta_abs(self):
        names, datasets, _ = self.datagroupTreeView.model().selected()
        dataset1, dataset2 = datasets[0], datasets[1]
        delta_dataset = DatagroupModel(dataset1.sweeps, dataset1.attributes)
        ref, val, delta_values = dataset1.values, dataset2.values, delta_dataset.values
        for k in ref.keys():
            if k in val:
                delta_values[k] = delta_abs(ref[k], val[k])
        self.datagroupTreeView.model().appendRow("delta_abs_%s_%s" % (names[0], names[1]), delta_dataset)

    @QtCore.Slot()
    def delta_rel(self):
        _, names, datasets, _ = self.datagroupTreeView.model().selected()
        dataset1, dataset2 = datasets[0], datasets[1]
        delta_dataset = DatagroupModel(dataset1.sweeps, dataset1.attributes)
        ref, val, delta_values = dataset1.values, dataset2.values, delta_dataset.values
        for k in ref.keys():
            if k in val:
                delta_values[k] = delta_rel(ref[k], val[k])
        self.datagroupTreeView.model().appendRow("delta_rel_%s_%s" % (names[0], names[1]), delta_dataset)

    @QtCore.Slot()
    def delta_ratio(self):
        _, names, datasets, _ = self.datagroupTreeView.model().selected()
        dataset1, dataset2 = datasets[0], datasets[1]
        delta_dataset = DatagroupModel(dataset1.sweeps, dataset1.attributes)
        ref, val, delta_values = dataset1.values, dataset2.values, delta_dataset.values
        for k in ref.keys():
            if k in val:
                delta_values[k] = delta_ratio(ref[k], val[k])
        self.datagroupTreeView.model().appendRow("delta_ratio_%s_%s" % (names[0], names[1]), delta_dataset)

    @QtCore.Slot()
    def delta_custom(self):
        _, names, datasets, _ = self.datagroupTreeView.model().selected()
        dataset1, dataset2 = datasets[0], datasets[1]
        delta_dataset = self._import_module.diff(dataset1, dataset2)
        self.datagroupTreeView.model().appendRow("delta_custom_%s_%s" % (names[0], names[1]), delta_dataset)

    def nop(self, arg):
        return

    def update(self, index=False, equations=False, interpolation=False, plots=False):
        super(DatagroupFrame, self).update()

        self.importLineEdit.setText(self._import_module_name)
        self.datagroupLineEdit.setText(self._datagroup_filename)
        self._parent.update(batch_index=index, equations=equations, interpolation=interpolation, plots=plots)
