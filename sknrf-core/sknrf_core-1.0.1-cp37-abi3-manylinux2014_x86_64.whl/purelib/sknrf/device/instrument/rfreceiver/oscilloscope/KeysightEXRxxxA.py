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
from sknrf.device.instrument.rfreceiver import base
from sknrf.device.instrument.shared.oscilloscope import KeysightEXRxxxA
from sknrf.device.instrument.shared.switch.MiniCircuits_RC_2SP6T_A12 import MiniCircuits_Switch
from sknrf.utilities.numeric import Info, bounded_property

__author__ = 'dtbespal'
logger = device_logger(logging.getLogger(__name__))


class KeysightEXRxxxAModulatedDiff(base.NoRFReceiverModulated):
    firmware_map = {}
    display_order = ["on", "initialized", "channel", "port", "freq", "a_p", "b_p", "v", "i",
                     "num_harmonics", "harmonics"]

    def __new__(cls, error_model, port, config_filename="",
                resource_id='TCPIP0::172.16.0.50::inst0::INSTR', use_switch=False):
        self = super(KeysightEXRxxxAModulatedDiff, cls).__new__(cls, error_model, port, config_filename)
        # Define object ATTRIBUTES
        self.resource_id = resource_id
        self.use_switch = use_switch
        self._on_ = False
        return self

    def __getnewargs__(self):
        return tuple(list(super(KeysightEXRxxxAModulatedDiff, self).__getnewargs__())
                     + [self.resource_id, self.use_switch])

    def __init__(self, error_model, port, config_filename="",
                 resource_id='TCPIP0::172.16.0.50::inst0::INSTR', use_switch=False):
        super().__init__(error_model, port, config_filename)
        self.resource_id = resource_id
        self.use_switch = use_switch

        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self.channel = 1
        self.measure()
        self.initialized = True

    def __getstate__(self, state={}):
        state = super(KeysightEXRxxxAModulatedDiff, self).__getstate__(state=state)
        state["channel"] = self.channel
        return state

    def __setstate__(self, state, *args, **kwargs):
        super().__setstate__(state)
        self.resource_id = state["resource_id"]
        self.use_switch = state["use_switch"]

        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self.channel = state["channel"]
        self.measure()
        self.initialized = True

    def __info__(self):
        super(KeysightEXRxxxAModulatedDiff, self).__info__()
        v_atol = 1e-3
        i_atol = v_atol/50.
        a_atol, b_atol = v_atol/np.sqrt(50.), v_atol/np.sqrt(50.)
        rtol = 1e-3
        v_max = self._config["voltage_limit"]
        i_max = v_max/50.
        a_max = b_max = v_max/np.sqrt(50.)
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["resource_id"] = Info("resource_id", read=True, write=True, check=False)
        self.info["use_switch"] = Info("use_switch", read=True, write=True, check=False)
        self.info["channel"] = Info("channel", read=True, write=True, check=False, min_=0, max_=6)
        self.info["_a_p"] = Info("_a_p", read=False, write=False, check=False,
                                 min_=si_eps_map[SI.A], max_=a_max, abs_tol=a_atol, rel_tol=rtol)
        self.info["_b_p"] = Info("_b", read=False, write=False, check=False,
                                 min_=si_eps_map[SI.B], max_=b_max, abs_tol=b_atol, rel_tol=rtol)
        self.info["_v"] = Info("_v", read=False, write=False, check=False,
                               min_=si_eps_map[SI.V], max_=v_max, abs_tol=v_atol, rel_tol=rtol)
        self.info["_i"] = Info("_i", read=False, write=False, check=False,
                               min_=si_eps_map[SI.I], max_=i_max, abs_tol=i_atol, rel_tol=rtol)
        self.info["a_p"].min, self.info["a_p"].max = 0., a_max
        self.info["b_p"].min, self.info["b_p"].max = 0., b_max
        self.info["v"].min, self.info["v"].max = 0, v_max
        self.info["i"].min, self.info["i"].max = 0, i_max

    def connect_handles(self):
        rm = visa.ResourceManager(os.environ["VISA_LIB"])
        self.handles["scope"] = rm.open_resource(self.resource_id)
        if self.use_switch:
            self.handles["switch"] = MiniCircuits_Switch()
        super(KeysightEXRxxxAModulatedDiff, self).connect_handles()

    def preset(self):
        super(KeysightEXRxxxAModulatedDiff, self).preset()
        if self.unique_handle(self.handles["scope"]):
            KeysightEXRxxxA.preset(self)
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

        p_chan, n_chan = 2 * (self.port - 1) + 1, 2 * (self.port - 1) + 2
        self.handles["scope"].write(":CHANnel%d:INPut DC" % (p_chan,))  # DC Coupling
        self.handles["scope"].write(":CHANnel%d:INPut %s" % (p_chan, self._config["z0"]))
        self.handles["scope"].write(":CHANnel%d:OFFSet %d" % (p_chan, 0.0))
        self.handles["scope"].write(":CHANnel%d:RANGe %d" % (p_chan, limit))
        self.handles["scope"].write(":CHANnel%d:UNITs %s" % (p_chan, unit_str))
        self.handles["scope"].write(":WAVeform:SOURce CHANnel%d" % (p_chan,))
        self.handles["scope"].query("*OPC?")

        self.handles["scope"].write(":CHANnel%d:INPut DC" % (n_chan,))  # DC Coupling
        self.handles["scope"].write(":CHANnel%d:INPut %s" % (n_chan, self._config["z0"]))
        self.handles["scope"].write(":CHANnel%d:OFFSet %d" % (n_chan, 0.0))
        self.handles["scope"].write(":CHANnel%d:RANGe %d" % (n_chan, limit))
        self.handles["scope"].write(":CHANnel%d:UNITs %s" % (n_chan, unit_str))
        self.handles["scope"].write(":WAVeform:SOURce CHANnel%d" % (n_chan,))
        self.handles["scope"].query("*OPC?")

    @property
    def channel(self):
        if "switch" in self.handles:
            p_chan, n_chan = 2 * (self.port - 1) + 1, 2 * (self.port - 1) + 2
            return self.handles["switch"].switch(p_chan)
        else:
            return 0

    @channel.setter
    def channel(self, channel):
        if "switch" in self.handles:
            p_chan, n_chan = 2 * (self.port - 1) + 1, 2 * (self.port - 1) + 2
            self.handles["switch"].set_switch(p_chan, channel)
            self.handles["switch"].set_switch(n_chan, channel)

    @property
    def _on(self):
        p_chan, n_chan = 2 * (self.port - 1) + 1, 2 * (self.port - 1) + 2
        return bool(int(self.handles["scope"].query(":CHANnel%d:DISPlay?" % (p_chan))) and
                    int(self.handles["scope"].query(":CHANnel%d:DISPlay?" % (n_chan))))

    @_on.setter
    def _on(self, _on):
        p_chan, n_chan = 2 * (self.port - 1) + 1, 2 * (self.port - 1) + 2
        self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (p_chan, int(_on)))
        self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (n_chan, int(_on)))
        self._on_ = _on

    @bounded_property
    def _a_p(self):
        return self._a_p_

    @bounded_property
    def _b_p(self):
        return self._b_p_

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
        KeysightEXRxxxA.arm(self)

    def trigger(self):
        KeysightEXRxxxA.trigger(self)

    def _acquisition_done(self):
        return not bool(int(self.handles["scope"].query(":OPERegister:CONDition?")) & 8)

    def measure(self):
        while not self._acquisition_done():
            time.sleep(0.1)
        t_points = self._b_p_.shape[-2]
        t_reps = t_points / Settings().t_points
        t_stop = t_reps * Settings().t_stop
        p_chan, n_chan = 2 * (self.port - 1) + 1, 2 * (self.port - 1) + 2
        try:
            self.handles["scope"].write(":WAVeform:SOURce CHANnel%d" % (p_chan,))
            preamble = self.handles["scope"].query(":WAVeform:PREamble?")
            preamble_list = preamble.split(",")
            if len(preamble_list) != 24:
                return
            format_, type_, points, avg,\
            x_step, x_origin, x_ref, y_step, y_origin, y_ref, coupling,\
            x_disp_range, x_disp_origin, y_disp_range, y_disp_origin, date, time_, frame_model, acquisition_mode, \
            completion, x_units, y_units, max_bw_lim, min_bw_lim = preamble_list
            t_old = (np.arange(0, float(points), dtype=np.float) - float(x_ref)) * float(x_step) + float(x_origin)
            t_new = np.linspace(0, t_stop, t_points)

            data_bytes = bytearray(self.handles["scope"].query_binary_values(":WAVeform:DATA?", datatype='s'))
            b_p = np.frombuffer(data_bytes, dtype=">i2")
            b_p = (b_p - float(y_ref)) * float(y_step) + float(y_origin)
            b_p = interp1d(t_old, b_p, "nearest")(t_new)
            b_p = b_p.reshape(-1, 1)/np.sqrt(50.)

            self.handles["scope"].write(":WAVeform:SOURce CHANnel%d" % (n_chan,))
            data_bytes = bytearray(self.handles["scope"].query_binary_values(":WAVeform:DATA?", datatype='s'))
            b_n = np.frombuffer(data_bytes, dtype=">i2")
            b_n = (b_n - float(y_ref)) * float(y_step) + float(y_origin)
            b_n = interp1d(t_old, b_n, "nearest")(t_new)
            b_n = b_n.reshape(-1, 1)/np.sqrt(50.)
        except VisaIOError:
            self.handles["scope"].clear()
            return

        if not self._on_:
            self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (p_chan, int(self._on_)))
            self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (n_chan, int(self._on_)))
        self._b_p_[:, 0:1] = th.as_tensor(b_p - b_n)
        self._a_p_[:, 0:1] = 0.0

        super().measure()
