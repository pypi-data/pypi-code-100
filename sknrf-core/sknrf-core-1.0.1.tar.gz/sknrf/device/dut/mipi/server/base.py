from sknrf.device import AbstractDevice
from sknrf.enums.device import Response
from sknrf.settings import Settings, DeviceFlag
from sknrf.enums.mipi import MIPI_VIO_MODE, MIPI_READ_MODE, MIPI_WRITE_MODE, MIPI_DATA_LIMIT, MIPI_ADDRESS_LIMIT
from sknrf.utilities.numeric import Info, Scale, Format


class NoMIPIServer(AbstractDevice):

    device_id = DeviceFlag.MIPI_SERVER
    signal_list = []
    transforms_list = []
    display_order = ["on"]

    def __new__(cls, error_model, dut, config_filename="", **kwargs):
        self = super(NoMIPIServer, cls).__new__(cls, error_model, dut, config_filename, **kwargs)
        self._clk_rate = 0.0
        self._vio_mode = MIPI_VIO_MODE.OFF
        self._read_mode = MIPI_READ_MODE.GENERIC
        self._write_mode = MIPI_WRITE_MODE.GENERIC
        return self

    def __getnewargs__(self):
        newargs = list(super(NoMIPIServer, self).__getnewargs__())
        newargs[0] = None
        return tuple(newargs)

    def __init__(self, error_model, dut, config_filename="", **kwargs):
        super(NoMIPIServer, self).__init__(error_model, dut, config_filename, **kwargs)
        if self.__class__ == NoMIPIServer:
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoMIPIServer, self).__getstate__(state=state)
        state["clk_rate"] = self.clk_rate
        state["vio_mode"] = self.vio_mode
        state["read_mode"] = self.read_mode
        state["write_mode"] = self.write_mode
        return state

    def __setstate__(self, state):
        super(NoMIPIServer, self).__setstate__(state)
        if self.__class__ == NoMIPIServer:
            self.connect_handles()
            self.preset()

            # Initialize object PROPERTIES
            self.clk_rate = state["clk_rate"]
            self.vio_mode = state["vio_mode"]
            self.read_mode = state["read_mode"]
            self.write_mode = state["write_mode"]
            self.initialized = True

    def __info__(self):
        super(NoMIPIServer, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["freq"] = Info("freq", read=False, write=False, check=False)
        self.info["clk_rate"] = Info("CLK rate", read=True, write=True, check=True,
                                     format_=Format.RE, scale=Scale.M, unit="Hz", min_=0)
        self.info["vio_mode"] = Info("VIO mode", read=True, write=True, check=True,
                                     format_=Format.RE, min_=0, max_=2)
        self.info["read_mode"] = Info("read mode", read=True, write=True, check=True,
                                      format_=Format.RE)
        self.info["write_mode"] = Info("write mode", read=True, write=True, check=True,
                                       format_=Format.RE)

    def connect_handles(self):
        super(NoMIPIServer, self).connect_handles()

    def preset(self):
        super(NoMIPIServer, self).preset()
        if self.__class__ == NoMIPIServer:
            pass

    @property
    def dut(self):
        return self.port

    @property
    def vio_mode(self):
        return self._vio_mode

    @vio_mode.setter
    def vio_mode(self, mode):
        self._vio_mode = mode

    @property
    def clk_rate(self):
        return self._clk_rate

    @clk_rate.setter
    def clk_rate(self, rate):
        self._clk_rate = rate

    @property
    def read_mode(self):
        return self._read_mode

    @read_mode.setter
    def read_mode(self, mode):
        self._read_mode = mode

    @property
    def write_mode(self):
        return self._write_mode

    @write_mode.setter
    def write_mode(self, mode):
        self._write_mode = mode

    def read(self, usid, address):
        if self._read_mode == MIPI_READ_MODE.BASIC:
            values = self._read_basic(usid, address)
        elif self._read_mode == MIPI_READ_MODE.EXTENDED:
            values = self._read_extended(usid, address)
        elif self._read_mode == MIPI_READ_MODE.EXTENDED_LONG:
            values = self._read_extended_long(usid, address)
        else:
            values = self._read_generic(usid, address)
        return values

    def write(self, usid, address, data):
        if self._write_mode == MIPI_WRITE_MODE.REG0:
            self._write_register0(usid, address, data)
        elif self._write_mode == MIPI_WRITE_MODE.BASIC:
            self._write_basic(usid, address, data)
        elif self._write_mode == MIPI_WRITE_MODE.EXTENDED:
            self._write_extended(usid, address, data)
        elif self._write_mode == MIPI_WRITE_MODE.EXTENDED_LONG:
            self._write_extended_long(usid, address, data)
        else:
            self._write_generic(usid, address, data)

    def _read_basic(self, usid, address):
        raise NotImplementedError("MIPI device does not support basic read")

    def _read_extended(self, usid, address):
        raise NotImplementedError("MIPI device does not support extended read")

    def _read_extended_long(self, usid, address):
        raise NotImplementedError("MIPI device does not support extended long read")

    def _read_generic(self, usid, address):
        if address <= MIPI_ADDRESS_LIMIT.BASIC:
            return self._read_basic(usid, address)
        elif address <= MIPI_ADDRESS_LIMIT.EXTENDED:
            return self._read_extended(usid, address)
        elif address <= MIPI_ADDRESS_LIMIT.EXTENDED_LONG:
            return self._read_extended_long(usid, address)
        else:
            raise ValueError("MIPI address exceeds the maximum readable address")

    def _write_register0(self, usid, address, data):
        raise NotImplementedError("MIPI device does not support register 0 write")

    def _write_basic(self, usid, address, data):
        raise NotImplementedError("MIPI device does not support basic write")

    def _write_extended(self, usid, address, data):
        raise NotImplementedError("MIPI device does not support extended write")

    def _write_extended_long(self, usid, address, data):
        raise NotImplementedError("MIPI device does not support extended long write")

    def _write_generic(self, usid, address, data):
        if address <= MIPI_ADDRESS_LIMIT.BASIC and data <= MIPI_DATA_LIMIT.BASIC:
            self._write_basic(usid, address, data)
        elif address <= MIPI_ADDRESS_LIMIT.EXTENDED and data <= MIPI_DATA_LIMIT.EXTENDED:
            self._write_extended(usid, address, data)
        elif address <= MIPI_ADDRESS_LIMIT.EXTENDED_LONG and data <= MIPI_DATA_LIMIT.EXTENDED_LONG:
            self._write_extended_long(usid, address, data)
        else:
            raise ValueError("MIPI address exceeds the maximum writeable address")

