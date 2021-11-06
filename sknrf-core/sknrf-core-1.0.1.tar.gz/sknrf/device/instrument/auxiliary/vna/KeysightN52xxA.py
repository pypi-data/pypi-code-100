import sys

import numpy as np
if sys.platform == "win32": from win32com.client import DispatchEx
import pyvisa as visa

from sknrf.enums.device import Response
from sknrf.settings import Settings
from sknrf.device.instrument.auxiliary.vna.base import NoVNA
from sknrf.utilities.numeric import AttributeInfo, Info, PkAvg, Format
from sknrf.device.instrument.shared.vna import KeysightN52xxA
from sknrf.device.instrument.shared.vna.KeysightN52xxA import wb_t_stop_ifbw_lut
if sys.platform == "win32": from sknrf.device.instrument.shared.pnax.PNACOM import constants as consts
from sknrf.utilities.numeric import Info
from sknrf.utilities.rf import dBm2rW, dBU2rU


class KeysightN52xxASP(NoVNA):
    signal_list = []
    transforms_list = []
    firmware_map = {'Application Code Version': "A.10.47.06",
                    'Hard Drive Disk Version': "S.28.03.07",
                    'System CPU Version': "6.0",
                    'DSP Version': "5.0"}
    display_order = []

    def __new__(cls, error_model, num_ports, config_filename="",
                machine_name="10.0.0.12",
                resource_id='TCPIP0::10.0.0.12::inst0::INSTR', **kwargs):
        self = super(KeysightN52xxASP, cls).__new__(cls, error_model, num_ports, config_filename, **kwargs)
        self.machine_name = machine_name
        self.resource_id = resource_id
        return self

    def __getnewargs__(self):
        return tuple(list(super().__getnewargs__()) + [self.machine_name, self.resource_id])

    def __init__(self, error_model, num_ports, config_filename="",
                 machine_name="10.0.0.12",
                 resource_id='TCPIP0::10.0.0.12::inst0::INSTR', **kwargs):
        super(KeysightN52xxASP, self).__init__(error_model, num_ports, config_filename, **kwargs)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self.measure()
        self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoVNA, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(KeysightN52xxASP, self).__setstate__(state)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self.measure()
        self.initialized = True

    def __info__(self):
        super().__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["machine_name"] = Info("machine_name", read=False, write=True, check=False)
        self.info["resource_id"] = Info("resource_id", read=False, write=True, check=False)
        self.info["t_drift"] = Info("t_drift", read=True, write=False, check=False, format_=Format.RE, scale=Scale.u, unit="s")

    def connect_handles(self):
        self.handles["vna"] = DispatchEx("AgilentPNA835x.Application", self.machine_name)
        rm = visa.ResourceManager()
        self.handles["vna_visa"] = rm.open_resource(self.resource_id)
        super(KeysightN52xxASP, self).connect_handles()

    def preset(self):
        super().preset()
        if self.unique_handle(self.handles['vna']):
            KeysightN52xxA.preset(self)

    @property
    def _on(self):
        return self.handles["vna"].SourcePowerState

    @_on.setter
    def _on(self, _on):
        self.handles["vna"].SourcePowerState = _on
        self._on_ = _on

    @property
    def t_drift(self):
        chan = self.handles["vna"].Channel(1)
        return chan.SweepDelay

    def arm(self):
        chan = self.handles["vna"].Channel(1)
        freq = self.freq.flatten()
        t_stop = freq.size*Settings().t_stop
        timing_lut = np.asarray(wb_t_stop_ifbw_lut)
        t_step = timing_lut[:, 0]/(timing_lut[:, 1]-1)
        t_step_index = np.argwhere(freq.size*t_step < t_stop)[0][0]
        ifbw = timing_lut[t_step_index, 2]
        t_dwell = Settings().t_stop % t_step[t_step_index]
        power = chan.TestPortPower(1)
        segs = chan.Segments
        segs.SourcePowerOption = True
        segs.IFBandwidthOption = True
        segs.SweepTimeOption = True
        self.handles["vna_visa"].write("SENS:SEGM:DEL:ALL")
        segdata = np.zeros((7, 1), dtype=np.float)
        segdata[0][:] = 1.0  # Enable
        segdata[1][:] = freq.size  # Number of Points
        segdata[2][:] = freq[0]  # Start Frequency
        segdata[3][:] = freq[-1]  # Stop Frequency
        segdata[4][:] = ifbw  # IFBW
        segdata[5][:] = t_dwell//1e-6*1e-6  # delay before measuring each point
        segdata[6][:] = power  # Power
        segs.SetAllSegments(segdata.tolist())
        chan.SweepType = consts.naSegmentSweep
        chan.SweepDelay = t_stop - chan.SweepTime  # delay before sweeping frequency
        chan.Continuous()

    def trigger(self):
        KeysightN52xxA.trigger(self)

    def measure(self):
        chan = self.handles["vna"].Channel(1)
        meass = self.handles["vna"].Measurements
        index = 1
        points = chan.NumberOfPoints//self.sp.shape[0]
        shape_ = (self.sp.shape[0], points, 1, 1)
        for src_index in range(self.num_ports):
            for rcvr_index in range(self.num_ports):
                self.sp[:, 0:points, rcvr_index:rcvr_index + 1, src_index:src_index + 1] = \
                    np.asarray(meass.Item(index).getData(consts.naCorrectedData, consts.naDataFormat_Real)).reshape(shape_) + \
                    1j * np.asarray(meass.Item(index).getData(consts.naCorrectedData, consts.naDataFormat_Imaginary)).reshape(shape_)
                index += 1
        super().measure()
