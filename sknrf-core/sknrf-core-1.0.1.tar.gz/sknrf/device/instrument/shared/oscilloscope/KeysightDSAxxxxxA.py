import time

import numpy as np

from sknrf.settings import Settings


def preset(self):
    self.handles["scope"].timeout = 60.0*1000
    timeout = self.handles["scope"].timeout
    # self.handles["scope"].timeout = 20.0*1000
    self.handles["scope"].write("*RST")
    self.handles["scope"].write("*CLS")
    time.sleep(5)
    self.handles["scope"].query("*OPC?")

    # Acquire Samples
    self.handles["scope"].write(":ACQuire:MODE RTIMe")  # Real-time Single Acquisition
    self.handles["scope"].write(":ACQuire:Average OFF")  # Average each time bucket
    self.handles["scope"].write(":ACQuire:INTerpolate INT16")  # Interpolation Filter
    srate = self._config["oversampling"]/Settings().t_step
    self.handles["scope"].write(":ACQuire:SRATe:ANALog %f" % (srate,))  # srate
    self.handles["scope"].query("*OPC?")

    # Read Waveform
    # self.handles["scope"].write(":WAVeform:TYPE INT")  # Set the waveform points mode.
    # self.handles["scope"].write(":WAVeform:POINts %d" % (points,))  # Set the points
    self.handles["scope"].write(":WAVeform:FORMat WORD")  # 16-Bit precision
    self.handles["scope"].write(":WAVeform:BYTeorder MSBFirst")  # MSB first
    self.handles["scope"].query("*OPC?")

    # Arm
    arm(self)

    # Manual Trigger
    trigger(self)
    self.handles["scope"].query("*OPC?")
    while not self._acquisition_done():
        time.sleep(0.1)

    # External Trigger (
    self.handles["scope"].write(":TRIGger:MODE EDGE")  # Edge Trigger
    self.handles["scope"].write(":TRIGger:SWEep AUTO")  # Only acquire after trigger
    self.handles["scope"].write(":TRIGger:EDGE:SOURce AUX")  # External Trigger
    self.handles["scope"].write(":TRIGger:LEVel AUX, %f" % (self._config["trigger_level"],))  # Trigger Level
    self.handles["scope"].write(":TRIGger:EDGE:SLOPe POSitive")  # Trigger Slope
    self.handles["scope"].query("*OPC?")

    self.handles["scope"].timeout = timeout


def arm(self):
    # Acquire Samples
    t_stop = Settings().t_step*self._v_.shape[-2] + 2*self.trigger_delay
    srate = float(self.handles["scope"].query(":ACQuire:SRATe:ANALog?"))
    t_points = np.ceil(t_stop*srate)
    self.handles["scope"].write("ACQuire:POINts %d" % (np.ceil(t_points),))  # t_points

    # Time
    self.handles["scope"].write(":TIMebase:RANGe %f" % (t_stop,))
    self.handles["scope"].write(":TIMebase:POSition %.9f" % (self.trigger_delay,))  # Trigger Delay
    self.handles["scope"].write(":TIMebase:REFerence LEFT")  # t=0 at left edge
    self.handles["scope"].query("*OPC?")

    self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (self._config["v_i_port"], 1))
    self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (self._config["v_q_port"], 1))
    self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (self._config["i_i_port"], 1))
    self.handles["scope"].write(":CHANnel%d:DISPlay %d" % (self._config["i_q_port"], 1))
    self.handles["scope"].query("*OPC?")


def trigger(self):
    self.handles["scope"].write(":SINGle")
