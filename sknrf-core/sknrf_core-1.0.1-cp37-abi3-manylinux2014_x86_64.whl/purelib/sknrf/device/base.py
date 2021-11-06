import abc
import sys
import logging
import os
import pickle

import matplotlib.pyplot as plt
import torch as th
import yaml
from scipy import interpolate

from sknrf.settings import Settings, DeviceFlag
from sknrf.utilities.numeric import AttributeInfo, Info, Scale, Format
from sknrf.utilities.os.path import realpath
from sknrf.model.base import AbstractModel

__author__ = 'dtbespal'
logger = logging.getLogger(__name__)


def device_logger(logger):
    log_level = logging.DEBUG if Settings().debug else logging.INFO

    if len(logger.handlers) == 0:
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        stream_handler.setLevel(log_level)
        logger.addHandler(stream_handler)

    if len(logger.handlers) == 1:
        filename = os.sep.join((Settings().root, "log.txt"))
        file_handler = logging.FileHandler(filename, mode="w")
        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)
    return logger


plt.style.use('ggplot')
th.set_default_tensor_type(th.DoubleTensor)

class AbstractDevice(object, metaclass=abc.ABCMeta):
    """ Abstract Device driver.

        Base class for all device types including:

            * Instruments:
                * LFSource.
                * LFReceiver.
                * LFZTuner.
                * RFSource.
                * RFReceiver.
                * RFZTuner.
            * Calkits.
            * DUTs

        Attributes:
            firmware_map (dict): Dictionary describing the supported firmware versions for each physical device.
            signal_list (list): List of property names that contain signal type data.
            transforms_list (list): List of signal transforms supported by the device driver.
            display_order (list): Preferred display order of device properties.

        Example:
            The device drive attributes could be defined as follows:

            >>> firmware_map = {"device_handle_name_1": "1.3.x", "device_handle_name_2": "2.5.3"}
            >>> signal_list = ["v"]
            >>> transforms_list = ["Envelope", "Time", "Time Envelope", "Frequency", "Spectrum", "Power"]
            >>> display_order = ["initialized", "freq", "v", "num_harmonics", "harmonics"]

    """
    device_id = DeviceFlag.NONE
    firmware_map = {}
    signal_list = []
    transforms_list = []
    display_order = []

    @abc.abstractmethod
    def __new__(cls, devices_model, port, config_filename="", **kwargs):
        """ Creates New Instance of the Device.

        Args:
            device_model (DevicesModel): Contains error correction functions.
            port (int): Port number.

        Returns:
            (Device): A new device object.
        """
        self = super(AbstractDevice, cls).__new__(cls)
        self.initialized = False
        self.port = port
        data_root = Settings().data_root
        device_dir = os.sep.join(self.__module__.split(".")[1:-1:])
        device_path = os.sep.join(self.__module__.split(".")[1::])
        if len(config_filename) == 0:
            config_filename = os.sep.join((data_root, "config", device_path))
        elif len(os.path.dirname(config_filename)) == 0:
            config_filename, _ = os.path.splitext(config_filename)
            config_filename = os.sep.join((data_root, "config", device_dir, config_filename))
        else:
            config_filename, _ = os.path.splitext(config_filename)
        try:
            f = open(realpath(config_filename + ".pkl"), "rb")
        except FileNotFoundError:
            with open(realpath(config_filename + ".yml"), "rt") as f:
                self._config = yaml.load(f, yaml.Loader)
                self.config_filename = config_filename + ".yml"
        else:
            self._config = pickle.load(f)
            self.config_filename = config_filename + ".pkl"

        self.handles = {}
        self._on_ = False
        self._trigger_delay = 0.0
        self._delay_ = 0.0
        self._pulse_width_ = self.period
        self.info = None
        return self

    def __getnewargs__(self):
        return None, self.port, self.config_filename

    def __init__(self, devices_model, port, config_filename="", **kwargs):
        """" Connects and Initializes the state of the Device.

        Args:
            devices_model (DevicesModel): Contains error correction functions.
            port (int): Port number.
        """
        super(AbstractDevice, self).__init__()
        data_root = Settings().data_root
        device_dir = os.sep.join(self.__module__.split(".")[1:-1:])
        device_path = os.sep.join(self.__module__.split(".")[1::])
        if len(config_filename) == 0:
            config_filename = os.sep.join((data_root, "config", device_path))
        elif len(os.path.dirname(config_filename)) == 0:
            config_filename, _ = os.path.splitext(config_filename)
            config_filename = os.sep.join((data_root, "config", device_dir, config_filename))
        elif len(os.path.dirname(config_filename)) == 0:
            config_filename, _ = os.path.splitext(config_filename)
            config_filename = os.sep.join((data_root, "config", device_path, config_filename))
        else:
            config_filename, _ = os.path.splitext(config_filename)
        try:
            f = open(realpath(config_filename + ".pkl"), "rb")
        except FileNotFoundError:
            with open(realpath(config_filename + ".yml"), "rt") as f:
                self._config = yaml.load(f, yaml.Loader)
                self.config_filename = config_filename + ".yml"
        else:
            self._config = pickle.load(f)
            f.close()
            self.config_filename = config_filename + ".pkl"
        devices_model.register_device(self, new=True)

    def __getstate__(self, state={}):
        """ Saves the device state in a dictionary.

            Returns:
                dict: saved state.
        """
        state = self.__dict__.copy()
        del state["info"]
        del state["handles"]
        del state["initialized"]
        return state

    def __setstate__(self, state):
        """ Loads the device state of a saved instrument object.

            Args:
                state (dict): saved state.
        """
        self.initialized = False
        self.__dict__.update(state)

    def __info__(self):
        """ Initializes the display information of a device and stores information in self.info.
        """
        self.info = AttributeInfo.initialize(self, self.display_order)
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["handles"].read = False
        self.info["signal_list"].read = False
        self.info["transforms_list"].read = False
        self.info["display_order"].read = False
        self.info["info"].read = False
        self.info["handles"].read = False
        self.info["harmonics"].read = False
        self.info["time_c"].read = False
        self.info["time"].read = False
        self.info["freq_m"].read = False
        self.info["initialized"] = Info("initialized", read=False, write=False, check=False)
        self.info["port"] = Info("port", read=False, write=False, check=False)
        self.info["config_filename"] = Info("config_filename", read=False, write=True, check=False)
        self.info["trigger_delay"] = Info("trigger_delay", read=True, write=True, check=False,
                                          format_=Format.RE, scale=Scale.n, unit="s",
                                          min_=self._config["trigger_delay_min"], max_=self._config["trigger_delay_max"])
        self.info["freq"] = Info("freq", read=False, write=False, check=False, format_=Format.RE, scale=Scale.G, unit="Hz")
        self.info["config_filename"] = Info("config_filename", read=False, write=True, check=False)
        self.info["f0"] = Info("f0", read=True, write=False, check=False)

        self.info["num_harmonics"] = Info("num harmonics", read=True, write=False, check=False)

    @abc.abstractmethod
    def connect_handles(self):
        """ Connect to the devices handles and store references in the handles dictionary.
        """
        for handle in self.handles.values():
            self._devices_model._add_handle_ref(handle)

    @abc.abstractmethod
    def preset(self):
        """ Preset device handles that have have unique connections.
        """
        pass

    def unique_handle(self, handle):
        """ Determines if the device handle is a unique connection.

            Args:
                handle_name (str): device key in the handles dictionary,

            Returns:
                bool: True if the cooresponding device handle is a device unique connection.
        """
        return self._devices_model._handle_ref_count(handle) == 1

    def disconnect_handles(self):
        if not self.handles:
            return
        for k in reversed(list(self.handles.keys())):
            self._devices_model._remove_handle_ref(self.handles.pop(k))

    @property
    def _devices_model(self):
        return AbstractModel.device_model()

    @property
    def _error_model(self):
        return self._devices_model.error_model

    @property
    def on(self):
        return self._on

    @on.setter
    def on(self, on):
        """ bool: On/Off switch.
        """
        self._on = on

    @property
    def _on(self):
        return self._on_

    @_on.setter
    def _on(self, _on):
        self._on_ = _on

    @property
    def f0(self):
        return Settings().f0

    @property
    def freq(self):
        """ ndarray: The subsection of Settings.freq available to the device driver.
        """
        return Settings().freq

    @property
    def time_c(self):
        """ ndarray: The subsection of Settings.time_c available to the device driver.
        """
        return Settings().time_c

    @property
    def num_harmonics(self):
        """ int: The total number of harmonics available to the device driver.
        """
        return Settings().num_harmonics

    @property
    def harmonics(self):
        """ ndarray: The actual harmonic indicies that are controlled by the device driver.
        """
        return Settings().harmonics

    @property
    def time(self):
        """ ndarray: The subsection of Settings.time available to the device driver.
        """
        return Settings().time

    @property
    def freq_m(self):
        """ ndarray: The subsection of Settings.freq_m available to the device driver.
        """
        return Settings().freq_m

    @staticmethod
    def time_interp(t_value):
        """ Interpolates the user provided t_value to the nearest point in the time sweep.

        Args:
            t_value: user provided time.

        Return:
            float: interpolated t_value in the time sweep.
        """
        t_value = max(min(t_value, Settings().time[-1, 0]), Settings().time[0, 0])
        t_system = Settings().time.flatten()
        nearest_time = interpolate.interp1d(t_system, t_system, kind="nearest", assume_sorted=True)
        return nearest_time(t_value)

    @property
    def period(self):
        """ float: Pulse Modulation period time.
        """
        return Settings().t_stop

    @period.setter
    def period(self, period):
        pass

    def arm(self):
        """ Arm Trigger and Pepare for measurement
        """

    @property
    def trigger_delay(self):
        return self._trigger_delay + self._config["trigger_delay"]

    @trigger_delay.setter
    def trigger_delay(self, trigger_delay):
        self._trigger_delay = trigger_delay - self._config["trigger_delay"]

    def trigger(self):
        """ Trigger for measurement synchronization.
        """
        pass

    def measure(self):
        """ Record measurement data.
        """
        pass
