from enum import Enum
from enum import IntEnum
from itertools import chain

from sknrf.device.dut.mipi.client.base import MIPI_REG
from sknrf.enums.mipi import MIPI_READ_MODE, MIPI_WRITE_MODE

ET_READ_OR_MASK = {
    MIPI_READ_MODE.BASIC:          0x60,
    MIPI_READ_MODE.EXTENDED:       0x20,
    MIPI_READ_MODE.EXTENDED_LONG:  0x38,
}


ET_WRITE_OR_MASK = {
    MIPI_WRITE_MODE.REG0:          0x80,
    MIPI_WRITE_MODE.BASIC:         0x40,
    MIPI_WRITE_MODE.EXTENDED:      0x00,
    MIPI_WRITE_MODE.EXTENDED_LONG: 0x30,
}


ET_READ_AND_MASK = {
    MIPI_READ_MODE.BASIC:          0x9F,
    MIPI_READ_MODE.EXTENDED:       0xDF,
    MIPI_READ_MODE.EXTENDED_LONG:  0xC7,
}


ET_WRITE_AND_MASK = {
    MIPI_WRITE_MODE.REG0:          0x7F,
    MIPI_WRITE_MODE.BASIC:         0xBF,
    MIPI_WRITE_MODE.EXTENDED:      0xFF,
    MIPI_WRITE_MODE.EXTENDED_LONG: 0xCF,
}


class _ET_REG(IntEnum):
    MODE_CTRL =     0x0001
    APT_VREG_VMAX = 0x0002  # APT voltage in APT mode, Vmax in ET mode. 30 mV LSB; 0 V = 0x00
    BANDWIDTH =     0x0003  # RB number. Bit<7> contains RSSI information. (Signal Bandwidth)
    ET_VMIN =       0x0004  # Vmin in ET mode and RSSI level. Bits<5:0> are used for Vmin with 30 mV LSB with offset of 690 mV (690 mV = 0x00); bit<7> indicates 256QAM (1 = 256QAM, 0 = lower 256QAM)
    BW      =       0x0005  # Chanel Bandwidth
    ALARM_LATCH =   0x1059  # Latched: 0=No Alarm, 5=Temp, 6=SIDO 7=Switch
    AG_VERSION =    0x1167  # Autogen version


ET_REG = IntEnum('ET_REG', [(i.name, i.value) for i in chain(MIPI_REG, _ET_REG)])


class ET_MOD_MODE(Enum):
    SLEEP =   0x00  # All circuits disabled, all outputs tri-stated.
    STANDBY = 0x01  # Support circuits and all switches enabled. Vbatt connected directly to PA.
    APT =     0x02  # ET and boost blocks disabled. Output on Vout_ET port for 3G, APT port for 2G
    ET =      0x03  # APT/ET with/without boost circuit enabled. Output on Vout_ET port