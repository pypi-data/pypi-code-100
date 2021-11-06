import os
import logging

import torch as th

from sknrf.enums.runtime import SI, si_eps_map
from sknrf.enums.sequencer import Sweep, sid2p
from sknrf.device.base import AbstractDevice, device_logger
from sknrf.settings import Settings, DeviceFlag
from sknrf.device.signal import tf
from sknrf.app.dataviewer.model.dataset import IQFile
from sknrf.utilities.numeric import Info, Scale, PkAvg, Format, Domain, bounded_property
from sknrf.utilities.rf import a2v, v2a

__author__ = 'dtbespal'
logger = device_logger(logging.getLogger(__name__))


class NoLFSource(AbstractDevice):
    """ LFSource base driver for CW measurements.

        Base class for all LFSource instruments including:

            * NoLFSourcePulsed.
            * NoLFSourceModulated.

    """
    device_id = DeviceFlag.LFSOURCE
    signal_list = ["v"]
    transforms_list = ["Envelope", "Time", "Time Envelope", "Frequency", "Power"]
    display_order = ["on", "initialized", "port",
                     "v",
                     "trigger_delay"]

    def __new__(cls, error_model, port, config_filename="", **kwargs):
        self = super(NoLFSource, cls).__new__(cls, error_model, port, config_filename, **kwargs)
        # Define object ATTRIBUTES
        self._v_ = None
        self._iq_ = None
        self._pulse_width_ = Settings().t_stop
        self._delay_ = 0.0
        return self

    def __getnewargs__(self):
        return tuple(list(super(NoLFSource, self).__getnewargs__()) + [])

    def __init__(self, error_model, port, config_filename="", **kwargs):
        super(NoLFSource, self).__init__(error_model, port, config_filename, **kwargs)
        self._iq_ = th.ones_like(self._v_)
        if self.__class__ == NoLFSource:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._v = th.zeros_like(self._v_)
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoLFSource, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(NoLFSource, self).__setstate__(state)
        if self.__class__ == NoLFSource:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._v = self._v_
            self.initialized = True

    def __info__(self):
        super(NoLFSource, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["port"] = Info("port", read=True, write=False, check=False,
                                 format_=Format.RE, min_=1, max_=Settings().num_ports)
        self.info["v"] = Info("v", read=True, write=True, check=True, domain=Domain.TF,
                              format_=Format.LIN_DEG, scale=Scale._, unit="V", pk_avg=PkAvg.PK,
                              min_=si_eps_map[SI.V], abs_tol=1e-5, rel_tol=1e-5)
        self.info["a_p"] = Info("a_p", read=False, write=True, check=False, domain=Domain.TF,
                                format_=Format.LOG_DEG, scale=Scale.m, unit="rW", pk_avg=PkAvg.PK,
                                min_=si_eps_map[SI.A], abs_tol=1e-5, rel_tol=1e-5)
        self.info["_v"] = Info("_v", read=True, write=True, check=True, domain=Domain.TF,
                               format_=Format.LIN_DEG, scale=Scale._, unit="V", pk_avg=PkAvg.PK,
                            min_=si_eps_map[SI.V], abs_tol=1e-5, rel_tol=1e-5)
        self.info["f0"] = Info("f0", read=False, write=False, check=False, min_=0.0,
                               format_=Format.RE, scale=Scale.G, unit="Hz")
        self.info["period"].read = False
        self.info["num_harmonics"].read = False

    def connect_handles(self):
        super(NoLFSource, self).connect_handles()

    def preset(self):
        super(NoLFSource, self).preset()

    @bounded_property
    def a_p(self):
        """ ndarray: LF Incident Power [freq, time] in rW.
        """
        return v2a(self.v)[0]

    @a_p.setter
    def a_p(self, a_p):
        self.v = a2v(a_p)[0]

    @bounded_property
    def v(self):
        """ ndarray: Low-Frequency Voltage [freq, time] in V.
        """
        return self._error_model._parameters[sid2p(Sweep.V_SET, self.port)][..., 0:1]

    @v.setter
    def v(self, v):
        self._error_model._parameters[sid2p(Sweep.V_SET, self.port)].data[..., 0:1] = v
        self._devices_model.set_stimulus()

    @bounded_property
    def _v(self):
        return self._v_

    @_v.setter
    def _v(self, _v):
        pass

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

    def set_iq(self, iq=None):
        """ Sets the normalized iq signal of the Low-Frequency Voltage.

        Sets the iq data of the Low-Frequency Voltage if the device is initialized.

        Args:
            iq (None/ndarray): multi-harmonic iq waveform [freq, time], default is None.
        """
        if self.initialized:
            if iq is None:
                iq = th.ones_like(self._iq_)
            tf.set_iq(self.v, iq)
            self._devices_model.set_stimulus()


class NoLFSourcePulsed(NoLFSource):
    """ LFSource base driver for pulse modulated measurements.

        Base class for pulse modulated LFSource instruments including:

            * NoLFSourceModulated.

    """
    display_order = ["on", "initialized", "port",
                     "v",
                     "delay", "pulse_width", "period",
                     "trigger_delay"]

    def __new__(cls, error_model, port, config_filename="", **kwargs):
        return super(NoLFSourcePulsed, cls).__new__(cls, error_model, port, config_filename, **kwargs)
        # Define object ATTRIBUTES

    def __getnewargs__(self):
        return tuple(list(super(NoLFSourcePulsed, self).__getnewargs__()) + [])

    def __init__(self, error_model, port, config_filename="", **kwargs):
        super(NoLFSourcePulsed, self).__init__(error_model, port, config_filename, **kwargs)
        if self.__class__ == NoLFSourcePulsed:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._pulse_width = self.period
            self._delay = 0
            self._v = th.zeros_like(self._v_)
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoLFSourcePulsed, self).__getstate__(state=state)
        state["_pulse_width"] = self._pulse_width
        state["_delay"] = self._delay
        return state

    def __setstate__(self, state):
        super(NoLFSourcePulsed, self).__setstate__(state)
        if self.__class__ == NoLFSourcePulsed:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._pulse_width = state["_pulse_width"]
            self._delay = state["_delay"]
            self._v = self._v_
            self.initialized = True

    def __info__(self):
        super(NoLFSourcePulsed, self).__info__()
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
        super(NoLFSourcePulsed, self).connect_handles()

    def preset(self):
        super(NoLFSourcePulsed, self).preset()

    @bounded_property
    def v(self):
        return NoLFSource.v.fget(self)

    @v.setter
    def v(self, v):
        eps = Settings().t_step/2
        mask = (self.time < self._delay_ - eps) | (self.time > self._delay_ + self._pulse_width_ + eps)
        mask = mask.flatten()
        v[mask, :] = 0
        NoLFSource.v.fset(self, v)

    @property
    def delay(self):
        """ float: Pulse modulation delay time in s.
        """
        return self._delay

    @delay.setter
    def delay(self, delay):
        eps = Settings().t_step/2
        try:
            delay = float(NoLFSourcePulsed.time_interp(delay))
            if delay < -eps or delay > (self.period - self.pulse_width) + eps:
                raise ValueError
        except ValueError:
            logger.error("delay out-of-range: %f - %f", 0, self.period - self.pulse_width, exc_info=True)
        else:
            self._delay = delay
            self.set_iq(self._iq_.clone())

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
            pulse_width = float(NoLFSourcePulsed.time_interp(pulse_width))
            if pulse_width < -eps or pulse_width > (self.period - self.delay) + eps:
                raise ValueError
        except ValueError:
            logger.error("pulse width out-of-range: %f - %f", 0, self.period - self.delay, exc_info=True)
        else:
            self._pulse_width = pulse_width
            self.set_iq(self._iq_.clone())

    @property
    def _pulse_width(self):
        return self._pulse_width_

    @_pulse_width.setter
    def _pulse_width(self, _pulse_width):
        self._pulse_width_ = _pulse_width

    def set_iq(self, iq=None):
        """ Sets the normalized iq signal of the Low-Frequency Voltage.

            Sets the iq data of the Low-Frequency Voltage to zero outside of the modulated pulse.

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
            super(NoLFSourcePulsed, self).set_iq(iq)


class NoLFSourceModulated(NoLFSourcePulsed):
    """ LFSource base driver for arbitrary modulated measurements.

        Base class for arbitrary modulated LFSource instruments.

    """
    display_order = ["on", "initialized", "port",
                     "v",
                     "delay", "pulse_width", "period",
                     "iq_files",
                     "trigger_delay"]

    def __new__(cls, error_model, port, config_filename="", **kwargs):
        self = super(NoLFSourceModulated, cls).__new__(cls, error_model, port, config_filename, **kwargs)
        # Define object ATTRIBUTES
        self._iq_files_ = [IQFile(os.sep.join([Settings().data_root, 'signals', 'CW.h5']), mode='r')] * self.num_harmonics
        return self

    def __getnewargs__(self):
        return tuple(list(super(NoLFSourceModulated, self).__getnewargs__()) + [])

    def __init__(self, error_model, port, config_filename="", **kwargs):
        super(NoLFSourceModulated, self).__init__(error_model, port, config_filename, **kwargs)
        if self.__class__ == NoLFSourceModulated:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._pulse_width = self.period
            self._delay = 0
            self.iq_files = self._iq_files_
            self._v = th.zeros_like(self._v_)
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoLFSourceModulated, self).__getstate__(state=state)
        state["iq_files"] = self.iq_files
        return state

    def __setstate__(self, state):
        super(NoLFSourceModulated, self).__setstate__(state)
        if self.__class__ == NoLFSourceModulated:  # Each Instrument defines its own initialization
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
        super(NoLFSourceModulated, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["iq_files"] = Info("iq_files", read=True, write=True, check=False)

    def connect_handles(self):
        super(NoLFSourceModulated, self).connect_handles()

    def preset(self):
        super(NoLFSourceModulated, self).preset()

    @property
    def iq_files(self):
        """ list[tb.file]: Multi-harmonic modulation IQ file.
        """
        return self._iq_files_

    @iq_files.setter
    def iq_files(self, iq_files):
        iq = th.ones_like(self._v_)
        for harm_idx, iq_file in enumerate(iq_files):
            try:
                iq_file = IQFile(iq_file.filename, "r")
            except ValueError:
                logger.warning("iq file is already open")
            finally:
                iq[:, harm_idx] = iq_file.iq
                iq_file.close()
                iq_files[harm_idx].close()
        self._iq_files_ = iq_files
        self._iq_ = iq
        self.set_iq(self._iq_.clone())

    def set_iq(self, iq=None):
        """ Sets the normalized iq signal of the Low-Frequency Voltage.

            Sets the iq data of the Low-Frequency Voltage.

            Keyword Args:
                iq (None/ndarray): multi-harmonic iq waveform [freq, time], default is None.
        """
        if self.initialized:
            if iq is None:
                iq = th.ones_like(self._iq_)
            super(NoLFSourceModulated, self).set_iq(iq)

