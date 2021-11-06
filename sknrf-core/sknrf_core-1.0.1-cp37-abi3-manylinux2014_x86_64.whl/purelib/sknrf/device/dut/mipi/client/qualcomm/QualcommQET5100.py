import time

import numpy as np

from sknrf.device.dut.mipi.client.base import NoMIPIClient
from sknrf.enums.device import Response
from sknrf.settings import Settings
from sknrf.enums.mipi import MIPI_VIO_MODE, MIPI_WRITE_MODE
from sknrf.enums.modulation import TECH
from sknrf.enums.modulation import GSM_BAND, GSM_BW, GSM_RB
from sknrf.enums.modulation import CDMA_BAND, CDMA_BW, CDMA_RB
from sknrf.enums.modulation import WCDMA_BAND, WCDMA_BW, WCDMA_RB
from sknrf.enums.modulation import LTE_BAND, LTE_BW, LTE_RB
from sknrf.device.dut.mipi.client.qualcomm.base import ET_REG, ET_MOD_MODE
from sknrf.utilities.numeric import Info, Scale, PkAvg, Format, bounded_property


class QualcomQET5100(NoMIPIClient):
    signal_list = []
    transforms_list = []
    display_order = ["on", "usid", "tech", "et_mode", "band", "bw", "rb",
                     "et_v_min", "apt_v_max", "et_v_max", "et_gain", "et_offset", "et_cm"]

    def __new__(cls, error_model, num_ports, config_filename="",
                mipi=0, tech=TECH.LTE, band=LTE_BAND.B41, bw=LTE_BW.BW_5M, rb=LTE_RB.RB_17, et_mode=ET_MOD_MODE.SLEEP,
                **kwargs):
        self = super(QualcomQET5100, cls).__new__(cls, error_model, num_ports, config_filename="",
                                                  mipi=mipi, **kwargs)
        self._et_v_min = 0.0
        self._apt_v_max = 1.0
        self._et_v_max = 1.0
        self._arb2mod_gain = 0.0
        self._et_gain = 0.0
        self._et_offset = 0.0
        self._et_cm = 0.0

        self._port_name = ""
        self._tech = tech
        self._band = band
        self._bw = bw
        self._rb = rb
        self._et_mode = et_mode
        return self

    def __init__(self, error_model, num_ports, config_filename="",
                 mipi=0, tech=TECH.LTE, band=LTE_BAND.B41, bw=LTE_BW.BW_5M, rb=LTE_RB.RB_17, et_mode=ET_MOD_MODE.SLEEP,
                 **kwargs):
        super(QualcomQET5100, self).__init__(error_model, num_ports, config_filename="",
                                             mipi=mipi, **kwargs)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self.et_mode = et_mode
        self.initialized = True

    def __info__(self):
        super(QualcomQET5100, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["tech"] = Info("tech", read=True, write=False, check=False)
        self.info["band"] = Info("band", read=True, write=True, check=False)
        self.info["bw"] = Info("BW", read=True, write=True, check=False)
        self.info["rb"] = Info("RB", read=True, write=True, check=False)
        self.info["et_mode"] = Info("ET mode", read=True, write=True, check=False)
        config = self._config
        abs_tol, rel_tol = config["abs_tol"], 1e-5
        self.info["apt_v_max"] = Info("apt_v_max", read=True, write=True, check=True,
                                  format_=Format.RE, scale=Scale._, unit="V", pk_avg=PkAvg.PK,
                                  min_=0.0, max_=config["et_v_max"], abs_tol=abs_tol, rel_tol=abs_tol)
        self.info["et_v_max"] = Info("et_v_max", read=True, write=True, check=True,
                                      format_=Format.RE, scale=Scale._, unit="V", pk_avg=PkAvg.PK,
                                      min_=0.0, max_=config["et_v_max"], abs_tol=abs_tol, rel_tol=abs_tol)
        self.info["et_v_min"] = Info("et_v_min", read=True, write=True, check=True,
                                  format_=Format.RE, scale=Scale._, unit="V", pk_avg=PkAvg.PK,
                                  min_=config["et_v_min"], max_=config["et_v_max"], abs_tol=abs_tol, rel_tol=abs_tol)
        self.info["arb2mod_gain"] = Info("arb2mod gain", read=True, write=True, check=True,
                                         format_=Format.RE, scale=Scale._, unit=" ", pk_avg=PkAvg.PK,
                                         min_=0.0, max_=1, abs_tol=abs_tol, rel_tol=abs_tol)
        self.info["et_gain"] = Info("et gain", read=True, write=True, check=True,
                                    format_=Format.RE, scale=Scale._, unit=" ", pk_avg=PkAvg.PK,
                                    min_=1.0, max_=2*config["et_gain"], abs_tol=abs_tol, rel_tol=abs_tol)
        self.info["et_offset"] = Info("et offset", read=True, write=True, check=True,
                                      format_=Format.RE, scale=Scale._, unit="V", pk_avg=PkAvg.PK,
                                      min_=0.0, max_=6.24, abs_tol=abs_tol, rel_tol=abs_tol)
        self.info["et_cm"] = Info("et cm", read=True, write=True, check=True,
                                  format_=Format.RE, scale=Scale._, unit="V", pk_avg=PkAvg.PK,
                                  min_=0.0, max_=2.5, abs_tol=abs_tol, rel_tol=abs_tol)

    def connect_handles(self):
        pass

    def preset(self):
        if self.__class__ == QualcomQET5100:
            self._et_v_min = self._config["et_v_min"]
            self._apt_v_max = self._config["apt_v_max"]
            self._et_v_max = self._config["et_v_max"]
            self.usid = self._config["usid"]
            self.arb2mod_gain = self._config["arb2mod_gain"]
            self.et_gain = self._config["et_gain"]
            self.et_offset = self._config["et_offset"]
            self.et_cm = self._config["et_cm"]

            revision = self._server._read_basic(self.usid, ET_REG.REV_ID)
            # if revision != self._config["rev_id"]: raise IOError("Unable to verify ET Board revision")

            self.et_mode = ET_MOD_MODE.SLEEP


    @property
    def _on(self):
        return self._server.vio_mode.value > 0

    @_on.setter
    def _on(self, on):
        on = MIPI_VIO_MODE.ON if on > 0 else MIPI_VIO_MODE.OFF
        self._server.vio_mode = on

    @bounded_property
    def arb2mod_gain(self):
        return self._arb2mod_gain

    @arb2mod_gain.setter
    def arb2mod_gain(self, arb2mod_gain):
        self._arb2mod_gain = float(arb2mod_gain)

    @bounded_property
    def et_gain(self):
        return self._et_gain

    @et_gain.setter
    def et_gain(self, et_gain):
        self._et_gain = float(et_gain)

    @bounded_property
    def et_offset(self):
        return self._et_offset

    @et_offset.setter
    def et_offset(self, et_offset):
        self._et_offset = float(et_offset)

    @bounded_property
    def et_cm(self):
        return self._et_cm

    @et_cm.setter
    def et_cm(self, et_cm):
        self._et_cm = float(et_cm)

    @bounded_property
    def apt_v_max(self):
        return self._apt_v_max

    @apt_v_max.setter
    def apt_v_max(self, v):
        self._apt_v_max = np.maximum(float(v), self._et_v_min)
        self.prepare_all(self.usid)

    @bounded_property
    def et_v_max(self):
        return self._et_v_max

    @et_v_max.setter
    def et_v_max(self, v):
        self._et_v_max = np.maximum(float(v), self._et_v_min)
        self.prepare_all(self.usid)

    @bounded_property
    def et_v_min(self):
        abs_tol = self._config["abs_tol"]*1000
        offset = self._config["et_min_offset"] * 1000
        et_v_min = self._server._read_basic(self.usid, ET_REG.ET_VMIN)
        et_v_min &= 0x7F  # 255 QAM Flag
        et_v_min = (et_v_min*abs_tol + offset) / 1000
        return et_v_min

    @et_v_min.setter
    def et_v_min(self, v):
        self._et_v_min = float(np.minimum(v, self._et_v_max))
        self.prepare_all(self.usid)

    @property
    def tech(self):
        return self._tech

    @tech.setter
    def tech(self, tech):
        self._tech = tech
        self.prepare_all(self.usid)

    @property
    def band(self):
        return self._band

    @band.setter
    def band(self, band):
        self._band = band
        self.prepare_all(self.usid)

    @property
    def bw(self):
        return self._bw

    @bw.setter
    def bw(self, bw):
        self._bw = bw
        self.prepare_all(self.usid)

    @property
    def rb(self):
        return self._rb

    @rb.setter
    def rb(self, rb):
        self._rb = rb
        self.prepare_all(self.usid)

    @property
    def et_mode(self):
        if not self._on or not self.initialized:
            return self._et_mode
        else:
            et_reg = self._server._read_basic(self.usid, ET_REG.MODE_CTRL)
            if et_reg == 2 or et_reg == 3:
                return ET_MOD_MODE.APT
            elif et_reg == 4:
                return ET_MOD_MODE.ET
            else:
                return ET_MOD_MODE(et_reg)

    @et_mode.setter
    def et_mode(self, et_mode):
        et_mode = ET_MOD_MODE(et_mode.value)
        self.prepare_all(self.usid, mode=et_mode)
        self._et_mode = et_mode

    def _set_v_max(self, data, mode):
        abs_tol = self._config["abs_tol"]*1000
        min_, max_ = 0, (2**8 - 1)*abs_tol
        if mode == ET_MOD_MODE.APT:
            #  vmax: 8-bit value rounded to nearest int
            v_max = np.uint8(np.round(np.real(np.maximum(np.minimum(self._apt_v_max*1000, max_), min_)/abs_tol)))
            self._apt_v_max = v_max*self._config["abs_tol"]
        elif mode == ET_MOD_MODE.ET:
            #  vmax: 8-bit value rounded up
            v_max = np.uint8(np.ceil(np.real(np.maximum(np.minimum(self._et_v_max * 1000, max_), min_) / abs_tol)))
            self._et_v_max = v_max * self._config["abs_tol"]
        else:
            return
        data[data[:, 1] == ET_REG.APT_VREG_VMAX, 2] = v_max

    def _set_v_min(self, data):
        #  vin: 6-bit value rounded down with offset
        #  Bit 7 Reserved for 256QAM modulation flag.
        abs_tol = self._config["abs_tol"] * 1000
        offset = self._config["et_min_offset"]*1000  # 690 mV = 0x00
        min_, max_ = offset, (2**6 - 1)*abs_tol + offset
        et_v_min = np.uint8(np.floor(np.real((np.maximum(np.minimum(self._et_v_min * 1000, max_), min_) - offset) / abs_tol)))
        self._et_v_min = et_v_min * self._config["abs_tol"] + self._config["et_min_offset"]
        data[data[:, 1] == ET_REG.ET_VMIN, 2] = et_v_min | np.uint8(self._config["qam_256"]) << 7

    def prepare_all(self, usid, mode=None):
        tech, band, bw, rb = self._tech, self._band, self._bw, self._rb
        et_mode = self._et_mode if mode is None else mode
        tech_name, band_name = tech.name.lower(), band.name.lower()
        bw_name, rb_name, mode_name = bw.name.lower(), rb.name.lower(), et_mode.name.lower()
        if et_mode == ET_MOD_MODE.SLEEP:
            self._port_name = ""
            data = self._config["sleep"]
        elif et_mode == ET_MOD_MODE.STANDBY:
            self._port_name = ""
            data = self._config["standby"]
        elif et_mode == ET_MOD_MODE.APT:
            if self._et_mode is not et_mode:
                self.et_mode = ET_MOD_MODE.STANDBY
            cmap = self._config[tech_name][mode_name][band_name][bw_name][rb_name]
            self._port_name = cmap["port_name"]
            data = np.asarray(cmap["tx_enable"] + cmap["tx_on"])
            if tech == TECH.LTE:
                self._set_v_max(data, et_mode)
            elif tech == TECH.WCDMA:
                self._set_v_max(data, et_mode)
            elif tech == TECH.CDMA:
                self._set_v_max(data, et_mode)
            elif tech == TECH.GSM:
                self._set_v_max(data, et_mode)
            else:
                raise ValueError("Unsupported TECH: %s" % tech_name)
            if self._et_mode is not et_mode:
                data = np.concatenate((np.asarray(self._config["power_up"] + self._config["wake_up"]), data), axis=0)
        elif et_mode == ET_MOD_MODE.ET:
            if self._et_mode is not et_mode:
                self.et_mode = ET_MOD_MODE.STANDBY
            cmap = self._config[tech_name][mode_name][band_name][bw_name][rb_name]
            self._port_name = cmap["port_name"]
            data = np.asarray(cmap["tx_enable"] + cmap["tx_on"])
            if tech == TECH.LTE:
                self._set_v_max(data, et_mode)
                self._set_v_min(data)
            elif tech == TECH.WCDMA:
                self._set_v_max(data, et_mode)
                self._set_v_min(data)
            elif tech == TECH.CDMA:
                self._set_v_max(data, et_mode)
                self._set_v_min(data)
            elif tech == TECH.GSM:
                self._set_v_max(data, et_mode)
                self._set_v_min(data)
            else:
                raise ValueError("Unsupported TECH: %s" % tech_name)
            if self._et_mode is not et_mode:
                data = np.concatenate((np.asarray(self._config["power_up"] + self._config["wake_up"]), data), axis=0)
        else:
            raise ValueError("Unsupported ET_MOD_MODE: %s" % mode_name)
        self.write_all(self.usid, data)

    def write_all(self, usid, data):
        # self.validata_all(usid, data)
        for code in data:
            write_mode, address, data = code
            write_mode = MIPI_WRITE_MODE(write_mode)
            if write_mode == MIPI_WRITE_MODE.REG0:
                self._server._write_register0(usid, address, data)
            if write_mode == MIPI_WRITE_MODE.BASIC:
                self._server._write_basic(usid, address, data)
            elif write_mode == MIPI_WRITE_MODE.EXTENDED:
                self._server._write_extended(usid, address, data)
            elif write_mode == MIPI_WRITE_MODE.EXTENDED_LONG:
                self._server._write_extended_long(usid, address, data)
            elif write_mode == MIPI_WRITE_MODE.DELAY:
                time.sleep(data*1e-6)
            else:
                raise ValueError("Unsupported write mode")

    def validata_all(self, usid, data):
        import os
        import csv
        import matlab.engine
        from numpy import testing as nptest

        port_name, tech_name, mode_name = self._port_name, self._tech.name, self._et_mode.name
        band_name, bw_name, rb_name = self._band.name, self._bw.name, self._rb.name
        config_dirname = os.path.dirname(self.config_filename)
        matlab_dirname = r"C:\ETTS_TCF"
        eng = matlab.engine.connect_matlab()
        if len(port_name) == 0:
            return
        py_codes = data
        with open(os.sep.join((config_dirname, "mipi.csv")), "at") as f:
            for code in py_codes:
                if code[0] == 5:  # Delay
                    f.write('0x%08x, 0x%08x, %010d\n' % (code[0], code[1], code[2]))
                else:
                    f.write('0x%08x, 0x%08x, 0x%08x\n' % (code[0], code[1], code[2]))
        with open(os.sep.join((matlab_dirname, "mipi_config.csv")), "wt") as f:
            f.write('%s, %s, %s, %s, %s, nRB%s\n' %
                    (port_name.upper(), tech_name.upper(), mode_name.upper(),
                     band_name.upper(), bw_name[3:].upper(), rb_name[3:].upper()))

        with open(os.sep.join((config_dirname, "mipi.csv")), 'rt') as f:
            py_codes = np.asarray(list(csv.reader(f)))
        eng.validate_mipi(nargout=0)
        with open(os.sep.join((matlab_dirname, "mipi.csv")), 'rt') as f:
            mat_codes = np.asarray(list(csv.reader(f)))
        try:
            nptest.assert_equal(py_codes[:, 2], mat_codes[:, 2])
        except AssertionError:
            print("Data Mismatch: %s_%s_%s_%s_%s" % (tech_name, mode_name, band_name, bw_name, rb_name))
        try:
            nptest.assert_equal(py_codes[:, 1], mat_codes[:, 1])
        except AssertionError:
            print("Address Mismatch: %s_%s_%s_%s_%s" % (tech_name, mode_name, band_name, bw_name, rb_name))
        try:
            nptest.assert_equal(py_codes[:, 0], mat_codes[:, 0])
        except AssertionError:
            print("Write Type Mismatch: %s_%s_%s_%s_%s" % (tech_name, mode_name, band_name, bw_name, rb_name))


if __name__ == "__main__":
    import os
    csv_directory = r"C:\ETTS_TCF\rffe-scripts\modulator\QET5100\1.0"
    config_filename = os.sep.join((Settings().data_root, "config", "device", "dut", "mipi", "et", "qet5100_3"))
    QualcomQET5100.from_csv(config_filename, csv_directory)


