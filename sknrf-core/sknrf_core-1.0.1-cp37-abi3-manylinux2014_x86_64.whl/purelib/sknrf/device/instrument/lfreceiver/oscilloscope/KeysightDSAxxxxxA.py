import logging
import time

import numpy as np
from scipy.interpolate import interp1d
import pyvisa as visa
from pyvisa.errors import VisaIOError

from sknrf.enums.device import Response
from sknrf.device import AbstractDevice
from sknrf.device.base import device_logger
from sknrf.device.instrument.lfreceiver import base
from sknrf.settings import Settings
from sknrf.device.instrument.shared.oscilloscope import KeysightDSAxxxxxA
from sknrf.utilities.numeric import AttributeInfo, Info, PkAvg, Format, bounded_property

__author__ = 'dtbespal'
logger = device_logger(logging.getLogger(__name__))


class KeysightDSAxxxxxAModulated(base.NoLFReceiverModulated):
    firmware_map = {}
    display_order = ["on", "initialized", "freq", "v", "i",
                     "v_i_port", "v_q_port", "i_i_port", "i_q_port"]

    def __new__(cls, error_model, port, config_filename="",
                resource_id='TCPIP0::10.0.0.40::inst0::INSTR',
                v_i_port=0, v_q_port=0, i_i_port=0, i_q_port=0):
        self = super(KeysightDSAxxxxxAModulated, cls).__new__(cls, error_model, port, config_filename)
        # Define object ATTRIBUTES
        self.resource_id = resource_id
        self.v_i_port = self._config["v_i_port"] if v_i_port < 1 else v_i_port
        self.v_q_port = self._config["v_q_port"] if v_q_port < 1 else v_q_port
        self.i_i_port = self._config["i_i_port"] if i_i_port < 1 else i_i_port
        self.i_q_port = self._config["i_q_port"] if i_q_port < 1 else i_q_port
        self._on_ = False
        return self

    def __getnewargs__(self):
        return tuple(list(super(KeysightDSAxxxxxAModulated, self).__getnewargs__())
                     + [self.resource_id, self.v_i_port, self.v_q_port, self.i_i_port, self.i_q_port])

    def __init__(self, error_model, port, config_filename="",
                 resource_id='USB0::0x2A8D::0x1764::MY57252090::0::INSTR',
                 v_i_port=0, v_q_port=0, i_i_port=0, i_q_port=0):
        super().__init__(error_model, port, config_filename)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self.measure()
        self.initialized = True

    def __getstate__(self, state={}):
        state = super(KeysightDSAxxxxxAModulated, self).__getstate__(state=state)
        return state

    def __setstate__(self, state, *args, **kwargs):
        super().__setstate__(state)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self.measure()
        self.initialized = True

    def __info__(self):
        super(KeysightDSAxxxxxAModulated, self).__info__()
        abs_tol = 1e-3
        rel_tol = 1e-3
        v_max = min(self._config["voltage_limit"][self.v_i_port - 1], self._config["voltage_limit"][self.v_q_port - 1])
        i_max = min(self._config["voltage_limit"][self.i_i_port - 1], self._config["voltage_limit"][self.i_q_port - 1])
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["resource_id"] = Info("resource_id", read=True, write=True, check=False)
        self.info["v_i_port"] = Info("v_i_port", read=True, write=False, check=False,
                                     min_=1, max_=self._config["num_outputs"])
        self.info["v_q_port"] = Info("v_q_port", read=True, write=False, check=False,
                                     min_=1, max_=self._config["num_outputs"])
        self.info["i_i_port"] = Info("i_i_port", read=True, write=False, check=False,
                                     min_=1, max_=self._config["num_outputs"])
        self.info["i_q_port"] = Info("i_q_port", read=True, write=False, check=False,
                                     min_=1, max_=self._config["num_outputs"])
        self.info["_v"] = Info("_v", read=False, write=False, check=False,
                               min_=0, max_=v_max,
                               abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["_i"] = Info("_i", read=False, write=False, check=False,
                               min_=0, max_=i_max,
                               abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["v"].min, self.info["v"].max = 0, v_max
        self.info["i"].min, self.info["i"].max = 0, i_max

    def connect_handles(self):
        rm = visa.ResourceManager()
        self.handles["scope"] = rm.open_resource(self.resource_id)
        super(KeysightDSAxxxxxAModulated, self).connect_handles()

    def preset(self):
        super(KeysightDSAxxxxxAModulated, self).preset()
        if self.unique_handle(self.handles["scope"]):
            KeysightDSAxxxxxA.preset(self)

        # Channel
        port = self._config["v_i_port"]
        self.handles["scope"].write(":CHANnel%d:PROBe 1" % (port,))  # Probe Attenuation
        self.handles["scope"].write(":CHANnel%d:OFFSet %f" % (port, self._config["voltage_offset"][port - 1]))
        self.handles["scope"].write(":CHANnel%d:RANGe %f" % (port, 2 * self._config["voltage_limit"][port - 1]))
        self.handles["scope"].write(":WAVeform:SOURce CHANnel%d" % (port,))
        self.handles["scope"].query("*OPC?")

        port = self._config["v_q_port"]
        self.handles["scope"].write(":CHANnel%d:PROBe 1" % (port,))  # Probe Attenuation
        self.handles["scope"].write(":CHANnel%d:OFFSet %f" % (port, self._config["voltage_offset"][port - 1]))
        self.handles["scope"].write(":CHANnel%d:RANGe %f" % (port, 2 * self._config["voltage_limit"][port - 1]))
        self.handles["scope"].write(":WAVeform:SOURce CHANnel%d" % (port,))
        self.handles["scope"].query("*OPC?")

        port = self._config["i_i_port"]
        self.handles["scope"].write(":CHANnel%d:PROBe 1" % (port,))  # Probe Attenuation
        self.handles["scope"].write(":CHANnel%d:OFFSet %f" % (port, self._config["current_offset"][port - 1]))
        self.handles["scope"].write(":CHANnel%d:RANGe %f" % (port, 2 * self._config["current_limit"][port - 1]))
        self.handles["scope"].write(":WAVeform:SOURce CHANnel%d" % (port,))
        self.handles["scope"].query("*OPC?")

        port = self._config["i_q_port"]
        self.handles["scope"].write(":CHANnel%d:PROBe 1" % (port,))  # Probe Attenuation
        self.handles["scope"].write(":CHANnel%d:OFFSet %f" % (port, self._config["current_offset"][port - 1]))
        self.handles["scope"].write(":CHANnel%d:RANGe %f" % (port, 2 * self._config["current_limit"][port - 1]))
        self.handles["scope"].write(":WAVeform:SOURce CHANnel%d" % (port,))
        self.handles["scope"].query("*OPC?")

    @property
    def _on(self):
        return self._on_

    @_on.setter
    def _on(self, _on):
        self._on_ = _on

    @bounded_property
    def _v(self):
        return self._v_

    @bounded_property
    def _i(self):
        return self._i_

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
        KeysightDSAxxxxxA.arm(self)

    def trigger(self):
        KeysightDSAxxxxxA.trigger(self)

    def _acquisition_done(self):
        return bool(int(self.handles["scope"].query(":WAVeform:COMPlete?")) == 100)

    def measure(self):
        while not self._acquisition_done():
            time.sleep(0.1)

        self.handles["scope"].write(":WAVeform:SOURce CHANnel%d" % (self._config["v_i_port"],))  # Set the waveform source
        preamble = self.handles["scope"].query(":WAVeform:PREamble?")
        format_, type_, points, avg, x_step, x_origin, x_ref, y_step, y_origin, y_ref,\
        coupling, x_disp_range, x_disp_origin, y_disp_range, y_disp_origin,\
        date_, time_, frame_model, mode, completion,\
        x_units, y_units, max_bw, min_bw = preamble.split(",")[0:24]
        t = (np.arange(0, float(points), dtype=np.float) - float(x_ref)) * float(x_step) + float(x_origin)
        t -= t[0]  # remove self.trigger_delay
        t_new = np.linspace(0, Settings().t_step*self._v_.shape[-2], self._v_.shape[-2])
        try:
            v_i = np.frombuffer(self.handles["scope"].query_binary_values(":WAVeform:DATA?", datatype='s')[0], dtype=">i2").astype(np.float)
        except VisaIOError:
            logger.warning("IO Read Error on port %d", self._config["v_i_port"], exc_info=True)
            v_i = np.zeros(t.shape, np.float)
        v_i = (v_i - float(y_ref)) * float(y_step) + float(y_origin)
        v_i = interp1d(t, v_i, "nearest")(t_new)

        self.handles["scope"].write(":WAVeform:SOURce CHANnel%d" % (self._config["v_q_port"],))  # Set the waveform source
        try:
            v_q = np.frombuffer(self.handles["scope"].query_binary_values(":WAVeform:DATA?", datatype='s')[0], dtype=">i2").astype(np.float)
        except VisaIOError:
            logger.warning("IO Read Error on port %d", self._config["v_q_port"], exc_info=True)
            v_q = np.zeros(t.shape, np.float)
        v_q = (v_q - float(y_ref)) * float(y_step) + float(y_origin)
        v_q = interp1d(t, v_q, "nearest")(t_new)

        self.handles["scope"].write(":WAVeform:SOURce CHANnel%d" % (self._config["i_i_port"],))  # Set the waveform source
        try:
            i_i = np.frombuffer(self.handles["scope"].query_binary_values(":WAVeform:DATA?", datatype='s')[0], dtype=">i2").astype(np.float)
        except VisaIOError:
            logger.warning("IO Read Error on port %d", self._config["i_i_port"], exc_info=True)
            i_i = np.zeros(t.shape, np.float)
        i_i = (i_i - float(y_ref)) * float(y_step) + float(y_origin)
        i_i = interp1d(t, i_i, "nearest")(t_new)

        self.handles["scope"].write(":WAVeform:SOURce CHANnel%d" % (self._config["i_q_port"],))  # Set the waveform source
        try:
            i_q = np.frombuffer(self.handles["scope"].query_binary_values(":WAVeform:DATA?", datatype='s')[0], dtype=">i2").astype(np.float)
        except VisaIOError:
            logger.warning("IO Read Error on port %d", self._config["i_q_port"], exc_info=True)
            i_q = np.zeros(t.shape, np.float)
        i_q = (i_q - float(y_ref)) * float(y_step) + float(y_origin)
        i_q = interp1d(t, i_q, "nearest")(t_new)

        self._v_[:, 0] = 2*(v_i.reshape(-1, 1) + 1j*v_q.reshape(-1, 1))
        self._i_[:, 0] = 2*(i_i.reshape(-1, 1) + 1j*i_q.reshape(-1, 1))
