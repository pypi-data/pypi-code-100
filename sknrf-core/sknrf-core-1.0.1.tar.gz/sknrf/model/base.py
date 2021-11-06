import os
import sys
import abc
import logging

from PySide2 import QtCore
from PySide2.QtCore import QObject, QMutex
from tables.exceptions import HDF5ExtError

from sknrf.settings import Settings
from sknrf.utilities.patterns import synchronized
from sknrf.utilities.numeric import AttributeInfo
from sknrf.utilities.patterns import AbstractType

__author__ = 'dtbespal'


def model_logger(logger):
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


class AbstractModel(QObject, metaclass=AbstractType):

    _initialized = False
    _device_model = None
    _datagroup_model = {}
    display_order = []
    lock = QMutex()

    @classmethod
    def init(cls):
        if not cls._initialized:
            from sknrf.device.base import Settings
            from sknrf.model.device import DevicesModel
            from sknrf.app.dataviewer.model import DatagroupModel

            pdmv = (Settings().num_ports, Settings().num_duts, Settings().num_mipi, Settings().num_video)
            cls._device_model = DevicesModel(*pdmv)
            datagroup, dataset = "Single", "Single"
            mode = "w"
            if datagroup in cls._datagroup_model:
                cls._datagroup_model[datagroup].close()
            try:
                cls._datagroup_model[datagroup] = DatagroupModel(mode=mode)
                cls._datagroup_model[datagroup].add(dataset)
            except HDF5ExtError:
                raise FileExistsError("Unable to open the %s datagroup that is already open in %s mode" % (datagroup, mode))
            cls.connect_signals()
            cls._initialized = True

    @classmethod
    def init_test(cls, dg):
        """reintit used by unit tests"""
        from sknrf.device.base import Settings
        from sknrf.model.device import DevicesModel
        from sknrf.app.dataviewer.model import DatagroupModel

        pdmv = (Settings().num_ports, Settings().num_duts, Settings().num_mipi, Settings().num_video)
        dg_dir = os.sep.join((Settings().data_root, "datagroups"))
        dg_filename = os.sep.join((dg_dir, dg + ".h5"))
        if os.path.exists(dg_filename):
            os.remove(dg_filename)
        Settings().datagroup = dg
        AbstractModel.set_device_model(DevicesModel(*pdmv))
        AbstractModel.set_datagroup_model({dg: DatagroupModel(dg_filename, mode="w")})

    @classmethod
    def connect_signals(cls):
        Settings().device_reset_required.connect(cls.init)

    @classmethod
    def disconnect_signals(cls):
        Settings().device_reset_required.connect(cls.init)

    @classmethod
    def __subclasshook__(cls, subclass):
        # Note: Only checks for direct inheritance
        if cls in getattr(subclass, '__mro__', ()):
            return True
        else:
            return False

    @abc.abstractmethod
    def __new__(cls, *args, **kwargs):
        self = super(AbstractModel, cls).__new__(cls)
        self.info = None
        return self

    @abc.abstractmethod
    def __getnewargs__(self):
        return tuple()

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super(AbstractModel, self).__init__()
        self.__key = 0

    @abc.abstractmethod
    def __getstate__(self, state={}):
        """ Saves the model state in a dictionary
        :return state:
        """
        state = self.__dict__.copy()
        for k in reversed(list(state.keys())):
            if isinstance(state[k], QtCore.Signal):
                del state[k]
        return state

    @abc.abstractmethod
    def __setstate__(self, state):
        """ Loads the model state of a saved model object
        :param state:
        :return:
        """
        super(AbstractModel, self).__init__()
        self.info = state["info"]

    @abc.abstractmethod
    def __info__(self):
        """ Initializes the display information of a device and stores information in self.info.
        """
        self.info = AttributeInfo.initialize(self, self.display_order)
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info.pop("display_order", None)
        self.info.pop("info", None)
        self.info.pop("lock", None)
        self.info.pop("staticMetaObject", None)
        self.info.pop("destroyed", None)
        self.info.pop("objectNameChanged", None)

    @classmethod
    @synchronized(None)
    def device_model(cls):
        return cls._device_model

    @classmethod
    @synchronized(None)
    def set_device_model(cls, device_model):
        cls._device_model = device_model

    @classmethod
    @synchronized(None)
    def datagroup_model(cls):
        return cls._datagroup_model

    @classmethod
    @synchronized(None)
    def set_datagroup_model(cls, datagroup_model):
        cls._datagroup_model = datagroup_model

    def moveToThread(self, thread):
        """
        Changes the thread affinity (lifetime) for self and its children.
        """
        super(AbstractModel, self).moveToThread(thread)

    def runInThread(self, thread):
        """
        Changes the thread that is run for self and its children.
        """
        pass
