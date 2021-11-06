import os

import torch as th

from sknrf.device.simulator.keysight.ads import ADSSimulator
from sknrf.device.instrument.lfsource import base
from sknrf.settings import Settings
from sknrf.device.signal import tf
from sknrf.utilities.numeric import Info, PkAvg, Format, bounded_property
from sknrf.utilities.dsp import load_iq_txt, save_iq_txt
from sknrf.utilities.rf import n2t

__author__ = 'dtbespal'


class ADSCW(base.NoLFSource):
    firmware_map = {'Keysight ADS': "2012.08"}
    display_order = ["on", "initialized", "port", "freq", "v",
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
        self._v = th.zeros_like(self._v_)
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
        self._v = self._v_
        self.initialized = True

    def __info__(self):
        super(ADSCW, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["_v"] = Info("_v", read=False, write=False, check=False,
                               min_=0, max_=100, abs_tol=1e-4, rel_tol=1e-3)
        self.info["v"].min, self.info["v"].max = 0, 100
        self.info["v"].abs_tol, self.info["v"].rel_tol = 1e-4, 1e-3

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
        return bool(self.handles['ads'].read_netlist("LFSource" + str(self.port) + ".On"))

    @_on.setter
    def _on(self, _on):
            self.handles['ads'].write("LFSource" + str(self.port) + ".On", int(_on))

    @bounded_property
    def _v(self):
        pk = self.handles['ads'].read_netlist("LFSource" + str(self.port) + ".Bias")
        self._v_[:, :] = self._v_.set_pk(pk)
        return self._v_

    @_v.setter
    def _v(self, _v):
        _v._rms = True
        pk = tf.pk(_v)
        self.handles['ads'].write("LFSource" + str(self.port) + ".Bias", pk[0, 0])
        iq = tf.iq(_v)
        i_filename = os.sep.join((Settings().data_root, "simulation", "V%d%d_I.txt" % (self.port, 0)))
        q_filename = os.sep.join((Settings().data_root, "simulation", "V%d%d_Q.txt" % (self.port, 0)))
        save_iq_txt(iq[0, :], i_filename, q_filename)

    def trigger(self):
        self.handles['ads'].write("_t_stop", Settings().t_step * (self._v_.shape[-2] - 1))
        self.handles['ads'].measure()


class ADSModulated(base.NoLFSourceModulated):
    firmware_map = {'Keysight ADS': "2012.08"}
    display_order = ["on", "initialized", "port", "freq", "v",
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
        self._v = th.zeros_like(self._v_)
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
        self._v = self._v_
        self.initialized = True

    def __info__(self):
        super(ADSModulated, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["_v"] = Info("_v", read=False, write=False, check=False,
                               min_=0, max_=100, abs_tol=1e-4, rel_tol=1e-3)
        self.info["v"].min, self.info["v"].max = 0, 100
        self.info["v"].abs_tol, self.info["v"].rel_tol = 1e-4, 1e-3

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
        return bool(self.handles['ads'].read_netlist("LFSource" + str(self.port) + ".On"))

    @_on.setter
    def _on(self, _on):
            self.handles['ads'].write("LFSource" + str(self.port) + ".On", int(_on))

    @property
    def _delay(self):
        return self._delay_

    @_delay.setter
    def _delay(self, _delay):
        self._delay_ = _delay

    @property
    def _pulse_width(self):
        return self._pulse_width_

    @_pulse_width.setter
    def _pulse_width(self, _pulse_width):
        self._pulse_width_ = _pulse_width

    @bounded_property
    def _v(self):
        pk = self.handles['ads'].read_netlist("LFSource" + str(self.port) + ".Bias")
        t_points = self._v_.shape[-1]
        i_filename = os.sep.join((Settings().data_root, "simulation", "V%d%d_I.txt" % (self.port, 0)))
        q_filename = os.sep.join((Settings().data_root, "simulation", "V%d%d_Q.txt" % (self.port, 0)))
        self._v_[0, :] = load_iq_txt(i_filename, q_filename, t_points).abs()
        self._v_[:, :] = self._v_.set_pk(pk)
        return self._v_

    @_v.setter
    def _v(self, _v):
        _v._rms = True
        pk = tf.pk(_v)
        self.handles['ads'].write("LFSource" + str(self.port) + ".Bias", pk[0, 0])
        iq = tf.iq(_v)
        i_filename = os.sep.join((Settings().data_root, "simulation", "V%d%d_I.txt" % (self.port, 0)))
        q_filename = os.sep.join((Settings().data_root, "simulation", "V%d%d_Q.txt" % (self.port, 0)))
        save_iq_txt(iq[0, :], i_filename, q_filename)

    def trigger(self):
        self.handles['ads'].write("_t_stop", Settings().t_step * (self._v_.shape[-2] - 1))
        self.handles['ads'].import_iq()
        self.handles['ads'].measure()
