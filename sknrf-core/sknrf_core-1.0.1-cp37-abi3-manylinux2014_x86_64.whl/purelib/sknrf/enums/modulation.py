from enum import Enum, IntFlag


class TECH(Enum):
    GSM   = 0x00
    CDMA =  0x01
    WCDMA = 0x02
    LTE   = 0x03


class GSM_BAND(Enum):
    GSM = 0
    EGSM = 1
    PCS = 2
    DCS = 3


class CDMA_BAND(Enum):
    BC0 =  0
    BC1 =  1
    BC2 =  2
    BC3 =  3
    BC4 =  4
    BC5 =  5
    BC6 =  6
    BC7 =  7
    BC8 =  8
    BC9 =  9
    BC10 = 10
    BC11 = 11
    BC12 = 12
    BC13 = 13
    BC14 = 14
    BC15 = 15
    BC16 = 16
    BC17 = 17
    BC18 = 18
    BC19 = 19
    BC20 = 20
    BC21 = 21
    BC22 = 22


class WCDMA_BAND(Enum):
    B0 = 0
    B1 = 1
    B2 = 2
    B3 = 3
    B4 = 4
    B5 = 5
    B6 = 6
    B7 = 7
    B8 = 8
    B9 = 9
    B10 = 10
    B11 = 11
    B12 = 12
    B13 = 13
    B14 = 14
    B15 = 15
    B16 = 16
    B17 = 17
    B18 = 18
    B19 = 19
    B20 = 20
    B21 = 21
    B22 = 22
    B23 = 23
    B24 = 24
    B25 = 25
    B26 = 26
    B27 = 27
    B28 = 28
    B29 = 29
    B30 = 30
    B31 = 31
    B32 = 32
    B33 = 33
    B34 = 34
    B35 = 35
    B36 = 36
    B37 = 37
    B38 = 38
    B39 = 39
    B40 = 40
    B41 = 41
    B42 = 42
    B43 = 43
    B44 = 44
    B45 = 45
    B46 = 46
    B47 = 47
    B48 = 48
    B49 = 49
    B66 = 50
    B67 = 51
    B68 = 52
    B69 = 53
    B70 = 54
    B71 = 55
    B28A = 56
    B28B = 57


class LTE_BAND(Enum):
    B0 =   0
    B1 =   1
    B2 =   2
    B3 =   3
    B4 =   4
    B5 =   5
    B6 =   6
    B7 =   7
    B8 =   8
    B9 =   9
    B10 = 10
    B11 = 11
    B12 = 12
    B13 = 13
    B14 = 14
    B15 = 15
    B16 = 16
    B17 = 17
    B18 = 18
    B19 = 19
    B20 = 20
    B21 = 21
    B22 = 22
    B23 = 23
    B24 = 24
    B25 = 25
    B26 = 26
    B27 = 27
    B28 = 28
    B29 = 29
    B30 = 30
    B31 = 31
    B32 = 32
    B33 = 33
    B34 = 34
    B35 = 35
    B36 = 36
    B37 = 37
    B38 = 38
    B39 = 39
    B40 = 40
    B41 = 41
    B42 = 42
    B43 = 43
    B44 = 44
    B45 = 45
    B46 = 46
    B47 = 47
    B48 = 48
    B49 = 49
    B66 = 50
    B67 = 51
    B68 = 52
    B69 = 53
    B70 = 54
    B71 = 55
    B28A = 56
    B28B = 57


tech2band_map = {
    TECH.GSM: GSM_BAND,
    TECH.CDMA: CDMA_BAND,
    TECH.WCDMA: WCDMA_BAND,
    TECH.LTE: LTE_BAND,
}


class GSM_BW(Enum):
    BW_1p4M = 0x00


class CDMA_BW(Enum):
    BW_1X =   0x00
    BW_3X =   0x01
    BW_5X =   0x02
    BW_7X =   0x03


class WCDMA_BW(Enum):
    BW_SC =   0x00
    BW_DC =   0x01


class LTE_BW(Enum):
    BW_1p4M = 0x00
    BW_3M =   0x01
    BW_5M =   0x02
    BW_10M =  0x03
    BW_15M =  0x04
    BW_20M =  0x05
    BW_30M =  0x07
    BW_35M =  0x08
    BW_40M =  0x09
    BW_45M =  0x0A
    BW_50M =  0x0B
    BW_55M =  0x0C
    BW_60M =  0x0D


tech2bw_map = {
    TECH.GSM: GSM_BW,
    TECH.CDMA: CDMA_BW,
    TECH.WCDMA: WCDMA_BW,
    TECH.LTE: LTE_BW,
}


bw2value_map = {
    GSM_BW.BW_1p4M: 1.4e6,
    CDMA_BW.BW_1X: 1.0e6,
    CDMA_BW.BW_3X: 3.0e3,
    CDMA_BW.BW_5X: 5.0e3,
    CDMA_BW.BW_7X: 7.0e3,
    WCDMA_BW.BW_SC: 5.0e6,
    WCDMA_BW.BW_DC: 5.0e6,
    LTE_BW.BW_1p4M: 1.4e6,
    LTE_BW.BW_3M: 3.0e6,
    LTE_BW.BW_5M: 5.0e6,
    LTE_BW.BW_10M: 10.0e6,
    LTE_BW.BW_15M: 15.0e6,
    LTE_BW.BW_20M: 20.0e6,
    LTE_BW.BW_30M: 30.0e6,
    LTE_BW.BW_35M: 35.0e6,
    LTE_BW.BW_40M: 40.0e6,
    LTE_BW.BW_45M: 45.0e6,
    LTE_BW.BW_50M: 50.0e6,
    LTE_BW.BW_55M: 55.0e6,
    LTE_BW.BW_60M: 60.0e6
}


class GSM_RB(Enum):
    NONE = 0x00


class CDMA_RB(Enum):
    NONE = 0x00


class WCDMA_RB(Enum):
    NONE = 0x00


class LTE_RB(Enum):
    RB_7 =   0x00
    RB_17 =  0x01
    RB_23 =  0x02
    RB_28 =  0x03
    RB_33 =  0x04
    RB_65 =  0x05
    RB_82 =  0x06
    RB_101 = 0x07
    RB_131 = 0x08
    RB_201 = 0x09
    RB_231 = 0x0A
    RB_301 = 0x0B


tech2rb_map = {
    TECH.GSM: GSM_RB,
    TECH.CDMA: CDMA_RB,
    TECH.WCDMA: WCDMA_RB,
    TECH.LTE: LTE_RB,
}

rb2bw_map = {
    LTE_RB.RB_7:  LTE_BW.BW_3M,
    LTE_RB.RB_17: LTE_BW.BW_5M,
    LTE_RB.RB_23: LTE_BW.BW_5M,
    LTE_RB.RB_28: LTE_BW.BW_10M,
    LTE_RB.RB_33: LTE_BW.BW_10M,
    LTE_RB.RB_65: LTE_BW.BW_15M,
    LTE_RB.RB_82: LTE_BW.BW_20M,
    LTE_RB.RB_101: LTE_BW.BW_40M,
    LTE_RB.RB_131: LTE_BW.BW_40M,
    LTE_RB.RB_201: LTE_BW.BW_40M,
    LTE_RB.RB_231: LTE_BW.BW_40M,
    LTE_RB.RB_301: LTE_BW.BW_60M,
}


class GAIN(Enum):
    G0 = 0x00
    G1 = 0x01


class ET(Enum):
    APT = 0x02
    ET = 0x03


class POWER_CLASS(Enum):
    GENERAL = 0
    CLASS1 = 1
    CLASS2 = 2


class CA(Enum):
    NONE =                 0
    INTRA_CONTIGUOUS =     1
    INTRA_NON_CONTIGUOUS = 2
    INTER =                3


class DF_OOB(IntFlag):
    UTRA1      = 0x01
    UTRA2      = 0x02
    E_UTRA1    = 0x04
    L          = 0x10
    U          = 0x20
    UTRA       = UTRA1 | UTRA2 | L | U
    E_UTRA     = E_UTRA1 | L | U
    ALL        = UTRA | E_UTRA


class MOD(Enum):
    BPSK = 0
    QPSK = 1
    QAM16 = 2
    QAM64 = 3
    QAM256 = 4
