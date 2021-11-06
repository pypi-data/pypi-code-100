import logging

import torch as th

from sknrf.enums.runtime import SI, si_eps_map, si_dtype_map
from sknrf.enums.device import Response, rid2p
from sknrf.device.base import AbstractDevice, device_logger
from sknrf.settings import Settings, DeviceFlag
from sknrf.device.signal import tf
from sknrf.utilities.numeric import Info, Scale, PkAvg, Format, Domain, bounded_property
from sknrf.utilities.rf import baz2viz

__author__ = 'dtbespal'
logger = device_logger(logging.getLogger(__name__))


class NoRFReceiver(AbstractDevice):
    """ RFReceiver base driver for CW measurements.

        Base class for all RFReceiver instruments including:

            * NoRFReceiverPulsed.
            * NoRFReceiverModulated.

    """
    device_id = DeviceFlag.RFRECEIVER
    signal_list = ["a_p", "b_p", "v", "i"]
    transforms_list = ["Envelope", "Time", "Time Envelope", "Frequency", "Spectrum", "Power"]
    display_order = ["on", "initialized", "port",
                     "a_p", "b_p", "v", "i",
                     "num_harmonics", "harmonics",
                     "trigger_delay"]

    def __new__(cls, error_model, port, config_filename="", **kwargs):
        self = super(NoRFReceiver, cls).__new__(cls, error_model, port, config_filename, **kwargs)
        # Define object ATTRIBUTES
        self._b_p_ = None
        self._a_p_ = None
        self._iq_ = th.ones((Settings().t_points, Settings().f_points), dtype=si_dtype_map[SI.B])
        self._pulse_width_ = Settings().t_stop
        self._delay_ = 0.0
        return self

    def __getnewargs__(self):
        return tuple(list(super(NoRFReceiver, self).__getnewargs__()) + [])

    def __init__(self, error_model, port, config_filename="", **kwargs):
        super(NoRFReceiver, self).__init__(error_model, port, config_filename, **kwargs)
        if self.__class__ == NoRFReceiver:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self.measure()
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoRFReceiver, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(NoRFReceiver, self).__setstate__(state)
        if self.__class__ == NoRFReceiver:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self.measure()
            self.initialized = True

    def __info__(self):
        super(NoRFReceiver, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["port"] = Info("port", read=True, write=False, check=False,
                                 format_=Format.RE, min_=1, max_=Settings().num_ports)
        self.info["a_p"] = Info("a_p", read=True, write=False, check=True, domain=Domain.TF,
                                format_=Format.LOG_DEG, scale=Scale.m, unit="rW", pk_avg=PkAvg.PK,
                                min_=si_eps_map[SI.A], abs_tol=1e-10, rel_tol=1e-10)
        self.info["b_p"] = Info("b_p", read=True, write=False, check=True, domain=Domain.TF,
                                format_=Format.LOG_DEG, scale=Scale.m, unit="rW", pk_avg=PkAvg.PK,
                                min_=si_eps_map[SI.B], abs_tol=1e-10, rel_tol=1e-10)
        self.info["v"] = Info("v", read=True, write=False, check=True, domain=Domain.TF,
                              format_=Format.LIN_DEG, scale=Scale._, unit="V", pk_avg=PkAvg.PK,
                              min_=si_eps_map[SI.V], abs_tol=1e-10, rel_tol=1e-10)
        self.info["i"] = Info("i", read=True, write=False, check=True, domain=Domain.TF,
                              format_=Format.LIN_DEG, scale=Scale._, unit="A", pk_avg=PkAvg.PK,
                              min_=si_eps_map[SI.I], abs_tol=1e-10, rel_tol=1e-10)
        self.info["_a_p"] = Info("_a_p", read=True, write=False, check=True, domain=Domain.TF,
                                format_=Format.LOG_DEG, scale=Scale.m, unit="rW", pk_avg=PkAvg.PK,
                                min_=si_eps_map[SI.A], abs_tol=1e-10, rel_tol=1e-10)
        self.info["_b_p"] = Info("_b_p", read=True, write=False, check=True, domain=Domain.TF,
                                format_=Format.LOG_DEG, scale=Scale.m, unit="rW", pk_avg=PkAvg.PK,
                                min_=si_eps_map[SI.B], abs_tol=1e-10, rel_tol=1e-10)
        self.info["f0"].read = False
        self.info["period"].read = False
        self.info["iq"] = Info("iq", read=False, write=False, check=False)

    def connect_handles(self):
        super(NoRFReceiver, self).connect_handles()

    def preset(self):
        super(NoRFReceiver, self).preset()

    @bounded_property
    def b_p(self):
        """ ndarray: RF Reflected Power [freq, time] in rW.
        """
        return self._error_model._parameters[rid2p(Response.B_GET, self.port)][..., 1:]

    @bounded_property
    def a_p(self):
        """ ndarray: RF Incident Power [freq, time] in rW.
        """
        return self._error_model._parameters[rid2p(Response.A_GET, self.port)][..., 1:]

    @bounded_property
    def v(self):
        """ ndarray: RF Voltage [freq, time] in V.
        """
        return baz2viz(self.b_p, self.a_p)[0]

    @bounded_property
    def i(self):
        """ ndarray: RF Current [freq, time] in A.
        """
        return baz2viz(self.b_p, self.a_p)[1]

    @bounded_property
    def iq(self):
        return self._iq_

    @iq.setter
    def iq(self, iq):
        self._iq_[...] = iq

    @bounded_property
    def _b_p(self):
        return self._b_p_

    @bounded_property
    def _a_p(self):
        return self._a_p_

    @bounded_property
    def f0(self):
        return self._f0

    @f0.setter
    def f0(self, f0):
        self._f0 = f0

    @bounded_property
    def _f0(self):
        return Settings().f0

    @_f0.setter
    def _f0(self, f0):
        pass

    @property
    def num_harmonics(self):
        return Settings().num_harmonics

    @property
    def harmonics(self):
        return Settings().harmonics[1:]

    @property
    def freq(self):
        return self.f0*self.harmonics

    @property
    def time(self):
        return Settings().time

    def measure(self):
        pass

    def set_iq(self, iq=None):
        """ Sets the normalized iq signal of the RF Incident Power.

        Sets the iq data of the Available Source Power if the device is initialized.

        Args:
            iq (None/ndarray): multi-harmonic iq waveform [freq, time], default is None.
        """
        if self.initialized:
            if iq is None:
                iq = th.ones_like(self._iq_)
            tf.set_iq(self.iq, iq)
    
    
class NoRFReceiverPulsed(NoRFReceiver):
    display_order = ["on", "initialized", "port",
                     "a_p", "b_p", "v", "i",
                     "delay", "pulse_width", "period",
                     "num_harmonics", "harmonics",
                     "trigger_delay"]

    def __new__(cls, error_model, port, config_filename="", **kwargs):
        return super(NoRFReceiverPulsed, cls).__new__(cls, error_model, port, config_filename, **kwargs)
        # Define object ATTRIBUTES

    def __getnewargs__(self):
        return tuple(list(super(NoRFReceiverPulsed, self).__getnewargs__()) + [])

    def __init__(self, error_model, port, config_filename="", **kwargs):
        super(NoRFReceiverPulsed, self).__init__(error_model, port, config_filename, **kwargs)
        if self.__class__ == NoRFReceiverPulsed:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._pulse_width = self._pulse_width
            self._delay = self._delay
            self.measure()
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoRFReceiverPulsed, self).__getstate__(state=state)
        state["_pulse_width"] = self.pulse_width
        state["_delay"] = self.delay
        return state

    def __setstate__(self, state):
        super(NoRFReceiverPulsed, self).__setstate__(state)
        if self.__class__ == NoRFReceiverPulsed:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._pulse_width = state["_pulse_width"]
            self._delay = state["_delay"]
            self.measure()
            self.initialized = True

    def __info__(self):
        super(NoRFReceiverPulsed, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["delay"] = Info("delay", read=True, write=True, check=True,
                                  format_=Format.RE, scale=Scale.u, unit="s",
                                  min_=0.0, max_=self.period - Settings().t_step)
        self.info["pulse_width"] = Info("pulse_width", read=True, write=True, check=True,
                                        format_=Format.RE, scale=Scale.u, unit="s",
                                        min_=Settings().t_step, max_=self.period)
        self.info["period"] = Info("period", read=True, write=False, check=False,
                                   format_=Format.RE, scale=Scale.u, unit="s",
                                   min_=0, max_=self.period)

    def connect_handles(self):
        super(NoRFReceiverPulsed, self).connect_handles()

    def preset(self):
        super(NoRFReceiverPulsed, self).preset()

    @property
    def delay(self):
        """ float: Pulse modulation delay time in s.
        """
        return self._delay

    @delay.setter
    def delay(self, delay):
        """ Pulse modulation delay time set function
        :param delay: Pulse delay time
        """
        eps = Settings().t_step/2
        try:
            delay = float(NoRFReceiverPulsed.time_interp(delay))
            if delay < -eps or delay > (self.period - self.pulse_width) + eps:
                raise ValueError
        except ValueError:
            logger.error("delay out-of-range: %f - %f", 0, self.period - self.pulse_width, exc_info=True)
        else:
            self._delay = delay

    @property
    def _delay(self):
        return self._delay_

    @_delay.setter
    def _delay(self, _delay):
        self._delay_ = _delay

    @property
    def pulse_width(self):
        """ float: Pulse modulation pulse width time.
        """
        return self._pulse_width

    @pulse_width.setter
    def pulse_width(self, pulse_width):
        eps = Settings().t_step/2
        try:
            pulse_width = float(NoRFReceiverPulsed.time_interp(pulse_width))
            if pulse_width < -eps or pulse_width > (self.period - self.delay) + eps:
                raise ValueError
        except ValueError:
            logger.error("pulse width out-of-range: %f - %f", 0, self.period - self.delay, exc_info=True)
        else:
            self._pulse_width = pulse_width

    @property
    def _pulse_width(self):
        return self._pulse_width_

    @_pulse_width.setter
    def _pulse_width(self, _pulse_width):
        self._pulse_width_ = _pulse_width

    def set_iq(self, iq=None):
        """ Sets the normalized iq signal of the RF Incident Power.

            Sets the iq data of the Available Source Power to zero outside of the modulated pulse.

            Keyword Args:
                iq (None/ndarray): multi-harmonic iq waveform [freq, time], default is None.
        """
        if self.initialized:
            if iq is None:
                iq = th.ones_like(self._iq_)
            eps = Settings().t_step/2
            mask = (self.time < self._delay_ - eps) | (self.time > self._delay_ + self._pulse_width_ + eps)
            mask = mask.flatten()
            iq[mask, :] = 0.0
            super(NoRFReceiverPulsed, self).set_iq(iq)


class NoRFReceiverModulated(NoRFReceiverPulsed):
    firmware_map = {}
    display_order = ["on", "initialized", "port",
                     "a_p", "b_p", "v", "i",
                     "delay", "pulse_width", "period",
                     "num_harmonics", "harmonics",
                     "trigger_delay"]

    def __new__(cls, error_model, port, config_filename="", **kwargs):
        self = super(NoRFReceiverModulated, cls).__new__(cls, error_model, port, config_filename, **kwargs)
        # Define object ATTRIBUTES
        return self

    def __getnewargs__(self):
        return tuple(list(super(NoRFReceiverPulsed, self).__getnewargs__()))

    def __init__(self, error_model, port, config_filename="", **kwargs):
        super(NoRFReceiverModulated, self).__init__(error_model, port, config_filename, **kwargs)
        if self.__class__ == NoRFReceiverModulated:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._pulse_width = self._pulse_width
            self._delay = self._delay
            self.measure()
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoRFReceiverModulated, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(NoRFReceiverModulated, self).__setstate__(state)
        if self.__class__ == NoRFReceiverModulated:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._pulse_width = state["_pulse_width"]
            self._delay = state["_delay"]
            self.measure()
            self.initialized = True

    def __info__(self):
        super(NoRFReceiverModulated, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###

    def connect_handles(self):
        super(NoRFReceiverModulated, self).connect_handles()

    def preset(self):
        super(NoRFReceiverModulated, self).preset()


class FromRFSource(NoRFReceiverModulated):
    firmware_map = {}
    display_order = ["on", "initialized", "port",
                     "a_p", "b_p", "v", "i",
                     "delay", "pulse_width", "period",
                     "num_harmonics", "harmonics",
                     "trigger_delay"]

    def __new__(cls, error_model, port, config_filename=""):
        self = super(FromRFSource, cls).__new__(cls, error_model, port, config_filename)
        # Define object ATTRIBUTES
        self._on_ = False
        return self

    def __init__(self, error_model, port, config_filename=""):
        super().__init__(error_model, port, config_filename)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self.measure()
        self.initialized = True

    def __getstate__(self, state={}):
        state = super(FromRFSource, self).__getstate__(state=state)
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
        super(FromRFSource, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###