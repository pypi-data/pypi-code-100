import os
import logging

import math as mt
import torch as th
import pyvisa as visa
from scipy.signal import resample

from sknrf.device.signal import tf
from sknrf.device.base import device_logger
from sknrf.device.instrument.rfsource import base
from sknrf.device.instrument.shared.sg.ape.quantiflash import QuantiFlash
from sknrf.settings import Settings
from sknrf.app.dataviewer.model.dataset import IQFile
from sknrf.utilities.numeric import Scale, Info, bounded_property, PkAvg, Format
from sknrf.utilities.rf import rW2dBm, dBm2rW, dBU2rU


logger = device_logger(logging.getLogger(__name__))

__author__ = 'dtbespal'


def scale(x, x_min, x_max, y_min=-1.0, y_max=1.0):
    return (x - x_min)/(x_max - x_min)*(y_max - y_min) + y_min


class QuantiFlashmcBDCW(base.NoRFSource):
    firmware_map = {}
    display_order = ["on", "initialized", "freq", "a_p", "v_s",
                     "num_harmonics", "harmonics"]


    def __new__(cls, error_model, port, config_filename="",
                resource_id="172.16.0.50"):
        self = super(QuantiFlashmcBDCW, cls).__new__(cls, error_model, port, config_filename)
        # Define object ATTRIBUTES
        self.resource_id = resource_id
        self.port = port
        self._on_ = False
        return self

    def __getnewargs__(self):
        return tuple(list(super(QuantiFlashmcBDCW, self).__getnewargs__()) + [self.resource_id])

    def __init__(self, error_model, port, config_filename="",
                 resource_id="172.16.0.50"):
        super().__init__(error_model, port, config_filename)
        self.connect_handles()
        self.__info__()
        self.preset()
        self.port = port

        # Initialize object PROPERTIES
        self._on = False
        self._a_p = dBm2rW(-130.00) * th.ones_like(self._a_p_)
        self.initialized = True

    def __getstate__(self, state={}):
        state = super(QuantiFlashmcBDCW, self).__getstate__(state=state)
        return state

    def __setstate__(self, state, *args, **kwargs):
        super().__setstate__(state)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self._a_p = self._a_p_
        self.initialized = True

    def __info__(self):
        super(QuantiFlashmcBDCW, self).__info__()
        abs_tol = dBm2rW(-30.0) - dBm2rW(-30.1)
        rel_tol = dBU2rU(0.1) - 1
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["resource_id"] = Info("resource_id", read=False, write=True, check=False)
        self.info["_a_p"] = Info("_a_p", read=False, write=False, check=False,
                                 min_=dBU2rU(-15.0), max_=dBU2rU(0.0), abs_tol=abs_tol, rel_tol=rel_tol,
                                 scale=Scale._)
        self.info["a_p"].scale = Scale._
        self.info["a_p"].min, self.info["a_p"].max = dBU2rU(-15.0), dBU2rU(0.0)
        self.info["v_s"].min, self.info["v_s"].max = dBU2rU(-15.0)*mt.sqrt(50.), dBU2rU(0.0)*mt.sqrt(50.)

    def connect_handles(self):
        self.handles["sg"] = QuantiFlash(host=self.resource_id)
        super(QuantiFlashmcBDCW, self).connect_handles()

    def disconnect_handles(self):
        super(QuantiFlashmcBDCW, self).disconnect_handles()

    def preset(self):
        super(QuantiFlashmcBDCW, self).preset()
        if self.unique_handle(self.handles["sg"]):

            self.handles["sg"].connect_target()
            if not self.handles["sg"].connected:
                raise ConnectionError("Quantiflash Not Connected")

            self.handles["sg"].setLEDControl('AUTOMATIC')  # MANUALLY | AUTOMATIC SETTING TO MANUAL mode
            self.handles["sg"].setPulseIntensity('OFF')  # OFF | -30 - 0
            self.handles["sg"].setTriggerIntensity(50)  # off | 0 - 100
            self.handles["sg"].selectPulseShape(0)  # 0: square

            f_rep = 1000
            if 1 / f_rep < Settings().t_stop:
                raise ValueError("frep too high, make sure 1/f_rep >= Settings().t_stop ")
            self.handles["sg"].setPulseRate(1000)  # 3 - 10000

    @property
    def _on(self):
        return self._on_

    @_on.setter
    def _on(self, _on):
        if _on:
            self.handles["sg"].setLEDControl('MANUALLY')  # if on change the setup to manual
            self.handles["sg"].setChannelActive(self.port)
            temp = 2**(self.port-1)
            self.handles["sg"].setChannel(temp)
            self.handles["sg"].setLEDMode('BRIGHT')  # DARK | BRIGHT
            pk = tf.pk(self._a_p_).abs().item()
            pk = int(scale(pk ** 2, 0.03162, 1.0, 165, (1 << 12) - 1))
            self.handles["sg"].setLedIntensity(pk)

        else:
            self.handles["sg"].setLEDControl('MANUALLY') # Have to set to manual to turn off channels
            self.handles["sg"].setChannel("0") #turn off all channels
            self.handles["sg"].setLEDControl('AUTOMATIC')
            self.handles["sg"].setPulseIntensity("OFF")

        self._on_ = _on



    @bounded_property
    def _a_p(self):
        return self._a_p_

    @_a_p.setter
    def _a_p(self, _a_p):
        pk_rW = tf.pk(_a_p).item()
        pk = int(scale(pk_rW ** 2, 0.03162, 1.0, 165, (1 << 12) - 1))
        self.handles["sg"].setLedIntensity(pk)
        self._a_p_[:, :] = pk_rW

    def arm(self):
        pass

    def trigger(self):
        pass


class QuantiFlashmcBDPulsed(base.NoRFSourcePulsed):
    firmware_map = {}
    display_order = ["on", "initialized", "freq", "a_p", "v_s",
                     "delay", "pulse_width",
                     "num_harmonics", "harmonics"]

    def __new__(cls, error_model, port, config_filename="",
                resource_id="172.16.0.50"):
        self = super(QuantiFlashmcBDPulsed, cls).__new__(cls, error_model, port, config_filename)
        # Define object ATTRIBUTES
        self.resource_id = resource_id
        self._on_ = False
        return self

    def __getnewargs__(self):
        return tuple(list(super(QuantiFlashmcBDPulsed, self).__getnewargs__()) + [self.resource_id])

    def __init__(self, error_model, port, config_filename="",
                 resource_id="172.16.0.50"):
        super().__init__(error_model, port, config_filename)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self._pulse_width = self.period
        self._delay = 0.0
        self._a_p = dBm2rW(-130.00)*th.ones_like(self._a_p_)
        self.initialized = True

    def __getstate__(self, state={}):
        state = super(QuantiFlashmcBDPulsed, self).__getstate__(state=state)
        return state

    def __setstate__(self, state, *args, **kwargs):
        super().__setstate__(state)
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
        super(QuantiFlashmcBDPulsed, self).__info__()
        abs_tol = dBm2rW(-30.0) - dBm2rW(-30.1)
        rel_tol = dBU2rU(0.1) - 1
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["resource_id"] = Info("resource_id", read=False, write=True, check=False)
        self.info["_a_p"] = Info("_a_p", read=False, write=False, check=False,
                                 min_=dBU2rU(-15.0), max_=dBU2rU(0.0), abs_tol=abs_tol, rel_tol=rel_tol,
                                 scale=Scale._)
        self.info["a_p"].scale = Scale._
        self.info["a_p"].min, self.info["a_p"].max = dBU2rU(-15.0), dBU2rU(0.0)
        self.info["v_s"].min, self.info["v_s"].max = dBU2rU(-15.0) * mt.sqrt(50.), dBU2rU(0.0) * mt.sqrt(50.)

    def connect_handles(self):
        self.handles["sg"] = QuantiFlash(host=self.resource_id)
        super(QuantiFlashmcBDPulsed, self).connect_handles()

    def disconnect_handles(self):
        super(QuantiFlashmcBDPulsed, self).disconnect_handles()

    def preset(self):
        super(QuantiFlashmcBDPulsed, self).preset()
        if self.unique_handle(self.handles["sg"]):

            self.handles["sg"].connect_target()
            if not self.handles["sg"].connected:
                raise ConnectionError("Quantiflash Not Connected")

            self.handles["sg"].setLEDControl('AUTOMATIC')  # MANUALLY | AUTOMATIC SETTING TO MANUAL mode
            self.handles["sg"].setPulseIntensity('OFF')  # OFF | -30 - 0
            self.handles["sg"].setTriggerIntensity(50)  # off | 0 - 100
            self.handles["sg"].selectPulseShape(0)  # 0: square
            f_rep = 1000
            if 1 / f_rep < Settings().t_stop:
                raise ValueError("frep too high, make sure 1/f_rep >= Settings().t_stop ")
            self.handles["sg"].setPulseRate(1000)  # 3 - 10000

    @property
    def _on(self):
        return self._on_

    @_on.setter
    def _on(self, _on):
        if _on:
            self.handles["sg"].setLEDControl('MANUALLY')  # if on change the setup to manual
            self.handles["sg"].setChannelActive(self.port)
            temp = 2 ** (self.port - 1)
            self.handles["sg"].setChannel(temp)
            self.handles["sg"].setLEDMode('BRIGHT')  # DARK | BRIGHT
            pk = tf.pk(self._a_p_).abs().item()
            pk = int(scale(pk ** 2, 0.03162, 1.0, 165, (1 << 12) - 1))
            self.handles["sg"].setLedIntensity(pk)
        else:
            self.handles["sg"].setLEDControl('MANUALLY')  # Have to set to manual to turn off channels
            self.handles["sg"].setChannel("0")  # turn off all channels
            self.handles["sg"].setLEDControl('AUTOMATIC')
            self.handles["sg"].setPulseIntensity("OFF")
        self._on_ = _on

    @bounded_property
    def _a_p(self):
        return self._a_p_

    @_a_p.setter
    def _a_p(self, _a_p):
        pk_rW = tf.pk(_a_p).item()
        pk = int(scale(pk_rW ** 2, 0.03162, 1.0, 165, (1 << 12) - 1))
        self.handles["sg"].setLedIntensity(pk)
        self._a_p_[:, :] = pk_rW


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
        self.handles["sg"].setPulseDuration(_pulse_width/1e-6)
        self._pulse_width_ = _pulse_width

    def arm(self):
        pass

    def trigger(self):
        pass

