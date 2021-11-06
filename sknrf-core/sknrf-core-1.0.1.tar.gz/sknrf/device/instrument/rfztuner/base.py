import os
import logging

import torch as th

from sknrf.settings import Settings, DeviceFlag
from sknrf.device.base import device_logger
from sknrf.enums.runtime import SI, si_eps_map
from sknrf.enums.device import Response, rid2p
from sknrf.enums.sequencer import Sweep, sid2p, sweep_fill_map
from sknrf.device import AbstractDevice
from sknrf.device.signal import tf
from sknrf.app.dataviewer.model.dataset import IQFile
from sknrf.utilities.numeric import Scale, Info, PkAvg, Format, Domain, bounded_property
from sknrf.utilities.rf import z2g, g2z

__author__ = 'dtbespal'
logger = device_logger(logging.getLogger(__name__))


class NoRFZTuner(AbstractDevice):

    device_id = DeviceFlag.RFZTUNER
    signal_list = ["z_set", "z", "gamma_set", "gamma"]
    transforms_list = ["Envelope", "Time", "Time Envelope", "Frequency", "Spectrum"]
    display_order = ["on", "initialized", "port",
                     "gamma_set", "gamma", "z_set", "z",
                     "num_harmonics", "trigger_delay"]

    def __new__(cls, error_model, port, config_filename="", **kwargs):
        self = super(NoRFZTuner, cls).__new__(cls, error_model, port, config_filename, **kwargs)
        # Define object ATTRIBUTES
        self._gamma_set_ = None
        self._gamma_ = None
        self._iq_ = None
        self._pulse_width_ = Settings().t_stop
        self._delay_ = 0.0
        return self

    def __getnewargs__(self):
        return tuple(list(super(NoRFZTuner, self).__getnewargs__()) + [])

    def __init__(self, error_model, port, config_filename="", **kwargs):
        super(NoRFZTuner, self).__init__(error_model, port, config_filename, **kwargs)
        if self.__class__ == NoRFZTuner:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._gamma_set = tf.delta_like(self._gamma_set, sweep_fill_map[Sweep.G_SET])
            self.measure()
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoRFZTuner, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(NoRFZTuner, self).__setstate__(state)
        if self.__class__ == NoRFZTuner:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._gamma_set = self._gamma_set_
            self.measure()
            self.initialized = True

    def __info__(self):
        super(NoRFZTuner, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["port"] = Info("port", read=True, write=False, check=False,
                                 format_=Format.RE)
        self.info["z_set"] = Info("z_set", read=True, write=True, check=True, domain=Domain.TF,
                                  format_=Format.RE_IM, scale=Scale._, unit="Ohm", pk_avg=PkAvg.AVG,
                                  abs_tol=1e-1, rel_tol=1e-1)
        self.info["z"] = Info("z", read=True, write=False, check=True, domain=Domain.TF,
                              format_=Format.RE_IM, scale=Scale._, unit="Ohm", pk_avg=PkAvg.AVG,
                              abs_tol=1e-1, rel_tol=1e-1)
        self.info["gamma_set"] = Info("gamma_set", read=True, write=True, check=True, domain=Domain.TF,
                                      format_=Format.LIN_DEG, scale=Scale._, unit="", pk_avg=PkAvg.AVG,
                                      min_=si_eps_map[SI.G], abs_tol=1e-3, rel_tol=1e-3)
        self.info["gamma"] = Info("gamma", read=True, write=False, check=True, domain=Domain.TF,
                                  format_=Format.LIN_DEG, scale=Scale._, unit="", pk_avg=PkAvg.AVG,
                                  min_=si_eps_map[SI.G], abs_tol=1e-3, rel_tol=1e-3)
        self.info["_gamma_set"] = Info("_gamma_set", read=False, write=False, check=False, domain=Domain.TF,
                                       min_=si_eps_map[SI.G], max_=0.9999, abs_tol=1e-3, rel_tol=1e-3)
        self.info["_gamma"] = Info("_gamma", read=True, write=False, check=True, domain=Domain.TF,
                                   format_=Format.LIN_DEG, scale=Scale._, unit="", pk_avg=PkAvg.AVG,
                                   min_=si_eps_map[SI.G], abs_tol=1e-3, rel_tol=1e-3)
        self.info["f0"] = Info("f0", read=False, write=True, check=False, min_=0.0,
                               format_=Format.RE, scale=Scale.G, unit="Hz")
        self.info["period"].read = False

    def connect_handles(self):
        super(NoRFZTuner, self).connect_handles()

    def preset(self):
        super(NoRFZTuner, self).preset()

    @bounded_property
    def gamma_set(self):
        """ ndarray: Desired RF Reflection Coefficient [freq, time].
        """
        return self._error_model._parameters[sid2p(Sweep.G_SET, self.port)][..., 1:]

    @gamma_set.setter
    def gamma_set(self, gamma_set):
        self._error_model._parameters[sid2p(Sweep.G_SET, self.port)].data[..., 1::] = gamma_set
        self._devices_model.set_stimulus()

    @bounded_property
    def z_set(self):
        """ ndarray: Desired RF Impedance [freq, time] in Ohms.
        """
        return g2z(self.gamma_set)[0]

    @z_set.setter
    def z_set(self, z_set):
        self.gamma_set = z2g(z_set)[0]

    @bounded_property
    def _gamma_set(self):
        return self._gamma_set_

    @_gamma_set.setter
    def _gamma_set(self, _gamma_set):
        pass

    @bounded_property
    def gamma(self):
        """ ndarray: Actual RF Reflection Coefficient [freq, time].
        """
        return self._error_model._parameters[rid2p(Response.G_GET, self.port)][..., 1:]

    @bounded_property
    def z(self):
        """ ndarray: Actual RF Impedance [freq, time] in Ohms.
        """
        return g2z(self.gamma)[0]

    @bounded_property
    def _gamma(self):
        return self._gamma_

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
        """ Sets the normalized iq signal of the Desired RF Impedance.

        Sets the iq data of the Desired RF Impedance if the device is initialized.

        Args:
            iq (None/ndarray): multi-harmonic iq waveform [freq, time], default is None.
        """
        if self.initialized:
            if iq is None:
                iq = tf.delta_like(self._gamma_set, 1.0)
            tf.set_iq(self.gamma_set, iq)
            self._devices_model.set_stimulus()


class NoRFZTunerPulsed(NoRFZTuner):
    display_order = ["on", "initialized", "port",
                     "gamma_set", "gamma", "z_set", "z",
                     "delay", "pulse_width", "period",
                     "num_harmonics", "trigger_delay"]

    def __new__(cls, error_model, port, config_filename="", **kwargs):
        return super(NoRFZTunerPulsed, cls).__new__(cls, error_model, port, config_filename, **kwargs)
        # Define object ATTRIBUTES

    def __getnewargs__(self):
        return tuple(list(super(NoRFZTunerPulsed, self).__getnewargs__()) + [])

    def __init__(self, error_model, port, config_filename="", **kwargs):
        super(NoRFZTunerPulsed, self).__init__(error_model, port, config_filename, **kwargs)
        if self.__class__ == NoRFZTunerPulsed:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._pulse_width = self.period
            self._delay = 0
            self._gamma_set = tf.delta_like(self._gamma_set, sweep_fill_map[Sweep.G_SET])
            self.measure()
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoRFZTunerPulsed, self).__getstate__(state=state)
        state["_pulse_width"] = self.pulse_width
        state["_delay"] = self.delay
        return state

    def __setstate__(self, state):
        super(NoRFZTunerPulsed, self).__setstate__(state)
        if self.__class__ == NoRFZTunerPulsed:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._pulse_width = state["_pulse_width"]
            self._delay = state["_delay"]
            self._gamma_set = self._gamma_set_
            self.measure()
            self.initialized = True

    def __info__(self):
        super(NoRFZTunerPulsed, self).__info__()
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
        super(NoRFZTunerPulsed, self).connect_handles()

    def preset(self):
        super(NoRFZTunerPulsed, self).preset()

    @bounded_property
    def gamma_set(self):
        return NoRFZTuner.gamma_set.fget(self)

    @gamma_set.setter
    def gamma_set(self, gamma_set):
        NoRFZTuner.gamma_set.fset(self, gamma_set)

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
        pass

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
        pass

    @property
    def _pulse_width(self):
        return self._pulse_width_

    @_pulse_width.setter
    def _pulse_width(self, _pulse_width):
        self._pulse_width_ = _pulse_width

    def set_iq(self, iq=None):
        """ Sets the normalized iq signal of the Desired RF Impedance.

            Sets the iq data of the Desired RF Impedance to 50 Ohm outside of the modulated pulse.

            Keyword Args:
                iq (None/ndarray): multi-harmonic iq waveform [freq, time], default is None.
        """
        if self.initialized:
            if iq is None:
                iq = tf.delta_like(self._gamma_set, 1.0)
            super(NoRFZTunerPulsed, self).set_iq(iq)


class NoRFZTunerModulated(NoRFZTunerPulsed):
    display_order = ["on", "initialized", "port",
                     "gamma_set", "gamma", "z_set", "z",
                     "delay", "pulse_width", "period",
                     "iq_files",
                     "num_harmonics", "trigger_delay"]

    def __new__(cls, error_model, port, config_filename="", **kwargs):
        self = super(NoRFZTunerModulated, cls).__new__(cls, error_model, port, config_filename, **kwargs)
        # Define object ATTRIBUTES
        self._iq_files_ = [IQFile(os.sep.join([Settings().data_root, 'signals', 'CW.h5']), mode='r')] * self.num_harmonics
        return self

    def __getnewargs__(self):
        return tuple(list(super(NoRFZTunerModulated, self).__getnewargs__()) + [])

    def __init__(self, error_model, port, config_filename="", **kwargs):
        super(NoRFZTunerModulated, self).__init__(error_model, port, config_filename, **kwargs)
        if self.__class__ == NoRFZTunerModulated:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._pulse_width = self.period
            self._delay = 0
            self.iq_files = self._iq_files_
            self._gamma_set = tf.delta_like(self._gamma_set, sweep_fill_map[Sweep.G_SET])
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoRFZTunerModulated, self).__getstate__(state=state)
        state["iq_files"] = self.iq_files
        return state

    def __setstate__(self, state):
        super(NoRFZTunerModulated, self).__setstate__(state)
        if self.__class__ == NoRFZTunerModulated:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._pulse_width = state["_pulse_width"]
            self._delay = state["_delay"]
            self.iq_files = state["iq_files"]
            self._gamma_set = self._gamma_set_
            self.initialized = True

    def __info__(self):
        super(NoRFZTunerModulated, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["iq_files"] = Info("iq_files", read=True, write=True, check=False)

    def connect_handles(self):
        super(NoRFZTunerModulated, self).connect_handles()

    def preset(self):
        super(NoRFZTunerModulated, self).preset()

    @property
    def iq_files(self):
        """ list[tb.file]: Multi-harmonic modulation IQ file.
        """
        return self._iq_files_

    @iq_files.setter
    def iq_files(self, iq_files):
        iq = th.ones_like(self._gamma_set_)
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
        """ Sets the normalized iq signal of the Desired RF Impedance.

            Sets the iq data of the Desired RF Impedance.

            Keyword Args:
                iq (None/ndarray): multi-harmonic iq waveform [freq, time], default is None.
        """
        if self.initialized:
            if iq is None:
                iq = tf.delta_like(self._gamma_set, 1.0)
            super(NoRFZTunerModulated, self).set_iq(iq)
