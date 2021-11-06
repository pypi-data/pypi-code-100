import logging
import time

import torch as th
import pyvisa as visa

from sknrf.device.base import device_logger
from sknrf.device.signal import tf
from sknrf.device.instrument.lfsource import base
from sknrf.utilities.numeric import Info, bounded_property


logger = device_logger(logging.getLogger(__name__))

__author__ = 'dtbespal'


class KeysightE364xxCW(base.NoLFSource):
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
        self._v = th.zeros_like(self._v_)
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
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self._v = self._v_
        self.initialized = True

    def __info__(self):
        super(KeysightE364xxCW, self).__info__()
        abs_tol = 1e-3
        rel_tol = 1e-3
        output_index = self.output_num - 1
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["resource_id"] = Info("resource_id", read=True, write=True, check=False)
        self.info["output_num"] = Info("output_num", read=True, write=True, check=False,
                                       min_=1, max_=self._config["num_outputs"])
        self.info["_v"] = Info("_v", read=False, write=False, check=False,
                               min_=0, max_=self._config["voltage_limit"][output_index],
                               abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["v"].min, self.info["v"].max = 0, self._config["voltage_limit"][output_index]
        self.info["v"].abs_tol, self.info["v"].rel_tol = abs_tol, rel_tol

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
        self.handles["dc"].write("Instrument:Select Output%d" % (self.output_num,))
        pk = float(self.handles["dc"].query("Voltage?"))
        self._v_[:, :] = self._v_.pk(pk)
        return self._v_

    @_v.setter
    def _v(self, _v):
        _v._rms = True
        pk = tf.pk(_v).reshape(-1, 1)
        self.handles["dc"].write("Instrument:Select Output%d" % (self.output_num,))
        self.handles["dc"].write("Voltage %f" % (pk.abs(),))

    def trigger(self):
        pass
