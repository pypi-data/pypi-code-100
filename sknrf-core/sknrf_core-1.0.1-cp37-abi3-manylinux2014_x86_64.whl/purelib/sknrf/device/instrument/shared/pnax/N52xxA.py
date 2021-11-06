import sys

from sknrf.settings import Settings

if sys.platform == "win32": from sknrf.device.instrument.shared.pnax.PNACOM import constants as consts

#                     |t_stop_min|t_points_min|RBW|
# where                t_step_min = t_stop_min/t_points_min,
# Point-In-Pulse:      t_pulse_width_min = t_stop_min/t_points_min*2
# Pulse-Profile:       t_res             = t_stop_min/t_points
wb_t_stop_ifbw_lut = [[0.883977600, 2,           1],
                      [0.442061400, 2,           2],
                      [0.294683400, 2,           3],
                      [0.176781000, 2,           5],
                      [0.126396600, 2,           7],
                      [0.088499400, 2,          10],
                      [0.059023800, 2,          15],
                      [0.044286000, 2,          20],
                      [0.029548200, 2,          30],
                      [0.017728920, 2,          50],
                      [0.012675960, 2,          70],
                      [0.008871720, 2,         100],
                      [0.005938680, 2,         150],
                      [0.004472160, 2,         200],
                      [0.002991120, 2,         300],
                      [0.001807740, 2,         500],
                      [0.001306800, 2,         700],
                      [0.000922020, 2,        1000],
                      [0.000631620, 2,        1500],
                      [0.000486420, 2,        2000],
                      [0.000333960, 2,        3000],
                      [0.000217800, 2,        5000],
                      [0.000166980, 2,        7000],
                      [0.000123420, 2,       10000],
                      [9.68000e-05, 2,       15000],
                      [0.000108900, 3,       20000],
                      [9.68000e-05, 4,       30000],
                      [8.71200e-05, 6,       50000],
                      [9.33300e-05, 9,       70000],
                      [9.43800e-05, 13,     100000],
                      [9.68000e-05, 20,     150000],
                      [9.80100e-05, 27,     200000],
                      [9.80400e-05, 38,     280000],
                      [9.88100e-05, 41,     360000],
                      [9.64000e-05, 40,     600000],
                      [9.93600e-05, 138,   1000000],
                      [9.98400e-05, 208,   1500000],
                      [9.97200e-05, 277,   2000000],
                      [1.00000e-04, 400,   3000000],
                      [1.00000e-04, 666,   5000000],
                      [1.00000e-04, 1000,  7000000],
                      [9.99600e-05, 1428, 10000000],
                      [1.00000e-04, 2000, 15000000]]


def preset(self):
    app = self.handles['pnax']
    chan = app.Channel(1)
    pathConfig = chan.PathConfiguration
    rx_level = chan.GetRxLevelingConfiguration()
    auxTrig = chan.AuxiliaryTrigger(1)
    trigSetup = app.TriggerSetup
    meass = app.Measurements

    # Application
    app.Preset()
    app.SourcePowerState = False

    # Channel
    chan.CouplePorts = consts.naOFF
    chan.StartFrequency = Settings().freq[1]
    chan.StopFrequency = Settings().freq[-1]
    chan.NumberOfPoints = Settings().f_points - 1

    # Path Config (Option 423)
    pathConfig.Element("Combiner").Value = "Normal"
    pathConfig.Element("Src1Out1LowBand").Value = "Filtered"
    pathConfig.Element("Src2Out1LowBand").Value = "Filtered"
    pathConfig.Element("Port1Bypass").Value = "Thru"
    pathConfig.Element("Port2Bypass").Value = "Thru"
    pathConfig.Element("Port3Bypass").Value = "Thru"
    pathConfig.Element("Port4Bypass").Value = "Thru"
    pathConfig.Element("Port1RefMxr").Value = "External"
    pathConfig.Element("Port2Src").Value = "Src1Out2"
    pathConfig.Element("Src1RearOut").Value = "Normal"

    # Receiver
    chan.IFBandwidth = Settings().RBW
    for port_num in range(1, 5):
        chan.SetReceiverAttenuator(port_num, 0)
    for index in range(meass.Count, 0, -1):
        meass.Remove(index)
    channel, source, window = 1, 1, 1
    meass.Add(channel, "B", source, window)
    # meass.Add(channel, "D/B", source, window)
    # meass.Add(channel, "A/B",  source, window)
    # meass.Add(channel, "R3/B", source, window)
    # meass.Add(channel, "C/B",  source, window)
    meass.Add(channel, "D", source, window)
    meass.Add(channel, "A", source, window)
    meass.Add(channel, "R3", source, window)
    meass.Add(channel, "C", source, window)

    # Source
    for port_num in range(1, 6):
        chan.SetSourcePortMode(port_num, consts.naSourcePortOff)
        chan.SetAttenuatorMode(port_num, consts.naMANUAL)
        chan.SetAttenuator(port_num, 10.0)
        if port_num != 2 and port_num != 4:
            chan.SetALCLevelingMode(port_num, consts.naALCOpenLoop)
        rx_level.SetState(port_num, False)

    # Averaging
    chan.AveragingFactor = Settings().averaging
    chan.AverageMode = 0  # Point Averaging
    chan.Averaging = True

    # Trigger
    trigSetup.Source = consts.naTriggerInternal
    # Low-Speed Timing using Auxilary Trigger1
    auxTrig.TriggerOutPolarity = consts.naTriggerPositive
    auxTrig.TriggerOutPosition = consts.naTriggerOutBeforeAcquire
    auxTrig.TriggerOutDuration = 1e-6
    auxTrig.enable = True


def preset_pulsed(self):
    app = self.handles['pnax']
    chan = app.Channel(1)
    pulse = chan.PulseGenerator
    auto_pulse = chan.PulseMeasControl
    # High-Speed Timing using Pulse Generators
    # Disable auto-configuration
    auto_pulse.PulseMeasMode = consts.naPulseProfileMeasurement
    auto_pulse.AutoCWSweepTime = False
    auto_pulse.AutoOptimizePRF = False
    auto_pulse.AutoPulseTiming = False
    auto_pulse.AutoDetection = False
    auto_pulse.WideBandDectionState = True  # Wideband
    auto_pulse.AutoIFBandWidth = False
    auto_pulse.AutoSelectPulseGen = False
    auto_pulse.SoftwareGateState = False
    # Time Sweep
    auto_pulse.PulseProfileStart = 0.0  # t_start
    chan.IFBandwidth = Settings().RBW  # Related to 1/t_step (see wb_t_stop_ifbw_lut)
    auto_pulse.PulseProfileStop = Settings().t_step*Settings().t_points  # t_stop
    auto_pulse.MasterFrequency = 1/(Settings().t_step*Settings().t_points)
    auto_pulse.MasterPeriod = Settings().t_step*Settings().t_points
    auto_pulse.MasterWidth = Settings().t_step*Settings().t_points
    # auto_pulse.PulseOffAlcMode = consts.naALCOpenLoop
    # Enable Manual Configuration
    #     - RFSourceN uses PulseN
    #     - All RFReceivers use Pulse0
    pulse.TriggerInType = consts.naTriggerLevel
    pulse.TriggerInPolarity = consts.naTriggerPositive
    pulse.Period = Settings().t_step*Settings().t_points
    pulse.SetSubPointTrigger(0, True)
    pulse.SetState(0, True)
    for pulse_num in range(1, 5):
        pulse.SetDelay(pulse_num, 0.0)
        pulse.SetDelayIncrement(pulse_num, Settings().t_step)
        pulse.SetWidth(pulse_num, Settings().t_step*Settings().t_points)
        pulse.SetInvert(pulse_num, False)
        pulse.SetState(pulse_num, True)


def trigger(self):
    app = self.handles['pnax']
    chan = app.Channel(1)
    app.SourcePowerState = True
    chan.Single(True)  # Block execution
    app.SourcePowerState = False
