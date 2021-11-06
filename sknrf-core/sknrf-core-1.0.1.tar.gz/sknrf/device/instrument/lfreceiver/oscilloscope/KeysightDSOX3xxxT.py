import logging
import time

import numpy as np
from scipy.interpolate import interp1d
import pyvisa as visa
from pyvisa.errors import VisaIOError

from sknrf.device import AbstractDevice
from sknrf.device.base import device_logger
from sknrf.enums.device import Response, ReceiverZ
from sknrf.device.instrument.lfreceiver import base
from sknrf.settings import Settings
from sknrf.device.instrument.shared.oscilloscope import KeysightDSOX3xxxT
from sknrf.utilities.numeric import AttributeInfo, Info, PkAvg, Format, bounded_property

__author__ = 'dtbespal'
logger = device_logger(logging.getLogger(__name__))


class KeysightDSOX3xxxTModulated(base.NoLFReceiverModulated):
    firmware_map = {}
    display_order = ["on", "initialized", "freq", "v", "i",
                     "v_i_port", "v_q_port", "i_i_port", "i_q_port"]

    def __new__(cls, error_model, port, config_filename="",
                resource_id='USB0::0x2A8D::0x1764::MY57252090::0::INSTR',
                v_i_port=0, v_q_port=0, i_i_port=0, i_q_port=0):
        self = super(KeysightDSOX3xxxTModulated, cls).__new__(cls, error_model, port, config_filename)
        # Define object ATTRIBUTES
        self.resource_id = resource_id
        self.v_i_port = self._config["v_i_port"] if v_i_port < 1 else v_i_port
        self.v_q_port = self._config["v_q_port"] if v_q_port < 1 else v_q_port
        self.i_i_port = self._config["i_i_port"] if i_i_port < 1 else i_i_port
        self.i_q_port = self._config["i_q_port"] if i_q_port < 1 else i_q_port
        self.auto_scale = False
        self.fixed_scale = True
        self._on_ = False
        return self

    def __getnewargs__(self):
        return tuple(list(super(KeysightDSOX3xxxTModulated, self).__getnewargs__())
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
        state = super(KeysightDSOX3xxxTModulated, self).__getstate__(state=state)
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
        super(KeysightDSOX3xxxTModulated, self).__info__()
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
        super(KeysightDSOX3xxxTModulated, self).connect_handles()

    def preset(self):
        super(KeysightDSOX3xxxTModulated, self).preset()
        if self.unique_handle(self.handles["scope"]):
            KeysightDSOX3xxxT.preset(self)

        # Channel
        port = self._config["v_i_port"]
        unit = self._config["unit"][port - 1]
        unit_str = "VOLT" if unit == "V" else "AMPere"
        limit = 2 * self._config["voltage_limit"][port - 1] if unit == "V" else 2 * self._config["current_limit"][port - 1]
        self.handles["scope"].write(":CHANnel%d:COUPling DC" % (port,))  # DC Coupling
        self.handles["scope"].write(":CHANnel%d:PROBe %f" % (port, self._config["attenuation"][port - 1]))
        self.handles["scope"].write(":CHANnel%d:OFFSet %d" % (port, 0.0))
        self.handles["scope"].write(":CHANnel%d:RANGe %d" % (port, limit))
        self.handles["scope"].write(":CHANnel%d:UNITs %s" % (port, unit_str))
        self.handles["scope"].write(":WAVeform:SOURce CHANnel%d" % (port,))
        self.handles["scope"].query("*OPC?")

        port = self._config["v_q_port"]
        unit = self._config["unit"][port - 1]
        unit_str = "VOLT" if unit == "V" else "AMPere"
        limit = 2 * self._config["voltage_limit"][port - 1] if unit == "V" else 2 * self._config["current_limit"][port - 1]
        self.handles["scope"].write(":CHANnel%d:COUPling DC" % (port,))  # DC Coupling
        self.handles["scope"].write(":CHANnel%d:PROBe %f" % (port, self._config["attenuation"][port - 1]))
        self.handles["scope"].write(":CHANnel%d:OFFSet %d" % (port, 0.0))
        self.handles["scope"].write(":CHANnel%d:RANGe %d" % (port, limit))
        self.handles["scope"].write(":CHANnel%d:UNITs %s" % (port, unit_str))
        self.handles["scope"].write(":WAVeform:SOURce CHANnel%d" % (port,))
        self.handles["scope"].query("*OPC?")

        port = self._config["i_i_port"]
        unit = self._config["unit"][port - 1]
        unit_str = "VOLT" if unit == "V" else "AMPere"
        limit = 2 * self._config["voltage_limit"][port - 1] if unit == "V" else 2 * self._config["current_limit"][port - 1]
        self.handles["scope"].write(":CHANnel%d:COUPling DC" % (port,))  # DC Coupling
        self.handles["scope"].write(":CHANnel%d:PROBe %f" % (port, self._config["attenuation"][port - 1]))
        self.handles["scope"].write(":CHANnel%d:OFFSet %d" % (port, 0.0))
        self.handles["scope"].write(":CHANnel%d:RANGe %d" % (port, limit))
        self.handles["scope"].write(":CHANnel%d:UNITs %s" % (port, unit_str))
        self.handles["scope"].write(":WAVeform:SOURce CHANnel%d" % (port,))
        self.handles["scope"].query("*OPC?")

        port = self._config["i_q_port"]
        unit = self._config["unit"][port - 1]
        unit_str = "VOLT" if unit == "V" else "AMPere"
        limit = 2 * self._config["voltage_limit"][port - 1] if unit == "V" else 2 * self._config["current_limit"][port - 1]
        self.handles["scope"].write(":CHANnel%d:COUPling DC" % (port,))  # DC Coupling
        self.handles["scope"].write(":CHANnel%d:PROBe %f" % (port, self._config["attenuation"][port - 1]))
        self.handles["scope"].write(":CHANnel%d:OFFSet %d" % (port, 0.0))
        self.handles["scope"].write(":CHANnel%d:RANGe %d" % (port, limit))
        self.handles["scope"].write(":CHANnel%d:UNITs %s" % (port, unit_str))
        self.handles["scope"].write(":WAVeform:SOURce CHANnel%d" % (port,))
        self.handles["scope"].query("*OPC?")

    @property
    def _on(self):
        return bool(int(self.handles["scope"].query(":CHANnel%d:DISPlay?" % (self._config["v_i_port"])))) \
               and bool(int(self.handles["scope"].query(":CHANnel%d:DISPlay?" % (self._config["v_q_port"])))) \
               and bool(int(self.handles["scope"].query(":CHANnel%d:DISPlay?" % (self._config["i_i_port"])))) \
               and bool(int(self.handles["scope"].query(":CHANnel%d:DISPlay?" % (self._config["i_q_port"]))))

    @_on.setter
    def _on(self, _on):
        self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (self._config["v_i_port"], int(_on)))
        self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (self._config["v_q_port"], int(_on)))
        self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (self._config["i_i_port"], int(_on)))
        self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (self._config["i_q_port"], int(_on)))
        self._on_ = _on

    @bounded_property
    def _v(self):
        return self._v_

    @bounded_property
    def _i(self):
        return self._i_

    @property
    def z(self):
        port = self._config["i_i_port"]
        z_str = str(self.handles["scope"].query(":CHANnel%d:INPut?" % (port)))
        z = ReceiverZ._50Ohm if z_str == 'FIFT\n' else ReceiverZ._1MOhm
        return z

    @z.setter
    def z(self, z):
        z = ReceiverZ(z)
        z_str = "DC50" if z is ReceiverZ._50Ohm else "DC"
        port = self._config["i_i_port"]
        self.handles["scope"].write(":CHANnel%d:INPut %s" % (port, z_str))
        port = self._config["i_q_port"]
        self.handles["scope"].write(":CHANnel%d:INPut %s" % (port, z_str))
        self.handles["scope"].query("*OPC?")

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
        KeysightDSOX3xxxT.arm(self)

    def trigger(self):
        KeysightDSOX3xxxT.trigger(self)

    def _acquisition_done(self):
        return not bool(int(self.handles["scope"].query(":OPERegister:CONDition?")) & 8)

    def measure(self):
        while not self._acquisition_done():
            time.sleep(0.1)

        try:
            self.handles["scope"].write(":WAVeform:SOURce CHANnel%d" % (self._config["v_i_port"],))  # Set the waveform source
            preamble = self.handles["scope"].query(":WAVeform:PREamble?")
            format_, type_, points, avg, x_step, x_origin, x_ref, y_step, y_origin, y_ref = preamble.split(",")
            t = (np.arange(0, float(points), dtype=np.float) - float(x_ref)) * float(x_step) + float(x_origin)
            t = t - self.trigger_delay
            t_old = t[t > 0-float(x_step)]
            t_new = np.linspace(0, min(Settings().t_step*self._v_.shape[-2], t[-1]), self._v_.shape[-2])
            v_i = np.frombuffer(self.handles["scope"].query_binary_values(":WAVeform:DATA?", datatype='s')[0], dtype=">u2").astype(np.float)
            v_i = (v_i - float(y_ref)) * float(y_step) + float(y_origin)
            v_i = v_i[t > 0-float(x_step)]
            v_i = interp1d(t_old, v_i, "nearest")(t_new)

            self.handles["scope"].write(":WAVeform:SOURce CHANnel%d" % (self._config["v_q_port"],))  # Set the waveform source
            preamble = self.handles["scope"].query(":WAVeform:PREamble?")
            format_, type_, points, avg, x_step, x_origin, x_ref, y_step, y_origin, y_ref = preamble.split(",")
            v_q = np.frombuffer(self.handles["scope"].query_binary_values(":WAVeform:DATA?", datatype='s')[0], dtype=">u2").astype(np.float)
            v_q = (v_q - float(y_ref)) * float(y_step) + float(y_origin)
            v_q = v_q[t > 0-float(x_step)]
            v_q = interp1d(t_old, v_q, "nearest")(t_new)

            self.handles["scope"].write(":WAVeform:SOURce CHANnel%d" % (self._config["i_i_port"],))  # Set the waveform source
            preamble = self.handles["scope"].query(":WAVeform:PREamble?")
            format_, type_, points, avg, x_step, x_origin, x_ref, y_step, y_origin, y_ref = preamble.split(",")
            i_i = np.frombuffer(self.handles["scope"].query_binary_values(":WAVeform:DATA?", datatype='s')[0], dtype=">u2").astype(np.float)
            i_i = (i_i - float(y_ref)) * float(y_step) + float(y_origin)
            i_i = i_i[t > 0-float(x_step)]
            i_i = interp1d(t_old, i_i, "nearest")(t_new)

            self.handles["scope"].write(":WAVeform:SOURce CHANnel%d" % (self._config["i_q_port"],))  # Set the waveform source
            preamble = self.handles["scope"].query(":WAVeform:PREamble?")
            format_, type_, points, avg, x_step, x_origin, x_ref, y_step, y_origin, y_ref = preamble.split(",")
            i_q = np.frombuffer(self.handles["scope"].query_binary_values(":WAVeform:DATA?", datatype='s')[0], dtype=">u2").astype(np.float)
            i_q = (i_q - float(y_ref)) * float(y_step) + float(y_origin)
            i_q = i_q[t > 0-float(x_step)]
            i_q = interp1d(t_old, i_q, "nearest")(t_new)
        except VisaIOError:
            self.handles["scope"].clear()
            return

        if not self._on_:
            self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (self._config["v_i_port"], int(self._on_)))
            self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (self._config["v_q_port"], int(self._on_)))
            self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (self._config["i_i_port"], int(self._on_)))
            self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (self._config["i_q_port"], int(self._on_)))
        self._v_[:, 0] = v_i.reshape(-1, 1) + 1j*v_q.reshape(-1, 1)
        self._i_[:, 0] = i_i.reshape(-1, 1) + 1j*i_q.reshape(-1, 1)
