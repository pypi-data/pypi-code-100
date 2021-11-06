import os
import logging

import torch as th

from sknrf.enums.runtime import SI, si_eps_map
from sknrf.enums.device import Response, rid2p
from sknrf.enums.sequencer import Sweep, sid2p
from sknrf.device import AbstractDevice
from sknrf.settings import Settings, DeviceFlag
from sknrf.device.base import device_logger
from sknrf.device.signal import tf
from sknrf.app.dataviewer.model.dataset import IQFile
from sknrf.utilities.numeric import Info, Scale, PkAvg, Format, Domain, bounded_property
from sknrf.utilities.rf import z2g, g2z

__author__ = 'dtbespal'
logger = device_logger(logging.getLogger(__name__))


class NoLFZTuner(AbstractDevice):

    device_id = DeviceFlag.LFZTUNER
    signal_list = ["z"]
    transforms_list = ["Envelope", "Time", "Time Envelope", "Frequency"]
    display_order = ["on", "initialized", "port",
                     "z_set", "z",
                     "trigger_delay"]

    def __new__(cls, error_model, port, config_filename="", **kwargs):
        self = super(NoLFZTuner, cls).__new__(cls, error_model, port, config_filename, **kwargs)
        # Define object ATTRIBUTES
        self._z_set_ = None
        self._z_ = None
        self._iq_ = None
        self._pulse_width_ = Settings().t_stop
        self._delay_ = 0.0
        return self

    def __getnewargs__(self):
        return tuple(list(super(NoLFZTuner, self).__getnewargs__()) + [])

    def __init__(self, error_model, port, config_filename="", **kwargs):
        super(NoLFZTuner, self).__init__(error_model, port, config_filename, **kwargs)
        if self.__class__ == NoLFZTuner:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._z_set = tf.delta_like(self._z_set, si_eps_map[SI.Z])
            self.measure()
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoLFZTuner, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(NoLFZTuner, self).__setstate__(state)
        if self.__class__ == NoLFZTuner:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._z_set = self._z_set_
            self.measure()
            self.initialized = True

    def __info__(self):
        super(NoLFZTuner, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["port"] = Info("port", read=True, write=False, check=False,
                                 format_=Format.RE, min_=1, max_=Settings().num_ports)
        self.info["z_set"] = Info("z_set", read=True, write=True, check=True, domain=Domain.TF,
                                  format_=Format.RE_IM, scale=Scale._, unit="Ohm", pk_avg=PkAvg.AVG,
                                  abs_tol=1e-1, rel_tol=1e-1)
        self.info["gamma_set"] = Info("gamma_set", read=False, write=True, check=True, domain=Domain.TF,
                                      format_=Format.LIN_DEG, scale=Scale._, unit="", pk_avg=PkAvg.AVG,
                                      min_=si_eps_map[SI.G], abs_tol=1e-3, rel_tol=1e-3)
        self.info["z"] = Info("z", read=True, write=False, check=True, domain=Domain.TF,
                              format_=Format.RE_IM, scale=Scale._, unit="Ohm", pk_avg=PkAvg.AVG,
                              abs_tol=1e-1, rel_tol=1e-1)
        self.info["gamma"] = Info("gamma", read=False, write=False, check=True, domain=Domain.TF,
                                  format_=Format.LIN_DEG, scale=Scale._, unit="", pk_avg=PkAvg.AVG,
                                  min_=si_eps_map[SI.G], abs_tol=1e-3, rel_tol=1e-3)
        self.info["_z_set"] = Info("_z_set", read=True, write=True, check=True, domain=Domain.TF,
                                   format_=Format.RE_IM, scale=Scale._, unit="Ohm", pk_avg=PkAvg.AVG,
                                   abs_tol=1e-1, rel_tol=1e-1)
        self.info["z"] = Info("_z", read=True, write=False, check=True, domain=Domain.TF,
                              format_=Format.RE_IM, scale=Scale._, unit="Ohm", pk_avg=PkAvg.AVG,
                              abs_tol=1e-1, rel_tol=1e-1)
        self.info["f0"] = Info("f0", read=False, write=False, check=False, min_=0.0,
                               format_=Format.RE, scale=Scale.G, unit="Hz")
        self.info["period"].read = False
        self.info["num_harmonics"].read = False

    def connect_handles(self):
        super(NoLFZTuner, self).connect_handles()

    def preset(self):
        super(NoLFZTuner, self).preset()

    @bounded_property
    def gamma_set(self):
        """ ndarray: Desired LF Reflection Coefficient [freq, time].
        """
        return z2g(self.z_set)[0]

    @gamma_set.setter
    def gamma_set(self, gamma_set):
        self.z_set = g2z(gamma_set)[0]

    @bounded_property
    def z_set(self):
        """ ndarray: Desired LF Impedance [freq, time] in Ohms.
        """
        return self._error_model._parameters[sid2p(Sweep.Z_SET, self.port)][..., 0:1]

    @z_set.setter
    def z_set(self, z_set):
        self._error_model._parameters[sid2p(Sweep.Z_SET, self.port)].data[..., 0:1] = z_set
        self._devices_model.set_stimulus()

    @bounded_property
    def _z_set(self):
        return self._z_set_

    @_z_set.setter
    def _z_set(self, _z_set):
        pass

    @bounded_property
    def gamma(self):
        """ ndarray: Actual LF Reflection Coefficient [freq, time].
        """
        return z2g(self.z)[0]

    @bounded_property
    def z(self):
        """ ndarray: Actual LF Impedance [freq, time] in Ohms.
        """
        return self._error_model._parameters[rid2p(Response.Z_GET, self.port)][..., 0:1]

    @bounded_property
    def _z(self):
        return self._z_

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
        pass

    def set_iq(self, iq=None):
        """ Sets the normalized iq signal of the Desired Low-Frequency Impedance.

        Sets the iq data of the Desired Low-Frequency Impedance if the device is initialized.

        Args:
            iq (None/ndarray): multi-harmonic iq waveform [freq, time], default is None.
        """
        if self.initialized:
            if iq is None:
                iq = tf.delta_like(self._z_set, 1.0)
            tf.set_iq(self.z_set, iq)
            self._devices_model.set_stimulus()


class NoLFZTunerPulsed(NoLFZTuner):
    display_order = ["on", "initialized", "port",
                     "z_set", "z",
                     "delay", "pulse_width", "period",
                     "trigger_delay"]

    def __new__(cls, error_model, port, config_filename="", **kwargs):
        return super(NoLFZTunerPulsed, cls).__new__(cls, error_model, port, config_filename, **kwargs)
        # Define object ATTRIBUTES

    def __getnewargs__(self):
        return tuple(list(super(NoLFZTunerPulsed, self).__getnewargs__()) + [])

    def __init__(self, error_model, port, config_filename="", **kwargs):
        super(NoLFZTunerPulsed, self).__init__(error_model, port, config_filename, **kwargs)
        if self.__class__ == NoLFZTunerPulsed:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._pulse_width = self.period
            self._delay = 0
            self._z_set = tf.delta_like(self._z_set, si_eps_map[SI.Z])
            self.measure()
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoLFZTunerPulsed, self).__getstate__(state=state)
        state["_pulse_width"] = self.pulse_width
        state["_delay"] = self.delay
        return state

    def __setstate__(self, state):
        super(NoLFZTunerPulsed, self).__setstate__(state)
        if self.__class__ == NoLFZTunerPulsed:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._pulse_width = state["_pulse_width"]
            self._delay = state["_delay"]
            self._z_set = self._z_set_
            self.measure()
            self.initialized = True

    def __info__(self):
        super(NoLFZTunerPulsed, self).__info__()
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
        super(NoLFZTunerPulsed, self).connect_handles()

    def preset(self):
        super(NoLFZTunerPulsed, self).preset()

    @bounded_property
    def z_set(self):
        return NoLFZTuner.z_set.fget(self)

    @z_set.setter
    def z_set(self, z_set):
        NoLFZTuner.z_set.fset(self, z_set)

    @property
    def delay(self):
        """ float: Pulse modulation delay time in s.
        """
        return self._delay

    @delay.setter
    def delay(self, delay):
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
        """ Sets the normalized iq signal of the Desired Low-Frequency Impedance.

            Sets the iq data of the Desired Low-Frequency Impedance to zero outside of the modulated pulse.

            Keyword Args:
                iq (None/ndarray): multi-harmonic iq waveform [freq, time], default is None.
        """
        if self.initialized:
            if iq is None:
                iq = tf.delta_like(self._z_set, 1.0)
            super(NoLFZTunerPulsed, self).set_iq(iq)


class NoLFZTunerModulated(NoLFZTunerPulsed):
    display_order = ["on", "initialized", "port",
                     "z_set", "z",
                     "delay", "pulse_width", "period",
                     "iq_files",
                     "trigger_delay"]

    def __new__(cls, error_model, port, config_filename="", **kwargs):
        self = super(NoLFZTunerModulated, cls).__new__(cls, error_model, port, config_filename, **kwargs)
        # Define object ATTRIBUTES
        self._iq_files_ = [IQFile(os.sep.join([Settings().data_root, 'signals', 'CW.h5']), mode='r')] * self.num_harmonics
        return self

    def __getnewargs__(self):
        return tuple(list(super(NoLFZTunerModulated, self).__getnewargs__()) + [])

    def __init__(self, error_model, port, config_filename="", **kwargs):
        super(NoLFZTunerModulated, self).__init__(error_model, port, config_filename, **kwargs)
        if self.__class__ == NoLFZTunerModulated:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._pulse_width = self.period
            self._delay = 0
            self.iq_files = self._iq_files_
            self._z_set = tf.delta_like(self._z_set, si_eps_map[SI.Z])
            self.measure()
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoLFZTunerModulated, self).__getstate__(state=state)
        state["iq_files"] = self.iq_files
        return state

    def __setstate__(self, state):
        super(NoLFZTunerModulated, self).__setstate__(state)
        if self.__class__ == NoLFZTunerModulated:  # Each Instrument defines its own initialization
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self._on = False
            self._pulse_width = state["_pulse_width"]
            self._delay = state["_delay"]
            self.iq_files = state["iq_files"]
            self._z_set = self._z_set_
            self.measure()
            self.initialized = True

    def __info__(self):
        super(NoLFZTunerModulated, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["iq_files"] = Info("iq_files", read=True, write=True, check=False)

    def connect_handles(self):
        super(NoLFZTunerModulated, self).connect_handles()

    def preset(self):
        super(NoLFZTunerModulated, self).preset()

    @property
    def iq_files(self):
        """ list[tb.file]: Multi-harmonic modulation IQ file.
        """
        return self._iq_files_

    @iq_files.setter
    def iq_files(self, iq_files):
        iq = th.ones_like(self._z_set_)
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
        """ Sets the normalized iq signal of the Desired Low-Frequency Impedance.

            Sets the iq data of the Desired Low-Frequency Impedance.

            Keyword Args:
                iq (None/ndarray): multi-harmonic iq waveform [freq, time], default is None.
        """
        if self.initialized:
            if iq is None:
                iq = tf.delta_like(self._z_set, 1.0)
            super(NoLFZTunerModulated, self).set_iq(iq)
