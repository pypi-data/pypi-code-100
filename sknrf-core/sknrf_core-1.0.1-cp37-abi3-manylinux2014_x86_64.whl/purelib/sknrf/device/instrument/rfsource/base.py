import os
import logging

import torch as th
import numpy as np

from sknrf.enums.runtime import SI, si_eps_map
from sknrf.enums.sequencer import Sweep, sid2p
from sknrf.settings import Settings, DeviceFlag
from sknrf.device.base import AbstractDevice, device_logger
from sknrf.device.signal import tf
from sknrf.app.dataviewer.model.dataset import IQFile
from sknrf.utilities.numeric import Info, Scale, PkAvg, Format, Domain, bounded_property
from sknrf.utilities.rf import a2v, v2a

__author__ = 'dtbespal'
logger = device_logger(logging.getLogger(__name__))


class NoRFSource(AbstractDevice):
    """ RFSource base driver for CW measurements.

        Base class for all RFSource instruments including:

            * NoRFSourcePulsed.
            * NoRFSourceModulated.

    """
    device_id = DeviceFlag.RFSOURCE
    signal_list = ["a_p"]
    transforms_list = [Domain.TF, Domain.FF, Domain.FT, Domain.TT]
    display_order = ["on", "initialized", "port", "f0",
                     "a_p", "v_s",
                     "num_harmonics", "harmonics",
                     "trigger_delay"]

    def __new__(cls, error_model, port, config_filename="", **kwargs):
        self = super(NoRFSource, cls).__new__(cls, error_model, port, config_filename, **kwargs)
        # Define object ATTRIBUTES
        self._a_p_ = None
        self._iq_ = None
        self._pulse_width_ = Settings().t_stop
        self._delay_ = 0.0
        return self

    def __getnewargs__(self):
        return tuple(list(super(NoRFSource, self).__getnewargs__()) + [])

    def __init__(self, error_model, port, config_filename="", **kwargs):
        super(NoRFSource, self).__init__(error_model, port, config_filename, **kwargs)
        self._iq_ = th.ones_like(self._a_p_)
        if self.__class__ == NoRFSource:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._a_p = th.zeros_like(self._a_p_)
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoRFSource, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(NoRFSource, self).__setstate__(state)
        if self.__class__ == NoRFSource:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._a_p = self._a_p_
            self.initialized = True

    def __info__(self):
        super(NoRFSource, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["port"] = Info("port", read=True, write=False, check=False,
                                 format_=Format.RE, min_=1, max_=Settings().num_ports)
        self.info["a_p"] = Info("a_p", read=True, write=True, check=True, domain=Domain.TF,
                                format_=Format.LOG_DEG, scale=Scale.m, unit="rW", pk_avg=PkAvg.PK,
                                min_=si_eps_map[SI.A], abs_tol=1e-5, rel_tol=1e-5)
        self.info["v_s"] = Info("v_s", read=True, write=True, check=True, domain=Domain.TF,
                                format_=Format.LIN_DEG, scale=Scale._, unit="V", pk_avg=PkAvg.PK,
                                min_=si_eps_map[SI.V], abs_tol=1e-5, rel_tol=1e-5)
        self.info["_a_p"] = Info("_a_p", read=True, write=True, check=True, domain=Domain.TF,
                                 format_=Format.LOG_DEG, scale=Scale.m, unit="rW", pk_avg=PkAvg.PK,
                                 min_=si_eps_map[SI.A], abs_tol=1e-5, rel_tol=1e-5)
        self.info["f0"] = Info("f0", read=True, write=True, check=False, min_=0.0,
                               format_=Format.RE, scale=Scale.G, unit="Hz")
        self.info["period"].read = False

    def connect_handles(self):
        super(NoRFSource, self).connect_handles()

    def preset(self):
        super(NoRFSource, self).preset()

    @bounded_property
    def a_p(self):
        """ ndarray: RF Incident Power [freq, time] in rW.
        """
        return self._error_model._parameters[sid2p(Sweep.A_SET, self.port)][..., 1:]

    @a_p.setter
    def a_p(self, a_p):
        self._error_model._parameters[sid2p(Sweep.A_SET, self.port)].data[..., 1:] = a_p
        self._devices_model.set_stimulus()

    @bounded_property
    def v_s(self):
        """ ndarray: RF Incident Power [freq, time] in rW.
        """
        return a2v(self.a_p)[0]

    @v_s.setter
    def v_s(self, v_s):
        self.a_p = v2a(v_s)[0]

    @bounded_property
    def _a_p(self):
        return self._a_p_

    @_a_p.setter
    def _a_p(self, _a_p):
        pass

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
        return self._f0*self.harmonics

    @property
    def time(self):
        return Settings().time

    def set_iq(self, iq=None):
        """ Sets the normalized iq signal of the RF Incident Power.

        Sets the iq data of the Available Source Power if the device is initialized.

        Args:
            iq (None/ndarray): multi-harmonic iq waveform [freq, time], default is None.
        """
        if self.initialized:
            if iq is None:
                iq = th.ones_like(self._a_p_)
            tf.set_iq(self.a_p, iq)
            self._devices_model.set_stimulus()


class NoRFSourcePulsed(NoRFSource):
    """ RFSource base driver for pulse modulated measurements.

        Base class for pulse modulated RFSource instruments including:

            * NoRFSourceModulated.

    """
    display_order = ["on", "initialized", "port", "f0",
                     "a_p", "v_s",
                     "delay", "pulse_width", "period",
                     "num_harmonics", "harmonics",
                     "trigger_delay"]

    def __new__(cls, error_model, port, config_filename="", **kwargs):
        return super(NoRFSourcePulsed, cls).__new__(cls, error_model, port, config_filename, **kwargs)
        # Define object ATTRIBUTES

    def __getnewargs__(self):
        return tuple(list(super(NoRFSourcePulsed, self).__getnewargs__()) + [])

    def __init__(self, error_model, port, config_filename="", **kwargs):
        super(NoRFSourcePulsed, self).__init__(error_model, port, config_filename, **kwargs)
        if self.__class__ == NoRFSourcePulsed:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._pulse_width = self.period
            self._delay = 0
            self._a_p = th.zeros_like(self._a_p_)
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoRFSourcePulsed, self).__getstate__(state=state)
        state["_pulse_width"] = self.pulse_width
        state["_delay"] = self.delay
        return state

    def __setstate__(self, state):
        super(NoRFSourcePulsed, self).__setstate__(state)
        if self.__class__ == NoRFSourcePulsed:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._pulse_width = state["_pulse_width"]
            self._delay = state["_delay"]
            self._a_p = self._a_p_
            self.initialized = True

    def __info__(self):
        super(NoRFSourcePulsed, self).__info__()
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
        super(NoRFSourcePulsed, self).connect_handles()

    def preset(self):
        super(NoRFSourcePulsed, self).preset()

    @bounded_property
    def a_p(self):
        return NoRFSource.a_p.fget(self)

    @a_p.setter
    def a_p(self, a_p):
        eps = Settings().t_step/2
        mask = (self.time < self._delay_ - eps) | (self.time > self._delay_ + self._pulse_width_ + eps)
        mask = mask.flatten()
        a_p[mask, :] = 0
        NoRFSource.a_p.fset(self, a_p)

    @property
    def delay(self):
        """ float: Pulse modulation delay time in s.
        """
        return self._delay

    @delay.setter
    def delay(self, delay):
        eps = Settings().t_step/2
        try:
            delay = float(NoRFSourcePulsed.time_interp(delay))
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
        eps = Settings().t_step / 2
        try:
            pulse_width = float(NoRFSourcePulsed.time_interp(pulse_width))
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
        """ Sets the normalized iq signal of the RF Incident Power.

            Sets the iq data of the Available Source Power to zero outside of the modulated pulse.

            Keyword Args:
                iq (None/ndarray): multi-harmonic iq waveform [freq, time], default is None.
        """
        if self.initialized:
            if iq is None:
                iq = th.ones_like(self._a_p_)
            eps = Settings().t_step/2
            mask = (self.time < self._delay_ - eps) | (self.time > self._delay_ + self._pulse_width_ + eps)
            mask = mask.flatten()
            iq[mask, :] = 0.0
            super(NoRFSourcePulsed, self).set_iq(iq)


class NoRFSourceModulated(NoRFSourcePulsed):
    """ RFSource base driver for arbitrary modulated measurements.

        Base class for arbitrary modulated RFSource instruments.

    """
    display_order = ["on", "initialized", "port", "f0",
                     "a_p", "v_s",
                     "delay", "pulse_width", "period",
                     "iq_files",
                     "num_harmonics", "harmonics",
                     "trigger_delay"]

    def __new__(cls, error_model, port, config_filename="", **kwargs):
        self = super(NoRFSourceModulated, cls).__new__(cls, error_model, port, config_filename, **kwargs)
        # Define object ATTRIBUTES
        self._iq_files_ = [IQFile(os.sep.join([Settings().data_root, 'signals', 'CW.h5']), mode='r')]*self.num_harmonics
        self._header_maps_ = [self._iq_files_[0].header]*self.num_harmonics
        self._markers_ = np.zeros((Settings().t_points, self.num_harmonics), dtype=">i1")
        return self

    def __getnewargs__(self):
        return tuple(list(super(NoRFSourceModulated, self).__getnewargs__()) + [])

    def __init__(self, error_model, port, config_filename="", **kwargs):
        super(NoRFSourceModulated, self).__init__(error_model, port, config_filename, **kwargs)
        if self.__class__ == NoRFSourceModulated:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._pulse_width = self.period
            self._delay = 0
            self.iq_files = self._iq_files_
            self._a_p = th.zeros_like(self._a_p_)
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoRFSourceModulated, self).__getstate__(state=state)
        state["iq_files"] = self.iq_files
        return state

    def __setstate__(self, state):
        super(NoRFSourceModulated, self).__setstate__(state)
        if self.__class__ == NoRFSourceModulated:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._pulse_width = state["_pulse_width"]
            self._delay = state["_delay"]
            self.iq_files = state["iq_files"]
            self._a_p = self._a_p_
            self.initialized = True

    def __info__(self):
        super(NoRFSourceModulated, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["iq_files"] = Info("iq_files", read=True, write=True, check=False)

    def connect_handles(self):
        super(NoRFSourceModulated, self).connect_handles()

    def preset(self):
        super(NoRFSourceModulated, self).preset()

    @property
    def iq_files(self):
        """ list[tb.file]: Multi-harmonic modulation IQ file.
        """
        return self._iq_files_

    @iq_files.setter
    def iq_files(self, iq_files):
        iq = th.ones_like(self._a_p_)
        header = [None]*self._a_p_.shape[0]
        marker = [None] * self._a_p_.shape[0]
        for harm_idx, iq_file in enumerate(iq_files):
            try:
                iq_file = IQFile(iq_file.filename, "r")
                iq[:, harm_idx] = iq_file.iq
                header[harm_idx] = iq_file.header
                marker[harm_idx] = iq_file.marker
            except ValueError:
                logger.warning("iq file is already open")
            finally:
                iq_file.close()
                iq_files[harm_idx].close()
        self._iq_files_ = iq_files
        self._iq_ = iq
        self._header_maps_ = header
        self._markers_ = marker
        self.set_iq(self._iq_.clone())

    def set_iq(self, iq=None):
        """ Sets the normalized iq signal of the RF Incident Power.

            Sets the iq data of the Available Source Power.

            Keyword Args:
                iq (None/ndarray): multi-harmonic iq waveform [freq, time], default is None.
        """
        if self.initialized:
            if iq is None:
                iq = th.ones_like(self._a_p_)
            super(NoRFSourceModulated, self).set_iq(iq)

