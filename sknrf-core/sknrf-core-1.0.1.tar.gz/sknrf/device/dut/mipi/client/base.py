from enum import Enum, IntEnum, unique

from sknrf.settings import DeviceFlag
from sknrf.device.base import AbstractDevice
from sknrf.enums.mipi import MIPI_VIO_MODE
from sknrf.utilities.numeric import AttributeInfo, Info, Scale, PkAvg, Format


@unique
class MIPI_REG(IntEnum):
    PM_TRIG =     0x1C
    PROD_ID =     0x1D  # Product ID (prod_id in  config file)
    MAN_ID1 =     0x1E
    MAN_ID2 =     0x1F
    EXT_PROD_ID = 0x20
    REV_ID      = 0x21  # Revision ID (rev_id config file)


class MIPI_TYPE(Enum):
    RFFE   =  0x00
    ET     =  0x01
    SWITCH = 0x02


class NoMIPIClient(AbstractDevice):

    device_id = DeviceFlag.MIPI_CLIENT
    firmware_map = {}
    signal_list = []
    transforms_list = []
    display_order = ["on", "usid"]

    def __new__(cls, error_model, dut, config_filename="",
                index=0, **kwargs):
        self = super(NoMIPIClient, cls).__new__(cls, error_model, dut, config_filename="", **kwargs)
        self.usid = 0
        self.index = index
        return self

    def __getnewargs__(self):
        args = super(NoMIPIClient, self).__getnewargs__()
        args += (self.index,)
        return args

    def __init__(self, error_model, dut, config_filename="",
                 index=0, **kwargs):
        super(NoMIPIClient, self).__init__(error_model, dut, config_filename="", **kwargs)
        self.usid = self._config["usid"]
        if self.__class__ == NoMIPIClient:
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoMIPIClient, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(NoMIPIClient, self).__setstate__(state)
        if self.__class__ == NoMIPIClient:
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self.initialized = True

    def __info__(self):
        self.info = AttributeInfo.initialize(self, self.display_order)
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["f0"].read = False
        self.info["num_harmonics"].read = False
        self.info["harmonics"].read = False
        self.info["freq"].read = False
        self.info["time_c"].read = False
        self.info["time"].read = False
        self.info["period"].read = False
        self.info["freq_m"].read = False
        self.info["usid"] = Info("USID", read=True, write=True, check=True,
                                 format_=Format.RE, scale=Scale._, min_=0, max_=15)
        self.info["initialized"] = Info("initialized", read=False, write=False, check=False)
        self.info["config_filename"] = Info("config_filename", read=True, write=True, check=False)

    def connect_handles(self):
        pass

    def disconnect_handles(self):
        pass

    def preset(self):
        if self.__class__ == NoMIPIClient:
            pass

    @property
    def dut(self):
        return self.port

    @property
    def on(self):
        return self._server.vio_mode.value > 0

    @on.setter
    def on(self, on):
        on = MIPI_VIO_MODE.ON if on > 0 else MIPI_VIO_MODE.OFF
        self._server.vio_mode = on

    @property
    def _server(self):
        return self._error_model.duts[0].mipi_server

    def arm(self):
        pass

    def trigger(self):
        pass

    def measure(self):
        pass
