from enum import Enum

from sknrf.enums.device import Response
from sknrf.enums.mipi import MIPI_VIO_MODE
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
    B1_ANT1 =   0
    B2_ANT1 =   1
    B25_ANT1 =   2
    B3_ANT1 =   3
    B4_ANT1 =   4
    B34_ANT1 =   5
    B39_ANT1 =   6
    B66_ANT1 =   7
    B7_ANT1 =   8
    B30_ANT1 =   9
    B40_ANT1 = 10
    B41_ANT1 = 11
    B1_ANT2 = 12
    B2_ANT2 = 13
    B25_ANT2 = 14
    B3_ANT2 = 15
    B34_ANT2 = 16
    B39_ANT2 = 17
    B66_ANT2 = 18
    B7_ANT2 = 19
    B30_ANT2 = 20
    B40_ANT2 = 21
    B41_ANT2 = 22
    B1_ISO = 23
    B3_ISO = 24
    B40_ISO = 25


class BroadcomAFEM9090(NoMIPIClient):
    signal_list = []
    transforms_list = []
    display_order = ["on", "usid", "band"]

    def __new__(cls, error_model, num_ports, config_filename="",
                mipi=0, **kwargs):
        self = super(BroadcomAFEM9090, cls).__new__(cls, error_model, num_ports, config_filename="",
                                                    mipi=mipi, **kwargs)
        self._band = RFFE_BAND.B1_ANT1
        return self

    def __init__(self, error_model, num_ports, config_filename="",
                 mipi=0, **kwargs):
        super(BroadcomAFEM9090, self).__init__(error_model, num_ports, config_filename="",
                                               mipi=mipi, **kwargs)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self.initialized = True

    def __info__(self):
        super(BroadcomAFEM9090, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["band"] = Info("band", read=True, write=True, check=False)

    def connect_handles(self):
        super(NoRFFE, self).connect_handles()

    def preset(self):
        super(NoRFFE, self).preset()
        if self._config:
            self.usid = self._config["usid"]

    @property
    def _on(self):
        return self._server.vio_mode.value > 0

    @_on.setter
    def _on(self, on):
        on = MIPI_VIO_MODE.ON if on > 0 else MIPI_VIO_MODE.OFF
        self._server.vio_mode = on

    @property
    def band(self):
        return self._band

    @band.setter
    def band(self, band):
        old_write_mode = self._server.write_mode
        try:
            for write_mode, address, data in self._config["band"][band.name.lower()]:
                self._server.write_mode = write_mode
                self._server.write(self.usid, address, data)
        finally:
            self._server.write_mode = old_write_mode
        self._band = band

