import os
import logging

import torch as th
import pyvisa as visa

from sknrf.enums.runtime import si_eps_map, SI
from sknrf.device.base import device_logger
from sknrf.device.signal import tf
from sknrf.device.instrument.lfsource import base
from sknrf.utilities.numeric import Info, bounded_property, Domain, Format, Scale, PkAvg


logger = device_logger(logging.getLogger(__name__))

__author__ = 'dtbespal'


class KeysightN67xx_E363xxxCW(base.NoLFSource):
    firmware_map = {}
    display_order = ["on", "initialized", "freq", "v", "v2"]

    def __new__(cls, error_model, port, config_filename="",
                resource_id='TCPIP0::172.16.0.10::inst0::INSTR',
                resource_id2='TCPIP0::172.16.0.12::inst0::INSTR'):
        self = super(KeysightN67xx_E363xxxCW, cls).__new__(cls, error_model, port, config_filename)
        # Define object ATTRIBUTES
        self.resource_id = resource_id
        self.resource_id2 = resource_id2
        return self

    def __getnewargs__(self):
        return tuple(list(super(KeysightN67xx_E363xxxCW, self).__getnewargs__()) + [self.resource_id])

    def __init__(self, error_model, port, config_filename="",
                 resource_id='TCPIP0::172.16.0.10::inst0::INSTR',
                 resource_id2='TCPIP0::172.16.0.12::inst0::INSTR'):
        super().__init__(error_model, port, config_filename)
        if self.__class__ == KeysightN67xx_E363xxxCW:
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._v = th.zeros_like(self._v_)
            self._v2 = th.zeros_like(self._v_)
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(KeysightN67xx_E363xxxCW, self).__getstate__(state=state)
        state["resource_id"] = self.resource_id
        state["resource_id2"] = self.resource_id2
        state["v2"] = float(tf.pk(self.v2).item())
        return state

    def __setstate__(self, state, *args, **kwargs):
        super().__setstate__(state)
        if self.__class__ == KeysightN67xx_E363xxxCW:
            self.resource_id = state["resource_id"]
            self.resource_id2 = state["resource_id2"]
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._v = self._v_
            self._v2 = th.full_like(self._v_, state["v2"])
            self.initialized = True

    def __info__(self):
        super(KeysightN67xx_E363xxxCW, self).__info__()
        abs_tol = 1e-3
        rel_tol = 1e-3
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["resource_id"] = Info("resource_id", read=True, write=True, check=False)
        self.info["resource_id2"] = Info("resource_id2", read=True, write=True, check=False)
        self.info["_v"] = Info("_v", read=False, write=False, check=False, domain=Domain.TF,
                               min_=si_eps_map[SI.V], max_=self._config["voltage_limit"],
                               abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["v"].min, self.info["v"].max = 0, self._config["voltage_limit"]
        self.info["v"].abs_tol, self.info["v"].rel_tol = abs_tol, rel_tol
        self.info["_v2"] = Info("_v2", read=True, write=True, check=True, domain=Domain.TF,
                                format_=Format.LIN_DEG, scale=Scale._, unit="V", pk_avg=PkAvg.PK,
                                min_=si_eps_map[SI.V], max_=self._config["voltage_limit2"], abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["v2"] = Info("v2", read=True, write=True, check=True, domain=Domain.TF,
                               format_=Format.LIN_DEG, scale=Scale._, unit="V", pk_avg=PkAvg.PK,
                               min_=si_eps_map[SI.V], abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["v2"].min, self.info["v2"].max = 0, self._config["voltage_limit2"]
        self.info["v2"].abs_tol, self.info["v2"].rel_tol = abs_tol, rel_tol

    def connect_handles(self):
        rm = visa.ResourceManager("@py")
        self.handles["dc"] = rm.open_resource(self.resource_id)
        self.handles["dc2"] = rm.open_resource(self.resource_id2)
        super(KeysightN67xx_E363xxxCW, self).connect_handles()

    def preset(self):
        super(KeysightN67xx_E363xxxCW, self).preset()
        if self.unique_handle(self.handles["dc"]):
            self.handles["dc"].write("*RST")
            self.handles["dc"].write("*CLS")
            self.handles["dc"].query("*OPC?")
            assert("N6702C" in self.handles["dc"].query("*IDN?"))
            self.handles["dc"].write("DISPlay:VIEW METER4")

            for index in range(self._config["num_outputs"]):
                chan = 2*index + 1
                self.handles["dc"].write("Output:Protection:Clear (@%d)" % (chan,))
                self.handles["dc"].write("Current:Level %f, (@%d)" % (self._config["current_limit"], chan))
                self.handles["dc"].write("Current:Protection:State %d, (@%d)" % (int(True), chan))
                self.handles["dc"].write("Voltage:Protection:Level %f, (@%d)" % (self._config["voltage_limit"], chan))
                self.handles["dc"].write("Voltage %f, (@%d)" % (0.0, chan))
                self.handles["dc"].query("*OPC?")

        if self.unique_handle(self.handles["dc2"]):
            self.handles["dc2"].write("*RST")
            self.handles["dc2"].write("*CLS")
            self.handles["dc2"].query("*OPC?")
            assert("E36" in self.handles["dc2"].query("*IDN?"))

            for index in range(self._config["num_outputs"]):
                chan = index + 1
                self.handles["dc2"].write("Output:Protection:Clear (@%d)" % (chan,))
                self.handles["dc2"].write("Current:Level %f, (@%d)" % (self._config["current_limit2"], chan))
                self.handles["dc2"].write("Current:Protection:State %d, (@%d)" % (int(True), chan))
                self.handles["dc2"].write("Voltage:Protection:Level %f, (@%d)" % (self._config["voltage_limit2"], chan))
                self.handles["dc2"].write("Voltage %f, (@%d)" % (0.0, chan))
                self.handles["dc2"].query("*OPC?")

    @property
    def _on(self):
        status = False
        for index in range(self._config["num_outputs"]):
            chan = 2*index + 1
            status |= bool(int(self.handles["dc"].query("Output? (@%d)" % (chan,))))
        for index in range(self._config["num_outputs"]):
            chan = index + 1
            status |= bool(int(self.handles["dc2"].query("Output? (@%d)" % (chan,))))
        return status

    @_on.setter
    def _on(self, _on):
        for index in range(self._config["num_outputs"]):
            chan = index + 1
            self.handles["dc2"].write("Output %d, (@%d)" % (int(_on), chan))
        for index in range(self._config["num_outputs"]):
            chan = 2*index + 1
            self.handles["dc"].write("Output %d, (@%d)" % (int(_on), chan))

    @bounded_property
    def _v(self):
        pk = th.zeros((2,), dtype=self._v_.dtype)
        for index in range(self._config["num_outputs"]):
            chan = 2*index + 1
            pk[index] = float(self.handles["dc"].query("Voltage? (@%d)" % (chan,)))
        self._v_[:, :] = self._v_.pk(pk.mean())
        return self._v_

    @_v.setter
    def _v(self, _v):
        pk = tf.pk(_v).reshape(-1, 1).abs()
        for index in range(self._config["num_outputs"]):
            chan = 2*index + 1
            self.handles["dc"].write("Voltage %f, (@%d)" % (pk, chan))

    @bounded_property
    def _v2(self):
        pk = th.zeros((2,), dtype=self._v_.dtype)
        for index in range(self._config["num_outputs"]):
            chan = index + 1
            pk[index] = float(self.handles["dc2"].query("Voltage? (@%d)" % (chan,)))
        return th.full_like(self._v_, max(float(pk.mean()), si_eps_map[SI.V]))

    @_v2.setter
    def _v2(self, _v):
        pk = tf.pk(_v).reshape(-1, 1).abs()
        for index in range(self._config["num_outputs"]):
            chan = index + 1
            self.handles["dc2"].write("Voltage %f, (@%d)" % (pk, chan))

    @bounded_property
    def v2(self):
        return self._v2

    @v2.setter
    def v2(self, v):
        self._v2 = v

    def trigger(self):
        pass
