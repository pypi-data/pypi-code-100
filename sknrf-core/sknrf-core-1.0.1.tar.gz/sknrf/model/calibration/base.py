"""
    ===========================
    Abstract Calibration Model
    ===========================

    This module defines all calibration models.

    See Also
    ----------
    sknrf.model.base.AbstractModel
"""

import abc
import logging
import os
import re
from collections import OrderedDict

import math as mt
import torch as th
import skrf

from sknrf.settings import Settings, InstrumentFlag
from sknrf.device.signal import ff
from sknrf.model.base import AbstractModel
from sknrf.app.dataviewer.model.mdif import MDIF
from sknrf.app.dataviewer.model.snp import SNP
from sknrf.model.sequencer.measure import Measure
from sknrf.utilities.numeric import Info
from sknrf.utilities.rf import g2z

logger = logging.getLogger(__name__)

instrument_label_map = OrderedDict(((InstrumentFlag.LFSOURCE, "LF Source"),
                                    (InstrumentFlag.LFRECEIVER, "LF Receiver"),
                                    (InstrumentFlag.LFZTUNER, "LF Impedance Tuner"),
                                    (InstrumentFlag.RFSOURCE, "RF Source"),
                                    (InstrumentFlag.RFRECEIVER, "RF Receiver"),
                                    (InstrumentFlag.RFZTUNER, "RF Impedance Tuner")))

instrument_enable_map = OrderedDict(((InstrumentFlag.LFSOURCE, True),
                                    (InstrumentFlag.LFRECEIVER, True),
                                    (InstrumentFlag.LFZTUNER, True),
                                    (InstrumentFlag.RFSOURCE, True),
                                    (InstrumentFlag.RFRECEIVER, True),
                                    (InstrumentFlag.RFZTUNER, True)))

label_instrument_map = OrderedDict((("LF Source", InstrumentFlag.LFSOURCE),
                                    ("LF Receiver", InstrumentFlag.LFRECEIVER),
                                    ("LF Impedance Tuner", InstrumentFlag.LFZTUNER),
                                    ("RF Source", InstrumentFlag.RFSOURCE),
                                    ("RF Receiver", InstrumentFlag.RFRECEIVER),
                                    ("RF Impedance Tuner", InstrumentFlag.RFZTUNER)))

calkit_connector_map = OrderedDict((
    ("ideal",os.sep.join((Settings().data_root, "calkits", "ideal"))),
    ("1.8 mm", os.sep.join((Settings().data_root, "calkits", "1.8mm"))),
    ("3.5 mm(m)", os.sep.join((Settings().data_root, "calkits", "3.5mm(m)"))),
    ("3.5 mm(f)", os.sep.join((Settings().data_root, "calkits", "3.5mm(f)"))),
    ("7 mm", os.sep.join((Settings().data_root, "calkits", "7mm"))),
    ("N Type(m)", os.sep.join((Settings().data_root, "calkits", "NType(m)"))),
    ("N Type(f)", os.sep.join((Settings().data_root, "calkits", "NType(f)")))
))


def delay1(rfztuner):
    z = th.zeros_like(rfztuner.z_set)
    z[:, 0] = g2z(0.9999)[0]  # *th.exp(1j*mt.pi/180*90))[0]*Settings().t_points
    return z


def delay2(rfztuner):
    z = th.zeros_like(rfztuner.z_set)
    z[:, 0] = g2z(0.9999)[0]  # *th.exp(1j*mt.pi/180*-90))[0]*Settings().t_points
    return z


def short(rfztuner):
    z = g2z(0.9999)[0]  # *th.exp(1j*mt.pi/180*180))[0]*Settings().t_points
    z = z + th.zeros_like(rfztuner.z_set)
    return z


def open(rfztuner):
    z = g2z(0.9999)[0] # * th.exp(1j*mt.pi/180*0))[0]*Settings().t_points
    z = z + th.zeros_like(rfztuner.z_set)
    return z


def load(rfztuner):
    z = th.full_like(rfztuner.z_set, 50.01*Settings().t_points)
    return z


cal_standard_map = {
    "short": short,
    "open": open,
    "load": load,
    "thru": load,
    "thru with b wave attenuator connected ss": load,
    "thru with b wave attenuator not connected ss": load,
    "line": load,
    "delay": delay1,
    "delay1": delay1,
    "delay2": delay2,
    "reflect": short,
    "rfsourceref": None,
    "rfreceiverref": None,
    "__HalfKnownReflection": short,
    "__Reflection": short,
    "__Transmission": short,
    "__Unknown": load
}


class AbstractCalibrationModel(AbstractModel):
    """A calibration model for a OnePort Calibration.

        See Also
        ----------
        SDDL, PHN
    """

    def __new__(cls, instrument_flags=InstrumentFlag.ALL):
        self = super(AbstractCalibrationModel, cls).__new__(cls)
        self.instrument_flags = instrument_flags
        return self

    def __getnewargs__(self):
        return (self.instrument_flags,)

    def __init__(self, instrument_flags=InstrumentFlag.ALL):
        AbstractModel.__init__(self)
        if not hasattr(self, "calibration"):
            self.calibration = None
        self._port_indices = []
        self.port_indices = []
        self.dataset_names = OrderedDict()
        self.port_connectors = ["ideal"] * Settings().num_ports
        self.adapter_filenames = [""] * Settings().num_ports
        self.calkit_connectors = ["ideal"] * Settings().num_ports
        self.instrument_flags = instrument_flags
        self.measured_ntwks = OrderedDict()
        self.ideal_ntwks = OrderedDict()
        self.measurement_type = ""
        if not self.instrument_flags:
            raise AttributeError("At least one instrument flag must be raised")

    def __getstate__(self, state={}):
        state = super(AbstractCalibrationModel, self).__getstate__(state=state)
        # ### Manually save selected object PROPERTIES here ###
        state["calibration"] = self.calibration
        state["_port_indices"] = self._port_indices
        state["dataset_names"] = self.dataset_names
        state["port_connectors"] = self.port_connectors
        state["adapter_filenames"] = self.adapter_filenames
        state["calkit_connectors"] = self.calkit_connectors
        state["measured_ntwks"] = self.measured_ntwks
        state["ideal_ntwks"] = self.ideal_ntwks
        state["measurement_type"] = self.measurement_type
        return state

    def __setstate__(self, state):
        super(AbstractCalibrationModel, self).__setstate__(state)
        # ### Manually load saved object ATTRIBUTES and PROPERTIES here ###
        self.calibration = state["calibration"]
        self._port_indices = state["_port_indices"]
        self.dataset_names = state["dataset_names"]
        self.port_connectors = state["port_connectors"]
        self.adapter_filenames = state["adapter_filenames"]
        self.calkit_connectors = state["calkit_connectors"]
        self.measured_ntwks = state["measured_ntwks"]
        self.ideal_ntwks = state["ideal_ntwks"]
        self.measurement_type = state["measurement_type"]

    def __info__(self):
        """ Initializes the display information of a device and stores information in self.info.
        """
        super(AbstractCalibrationModel, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["calibration"] = Info("calibration", read=False, write=False, check=False)
        self.info["port_indices"] = Info("port_indices", read=False, write=False, check=False)
        self.info["dataset_names"] = Info("dataset_names", read=False, write=False, check=False)
        self.info["port_connectors"] = Info("port_connectors", read=False, write=False, check=False)
        self.info["adapter_filenames"] = Info("adapter_filenames", read=False, write=False, check=False)
        self.info["calkit_connectors"] = Info("calkit_connectors", read=False, write=False, check=False)
        self.info["instrument_flags"] = Info("instrument_flags", read=False, write=False, check=False)
        self.info["measured_ntwks"] = Info("measured_ntwks", read=False, write=False, check=False)
        self.info["ideal_ntwks"] = Info("ideal_ntwks", read=False, write=False, check=False)
        self.info["measurement_type"] = Info("measurement_type", read=False, write=False, check=False)

    @property
    def _min_freq(self):
        return 0 if self.instrument_flags & InstrumentFlag.LF else 1

    @property
    def _max_freq(self):
        return Settings().f_points if self.instrument_flags & InstrumentFlag.RF else 1

    def freq_slice(self):
        return slice(Settings().t_points*self._min_freq, Settings().t_points*self._max_freq, 1), slice(None), slice(None)

    def datagroup_name(self):
        return self.__class__.__name__

    @property
    def port_indices(self):
        return self._port_indices

    @port_indices.setter
    def port_indices(self, port_indices):
        self._port_indices = port_indices

    @staticmethod
    def name_info(name):
        page_name, port_nums = re.search(r"([\_]*[^\_]+)([\_\d]+)", name).groups()
        page_name = page_name.replace(" ", "_")
        return page_name, port_nums

    def set_ideal(self, page_name, port_nums, old_name, new_name, ntwk):
        if old_name == page_name:
            old_name += port_nums
            new_name += port_nums
            if old_name in self.ideal_ntwks:
                self.ideal_ntwks.pop(old_name)
            if old_name in self.measured_ntwks:
                self.measured_ntwks[new_name] = self.measured_ntwks.pop(old_name)
                self.measured_ntwks[new_name].name = new_name
            self.ideal_ntwks[new_name] = ntwk
            self.ideal_ntwks[new_name].name = new_name
        else:
            self.ideal_ntwks[page_name + port_nums] = ntwk
            self.ideal_ntwks[page_name + port_nums].name = page_name + port_nums

    def measure(self, page_name, port_nums, calkit_standard):
        if self.measurement_type == "SS":
            sp_port_indices = list(filter(None, port_nums.split("_")))
            sp_port_indices = [int(ind) for ind in sp_port_indices]
            port_indices = [0] + sp_port_indices
            cal_port = self.device_model().ports[0]
            if len(sp_port_indices) == 1:
                cal_standard = cal_standard_map[calkit_standard.lower()]
                if cal_standard:
                    cal_port.rfztuner.z_set = cal_standard(cal_port.rfztuner)
                    cal_port.rfreceiver.on = True
            for port in self.device_model().ports[1::]:
                port.rfreceiver.on = port.port_num in sp_port_indices

            measure = Measure()
            Settings().datagroup = self.datagroup_name()
            Settings().dataset = page_name + port_nums
            measure.ports = port_indices
            measure.ss_ports = sp_port_indices
            func = measure.single_sparameter_measurement
        elif self.measurement_type == "LS":
            port_indices = [0] + self.port_indices
            port = self.device_model().ports[port_indices[1]]
            cal_port = self.device_model().ports[0]
            cal_port.rfreceiver.on = True
            port.rfreceiver.on = True

            measure = Measure()
            Settings().datagroup = self.datagroup_name()
            Settings().dataset = page_name + port_nums
            measure.ports = port_indices
            func = measure.swept_measurement
        else:
            measure = Measure()
            func = measure.skip_measurement
        return measure, func

    def set_measurement(self, page_name, port_nums, calkit_standard):
        if self.measurement_type == "SS":
            sp_port_indices = list(filter(None, port_nums.split("_")))
            sp_port_indices = [int(ind) for ind in sp_port_indices]
            cal_port = self.device_model().ports[0]
            for port in self.device_model().ports[1::]:
                port.rfreceiver.on = False
            if len(sp_port_indices) == 1:
                cal_standard = cal_standard_map[calkit_standard.lower()]
                if cal_standard:
                    cal_port.rfreceiver.on = False
                    cal_port.rfztuner.z_set = cal_standard_map["load"](cal_port.rfztuner)

            freq = ff.freq()
            freq = skrf.Frequency.from_f(freq, unit="hz")
            freq_slice = self.freq_slice()

            dataset = self.datagroup_model()[self.datagroup_name()].dataset(page_name + port_nums)
            s = dataset.s[:, :, :]
            network = skrf.Network(name=page_name + port_nums, frequency=freq[freq_slice[0]], s=s[freq_slice])
            self.measured_ntwks[page_name + port_nums] = network
        elif self.measurement_type == "LS":
            port_indices = (0,) + tuple(self.port_indices)
            port = self.device_model().ports[port_indices[1]]
            cal_port = self.device_model().ports[0]
            cal_port.rfreceiver.on = False
            port.rfreceiver.on = False
            self.dataset_names[page_name + port_nums] = page_name + port_nums
        else:
            return

    def save_measurement(self, dirname, page_name, port_nums, calkit_standard):
        if self.measurement_type == "SS":
            num_ports = len(list(filter(None, port_nums.split("_"))))
            network = self.measured_ntwks[page_name + port_nums]
            filename = os.sep.join((dirname, "%s%s.s%dp" % (page_name.replace(" ", "_"), port_nums, num_ports)))
            SNP.write_network(network, filename)
        elif self.measurement_type == "LS":
            dataset = self.datagroup_model()[self.datagroup_name()].dataset(page_name + port_nums)
            filename = os.sep.join((dirname, "%s%s.mdf" % (page_name.replace(" ", "_"), port_nums)))
            MDIF.write_dataset(dataset, filename)
        else:
            return

    @abc.abstractmethod
    def calculate(self):
        """Calculates the error model coefficients.
        """
        return True

    @abc.abstractmethod
    def apply_cal(self):
        """Applies the error correction transform.
        """
        pass
