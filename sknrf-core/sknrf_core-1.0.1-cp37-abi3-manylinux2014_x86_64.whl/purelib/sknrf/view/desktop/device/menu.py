"""Device Views that define GUI interaction with device models
"""
import os
import importlib
import inspect
import logging
import pkgutil
import re
import unittest
from collections import OrderedDict
import yaml

from PySide2 import QtCore
from PySide2.QtCore import Qt, QThread, QSize
from PySide2.QtGui import QIcon, QPixmap, QCloseEvent
from PySide2.QtWidgets import QApplication, QMainWindow, QFrame, QWidget, QMessageBox
from PySide2.QtWidgets import QHBoxLayout, QSplitter, QSizePolicy

from sknrf.device import AbstractDevice
from sknrf.device.instrument.auxiliary.base import NoAux
from sknrf.device.tests import test_device
from sknrf.model.base import AbstractModel
from sknrf.settings import Settings
from sknrf.view.base import AbstractView
from sknrf.view.desktop.base import BusyFrame
from sknrf.widget.propertybrowser.view.enums import DISPLAY
from sknrf.view.desktop.device.QDeviceLoadFrame import Ui_deviceLoadFrame
from sknrf.view.desktop.device.QDeviceMenuView import Ui_deviceMenuView
from sknrf.view.desktop.device.QPropertyFrame import Ui_propertyFrame
from sknrf.view.desktop.preview.frame import SignalPreviewFrame, AuxiliarySignalPreviewFrame
from sknrf.view.desktop.sideview.base import AbstractSideView, SideViewTabWidget, LogSideView
from sknrf.view.desktop.sideview.dutmipi import MIPISideView
from sknrf.view.desktop.sideview.dutvideo import DUTVideoSideView
from sknrf.view.desktop.base import desktop_logger

from sknrf.widget.propertybrowser.view import BrowserCol

__author__ = 'dtbespal'
logger = desktop_logger(logging.getLogger(__name__))


class DeviceTestThread(QThread):

    def __init__(self, func, *args):
        super(DeviceTestThread, self).__init__()
        self._func = func
        self._args = args

    def run(self):
        self._func(*self._args)


class DeviceSideView(AbstractSideView, QFrame, Ui_deviceLoadFrame):

    def __init__(self, driver_package, base_class=AbstractDevice, model=None, model_icon=QIcon(), parent=None):
        super(DeviceSideView, self).__init__(parent=parent)
        self.setupUi(self)

        self._model_icon = model_icon
        self.imageLabel.setPixmap(QPixmap(self._model_icon.pixmap(QSize(128, 128))))
        self.driver_package = driver_package
        self.base_class = base_class
        self.driver_map = {}
        self.update_driver_map()
        driver_list = list(self.driver_map.keys())
        self.driverComboBox.addItems(driver_list)

        self.address_model = OrderedDict()
        self.addressTable.property_browser.display = DISPLAY.READ
        self.addressTable.property_browser.set_update(self.update,
                                                      **{"on_off": True, "address": True, "firmware": True})

    def connect_signals(self, *args, **kwargs):
        pass

    def disconnect_signals(self, *args, **kwargs):
        pass

    def update_driver_map(self):
        """Updates the device driver list based on the contents of the device driver_package folder.
        """
        driver_map = {}
        package = self.driver_package
        base_class = self.base_class
        for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__,
                                                              prefix=package.__name__+'.',
                                                              onerror=lambda x: None):
            module = importlib.import_module(modname)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) \
                        and not inspect.isabstract(obj)\
                        and base_class in inspect.getmro(obj)\
                        and not name.startswith("_"):
                    driver_map[name] = module
        self.driver_map = driver_map

    def set_model(self, model):
        self.disconnect_signals()
        super(DeviceSideView, self).set_model(model)

        if self._model.initialized:
            if hasattr(self._model, "on"):
                self.onButton.show()
                self.offButton.show()
            else:
                self.onButton.hide()
                self.offButton.hide()

            driver_list = list(self.driver_map.keys())
            selected_driver = re.split(r"\.", self._model.__class__.__name__)
            driver_index = driver_list.index(selected_driver[-1])
            self.driverComboBox.setCurrentIndex(driver_index)

        self.address_model.clear()
        argument_spec = inspect.getfullargspec(model.__init__)
        if argument_spec.defaults:
            keyword_arguments = argument_spec.args[-len(argument_spec.defaults):]
            for idx in range(0, len(keyword_arguments)):
                if keyword_arguments[idx][0] != "_":
                    self.address_model[keyword_arguments[idx]] = argument_spec.defaults[idx]
            self.address_model["config_filename"] = getattr(self._model, "config_filename")
        self.addressTable.property_browser.set_model(self.address_model)
        self.firmwareTable.property_browser.set_model(self._model.firmware_map)
        self.connect_signals()

    def update(self, on_off=False, address=False, firmware=False):
        super(DeviceSideView, self).update()
        all_ = not(on_off or address or firmware)

        if (on_off or all_) and self._model.initialized and hasattr(self._model, "on"):
            if self._model.on:
                self.onButton.setStyleSheet("color: white; background-color: green")
                self.offButton.setStyleSheet("color: black; background-color: grey")
            else:
                self.onButton.setStyleSheet("color: black; background-color: grey")
                self.offButton.setStyleSheet("color: white; background-color: red")

        if address or all_:
            self.addressTable.property_browser.render()
        if firmware or all_:
            self.firmwareTable.property_browser.render()


class PropertyFrame(QFrame, Ui_propertyFrame):
    def __init__(self, parent=None):
        super(PropertyFrame, self).__init__(parent=parent)
        self.setupUi(self)


class DeviceMenuView(AbstractView, QMainWindow, Ui_deviceMenuView):
    """Device Menu View Widget for detailed device settings

        ..  figure:: ../_images/PNG/device_menu_view.png
            :width: 100 %
            :align: center

            A Multi-Harmonic RF Source with digital I/Q modulation.

        Args:
            driver_package (package): The root package containing all drivers of a given device type eg.) sknrf.device.instrument.rfsource
            model (Device_like): The device object
        Keyword Args:
            model_args (tuple): Required args passed to a new device model
            parent (QWidget): Parent GUI container
    """
    device_selected = QtCore.Signal(object)
    device_loaded = QtCore.Signal(object)
    device_removed = QtCore.Signal()
    single_measurement = QtCore.Signal()

    def __init__(self, driver_package, base_class=AbstractDevice, model=None, model_args=(), model_icon=QIcon(), parent=None):
        super(DeviceMenuView, self).__init__(parent)
        self.setupUi(self)
        # Right Align Measurement Buttons of Toolbar
        empty = QWidget()
        empty.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolBar.insertWidget(self.actionSingle, empty)

        self.hbl = QHBoxLayout(self.centralwidget)
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setOrientation(Qt.Horizontal)
        self.sideViewTabWidget = SideViewTabWidget(parent=self.splitter)
        self.content_frame = QFrame(self.splitter)
        self.hbl2 = QHBoxLayout(self.content_frame)

        self.sidebar_views = OrderedDict((("Device", DeviceSideView(driver_package, base_class=base_class, model=OrderedDict(), model_icon=model_icon, parent=self.sideViewTabWidget)),
                                          ("Log", LogSideView(AbstractModel, logger, parent=self.sideViewTabWidget)),))
        for tab_name, tab_widget in self.sidebar_views.items():
            self.sideViewTabWidget.addTab(tab_widget, tab_name)

        # Initialize Models
        self.driver_package = driver_package
        self._model, self._model_args = None, model_args
        self.runtime_thread = None
        if model is None:
            model = self.driver_package.default_driver(self._model_args)

        # Initialize Views
        self.propertyFrame = PropertyFrame(parent=self.content_frame)
        self.propertyTabWidget = self.propertyFrame.propertyTabWidget
        self.propertyTable = self.propertyFrame.propertyTable
        self.hbl2.addWidget(self.propertyFrame)
        if isinstance(model, NoAux):
            self.signal_preview_frame = AuxiliarySignalPreviewFrame(parent=self.content_frame)
        else:
            self.signal_preview_frame = SignalPreviewFrame(parent=self.content_frame)
        self.hbl2.addWidget(self.signal_preview_frame)
        self.hbl.addWidget(self.splitter)

        self.connect_signals()
        self.propertyTable.property_browser.display = DISPLAY.PUBLIC
        self.propertyTable.property_browser.setAttributes([BrowserCol.UNIT, BrowserCol.PKAVG, BrowserCol.FORMAT])
        self.propertyTable.property_browser.set_update(self.update,
                                                       **{"on_off": True, "address": False, "firmware": False,
                                                          "value": True, "preview": True})
        self._new_model = model
        self.set_model(model)

    def connect_signals(self, *args, **kwargs):
        device_sideview = self.sidebar_views["Device"]
        self.actionDocumentation.triggered.connect(self.clicked_doc)
        self.actionSingle.triggered.connect(self.triggered_single)
        device_sideview.onButton.clicked.connect(self.clicked_on_off)
        device_sideview.offButton.clicked.connect(self.clicked_on_off)
        device_sideview.testButton.clicked.connect(self.clicked_test_driver)
        device_sideview.loadDriverButton.clicked.connect(self.load_driver)
        device_sideview.driverComboBox.activated[str].connect(self.select_driver)
        self.propertyTabWidget.currentChanged.connect(self.selected_property_tab)

    def disconnect_signals(self, *args, **kwargs):
        device_sideview = self.sidebar_views["Device"]
        self.actionDocumentation.triggered.disconnect()
        self.actionSingle.triggered.disconnect()
        device_sideview.onButton.clicked.disconnect()
        device_sideview.offButton.clicked.disconnect()
        device_sideview.testButton.clicked.disconnect()
        device_sideview.loadDriverButton.clicked.disconnect()
        device_sideview.driverComboBox.activated[str].disconnect()
        self.propertyTabWidget.currentChanged.disconnect()

    def set_model(self, model):
        self.disconnect_signals()
        self._model = model
        self._model.info["config_filename"].read = False
        self.sidebar_views["Device"].set_model(self._model)
        self.propertyTable.property_browser.set_model(self._model, info=self._model.info)
        self.signal_preview_frame.set_model(self._model)
        self.connect_signals()

    def selected_property_tab(self, _):
        self.disconnect_signals()
        tab = self.propertyTabWidget.currentWidget()
        self.propertyTable.setParent(tab)
        self.propertyTable.show()
        self.propertyTable.property_browser.clear()
        if tab == self.propertyFrame.propertyTab:
            self.propertyTable.property_browser.setAttributes([BrowserCol.UNIT, BrowserCol.PKAVG, BrowserCol.FORMAT])
        elif tab == self.propertyFrame.limitTab:
            self.propertyTable.property_browser.setAttributes([BrowserCol.MINIMUM, BrowserCol.MAXIMUM, BrowserCol.FORMAT])
        elif tab == self.propertyFrame.optimizationTab:
            self.propertyTable.property_browser.setAttributes([BrowserCol.MINIMUM, BrowserCol.MAXIMUM, BrowserCol.FORMAT])
        elif tab == self.propertyFrame.displayTab:
            self.propertyTable.property_browser.setAttributes([BrowserCol.CHECK])
        self.propertyTable.property_browser.set_model(self._model)
        self.connect_signals()

    def set_new_model(self, new_model):
        self._new_model = new_model
        self.sidebar_views["Device"].set_model(self._new_model)

    def triggered_single(self):
        self.single_measurement.emit()

    def clicked_on_off(self):
        self._model.on = not self._model.on
        self.update(on_off=True, value=True)

    def select_driver(self, driver_name):
        """Creates a new model instance by calling the __new__() function of the selected device driver

        Args:
            driver_name (str): The class name of the new device model eg.) "NoRFSource"
        """
        device_sideview = self.sidebar_views["Device"]
        combo = device_sideview.driverComboBox
        combo.setCurrentIndex(combo.findText(driver_name))
        driver = getattr(device_sideview.driver_map[driver_name], driver_name)
        with BusyFrame(self.sidebar_views["Device"], self.device_selected, "Loading Device..."):
            try:
                new_model = driver.__new__(driver, *self._model_args)
            except Exception as e:
                logger.error('An error occured while inspecting the instrument driver: %s.' % (driver_name,),
                             exc_info=True)
                QMessageBox.critical(self, 'Unable to select device driver',
                                           str(e))
                # Select Default Driver
                driver_name = self.driver_package.default_driver.__name__
                combo = device_sideview.driverComboBox
                combo.setCurrentIndex(combo.findText(driver_name))
                driver = getattr(device_sideview.driver_map[driver_name], driver_name)
                new_model = driver.__new__(driver, *self._model_args)
            finally:
                # Select Specified Driver
                self.set_new_model(new_model)
                self.device_selected.emit(new_model)

    def load_driver(self):
        """Connects and initializes the device by calling  __init__() function of the device driver with the provided address map
        """
        device_sideview = self.sidebar_views["Device"]
        with BusyFrame(self.content_frame, self.device_loaded, "Loading Device..."):
            if self._new_model is self._model:
                driver_name = self._new_model.__class__.__name__
                self.select_driver(driver_name)
            self._model.disconnect_handles()
            self.device_removed.emit()
            self._model = None
            try:
                self._new_model.__init__(*self._model_args, **device_sideview.address_model)
            except Exception as e:
                self._new_model.disconnect_handles()
                logger.error(str(e), exc_info=True)
                QMessageBox.critical(self, 'Unable to load device driver', str(e))
                self._new_model.disconnect_handles()
                self.reset()
            else:
                # Load Specified Driver
                self._model_args[0].set_stimulus(self._model_args[0].stimulus())
                self._model_args[0].measure()
                self.set_model(self._new_model)
                self.device_loaded.emit(self._model)

    def clicked_test_driver(self):
        self._model.disconnect_handles()
        self.device_removed.emit()
        self._model = None
        short_name = self.driver_package.__name__.split(".")[-1]
        test_module = importlib.import_module(
            ".".join((self.driver_package.__name__, "tests", "test_" + short_name)))
        test_device.logger = desktop_logger(logging.getLogger(self._new_model.__module__))
        runner = unittest.TextTestRunner()
        runner.resultclass = test_device.LogTestResult
        config = {}
        with open(os.sep.join((Settings().data_root, "testdata", "test_device.yml")), 'w') as f:
            config["module"] = self._new_model.__module__
            config["class"] = self._new_model.__class__.__name__
            config["args"] = self._model_args[1:]
            config["kwargs"] = self.sidebar_views["Device"].address_model
            yaml.dump(config, f)
        self.sideViewTabWidget.setCurrentIndex(list(self.sidebar_views.keys()).index("Log"))
        self.runtime_thread = DeviceTestThread(runner.run, test_module.driver_test_suite())
        self.runtime_thread.finished.connect(self.reset)
        self.runtime_thread.finished.connect(self.runtime_thread.deleteLater)
        self.sidebar_views["Log"].set_logger(test_device.logger)
        with BusyFrame(self.content_frame, self.runtime_thread.finished, "Testing Device..."):
            try:
                self.runtime_thread.start()
            except Exception as e:
                QMessageBox.critical(self, 'Driver Test Failed', str(e))
                self.reset()

    def reset(self):
        self.sidebar_views["Log"].set_logger(logger)
        device_sideview = self.sidebar_views["Device"]
        # Select Default Driver
        driver_name = self.driver_package.default_driver.__name__
        combo = device_sideview.driverComboBox
        combo.setCurrentIndex(combo.findText(driver_name))
        driver = getattr(device_sideview.driver_map[driver_name], driver_name)
        new_model = driver.__new__(driver, *self._model_args)
        self.set_new_model(new_model)

        # Load Default Driver
        device_sideview.address_model.clear()
        self._new_model.__init__(*self._model_args, **device_sideview.address_model)
        self.set_model(self._new_model)
        self._model_args[0].set_stimulus(self._model_args[0].stimulus())
        self._model_args[0].measure()
        self.device_loaded.emit(self._model)
        self.update(on_off=True, address=True, firmware=True, value=True, preview=True)

    def update(self, on_off=False, address=False, firmware=False, value=False, preview=False):
        """Updates the GUI.

        The entire menu will update by default.

        Keyword Args:
            on_off (bool): Update only the on_off button if True
            address (bool): Update only the address table if True
            firmware (bool): Update only the firmware table if True
            value (bool): Update only the value table if True
            preview (bool): Update only the preview frame if True
        """
        super(DeviceMenuView, self).update()
        all_ = not(on_off or address or firmware or value or preview)

        self.sidebar_views["Device"].update(on_off, address, firmware)
        if self._model and (value or all_):
            self.propertyTable.property_browser.render()
        if self._model and (preview or all_):
            self.signal_preview_frame.update()

    def closeEvent(self, event: QCloseEvent):
        try:
            _ = self.runtime_thread.metaObject()
        except AttributeError:  # Runtime Thread never used
            pass
        except RuntimeError:  # Runtime Thread was deleted
            pass
        else:
            self.runtime_thread.exit(1)
            self.runtime_thread.wait(1.0)
            self.reset()
            self.load_driver()
            raise RuntimeError("Device Menu closed during task execution, restart required")
        super().closeEvent(event)


class DUTMenuView(DeviceMenuView):

    def __init__(self, driver_package, base_class=AbstractDevice, model=None, model_args=(), model_icon=QIcon(), parent=None):
        super().__init__(driver_package, base_class=base_class,
                         model=model, model_args=model_args, model_icon=model_icon, parent=parent)
        self.sidebar_views["MIPI"] = MIPISideView(model=AbstractModel, parent=self.sideViewTabWidget)
        self.sidebar_views["Video"] = DUTVideoSideView(model=AbstractModel, parent=self.sideViewTabWidget)
        self.sideViewTabWidget.addTab(self.sidebar_views["MIPI"], "MIPI")
        self.sideViewTabWidget.addTab(self.sidebar_views["Video"], "Video")

