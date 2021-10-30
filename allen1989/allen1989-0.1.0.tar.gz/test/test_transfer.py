import pytest

from allen1989 import raw
from allen1989.transfer import heat_conductance


def test_heat_conductance_corresponds_to_raw():
    hc = 1.5  # [m]
    zm = zh = 2  # [m] weather station altitude
    zom = raw.eq4(hc)
    zoh = raw.eq5(hc)
    d = raw.eq6(hc)

    for ws in (0.3, 1, 2, 10):  # [m.s-1]
        ra = raw.eq3(zm, zh, d, zom, zoh, ws)
        assert pytest.approx(heat_conductance(hc, ws), ra, abs=1e-15)
