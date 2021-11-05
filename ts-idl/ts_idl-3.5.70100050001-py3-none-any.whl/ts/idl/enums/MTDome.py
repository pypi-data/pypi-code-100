# This file is part of ts_idl.
#
# Developed for Vera Rubin Observatory.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License

__all__ = ["EnabledState", "Louver", "MotionState", "OperationalMode", "SubSystemId"]

import enum


class EnabledState(enum.IntEnum):
    """Drive enabled state."""

    DISABLED = 1
    ENABLED = 2
    FAULT = 3


class Louver(enum.IntEnum):
    """Louver name and associated array index."""

    A1 = 0
    A2 = 1
    B1 = 2
    B2 = 3
    B3 = 4
    C1 = 5
    C2 = 6
    C3 = 7
    D1 = 8
    D2 = 9
    D3 = 10
    E1 = 11
    E2 = 12
    E3 = 13
    F1 = 14
    F2 = 15
    F3 = 16
    G1 = 17
    G2 = 18
    G3 = 19
    H1 = 20
    H2 = 21
    H3 = 22
    I1 = 23
    I2 = 24
    I3 = 25
    L1 = 26
    L2 = 27
    L3 = 28
    M1 = 29
    M2 = 30
    M3 = 31
    N1 = 32
    N2 = 33


class MotionState(enum.IntEnum):
    """Motion state."""

    ERROR = 0
    CLOSED = 1
    CRAWLING = 2
    MOVING = 3
    OPEN = 4
    PARKED = 5
    PARKING = 6
    STOPPED = 7
    STOPPING = 8
    STOPPING_BRAKING = 9
    STOPPED_BRAKED = 10


class OperationalMode(enum.IntEnum):
    """Operational Modes."""

    NORMAL = 1
    DEGRADED = 2


class SubSystemId(enum.IntEnum):
    """SubSystem ID bitmask."""

    # Azimuth Motion Control System
    AMCS = 0x1
    # Light and Wind Screen Control System
    LWSCS = 0x2
    # APerture Shutter Control System
    APSCS = 0x4
    # Louvers Control System
    LCS = 0x8
    # THermal Control System
    THCS = 0x10
    # MONitoring Control System
    MONCS = 0x20
