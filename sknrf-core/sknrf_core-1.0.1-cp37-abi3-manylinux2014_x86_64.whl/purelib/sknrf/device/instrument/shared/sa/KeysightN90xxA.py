import time

from sknrf.settings import Settings
from sknrf.utilities.rf import rU2dBU


#                           |t_step                |Digtal IFBW|
gaussian_t_step_ifbw_lut = [[0.007543466669447491  ,       10],
                            [0.006860800000702546  ,       11],
                            [0.006280533334876838  ,       12],
                            [0.005802666667458924  ,       13],
                            [0.005015000000406215  ,       15],
                            [0.004710399998938841  ,       16],
                            [0.004181999999286551  ,       18],
                            [0.003430400000351273  ,       22],
                            [0.003140266666452291  ,       24],
                            [0.002787999999913014  ,       27],
                            [0.0022869333335675153 ,       33],
                            [0.0020910000000805037 ,       36],
                            [0.0019304000001646245 ,       39],
                            [0.0017509999999959728 ,       44],
                            [0.0016042666665571487 ,       47],
                            [0.001478999999943798  ,       51],
                            [0.0013430000000425732 ,       56],
                            [0.0012144000000124354 ,       62],
                            [0.001109333333323867  ,       68],
                            [0.001002999999980642  ,       75],
                            [0.000917999999777844  ,       82],
                            [0.0008264666667141609 ,       91],
                            [0.000753000000192768  ,      100],
                            [0.0006860666666471366 ,      110],
                            [0.0006265333334313232 ,      120],
                            [0.0005802666667458924 ,      130],
                            [0.000501999999876508  ,      150],
                            [0.00047040000003010563,      160],
                            [0.00041833333333542497,      180],
                            [0.0003771999999511149 ,      200],
                            [0.00034300000000514496,      220],
                            [0.0003141333333216057 ,      240],
                            [0.00027879999999130145,      270],
                            [0.000251000000001255  ,      300],
                            [0.00022866666664395242,      330],
                            [0.00020886666666470333,      360],
                            [0.00019279999998889473,      390],
                            [0.00017526666665591698,      430],
                            [0.00016               ,      470],
                            [0.00014759999999297424,      510],
                            [0.00013440000000860159,      560],
                            [0.00012159999999299584,      620],
                            [0.00011060000000088481,      680],
                            [0.00010039999999546191,      750],
                            [9.199999997791999e-05 ,      820],
                            [8.266666669091555e-05 ,      910],
                            [7.533333335141333e-05 ,     1000],
                            [6.833333334016667e-05 ,     1100],
                            [6.266666666081778e-05 ,     1200],
                            [5.7866666669289954e-05,     1300],
                            [5.01999999876508e-05  ,     1500],
                            [4.700000001034e-05    ,     1600],
                            [4.17999999931448e-05  ,     1800],
                            [3.76000000012032e-05  ,     2000],
                            [3.42000000021888e-05  ,     2200],
                            [3.133333333040889e-05 ,     2400],
                            [2.7866666669862046e-05,     2700],
                            [2.5066666667468802e-05,     3000],
                            [2.28000000014592e-05  ,     3300],
                            [2.09333333319936e-05  ,     3600],
                            [1.933333333372e-05    ,     3900],
                            [1.746666666573511e-05 ,     4300],
                            [1.6e-05               ,     4700],
                            [1.47999999994672e-05  ,     5100],
                            [1.346666666713351e-05 ,     5600],
                            [1.2133333332977422e-05,     6200],
                            [1.1066666667050312e-05,     6800],
                            [1.00666666671096e-05  ,     7500],
                            [9.199999997792e-06    ,     8200],
                            [8.266666669091556e-06 ,     9100],
                            [7.533333335141333e-06 ,    10000],
                            [6.866666664835556e-06 ,    11000],
                            [6.266666666081778e-06 ,    12000],
                            [5.800000000116e-06    ,    13000],
                            [5e-06                 ,    15000],
                            [4.7333333340906665e-06,    16000],
                            [4.199999999916e-06    ,    18000],
                            [3.733333332736e-06    ,    20000],
                            [3.399999999524e-06    ,    22000],
                            [3.133333333040889e-06 ,    24000],
                            [2.8000000003359996e-06,    27000],
                            [2.533333333367111e-06 ,    30000],
                            [2.266666666606222e-06 ,    33000],
                            [2.0666666668457777e-06,    36000],
                            [1.9333333333720002e-06,    39000],
                            [1.7333333334026666e-06,    43000],
                            [1.6e-06               ,    47000],
                            [1.4666666667057778e-06,    51000],
                            [1.3333333333333334e-06,    56000],
                            [1.2000000000479998e-06,    62000],
                            [1.133333333303111e-06 ,    68000],
                            [1e-06                 ,    75000],
                            [9.333333337066667e-07 ,    82000],
                            [8e-07                 ,    91000],
                            [7.333333331377778e-07 ,   100000],
                            [6.666666666666667e-07 ,   110000],
                            [5.999999998800001e-07 ,   120000],
                            [5.999999998800001e-07 ,   130000],
                            [5.333333333333333e-07 ,   150000],
                            [4.666666666355555e-07 ,   160000],
                            [4e-07                 ,   180000],
                            [4e-07                 ,   200000],
                            [3.3333333333333335e-07,   220000],
                            [3.3333333333333335e-07,   240000],
                            [2.6666666666666667e-07,   270000],
                            [2.6666666666666667e-07,   300000],
                            [2.6666666666666667e-07,   330000],
                            [2e-07                 ,   360000],
                            [2e-07                 ,   390000],
                            [2e-07                 ,   430000],
                            [2e-07                 ,   470000],
                            [2e-07                 ,   510000],
                            [1.3333333333333334e-07,   560000],
                            [1.3333333333333334e-07,   620000],
                            [1.3333333333333334e-07,   680000],
                            [1.3333333333333334e-07,   750000],
                            [1.3333333333333334e-07,   820000],
                            [1.3333333333333334e-07,   910000],
                            [1.3333333333333334e-07,  1000000],
                            [6.666666666666667e-08 ,  1100000],
                            [6.666666666666667e-08 ,  1200000],
                            [6.666666666666667e-08 ,  1300000],
                            [6.666666666666667e-08 ,  1500000],
                            [6.666666666666667e-08 ,  1600000],
                            [6.666666666666667e-08 ,  1800000],
                            [6.666666666666667e-08 ,  2000000],
                            [6.666666666666667e-08 ,  2200000],
                            [6.666666666666667e-08 ,  2400000],
                            [6.666666666666667e-08 ,  2700000],
                            [6.666666666666667e-08 ,  3000000],
                            [6.666666666666667e-08 ,  4000000],
                            [6.666666666666667e-08 ,  5000000],
                            [6.666666666666667e-08 ,  6000000],
                            [6.666666666666667e-08 ,  8000000],
                            [6.666666666666667e-08 , 10000000]]


def print_t_step(self):
    for t_step, ifbw in gaussian_t_step_ifbw_lut:
        self.handles["sa"].write(":SENSe:WAVeform:DIF:BANDwidth %d" %(ifbw,))
        self.handles["sa"].write(":INITiate:WAVeform")
        print(1/float(self.handles["sa"].query(":SENSe:WAVeform:SRATe?")))


def preset(self):
    self.handles["sa"].timeout = 70.0 * 1000
    timeout = self.handles["sa"].timeout
    self.handles["sa"].timeout = 20.0 * 1000
    self.handles["sa"].write("*RST")
    self.handles["sa"].write("*CLS")
    self.handles["sa"].write(":INSTrument:SELect BASIC")
    time.sleep(5)
    self.handles["sa"].write(":SYSTem:PRESet")
    self.handles["sa"].query("*OPC?")

    output_index = 0
    self.handles["sa"].write(":SENSe:FEED:RF:PORT:INPut RFIN")  # RFIN Input Port

    #Pre-Amp Gain and Attenuation
    self.handles["sa"].write(":SENSe:CORRection:SA:RF:GAIN %d" % (int(rU2dBU(self._config["pre_amplifier_gain"])),))
    self.handles["sa"].write(":SENSe:POWer:RF:ATTenuation %d" % (int(rU2dBU(self._config["mechanical_attenuation"]))))
    self.handles["sa"].write(":SENSe:POWer:RF:EATTenuation %d" % (int(rU2dBU(self._config["electrical_attenuation"]))))

    # Error Corrections
    self.handles["sa"].write(":SENSe:CORRection:CSET1:STATe 0")
    self.handles["sa"].write(":SENSe:CORRection:CSET2:STATe 0")
    self.handles["sa"].write(":SENSe:CORRection:CSET3:STATe 0")
    self.handles["sa"].write(":SENSe:CORRection:CSET4:STATe 0")
    self.handles["sa"].write(":SENSe:CORRection:CSET5:STATe 0")
    self.handles["sa"].write(":SENSe:CORRection:CSET6:STATe 0")
    self.handles["sa"].write(":SENSe:CORRection:CSET7:STATe 0")
    self.handles["sa"].write(":SENSe:CORRection:CSET8:STATe 0")

    # Waveform Mode
    self.handles["sa"].write(":CONFigure:WAVeform")

    # Frequency
    self.f0 = Settings().f0

    # Display Y
    self.handles["sa"].write(":DISPlay:WAVeform:VIEW1:WINDow1:TRACe:Y:SCALe:RLEVel %d" % (0,))  # Reference Level
    self.handles["sa"].write(":DISPlay:WAVeform:VIEW1:WINDow1:TRACe:Y:SCALe:RPOSition TOP")  # Reference Position
    self.handles["sa"].query("*OPC?")

    # Arm
    arm(self)

    # Internal Trigger
    self.handles["sa"].write("TRIG:WAVeform:SOURce IMMediate")
    self.handles["sa"].query("*OPC?")
    self.handles["sa"].write(":INITiate:WAVeform")
    self.handles["sa"].query("*OPC?")

    # External Trigger IN
    self.handles["sa"].write("TRIG:WAVeform:SOURce EXT1")  # External Trigger
    self.handles["sa"].write(":TRIGger:SEQuence:EXTernal1:LEVel %d" % (self._config["trigger_level"],))  # Trigger Level
    self.handles["sa"].write(":TRIGger:SEQuence:EXTernal1:SLOPe POSitive")  # Trigger Slope
    self.handles["sa"].write(":TRIGger:SEQuence:EXTernal1:DELay %.9f" % (self.trigger_delay,))  # Trigger Delay
    self.handles["sa"].write(":TRIGger:SEQuence:EXTernal1:DELay:STATe 1")  # Enable Trigger Delay
    self.handles["sa"].query("*OPC?")

    # External Trigger Out
    self.handles["sa"].write(":TRIGger1:SEQuence:OUTput MAIN")  # Main Trigger
    self.handles["sa"].write(":TRIGger1:SEQuence:OUTPut:POLarity POSitive")  # Positive polarity
    self.handles["sa"].query("*OPC?")

    self.handles["sa"].timeout = timeout


def arm(self):
    # External Trigger
    self.handles["sa"].write(":TRIGger:SEQuence:EXTernal1:DELay %.9f" % (self.trigger_delay,))  # Trigger Delay
    self.handles["sa"].query("*OPC?")

    # Time
    t_stop = Settings().t_step*self._b_p_.shape[-2]
    self.handles["sa"].write(":SENSe:WAVeform:SWEep:TIME %f" % (t_stop,))  # t_stop
    self.handles["sa"].write(":SENSe:WAVeform:SRATe %f" % (1/Settings().t_step))  # t_step
    increment = 1
    while float(self.handles["sa"].query(":SENSe:WAVeform:SWEep:TIME?")) < t_stop:
        self.handles["sa"].write(":SENSe:WAVeform:SWEep:TIME %f" % (t_stop + Settings().t_step*increment,))
        increment += 1
    self.handles["sa"].query("*OPC?")

    self.handles["sa"].write(":INIT:CONT 0")
    self.handles["sa"].write(":INITiate:IMMediate")
    time.sleep(1)


def trigger(self):
    self.handles["sa"].write("TRIG")
