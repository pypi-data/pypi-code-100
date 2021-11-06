import os
import logging
from enum import Enum

import numpy as np
import torch as th
import pyvisa as visa

from sknrf.enums.runtime import SI, si_eps_map
from sknrf.settings import Settings
from sknrf.device.base import device_logger
from sknrf.device.instrument.lfsource import base
from sknrf.device.instrument.shared.awg import Keysight33xxx
from sknrf.device.signal import tf
from sknrf.utilities.numeric import Info, bounded_property


logger = device_logger(logging.getLogger(__name__))

__author__ = 'dtbespal'


def scale(x, x_min, x_max, y_min=-1.0, y_max=1.0):
    return (x - x_min)/(x_max - x_min)*(y_max - y_min) + y_min


class OutputFilter(Enum):
    OFF = 0
    NORM = 1
    STEP = 2


class Keysight33xxxModulated(base.NoLFSourceModulated):
    firmware_map = {}
    display_order = ["on", "initialized", "port", "freq", "v",
                     "delay", "pulse_width",
                     "iq_files",
                     "output_filter"]

    def __new__(cls, error_model, port, config_filename="",
                resource_id='TCPIP0::172.16.0.10::inst0::INSTR'):
        self = super(Keysight33xxxModulated, cls).__new__(cls, error_model, port, config_filename)
        # Define object ATTRIBUTES
        self.resource_id = resource_id
        return self

    def __getnewargs__(self):
        return tuple(list(super(Keysight33xxxModulated, self).__getnewargs__()) + [self.resource_id])

    def __init__(self, error_model, port, config_filename="",
                 resource_id='TCPIP0::172.16.0.10::inst0::INSTR'):
        super().__init__(error_model, port, config_filename)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self._pulse_width = self.period
        self._delay = 0.0
        self.iq_files = self._iq_files_
        self._v = th.zeros_like(self._v_)
        self.initialized = True

    def __getstate__(self, state={}):
        state = super(Keysight33xxxModulated, self).__getstate__(state=state)
        return state

    def __setstate__(self, state, *args, **kwargs):
        super().__setstate__(state)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self._pulse_width = state["_pulse_width"]
        self._delay = state["_delay"]
        self.iq_files = state["iq_files"]
        self._v = self._v_
        self.initialized = True

    def __info__(self):
        super(Keysight33xxxModulated, self).__info__()
        abs_tol = 1e-3
        rel_tol = 1/2**16
        v_max = self._config["voltage_limit"]
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["resource_id"] = Info("resource_id", read=True, write=True, check=False)
        self.info["_v"] = Info("_v", read=False, write=False, check=False,
                               min_=si_eps_map[SI.V], max_=v_max, abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["v"].min, self.info["v"].max = si_eps_map[SI.V], v_max
        self.info["v"].abs_tol, self.info["v"].rel_tol = abs_tol, rel_tol

    def connect_handles(self):
        rm = visa.ResourceManager(os.environ["VISA_LIB"])
        self.handles["awg"] = rm.open_resource(self.resource_id)
        super(Keysight33xxxModulated, self).connect_handles()

    def preset(self):
        super(Keysight33xxxModulated, self).preset()
        if self.unique_handle(self.handles['awg']):
            Keysight33xxx.preset(self)
        self.handles["awg"].write("SOURCE1:FUNCtion:ARBitrary:FILTer NORMAL")  # NORMAL (27%BW) | STEP (13%BW) | OFF
        self.handles["awg"].write("SOURCE2:FUNCtion:ARBitrary:FILTer NORMAL")  # NORMAL (27%BW) | STEP (13%BW) | OFF
        self.handles["awg"].write("OUTPut%d:LOAD %d" % (1, 50))
        self.handles["awg"].write("OUTPut%d:LOAD %d" % (2, 50))
        self.handles["awg"].query("*OPC?")

    @property
    def _on(self):
        return bool(int(self.handles["awg"].query("OUTPut1?"))) and bool(int(self.handles["awg"].query("OUTPut2?")))

    @_on.setter
    def _on(self, _on):
        self.handles["awg"].write("OUTPut1 %d" % (int(_on),))
        self.handles["awg"].write("OUTPut2 %d" % (int(_on),))

    @bounded_property
    def _v(self):
        return self._v_

    @_v.setter
    def _v(self, _v):
        atol, rtol = self.info["_v"].abs_tol, self.info["_v"].rel_tol
        t_points = int(Settings().t_points*self._config["resample"])
        end = t_points + 32 - t_points % 32  # Minimum 64 bytes
        v_r_max, v_r_min = _v.real.max().item(), _v.real.min().item()
        v_i_max, v_i_min = _v.imag.max().item(), _v.imag.min().item()
        iq = np.asarray(tf.iq(_v)).reshape(-1)
        iq.dtype = np.float  # Interleave IQ
        iq = iq[::int(1 / self._config["resample"])]
        encoding = ">i2"
        iq = np.round(iq * (32767 / np.max(np.abs(iq))))
        iq = iq.astype(encoding)
        i = np.zeros(end, dtype=encoding)
        q = np.zeros(end, dtype=encoding)
        i[0:t_points] = iq[0:2 * t_points:2]
        q[0:t_points] = iq[1:2 * t_points + 1:2]

        # This prevents min and max from equal during scaling.
        if np.isclose(v_r_max, v_r_min, atol=atol, rtol=rtol):
            v_r_max = v_r_min + atol
        if np.isclose(v_i_max, v_i_min, atol=atol, rtol=rtol):
            v_i_max = v_i_min + atol

        i_bytes = i.tobytes()
        q_bytes = q.tobytes()
        n_bytes = str(len(i_bytes)).encode()
        prefix = str(len(n_bytes)).encode()
        self.handles["awg"].write("SOURCE1:DATA:VOLatile:CLEar")
        self.handles["awg"].write("SOURCE2:DATA:VOLatile:CLEar")
        self.handles["awg"].query("*OPC?")
        self.handles["awg"].write_raw(b"SOURCE1:DATA:ARB:DAC MODULATED_I, #" + prefix + n_bytes + i_bytes)
        self.handles["awg"].write_raw(b"SOURCE2:DATA:ARB:DAC MODULATED_Q, #" + prefix + n_bytes + q_bytes)
        self.handles["awg"].write('SOURCE1:FUNCtion:ARBitrary "MODULATED_I"')
        self.handles["awg"].write('SOURCE2:FUNCtion:ARBitrary "MODULATED_Q"')
        self.handles["awg"].query("*OPC?")
        if end > t_points:
            v_r_max, v_r_min = max(0, v_r_max), min(0, v_r_min)
            v_i_max, v_i_min = max(0, v_i_max), min(0, v_i_min)
        self.handles["awg"].write("SOURCE1:VOLTage:HIGH %.4f;:SOURCE1:VOLTage:LOW %.4f" % (v_r_max, v_r_min))
        self.handles["awg"].write("SOURCE2:VOLTage:HIGH %.4f;:SOURCE2:VOLTage:LOW %.4f" % (v_i_max, v_i_min))
        self.handles["awg"].query("*OPC?")
        self._v_[:, :] = _v

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

    @property
    def output_filter(self):
        filter_str = self.handles["awg"].query("SOURCE1:FUNCtion:ARBitrary:FILTer?").strip("\n")
        return OutputFilter.__members__[filter_str]

    @output_filter.setter
    def output_filter(self, filter_):
        self.handles["awg"].write("SOURCE1:FUNCtion:ARBitrary:FILTer %s" % filter_._name_)
        self.handles["awg"].write("SOURCE2:FUNCtion:ARBitrary:FILTer %s" % filter_._name_)

    def arm(self):
        Keysight33xxx.arm(self)

    def trigger(self):
        Keysight33xxx.trigger(self)
