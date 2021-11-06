import logging
import time
import os

import numpy as np
import torch as th
from scipy.interpolate import interp1d

from sknrf.utilities import myaml
from sknrf.enums.device import SI, si_eps_map
from sknrf.settings import Settings
from sknrf.device.base import device_logger
from sknrf.device.signal import tf, ff
from sknrf.device.instrument.rfreceiver import base
from sknrf.device.instrument.shared.adc import Bird664469
from sknrf.device.instrument.shared.adc.Bird664469 import Bird664469Controller
from sknrf.utilities.numeric import Info, bounded_property

__author__ = 'dtbespal'
logger = device_logger(logging.getLogger(__name__))


# To harcode channel, search/replace chan =
class Bird664469Modulated(base.NoRFReceiverModulated):
    firmware_map = {}
    display_order = ["on", "initialized", "port", "freq", "a_p", "b_p", "v", "i",
                     "num_harmonics", "harmonics",
                     "channel", "adc_offset"]

    def __new__(cls, error_model, port, config_filename="", resource_id='172.16.0.132'):
        self = super(Bird664469Modulated, cls).__new__(cls, error_model, port, config_filename)
        # Define object ATTRIBUTES
        self.resource_id = resource_id
        self._on_ = False
        return self

    def __getnewargs__(self):
        return tuple(list(super(Bird664469Modulated, self).__getnewargs__())
                     + [self.resource_id, ])

    def __init__(self, error_model, port, config_filename="", resource_id='172.16.0.132'):
        super().__init__(error_model, port, config_filename)
        self.resource_id = resource_id

        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self.on = False
        self.channel = self.port - 1
        self.adc_offset = 0
        self.measure()
        self.initialized = True

    def __getstate__(self, state={}):
        state = super(Bird664469Modulated, self).__getstate__(state=state)
        return state

    def __setstate__(self, state, *args, **kwargs):
        super().__setstate__(state)
        self.resource_id = state["resource_id"]

        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self.on = False
        self.channel = self.port - 1
        self.adc_offset = state["_adc_offset"]
        self.measure()
        self.initialized = True

    def __info__(self):
        super(Bird664469Modulated, self).__info__()
        v_atol = 1e-3
        i_atol = v_atol/50.
        a_atol, b_atol = v_atol/np.sqrt(50.), v_atol/np.sqrt(50.)
        rtol = 1e-3
        v_max = self._config["voltage_limit"]
        i_max = v_max/50.
        a_max = b_max = v_max/np.sqrt(50.)
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["resource_id"] = Info("resource_id", read=True, write=True, check=False)
        self.info["channel"] = Info("channel", read=True, write=True, check=False,
                                       min_=0, max_=0xF)
        self.info["adc_offset"] = Info("adc_offset", read=True, write=True, check=False,
                                       min_=0, max_=0x3FFF)
        self.info["_a_p"] = Info("_a_p", read=False, write=False, check=False,
                                 min_=si_eps_map[SI.A], max_=a_max, abs_tol=a_atol, rel_tol=rtol)
        self.info["_b_p"] = Info("_b", read=False, write=False, check=False,
                                 min_=si_eps_map[SI.B], max_=b_max, abs_tol=b_atol, rel_tol=rtol)
        self.info["_v"] = Info("_v", read=False, write=False, check=False,
                               min_=si_eps_map[SI.V], max_=v_max, abs_tol=v_atol, rel_tol=rtol)
        self.info["_i"] = Info("_i", read=False, write=False, check=False,
                               min_=si_eps_map[SI.I], max_=i_max, abs_tol=i_atol, rel_tol=rtol)
        self.info["a_p"].min, self.info["a_p"].max = 0., a_max
        self.info["b_p"].min, self.info["b_p"].max = 0., b_max
        self.info["v"].min, self.info["v"].max = 0, v_max
        self.info["i"].min, self.info["i"].max = 0, i_max

    def connect_handles(self):
        self.handles["adc"] = Bird664469Controller(self._config, self.resource_id)
        super(Bird664469Modulated, self).connect_handles()

    def preset(self):
        super(Bird664469Modulated, self).preset()
        if self.unique_handle(self.handles["adc"]):
            Bird664469.preset(self)

    @property
    def channel(self):
        ctrl = self.handles["adc"]
        return self._channel


    @channel.setter
    def channel(self, channel):
        ctrl = self.handles["adc"]
        ctrl.set_reg("{:s}_top_ctrl".format(self._config["FPGA_NAME"]), 0, "ila_testbus_sel", int(channel/8))
        self._channel = channel

    @property
    def adc_offset(self):
        return self._adc_offset

    @adc_offset.setter
    def adc_offset(self, adc_offset):
        if self._config["FPGA_NAME"] == "mela":
            if adc_offset >= 0:
                chan = self.port - 1
                ctrl = self.handles["adc"]
                ctrl.socket.sendall(bytes("dac_write(0, {:d}, {:d})\n".format(chan + 16, adc_offset), "utf-8"))
                resp = str(ctrl.socket.recv(1024), "utf-8")
                if len(resp.strip()):
                    raise ConnectionError("Unable to set adc_offset: {:s}".format(resp))
                self._adc_offset = adc_offset

    @property
    def _on(self):
        return self._on_

    @_on.setter
    def _on(self, _on):
        self._on_ = _on

    @bounded_property
    def _a_p(self):
        return self._a_p_

    @bounded_property
    def _b_p(self):
        return self._b_p_

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

    def arm(self):
        Bird664469.arm(self)

    def trigger(self):
        Bird664469.trigger(self)

    def measure(self):
        if self.port == 1:
            self.handles["adc"].measure()
        chan = (self.port - 1) % 8
        v_ = self.handles["adc"].data[:Settings().t_points, chan:chan+1]
        self._b_p_[:, 0:1] = v_/np.sqrt(50.)
        super().measure()


class Bird664469CeresModulated(Bird664469Modulated):

    def __new__(cls, error_model, port, config_filename="Bird664469Ceres.yml", resource_id='172.16.0.133'):
        self = super(Bird664469Modulated, cls).__new__(cls, error_model, port, config_filename)
        return self

    def __init__(self, error_model, port, config_filename="Bird664469Ceres.yml", resource_id='172.16.0.133'):
        super().__init__(error_model, port, config_filename)


class Bird664469MetisModulated(Bird664469Modulated):

    def __new__(cls, error_model, port, config_filename="Bird664469Metis.yml", resource_id='172.16.0.133'):
        self = super(Bird664469Modulated, cls).__new__(cls, error_model, port, config_filename)
        return self

    def __init__(self, error_model, port, config_filename="Bird664469Metis.yml", resource_id='172.16.0.133'):
        super().__init__(error_model, port, config_filename)
