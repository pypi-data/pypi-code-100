from collections import OrderedDict

import numpy as np
from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QFrame
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout

from sknrf.settings import Settings
from sknrf.device.base import AbstractDevice
from sknrf.device.instrument import lfsource as instrument_lfsource
from sknrf.device.instrument import lfreceiver as instrument_lfreceiver
from sknrf.device.instrument import lfztuner as instrument_lfztuner
from sknrf.device.instrument import rfsource as instrument_rfsource
from sknrf.device.instrument import rfreceiver as instrument_rfreceiver
from sknrf.device.instrument import rfztuner as instrument_rfztuner
from sknrf.device import dut
from sknrf.device.dut.base import NoDUT
from sknrf.device.dut.mipi import client
from sknrf.device.dut.mipi.client.base import NoMIPIClient
from sknrf.device.dut import video
from sknrf.device.dut.video.base import NoVideo
from sknrf.device.instrument.auxiliary import pm, sa, vna
from sknrf.device.instrument.auxiliary.pm import NoPM
from sknrf.device.instrument.auxiliary.sa import NoSA
from sknrf.device.instrument.auxiliary.vna import NoVNA
from sknrf.model.device import DevicesModel
from sknrf.widget.propertybrowser.view.base import DISPLAY
from sknrf.view.desktop.device.QDevicePanelView import Ui_devicePanelView

from sknrf.widget.propertybrowser.view import BrowserCol, QtBrowserItem
from sknrf.icons import black_64_rc

__author__ = 'dtbespal'


class DeviceTileView(QFrame, Ui_devicePanelView):
    """Device status tile view.

    A summary of all device properties that have the info.display attribute enabled.

        Args:
            driver_package (module): The parent package/module where device drivers are stored.

        Keyword Args:
            model (Device_like): Any device object whose class is stored in the driver_package.
            model_args (tuple): Positional args to be passed to the device driver __init__() function.
            model_icon (QIcon): An icon that represents the driver_package type.
            parent (QWidget): Parent GUI container.
    """
    single_measurement = QtCore.Signal()

    def __init__(self, driver_package, base_class=AbstractDevice,
                 model=None, model_args=(), model_icon=QIcon(), parent=None):
        super(DeviceTileView, self).__init__(parent)
        self.setupUi(self)
        self.driver_package = driver_package
        self.base_class = base_class
        self._model = None
        self.model_args = model_args
        self.menuButton.setIcon(model_icon)
        self.value_manager_map = None
        self.value_factory_map = None
        self.menu = None

        self.connect_signals()
        self.propertyTable.property_browser.display = DISPLAY.CHECK
        self.propertyTable.property_browser.setAttributes([BrowserCol.UNIT, BrowserCol.PKAVG, BrowserCol.FORMAT])
        self.propertyTable.property_browser.set_update(self.update, **{"on_off": True, "value": True})
        if model is None:
            model = self.driver_package.default_driver(self.model_args)
        self.set_model(model)

    def connect_signals(self):
        self.onButton.clicked.connect(self.clicked_on_off)
        self.offButton.clicked.connect(self.clicked_on_off)
        self.menuButton.clicked.connect(self.clicked_menu_button)

    def disconnect_signals(self):
        self.onButton.clicked.disconnect(self.clicked_on_off)
        self.offButton.clicked.disconnect(self.clicked_on_off)
        self.menuButton.clicked.disconnect(self.clicked_menu_button)

    def model(self):
        return self._model

    def set_model(self, model):
        self.disconnect_signals()
        self._model = model
        if hasattr(self._model, "on"):
                self.onButton.show()
                self.offButton.show()
        else:
            self.onButton.hide()
            self.offButton.hide()
        property_browser = self.propertyTable.property_browser
        property_browser.set_model(self._model, info=self._model.info)
        self.connect_signals()
        self.update(on_off=True)

    def clicked_on_off(self):
        self._model.on = not self._model.on
        self.update(on_off=True, value=True)

    def clicked_menu_button(self, checked=False):
        from sknrf.view.desktop.device.menu import DeviceMenuView, DUTMenuView
        if isinstance(self._model, NoDUT):
            self.menu = DUTMenuView(self.driver_package, base_class=self.base_class,
                                    model=self._model, model_args=self.model_args, model_icon=self.menuButton.icon(),
                                    parent=self)
        else:
            self.menu = DeviceMenuView(self.driver_package, base_class=self.base_class,
                                       model=self._model, model_args=self.model_args, model_icon=self.menuButton.icon(),
                                       parent=self)
        self.menu.setAttribute(Qt.WA_DeleteOnClose)
        self.menu.destroyed.connect(self.slot_menu_closed)
        self.menu.device_loaded.connect(self.__load_driver)
        self.menu.device_removed.connect(self.__remove_driver)
        self.menu.single_measurement.connect(self.__single_measurement)
        self.menu.show()

    def __load_driver(self, model):
        self.set_model(model)

    def __remove_driver(self):
        self._model = None

    def __single_measurement(self):
        self.single_measurement.emit()

    def slot_menu_closed(self):
        self.set_model(self._model)
        self.window().update()

    def update(self, on_off=False, value=False):
        super(DeviceTileView, self).update()
        all_ = not (on_off or value)

        if (on_off or all_) and hasattr(self._model, "on"):
            if self._model.on:
                self.onButton.setStyleSheet("color: white; background-color: green")
                self.offButton.setStyleSheet("color: black; background-color: grey")
            else:
                self.onButton.setStyleSheet("color: black; background-color: grey")
                self.offButton.setStyleSheet("color: white; background-color: red")
        if value or all_:
            self.propertyTable.property_browser.render()


class AbstractTileGroupView(QFrame):
    """Abstract Device Tile Group

    A container that stores multiple device summary tiles.

        Args:
            model (custom): A custom device container defined by the base class.

        Keyword Args:
            parent (QWidget): Parent GUI container.
    """
    def __init__(self, model, error_model, parent=None):
        super(AbstractTileGroupView, self).__init__(parent)
        self.tile_map = OrderedDict()
        self.vbl = QVBoxLayout()
        self.vbl.setContentsMargins(0, 0, 0, 0)
        self.vbl.setSpacing(0)

        self._error_model = error_model
        if model is not None:
            self.set_model(model)

    def set_model(self, model):
        for child in self.findChildren(DeviceTileView):
            self.vbl.removeWidget(child)
        for _, v in self.tile_map.items():
            self.vbl.addWidget(v)
        self.setLayout(self.vbl)

    def update(self, value=False):
        super(AbstractTileGroupView, self).update()
        all_ = not(value)

        if value or all_:
            for _, v in self.tile_map.items():
                v.update()


class PortTileGroupView(AbstractTileGroupView):
    """Port Device Tile Group

    A container that stores all device connected to a given port.

        Args:
            model (PortModel): A collection of all device objects connected to a given port.

        Keyword Args:
            parent (QWidget): Parent GUI container.
    """
    def __init__(self, model, error_model, parent=None):
        super(PortTileGroupView, self).__init__(model, error_model, parent)

    def set_model(self, model):
        self.tile_map["lfsource"] = DeviceTileView(instrument_lfsource, model=model.lfsource,
                                                   model_args=[self._error_model, model.port_num],
                                                   model_icon=QIcon(":/PNG/black/64/lfsource.png"),
                                                   parent=self)
        self.tile_map["lfreceiver"] = DeviceTileView(instrument_lfreceiver, model=model.lfreceiver,
                                                     model_args=[self._error_model, model.port_num],
                                                     model_icon=QIcon(":/PNG/black/64/lfreceiver.png"),
                                                     parent=self)
        self.tile_map["lfztuner"] = DeviceTileView(instrument_lfztuner, model=model.lfztuner,
                                                   model_args=[self._error_model,model.port_num],
                                                   model_icon=QIcon(":/PNG/black/64/lfztuner.png"),
                                                   parent=self)
        self.tile_map["rfsource"] = DeviceTileView(instrument_rfsource, model=model.rfsource,
                                                   model_args=[self._error_model, model.port_num],
                                                   model_icon=QIcon(":/PNG/black/64/rfsource.png"),
                                                   parent=self)
        self.tile_map["rfreceiver"] = DeviceTileView(instrument_rfreceiver, model=model.rfreceiver,
                                                     model_args=[self._error_model, model.port_num],
                                                     model_icon=QIcon(":/PNG/black/64/rfreceiver.png"),
                                                     parent=self)
        self.tile_map["rfztuner"] = DeviceTileView(instrument_rfztuner, model=model.rfztuner,
                                                   model_args=[self._error_model, model.port_num],
                                                   model_icon=QIcon(":/PNG/black/64/rfztuner.png"),
                                                   parent=self)
        super(PortTileGroupView, self).set_model(model)

    def update(self, value=False):
        super(PortTileGroupView, self).update(value=value)


class AuxiliaryGroupView(AbstractTileGroupView):
    """Auxiliary Instrument Tile Group

    A container that stores all Auxiliary Instrument devices.

        Args:
            model (list): A list of all auxiliary instruments.

        Keyword Args:
            parent (QWidget): Parent GUI container.
    """
    def __init__(self, model, error_model, parent=None):
        super(AuxiliaryGroupView, self).__init__(model, error_model, parent)

    def set_model(self, model):
        self.tile_map["pm"] = DeviceTileView(pm, base_class=NoPM, model=model[0],
                                             model_args=[self._error_model, Settings().num_ports],
                                             model_icon=QIcon(":/PNG/black/64/pm.png"),
                                             parent=self)
        self.tile_map["sa"] = DeviceTileView(sa, base_class=NoSA, model=model[1],
                                             model_args=[self._error_model, Settings().num_ports],
                                             model_icon=QIcon(":/PNG/black/64/sa.png"),
                                             parent=self)
        self.tile_map["vna"] = DeviceTileView(vna, base_class=NoVNA, model=model[2],
                                             model_args=[self._error_model, Settings().num_ports],
                                             model_icon=QIcon(":/PNG/black/64/vna.png"),
                                             parent=self)
        super(AuxiliaryGroupView, self).set_model(model)

    def update(self, value=False):
        super(AuxiliaryGroupView, self).update(value=value)


class DUTTileGroupView(AbstractTileGroupView):
    """DUT Device Tile Group

    A container that stores all DUT device.

        Args:
            model (list): A list of all DUT device.

        Keyword Args:
            parent (QWidget): Parent GUI container.
    """
    def __init__(self, model, error_model, parent=None):
        super(DUTTileGroupView, self).__init__(model, error_model, parent)

    def set_model(self, model):
        for index in range(len(model)):
            self.tile_map["DUT" + str(index)] = DeviceTileView(dut, base_class=NoDUT, model=model[index],
                                                               model_args=[self._error_model, 0],
                                                               model_icon=QIcon(":/PNG/black/64/dut.png"),
                                                               parent=self)
        super(DUTTileGroupView, self).set_model(model)

    def update(self, value=False):
        super(DUTTileGroupView, self).update(value=value)


class MIPIGroupView(AbstractTileGroupView):
    """DUT Control Tile Group

    A container that stores all DUT MIPI devices.

        Args:
            model (list): A DUT MIPI device.

        Keyword Args:
            parent (QWidget): Parent GUI container.
    """
    def __init__(self, model, error_model, parent=None):
        super(MIPIGroupView, self).__init__(model, error_model, parent)

    def set_model(self, model):
        self.tile_map["rffe"] = DeviceTileView(client, base_class=NoMIPIClient,
                                               model=model.mipi[0], model_args=[self._error_model, 0],
                                               model_icon=QIcon(":/PNG/black/64/rffe.png"),
                                               parent=self)
        self.tile_map["et"] = DeviceTileView(client, base_class=NoMIPIClient,
                                             model=model.mipi[1], model_args=[self._error_model, 0],
                                             model_icon=QIcon(":/PNG/black/64/et.png"),
                                             parent=self)
        super(MIPIGroupView, self).set_model(model)

    def update(self, value=False):
        super(MIPIGroupView, self).update(value=value)


class DUTVideoGroupView(AbstractTileGroupView):
    """DUT Video Tile Group

    A container that stores all DUT video devices.

        Args:
            model (list): A DUT Video device.

        Keyword Args:
            parent (QWidget): Parent GUI container.
    """
    def __init__(self, model, error_model, parent=None):
        super(DUTVideoGroupView, self).__init__(model, error_model, parent)

    def set_model(self, model):
        for index in range(len(model)):
            self.tile_map["video" + str(index)] = DeviceTileView(video, base_class=NoVideo, model=model[index],
                                                                 model_args=[self._error_model, 0],
                                                                 model_icon=QIcon(":/PNG/black/64/unknown.png"),
                                                                 parent=self)
        super(DUTVideoGroupView, self).set_model(model)

    def update(self, value=False):
        super(DUTVideoGroupView, self).update(value=value)


class DeviceManagerView(QFrame):
    """Device Manager Port Tile Group container

    A container that Port Tile Group containers.

        Args:
            model (DevicesModel): A reference to all connected device.

        Keyword Args:
            parent (QWidget): Parent GUI container.
    """
    def __init__(self, model, parent=None):
        super(DeviceManagerView, self).__init__(parent)
        self.port_panels_map = OrderedDict()
        self.hbl = QHBoxLayout()
        self.hbl.setContentsMargins(0, 0, 0, 0)
        self.hbl.setSpacing(0)
        self.set_model(model)

    def set_model(self, model):
        for child in self.findChildren(PortTileGroupView):
            child.deleteLater()
        for index in range(1, len(model.ports)):
            self.port_panels_map["Port" + str(index)] = PortTileGroupView(model.ports[index], model, parent=self)
            self.hbl.addWidget(self.port_panels_map["Port" + str(index)])
        self.setLayout(self.hbl)

    def update(self, value=False):
        super(DeviceManagerView, self).update()
        all_ = not(value)

        if value or all_:
            for _, v in self.port_panels_map.items():
                v.update()
