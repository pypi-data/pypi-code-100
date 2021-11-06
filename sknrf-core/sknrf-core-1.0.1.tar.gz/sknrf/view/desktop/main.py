import sys
import os
import webbrowser
import pickle
import logging
from collections import OrderedDict

import torch as th
import skrf
from PySide2 import QtCore
from PySide2.QtWidgets import QMainWindow, QMessageBox, QWidget, QFileDialog
from PySide2.QtWidgets import QSplitter, QSizePolicy

from sknrf.settings import Settings
from sknrf.device.signal import ff
from sknrf.model.base import AbstractModel
from sknrf.model.runtime import RuntimeThread
from sknrf.app.dataviewer.model.dataset import DatagroupModel
from sknrf.app.dataviewer.model.snp import SNP
from sknrf.model.sequencer.measure import Measure
from sknrf.model.sequencer.base import SequencerSideModel
from sknrf.view.base import AbstractView
from sknrf.view.desktop.base import BusyFrame
from sknrf.view.desktop.QMainMenuView import Ui_mainMenu
from sknrf.view.desktop.settings.settings import SettingsView
from sknrf.view.desktop.sideview.base import SideViewTabWidget, LogSideView
from sknrf.view.desktop.sideview.main import MainSideView
from sknrf.view.desktop.sideview.calkit import CalkitSideView
from sknrf.view.desktop.sideview.dut import DUTSideView
from sknrf.view.desktop.sideview.auxiliary import AuxiliarySideView
from sknrf.view.desktop.transform.circuit import TransformSideView
from sknrf.view.desktop.device.tile import DeviceManagerView
from sknrf.view.desktop.launcher.menu import LauncherMenuView
from sknrf.view.desktop.sequencer.menu import SequencerView
from sknrf.view.desktop.runtime.ls import LargeSignalRuntimeView
from sknrf.view.desktop.runtime.ss import SmallSignalRuntimeView
from sknrf.utilities.dsp import fm_grid

from sknrf.model import sequencer as core
from sknrf.view.desktop import calibration

if sys.platform == "win32": import pythoncom

logger = logging.getLogger(__name__)


class MainMenuView(AbstractView, QMainWindow, Ui_mainMenu):
    """Main Menu View Widget for device settings overview

        ..  figure:: ../_images/PNG/setup_type_ltf.png
            :width: 50 %
            :align: center

            A 2-Port Test-bench circuit representation.

        ..  figure:: ../_images/PNG/main_menu_view.png
            :width: 100 %
            :align: center

            The equivalent Main Menu View dashboard representation of the Test-bench.

        Keyword Args:
            parent (QWidget): Parent GUI container
    """
    loaded_state = QtCore.Signal()
    saved_state = QtCore.Signal()

    def __init__(self, parent=None):
        super(MainMenuView, self).__init__(parent)
        self.setupUi(self)
        # Right Align Measurement Buttons of Toolbar
        empty = QWidget()
        empty.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolBar.insertWidget(self.actionSParameter, empty)
        # Content Splitter
        self.splitter = QSplitter(self.centralwidget)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.splitter.setSizePolicy(size_policy)
        self.sideViewTabWidget = SideViewTabWidget(parent=self.centralwidget)
        log_side_view = LogSideView(AbstractModel, logger, parent=self.sideViewTabWidget)

        # Initialize Models
        AbstractModel.init()
        self.runtime_thread = RuntimeThread()
        self.runtime_model = None

        # Initialize Views
        self.sidebar_views = OrderedDict((("Main", MainSideView(model=AbstractModel, parent=self.sideViewTabWidget)),
                                          ("Calkits", CalkitSideView(model=AbstractModel, parent=self.sideViewTabWidget)),
                                          ("Transforms", TransformSideView(model=AbstractModel, parent=self.sideViewTabWidget)),
                                          ("Aux", AuxiliarySideView(model=AbstractModel, parent=self.sideViewTabWidget)),
                                          ("DUT", DUTSideView(model=AbstractModel, parent=self.sideViewTabWidget)),
                                          ("Log", log_side_view),))
        for tab_name, tab_widget in self.sidebar_views.items():
            self.sideViewTabWidget.addTab(tab_widget, tab_name)
        self.device_manager_view = DeviceManagerView(AbstractModel.device_model(), parent=self.centralwidget)
        self.settings_view = None
        self.devices_view = None
        self.sequencer_view = None
        self.app_view = None
        self.data_viewer = None
        self.runtime_view = None

        self.splitter.addWidget(self.sideViewTabWidget)
        self.splitter.addWidget(self.device_manager_view)
        self.layout = self.centralwidget.layout()
        self.layout.addWidget(self.splitter)

        self.connect_signals()

    def connect_signals(self):
        self.actionLoad.triggered.connect(self.clicked_load)
        self.actionSave.triggered.connect(self.clicked_save)
        self.actionSave_As.triggered.connect(self.clicked_save_as)

        self.actionSequencer.triggered.connect(self.clicked_sequencer)
        self.actionApp.triggered.connect(self.clicked_app)

        self.actionPreferences.triggered.connect(self.clicked_settings)
        self.actionAbout.triggered.connect(self.clicked_about)
        self.actionHelp.triggered.connect(self.clicked_doc)

        self.actionSParameter.triggered.connect(self.clicked_sparameter)
        self.actionSingle.triggered.connect(self.clicked_single)

        for side_view in self.sidebar_views.values():
            side_view.update_main_window.connect(self.update)
        self.actionExit.triggered.connect(self.closeEvent)
        Settings().device_reset_requested.connect(self.reset_request)
        Settings().device_reset_required.connect(self.reset)

        for port in self.device_manager_view.port_panels_map.values():
            for instrument in port.tile_map.values():
                instrument.single_measurement.connect(self.clicked_single)

    def disconnect_signals(self):
        self.actionLoad.triggered.disconnect()
        self.actionSave.triggered.disconnect()
        self.actionSave_As.triggered.disconnect()

        self.actionSequencer.triggered.disconnect()
        self.actionApp.triggered.disconnect()

        self.actionPreferences.triggered.disconnect()
        self.actionAbout.triggered.disconnect()
        self.actionHelp.triggered.disconnect()

        self.actionSParameter.triggered.disconnect()
        self.actionSingle.triggered.disconnect()

        self.actionExit.triggered.disconnect()
        Settings().device_reset_requested.disconnect()
        Settings().device_reset_required.disconnect()

        for port in self.device_manager_view.port_panels_map.values():
            for instrument in port.tile_map.values():
                instrument.single_measurement.disconnect()

    def clicked_load(self):
        filenames = list()
        filename = "saved_state.state"
        filenames = QFileDialog.getOpenFileName(self,
                                                "Load System State",
                                                os.sep.join((Settings().data_root, "saved_states", filename)),
                                                "State File (*.state)")

        if len(filenames[0]):
            filename = filenames[0]
            with BusyFrame(self.device_manager_view, self.loaded_state, "Loading State..."):
                self.disconnect_signals()
                if sys.platform == "win32": pythoncom.CoInitialize()
                with open(filename, "rb") as file_id:
                    Settings().__setstate__(pickle.load(file_id).__getstate__(state={}))
                    AbstractModel.device_model().disconnect_handles()
                    AbstractModel.set_device_model(pickle.load(file_id))
                    AbstractModel.datagroup_model()["Single"].close()
                    AbstractModel.datagroup_model()["Single"] = DatagroupModel(mode="w")
                    AbstractModel.datagroup_model()["Single"].add("Single")
                for tab_name, tab_widget in self.sidebar_views.items():
                    tab_widget.set_model(AbstractModel)
                self.device_manager_view.set_model(AbstractModel.device_model())

                self.connect_signals()
                self.update()
                self.loaded_state.emit()

    def clicked_save(self):
        filenames = list()
        filename = "saved_state.state"
        filenames = QFileDialog.getSaveFileName(self,
                                                "Save System State",
                                                os.sep.join((Settings().data_root, "saved_states", filename)),
                                                "State File (*.state)")

        if len(filenames[0]):
            filename = filenames[0]
            with open(filename, "wb") as file_id:
                pickle.dump(Settings(), file_id)
                pickle.dump(AbstractModel.device_model(), file_id)
            return True
        return False

    def clicked_save_as(self):
        pass

    def clicked_sequencer(self):
        package_map = OrderedDict((("Core", [core]),))
        side_model = SequencerSideModel(package_map)
        self.sequencer_view = SequencerView(AbstractModel.device_model(), AbstractModel.datagroup_model(), side_model, parent=self)
        self.connect_submenu(self.sequencer_view)
        self.sequencer_view.showMaximized()

    def clicked_app(self):
        package_map = OrderedDict((("Calibration", [calibration]),))

        side_model = SequencerSideModel(package_map)
        self.app_view = LauncherMenuView(AbstractModel.device_model(), AbstractModel.datagroup_model(), side_model, parent=self)
        self.connect_submenu(self.app_view)
        self.app_view.showMaximized()

    def clicked_settings(self):
        self.settings_view = SettingsView(parent=self)
        self.connect_submenu(self.settings_view)
        self.settings_view.show()

    def clicked_store(self):
        url = Settings().url_root + "index.html"
        webbrowser.open(url, new=2, autoraise=True)

    def clicked_about(self):
        url = Settings().url_root + "index.html"
        webbrowser.open(url, new=2, autoraise=True)

    def clicked_sparameter(self):
        """ Perform a S-Parameter model extraction for all measurement ports.

        Perform a S-Parameter model extraction and update the GUI.
        """
        self.runtime_thread = RuntimeThread()
        self.runtime_view = SmallSignalRuntimeView()
        self.runtime_model = Measure()
        self.runtime_model.ports = list(range(0, Settings().num_ports + 1))
        self.runtime_model.ss_ports = list(range(1, Settings().num_ports + 1))

        self.runtime_thread.connect_signals(self.runtime_model, self.runtime_view)
        self.runtime_thread.started_.connect(self.runtime_model.single_sparameter_measurement)  # Pycharm Debugger does not work with Qthread.started
        self.runtime_thread.finished.connect(self.save_measurement)
        self.runtime_thread.finished.connect(self.update)
        Settings().datagroup = "Single"
        Settings().dataset = "S_Param"
        self.runtime_thread.start()

    def clicked_single(self):
        """ Perform a single measurement

        Perform a single measurement and update the GUI.
        """
        self.runtime_thread = RuntimeThread()
        self.runtime_view = LargeSignalRuntimeView()
        self.runtime_model = Measure()
        self.runtime_model.ports = list(range(0, Settings().num_ports + 1))
        self.runtime_model.ss_ports = list()

        self.runtime_thread.connect_signals(self.runtime_model, self.runtime_view)
        self.runtime_thread.started_.connect(self.runtime_model.single_measurement)  # Pycharm Debugger does not work with Qthread.started
        self.runtime_thread.finished.connect(self.update)
        Settings().datagroup = "Single"
        Settings().dataset = "Single"
        self.runtime_thread.start()

        # self.runtime_thread.connect_signals(self.runtime_model, self.runtime_view)
        # self.runtime_thread.started_.connect(self.runtime_model.swept_measurement)  # Pycharm Debugger does not work with Qthread.started
        # self.runtime_thread.finished.connect(self.update)
        # Settings().datagroup = "Single"
        # Settings().dataset = "Swept"
        # self.runtime_thread.start()

    def reset_request(self):
        ret = QMessageBox.question(self, "Device Reset Required",
                                         "The device drivers will be reset to the default drivers.\n"
                                                    "Do you want to save your changes?",
                                   QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                                   QMessageBox.Save)
        if ret == QMessageBox.Save:
            ret = self.clicked_save()
            Settings().set_request_response(ret)
        elif ret == QMessageBox.Discard:
            Settings().set_request_response(True)
        else:  # QMessageBox.Cancel
            Settings().set_request_response(False)

    def reset(self):
        self.disconnect_signals()
        for tab_name, tab_widget in self.sidebar_views.items():
            tab_widget.set_model(AbstractModel)
        self.device_manager_view.set_model(AbstractModel.device_model())
        self.connect_signals()
        self.update()

    def save_measurement(self):
        datagroup_name = "Single"
        dataset_name = "S_Param"
        ds = AbstractModel.datagroup_model()[datagroup_name].dataset(dataset_name)
        ds_shape = [1] * len(ds.shape)
        ds_shape[-3] = ds.shape[-3]
        ds_index = th.arange(0, ds.shape[-3], 1, dtype=th.int64).reshape(ds_shape)
        freq = (fm_grid(ds.sp_fund[...].gather(-3, ds_index)) + Settings().f0).flatten()
        s = ds.s[...]
        network = skrf.network.Network(name="S_Param", f=freq.detach().numpy(), s=s.detach().numpy(), f_unit="Hz")
        num_ports = s.shape[-1]

        filenames = list()
        filename = "%s.s%dp" % (dataset_name, num_ports)
        filenames = QFileDialog.getSaveFileName(self,
                                                "Save Validation S-Parameter File",
                                                os.sep.join((Settings().data_root, "testdata", filename)),
                                                "S-Parameter File (*.s%dp)" % (num_ports, ))

        if len(filenames[0]):
            filename = filenames[0]
            SNP.write_network(network, filename)
            return True
        return False

    def update(self, sideview=False, value=False):
        super(MainMenuView, self).update()
        all_ = not (sideview or value)

        if sideview or all_:
            self.sideViewTabWidget.currentWidget().update()
        if value or all_:
            self.device_manager_view.update(value=value)

