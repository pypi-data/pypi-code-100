from enum import Enum, Flag, auto, unique

import numpy as np
import torch as th

from sknrf.widget.propertybrowser.view import Format, Scale


@unique
class RuntimeState(Enum):
    RUN = 0
    SINGLE = 1
    PAUSED = 2
    STOPPED = 3


class Bound(Flag):
    OFF = 0  # No checks
    OUT = auto()  # Functionals optionally define output bound checking
    IN = auto()  # Functionals optionally define input bound checking
    SET = auto()  # Tensor defines bound checking during Tensor.__setitem__
    GET = auto()  # Tensor defines bound checking during Tensor.__getitem__
    LEVEL1 = OUT
    LEVEL2 = LEVEL1 | IN
    LEVEL3 = LEVEL2 | SET
    LEVEL4 = LEVEL3 | GET


class SI (Enum):
    F = auto()
    T = auto()
    V = auto()
    I = auto()
    Z = auto()
    B = auto()
    A = auto()
    G = auto()
    TEMP = auto()


si_dtype_map = {
    SI.F: th.double,
    SI.T: th.double,
    SI.V: th.complex128,
    SI.I: th.complex128,
    SI.Z: th.complex128,
    SI.B: th.complex128,
    SI.A: th.complex128,
    SI.G: th.complex128,
    SI.TEMP: th.float,
}


si_eps_map = {
    SI.F:    1,
    SI.T:    th.finfo(si_dtype_map[SI.T]).eps*2**3,
    SI.V:    np.conj(50.0)/np.sqrt(np.real(50.0))*th.finfo(si_dtype_map[SI.A]).eps*2**3,  # a2v()
    SI.I:    th.finfo(si_dtype_map[SI.I]).eps*2**3,
    SI.Z:    th.finfo(si_dtype_map[SI.Z]).eps*2**3,
    SI.B:    th.finfo(si_dtype_map[SI.I]).eps*2**3,
    SI.A:    th.finfo(si_dtype_map[SI.A]).eps*2**3,
    SI.G:    th.finfo(si_dtype_map[SI.G]).eps*2**3,
    SI.TEMP: th.finfo(si_dtype_map[SI.TEMP]).eps*2**3,
}


si_format_map = {
    SI.F:    Format.RE,
    SI.T:    Format.RE,
    SI.V:    Format.RE_IM,
    SI.I:    Format.RE_IM,
    SI.Z:    Format.RE_IM,
    SI.B:    Format.LOG_DEG,
    SI.A:    Format.LOG_DEG,
    SI.G:    Format.LIN_DEG,
    SI.TEMP: Format.RE,
}


si_scale_map = {
    SI.F:    Scale.G,
    SI.T:    Scale.m,
    SI.V:    Scale._,
    SI.I:    Scale._,
    SI.Z:    Scale._,
    SI.B:    Scale.m,
    SI.A:    Scale.m,
    SI.G:    Scale._,
    SI.TEMP: Scale._,
}


si_unit_map = {
    SI.F:    "Hz",
    SI.T:    "s",
    SI.V:    "V",
    SI.I:    "A",
    SI.Z:    "ohm",
    SI.B:    "rW",
    SI.A:    "rW",
    SI.G:    "U",
    SI.TEMP: "K",
}



