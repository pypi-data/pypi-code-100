import sys

import torch as th

from sknrf.device.signal import tf
from sknrf.device.instrument.rfsource import base
from sknrf.device.instrument.shared.pnax import N52xxA
from sknrf.utilities.numeric import Info, bounded_property
from sknrf.utilities.rf import rW2dBm, dBm2rW, dBU2rU

if sys.platform == "win32": from win32com.client import DispatchEx
if sys.platform == "win32": from sknrf.device.instrument.shared.pnax.PNACOM import constants as consts


class N52xxACW(base.NoRFSource):

    firmware_map = {'Application Code Version': "A.10.47.06",
                    'Hard Drive Disk Version': "S.28.03.07",
                    'System CPU Version': "6.0",
                    'DSP Version': "5.0"}
    display_order = ["on", "initialized", "port", "freq", "a_p",
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
        gpl = self.handles["pnax"].GlobalPowerLimit
        gpl.Lock = False
        try:
            gpl.SetLimit(self._pna_port, rW2dBm(self.info["_a_p"].max))
            gpl.SetState(self._pna_port, True)
        finally:
            gpl.Lock = True

        self._on = False
        self._a_p = dBm2rW(-30.00)*th.ones_like(self._a_p_)
        self.initialized = True

    def __setstate__(self, state):
        super().__setstate__(state)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        gpl = self.handles["pnax"].GlobalPowerLimit
        gpl.Lock = False
        try:
            gpl.SetLimit(self._pna_port, self.info["_a_p"].max)
            gpl.SetState(self._pna_port, True)
        finally:
            gpl.Lock = True

        self._on = False
        self._a_p = self._a_p_
        self.initialized = True

    def __info__(self):
        super().__info__()
        abs_tol = dBm2rW(-30.00) - dBm2rW(-30.01)
        rel_tol = dBU2rU(0.01) - 1
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["machine_name"] = Info("machine_name", read=False, write=True, check=False)
        self.info["_a_p"] = Info("_a_p", read=False, write=False, check=False,
                                 min_=dBm2rW(-30), max_=dBm2rW(-10), abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["a_p"].min, self.info["a_p"].max = dBm2rW(-30), dBm2rW(45)
        self.info["v_s"].min, self.info["v_s"].max = dBm2rW(-30), dBm2rW(45)

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
    def _on(self):
        chan = self.handles["pnax"].Channel(1)
        _on = False if chan.SourcePortMode(self._pna_port) == 2 else True
        return _on

    @_on.setter
    def _on(self, _on):
        chan = self.handles["pnax"].Channel(1)
        chan.SetSourcePortMode(self._pna_port, consts.naSourcePortOn) if _on else chan.SetSourcePortMode(self._pna_port, consts.naSourcePortOff)

    @bounded_property
    def _a_p(self):
        chan = self.handles["pnax"].Channel(1)
        pk = dBm2rW(chan.TestPortPower(self._pna_port))
        self._a_p_[:, :] = self._a_p_.pk(pk)
        return self._a_p_

    @_a_p.setter
    def _a_p(self, _a_p):
        _a_p._rms = True
        pk = tf.pk(_a_p)
        chan = self.handles["pnax"].Channel(1)
        chan.SetTestPortPower(self._pna_port, rW2dBm(pk[0, 0]))

    def trigger(self):
        N52xxA.trigger(self)


class N52xxAPulsed(base.NoRFSourcePulsed):

    firmware_map = {'Application Code Version': "A.10.47.06",
                    'Hard Drive Disk Version': "S.28.03.07",
                    'System CPU Version': "6.0",
                    'DSP Version': "5.0"}
    display_order = ["on", "initialized", "port", "freq", "a_p",
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
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        gpl = self.handles["pnax"].GlobalPowerLimit
        gpl.Lock = False
        try:
            gpl.SetLimit(self._pna_port, rW2dBm(self.info["_a_p"].max))
            gpl.SetState(self._pna_port, True)
        finally:
            gpl.Lock = True

        self._on = False
        self._a_p = dBm2rW(-30.00)*th.ones_like(self._a_p_)
        self.initialized = True

    def __setstate__(self, state):
        super().__setstate__(state)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        gpl = self.handles["pnax"].GlobalPowerLimit
        gpl.Lock = False
        try:
            gpl.SetLimit(self._pna_port, self.info["_a_p"].max)
            gpl.SetState(self._pna_port, True)
        finally:
            gpl.Lock = True

        self._on = False
        self._a_p = self._a_p_
        self.initialized = True

    def __info__(self):
        super().__info__()
        abs_tol = dBm2rW(-30.00) - dBm2rW(-30.01)
        rel_tol = dBU2rU(0.01) - 1
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["machine_name"] = Info("machine_name", read=False, write=True, check=False)
        self.info["_a_p"] = Info("_a_p", read=False, write=False, check=False,
                                 min_=dBm2rW(-30), max_=dBm2rW(-10), abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["a_p"].min, self.info["a_p"].max = dBm2rW(-30), dBm2rW(45)
        self.info["v_s"].min, self.info["v_s"].max = dBm2rW(-30), dBm2rW(45)
        self.info["delay"].min = 100e-9

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
    def _on(self):
        chan = self.handles["pnax"].Channel(1)
        _on = False if chan.SourcePortMode(self._pna_port) == 2 else True
        return _on

    @_on.setter
    def _on(self, _on):
        chan = self.handles["pnax"].Channel(1)
        chan.SetSourcePortMode(self._pna_port, consts.naSourcePortOn) if _on else chan.SetSourcePortMode(self._pna_port, consts.naSourcePortOff)

    @bounded_property
    def _a_p(self):
        chan = self.handles["pnax"].Channel(1)
        pk = dBm2rW(chan.TestPortPower(self._pna_port))
        self._a_p_[:, :] = self._a_p_.set_pk(pk)
        return self._a_p_

    @_a_p.setter
    def _a_p(self, _a_p):
        _a_p._rms = True
        pk = tf.pk(_a_p)
        chan = self.handles["pnax"].Channel(1)
        chan.SetTestPortPower(self._pna_port, rW2dBm(pk[0, 0]))

    def trigger(self):
        N52xxA.trigger(self)

    @property
    def _delay(self):
        chan = self.handles['pnax'].Channel(1)
        pulse = chan.PulseGenerator
        pulse_num = self.port
        return pulse.Delay(pulse_num)

    @_delay.setter
    def _delay(self, _delay):
        chan = self.handles['pnax'].Channel(1)
        pulse = chan.PulseGenerator
        pulse_num = self.port
        pulse.SetDelay(pulse_num, _delay)

    @property
    def _pulse_width(self):
        chan = self.handles['pnax'].Channel(1)
        pulse = chan.PulseGenerator
        pulse_num = self.port
        return pulse.Width(pulse_num)

    @_pulse_width.setter
    def _pulse_width(self, _pulse_width):
        chan = self.handles['pnax'].Channel(1)
        pulse = chan.PulseGenerator
        pulse_num = self.port
        pulse.SetWidth(pulse_num, _pulse_width)
