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

from __future__ import absolute_import
from functools import partial
import time
import sys
import logging

from serial import Serial as PY_SERIAL
from serial.tools.list_ports import comports
from serial.threaded import Protocol, ReaderThread
from mcutk.spawns.serialspawn import SerialSpawn

LOGGER = logging.getLogger(__name__)

PY = sys.version_info[0]

class DataHandler(Protocol):
    """Data handler for ReaderThread."""

    def connection_made(self, transport):
        super(DataHandler, self).connection_made(transport)
        self._serial = transport.serial

    def data_received(self, data):
        if data:
            self._serial.append_data(data)


class Serial(PY_SERIAL):
    """This class is inherited from pyserial::serial.Serial class.
    It extended the Serial class to support data reading in a background thread.

    The attribute serial.reader is the instance of reading thread.

    Example:
        >>> from mcutk.pserial import Serial
        >>> ser = Serial("COM4", 115200)
        >>> ser.start_reader() # start a reader
        >>> ser.write("write something")
        >>> ser.close()
        >>> print(ser.data) # access reader data
    """

    def __init__(self, *args, **kwargs):
        if not kwargs.get('timeout', None):
            kwargs['timeout'] = 1
        super(Serial, self).__init__(*args, **kwargs)
        self._data = list()
        self.reader = None
        self.Spawn = partial(SerialSpawn, self)
        self.SerialSpawn = self.Spawn

    def __str__(self) -> str:
        return "Serial.%s" % self.port

    def write(self, data):
        # safe to convert str to bytes
        # because pyserial do not support unicode
        if not isinstance(data, bytearray):
            LOGGER.info("%s write: %s", self, repr(data))

        if isinstance(data, str):
            data = data.encode()
        super(Serial, self).write(data)

    def write_chars(self, data, interval=0.03):
        """Send char one by one in a string with a fixed interval.

        Arguments:
            data {str} -- input data
            interval {float} -- interval seconds (default: {0.03})
        """
        for s in data:
            super(Serial, self).write(s.encode())
            time.sleep(interval)
        LOGGER.info("%s write chars: %s, interval: %ss", self, repr(data), interval)

    def start_reader(self):
        """Start the reader thread, and return the data handler when the reader is running.
        If the port is not open, it will open it at first.
        """
        if not self.is_open:
            self.open()

        if self.reader_isalive:
            raise RuntimeError('failed to start reader, reader thread is already running.')

        self.reader = ReaderThread(self, DataHandler)
        data_handler = self.reader.__enter__()
        LOGGER.info('%s read threading is running!', self)
        return data_handler

    def stop_reader(self):
        """Stop the reader thread."""
        if self.reader_isalive:
            self.reader.stop()
            LOGGER.info('%s read threading is stopped!', self)

    def clear_reader_buffer(self):
        """Clear the data buffer for the reader thread.
        """
        self._data = list()

    @property
    def reader_isalive(self):
        """Return a boolean value to identify the reader is alive or not.
        """
        return self.reader and self.reader.alive

    @property
    def data(self):
        """Return all of data in the internal data buffer."""
        return "".join(self._data)

    def append_data(self, data):
        """Append data to internal buffer."""

        if PY > 2 and isinstance(data, bytes):
            data = data.decode(errors="replace")
        self._data.append(data)

    def close(self):
        """Close the serial port.
        """
        if self.reader and self.reader.alive:
            self.stop_reader()
        super(Serial, self).close()

    @property
    def is_installed(self):
        """ Return a boolean value to check if this serial device is installed """
        ports_list = comports()
        for port_info in ports_list:
            if self.port in port_info.device:
                return True
        return False
