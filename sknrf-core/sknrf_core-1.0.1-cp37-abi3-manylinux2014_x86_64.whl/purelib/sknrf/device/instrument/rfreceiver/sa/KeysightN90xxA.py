import logging

import numpy as np
import pyvisa as visa
from scipy.interpolate import interp1d

from sknrf.enums.device import Response
from sknrf.settings import Settings
from sknrf.device.base import device_logger
from sknrf.device.instrument.rfreceiver import base
from sknrf.device.instrument.shared.sa import KeysightN90xxA
from sknrf.utilities.numeric import AttributeInfo, Info, Scale, PkAvg, Format, bounded_property
from sknrf.utilities.rf import viz2baz
from sknrf.utilities.rf import dBm2rW, rW2dBm, dBU2rU, rU2dBU

__author__ = 'dtbespal'
logger = device_logger(logging.getLogger(__name__))


class KeysightN90xxAModulated(base.NoRFReceiverModulated):
    firmware_map = {}
    display_order = ["on","initialized", "port", "freq", "a_p", "b_p", "v", "i",
                     "num_harmonics", "harmonics"]

    def __new__(cls, error_model, port, config_filename="",
                resource_id='TCPIP0::10.0.0.13::hislip0::INSTR'):
        self = super(KeysightN90xxAModulated, cls).__new__(cls, error_model, port, config_filename)
        # Define object ATTRIBUTES
        self.resource_id = resource_id
        self._on_ = False
        return self

    def __getnewargs__(self):
        return tuple(list(super(KeysightN90xxAModulated, self).__getnewargs__()) + [self.resource_id])

    def __init__(self, error_model, port, config_filename="",
                 resource_id='TCPIP0::10.0.0.13::hislip0::INSTR'):
        super().__init__(error_model, port, config_filename)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self.measure()
        self.initialized = True

    def __getstate__(self, state={}):
        state = super(KeysightN90xxAModulated, self).__getstate__(state=state)
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
        super(KeysightN90xxAModulated, self).__info__()
        abs_tol = dBm2rW(-154.00) - dBm2rW(-154.01)  # MXA Accuracy
        rel_tol = dBU2rU(0.23) - 1  # MXA Accuracy
        _max_ = dBm2rW(0)  # 1dB Compression
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["resource_id"] = Info("resource_id", read=True, write=True, check=False)
        self.info["_a_p"] = Info("_a_p", read=False, write=False, check=False, pk_avg=PkAvg.AVG,
                                 min_=1e-1000, max_=_max_, abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["_b_p"] = Info("_b_p", read=False, write=False, check=False, pk_avg=PkAvg.AVG,
                                 min_=1e-100, max_=_max_, abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["_v"] = Info("_a_p", read=False, write=False, check=False, pk_avg=PkAvg.AVG,
                               min_=1e-100, max_=_max_, abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["_i"] = Info("_b_p", read=False, write=False, check=False, pk_avg=PkAvg.AVG,
                               min_=1e-100, max_=_max_, abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["a_p"].min, self.info["a_p"].max = dBm2rW(-100), dBm2rW(50)
        self.info["b_p"].min, self.info["b_p"].max = dBm2rW(-100), dBm2rW(50)
        self.info["a_p"].pk_avg, self.info["b_p"].pk_avg = PkAvg.AVG, PkAvg.AVG
        self.info["v"].min, self.info["v"].max = dBm2rW(-100), dBm2rW(60)
        self.info["i"].min, self.info["i"].max = dBm2rW(-100), dBm2rW(50)
        self.info["v"].pk_avg, self.info["i"].pk_avg = PkAvg.AVG, PkAvg.AVG
        self.info["_f0"] = Info("_f0", read=False, write=False, check=False, min_=2,
                                format_=Format.RE, scale=Scale.G, unit="Hz")

    def connect_handles(self):
        rm = visa.ResourceManager()
        self.handles["sa"] = rm.open_resource(self.resource_id)
        super(KeysightN90xxAModulated, self).connect_handles()

    def preset(self):
        super(KeysightN90xxAModulated, self).preset()
        if self.unique_handle(self.handles['sa']):
            KeysightN90xxA.preset(self)

    @property
    def _on(self):
        return self._on_

    @_on.setter
    def _on(self, _on):
        self._on_ = _on

    @property
    def freq(self):
        return float(self.handles["sa"].query(":SENSe:FREQuency:RF:CENTer?"))*self.harmonics

    @bounded_property
    def _a_p(self):
        return self._a_p_

    @bounded_property
    def _b_p(self):
        return self._b_p_

    @bounded_property
    def _f0(self):
        return float(self.handles["sa"].query(":SENSe:FREQuency:RF:CENTer?"))

    @_f0.setter
    def _f0(self, f0):
        self.handles["sa"].write(":SENSe:FREQuency:RF:CENTer %d" % (int(f0),))

    def arm(self):
        KeysightN90xxA.arm(self)

    def trigger(self):
        KeysightN90xxA.trigger(self)

    def measure(self):
        t_points = self._v_.shape[-2]
        _b_ = np.array(self.handles["sa"].query(":FETCh:WAVeform0?").split(","), dtype=np.float)/np.sqrt(2) # Interleaved RMS Volts
        _b_.dtype = np.complex
        _b_ /= np.sqrt(50.0)
        _b_ = _b_[0:t_points]
        _b_ = _b_.reshape(-1, 1)

        # _a_ = _b_*self._error_model._rf_response_bag(self.port, 2)
        _a_ = np.zeros(_b_.shape, dtype=np.complex)
        self._b_p_[:, :], self._a_p_[:, :] = _b_, _a_
