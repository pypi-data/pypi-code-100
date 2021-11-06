import sys

import numpy as np
if sys.platform == "win32": from win32com.client import DispatchEx

from scipy.interpolate import interp1d

from sknrf.enums.device import Response
from sknrf.settings import Settings
from sknrf.device.instrument.rfreceiver import base
from sknrf.device.instrument.shared.pnax import N52xxA
if sys.platform == "win32": from sknrf.device.instrument.shared.pnax.PNACOM import constants as consts
from sknrf.utilities.numeric import Info
from sknrf.utilities.rf import dBm2rW, dBU2rU


class N52xxACW(base.NoRFReceiver):

    firmware_map = {'Application Code Version': "A.10.47.06",
                    'Hard Drive Disk Version': "S.28.03.07",
                    'System CPU Version': "6.0",
                    'DSP Version': "5.0"}
    display_order = ["port", "freq", "a_p", "b_p", "v", "i",
                     "num_harmonics", "harmonics"]

    def __new__(cls, error_model, port, config_filename="",
                machine_name="10.0.0.12"):
        self = super().__new__(cls, error_model, port, config_filename)
        self.machine_name = machine_name
        return self

    def __getnewargs__(self):
        return tuple(list(super().__getnewargs__()) + [self.machine_name])

    def __init__(self, error_model, port, config_filename="",
                 machine_name="10.0.0.12"):
        super().__init__(error_model, port, config_filename)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self.measure()
        self.initialized = True

    def __setstate__(self, state):
        super().__setstate__(state)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self.measure()
        self.initialized = True

    def __info__(self):
        super().__info__()
        abs_tol = dBm2rW(-150) - dBm2rW(-151)
        rel_tol = dBU2rU(0.001) - 1
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["machine_name"] = Info("machine_name", read=False, write=True, check=False)
        self.info["_a_p"] = Info("_a_p", read=False, write=False, check=False,
                                 min_=dBm2rW(-200), max_=dBm2rW(0), abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["_b_p"] = Info("_b_p", read=False, write=False, check=False,
                                 min_=dBm2rW(-200), max_=dBm2rW(0), abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["_v"] = Info("_a_p", read=False, write=False, check=False,
                               min_=dBm2rW(-200), max_=dBm2rW(0), abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["_i"] = Info("_b_p", read=False, write=False, check=False,
                               min_=dBm2rW(-200), max_=dBm2rW(0), abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["a_p"].min, self.info["a_p"].max = dBm2rW(-155), dBm2rW(45)
        self.info["b_p"].min, self.info["b_p"].max = dBm2rW(-155), dBm2rW(45)
        self.info["v"].min, self.info["v"].max = dBm2rW(-155), dBm2rW(45)
        self.info["i"].min, self.info["i"].max = dBm2rW(-155), dBm2rW(45)

    def connect_handles(self):
        self.handles["pnax"] = DispatchEx("AgilentPNA835x.Application", self.machine_name)
        super().connect_handles()

    def preset(self):
        super().preset()
        if self.unique_handle(self.handles['pnax']):
            N52xxA.preset(self)

    @property
    def _pna_port(self):
        if self.port == 1:
            return 1
        elif self.port == 2:
            return 3
        else:
            raise NotImplemented("Driver not valid for this port")

    @property
    def freq(self):
        chan = self.handles["pnax"].Channel(1)
        return chan.centerFrequency * Settings().harmonics[1:]

    def trigger(self):
        N52xxA.trigger(self)

    def measure(self):
        meass = self.handles["pnax"].Measurements
        port_offset = 2*self.port
        p_ref = np.asarray(meass.Item(1).getData(consts.naRawData, consts.naDataFormat_Real)) + \
             1j*np.asarray(meass.Item(1).getData(consts.naRawData, consts.naDataFormat_Imaginary))
        _a_ = np.asarray(meass.Item(port_offset).getData(consts.naRawData, consts.naDataFormat_Real)) + \
         1j * np.asarray(meass.Item(port_offset).getData(consts.naRawData, consts.naDataFormat_Imaginary))
        _b_ = np.asarray(meass.Item(port_offset + 1).getData(consts.naRawData, consts.naDataFormat_Real)) + \
         1j * np.asarray(meass.Item(port_offset + 1).getData(consts.naRawData, consts.naDataFormat_Imaginary))
        self._b_p_[:, :] = (_b_/np.sqrt(1000)*1).reshape(1, -1)
        self._a_p_[:, :] = (_a_/np.sqrt(1000)*1).reshape(1, -1)


class N52xxAPulsed(base.NoRFReceiverPulsed):

    firmware_map = {'Application Code Version': "A.10.47.06",
                    'Hard Drive Disk Version': "S.28.03.07",
                    'System CPU Version': "6.0",
                    'DSP Version': "5.0"}
    display_order = ["port", "freq", "a_p", "b_p", "v", "i",
                     "delay", "pulse_width", "period",
                     "num_harmonics", "harmonics"]

    def __new__(cls, error_model, port, config_filename="",
                machine_name="10.0.0.12"):
        self = super().__new__(cls, error_model, port, config_filename)
        self.machine_name = machine_name
        return self

    def __getnewargs__(self):
        return tuple(list(super().__getnewargs__()) + [self.machine_name])

    def __init__(self, error_model, port, config_filename="",
                 machine_name="10.0.0.12"):
        super().__init__(error_model, port, config_filename)
        self.connect_handles()
        self.preset()
        self.__info__()

        # Initialize object PROPERTIES
        self._on = False
        self.measure()
        self.initialized = True

    def __setstate__(self, state):
        super().__setstate__(state)
        self.connect_handles()
        self.preset()
        self.__info__()

        # Initialize object PROPERTIES
        self._on = False
        self.measure()
        self.initialized = True

    def __info__(self):
        super().__info__()
        abs_tol = dBm2rW(-150) - dBm2rW(-151)
        rel_tol = dBU2rU(0.001) - 1
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["machine_name"] = Info("machine_name", read=False, write=True, check=False)
        self.info["_a_p"] = Info("_a_p", read=False, write=False, check=False,
                                 min_=dBm2rW(-200), max_=dBm2rW(0), abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["_b_p"] = Info("_b_p", read=False, write=False, check=False,
                                 min_=dBm2rW(-200), max_=dBm2rW(0), abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["_v"] = Info("_a_p", read=False, write=False, check=False,
                               min_=dBm2rW(-200), max_=dBm2rW(0), abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["_i"] = Info("_b_p", read=False, write=False, check=False,
                               min_=dBm2rW(-200), max_=dBm2rW(0), abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["a_p"].min, self.info["a_p"].max = dBm2rW(-155), dBm2rW(45)
        self.info["b_p"].min, self.info["b_p"].max = dBm2rW(-155), dBm2rW(45)
        self.info["v"].min, self.info["v"].max = dBm2rW(-155), dBm2rW(45)
        self.info["i"].min, self.info["i"].max = dBm2rW(-155), dBm2rW(45)
        self.info["delay"].min = 300e-9 + 4e-9
        self.info["pulse_width"].min = 100e-9
        self.info["pulse_width"].read = False
        self.info["pulse_width"].write = False

    def connect_handles(self):
        self.handles["pnax"] = DispatchEx("AgilentPNA835x.Application", self.machine_name)
        super().connect_handles()

    def preset(self):
        super().preset()
        if self.unique_handle(self.handles['pnax']):
            N52xxA.preset(self)
            N52xxA.preset_pulsed(self)

    @property
    def _pna_port(self):
        if self.port == 1:
            return 1
        elif self.port == 2:
            return 3
        else:
            raise NotImplemented("Driver not valid for this port")

    @property
    def freq(self):
        chan = self.handles["pnax"].Channel(1)
        return chan.centerFrequency*Settings().harmonics[1:]

    @property
    def _delay(self):
        chan = self.handles['pnax'].Channel(1)
        pulse = chan.PulseGenerator
        pulse_num = 0
        return pulse.Delay(pulse_num)

    @_delay.setter
    def _delay(self, _delay):
        chan = self.handles['pnax'].Channel(1)
        pulse = chan.PulseGenerator
        pulse_num = 0
        pulse.SetDelay(pulse_num, _delay)

    @property
    def _pulse_width(self):
        chan = self.handles['pnax'].Channel(1)
        pulse = chan.PulseGenerator
        pulse_num = 0
        return pulse.Width(pulse_num)

    def trigger(self):
        N52xxA.trigger(self)

    def measure(self):
        meass = self.handles["pnax"].Measurements
        port_offset = 2*self.port
        p_ref = np.asarray(meass.Item(1).getData(consts.naRawData, consts.naDataFormat_Real)) + \
             1j*np.asarray(meass.Item(1).getData(consts.naRawData, consts.naDataFormat_Imaginary))
        _a_ = np.asarray(meass.Item(port_offset).getData(consts.naRawData, consts.naDataFormat_Real)) + \
         1j * np.asarray(meass.Item(port_offset).getData(consts.naRawData, consts.naDataFormat_Imaginary))
        _b_ = np.asarray(meass.Item(port_offset + 1).getData(consts.naRawData, consts.naDataFormat_Real)) + \
         1j * np.asarray(meass.Item(port_offset + 1).getData(consts.naRawData, consts.naDataFormat_Imaginary))
        self._b_p_[0, :] = _b_/np.sqrt(1000)*1
        self._a_p_[0, :] = _a_/np.sqrt(1000)*1
