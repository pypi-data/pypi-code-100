import logging
import time
import os

import numpy as np
import torch as th
from scipy.interpolate import interp1d
import pyvisa as visa
from pyvisa.errors import VisaIOError

from sknrf.enums.device import SI, si_eps_map, ReceiverZ
from sknrf.settings import Settings
from sknrf.device.base import device_logger
from sknrf.device.instrument.lfreceiver import base
from sknrf.device.instrument.shared.oscilloscope import KeysightDSOX6xxxA
from sknrf.device.instrument.shared.switch.MiniCircuits_RC_2SP6T_A12 import MiniCircuits_Switch
from sknrf.utilities.numeric import Info, bounded_property

__author__ = 'dtbespal'
logger = device_logger(logging.getLogger(__name__))


class KeysightDSOX6xxxAModulated(base.NoLFReceiverModulated):
    firmware_map = {}
    display_order = ["on", "initialized", "channel", "freq", "v", "i"]

    def __new__(cls, error_model, port, config_filename="",
                # resource_id='TCPIP0::172.16.0.20::inst0::INSTR', switch_id='USB0::0x20CE::0x0022::bef34d4RAW'
                resource_id='TCPIP0::172.16.0.20::inst0::INSTR', switch_id=''):
        self = super(KeysightDSOX6xxxAModulated, cls).__new__(cls, error_model, port, config_filename)
        # Define object ATTRIBUTES
        self.resource_id = resource_id
        self.switch_id = switch_id
        self._on_ = False
        return self

    def __getnewargs__(self):
        return tuple(list(super(KeysightDSOX6xxxAModulated, self).__getnewargs__())
                     + [self.resource_id, self.switch_id])

    def __init__(self, error_model, port, config_filename="",
                 # resource_id='TCPIP0::172.16.0.20::inst0::INSTR', switch_id='USB0::0x20CE::0x0022::bef34d4RAW'):
                 resource_id='TCPIP0::172.16.0.20::inst0::INSTR', switch_id=''):
        super().__init__(error_model, port, config_filename)
        self.resource_id = resource_id
        self.switch_id = switch_id

        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self.channel = 1
        self.measure()
        self.initialized = True

    def __getstate__(self, state={}):
        state = super(KeysightDSOX6xxxAModulated, self).__getstate__(state=state)
        state["channel"] = self.channel
        return state

    def __setstate__(self, state, *args, **kwargs):
        super().__setstate__(state)
        self.resource_id = state["resource_id"]
        self.switch_id = state["switch_id"]

        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self.channel = state["channel"]
        self.measure()
        self.initialized = True

    def __info__(self):
        super(KeysightDSOX6xxxAModulated, self).__info__()
        abs_tol = 1e-3
        rel_tol = 1e-3
        v_max = self._config["voltage_limit"]
        i_max = self._config["current_limit"]
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["resource_id"] = Info("resource_id", read=True, write=True, check=False)
        self.info["switch_id"] = Info("switch_id", read=True, write=True, check=False)
        self.info["channel"] = Info("channel", read=True, write=True, check=False,
                                    min_=0, max_=6)
        self.info["z0"] = Info("z0", read=True, write=False, check=False)
        self.info["_v"] = Info("_v", read=False, write=False, check=False,
                               min_=si_eps_map[SI.V], max_=v_max,
                               abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["_i"] = Info("_i", read=False, write=False, check=False,
                               min_=si_eps_map[SI.I], max_=i_max,
                               abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["v"].min, self.info["v"].max = 0., v_max
        self.info["i"].min, self.info["i"].max = 0., i_max

    def connect_handles(self):
        rm = visa.ResourceManager(os.environ["VISA_LIB"])
        self.handles["scope"] = rm.open_resource(self.resource_id)
        if len(self.switch_id):
            self.handles["switch"] = MiniCircuits_Switch()
        super(KeysightDSOX6xxxAModulated, self).connect_handles()

    def preset(self):
        super(KeysightDSOX6xxxAModulated, self).preset()
        if self.unique_handle(self.handles["scope"]):
            KeysightDSOX6xxxA.preset(self)
        if "switch" in self.handles and self.unique_handle(self.handles["switch"]):
            MiniCircuits_Switch.preset(self.handles["switch"])

        # Channel
        aten = self._config["attenuation"]
        unit = self._config["unit"]
        unit_str = "VOLT" if unit == "V" else "AMPere"
        if unit == "V":
            limit = 2 * self._config["voltage_limit"]
        else:
            limit = 2 * self._config["current_limit"]
        self.handles["scope"].write(":CHANnel%d:COUPling DC" % (self.port,))  # DC Coupling
        self.handles["scope"].write(":CHANnel%d:INPut %s" % (self.port, self._config["z0"]))
        self.handles["scope"].write(":CHANnel%d:PROBe %f" % (self.port, aten))
        self.handles["scope"].write(":CHANnel%d:OFFSet %d" % (self.port, 0.0))
        self.handles["scope"].write(":CHANnel%d:RANGe %d" % (self.port, limit))
        self.handles["scope"].write(":CHANnel%d:UNITs %s" % (self.port, unit_str))
        self.handles["scope"].write(":WAVeform:SOURce CHANnel%d" % (self.port,))
        self.handles["scope"].query("*OPC?")

    @property
    def channel(self):
        if "switch" in self.handles:
            return self.handles["switch"].switch(self.port)
        else:
            return 0

    @channel.setter
    def channel(self, channel):
        if "switch" in self.handles:
            self.handles["switch"].set_switch(self.port, channel)

    @property
    def _on(self):
        return bool(int(self.handles["scope"].query(":CHANnel%d:DISPlay?" % (self.port,))))

    @_on.setter
    def _on(self, _on):
        self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (self.port, int(_on)))
        self._on_ = _on

    @bounded_property
    def _v(self):
        return self._v_

    @bounded_property
    def _i(self):
        return self._i_

    @property
    def z0(self):
        z_str = self.handles["scope"].query(":CHANnel%d:INPut?" % (self.port,))
        return ReceiverZ._1MOhm if z_str == "ONEMeg" else ReceiverZ._50Ohm

    @property
    def _delay(self):
        return self._delay_

    @_delay.setter
    def _delay(self, _delay):
        self._delay_ = _delay

    @property
    def _pulse_width(self):
        return self._pulse_width_

    @_pulse_width.setter
    def _pulse_width(self, _pulse_width):
        self._pulse_width_ = _pulse_width

    def arm(self):
        KeysightDSOX6xxxA.arm(self)

    def trigger(self):
        KeysightDSOX6xxxA.trigger(self)

    def _acquisition_done(self):
        return not bool(int(self.handles["scope"].query(":OPERegister:CONDition?")) & 8)

    def measure(self):
        while not self._acquisition_done():
            time.sleep(0.1)

        try:
            self.handles["scope"].write(":WAVeform:SOURce CHANnel%d" % (self.port,))  # Set the waveform source
            preamble = self.handles["scope"].query(":WAVeform:PREamble?")
            format_, type_, points, avg, x_step, x_origin, x_ref, y_step, y_origin, y_ref = preamble.split(",")
            t_old = (np.arange(0, float(points), dtype=np.float) - float(x_ref)) * float(x_step) + float(x_origin)
            t_new = np.linspace(0, Settings().t_stop, Settings().t_points)
            data_bytes = bytearray(self.handles["scope"].query_binary_values(":WAVeform:DATA?", datatype='s'))
            v_i = np.frombuffer(data_bytes, dtype=">u2")
            v_i = (v_i - float(y_ref)) * float(y_step) + float(y_origin)
            v_i = interp1d(t_old, v_i, "nearest")(t_new)
        except VisaIOError:
            self.handles["scope"].clear()
            return

        if not self._on_:
            self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (self.port, int(self._on_)))
        self._v_[:, 0:1] = th.as_tensor(v_i.reshape(-1, 1))

        super().measure()
