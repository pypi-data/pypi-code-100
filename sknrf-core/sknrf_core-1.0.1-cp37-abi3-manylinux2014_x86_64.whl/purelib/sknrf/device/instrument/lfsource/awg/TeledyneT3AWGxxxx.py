import os
import logging

import numpy as np
import torch as th
import pyvisa as visa

from sknrf.settings import Settings
from sknrf.device.base import device_logger
from sknrf.utilities.numeric import Info, bounded_property
from sknrf.enums.runtime import SI, si_eps_map
from sknrf.device.instrument.lfsource import base
from sknrf.device.instrument.shared.awg import TeledyneT3AWGxxxx
from sknrf.device.signal import tf, ff
from sknrf.utilities.rf import dBU2rU


logger = device_logger(logging.getLogger(__name__))

__author__ = 'dtbespal'


class TeledyneT3AWGxxxxModulated(base.NoLFSourceModulated):
    firmware_map = {}
    display_order = ["on", "initialized", "port", "freq", "v",
                     "delay", "pulse_width", "period",
                     "iq_files"]

    def __new__(cls, error_model, port, config_filename="",
                resource_id='TCPIP0::172.16.0.40::inst0::INSTR'):
        self = super(TeledyneT3AWGxxxxModulated, cls).__new__(cls, error_model, port, config_filename)
        # Define object ATTRIBUTES
        self.resource_id = resource_id
        return self

    def __getnewargs__(self):
        return tuple(list(super(TeledyneT3AWGxxxxModulated, self).__getnewargs__()) + [self.resource_id])

    def __init__(self, error_model, port, config_filename="",
                 resource_id='TCPIP0::172.16.0.40::inst0::INSTR'):
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
        state = super(TeledyneT3AWGxxxxModulated, self).__getstate__(state=state)
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
        super(TeledyneT3AWGxxxxModulated, self).__info__()
        abs_tol = 1e-1
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
        super(TeledyneT3AWGxxxxModulated, self).connect_handles()

    def preset(self):
        super(TeledyneT3AWGxxxxModulated, self).preset()
        if self.unique_handle(self.handles['awg']):
            TeledyneT3AWGxxxx.preset(self)

        self.handles["awg"].write("OUTPut%d:SERIESIMPedance %s" % (self.port, "50Ohm"))
        self.handles["awg"].write("OUTPut%d:DELay %fps" % (self.port, self._config["trigger_delay"]/1e-12))
        self.handles["awg"].write("DISPlay:UNIT:VOLT AMPLitudeoff")
        self.handles["awg"].write("SEQuence:ELEM1:OFFSET%d %f;AMPlitude%d %f" % (self.port, 0.0, self.port, 0.0))
        self.handles["awg"].query("*OPC?")

    @property
    def _on(self):
        return bool(int(self.handles["awg"].query("OUTPut%d:STATe?" % (self.port,))))

    @_on.setter
    def _on(self, _on):
        self.handles["awg"].write("OUTPut%d:STATe %d" % (self.port, int(_on),))

    @bounded_property
    def _v(self):
        return tf.pk(self._v_)

    @_v.setter
    def _v(self, _v):
        _v = _v.detach()
        t_points = int(Settings().t_points*self._config["resample"])
        end = t_points + 16 - t_points % 16
        v_r_max, v_r_min = _v.real.max().item(), _v.real.min().item()
        v_i_max, v_i_min = _v.imag.max().item(), _v.imag.min().item()
        iq = tf.iq(_v).numpy().reshape(-1)
        iq.dtype = np.float  # Interleave IQ
        iq = iq[::int(1/self._config["resample"])]
        encoding = "<i2"  # Convert to little endian int16
        iq = np.round(iq * (32767 / np.max(np.abs(iq))))  # Scaling
        iq = iq.astype(encoding)
        i = np.zeros(end, dtype=encoding)
        i[0:t_points] = iq[0:2*t_points:2]

        waveform = "_".join((self.__class__.__name__, str(self.port), "i"))
        i_bytes = '\r\n'.join(i.astype(str)).encode()
        n_bytes = str(len(i_bytes)).encode()
        prefix = str(len(n_bytes)).encode()
        self.handles["awg"].write('WLISt:WAVeform:DELete "%s"' % (waveform,))
        self.handles["awg"].write(r'MMEM:DOWN:FNAM "%s.txt"' % (waveform,))
        TeledyneT3AWGxxxx.download_waveform_bug(self, b'MMEM:DOWN:DATA #' + prefix + n_bytes + i_bytes)
        self.handles["awg"].write('WLISt:WAVeform:IMPort "%s", "%s.txt", ANAlog' % (waveform, waveform))
        self.handles["awg"].write('SEQuence:ELEM1:WAVeform%d "%s"' % (self.port, waveform))
        if end > t_points:
            v_r_max, v_r_min = max(0, v_r_max), min(0, v_r_min)
        self.handles["awg"].write("DISPlay:UNIT:VOLT HIGHlow")
        self.handles["awg"].write("SEQuence:ELEM1:VOLT:LOW%d %f;HIGH%d %f" % (self.port, v_r_min, self.port, v_r_max))
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

    def arm(self):
        TeledyneT3AWGxxxx.arm(self)

    def trigger(self):
        TeledyneT3AWGxxxx.trigger(self)

    def measure(self):
        self.handles["awg"].write("AWGControl:STOP")
