import logging

import torch as th
import pyvisa as visa

from sknrf.enums.runtime import si_eps_map, SI
from sknrf.device.base import device_logger
from sknrf.utilities.numeric import Info, bounded_property, Domain
from sknrf.device.instrument.lfsource.dcsupply.KeysightN67xx import KeysightN67xxCWDiff


logger = device_logger(logging.getLogger(__name__))

__author__ = 'dtbespal'


class KeysightN67xxCWP2(KeysightN67xxCWDiff):
    firmware_map = {}
    display_order = ["on", "initialized", "freq", "v", "v_high"]

    def __new__(cls, error_model, port, config_filename="",
                resource_id='TCPIP0::172.16.0.10::inst0::INSTR', v_high=2.5):
        self = super(KeysightN67xxCWP2, cls).__new__(cls, error_model, port, config_filename)
        # Define object ATTRIBUTES
        self.resource_id = resource_id
        return self

    def __getnewargs__(self):
        return tuple(list(super(KeysightN67xxCWP2, self).__getnewargs__()) + [self.v_high])

    def __init__(self, error_model, port, config_filename="",
                 resource_id='TCPIP0::172.16.0.10::inst0::INSTR', v_high=2.5):
        super().__init__(error_model, port, config_filename)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self._v = th.zeros_like(self._v_)
        self.v_high = v_high
        self.initialized = True

    def __getstate__(self, state={}):
        state = super(KeysightN67xxCWP2, self).__getstate__(state=state)
        state["resource_id"] = self.resource_id
        state["v_high"] = self.v_high
        return state

    def __setstate__(self, state, *args, **kwargs):
        super().__setstate__(state)
        self.resource_id = state["resource_id"]
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self._v = self._v_
        self.v_high = state["v_high"]
        self.initialized = True

    def __info__(self):
        super(KeysightN67xxCWP2, self).__info__()
        abs_tol = 1e-3
        rel_tol = 1e-3
        self.info["v_high"] = Info("v_high", read=True, write=True, check=False, domain=Domain.TF,
                                   min_=si_eps_map[SI.V], max_=self._config["voltage_limit"][0],
                                   abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["v_high"].min, self.info["v_high"].max = 0, self._config["voltage_limit"][0]
        self.info["v_high"].abs_tol, self.info["v_high"].rel_tol = abs_tol, rel_tol

    @property
    def _on(self):
        chan = 2 * (self.port - 1) + 1
        return bool(int(self.handles["dc"].query("Output? (@%d)" % (chan,)))) and \
               bool(int(self.handles["dc"].query("Output? (@%d)" % (1,))))

    @_on.setter
    def _on(self, _on):
        chan = 2 * (self.port - 1) + 1
        self.handles["dc"].write("Output %d, (@%d)" % (int(_on), chan))
        self.handles["dc"].write("Output %d, (@%d)" % (int(_on), 1))

    @property
    def v_high(self):
        chan = 1
        return float(self.handles["dc"].query("Voltage? (@%d)" % (chan,)))

    @v_high.setter
    def v_high(self, v):
        chan = 1
        self.handles["dc"].write("Voltage %f, (@%d)" % (v, chan))
