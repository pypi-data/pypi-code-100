#
# MIT License
#
# Copyright 2021 NXP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import sys
import logging
from mcutk import pserial
from mcutk.spawns.base import MCUTKSpawn

class SerialSpawn(MCUTKSpawn):
    """Due to pyserial not support file descriptor for windows, fdspawn could not be used.
    This class implement a spawn for pyserial, all interfaces are defined from the base
    `SpawnBase`. For more information about the usage, please refer the pexpect documentation.

    Simple example:
        >>> from mcutk.pserial import Serial
        >>> ser = Serial('COM3', 9600)
        >>> spawn = ser.SerialSpawn()
        >>> spawn.write_expect("Waiting for power mode select..", timeout=3)
    """
    def __init__(self, serial, **kwargs):
        """
        Arguments:
            serial: {serial.Serial object}
            open_port: {boolean} open port if it is not open, default True
        """
        if hasattr(serial, 'reader_isalive'):
            if serial.reader_isalive:
                serial.stop_reader()
                logging.debug('reader thread is stopped!')

        if kwargs.get("encoding") is None:
            kwargs["encoding"] = "utf-8" if sys.version_info.major >= 3 else None

        self.serial = serial
        self.serial.timeout = 0.3
        auto_open = kwargs.pop("open") if "open" in kwargs else True
        super(SerialSpawn, self).__init__(**kwargs)
        if auto_open:
            self.open()
        self.closed = not self.serial.is_open

    def open(self):
        """Open serial port"""
        if not self.serial.is_open:
            logging.info("open port %s, baudrate: %s", self.serial, self.serial.baudrate)
            self.serial.open()
        return self

    def __str__(self):
        return str(self.serial) or "SerialSpawn(port={})".format(self.serial.port)

    def read_nonblocking(self, size=1, timeout=None):
        """This is fake nonblocking, the size is decided by how many data in the buffer,
        rather than specific value, this is because big size will block the serial read,
        small size will effect the performance when many data in buffer. timeout is useless.
        """
        raw = self.serial.read(self.serial.in_waiting or 1)
        str_data = self._decoder.decode(raw, final=False)
        self._log_read_data(str_data)
        return str_data

    def write(self, data):
        return self.serial.write(self._encoder.encode(data, final=False))

    def flush(self):
        """
        Flush serial
        """
        self.serial.flush()

    def flush_log(self):
        """
        Flush logfile_read to a readable attribute: SerialSpawn.data
        """
        if not isinstance(self.serial, pserial.Serial):
            logging.error("Cannot flush_log: serial is not mcutk.pserial.Serial object!")

        logging.debug("dump reading log to serial object!")
        self.serial.append_data(self.get_log())

    def close(self):
        """Close serial port, and dump the logfile_read to mcutk.pserial.Serial.data.
        If the serial instance is comes from pyserial, dump action will not take.
        """
        self.serial.close()
        self.flush_log()
        self.closed = True

    def isalive(self):
        """
        Return a boolean the port is open or not
        """
        return self.serial.is_open

    @property
    def is_open(self):
        """
        Return a boolean the port is open or not
        """
        return self.serial.is_open
