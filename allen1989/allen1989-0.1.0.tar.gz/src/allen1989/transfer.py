"""
Formalisms related to heat transfers.
"""
import math

from . import raw


def heat_conductance(hc, ws):
    """Resistance to heat transfer between canopy and atmosphere.

    Weather station is supposed to be at 2m height.

    References: eq3, 4, 5 and 6

    Args:
        hc (float): [m] canopy height
        ws (float): [m.s-1] wind speed at 2m high

    Returns:
        (float): [m.s-1] heat conductance
    """
    zm = zh = 2  # [m] weather station altitude
    zom = raw.eq4(hc)
    zoh = raw.eq5(hc)
    d = raw.eq6(hc)

    # don't use eq3 in the end to avoid numerical instabilities when ws=0
    # ra = raw.eq3(zm, zh, d, zom, zoh, ws)

    return raw.von_karman ** 2 * ws / (math.log((zm - d) / zom) * math.log((zh - d) / zoh))
