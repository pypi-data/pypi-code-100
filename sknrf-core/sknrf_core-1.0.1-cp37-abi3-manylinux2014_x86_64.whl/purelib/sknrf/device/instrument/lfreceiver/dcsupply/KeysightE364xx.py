import logging
import time

import numpy as np
import pyvisa as visa
from pyvisa.errors import VisaIOError

from sknrf.enums.device import Response
from sknrf.settings import Settings
from sknrf.device import AbstractDevice
from sknrf.device.base import device_logger
from sknrf.device.instrument.lfreceiver import base
from sknrf.utilities.numeric import AttributeInfo, Info, PkAvg, Format, bounded_property

__author__ = 'dtbespal'
logger = device_logger(logging.getLogger(__name__))


class KeysightE364xxCW(base.NoLFReceiver):
    firmware_map = {}
    display_order = ["on", "initialized", "freq", "v"]

    def __new__(cls, error_model, port, config_filename="",
                resource_id='GPIB0::5::INSTR', output_num=1):
        self = super(KeysightE364xxCW, cls).__new__(cls, error_model, port, config_filename)
        # Define object ATTRIBUTES
        self.resource_id = resource_id
        self.output_num = output_num
        return self

    def __getnewargs__(self):
        return tuple(list(super(KeysightE364xxCW, self).__getnewargs__()) + [self.resource_id, self.output_num])

    def __init__(self, error_model, port, config_filename="",
                 resource_id='GPIB0::5::INSTR', output_num=1):
        super().__init__(error_model, port, config_filename)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self.measure()
        self.initialized = True

    def __getstate__(self, state={}):
        state = super(KeysightE364xxCW, self).__getstate__(state=state)
        state["resource_id"] = self.resource_id
        state["output_num"] = self.output_num
        return state

    def __setstate__(self, state, *args, **kwargs):
        super().__setstate__(state)
        self.resource_id = state["resource_id"]
        self.output_num = state["output_num"]
        self.connect_handles()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self.measure()
        self.initialized = True

    def __info__(self):
        super(KeysightE364xxCW, self).__info__()
        abs_tol = 1e-3
        rel_tol = 1e-3
        output_index = self.output_num - 1
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["_v"] = Info("_v", read=False, write=False, check=False,
                               min_=0, max_=self._config["voltage_limit"][output_index],
                               abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["_i"] = Info("_i", read=False, write=False, check=False,
                               min_=0, max_=self._config["current_limit"][output_index],
                               abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["v"].min, self.info["v"].max = 0, self._config["voltage_limit"][output_index]
        self.info["i"].min, self.info["i"].max = 0, self._config["current_limit"][output_index]

    def connect_handles(self):
        rm = visa.ResourceManager()
        self.handles["dc"] = rm.open_resource(self.resource_id)
        super(KeysightE364xxCW, self).connect_handles()

    def preset(self):
        super(KeysightE364xxCW, self).preset()
        if self.unique_handle(self.handles["dc"]):
            timeout = self.handles["dc"].timeout
            self.handles["dc"].write("*RST")
            self.handles["dc"].write("*CLS")
            time.sleep(5)
            self.handles["dc"].query("*OPC?")
            self.handles["dc"].timeout = timeout

            for output_index in range(self._config["num_outputs"]):
                output_num = output_index + 1
                self.handles["dc"].write("Instrument:Select Output%d" % (output_num,))
                self.handles["dc"].write("Voltage:Range %s" % (self._config["voltage_range"][output_index],))
                self.handles["dc"].write("Voltage:Protection:Level %f" % (self._config["voltage_limit"][output_index],))
                self.handles["dc"].write("Current:Level %f" % (self._config["current_limit"][output_index],))
                self.handles["dc"].write("Voltage:Protection:State 1")
                self.handles["dc"].write("Voltage %f" % (0.0,))
                self.handles["dc"].query("*OPC?")

    @property
    def _on(self):
        return bool(int(self.handles["dc"].query("Output?")))

    @_on.setter
    def _on(self, _on):
        self.handles["dc"].write("Instrument:Select Output%d" % (self.output_num,))
        self.handles["dc"].write("Output %d" % (int(_on),))

    @bounded_property
    def _v(self):
        return self._v_

    @bounded_property
    def _i(self):
        return self._i_

    def trigger(self):
        pass

    def measure(self):
        self.handles["dc"].write("Instrument:Select Output%d" % (self.output_num,))
        _v_ = float(self.handles["dc"].query("MEASure:Scalar:Voltage?"))
        _i_ = float(self.handles["dc"].query("MEASure:Scalar:Current?"))
        self._v_[:, :] = _v_
        self._i_[:, :] = _i_