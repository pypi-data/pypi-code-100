from enum import Enum, IntEnum, unique


class MIPI_VIO_MODE(Enum):
    OFF = 0x00
    ON = 0x01
    EXTERNAL = 0x02
    V1V2 = 0x03
    V1P8 = 0x04


@unique
class MIPI_VOLTAGE(IntEnum):
    V1P2 = 0x0100
    V1P5 = 0x0200
    V1P8 = 0x0300
    V2P0 = 0x0400


@unique
class MIPI_SCLK(IntEnum):
    DRIVE0 = 0x0001
    DRIVE1 = 0x0002
    DRIVE2 = 0x0003
    DRIVE3 = 0x0004


@unique
class MIPI_SDATA(IntEnum):
    DRIVE0 = 0x0010
    DRIVE1 = 0x0020
    DRIVE2 = 0x0030
    DRIVE3 = 0x0040


class MIPI_READ_MODE(Enum):
    GENERIC = 0x00  # auto
    BASIC = 0x01  # 8-bits
    EXTENDED = 0x02  # 32-bits
    EXTENDED_LONG = 0x03  # 128-bits


class MIPI_WRITE_MODE(Enum):
    GENERIC = 0x00  # auto
    REG0 = 0x01  # 1-bits
    BASIC = 0x02  # 1-byte
    EXTENDED = 0x03  # 8-bytes
    EXTENDED_LONG = 0x04  # 16-bytes
    DELAY = 0x05


class MIPI_DATA_LIMIT(IntEnum):
    REG0 =          0x00000000  # 1-bits
    BASIC =         0x0000000F  # 1-bytes
    EXTENDED =      0xFFFFFFFF  # 16-bytes
    EXTENDED_LONG = 0xFFFFFFFF  # 16-bytes


class MIPI_ADDRESS_LIMIT(IntEnum):
    REG0 = 0x0000  # 1-bits
    BASIC = 0x001F  # 5-bits
    EXTENDED = 0x00FF  # 8-bits
    EXTENDED_LONG = 0xFFFF  # 16-bits