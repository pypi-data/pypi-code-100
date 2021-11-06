import os
import logging

import torch as th

from sknrf.enums.runtime import SI, si_eps_map
from sknrf.settings import Settings
from sknrf.device.base import device_logger
from sknrf.device.simulator.keysight.ads import ADSSimulator
from sknrf.device.instrument.lfztuner import base
from sknrf.device.signal import tf
from sknrf.utilities.numeric import PkAvg, Format, bounded_property
from sknrf.utilities.dsp import load_iq_txt, save_iq_txt

__author__ = 'dtbespal'
logger = device_logger(logging.getLogger(__name__))


class ADSCW(base.NoLFZTuner):
    firmware_map = {'Keysight ADS': "2012.08"}
    display_order = ["on", "initialized", "port", "freq", "z_set", "z",
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
        self._z_set = th.zeros_like(self._z_set_)
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
        self.info["z_set"].abs_tol, self.info["z_set"].rel_tol = 1e-1, 1e-1

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

    @bounded_property
    def _z_set(self):
        avg = self.handles['ads'].read_netlist("LFZTuner" + str(self.port) + ".Z")
        self._z_set_[:, :] = self._z_set_.set_avg(avg)
        return self._z_set_

    @_z_set.setter
    def _z_set(self, _z_set):
        _z_set._rms = False
        avg = tf.avg(_z_set)
        self.handles['ads'].write("LFZTuner" + str(self.port) + ".Z", avg[0, 0])
        iq = tf.iq(_z_set)
        i_filename = os.sep.join((Settings().data_root, "simulation", "Z%d%d_I.txt" % (self.port, 0)))
        q_filename = os.sep.join((Settings().data_root, "simulation", "Z%d%d_Q.txt" % (self.port, 0)))
        save_iq_txt(iq[0, :], i_filename, q_filename)

    @bounded_property
    def _z(self):
        return self._z_

    def trigger(self):
        self.handles['ads'].write("_t_stop", Settings().t_step * (self._z_.shape[-1] - 1))
        self.handles['ads'].measure()

    def measure(self):
        self._z_[:, :] = si_eps_map[SI.Z]
        try:
            _z_ = self.handles['ads'].read("LFZTuner" + str(self.port) + ".Z_", 0, 0)
            self._z_[:, 0] = _z_[0, :, 0].reshape((-1, 1)) * len(self.time)
        except IndexError:
            logging.warning("ADS dataset buffer does not contain enough data, please run a measurement to update buffer")


class ADSModulated(base.NoLFZTunerModulated):
    firmware_map = {'Keysight ADS': "2012.08"}
    display_order = ["on", "initialized", "port", "freq", "z_set", "z",
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
        self.simulator_type = simulator_type
        self.simulator_name = simulator_name
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self._pulse_width = self.period
        self._delay = 0
        self.iq_files = self._iq_files_
        self._z_set = th.zeros_like(self._z_set_)
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
        self.info["z_set"].abs_tol, self.info["z_set"].rel_tol = 1e-1, 1e-1

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

    @bounded_property
    def _z_set(self):
        avg = self.handles['ads'].read_netlist("LFZTuner" + str(self.port) + ".Z")
        t_points = self._z_set_.shape[-1]
        i_filename = os.sep.join((Settings().data_root, "simulation", "Z%d%d_I.txt" % (self.port, 0)))
        q_filename = os.sep.join((Settings().data_root, "simulation", "Z%d%d_Q.txt" % (self.port, 0)))
        self._z_set_[0, :] = load_iq_txt(i_filename, q_filename, t_points)
        self._z_set_[:, :] = self._z_set_.set_avg(avg)
        return self._z_set_

    @_z_set.setter
    def _z_set(self, _z_set):
        _z_set._rms = False
        avg = tf.avg(_z_set)
        self.handles['ads'].write("LFZTuner" + str(self.port) + ".Z", avg[0, 0])
        iq = tf.iq(_z_set)
        i_filename = os.sep.join((Settings().data_root, "simulation", "Z%d%d_I.txt" % (self.port, 0)))
        q_filename = os.sep.join((Settings().data_root, "simulation", "Z%d%d_Q.txt" % (self.port, 0)))
        save_iq_txt(iq[0, :], i_filename, q_filename)

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
            _z_ = self.handles['ads'].read("LFZTuner" + str(self.port) + ".Z_", 0, 0, mask)
            self._z_[:, 0] = _z_[0, :, 0].reshape((-1, 1)) * len(self.time)
        except IndexError:
            logging.warning("ADS dataset buffer does not contain enough data, please run a measurement to update buffer")

