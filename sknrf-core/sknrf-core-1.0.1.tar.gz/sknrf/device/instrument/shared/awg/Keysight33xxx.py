import time

import numpy as np

from sknrf.settings import Settings
from sknrf.utilities.rf import rW2dBm, dBm2rW, dBU2rU


def preset(self):
    self.handles["awg"].timeout = 60.0 * 1000
    timeout = self.handles["awg"].timeout
    self.handles["awg"].write("*CLS")
    self.handles["awg"].write("*RST")
    time.sleep(5)
    self.handles["awg"].query("*OPC?")
    self.handles["awg"].timeout = timeout

    self.handles["awg"].write("OUTPut%d:LOAD %d" % (1, 50))
    self.handles["awg"].write("OUTPut%d:LOAD %d" % (2, 50))

    # Configure ARB
    self.handles["awg"].write("SOURCE1:FUNCtion ARB")  # ARB Mode
    self.handles["awg"].write("SOURCE2:FUNCtion ARB")  # ARB Mode
    self.handles["awg"].write("SOURCE1:FUNCtion:ARBitrary:FILTer NORM")  # NORMAL (27 MHzBW) | STEP (13 MHz BW) | OFF
    self.handles["awg"].write("SOURCE2:FUNCtion:ARBitrary:FILTer NORM")  # NORMAL (27 MHzBW) | STEP (13 MHz BW) | OFF
    self.handles["awg"].write("SOURCE1:FUNCtion:ARB:SRAT %f" % (self._config["resample"]/Settings().t_step,))  # Sample Rate
    self.handles["awg"].write("SOURCE2:FUNCtion:ARB:SRAT %f" % (self._config["resample"]/Settings().t_step,))  # Sample Rate
    self.handles["awg"].write("SOURCE1:DATA:VOLatile:CLEar")  # Clear Memory
    self.handles["awg"].write("SOURCE2:DATA:VOLatile:CLEar")  # Clear Memory
    self.handles["awg"].write("SOURce1:VOLTage:UNIT VPP")
    self.handles["awg"].write("SOURce2:VOLTage:UNIT VPP")
    self.handles["awg"].write("SOURCE1:VOLTage %f" % (1e-3,))
    self.handles["awg"].write("SOURCE2:VOLTage %f" % (1e-3,))
    self.handles["awg"].write("SOURce1:VOLTage:OFFSet %f" % (0.0,))
    self.handles["awg"].write("SOURce2:VOLTage:OFFSet %f" % (0.0,))
    self.handles["awg"].query("*OPC?")

    # Trigger
    is_master = (Settings().trigger_device & self.device_id).value and Settings().trigger_port == self.port
    self.handles["awg"].write(":TRIGger1:SOURce %s" % ("IMM" if is_master else "EXT",))
    self.handles["awg"].write(":TRIGger2:SOURce %s" % ("IMM" if is_master else "EXT",))
    self.handles["awg"].write(":TRIGger1:LEVel %d" % (self._config["trigger_level"],))  # Trigger Level
    self.handles["awg"].write(":TRIGger2:LEVel %d" % (self._config["trigger_level"],))  # Trigger Level
    self.handles["awg"].write(":TRIGger1:SLOPe POSitive")  # Trigger Slope
    self.handles["awg"].write(":TRIGger2:SLOPe POSitive")  # Trigger Slope
    self.handles["awg"].write(":TRIGger1:DELay %.9f" % (self.trigger_delay,))  # Trigger Delay
    self.handles["awg"].write(":TRIGger2:DELay %.9f" % (self.trigger_delay,))  # Trigger Delay
    self.handles["awg"].query("*OPC?")

    # Burst
    num_cycles = str(Settings().signal_rep) if Settings().signal_rep > 0 else "INFinity"
    self.handles["awg"].write("SOURce1:BURSt:MODE TRIGgered")  # Triggered Burst
    self.handles["awg"].write("SOURce2:BURSt:MODE TRIGgered")  # Triggered Burst
    self.handles["awg"].write("SOURce1:BURSt:NCYCles %s" % (num_cycles,))
    self.handles["awg"].write("SOURce2:BURSt:NCYCles %s" % (num_cycles,))
    self.handles["awg"].write("SOURce1:BURSt:STATe ON")  # Burst On
    self.handles["awg"].write("SOURce2:BURSt:STATe ON")  # Burst On
    self.handles["awg"].query("*OPC?")


def arm(self):
    self.handles["awg"].write(":TRIGger1:DELay %.9f" % (self.trigger_delay,))  # Trigger Delay
    self.handles["awg"].write(":TRIGger2:DELay %.9f" % (self.trigger_delay,))  # Trigger Delay
    self.handles["awg"].query("*OPC?")


def trigger(self):
    pass
