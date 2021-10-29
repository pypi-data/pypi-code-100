from .core import soc


#pylint: disable=no-self-use
class SocClockWrapper:
    """Clock of SoC currently connected.
    The clock mode affect the mesh processing speed.
    three modes are possible:
    - Performance (300 MHz)
    - Economy (100 MHz)
    - LowPower (5 MHz)
    """

    @property
    def mode(self):
        return soc.get_clock_mode()

    @mode.setter
    def mode(self, v):
        soc.set_clock_mode(v)


# Add an object that is just a wrapper to have properties to get/set clock
soc.clock = SocClockWrapper()
