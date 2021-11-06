import numpy as np
import pyvisa as visa
from pyvisa.errors import VisaIOError

from sknrf.device.dut.mipi.server.base import NoMIPIServer
from sknrf.enums.device import Response
from sknrf.enums.mipi import MIPI_VIO_MODE, MIPI_READ_MODE, MIPI_WRITE_MODE

READ_OR_MASK = {
    MIPI_READ_MODE.BASIC:          0x60,
    MIPI_READ_MODE.EXTENDED:       0x20,
    MIPI_READ_MODE.EXTENDED_LONG:  0x38,
}

WRITE_OR_MASK = {
    MIPI_WRITE_MODE.REG0:          0x80,
    MIPI_WRITE_MODE.BASIC:         0x40,
    MIPI_WRITE_MODE.EXTENDED:      0x00,
    MIPI_WRITE_MODE.EXTENDED_LONG: 0x30,
}

READ_AND_MASK = {
    MIPI_READ_MODE.BASIC:          0x9F,
    MIPI_READ_MODE.EXTENDED:       0xDF,
    MIPI_READ_MODE.EXTENDED_LONG:  0xC7,
}

WRITE_AND_MASK = {
    MIPI_WRITE_MODE.REG0:          0x7F,
    MIPI_WRITE_MODE.BASIC:         0xBF,
    MIPI_WRITE_MODE.EXTENDED:      0xFF,
    MIPI_WRITE_MODE.EXTENDED_LONG: 0xCF,
}


class LatticeMachXO2(NoMIPIServer):
    signal_list = []
    transforms_list = []

    def __new__(cls, error_model, num_ports, config_filename="", resource_id='ASRL6::INSTR', **kwargs):
        self = super(LatticeMachXO2, cls).__new__(cls, error_model, num_ports, config_filename, **kwargs)
        self.resource_id = resource_id
        return self

    def __getnewargs__(self):
        return tuple(list(super(LatticeMachXO2, self).__getnewargs__()) + [self.resource_id])

    def __init__(self, error_model, num_ports, config_filename="", resource_id='ASRL6::INSTR', **kwargs):
        super(LatticeMachXO2, self).__init__(error_model, num_ports, config_filename, **kwargs)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self.initialized = True

    def __getstate__(self, state={}):
        state = super(LatticeMachXO2, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(NoMIPIServer, self).__setstate__(state)
        self.connect_handles()
        self.preset()

        # Initialize object PROPERTIES
        self.vio_mode = state["vio_mode"]
        self.clk_rate = state["clk_rate"]
        self.read_mode = state["read_mode"]
        self.write_mode = state["write_mode"]
        self.initialized = True

    def __info__(self):
        super(LatticeMachXO2, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###

    def connect_handles(self):
        rm = visa.ResourceManager()
        self.handles["lattice"] = rm.open_resource(self.resource_id)
        super(LatticeMachXO2, self).connect_handles()

    def preset(self):
        if self.__class__ == LatticeMachXO2:
            self.handles["lattice"].baud_rate = 115200
            self.handles["lattice"].chunk_size = 2048

    @property
    def vio_mode(self):
        return self._vio_mode

    @vio_mode.setter
    def vio_mode(self, mode):
        handle = self.handles["lattice"]
        try:
            if mode == MIPI_VIO_MODE.EXTERNAL or mode == MIPI_VIO_MODE.OFF:
                if not handle.write("w0800"): raise IOError()
            elif mode == MIPI_VIO_MODE.V1P8 or mode == MIPI_VIO_MODE.ON:
                if not handle.write("w0801"): raise IOError()
            else:
                raise ValueError("Unsupported VIO mode")
        except (IOError, VisaIOError):
            raise IOError("Unable to write VIO")
        self._vio_mode = mode

    def _read_basic(self, usid, address):
        handle = self.handles["lattice"]
        dtype = np.uint8
        values = dtype(0)
        try:
            if not handle.write("w01%02X" % (usid,)): raise IOError()
            if not handle.write("w02%02X" % (READ_OR_MASK[MIPI_READ_MODE.BASIC] | address,)): raise IOError()
            if not handle.write("w0080"): raise IOError()
            if not handle.write("r06"): raise IOError()
            with handle.ignore_warning(visa.constants.VI_SUCCESS_DEV_NPRESENT, visa.constants.VI_SUCCESS_MAX_CNT):
                value, status = handle.visalib.read(handle.session, 2)
                values |= dtype(int(value, 16))
        except (IOError, VisaIOError):
            raise IOError("Unable to read basic")
        return values

    def _read_extended(self, usid, address):
        handle = self.handles["lattice"]
        byte_count = 4
        dtype = np.uint32
        values = dtype(0)
        try:
            if not handle.write("w01%02X" % (usid,)): raise IOError()
            if not handle.write("w02%02X" % (READ_OR_MASK[MIPI_READ_MODE.EXTENDED],)): raise IOError()
            if not handle.write("w04%02X" % (address,)): raise IOError()
            if not handle.write("w0080"): raise IOError()
            # if not handle.write("r06"): raise IOError()
            headers = [6, 11, 12, 13]
            for index in range(byte_count):
                offset = len(headers) - byte_count + index
                if not handle.write('r%02d' % (headers[offset])): raise IOError()
                with handle.ignore_warning(visa.constants.VI_SUCCESS_DEV_NPRESENT, visa.constants.VI_SUCCESS_MAX_CNT):
                    value, status = handle.visalib.read(handle.session, 2)
                    values |= dtype(int(value, 16)) << 8 * index
        except (IOError, VisaIOError):
            raise IOError("Unable to read extended")
        return np.uint32(values)

    def _read_extended_long(self, usid, address):
        handle = self.handles["lattice"]
        byte_count = 4
        dtype = np.uint32
        values = dtype(0)
        try:
            if not handle.write("w01%02X" % (usid,)): raise IOError()
            if not handle.write("w02%02X" % (READ_OR_MASK[MIPI_READ_MODE.EXTENDED_LONG],)): raise IOError()
            if not handle.write("w03%02X" % ((address & 0xFF00) >> 8,)): raise IOError()
            if not handle.write("w04%02X" % (address & 0x00FF,)): raise IOError()
            if not handle.write("w0080"): raise IOError()
            # if not handle.write("r06"): raise IOError()
            headers = [6, 11, 12, 13]
            for index in range(byte_count):
                offset = len(headers) - byte_count + index
                if not handle.write('r%02d' % (headers[offset])): raise IOError()
                with handle.ignore_warning(visa.constants.VI_SUCCESS_DEV_NPRESENT, visa.constants.VI_SUCCESS_MAX_CNT):
                    value, status = handle.visalib.read(handle.session, 2)
                    values |= np.uint32(int(value, 16)) << 8 * index
        except (IOError, VisaIOError):
            raise IOError("Unable to read extended long")
        return np.uint64(values)

    def _write_register0(self, usid, address, data):
        handle = self.handles["lattice"]
        try:
            if not handle.write("w01%02X" % (usid,)): raise IOError()
            if not handle.write("w02%02X" % (WRITE_OR_MASK[MIPI_WRITE_MODE.REG0] | data & 0x7F,)): raise IOError()
            if not handle.write("w0080"): raise IOError()
        except (IOError, VisaIOError):
            raise IOError("Unable to write basic")

    def _write_basic(self, usid, address, data):
        handle = self.handles["lattice"]
        try:
            if not handle.write("w01%02X" % (usid,)): raise IOError()
            if not handle.write("w02%02X" % (WRITE_OR_MASK[MIPI_WRITE_MODE.BASIC] | address,)): raise IOError()
            if not handle.write("w05%02X" % (data,)): raise IOError()
            if not handle.write("w0080"): raise IOError()
        except (IOError, VisaIOError):
            raise IOError("Unable to write basic")

    def _write_extended(self, usid, address, data):
        handle = self.handles["lattice"]
        byte_count = 1 if data == 0 else int(np.ceil((len(hex(data)) - 2)/2))
        byte_count = 1 if byte_count == 1 else 4
        try:
            if not handle.write("w01%02X" % (usid,)): raise IOError()
            if not handle.write("w02%02X" % (WRITE_OR_MASK[MIPI_WRITE_MODE.EXTENDED] | (byte_count - 1),)): raise IOError()
            if not handle.write("w04%02X" % (address,)): raise IOError()
            headers = [5, 11, 12, 13]
            for index in range(byte_count):
                offset = len(headers) - byte_count + index
                if not handle.write("w%02d%02X" % (headers[offset], data >> 8 * index & 0xFF)): raise IOError()
            if not handle.write("w0080"): raise IOError()
        except (IOError, VisaIOError):
            raise IOError("Unable to write extended")

    def _write_extended_long(self, usid, address, data):
        handle = self.handles["lattice"]
        byte_count = 1 if data == 0 else int(np.ceil((len(hex(data)) - 2) / 2))
        byte_count = 1 if byte_count == 1 else 4
        try:
            if not handle.write("w01%02X" % (usid,)): raise IOError()
            if not handle.write("w02%02X" % (WRITE_OR_MASK[MIPI_WRITE_MODE.EXTENDED_LONG] | (byte_count - 1),)): raise IOError()
            if not handle.write("w03%02X" % ((address & 0xFF00) >> 8,)): raise IOError()
            if not handle.write("w04%02X" % (address & 0x00FF,)): raise IOError()
            headers = [5, 11, 12, 13]
            for index in range(byte_count):
                offset = len(headers) - byte_count + index
                if not handle.write("w%02d%02X" % (headers[offset], data >> 8*index & 0xFF)): raise IOError()
            if not handle.write("w0080"): raise IOError()
        except (IOError, VisaIOError):
            raise IOError("Unable to write extended long")
