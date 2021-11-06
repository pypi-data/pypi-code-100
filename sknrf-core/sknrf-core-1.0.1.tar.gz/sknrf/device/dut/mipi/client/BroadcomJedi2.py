from enum import Enum

from sknrf.enums.device import Response
from sknrf.device.dut.mipi.client.base import NoMIPIClient
from sknrf.utilities.numeric import Info
from sknrf.enums.mipi import MIPI_READ_MODE, MIPI_WRITE_MODE

RFFE_READ_OR_MASK = {
    MIPI_READ_MODE.BASIC:          0x60,
    MIPI_READ_MODE.EXTENDED:       0x20,
    MIPI_READ_MODE.EXTENDED_LONG:  0x38,
}

RFFE_WRITE_OR_MASK = {
    MIPI_WRITE_MODE.REG0:          0x80,
    MIPI_WRITE_MODE.BASIC:         0x40,
    MIPI_WRITE_MODE.EXTENDED:      0x00,
    MIPI_WRITE_MODE.EXTENDED_LONG: 0x30,
}

RFFE_READ_AND_MASK = {
    MIPI_READ_MODE.BASIC:          0x9F,
    MIPI_READ_MODE.EXTENDED:       0xDF,
    MIPI_READ_MODE.EXTENDED_LONG:  0xC7,
}

RFFE_WRITE_AND_MASK = {
    MIPI_WRITE_MODE.REG0:          0x7F,
    MIPI_WRITE_MODE.BASIC:         0xBF,
    MIPI_WRITE_MODE.EXTENDED:      0xFF,
    MIPI_WRITE_MODE.EXTENDED_LONG: 0xCF,
}


class RFFE_BAND(Enum):
    B25_LTE_APT_HPM = 0
    B25_LTE_APT_LPM = 1


class BroadcomJedi2(NoMIPIClient):
    signal_list = []
    transforms_list = []
    display_order = ["on", "usid"]

    def __new__(cls, error_model, num_ports, config_filename="",
                mipi=0, **kwargs):
        self = super(BroadcomJedi2, cls).__new__(cls, error_model, num_ports, config_filename="",
                                                 mipi=mipi, **kwargs)
        self._band = RFFE_BAND.B25_LTE_APT_HPM
        self._daq1 = 42.0
        self._daq2 = 47.5
        return self

    def __init__(self, error_model, num_ports, config_filename="",
                 mipi=0, **kwargs):
        super(BroadcomJedi2, self).__init__(error_model, num_ports, config_filename="",
                                            mipi=mipi, **kwargs)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        # DAC1 = 0xA8
        # DAC2 = 0xBE
        # self._mipi.write(self.usid, 0x00, 0x06)
        # self._mipi.write(self.usid, 0x02, 0x04)
        # self._mipi.write(self.usid, 0x03, 0x00)
        # self._mipi.write(self.usid, 0x04, 0x02)
        # self._mipi.write(self.usid, 0x05, 0x10)
        # self._mipi.write(self.usid, 0x06, 0x00)
        # self._mipi.write(self.usid, 0x09, DAC1)
        # self._mipi.write(self.usid, 0x08, DAC2)
        # self._mipi.write(self.usid, 0x0A, 0x03)
        # self._mipi.write(self.usid, 0x1C, 0x03)
        self.initialized = True

    def __info__(self):
        super(BroadcomJedi2, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["band"] = Info("band", read=True, write=True, check=False)

    def connect_handles(self):
        super(NoRFFE, self).connect_handles()

    def preset(self):
        super(NoRFFE, self).preset()
        if self._config:
            self.usid = self._config["usid"]
            self.band = iter(RFFE_BAND).__next__()

    @property
    def band(self):
        return self._band

    @band.setter
    def band(self, band):
        old_write_mode = self._server.write_mode
        try:
            for write_mode, address, data in self._config["band"][band.name]:
                self._server.write_mode = write_mode
                self._server.write(self.usid, address, data)
        finally:
            self.daq1 = self._daq1
            self.daq2 = self._daq2
            self._server.write_mode = old_write_mode
        self._band = band

    @property
    def daq1(self):
        daq1 = self._server.read(self.usid, 0x08)
        return float(daq1/4)

    @daq1.setter
    def daq1(self, daq1):
        self._server.write(self.usid, 0x08, int(daq1 * 4))
        self._daq1 = daq1

    @property
    def daq2(self):
        daq2 = self._server.read(self.usid, 0x09)
        return float(daq2/4)

    @daq2.setter
    def daq2(self, daq2):
        self._server.write(self.usid, 0x09, int(daq2 * 4))
        self._daq2 = daq2

    def arm(self):
        self._server.write(self.usid, 0x1C, 0x03)
