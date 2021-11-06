import logging

from sknrf.enums.runtime import SI, si_eps_map
from sknrf.enums.device import Response, rid2p
from sknrf.device import AbstractDevice
from sknrf.device.base import device_logger
from sknrf.settings import Settings, DeviceFlag
from sknrf.utilities.numeric import Info, Scale, PkAvg, Format, Domain, bounded_property
from sknrf.utilities.rf import viz2baz

__author__ = 'dtbespal'
logger = device_logger(logging.getLogger(__name__))


class NoLFReceiver(AbstractDevice):
    """ LFReceiver base driver for CW measurements.

        Base class for all LFReceiver instruments including:

            * NoLFReceiverPulsed.
            * NoLFReceiverModulated.

    """
    device_id = DeviceFlag.LFRECEIVER
    signal_list = ["v", "i"]
    transforms_list = ["Envelope", "Time", "Time Envelope", "Frequency", "Power"]
    display_order = ["on", "initialized", "port",
                     "v", "i",
                     "trigger_delay"]

    def __new__(cls, error_model, port, config_filename="", **kwargs):
        self = super(NoLFReceiver, cls).__new__(cls, error_model, port, config_filename, **kwargs)
        # Define object ATTRIBUTES
        self._v_ = None
        self._i_ = None
        self._pulse_width_ = Settings().t_stop
        self._delay_ = 0.0
        return self

    def __getnewargs__(self):
        return tuple(list(super(NoLFReceiver, self).__getnewargs__()) + [])

    def __init__(self, error_model, port, config_filename="", **kwargs):
        super(NoLFReceiver, self).__init__(error_model, port, config_filename, **kwargs)
        if self.__class__ == NoLFReceiver:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self.measure()
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoLFReceiver, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(NoLFReceiver, self).__setstate__(state)
        if self.__class__ == NoLFReceiver:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self.measure()
            self.initialized = True

    def __info__(self):
        super(NoLFReceiver, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["port"] = Info("port", read=True, write=False, check=False,
                                 format_=Format.RE, min_=1, max_=Settings().num_ports)
        self.info["v"] = Info("v", read=True, write=False, check=True, domain=Domain.TF,
                              format_=Format.LIN_DEG, scale=Scale._, unit="V", pk_avg=PkAvg.PK,
                              min_=si_eps_map[SI.V], abs_tol=1e-10, rel_tol=1e-10)
        self.info["i"] = Info("i", read=True, write=False, check=True, domain=Domain.TF,
                              format_=Format.LIN_DEG, scale=Scale._, unit="A", pk_avg=PkAvg.PK,
                              min_=si_eps_map[SI.I], abs_tol=1e-10, rel_tol=1e-10)
        self.info["a_p"] = Info("a_p", read=False, write=False, check=False, domain=Domain.TF,
                                format_=Format.LOG_DEG, scale=Scale.m, unit="rW", pk_avg=PkAvg.PK,
                                min_=si_eps_map[SI.A], abs_tol=1e-10, rel_tol=1e-10)
        self.info["b_p"] = Info("b_p", read=False, write=False, check=False, domain=Domain.TF,
                                format_=Format.LIN_DEG, scale=Scale.m, unit="rW", pk_avg=PkAvg.PK,
                                min_=si_eps_map[SI.B], abs_tol=1e-10, rel_tol=1e-10)
        self.info["_v"] = Info("_v", read=True, write=False, check=True, domain=Domain.TF,
                               format_=Format.LIN_DEG, scale=Scale._, unit="V", pk_avg=PkAvg.PK,
                               min_=si_eps_map[SI.V], abs_tol=1e-10, rel_tol=1e-10)
        self.info["_i"] = Info("_i", read=True, write=False, check=True, domain=Domain.TF,
                               format_=Format.LIN_DEG, scale=Scale._, unit="A", pk_avg=PkAvg.PK,
                               min_=si_eps_map[SI.I], abs_tol=1e-10, rel_tol=1e-10)
        self.info["f0"] = Info("f0", read=False, write=False, check=False, min_=0.0,
                               format_=Format.RE, scale=Scale.G, unit="Hz")
        self.info["period"].read = False
        self.info["num_harmonics"].read = False

    def connect_handles(self):
        super(NoLFReceiver, self).connect_handles()

    def preset(self):
        super(NoLFReceiver, self).preset()

    @bounded_property
    def b_p(self):
        """ ndarray: LF Reflected Power [freq, time] in rW.
        """
        return viz2baz(self.v, self.i)[0]

    @bounded_property
    def a_p(self):
        """ ndarray: LF Incident Power [freq, time] in rW.
        """
        return viz2baz(self.v, self.i)[1]

    @bounded_property
    def v(self):
        """ ndarray: LF Voltage [freq, time] in V.
        """
        return self._error_model._parameters[rid2p(Response.V_GET, self.port)][..., 0:1]

    @bounded_property
    def i(self):
        """ ndarray: LF Current [freq, time] in A.
        """
        return self._error_model._parameters[rid2p(Response.I_GET, self.port)][..., 0:1]

    @ bounded_property
    def _v(self):
        return self._v_

    @ bounded_property
    def _i(self):
        return self._i_

    @property
    def f0(self):
        return 0.0

    @property
    def num_harmonics(self):
        return 1

    @property
    def harmonics(self):
        return Settings().harmonics[0:1]

    @property
    def freq(self):
        return self.f0*self.harmonics

    @property
    def time(self):
        return Settings().time

    def measure(self):
        """ Record measurement data (Required).
        """
        pass


class NoLFReceiverPulsed(NoLFReceiver):
    """ LFReceiver base driver for pulse modulated measurements.

        Base class for pulse modulated LFReceiver instruments including:

            * NoLFReceiverModulated.

    """
    firmware_map = {}
    display_order = ["on", "initialized", "port",
                     "v", "i",
                     "delay", "pulse_width", "period",
                     "trigger_delay"]

    def __new__(cls, error_model, port, config_filename="", **kwargs):
        return super(NoLFReceiverPulsed, cls).__new__(cls, error_model, port, config_filename, **kwargs)
        # Define object ATTRIBUTES

    def __getnewargs__(self):
        return tuple(list(super(NoLFReceiverPulsed, self).__getnewargs__()) + [])

    def __init__(self, error_model, port, config_filename="", **kwargs):
        super(NoLFReceiverPulsed, self).__init__(error_model, port, config_filename, **kwargs)
        if self.__class__ == NoLFReceiverPulsed:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._pulse_width = self.period
            self._delay = 0
            self.measure()
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoLFReceiverPulsed, self).__getstate__(state=state)
        state["_pulse_width"] = self.pulse_width
        state["_delay"] = self.delay
        return state

    def __setstate__(self, state):
        super(NoLFReceiverPulsed, self).__setstate__(state)
        if self.__class__ == NoLFReceiverPulsed:  # Each Instrument defines its own initialization
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
        super(NoLFReceiverPulsed, self).__info__()
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
        super(NoLFReceiverPulsed, self).connect_handles()

    def preset(self):
        super(NoLFReceiverPulsed, self).preset()

    @property
    def delay(self):
        """ float: Pulse modulation delay time in s.
        """
        return self._delay

    @delay.setter
    def delay(self, delay):
        eps = Settings().t_step / 2
        try:
            delay = float(NoLFReceiverPulsed.time_interp(delay))
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
        eps = Settings().t_step / 2
        try:
            pulse_width = float(NoLFReceiverPulsed.time_interp(pulse_width))
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


class NoLFReceiverModulated(NoLFReceiverPulsed):
    """ LFReceiver base driver for arbitrary modulated measurements.

        Base class for arbitrary modulated LFReceiver instruments.

    """
    firmware_map = {}
    display_order = ["on", "initialized", "port",
                     "v", "i",
                     "delay", "pulse_width", "period",
                     "trigger_delay"]

    def __new__(cls, error_model, port, config_filename="", **kwargs):
        return super(NoLFReceiverModulated, cls).__new__(cls, error_model, port, config_filename, **kwargs)
        # Define object ATTRIBUTES

    def __init__(self, error_model, port, config_filename="", **kwargs):
        super(NoLFReceiverModulated, self).__init__(error_model, port, config_filename, **kwargs)
        if self.__class__ == NoLFReceiverModulated:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._pulse_width = self.period
            self._delay = 0
            self.measure()
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoLFReceiverModulated, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(NoLFReceiverModulated, self).__setstate__(state)
        if self.__class__ == NoLFReceiverModulated:  # Each Instrument defines its own initialization
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
        super(NoLFReceiverModulated, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###

    def connect_handles(self):
        super(NoLFReceiverModulated, self).connect_handles()

    def preset(self):
        super(NoLFReceiverModulated, self).preset()


class FromLFSource(NoLFReceiverModulated):
    firmware_map = {}
    display_order = ["on", "initialized", "port",
                     "v", "i",
                     "delay", "pulse_width", "period",
                     "trigger_delay"]

    def __new__(cls, error_model, port, config_filename=""):
        self = super(FromLFSource, cls).__new__(cls, error_model, port, config_filename)
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
        state = super(FromLFSource, self).__getstate__(state=state)
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
        super(FromLFSource, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###


