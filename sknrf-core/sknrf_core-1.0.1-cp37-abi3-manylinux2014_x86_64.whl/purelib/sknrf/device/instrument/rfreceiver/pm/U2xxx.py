import logging
import time

import numpy as np
import pyvisa as visa
from pyvisa.errors import VisaIOError

from sknrf.enums.device import Response
from sknrf.settings import Settings
from sknrf.device.base import device_logger
from sknrf.device.signal import tf
from sknrf.device.instrument.rfreceiver import base
from sknrf.utilities.numeric import Info, PkAvg, Format, bounded_property
from sknrf.utilities.rf import dBm2rW, dBU2rU, rW2dBm

logger = device_logger(logging.getLogger(__name__))


class U2xxxCW(base.NoRFReceiver):

    firmware_map = {}
    display_order = ["port", "freq", "b_p", "b_exp", "res"]

    def __new__(cls, error_model, port, config_filename="",
                resource_id='USB0::0x0957::0x2C18::MY56040006::INSTR', b_exp=0.001, res=3):
        self = super().__new__(cls, error_model, port, config_filename)
        self.resource_id = resource_id
        self._b_exp = np.asarray(b_exp, dtype=np.complex).reshape(1, -1) + np.zeros((1, Settings().num_harmonics), dtype=np.complex)
        self._res = res
        self._tracking = False
        return self

    def __getnewargs__(self):
        return tuple(list(super().__getnewargs__()) + [self.resource_id, self._b_exp, self._res])

    def __init__(self, error_model, port, config_filename="",
                 resource_id='USB0::0x0957::0x2C18::MY56040006::INSTR', b_exp=0.001, res=3):
        super().__init__(error_model, port, config_filename)
        self._tracking = False
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self.measure()
        self.initialized = True

    def __getstate__(self, state={}):
        state = super().__getstate__(state=state)
        state['_tracking'] = self._tracking
        return state

    def __setstate__(self, state):
        super().__setstate__(state)
        self._tracking = state['_tracking']
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self.measure()
        self.initialized = True

    def __info__(self):
        """Uncertainty based on "U2000 and U8480 Series USB sensor measurement uncertainty calculator at:
            - 2 GHz
            - 5 dBm
        """

        super().__info__()

        abs_tol = dBm2rW(-60)-dBm2rW(-60.01)
        rel_tol = dBU2rU(0.001) - 1
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["resource_id"] = Info("resource_id", read=True, write=True, check=False)
        self.info["b_exp"] = Info("b_exp", read=True, write=True, check=False,
                                  format_=Format.LOG_DEG, scale=Scale.m, unit="rW", pk_avg=PkAvg.PK,
                                  min_=dBm2rW(-70), max_=dBm2rW(20), abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["_b_exp"] = Info("_b_exp", read=False, write=False, check=False)
        self.info["res"] = Info("res", read=True, write=True, check=False,
                                min_=1, max_=4)
        self.info["_res"] = Info("_res", read=False, write=False, check=False)
        self.info["tracking"] = Info("tracking", read=True, write=True, check=False)
        self.info["_tracking"] = Info("_tracking", read=False, write=False, check=False)

        self.info["a_p"] = Info("a_p", read=False, write=False, check=False)
        self.info["_a_p"] = Info("_a_p", read=False, write=False, check=False)
        self.info["_b_p"] = Info("_b_p", read=False, write=False, check=False,
                                 min_=dBm2rW(-60), max_=dBm2rW(20), abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["v"] = Info("v", read=False, write=False, check=False)
        self.info["_v"] = Info("_v", read=False, write=False, check=False)
        self.info["i"] = Info("_b_p", read=False, write=False, check=False)
        self.info["_i"] = Info("_b_p", read=False, write=False, check=False)
        self.info["b_p"].min, self.info["b_p"].max = dBm2rW(-60), dBm2rW(20)

    def connect_handles(self):
        rm = visa.ResourceManager()
        self.handles["pm"] = rm.open_resource(self.resource_id)
        super().connect_handles()

    def preset(self):
        super().preset()
        if self.unique_handle(self.handles['pm']):
            self.handles["pm"].write("DCL")
            self.handles["pm"].write("*RST")
            self.handles["pm"].write("*CLS")
            self.handles["pm"].write("SYSTEM.PRESET DEF")
            self.handles["pm"].write("FREQ %fMHz" % (Settings().f0 / 1e6,))
            self.handles["pm"].write("CAL:ZERO:TYPE INT")  # Performs internal zeroing
            # self.handles["pm"].timeout = 60*1000
            # self.handles["pm"].query("CAL;*OPC?")  # Initializes calibration.
            # self.handles["pm"].timeout = 2 * 1000
            self._configure(self._b_exp, self._res)

            self.handles["pm"].write("INIT:CONT OFF")
            self.handles["pm"].write("DET:FUNC NORMAL")
            self.handles["pm"].write("TRIG:SOUR EXT")
            self.handles["pm"].write("SWE:TIME %f" % (1/Settings().RBW))  # Pulse Width
            self.handles["pm"].write("SWE:OFFS:TIME 0.0001")  # Offset

            self.handles["pm"].write("INIT:IMM")

    @property
    def freq(self):
        return float(self.handles["pm"].query("FREQ?"))*Settings().harmonics[1:]

    @bounded_property
    def b_exp(self):
        return self._b_exp

    @b_exp.setter
    def b_exp(self, b_exp):
        if not self._tracking:
            self._configure(self._b_exp, self._res)
        self._b_exp = b_exp

    @property
    def tracking(self):
        return self._tracking

    @tracking.setter
    def tracking(self, tracking):
        if not tracking:
            self._configure(self._b_exp, self._res)
        self._tracking = tracking

    @bounded_property
    def res(self):
        return self._res

    @res.setter
    def res(self, res):
        if not self._tracking:
            self._configure(self._b_exp, self._res)
        self._res = int(np.round(res))

    def _configure(self, b_exp, res):
        for harm_idx in range(0, self.num_harmonics):
            self.handles["pm"].write("CONF %d, %d, @1" % (int(np.round(rW2dBm(b_exp[harm_idx, 0]))), res))

    def trigger(self):
        self.handles["pm"].write("INIT:IMM")

    def measure(self):
        if not self.initialized:
            self._b_p_[:, :] = self.info["_a_p"].min
            self._a_p_[:, :] = self.info["_b_p"].min
            self.handles["pm"].write("INIT:IMM")  # Arm Trigger for next measurement
            return
        if not self._on:
            self.handles["pm"].write("INIT:IMM")  # Arm Trigger for next measurement
            return

        for harm_idx in range(0, self.num_harmonics):
            _a_ = np.array([0.0], dtype=np.complex128)
            self._a_p_[harm_idx, :] = _a_
            try:
                _b_ = np.array([dBm2rW(float(self.handles["pm"].query("FETC?")))], dtype=np.complex128)
            except VisaIOError:
                wait_time = 60
                logger.warning("Power Meter Timeout after %ds. Attempting to continue in %ds" % (self.handles["pm"].timeout/1000, wait_time), exc_info=True)
                time.sleep(wait_time)
                self.handles["pm"].write("*ESR")
                self.handles["pm"].write("*CLS")
                self._b_p_[harm_idx, :] = self.info["_b_p"].min
            else:
                self._b_p_[harm_idx, :] = _b_
        if self._tracking:
            self._b_exp = tf.pk(self._b_p_).reshape(1, -1)
            self._configure(self._b_exp, self._res)
        self.handles["pm"].write("INIT:IMM")  # Arm Trigger for next measurement


class U2xxxPulsed(base.NoRFReceiverPulsed):

    firmware_map = {}
    display_order = ["port", "freq", "b_p", "b_exp", "res",
                     "delay", "pulse_width", "period"]

    def __new__(cls, error_model, port, config_filename="",
                resource_id='USB0::0x0957::0x2C18::MY56040006::INSTR', b_exp=0.001, res=3):
        self = super().__new__(cls, error_model, port, config_filename)
        self.resource_id = resource_id
        self._b_exp = np.asarray(b_exp, dtype=np.complex).reshape(1, -1) + np.zeros((1, Settings().num_harmonics), dtype=np.complex)
        self._res = res
        self._tracking = False
        return self

    def __getnewargs__(self):
        return tuple(list(super().__getnewargs__()) + [self.resource_id, self._b_exp, self._res])

    def __init__(self, error_model, port, config_filename="",
                 resource_id='USB0::0x0957::0x2C18::MY56040006::INSTR', b_exp=0.001, res=3):
        super().__init__(error_model, port, config_filename)
        self._tracking = False
        self.connect_handles()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self.measure()
        self.initialized = True

    def __getstate__(self, state={}):
        state = super().__getstate__(state=state)
        state['_tracking'] = self._tracking
        return state

    def __setstate__(self, state):
        super().__setstate__(state)
        self._tracking = state['_tracking']
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self.measure()
        self.initialized = True

    def __info__(self):
        """Uncertainty based on "U2000 and U8480 Series USB sensor measurement uncertainty calculator at:
            - 2 GHz
            - 5 dBm
        """

        super().__info__()

        abs_tol = dBm2rW(-60)-dBm2rW(-60.01)
        rel_tol = dBU2rU(0.001) - 1
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["resource_id"] = Info("resource_id", read=True, write=True, check=False)
        self.info["b_exp"] = Info("b_exp", read=True, write=True, check=False,
                                  format_=Format.LOG_DEG, scale=Scale.m, unit="rW", pk_avg=PkAvg.PK,
                                  min_=dBm2rW(-70), max_=dBm2rW(20), abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["_b_exp"] = Info("_b_exp", read=False, write=False, check=False)
        self.info["res"] = Info("res", read=True, write=True, check=False,
                                min_=1, max_=4)
        self.info["_res"] = Info("_res", read=False, write=False, check=False)
        self.info["tracking"] = Info("tracking", read=True, write=True, check=False)
        self.info["_tracking"] = Info("_tracking", read=False, write=False, check=False)

        self.info["a_p"] = Info("a_p", read=False, write=False, check=False)
        self.info["_a_p"] = Info("_a_p", read=False, write=False, check=False)
        self.info["_b_p"] = Info("_b_p", read=False, write=False, check=False,
                                 min_=dBm2rW(-60), max_=dBm2rW(20), abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["v"] = Info("v", read=False, write=False, check=False)
        self.info["_v"] = Info("_v", read=False, write=False, check=False)
        self.info["i"] = Info("_b_p", read=False, write=False, check=False)
        self.info["_i"] = Info("_b_p", read=False, write=False, check=False)
        self.info["b_p"].min, self.info["b_p"].max = dBm2rW(-60), dBm2rW(20)

    def connect_handles(self):
        rm = visa.ResourceManager()
        self.handles["pm"] = rm.open_resource(self.resource_id)
        super().connect_handles()

    def preset(self):
        super().preset()
        if self.unique_handle(self.handles['pm']):
            self.handles["pm"].write("DCL")
            self.handles["pm"].write("*RST")
            self.handles["pm"].write("*CLS")
            self.handles["pm"].write("SYSTEM.PRESET DEF")
            self.handles["pm"].write("FREQ %fMHz" % (Settings().f0 / 1e6,))
            self.handles["pm"].write("CAL:ZERO:TYPE INT")  # Performs internal zeroing
            # self.handles["pm"].timeout = 60*1000
            # self.handles["pm"].query("CAL;*OPC?")  # Initializes calibration.
            # self.handles["pm"].timeout = 2 * 1000
            self._configure(self._b_exp, self._res)

            self.handles["pm"].write("INIT:CONT OFF")
            self.handles["pm"].write("DET:FUNC NORMAL")
            self.handles["pm"].write("TRIG:SOUR EXT")
            self.handles["pm"].write("TRAC: STAT ON")

            self.handles["pm"].write("TRAC:OFFS:TIME %f" % (0.0,))  # Delay
            self.handles["pm"].write("TRAC:TIME %f" % (Settings().t_stop, ))  # Pulse Width
            self.handles["pm"].write("TRAC:DATA? MRES")

    @property
    def freq(self):
        return float(self.handles["pm"].query("FREQ?"))*Settings().harmonics[1:]

    @bounded_property
    def b_exp(self):
        return self._b_exp

    @b_exp.setter
    def b_exp(self, b_exp):
        if not self._tracking:
            self._configure(self._b_exp, self._res)
        self._b_exp = b_exp

    @property
    def tracking(self):
        return self._tracking

    @tracking.setter
    def tracking(self, tracking):
        if not tracking:
            self._configure(self._b_exp, self._res)
        self._tracking = tracking

    @bounded_property
    def res(self):
        return self._res

    @res.setter
    def res(self, res):
        if not self._tracking:
            self._configure(self._b_exp, self._res)
        self._res = int(np.round(res))

    def _configure(self, b_exp, res):
        for harm_idx in range(0, self.num_harmonics):
            self.handles["pm"].write("CONF %d, %d, @1" % (int(np.round(rW2dBm(b_exp[harm_idx, 0]))), res))

    @property
    def _delay(self):
        return float(self.handles["pm"].query("TRAC:OFFS:TIME?"))

    @_delay.setter
    def _delay(self, _delay):
        self.handles["pm"].write("TRAC:OFFS:TIME %f" % (_delay, ))

    @property
    def _pulse_width(self):
        return float(self.handles["pm"].query("TRAC:TIME?"))

    @_pulse_width.setter
    def _pulse_width(self, _pulse_width):
        self.handles["pm"].write("TRAC:TIME %f" % (_pulse_width, ))

    def trigger(self):
        self.handles["pm"].write("INIT:IMM")

    def measure(self):
        if not self.initialized:
            self._b_p_[:, :] = self.info["_a_p"].min
            self._a_p_[:, :] = self.info["_b_p"].min
            self.handles["pm"].write("INIT:IMM")  # Arm Trigger for next measurement
            return
        if not self._on:
            self.handles["pm"].write("INIT:IMM")  # Arm Trigger for next measurement
            return

        for harm_idx in range(0, self.num_harmonics):
            _a_ = np.array([0.0], dtype=np.complex128)
            self._a_p_[harm_idx, :] = _a_
            try:
                # _b_ = np.array([dBm2rW(float(self.handles["pm"].query("FETC?")))], dtype=np.complex128)
                _b_str = self.handles["pm"].write("TRAC:DATA? MRES")
                offset = 1
                header_size = float(_b_str[offset])
                offset += 1
                num_bytes = float(_b_str[offset:header_size+offset])
                offset += header_size
                _b_ = np.array([dBm2rW(float(_b_str[offset:]))], dtype=np.complex128)
            except VisaIOError:
                wait_time = 60
                logger.warning("Power Meter Timeout after %ds. Attempting to continue in %ds" % (self.handles["pm"].timeout/1000, wait_time), exc_info=True)
                time.sleep(wait_time)
                self.handles["pm"].write("*ESR")
                self.handles["pm"].write("*CLS")
                self._b_p_[harm_idx, :] = self.info["_b_p"].min
            else:
                self._b_p_[harm_idx, :] = _b_
        if self._tracking:
            self._b_exp = tf.pk(self._b_p_).reshape(1, -1)
            self._configure(self._b_exp, self._res)
        self.handles["pm"].write("INIT:IMM")  # Arm Trigger for next measurement

