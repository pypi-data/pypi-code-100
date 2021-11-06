import os
import logging

import numpy as np
import torch as th
import pyvisa as visa
from scipy.signal import resample

from sknrf.device.signal import tf
from sknrf.device.base import device_logger
from sknrf.device.instrument.rfsource import base
from sknrf.device.instrument.shared.sg import KeysightPSG8xxxx
from sknrf.settings import Settings
from sknrf.app.dataviewer.model.dataset import IQFile
from sknrf.utilities.numeric import Scale, Info, bounded_property, PkAvg, Format
from sknrf.utilities.rf import rW2dBm, dBm2rW, dBU2rU


logger = device_logger(logging.getLogger(__name__))

__author__ = 'dtbespal'


class KeysightPSGE8xxxxCW(base.NoRFSource):
    firmware_map = {}
    display_order = ["on", "initialized", "freq", "a_p", "v_s",
                     "num_harmonics", "harmonics"]

    def __new__(cls, error_model, port, config_filename="",
                resource_id="TCPIP0::10.0.0.60::inst0::INSTR"):
        self = super(KeysightPSGE8xxxxCW, cls).__new__(cls, error_model, port, config_filename)
        # Define object ATTRIBUTES
        self.resource_id = resource_id
        return self

    def __getnewargs__(self):
        return tuple(list(super(KeysightPSGE8xxxxCW, self).__getnewargs__()) + [self.resource_id])

    def __init__(self, error_model, port, config_filename="",
                 resource_id="TCPIP0::10.0.0.60::inst0::INSTR"):
        super().__init__(error_model, port, config_filename)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self._a_p = dBm2rW(-130.00)*th.ones_like(self._a_p_)
        self.initialized = True

    def __getstate__(self, state={}):
        state = super(KeysightPSGE8xxxxCW, self).__getstate__(state=state)
        return state

    def __setstate__(self, state, *args, **kwargs):
        super().__setstate__(state)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self._a_p = self._a_p_
        self.initialized = True

    def __info__(self):
        super(KeysightPSGE8xxxxCW, self).__info__()
        abs_tol = dBm2rW(-130.00) - dBm2rW(-130.01)
        rel_tol = dBU2rU(0.01) - 1
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["resource_id"] = Info("resource_id", read=False, write=True, check=False)
        self.info["_a_p"] = Info("_a_p", read=False, write=False, check=False,
                                 min_=dBm2rW(-130), max_=dBm2rW(0.0), abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["a_p"].min, self.info["a_p"].max = dBm2rW(-130), dBm2rW(45)
        self.info["v_s"].min, self.info["v_s"].max = dBm2rW(-130), dBm2rW(45)
        self.info["_f0"] = Info("_f0", read=False, write=False, check=False, min_=250e3,
                                format_=Format.RE, scale=Scale.G, unit="Hz")

    def connect_handles(self):
        rm = visa.ResourceManager()
        self.handles["sg"] = rm.open_resource(self.resource_id)
        super(KeysightPSGE8xxxxCW, self).connect_handles()

    def preset(self):
        super(KeysightPSGE8xxxxCW, self).preset()
        if self.unique_handle(self.handles["sg"]):
            KeysightPSG8xxxx.preset(self)
        iq_file = IQFile(os.sep.join((Settings().data_root, 'signals', 'CW.h5')), mode='r')
        _, self._header_map, _ = iq_file.to_waveform()
        self._header_map["sample_rate"] = self._config["upsample_factor"]/Settings().t_step

    @property
    def _on(self):
        return bool(int(self.handles["sg"].query(":OUTPut:STATe?")))

    @_on.setter
    def _on(self, _on):
        if _on:
            self.handles["sg"].write(":OUTPut:STATe %d" % (int(_on),))
            self.handles["sg"].write(":OUTPut:MOD %d" % (int(_on),))
        else:
            self.handles["sg"].write(":OUTPut:MOD %d" % (int(_on),))
            self.handles["sg"].write(":OUTPut:STATe %d" % (int(_on),))

    @bounded_property
    def _a_p(self):
        pk = dBm2rW(float(self.handles["sg"].query(":POW:LEVel:IMMediate:AMPLitude?")))
        self._a_p_[:, :] = self._a_p_.set_pk(pk)
        return self._a_p_

    @_a_p.setter
    def _a_p(self, _a_p):
        _a_p._rms = True
        pk = tf.pk(_a_p).reshape(-1, 1)

        t_points = _a_p.shape[-2]
        num_reps = int(np.ceil(60/t_points))
        iq = tf.iq(_a_p)
        iq.dtype = np.float  # Interleave IQ
        iq = np.round(iq * (32767 / np.max(np.abs(iq))))  # Scaling
        iq = iq.astype(">i2")  # Convert to big endian uint16.
        iq = np.tile(iq, (num_reps,))  # Minimum 60 samples
        marker = np.zeros((t_points,), dtype=">i1")
        marker_index = 2 - 1  # TRIGGER OUT
        marker[0:1] |= np.left_shift(1, marker_index)
        marker_index = 1 - 1  # Pulse ON
        marker[0:1] |= np.left_shift(1, marker_index)
        marker = np.tile(marker, (num_reps,))  # Minimum 60 samples

        self.handles["sg"].write(":SOURce:RADio:ARB:STATe 0")  # Turn Off ARB

        # Configure Modulation
        self.handles["sg"].write(":MEM:DELete:BINary")
        n_bytes = str(iq.nbytes).encode()
        prefix = str(len(n_bytes)).encode()
        self.handles["sg"].write_raw(b':MEM:DATA:UNPRotected "/user/bbg1/waveform/CW",#' + prefix + n_bytes + iq.tobytes())
        n_bytes = str(marker.nbytes).encode()
        prefix = str(len(n_bytes)).encode()
        self.handles["sg"].write_raw(b':MEM:DATA:UNPRotected "/user/bbg1/markers/CW",#' + prefix + n_bytes + marker.tobytes())

        # Configure Header
        # header = self.handles["sg"].query_binary_values(':MEM:DATA? "/user/bbg1/header/CW"', datatype='s')[0]
        self.handles["sg"].write(':SOURce:RADio:ARB:SCLock:RATE %d' % (self._header_map["sample_rate"],))
        self.handles["sg"].write(':SOURce:RADio:ARB:SCALing "/user/bbg1/waveform/CW", %d' % (self._header_map["waveform_runtime_scaling"]*100,))
        self.handles["sg"].write(':SOURce:RADio:ARB:IQ:MODulation:FILTer %s' % (self._header_map["iq_modulation_filter"],))
        self.handles["sg"].write(':SOURce:RADio:ARB:IQ:EXTernal:FILTer %s' % (self._header_map["iq_output_filter"],))
        self.handles["sg"].write(':SOURce:POWer:ALC:SEARch:REFerence %s' % (self._header_map["power_search_reference"][0:3],))
        auto_bandwidth = self._header_map["bandwidth"].lower() == "auto"
        self.handles["sg"].write(':SOURce:POWer:ALC:BANDwidth:AUTO %d' % (int(auto_bandwidth),))
        if not auto_bandwidth:
            self.handles["sg"].write(':SOURce:POWer:ALC:BANDwidth %d' % int(self._header_map["bandwidth"],))
        self.handles["sg"].write(':SOURce:POWer:ALC:STATe %s' % (self._header_map["alc_status"],))

        self.handles["sg"].write(':SOURce:RADio:ARB:WAVeform "/user/bbg1/waveform/CW"')
        self.handles["sg"].write(":SOURce:RADio:ARB:STATe 1")  # Turn On ARB

        # Configure Power
        self.handles["sg"].write(":SOURce:POW:LEVel:IMMediate:AMPLitude %.2fDBM" % (rW2dBm(max(np.abs(pk[0, 0]), self.info["_a_p"].abs_tol)),))
        self._a_p_[:, :] = _a_p

    @bounded_property
    def _f0(self):
        return float(self.handles["sg"].query(":SOURce:FREQuency:FIXed?"))

    @_f0.setter
    def _f0(self, f0):
        self.handles["sg"].write(":SOURce:FREQuency:MODE FIXed")  # Fixed Frequency
        self.handles["sg"].write(":SOURce:FREQuency:FIXed %d" % (int(f0),))  # Center Frequency
        self.handles["sg"].query("*OPC?")

    def arm(self):
        KeysightPSG8xxxx.arm(self)

    def trigger(self):
        KeysightPSG8xxxx.trigger(self)


class KeysightPSGE8xxxxPulsed(base.NoRFSourcePulsed):
    firmware_map = {}
    display_order = ["on", "initialized", "freq", "a_p", "v_s",
                     "delay", "pulse_width",
                     "num_harmonics", "harmonics"]

    def __new__(cls, error_model, port, config_filename="",
                resource_id="TCPIP0::10.0.0.60::inst0::INSTR"):
        self = super(KeysightPSGE8xxxxPulsed, cls).__new__(cls, error_model, port, config_filename)
        # Define object ATTRIBUTES
        self.resource_id = resource_id
        return self

    def __getnewargs__(self):
        return tuple(list(super(KeysightPSGE8xxxxPulsed, self).__getnewargs__()) + [self.resource_id])

    def __init__(self, error_model, port, config_filename="",
                 resource_id="TCPIP0::10.0.0.60::inst0::INSTR"):
        super().__init__(error_model, port, config_filename)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self._pulse_width = self.period
        self._delay = 0.0
        self._a_p = dBm2rW(-130.00)*th.ones_like(self._a_p_)
        self.initialized = True

    def __getstate__(self, state={}):
        state = super(KeysightPSGE8xxxxPulsed, self).__getstate__(state=state)
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
        self._a_p = self._a_p_
        self.initialized = True

    def __info__(self):
        super(KeysightPSGE8xxxxPulsed, self).__info__()
        abs_tol = dBm2rW(-130.00) - dBm2rW(-130.01)
        rel_tol = dBU2rU(0.01) - 1
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["resource_id"] = Info("resource_id", read=False, write=True, check=False)
        self.info["_a_p"] = Info("_a_p", read=False, write=False, check=False,
                                 min_=dBm2rW(-130), max_=dBm2rW(0.0), abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["a_p"].min, self.info["a_p"].max = dBm2rW(-130), dBm2rW(45)
        self.info["v_s"].min, self.info["v_s"].max = dBm2rW(-130), dBm2rW(45)
        self.info["_f0"] = Info("_f0", read=False, write=False, check=False, min_=250e3,
                                format_=Format.RE, scale=Scale.G, unit="Hz")

    def connect_handles(self):
        rm = visa.ResourceManager()
        self.handles["sg"] = rm.open_resource(self.resource_id)
        super(KeysightPSGE8xxxxPulsed, self).connect_handles()

    def preset(self):
        super(KeysightPSGE8xxxxPulsed, self).preset()
        if self.unique_handle(self.handles["sg"]):
            KeysightPSG8xxxx.preset(self)
        iq_file = IQFile(os.sep.join((Settings().data_root, 'signals', 'CW.h5')), mode='r')
        _, self._header_map, _ = iq_file.to_waveform()
        self._header_map["sample_rate"] = self._config["upsample_factor"]/Settings().t_step
        self._header_map["alc_status"] = "Off"

    @property
    def _on(self):
        return bool(int(self.handles["sg"].query(":OUTPut:STATe?")))

    @_on.setter
    def _on(self, _on):
        if _on:
            self.handles["sg"].write(":OUTPut:STATe %d" % (int(_on),))
            self.handles["sg"].write(":OUTPut:MOD %d" % (int(_on),))
        else:
            self.handles["sg"].write(":OUTPut:MOD %d" % (int(_on),))
            self.handles["sg"].write(":OUTPut:STATe %d" % (int(_on),))

    @bounded_property
    def _a_p(self):
        pk = dBm2rW(float(self.handles["sg"].query(":POW:LEVel:IMMediate:AMPLitude?")))
        self._a_p_[:, :] = self._a_p_.set_pk(pk)
        return self._a_p_

    @_a_p.setter
    def _a_p(self, _a_p):
        _a_p._rms = True
        pk = tf.pk(_a_p).reshape(-1, 1)

        t_points = _a_p.shape[-2]
        num_reps = int(np.ceil(60 / t_points))
        iq = tf.iq(_a_p)
        iq.dtype = np.float  # Interleave IQ
        iq = np.round(iq * (32767 / np.max(np.abs(iq))))  # Scaling
        iq = iq.astype(">i2")  # Convert to big endian uint16.
        iq = np.tile(iq, (num_reps,))  # Minimum 60 samples
        marker = np.zeros((t_points,), dtype=">i1")
        marker_index = 2 - 1  # TRIGGER OUT
        marker[0:1] |= np.left_shift(1, marker_index)
        marker_index = 1 - 1  # Pulse ON
        marker[0:1] |= np.left_shift(1, marker_index)
        marker_index = self._header_map["pulse__rf_blanking"] - 1
        marker |= np.left_shift(1, marker_index)
        marker = np.tile(marker, (num_reps,))  # Minimum 60 samples

        self.handles["sg"].write(":SOURce:RADio:ARB:STATe 0")  # Turn Off ARB

        # Configure Modulation
        self.handles["sg"].write(":MEM:DELete:BINary")
        n_bytes = str(iq.nbytes).encode()
        prefix = str(len(n_bytes)).encode()
        self.handles["sg"].write_raw(b':MEM:DATA:UNPRotected "/user/bbg1/waveform/PULSED",#' + prefix + n_bytes + iq.tobytes())
        n_bytes = str(marker.nbytes).encode()
        prefix = str(len(n_bytes)).encode()
        self.handles["sg"].write_raw(b':MEM:DATA:UNPRotected "/user/bbg1/markers/PULSED",#' + prefix + n_bytes + marker.tobytes())

        # Configure Header
        # header = self.handles["sg"].query_binary_values(':MEM:DATA? "/user/bbg1/header/PULSED"', datatype='s')[0]
        self.handles["sg"].write(':SOURce:RADio:ARB:SCLock:RATE %d' % (self._header_map["sample_rate"],))
        self.handles["sg"].write(':SOURce:RADio:ARB:SCALing "/user/bbg1/waveform/PULSED", %d' % (
        self._header_map["waveform_runtime_scaling"] * 100,))
        self.handles["sg"].write(':SOURce:RADio:ARB:IQ:MODulation:FILTer %s' % (self._header_map["iq_modulation_filter"],))
        self.handles["sg"].write(':SOURce:RADio:ARB:IQ:EXTernal:FILTer %s' % (self._header_map["iq_output_filter"],))
        self.handles["sg"].write(':SOURce:POWer:ALC:SEARch:REFerence %s' % (self._header_map["power_search_reference"][0:3],))
        auto_bandwidth = self._header_map["bandwidth"].lower() == "auto"
        self.handles["sg"].write(':SOURce:POWer:ALC:BANDwidth:AUTO %d' % (int(auto_bandwidth),))
        if not auto_bandwidth:
            self.handles["sg"].write(':SOURce:POWer:ALC:BANDwidth %d' % int(self._header_map["bandwidth"], ))
        self.handles["sg"].write(':SOURce:POWer:ALC:STATe %s' % (self._header_map["alc_status"],))

        self.handles["sg"].write(':SOURce:RADio:ARB:WAVeform "/user/bbg1/waveform/PULSED"')
        self.handles["sg"].write(":SOURce:RADio:ARB:STATe 1")  # Turn On ARB

        # Configure Power
        self.handles["sg"].write(":SOURce:POW:LEVel:IMMediate:AMPLitude %.2fDBM" % (rW2dBm(max(np.abs(pk[0, 0]), self.info["_a_p"].abs_tol)),))
        self._a_p_[:, :] = _a_p

    @bounded_property
    def _f0(self):
        return float(self.handles["sg"].query(":SOURce:FREQuency:FIXed?"))

    @_f0.setter
    def _f0(self, f0):
        self.handles["sg"].write(":SOURce:FREQuency:MODE FIXed")  # Fixed Frequency
        self.handles["sg"].write(":SOURce:FREQuency:FIXed %d" % (int(f0),))  # Center Frequency
        self.handles["sg"].query("*OPC?")

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
        KeysightPSG8xxxx.arm(self)

    def trigger(self):
        KeysightPSG8xxxx.trigger(self)


class KeysightPSGE8xxxxModulated(base.NoRFSourceModulated):
    firmware_map = {}
    display_order = ["on", "initialized", "freq", "a_p", "v_s",
                     "delay", "pulse_width",
                     "iq_files",
                     "num_harmonics", "harmonics"]

    def __new__(cls, error_model, port, config_filename="",
                resource_id="TCPIP0::10.0.0.60::inst0::INSTR"):
        self = super(KeysightPSGE8xxxxModulated, cls).__new__(cls, error_model, port, config_filename)
        # Define object ATTRIBUTES
        self.resource_id = resource_id
        return self

    def __getnewargs__(self):
        return tuple(list(super(KeysightPSGE8xxxxModulated, self).__getnewargs__()) + [self.resource_id])

    def __init__(self, error_model, port, config_filename="",
                 resource_id="TCPIP0::10.0.0.60::inst0::INSTR"):
        super().__init__(error_model, port, config_filename)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self._on = False
        self._pulse_width = self.period
        self._delay = 0.0
        self.iq_files = self._iq_files_
        self._a_p = dBm2rW(-130.00)*th.ones_like(self._a_p_)
        self.initialized = True

    def __getstate__(self, state={}):
        state = super(KeysightPSGE8xxxxModulated, self).__getstate__(state=state)
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
        super(KeysightPSGE8xxxxModulated, self).__info__()
        abs_tol = dBm2rW(-130.00) - dBm2rW(-130.01)
        rel_tol = dBU2rU(0.01) - 1
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["resource_id"] = Info("resource_id", read=False, write=True, check=False)
        self.info["_a_p"] = Info("_a_p", read=False, write=False, check=False, pk_avg=PkAvg.AVG,
                                 min_=dBm2rW(-130), max_=dBm2rW(20.0), abs_tol=abs_tol, rel_tol=rel_tol)
        self.info["a_p"].min, self.info["a_p"].max = dBm2rW(-130), dBm2rW(45)
        self.info["a_p"].pk_avg = PkAvg.AVG
        self.info["v_s"].min, self.info["v_s"].max = dBm2rW(-130), dBm2rW(45)
        self.info["v_s"].pk_avg = PkAvg.AVG
        self.info["_f0"] = Info("_f0", read=False, write=False, check=False, min_=250e3,
                                format_=Format.RE, scale=Scale.G, unit="Hz")

    def connect_handles(self):
        rm = visa.ResourceManager()
        self.handles["sg"] = rm.open_resource(self.resource_id)
        super(KeysightPSGE8xxxxModulated, self).connect_handles()

    def preset(self):
        super(KeysightPSGE8xxxxModulated, self).preset()
        if self.unique_handle(self.handles["sg"]):
            KeysightPSG8xxxx.preset(self)

    @property
    def _on(self):
        return bool(int(self.handles["sg"].query(":OUTPut:STATe?")))

    @_on.setter
    def _on(self, _on):
        if _on:
            self.handles["sg"].write(":OUTPut:STATe %d" % (int(_on),))
            self.handles["sg"].write(":OUTPut:MOD %d" % (int(_on),))
        else:
            self.handles["sg"].write(":OUTPut:MOD %d" % (int(_on),))
            self.handles["sg"].write(":OUTPut:STATe %d" % (int(_on),))

    @bounded_property
    def _a_p(self):
        avg = dBm2rW(float(self.handles["sg"].query(":POW:LEVel:IMMediate:AMPLitude?")))
        self._a_p_[:, :] = self._a_p_.set_avg(avg)
        return self._a_p_

    @_a_p.setter
    def _a_p(self, _a_p):
        _a_p._rms = True
        avg = tf.avg(_a_p).reshape(-1, 1)
        harm_idx = 0

        t_points = _a_p.shape[-2]
        num_reps = int(np.ceil(60 / t_points))
        iq = tf.iq(_a_p)
        iq = resample(iq, self._config["upsample_factor"]*iq.size)
        iq.dtype = np.float  # Interleave IQ
        iq = np.round(iq * (32767/np.max(np.abs(iq))))  # Scaling
        iq = iq.astype(">i2")  # Convert to big endian uint16.
        iq = np.tile(iq, (num_reps,))  # Minimum 60 samples
        marker = self._markers_[harm_idx]
        marker_index = 2 - 1  # TRIGGER OUT
        marker[0:1] |= np.left_shift(1, marker_index)
        marker = np.tile(marker, (num_reps,))  # Minimum 60 samples
        header_map = self._header_maps_[harm_idx]

        self.handles["sg"].write(":SOURce:RADio:ARB:STATe 0")  # Turn Off ARB

        # Configure Modulation
        self.handles["sg"].write(":MEM:DELete:BINary")
        n_bytes = str(iq.nbytes).encode()
        prefix = str(len(n_bytes)).encode()
        self.handles["sg"].write_raw(b':MEM:DATA:UNPRotected "/user/bbg1/waveform/MODULATED",#' + prefix + n_bytes + iq.tobytes())
        n_bytes = str(marker.nbytes).encode()
        prefix = str(len(n_bytes)).encode()
        self.handles["sg"].write_raw(b':MEM:DATA:UNPRotected "/user/bbg1/markers/MODULATED",#' + prefix + n_bytes + marker.tobytes())

        # Configure Header
        header_map["alc_status"] = "Off"
        header_map["sample_rate"] = self._config["upsample_factor"]/Settings().t_step
        # header = self.handles["sg"].query_binary_values(':MEM:DATA? "/user/bbg1/header/MODULATED"', datatype='s')[0]
        self.handles["sg"].write(':SOURce:RADio:ARB:SCLock:RATE %d' % (header_map["sample_rate"],))
        self.handles["sg"].write(':SOURce:RADio:ARB:SCALing "/user/bbg1/waveform/MODULATED", %d' % (
            header_map["waveform_runtime_scaling"] * 100,))
        if not np.isnan(header_map["iq_modulation_filter"]):
            self.handles["sg"].write(':SOURce:RADio:ARB:IQ:MODulation:FILTer %s' % (header_map["iq_modulation_filter"],))
        if not np.isnan(header_map["iq_output_filter"]):
            self.handles["sg"].write(':SOURce:RADio:ARB:IQ:EXTernal:FILTer %s' % (header_map["iq_output_filter"],))
        self.handles["sg"].write(':SOURce:POWer:ALC:SEARch:REFerence %s' % (header_map["power_search_reference"][0:3],))
        auto_bandwidth = header_map["bandwidth"].lower() == "auto"
        self.handles["sg"].write(':SOURce:POWer:ALC:BANDwidth:AUTO %d' % (int(auto_bandwidth),))
        if not auto_bandwidth:
            self.handles["sg"].write(':SOURce:POWer:ALC:BANDwidth %d' % int(header_map["bandwidth"], ))
        alc_status = True if header_map["alc_status"] is True or header_map["alc_status"].lower() in("on", "true") else False
        self.handles["sg"].write(':SOURce:POWer:ALC:STATe %s' % (int(alc_status),))

        # Signal Rep
        rep = Settings().signal_rep
        rep = rep if rep > 0 else 1
        self.handles["sg"].write(':SOURce:RADio:ARB:SEQuence "/user/seq/MODULATED",'
                                 ' "/user/bbg1/waveform/MODULATED", %d' % (rep,))

        self.handles["sg"].write(':SOURce:RADio:ARB:WAVeform "/user/seq/MODULATED"')
        self.handles["sg"].write(":SOURce:RADio:ARB:STATe 1")  # Turn On ARB

        # Configure Power
        self.handles["sg"].write(":SOURce:POW:LEVel:IMMediate:AMPLitude %.2fDBM" % (rW2dBm(max(np.abs(avg[0, 0]), self.info["_a_p"].abs_tol)),))
        self._a_p_[:, :] = _a_p

    @bounded_property
    def _f0(self):
        return float(self.handles["sg"].query(":SOURce:FREQuency:FIXed?"))

    @_f0.setter
    def _f0(self, f0):
        self.handles["sg"].write(":SOURce:FREQuency:MODE FIXed")  # Fixed Frequency
        self.handles["sg"].write(":SOURce:FREQuency:FIXed %d" % (int(f0),))  # Center Frequency
        self.handles["sg"].query("*OPC?")

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
        KeysightPSG8xxxx.arm(self)

    def trigger(self):
        KeysightPSG8xxxx.trigger(self)

# HEADER Format
# header[17]                         The letter 'l'                        l = header[17].decode("utf-8")
# header[18:50]                      32-Character utf-8 description        description = header[18:50].decode("utf-8")
#
# header[50:52], header[109]         Sample Rate (Todo)
#
# header[58]                         Marker1 Polarity (1=Pos, 0=Neg)        m1_pol = bool(header[58])
# header[86]                         Marker1 Polarity??? (0=Pos, 1=Neg)
# header[59]                         Marker2 Polarity (1=Pos, 0=Neg)        m2_pol = bool(header[59])
# header[86]                         Marker2 Polarity??? (0=Pos, 2=Neg)
# header[60]                         Marker3 Polarity (1=Pos, 0=Neg)        m3_pol = bool(header[60])
# header[86]                         Marker3 Polarity??? (0=Pos, 4=Neg)
# header[61]                         Marker4 Polarity (1=Pos, 0=Neg)        m4_pol = bool(header[61])
# header[86]                         Marker4 Polarity??? (0=Pos, 8=Neg)
#
# header[62]                         ALC Routing Marker Number (1-4)        alc_routing = header[62]
# header[63]                         Alt. Ampl. Routing Marker Number(1-4)? alt_routing = header[63]
# header[64]                         RF Blank Routing Marker Number (1-4)   rf_blank_routing = header[64]
#
# header[128:32]                        I/Q Mod Filter (4-bytes)
#                                     - (Man=0b00000000..., Auto=0b11000000...)
#
#
# header[128:32]                        Mod Attenuation (4-bytes)
#                                     - (Man=0b00000000..., Auto=0b11000000...)
#
#
# Sample Point: (Length of the Waveform)
# Sample Rate (MHz): [:SOURce]:RADio:ARB:SCLock:RATE <sample_clock_rate> (in Hz)
# Waveform Runtime Scaling (%): [:SOURce]:RADio:ARB:SCALing "<file_name>",<val> (1-100)
# IQ Modulation Filter (MHz): [:SOURce]:RADio:ARB:IQ:MODulation:FILTer 40e6|THRough
# IQ Output Filter (MHz): [:SOURce]:RADio:ARB:IQ:EXTernal:FILTer 40e6|THRough
# Marker 1: [:SOURce]:RADio:ARB:MARKer:[SET]"<file_name>",<marker>,<first_point>,<last_point>,<skip_count>
# Marker 2: [:SOURce]:RADio:ARB:MARKer:[SET]"<file_name>",<marker>,<first_point>,<last_point>,<skip_count>
# Marker 3: [:SOURce]:RADio:ARB:MARKer:[SET]"<file_name>",<marker>,<first_point>,<last_point>,<skip_count>
# Marker 4: [:SOURce]:RADio:ARB:MARKer:[SET]"<file_name>",<marker>,<first_point>,<last_point>,<skip_count>
# Pulse/RF Blanking: [:SOURce]:RADio:ARB:MDEStination:PULSe NONE|M1|M2|M3|M4
# ALC Hold: [:SOURce]:RADio:ARB:MDEStination:ALCHold NONE|M1|M2|M3|M4
# Alt. Ampl. Routing: [:SOURce]:RADio:ARB:MDEStination:AAMPlitude NONE|M1|M2|M3|M4
# ALC Status: [:SOURce]:POWer:ALC[:STATe] ON|OFF|1|0
# Bandwidth: [:SOURce]:POWer:ALC:BANDwidth|BWIDth:AUTO ON|OFF|1|0,
# Power Search Reference: [:SOURce]:POWer:ALC:SEARch:REFerence Modulated, [:SOURce]:POWer:ALC:BANDwidth|BWIDth <num>[<freq_suffix>]
