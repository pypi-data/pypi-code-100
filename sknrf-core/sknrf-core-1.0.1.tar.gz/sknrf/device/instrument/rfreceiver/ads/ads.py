import logging

import numpy as np

from sknrf.enums.device import Response
from sknrf.settings import Settings
from sknrf.device.base import AbstractDevice, device_logger
from sknrf.device.simulator.keysight.ads import ADSSimulator
from sknrf.device.instrument.rfreceiver import base
from sknrf.utilities.numeric import AttributeInfo, Info, PkAvg, Format, bounded_property
from sknrf.utilities.rf import viz2baz

__author__ = 'dtbespal'
logger = device_logger(logging.getLogger(__name__))


class ADSCW(base.NoRFReceiver):
    firmware_map = {'Keysight ADS': "2012.08"}
    display_order = ["initialized", "port", "freq", "a_p", "b_p", "v", "i",
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
        self.measure()
        self.initialized = True

    def __info__(self):
        super(ADSCW, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["_a_p"] = Info("_a_p", read=False, write=False, check=False,
                                 min_=1e-1000, max_=100, abs_tol=1e-4, rel_tol=1e-3)
        self.info["_b_p"] = Info("_b_p", read=False, write=False, check=False,
                                 min_=1e-100, max_=100, abs_tol=1e-4, rel_tol=1e-3)
        self.info["_v"] = Info("_a_p", read=False, write=False, check=False,
                               min_=1e-100, max_=100, abs_tol=1e-4, rel_tol=1e-3)
        self.info["_i"] = Info("_b_p", read=False, write=False, check=False,
                               min_=1e-100, max_=100, abs_tol=1e-4, rel_tol=1e-3)
        self.info["a_p"].min, self.info["a_p"].max = 0, 100
        self.info["b_p"].min, self.info["b_p"].max = 0, 100
        self.info["v"].min, self.info["v"].max = 0, 100
        self.info["i"].min, self.info["i"].max = 0, 100

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
        return bool(self.handles['ads'].read_netlist("_Enable" + str(self.port)))

    @_on.setter
    def _on(self, _on):
        self.handles['ads'].write("_Enable" + str(self.port), int(_on))

    @property
    def freq(self):
        return self.handles['ads'].read_netlist("_fund_1")*self.harmonics

    @bounded_property
    def _a_p(self):
        return self._a_p_

    @bounded_property
    def _b_p(self):
        return self._b_p_

    def trigger(self):
        self.handles['ads'].write("_t_stop", Settings().t_step * (self._a_p_.shape[-2] - 1))
        self.handles['ads'].measure()

    def measure(self):
        factor = 1
        try:
            _v_ = factor*self.handles['ads'].read("V" + str(self.port), 0, range(1,self.num_harmonics+1))
            # if self.port == 0:
            _i_ = factor*self.handles['ads'].read("I" + str(self.port) + ".i", 0, range(1,self.num_harmonics+1))
            # else:
            #     _i_ = factor * self.handles['ads'].read("I" + str(self.port), 0, range(1, self.num_harmonics + 1))
        except IndexError:
            logging.warning("ADS dataset buffer does not contain enough data, please run a measurement to update buffer")
            _v_ = self.info["_v"].min
            _i_ = self.info["_i"].min
        self._b_p_[:, :], self._a_p_[:, :], _ = viz2baz(_v_, _i_)



class ADSModulated(base.NoRFReceiverModulated):
    firmware_map = {'Keysight ADS': "2012.08"}
    display_order = ["initialized", "freq", "a_p", "b_p", "v", "i",
                     "delay", "pulse_width", "period",
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
        self._pulse_width = self._pulse_width
        self._delay = self._delay
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
        self.measure()
        self.initialized = True

    def __info__(self):
        super(ADSModulated, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["_a_p"] = Info("_a_p", read=False, write=False, check=False,
                                 min_=1e-100, max_=100, abs_tol=1e-4, rel_tol=1e-3)
        self.info["_b_p"] = Info("_b_p", read=False, write=False, check=False,
                                 min_=1e-100, max_=100, abs_tol=1e-4, rel_tol=1e-3)
        self.info["_v"] = Info("_a_p", read=False, write=False, check=False,
                               min_=1e-100, max_=100, abs_tol=1e-4, rel_tol=1e-3)
        self.info["_i"] = Info("_b_p", read=False, write=False, check=False,
                               min_=1e-100, max_=100, abs_tol=1e-4, rel_tol=1e-3)
        self.info["a_p"].min, self.info["a_p"].max = 0, 100
        self.info["b_p"].min, self.info["b_p"].max = 0, 100
        self.info["v"].min, self.info["v"].max = 0, 100
        self.info["i"].min, self.info["i"].max = 0, 100

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
        return bool(self.handles['ads'].read_netlist("_Enable" + str(self.port)))

    @_on.setter
    def _on(self, _on):
        self.handles['ads'].write("_Enable" + str(self.port), int(_on))

    @property
    def freq(self):
        return self.handles['ads'].read_netlist("_fund_1")*self.harmonics

    @bounded_property
    def _a_p(self):
        return self._a_p_

    @bounded_property
    def _b_p(self):
        return self._b_p_

    def trigger(self):
        self.handles['ads'].write("_t_stop", Settings().t_step*(self._a_p_.shape[-2]-1))
        # self.handles['ads'].import_iq()
        self.handles['ads'].measure()

    def measure(self):
        _v_ = np.zeros(self._b_p_.shape, dtype=np.complex)
        _i_ = np.zeros(self._a_p_.shape, dtype=np.complex)
        mask_array = np.bitwise_or(self.time >= self.delay, self.time < self.delay + self.pulse_width)
        mask_array = mask_array.flatten()
        try:
            _v_[mask_array, :] = self.handles['ads'].read("V" + str(self.port), 0, range(1, self.num_harmonics+1), mask_array)
            _i_[mask_array, :] = self.handles['ads'].read("I" + str(self.port) + ".i", 0, range(1, self.num_harmonics+1), mask_array)
        except IndexError:
            logging.warning("ADS dataset buffer does not contain enough data, please run a measurement to update buffer")
            _v_[mask_array, :] = self.info["_v"].min
            _i_[mask_array, :] = self.info["_i"].min
        self._b_p_[:, :], self._a_p_[:, :], _ = viz2baz(_v_, _i_)

