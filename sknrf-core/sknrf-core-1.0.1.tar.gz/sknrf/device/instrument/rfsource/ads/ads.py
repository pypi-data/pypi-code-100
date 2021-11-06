import os

import numpy as np
import torch as th

from sknrf.enums.runtime import SI, si_eps_map
from sknrf.device.signal import tf
from sknrf.device.simulator.keysight.ads import ADSSimulator
from sknrf.device.instrument.rfsource import base
from sknrf.settings import Settings
from sknrf.utilities.numeric import Info, PkAvg, Format, bounded_property
from sknrf.utilities.dsp import load_iq_txt, save_iq_txt

__author__ = 'dtbespal'


class ADSCW(base.NoRFSource):
    firmware_map = {'Keysight ADS': "2012.08"}
    display_order = ["on", "initialized", "port", "freq", "a_p",
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
        self._a_p = th.zeros_like(self._a_p_)
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
        self._a_p = self._a_p_
        self.initialized = True

    def __info__(self):
        super(ADSCW, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["_a_p"] = Info("_a_p", read=False, write=False, check=False,
                                 min_=0, max_=100, abs_tol=1e-4, rel_tol=1e-3)
        self.info["a_p"].min, self.info["a_p"].max = 0, 100
        self.info["a_p"].abs_tol, self.info["a_p"].rel_tol = 1e-4, 1e-3

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
    def _on(self):
        return bool(self.handles['ads'].read_netlist("RFPwrSource" + str(self.port) + ".On"))

    @_on.setter
    def _on(self, _on):
            self.handles['ads'].write("RFPwrSource" + str(self.port) + ".On", int(_on))

    @property
    def freq(self):
        return self.handles['ads'].read_netlist("_fund_1")*self.harmonics

    @bounded_property
    def _a_p(self):
        pk = self.handles['ads'].read_netlist("_A" + str(self.port))[0:self.num_harmonics]
        self._a_p_[:, :] = self._a_p_.set_pk(pk)
        return self._a_p_

    @_a_p.setter
    def _a_p(self, _a_p):
        _a_p._rms = True
        pk = tf.pk(_a_p).reshape(-1, 1)
        pk = np.pad(pk, ((0, self.handles['ads'].order - pk.shape[-1]), (0, 0)),
                    mode="constant", constant_values=si_eps_map[SI.A])
        self.handles['ads'].write("_A" + str(self.port), pk)
        iq = tf.iq(_a_p)
        for harm_idx in range(1, self.num_harmonics+1):
            i_filename = os.sep.join((Settings().data_root, "simulation", "A%d%d_I.txt" % (self.port, harm_idx)))
            q_filename = os.sep.join((Settings().data_root, "simulation", "A%d%d_Q.txt" % (self.port, harm_idx)))
            save_iq_txt(iq[harm_idx - 1, :], i_filename, q_filename)

    def trigger(self):
        self.handles['ads'].write("_t_stop", Settings().t_step * (self._a_p_.shape[-2] - 1))
        self.handles['ads'].measure()


class ADSModulated(base.NoRFSourceModulated):
    firmware_map = {'Keysight ADS': "2012.08"}
    display_order = ["on", "initialized", "port", "freq", "a_p",
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
        self._a_p = th.zeros_like(self._a_p_)
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
        self._a_p = self._a_p_
        self.initialized = True

    def __info__(self):
        super(ADSModulated, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["_a_p"] = Info("a_p", read=False, write=False, check=False,
                                 min_=0, max_=100, abs_tol=1e-4, rel_tol=1e-3)
        self.info["a_p"].min, self.info["a_p"].max = 0, 100
        self.info["a_p"].abs_tol, self.info["a_p"].rel_tol = 1e-4, 1e-3

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
    def _on(self):
        return bool(self.handles['ads'].read_netlist("RFPwrSource" + str(self.port) + ".On"))

    @_on.setter
    def _on(self, _on):
            self.handles['ads'].write("RFPwrSource" + str(self.port) + ".On", int(_on))

    @property
    def freq(self):
        return self.handles['ads'].read_netlist("_fund_1")*self.harmonics

    @bounded_property
    def _a_p(self):
        pk = self.handles['ads'].read_netlist("_A" + str(self.port))[0:self.num_harmonics]
        t_points = self._a_p_.shape[-1]
        for harm_idx in range(1, self.num_harmonics+1):
            i_filename = os.sep.join((Settings().data_root, "simulation", "A%d%d_I.txt" % (self.port, harm_idx)))
            q_filename = os.sep.join((Settings().data_root, "simulation", "A%d%d_Q.txt" % (self.port, harm_idx)))
            self._a_p_[harm_idx - 1, :] = load_iq_txt(i_filename, q_filename, t_points)
            self._a_p_[:, :] = self._a_p_.set_pk(pk)
        return self._a_p_

    @_a_p.setter
    def _a_p(self, _a_p):
        _a_p._rms = True
        pk = tf.pk(_a_p).reshape(-1, 1)
        pk = np.pad(pk, ((0, self.handles['ads'].order - pk.shape[-1]), (0, 0)),
                    mode="constant", constant_values=si_eps_map[SI.A])
        self.handles['ads'].write("_A" + str(self.port), pk)
        iq = tf.iq(_a_p)
        for harm_idx in range(1, self.num_harmonics+1):
            i_filename = os.sep.join((Settings().data_root, "simulation", "A%d%d_I.txt" % (self.port, harm_idx)))
            q_filename = os.sep.join((Settings().data_root, "simulation", "A%d%d_Q.txt" % (self.port, harm_idx)))
            save_iq_txt(iq[harm_idx-1, :], i_filename, q_filename)

    def trigger(self):
        self.handles['ads'].write("_t_stop", Settings().t_step * (self._a_p_.shape[-2] - 1))
        self.handles['ads'].import_iq()
        self.handles['ads'].measure()


if __name__ == "__main__":
    Settings().netlist_filename = "test_ADSCW_netlist.txt"
    Settings().dataset_filename = "test_ADSCW_dataset.mat"
    Settings().t_stop = 1e-6
    Settings().t_step = 2e-6
    Settings().f0 = 1e9
    Settings().num_harmonics = 3
    rf_source = ADSModulated(port=1, simulator_type="HB.Env1", simulator_name="Env1")
    rf_source.a_p[:, :] = 1
    rf_source.on = True
