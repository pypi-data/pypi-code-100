import time

import numpy as np

from sknrf.settings import Settings


def preset(self):
    self.handles["scope"].write("*CLS")
    self.handles["scope"].write("*RST")
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
    self.handles["scope"].write(":TRIGger:LEVel AUX, %d" % (self._config["trigger_level"],))  # Trigger Level
    self.handles["scope"].write(":TRIGger:EDGE:SLOPe POSitive")  # Trigger Slope
    self.handles["scope"].write(":TRIGger:SWEep TRIGgered")
    self.handles["scope"].query("*OPC?")


def arm(self):
    t_points = self._b_p_.shape[-2]
    t_reps = t_points / Settings().t_points
    t_stop = t_reps * Settings().t_stop

    #  Acquire
    points = np.asarray(self._config["points"], dtype=np.int)
    waveform_points = points[points*self._config["resample"]/t_points > 1][0]
    self.handles["scope"].write(":ACQuire:MODE RTIMe")  # Normal Aquisition
    # self.handles["scope"].write(":ACQuire:MODE HRESolution")  # High Resolution Mode
    self.handles["scope"].write(":ACQuire:COUNT 1")  # Normal Aquisition
    self.handles["scope"].write(":ACQuire:POINts %d" % (waveform_points,))  # Set the waveform points
    self.handles["scope"].query("*OPC?")

    #  Waveform# Up-sample on instrument
    self.handles["scope"].write(":WAVeform:FORMat WORD")  # 16-Bit precision
    self.handles["scope"].write(":WAVeform:BYTeorder MSBFirst")  # MSB first
    self.handles["scope"].query("*OPC?")

    # Time
    t_stop_min = 1.01*t_stop
    self.handles["scope"].write(":TIMebase:RANGe %f" % (t_stop,))
    while float(self.handles["scope"].query(":TIMebase:RANGe?")) < t_stop_min:
        t_stop *= 1.1
        self.handles["scope"].write(":TIMebase:RANGe %f" % (t_stop,))
        self.handles["scope"].query("*OPC?")
    self.handles["scope"].write(":TIMebase:REFerence LEFT")  # t=0 at left edge
    self.handles["scope"].query("*OPC?")

    for index in range(self._config["num_channels"]):
        self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (index + 1, 1))
    # self.handles["scope"].query("*OPC?")
    self.handles["scope"].write(":SINGle")
    time.sleep(0.1)


def trigger(self):
    self.handles["scope"].write(":TRIGger:FORCe")
