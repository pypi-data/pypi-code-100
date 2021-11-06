import time

import numpy as np

from sknrf.settings import Settings


def preset(self):
    self.handles["scope"].timeout = 60.0*1000
    timeout = self.handles["scope"].timeout
    # self.handles["scope"].timeout = 20.0*1000
    self.handles["scope"].write("*RST")
    self.handles["scope"].write("*CLS")
    self.handles["scope"].clear()
    time.sleep(5)
    self.handles["scope"].query("*OPC?")

    # Waveform
    points = np.asarray(self._config["points"], dtype=np.int)
    waveform_points = points[points/Settings().t_points > self._config["oversampling"]][0]  # Minimum oversampling for time-interpolation
    self.handles["scope"].write(":ACQuire:TYPE NORMal")  # Normal Aquisition
    self.handles["scope"].write(":ACQuire:COUNt")  # Averaging

    self.handles["scope"].write(":WAVeform:POINts:MODE RAW")  # Set the waveform points mode.
    self.handles["scope"].write(":WAVeform:POINts %d" % (waveform_points,))  # Set the waveform points
    self.handles["scope"].write(":WAVeform:FORMat WORD")  # 16-Bit precision
    self.handles["scope"].write(":WAVeform:BYTeorder MSBFirst")  # MSB first
    self.handles["scope"].query("*OPC?")

    # Arm
    arm(self)

    # Manual Trigger
    trigger(self)
    self.handles["scope"].query("*OPC?")

    self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (self._config["v_i_port"], 0))
    self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (self._config["v_q_port"], 0))
    self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (self._config["i_i_port"], 0))
    self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (self._config["i_q_port"], 0))
    self.handles["scope"].query("*OPC?")

    # External Trigger
    self.handles["scope"].write(":TRIGger:MODE EDGE")  # Edge Trigger
    self.handles["scope"].write(":TRIGger:SWEep AUTO")  # Only acquire after trigger
    self.handles["scope"].write(":TRIGger:EDGE:SOURce EXTernal")  # External Trigger
    self.handles["scope"].write(":TRIGger:EDGE:LEVel %d" % (self._config["trigger_level"],))  # Trigger Level
    self.handles["scope"].write(":TRIGger:SLOPe POSitive")  # Trigger Slope
    self.handles["scope"].query("*OPC?")

    self.handles["scope"].timeout = timeout


def arm(self):
    # Time
    self.handles["scope"].write(":TIMebase:MODE MAIN")
    self.handles["scope"].write(":TIMebase:RANGe %f" % (Settings().t_step*self._v_.shape[-2] + 2*self.trigger_delay,))
    self.handles["scope"].write(":TIMebase:REFerence CUSTOM")
    self.handles["scope"].write(":TIMebase:REFerence:LOCation 0.0")  # t=0 at left edge
    self.handles["scope"].query("*OPC?")

    self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (self._config["v_i_port"], 1))
    self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (self._config["v_q_port"], 1))
    self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (self._config["i_i_port"], 1))
    self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (self._config["i_q_port"], 1))
    self.handles["scope"].query("*OPC?")

    self.handles["scope"].write(":SINGle")

def trigger(self):
    self.handles["scope"].write(":TRIGger:FORCe")
