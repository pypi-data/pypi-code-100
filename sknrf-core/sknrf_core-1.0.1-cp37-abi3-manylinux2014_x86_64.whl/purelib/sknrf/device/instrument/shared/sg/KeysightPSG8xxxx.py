import time

import numpy as np

from sknrf.settings import Settings
from sknrf.utilities.rf import rW2dBm, dBm2rW, dBU2rU


def preset(self):
    self.handles["sg"].timeout = 60.0*1000
    timeout = self.handles["sg"].timeout
    self.handles["sg"].write("*RST")
    self.handles["sg"].write("*CLS")
    self.handles["sg"].write(":SYSTEM:PRESet:ALL")
    time.sleep(5)
    self.handles["sg"].query("*OPC?")
    self.handles["sg"].timeout = timeout

    output_index = 0
    self.handles["sg"].write(":OUTPut:STATe %d" % (int(False),))
    self.handles["sg"].write(":OUTPut:MOD %d" % (int(False),))
    self.handles["sg"].write(":SOURce:RADio:ARB:STATe 0")  # Turn Off ARB

    # Configure Modulation
    self.handles["sg"].write(":SOURce:RADio:ARB:VCO:CLOCk:SOURce INTernal")  # Internal Clock
    # self.handles["sg"].write(":SOURce:RADio:ARB:DACS:ALIGn")  # Re-align DACS after disconnecting/connecting external clock.
    self.handles["sg"].query("*OPC?")

    # Configure Markers
    self.handles["sg"].write(':SOURce:RADio:ARB:MPOLarity:MARKer1 POSitive')  # Positive polarity on Marker 1
    self.handles["sg"].write(':SOURce:RADio:ARB:MPOLarity:MARKer2 POSitive')  # Positive polarity on Marker 2
    self.handles["sg"].write(':SOURce:RADio:ARB:MPOLarity:MARKer3 POSitive')  # Positive polarity on Marker 3
    self.handles["sg"].write(':SOURce:RADio:ARB:MPOLarity:MARKer4 POSitive')  # Positive polarity on Marker 4
    self.handles["sg"].query("*OPC?")

    # Configure Header
    # self.handles["sg"].write(":SOURce:RADio:ARB:HEADer:CLEar")  # Clear Header
    self.handles["sg"].write(":SOURce:RADio:ARB:IQ:MODulation:FILTer:AUTO 0")  # Manual IQ Modulation Filter
    self.handles["sg"].write(":SOURce:RADio:ARB:IQ:EXTernal:FILTer:AUTO 0")  # Manual IQ Output Filter
    self.handles["sg"].query("*OPC?")

    # Configure Frequency
    self.f0 = Settings().f0

    # Configure Power
    power_limit = int(np.floor(rW2dBm(self._config["power_limit"][output_index])))
    self.handles["sg"].write(":SOURce:POWer:MODE FIXed")  # Fixed Power Level
    self.handles["sg"].write(":SOURce:POWer:ATTenuation:AUTO 1")  # Auto Source Attenuation (Safer for ALC)
    self.handles["sg"].write(":SOURce:POWer:LIMit:MAX:ADJust 1")  # Enable Adjust Power Limit
    self.handles["sg"].write(":SOURce:POWer:LIMit:MAX %d dBm" % (power_limit,))  # Adjust Power Limit
    self.handles["sg"].write(":SOURce:POWer:LIMit:MAX:ADJust 0")  # Disable Enable Adjust Power Limit
    # self.handles["sg"].write(":NOISe:STATe 0")  # Don't Optimize SNR
    self.handles["sg"].query("*OPC?")

    # # Continuous Trigger
    # self.handles["sg"].write(":SOURce:RADio:ARB:TRIGger:SOURce BUS")  # Internal Trigger
    # self.handles["sg"].query("*OPC?")

    # Single Trigger
    trigger_type = "SINGle" if Settings().signal_rep > 0 else "CONTinuous"
    self.handles["sg"].write(":SOURce:RADio:ARB:TRIGger:TYPE %s" % (trigger_type,))  # Trigger type
    self.handles["sg"].write(":SOURce:RADio:ARB:RETRigger OFF")  # Ignore Re-Triggers
    self.handles["sg"].write(":SOURce:RADio:ARB:TRIGger:SOURce:EXTernal:SLOPe POSitive")  # Trigger Polarity
    self.handles["sg"].write(":SOURce:RADio:ARB:TRIGger:TYPE:CONTinuous:TYPE  TRIGger")  # Wait for Trigger
    self.handles["sg"].write(":SOURce:RADio:ARB:TRIGger:SOURce:EXTernal:SOURce EPT1")  # Pattern Trig 1 Input
    if self.trigger_delay > 0.0:
        self.handles["sg"].write(":SOURce:RADio:ARB:TRIGger:SOURce:EXTernal:DELay %.8f" % (self.trigger_delay,))  # Trigger Delay
        self.handles["sg"].write(":SOURce:RADio:ARB:TRIGger:SOURce:EXTernal:DELay:STATe 1")  # Trigger Delay Enable
    else:
        self.handles["sg"].write(":SOURce:RADio:ARB:TRIGger:SOURce:EXTernal:DELay:STATe 0")  # Trigger Delay Enable
    self.handles["sg"].write(":SOURce:RADio:ARB:TRIGger:SOURce EXT")  # Internal Trigger
    self.handles["sg"].query("*OPC?")


def arm(self):
    if self.trigger_delay > 0.0:
        self.handles["sg"].write(":SOURce:RADio:ARB:TRIGger:SOURce:EXTernal:DELay %.8f" % (self.trigger_delay,))  # Trigger Delay
        self.handles["sg"].write(":SOURce:RADio:ARB:TRIGger:SOURce:EXTernal:DELay:STATe 1")  # Trigger Delay Enable
    else:
        self.handles["sg"].write(":SOURce:RADio:ARB:TRIGger:SOURce:EXTernal:DELay:STATe 0")  # Trigger Delay Enable
    self.handles["sg"].write(":SOURce:RADio:ARB:TRIGger:SOURce EXT")  # Internal Trigger
    self.handles["sg"].query("*OPC?")


def trigger(self):
    self.handles["sg"].write("*TRG")  # Trigger
