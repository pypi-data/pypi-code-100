import os
import logging

import numpy as np
from scipy.signal import resample
from scipy.interpolate import interp1d
import torch as th
import pyvisa as visa

from sknrf.settings import Settings
from sknrf.utilities.numeric import Info, bounded_property
from sknrf.enums.runtime import SI, si_eps_map
from sknrf.device.instrument.rfsource import base
from sknrf.device.instrument.shared.awg import TeledyneT3AWGxxxx
from sknrf.device.signal import tf
from sknrf.utilities.rf import dBU2rU
from sknrf.device.instrument.shared.switch.MiniCircuits_RC_2SP6T_A12 import MiniCircuits_Switch


logger = logging.getLogger(__name__)

__author__ = 'dtbespal'


class RitptideModulatedDiff(base.NoRFSourceModulated):
    firmware_map = {}
    display_order = ["on", "initialized", "channel", "port", "freq", "a_p",
                     "delay", "pulse_width", "period",
                     "iq_files"]

    def __new__(cls, error_model, port="9760", config_filename="",
                resource_id='172.16.0.160'):  # switch_id="USB::0x20CE::0x0022"
        self = super(RitptideModulatedDiff, cls).__new__(cls, error_model, port, config_filename)
        # Define object ATTRIBUTES
        self.port = port
        self.resource_id = resource_id

        return self

    def __getnewargs__(self):
        return tuple(list(super(RitptideModulatedDiff, self).__getnewargs__())
                     + [self.resource_id, self.switch_id])

    def __init__(self, error_model, port="9760", config_filename="",
                 resource_id='172.16.0.160'):
        super().__init__(error_model, port, config_filename)
        self.port = port
        self.resource_id = resource_id

        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self._pulse_width = self.period
        self._delay = 0.0
        self.iq_files = self._iq_files_
        self._a_p = th.zeros_like(self._a_p_)
        self.initialized = True

    def __getstate__(self, state={}):
        state = super(RitptideModulatedDiff, self).__getstate__(state=state)
        state["channel"] = self.channel
        return state

    def __setstate__(self, state, *args, **kwargs):
        super().__setstate__(state)
        self.resource_id = state["resource_id"]
        self.switch_id = state["switch_id"]

        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self._pulse_width = state["_pulse_width"]
        self._delay = state["_delay"]
        self.iq_files = state["iq_files"]
        self._a_p = self._a_p_
        self.initialized = True

    def __info__(self):
        super(RitptideModulatedDiff, self).__info__()
        rtol = 1/2**16
        v_atol = 1e-3
        a_atol = v_atol/np.sqrt(50.)
        v_max = 2*(self._config["voltage_limit"] - v_atol)
        a_max = v_max/np.sqrt(50.)
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["resource_id"] = Info("resource_id", read=True, write=True, check=False)
        self.info["switch_id"] = Info("switch_id", read=True, write=True, check=False)
        self.info["channel"] = Info("channel", read=True, write=True, check=False, min_=0, max_=6)
        self.info["_a_p"] = Info("_a_p", read=False, write=False, check=False,
                                 min_=a_atol, max_=a_max, abs_tol=a_atol, rel_tol=rtol)
        self.info["a_p"].min, self.info["a_p"].max = a_atol, a_max
        self.info["a_p"].abs_tol, self.info["a_p"].rel_tol = a_atol, rtol
        self.info["v_s"].min, self.info["v_s"].max = v_atol, v_max
        self.info["v_s"].abs_tol, self.info["v_s"].rel_tol = v_atol, rtol

    def connect_handles(self):
        rm = visa.ResourceManager(os.environ["VISA_LIB"])
        self.handles["awg"] = rm.open_resource(self.resource_id)
        super(RitptideModulatedDiff, self).connect_handles()

    # def preset(self):
    #     super(RitptideModulatedDiff, self).preset()
    #     if self.unique_handle(self.handles['awg']):
    #         TeledyneT3AWGxxxx.preset(self)
    #     if "switch" in self.handles and self.unique_handle(self.handles["switch"]):
    #         MiniCircuits_Switch.preset(self.handles["switch"])
    #
    #     self.handles["awg"].write("OUTPut%d:SERIESIMPedance %s" % (1, "50Ohm"))
    #     self.handles["awg"].write("DISPlay:UNIT:VOLT AMPLitudeoff")
    #     self.handles["awg"].write("SEQuence:ELEM1:OFFSET%d %f;AMPlitude%d %f" % (1, 0.0, 1, 0.0))
    #     self.handles["awg"].query("*OPC?")
    #
    #     self.handles["awg"].write("OUTPut%d:SERIESIMPedance %s" % (2, "50Ohm"))
    #     self.handles["awg"].write("DISPlay:UNIT:VOLT AMPLitudeoff")
    #     self.handles["awg"].write("SEQuence:ELEM1:OFFSET%d %f;AMPlitude%d %f" % (2, 0.0, 2, 0.0))
    #     self.handles["awg"].query("*OPC?")

    @property
    def channel(self):
        if "switch" in self.handles:
            p_chan, n_chan = 1, 2
            return self.handles["switch"].switch(p_chan)
        else:
            return 0

    @channel.setter
    def channel(self, channel):
        if "switch" in self.handles:
            p_chan, n_chan = 1, 2
            self.handles["switch"].set_switch(p_chan, channel)
            self.handles["switch"].set_switch(n_chan, channel)

    @property
    def _on(self):
        return bool(int(self.handles["awg"].query("OUTPut%d:STATe?" % (1,)))) and \
               bool(int(self.handles["awg"].query("OUTPut%d:STATe?" % (2,))))

    @_on.setter
    def _on(self, _on):
        self.handles["awg"].write("OUTPut%d:STATe %d" % (1, int(_on),))
        self.handles["awg"].write("OUTPut%d:STATe %d" % (2, int(_on),))

    @bounded_property
    def _a_p(self):
        return tf.pk(self._a_p_)

    @_a_p.setter
    def _a_p(self, _a_p):
        _a_p = _a_p.detach()
        _v = _a_p/2.*np.sqrt(50.)
        atol, rtol = self.info["v_s"].abs_tol, self.info["v_s"].rel_tol
        t_points = int(_a_p.shape[-2]*self._config["resample"])
        end = t_points + 16 - t_points % 16
        v_r_max, v_r_min = _v.real.max().item(), _v.real.min().item()
        iq = tf.iq(_v).numpy().reshape(-1)
        # iq = iq[::int(1/self._config["resample"])]  # Downsample only
        iq = interp1d(np.linspace(0, 1, Settings().t_points), iq, kind="linear")(np.linspace(0, 1, t_points)) # Upsample Only
        # iq = resample(iq, t_points)  # Upsample or Downsample
        iq.dtype = np.float  # Interleave IQ
        encoding = "<i2"  # Convert to little endian int16
        iq = np.round(iq * (32767 / np.max(np.abs(iq))))  # Scaling
        iq = iq.astype(encoding)
        i = np.zeros(end, dtype=encoding)
        q = np.zeros(end, dtype=encoding)
        i[0:t_points] = iq[0:2*t_points:2]
        q[0:t_points] = -iq[0:2 * t_points:2]

        # This prevents min and max from equal during scaling.
        if np.isclose(v_r_max, v_r_min, atol=atol, rtol=rtol):
            v_r_max = v_r_min + atol

        i_waveform = "_".join((self.__class__.__name__, "p"))
        i_bytes = '\r\n'.join(i.astype(str)).encode()
        n_bytes = str(len(i_bytes)).encode()
        prefix = str(len(n_bytes)).encode()
        self.handles["awg"].write('WLISt:WAVeform:DELete "%s"' % (i_waveform,))
        self.handles["awg"].write(r'MMEM:DOWN:FNAM "%s.txt"' % (i_waveform,))
        Ritptide.download_waveform_bug(self, b'MMEM:DOWN:DATA #' + prefix + n_bytes + i_bytes)
        self.handles["awg"].write('WLISt:WAVeform:IMPort "%s", "%s.txt", ANAlog' % (i_waveform, i_waveform))
        self.handles["awg"].write('SEQuence:ELEM1:WAVeform%d "%s"' % (1, i_waveform))

        q_waveform = "_".join((self.__class__.__name__, "n"))
        q_bytes = '\r\n'.join(q.astype(str)).encode()
        n_bytes = str(len(q_bytes)).encode()
        prefix = str(len(n_bytes)).encode()
        self.handles["awg"].write('WLISt:WAVeform:DELete "%s"' % (q_waveform,))
        self.handles["awg"].write(r'MMEM:DOWN:FNAM "%s.txt"' % (q_waveform,))
        Ritptide.download_waveform_bug(self, b'MMEM:DOWN:DATA #' + prefix + n_bytes + q_bytes)
        self.handles["awg"].write('WLISt:WAVeform:IMPort "%s", "%s.txt", ANAlog' % (q_waveform, q_waveform))
        self.handles["awg"].write('SEQuence:ELEM1:WAVeform%d "%s"' % (2, q_waveform))
        if end > t_points:
            v_r_max, v_r_min = max(0, v_r_max), min(0, v_r_min)
        self.handles["awg"].write("DISPlay:UNIT:VOLT HIGHlow")
        self.handles["awg"].write("SEQuence:ELEM1:VOLT:LOW%d %f;HIGH%d %f" % (1, +v_r_min, 1, +v_r_max))
        self.handles["awg"].write("SEQuence:ELEM1:VOLT:LOW%d %f;HIGH%d %f" % (2, -v_r_max, 2, -v_r_min))
        self.handles["awg"].query("*OPC?")
        self._a_p_[:, :] = _a_p

    @property
    def _delay(self):
        return self._delay_

    @_delay.setter
    def _delay(self, _delay):
        self._delay_ = _delay

    @property
    def _pulse_width(self):
        return self._pulse_width_

    @_pulse_width.setter
    def _pulse_width(self, _pulse_width):
        self._pulse_width_ = _pulse_width

    def arm(self):
        Ritptide.arm(self)

    def trigger(self):
        Ritptide.trigger(self)

    def measure(self):
        self.handles["awg"].write("AWGControl:STOP")


class RitptideModulatedIQ(base.NoRFSourceModulated):
    firmware_map = {}
    display_order = ["on", "initialized", "port", "freq", "a_p",
                     "delay", "pulse_width", "period",
                     "iq_files"]

    def __new__(self, error_model, port="9760", config_filename="",
                 resource_id='172.16.0.160'):
        self = super(RitptideModulatedIQ, cls).__new__(cls, error_model, port, config_filename)
        # Define object ATTRIBUTES
        self.resource_id = resource_id
        self.port = port
        return self

    def __getnewargs__(self):
        return tuple(list(super(RitptideModulatedIQ, self).__getnewargs__()) + [self.resource_id])

    def __init__(self, error_model, port="9760", config_filename="",
                 resource_id='172.16.0.160'):
        super().__init__(error_model, port, config_filename)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self._pulse_width = self.period
        self._delay = 0.0
        self.iq_files = self._iq_files_
        self._a_p = th.zeros_like(self._a_p_)
        self.initialized = True

    def __getstate__(self, state={}):
        state = super(RitptideModulatedIQ, self).__getstate__(state=state)
        return state

    def __setstate__(self, state, *args, **kwargs):
        super().__setstate__(state)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self._pulse_width = state["_pulse_width"]
        self._delay = state["_delay"]
        self.iq_files = state["iq_files"]
        self._a_p = self._a_p_
        self.initialized = True

    def __info__(self):
        super(RitptideModulatedIQ, self).__info__()
        rtol = 1/2**16
        v_atol = 1e-3
        a_atol = v_atol/np.sqrt(50.)
        v_max = 2*(self._config["voltage_limit"] - v_atol)
        a_max = v_max/np.sqrt(50.)
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["resource_id"] = Info("resource_id", read=True, write=True, check=False)
        self.info["_a_p"] = Info("_a_p", read=False, write=False, check=False,
                                 min_=a_atol, max_=a_max, abs_tol=a_atol, rel_tol=rtol)
        self.info["a_p"].min, self.info["a_p"].max = a_atol, a_max
        self.info["a_p"].abs_tol, self.info["a_p"].rel_tol = a_atol, rtol
        self.info["v_s"].min, self.info["v_s"].max = v_atol, v_max
        self.info["v_s"].abs_tol, self.info["v_s"].rel_tol = v_atol, rtol

    def connect_handles(self):
        rm = visa.ResourceManager(os.environ["VISA_LIB"])
        self.handles["awg"] = rm.open_resource(self.resource_id)
        super(RitptideModulatedIQ, self).connect_handles()

    def preset(self):
        super(RitptideModulatedIQ, self).preset()
        if self.unique_handle(self.handles['awg']):
            Ritptide.preset(self)

        t_points = self._a_p_.shape[-2]
        end = t_points + 16 - t_points % 16
        bytes = ('0\r\n'*end).encode()  # todo: correct this
        n_bytes = str(len(bytes)).encode()
        prefix = str(len(n_bytes)).encode()

        waveform = "_".join((self.__class__.__name__, "i"))
        self.handles["awg"].write(r'MMEM:DOWN:FNAM "%s.txt"' % (waveform,))
        Ritptide.download_waveform_bug(self, b'MMEM:DOWN:DATA #' + prefix + n_bytes + bytes)
        self.handles["awg"].query("*OPC?")
        self.handles["awg"].write('WLISt:WAVeform:IMPort "%s", "%s.txt", ANAlog' % (waveform, waveform))
        self.handles["awg"].query("*OPC?")

        waveform = "_".join((self.__class__.__name__, "q"))
        self.handles["awg"].write(r'MMEM:DOWN:FNAM "%s.txt"' % (waveform,))
        Ritptide.download_waveform_bug(self, b'MMEM:DOWN:DATA #' + prefix + n_bytes + bytes)
        self.handles["awg"].query("*OPC?")
        self.handles["awg"].write('WLISt:WAVeform:IMPort "%s", "%s.txt", ANAlog' % (waveform, waveform))
        self.handles["awg"].query("*OPC?")

        self.handles["awg"].write("OUTPut%d:SERIESIMPedance %s" % (1, "50Ohm"))
        self.handles["awg"].write("DISPlay:UNIT:VOLT AMPLitudeoff")
        self.handles["awg"].write("SEQuence:ELEM1:OFFSET%d %f;AMPlitude%d %f" % (1, 0.0, 1, 0.0))
        self.handles["awg"].query("*OPC?")

        self.handles["awg"].write("OUTPut%d:SERIESIMPedance %s" % (2, "50Ohm"))
        self.handles["awg"].write("DISPlay:UNIT:VOLT AMPLitudeoff")
        self.handles["awg"].write("SEQuence:ELEM1:OFFSET%d %f;AMPlitude%d %f" % (2, 0.0, 2, 0.0))
        self.handles["awg"].query("*OPC?")

    @property
    def _on(self):
        return bool(int(self.handles["awg"].query("OUTPut%d:STATe?" % (1,)))) and \
               bool(int(self.handles["awg"].query("OUTPut%d:STATe?" % (2,))))

    @_on.setter
    def _on(self, _on):
        self.handles["awg"].write("OUTPut%d:STATe %d" % (1, int(_on),))
        self.handles["awg"].write("OUTPut%d:STATe %d" % (2, int(_on),))

    @bounded_property
    def _a_p(self):
        return tf.pk(self._a_p_)

    @_a_p.setter
    def _a_p(self, _a_p):
        _a_p = _a_p.detach()
        _v = _a_p*np.sqrt(50.)
        atol, rtol = self.info["v_s"].abs_tol, self.info["v_s"].rel_tol
        t_points = int(self._a_p_.shape[-2]*self._config["resample"])
        end = t_points + 16 - t_points % 16
        v_r_max, v_r_min = _v.real.max().item(), _v.real.min().item()
        v_i_max, v_i_min = _v.imag.max().item(), _v.imag.min().item()
        iq = tf.iq(_v).numpy().reshape(-1)
        iq.dtype = np.float  # Interleave IQ
        iq = iq[::int(1/self._config["resample"])]
        encoding = "<i2"  # Convert to little endian int16
        iq = np.round(iq * (32767 / np.max(np.abs(iq))))  # Scaling
        iq = iq.astype(encoding)
        i = np.zeros(end, dtype=encoding)
        q = np.zeros(end, dtype=encoding)
        i[0:t_points] = iq[0:2*t_points:2]
        q[0:t_points] = iq[1:2 * t_points + 1:2]

        # This prevents min and max from equal during scaling.
        if np.isclose(v_r_max, v_r_min, atol=atol, rtol=rtol):
            v_r_max = v_r_min + atol
        if np.isclose(v_i_max, v_i_min, atol=atol, rtol=rtol):
            v_i_max = v_i_min + atol

        i_waveform = "_".join((self.__class__.__name__, "i"))
        i_bytes = '\r\n'.join(i.astype(str)).encode()
        n_bytes = str(len(i_bytes)).encode()
        prefix = str(len(n_bytes)).encode()
        self.handles["awg"].write('WLISt:WAVeform:DELete "%s"' % (i_waveform,))
        self.handles["awg"].write(r'MMEM:DOWN:FNAM "%s.txt"' % (i_waveform,))
        Ritptide.download_waveform_bug(self, b'MMEM:DOWN:DATA #' + prefix + n_bytes + i_bytes)
        self.handles["awg"].write('WLISt:WAVeform:IMPort "%s", "%s.txt", ANAlog' % (i_waveform, i_waveform))
        self.handles["awg"].write('SEQuence:ELEM1:WAVeform%d "%s"' % (1, i_waveform))

        q_waveform = "_".join((self.__class__.__name__, "q"))
        q_bytes = '\r\n'.join(q.astype(str)).encode()
        n_bytes = str(len(q_bytes)).encode()
        prefix = str(len(n_bytes)).encode()
        self.handles["awg"].write('WLISt:WAVeform:DELete "%s"' % (q_waveform,))
        self.handles["awg"].write(r'MMEM:DOWN:FNAM "%s.txt"' % (q_waveform,))
        Ritptide.download_waveform_bug(self, b'MMEM:DOWN:DATA #' + prefix + n_bytes + q_bytes)
        self.handles["awg"].write('WLISt:WAVeform:IMPort "%s", "%s.txt", ANAlog' % (q_waveform, q_waveform))
        self.handles["awg"].write('SEQuence:ELEM1:WAVeform%d "%s"' % (2, q_waveform))

        if end > t_points:
            v_r_max, v_r_min = max(0, v_r_max), min(0, v_r_min)
            v_i_max, v_i_min = max(0, v_i_max), min(0, v_i_min)
        self.handles["awg"].write("DISPlay:UNIT:VOLT HIGHlow")
        self.handles["awg"].write("SEQuence:ELEM1:VOLT:LOW%d %f;HIGH%d %f" % (1, v_r_min, 1, v_r_max))
        self.handles["awg"].write("SEQuence:ELEM1:VOLT:LOW%d %f;HIGH%d %f" % (2, v_i_min, 2, v_i_max))
        self.handles["awg"].query("*OPC?")
        self._a_p_[:, :] = _a_p

    @property
    def _delay(self):
        return self._delay_

    @_delay.setter
    def _delay(self, _delay):
        self._delay_ = _delay

    @property
    def _pulse_width(self):
        return self._pulse_width_

    @_pulse_width.setter
    def _pulse_width(self, _pulse_width):
        self._pulse_width_ = _pulse_width

    def arm(self):
        Ritptide.arm(self)

    def trigger(self):
        Ritptide.trigger(self)

    def measure(self):
        self.handles["awg"].write("AWGControl:STOP")
