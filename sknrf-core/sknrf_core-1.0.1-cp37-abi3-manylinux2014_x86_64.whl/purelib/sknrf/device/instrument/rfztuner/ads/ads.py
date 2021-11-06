import os
import logging

import numpy as np
import torch as th

from sknrf.enums.runtime import SI, si_eps_map
from sknrf.settings import Settings
from sknrf.device.base import device_logger
from sknrf.device.simulator.keysight.ads import ADSSimulator
from sknrf.device.instrument.rfztuner import base
from sknrf.device.signal import tf
from sknrf.utilities.numeric import Info, PkAvg, Format, bounded_property
from sknrf.utilities.dsp import load_iq_txt, save_iq_txt

__author__ = 'dtbespal'
logger = device_logger(logging.getLogger(__name__))


class ADSCW(base.NoRFZTuner):
    firmware_map = {'Keysight ADS': "2012.08"}
    display_order = ["on", "initialized", "freq", "z_set", "z", "gamma_set", "gamma",
                     "num_harmonics", "harmonics"]

    def __new__(cls, error_model, port, config_filename="",
                simulator_type="Envelope.HB", simulator_name="Envelope"):
        self = super(ADSCW, cls).__new__(cls, error_model, port, config_filename)
        # Define object ATTRIBUTES
        self.simulator_type = simulator_type
        self.simulator_name = simulator_name
        return self

    def __getnewargs__(self):
        return tuple(list(super(ADSCW, self).__getnewargs__()) + [self.simulator_type, self.simulator_name])

    def __init__(self, error_model, port, config_filename="",
                 simulator_type="Envelope.HB", simulator_name="Envelope"):
        super().__init__(error_model, port, config_filename)
        self.simulator_type = simulator_type
        self.simulator_name = simulator_name
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        _z_set = th.zeros_like(self._gamma_set_)
        _z_set[:, 0] = 50*len(self.time)
        self._z_set = _z_set
        self.measure()
        self.initialized = True

    def __getstate__(self, state={}):
        state = super(ADSCW, self).__getstate__(state=state)
        state["simulator_type"] = self.simulator_type
        state["simulator_name"] = self.simulator_name
        return state

    def __setstate__(self, state, *args, **kwargs):
        super().__setstate__(state)
        self.simulator_type = state["simulator_type"]
        self.simulator_name = state["simulator_name"]
        self.connect_handles()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self._z_set = self._z_set_
        self.measure()
        self.initialized = True

    def __info__(self):
        super(ADSCW, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["_z_set"] = Info("_z_set", read=False, write=False, check=False,
                                   abs_tol=1e-1, rel_tol=1e-1)
        self.info["z_set"].abs_tol, self.info["z_set"].rel_tol = 1e-1, 1e-1
        self.info["gamma_set"].abs_tol, self.info["gamma_set"].rel_tol = 1e-3, 1e-3

    def connect_handles(self):
        self.handles['ads'] = ADSSimulator(Settings().netlist_filename, Settings().dataset_filename,
                                self.simulator_type, self.simulator_name, config_filename=None,
                                remote_host=Settings().remote_host, remote_user=Settings().remote_user,
                                remote_password=Settings().remote_password, remote_key_filename=Settings().remote_key_filename,
                                remote_port=Settings().remote_port)
        super(ADSCW, self).connect_handles()

    def preset(self):
        super(ADSCW, self).preset()
        if self.unique_handle(self.handles['ads']):
            self.handles['ads'].preset()
            self.handles['ads'].write("_fund_0", Settings().f0)
            self.handles['ads'].write("_t_stop", Settings().t_stop)
            self.handles['ads'].write("_t_step", Settings().t_step)

    @property
    def freq(self):
        return self.handles['ads'].read_netlist("_fund_1")*self.harmonics

    @bounded_property
    def _z_set(self):
        avg = self.handles['ads'].read_netlist("_Z" + str(self.port))[0:self.num_harmonics]
        self._z_set_[:, :] = self._z_set_.set_avg(avg)
        return self._z_set_

    @_z_set.setter
    def _z_set(self, _z_set):
        _z_set._rms = False
        avg = tf.avg(_z_set)
        avg = np.pad(avg, ((0, self.handles['ads'].order - avg.shape[-1]), (0, 0)),
                     mode='constant', constant_values=50)
        self.handles['ads'].write("_Z" + str(self.port), avg)
        iq = tf.iq(_z_set)
        for harm_idx in range(1, self.num_harmonics + 1):
            i_filename = os.sep.join((Settings().data_root, "simulation", "Z%d%d_I.txt" % (self.port, harm_idx)))
            q_filename = os.sep.join((Settings().data_root, "simulation", "Z%d%d_Q.txt" % (self.port, harm_idx)))
            save_iq_txt(iq[harm_idx - 1, :], i_filename, q_filename)

    @bounded_property
    def _z(self):
        return self._z_

    def trigger(self):
        self.handles['ads'].write("_t_stop", Settings().t_step * (self._z_.shape[-2] - 1))
        self.handles['ads'].measure()

    def measure(self):
        self._z_[:, :] = si_eps_map[SI.Z]
        try:
            _z_ = self.handles['ads'].read("RFPwrSource" + str(self.port) + ".Z_", 0, range(1, self.num_harmonics + 1))
            self._z_[:, 0] = _z_[0, :, 0].reshape((-1, 1))*len(self.time)
        except IndexError:
            logging.warning("ADS dataset buffer does not contain enough data, please run a measurement to update buffer")
            self._z_[:, 0] = 50 * len(self.time)


class ADSModulated(base.NoRFZTunerModulated):
    firmware_map = {'Keysight ADS': "2012.08"}
    display_order = ["on", "initialized", "freq", "z_set", "z", "gamma_set", "gamma",
                     "delay", "pulse_width", "period",
                     "iq_files",
                     "num_harmonics", "harmonics"]

    def __new__(cls, error_model, port, config_filename="",
                simulator_type="Envelope.HB", simulator_name="Envelope"):
        self = super(ADSModulated, cls).__new__(cls, error_model, port, config_filename)
        # Define object ATTRIBUTES
        self.simulator_type = simulator_type
        self.simulator_name = simulator_name
        return self

    def __getnewargs__(self):
        return tuple(list(super(ADSModulated, self).__getnewargs__()) + [self.simulator_type, self.simulator_name])

    def __init__(self, error_model, port, config_filename="",
                 simulator_type="Envelope.HB", simulator_name="Envelope"):
        super().__init__(error_model, port, config_filename)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self._pulse_width = self.period
        self._delay = 0
        self.iq_files = self._iq_files_
        _z_set = th.zeros_like(self._gamma_set_)
        _z_set[:, 0] = 50 * len(self.time)
        self._z_set = _z_set
        self.measure()
        self.initialized = True

    def __getstate__(self, state={}):
        state = super(ADSModulated, self).__getstate__(state=state)
        state["simulator_type"] = self.simulator_type
        state["simulator_name"] = self.simulator_name
        return state

    def __setstate__(self, state, *args, **kwargs):
        super().__setstate__(state)
        self.simulator_type = state["simulator_type"]
        self.simulator_name = state["simulator_name"]
        self.connect_handles()
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
        super(ADSModulated, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["_z_set"] = Info("_z_set", read=False, write=False, check=False,
                                   abs_tol=1e-1, rel_tol=1e-1)
        self.info["z_set"].abs_tol, self.info["z_set"].rel_tol = 1e-1, 1e-1
        self.info["gamma_set"].abs_tol, self.info["gamma_set"].rel_tol = 1e-3, 1e-3

    def connect_handles(self):
        self.handles['ads'] = ADSSimulator(Settings().netlist_filename, Settings().dataset_filename,
                                self.simulator_type, self.simulator_name, config_filename=None,
                                remote_host=Settings().remote_host, remote_user=Settings().remote_user,
                                remote_password=Settings().remote_password, remote_key_filename=Settings().remote_key_filename,
                                remote_port=Settings().remote_port)
        super(ADSModulated, self).connect_handles()

    def preset(self):
        super(ADSModulated, self).preset()
        if self.unique_handle(self.handles['ads']):
            self.handles['ads'].preset()
            self.handles['ads'].write("_fund_0", Settings().f0)
            self.handles['ads'].write("_t_stop", Settings().t_stop)
            self.handles['ads'].write("_t_step", Settings().t_step)

    @property
    def freq(self):
        return self.handles['ads'].read_netlist("_fund_1")*self.harmonics

    @bounded_property
    def _z_set(self):
        avg = self.handles['ads'].read_netlist("_Z" + str(self.port))[0:self.num_harmonics]
        t_points = self._z_set_.shape[-1]
        for harm_idx in range(1, self.num_harmonics+1):
            i_filename = os.sep.join((Settings().data_root, "simulation", "Z%d%d_I.txt" % (self.port, harm_idx)))
            q_filename = os.sep.join((Settings().data_root, "simulation", "Z%d%d_Q.txt" % (self.port, harm_idx)))
            self._z_set_[harm_idx - 1, :] = load_iq_txt(i_filename, q_filename, t_points)
        self._z_set_[:, :] = self._z_set_.set_avg(avg)
        return self._z_set_

    @_z_set.setter
    def _z_set(self, _z_set):
        _z_set._rms = False
        avg = tf.avg(_z_set)
        avg = np.pad(avg, ((0, self.handles['ads'].order - avg.shape[-1]), (0, 0)),
                     mode='constant', constant_values=50)
        self.handles['ads'].write("_Z" + str(self.port), avg)
        iq = tf.iq(_z_set)
        for harm_idx in range(1, self.num_harmonics+1):
            i_filename = os.sep.join((Settings().data_root, "simulation", "Z%d%d_I.txt" % (self.port, harm_idx)))
            q_filename = os.sep.join((Settings().data_root, "simulation", "Z%d%d_Q.txt" % (self.port, harm_idx)))
            save_iq_txt(iq[harm_idx - 1, :], i_filename, q_filename)

    @bounded_property
    def _z(self):
        return self._z_

    def trigger(self):
        self.handles['ads'].write("_t_stop", Settings().t_step * (self._z_.shape[-2] - 1))
        self.handles['ads'].import_iq()
        self.handles['ads'].measure()

    def measure(self):
        self._z_[:, :] = si_eps_map[SI.Z]
        eps = Settings().t_step/2
        mask = (self.time < self._delay - eps) | (self.time > self._delay + self._pulse_width + eps)
        try:
            _z_ = self.handles['ads'].read("RFPwrSource" + str(self.port) + ".Z_", 0, range(1,self.num_harmonics+1), mask)
            self._z_[:, 0] = _z_[0, :, 0].reshape((-1, 1)) * len(self.time)
        except IndexError:
            logging.warning("ADS dataset buffer does not contain enough data, please run a measurement to update buffer")
            self._z_[:, 0] = 50 * len(self.time)
