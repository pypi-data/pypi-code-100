import numba
from functools import lru_cache
from PyMPDATA.impl.enumerations import (SIGN_RIGHT, INVALID_HALO_VALUE,
                                        ARG_DATA, OUTER, ARG_FOCUS,
                                        META_AND_DATA_DATA, META_AND_DATA_META)
import numpy as np


@lru_cache()
def _make_scalar(value, at, halo, dr, dz, dtype, jit_flags):
    @numba.njit(**jit_flags)
    def impl(psi, n, sign):
        if sign == SIGN_RIGHT:
            return 0
        z = psi[ARG_FOCUS][OUTER]
        activated = np.sum(psi[ARG_DATA][z:z+1, halo:-halo])
        # assert activated < value
        result = max(0, value - activated)
        return result

    if dtype == complex:
        @numba.njit(**jit_flags)
        def fill_halos_scalar(psi, n, sign):
            return complex(
                impl((psi[META_AND_DATA_META], psi[META_AND_DATA_DATA].real), n, sign),
                impl((psi[META_AND_DATA_META], psi[META_AND_DATA_DATA].imag), n, sign)
            )
    else:
        @numba.njit(**jit_flags)
        def fill_halos_scalar(psi, n, sign):
            return impl(psi, n, sign)
    return fill_halos_scalar

class DropletActivation:
    def __init__(self, value, dr, dz):
        self._value = value / dz / dr
        self.dz = dz
        self.dr = dr

    def make_scalar(self, _at, _halo, dtype, jit_flags):
        return _make_scalar(self._value, _at, _halo, self.dr, self.dz, dtype, jit_flags)
