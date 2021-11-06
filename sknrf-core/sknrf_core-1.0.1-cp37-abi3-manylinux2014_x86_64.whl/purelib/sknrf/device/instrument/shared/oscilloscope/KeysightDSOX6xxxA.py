import time

import numpy as np

from sknrf.settings import Settings


def preset(self):
    self.handles["scope"].write("*CLS")
    self.handles["scope"].write("*RST")
    self.handles["scope"].query("*OPC?")

    #  Aquire
    self.handles["scope"].write(":ACQuire:TYPE NORMal")  # Normal Aquisition
    self.handles["scope"].write(":ACQuire:COUNT 1")  # Normal Aquisition
    self.handles["scope"].query("*OPC?")

    #  Waveform
    points = np.asarray(self._config["points"], dtype=np.int)
    waveform_points = points[points/Settings().t_points > int(self._config["resample"])][0]  # Up-sample on instrument
    self.handles["scope"].write(":WAVeform:POINts:MODE RAW")  # Set the waveform points mode.
    self.handles["scope"].write(":WAVeform:POINts %d" % (waveform_points,))  # Set the waveform points
    self.handles["scope"].write(":WAVeform:FORMat WORD")  # 16-Bit precision
    self.handles["scope"].write(":WAVeform:BYTeorder MSBFirst")  # MSB first
    self.handles["scope"].query("*OPC?")

    # Time
    self.handles["scope"].write(":TIMebase:MODE MAIN")
    t_stop = 1.1*Settings().t_stop
    self.handles["scope"].write(":TIMebase:RANGe %f" % (t_stop,))
    while float(self.handles["scope"].query(":TIMebase:RANGe?")) < 1.01*Settings().t_stop:
        t_stop *= 1.1
        self.handles["scope"].write(":TIMebase:RANGe %f" % (t_stop,))
        self.handles["scope"].query("*OPC?")
    self.handles["scope"].write(":TIMebase:REFerence CUSTOM")
    self.handles["scope"].write(":TIMebase:REFerence:LOCation 0.0")  # t=0 at left edge
    self.handles["scope"].query("*OPC?")

    # Arm
    arm(self)

    # Manual Trigger
    trigger(self)
    self.handles["scope"].query("*OPC?")
    for index in range(self._config["num_channels"]):
        self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (index + 1, 0))
    self.handles["scope"].query("*OPC?")

    # External Trigger
    self.handles["scope"].write(":TRIGger:MODE EDGE")  # Edge Trigger
    self.handles["scope"].write(":TRIGger:SWEep AUTO")  # Only acquire after trigger
    self.handles["scope"].write(":TRIGger:EDGE:SOURce EXTernal")  # External Trigger
    self.handles["scope"].write(":TRIGger:EDGE:LEVel %d" % (self._config["trigger_level"],))  # Trigger Level
    self.handles["scope"].write(":TRIGger:EDGE:SLOPe POSitive")  # Trigger Slope
    self.handles["scope"].query("*OPC?")


def arm(self):
    for index in range(self._config["num_channels"]):
        self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (index + 1, 1))
    self.handles["scope"].query("*OPC?")
    self.handles["scope"].write(":SINGle")
    time.sleep(0.1)


def trigger(self):
    self.handles["scope"].write(":TRIGger:FORCe")
