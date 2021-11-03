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

import io
import sys
import pexpect
from pexpect.spawnbase import SpawnBase

PY = sys.version_info[0]

class MCUTKSpawn(SpawnBase):
    """
    MCUTK spawn extend pexpect spawn to save read log to a internal
    bugger. And provided extra functions like:
        - self.get_log()
        - self.is_open()

    To add new spawn type, you must to provide below functions:
        - self.read_nonblocking()
        - self.is_open()
        - self.write()
        - self.close()
    """

    def __init__(self, *args, **kwargs):
        if kwargs.get("encoding") is None:
            kwargs["encoding"] = "utf-8" if sys.version_info.major >= 3 else None

        super(MCUTKSpawn, self).__init__(*args, **kwargs)
        self.log_buffer = io.StringIO() if PY > 2 else io.BytesIO()

    def _log_read_data(self, data):
        """
        Save read data to internal buffers.
        """
        # save to spawn.logfile_read
        self._log(data, 'read')
        self.log_buffer.write(data)
        self.log_buffer.flush()

    @property
    def is_open(self):
        """
        Return a boolean to identify if the stream is open.
        """
        raise NotImplementedError("need add support")

    def write(self, data):
        """Write data to stream."""
        raise NotImplementedError("need add support")

    def close(self):
        raise NotImplementedError("need add support")

    def send(self, data):
        """Send data to serial, and logging to log_send."""
        data = self._coerce_send_string(data)
        self._log(data, 'send')
        return self.write(data)

    def sendline(self, data):
        """Send line"""
        data = self._coerce_send_string(data)
        return self.send(data + self.linesep)

    def writelines(self, sequence):
        """Write a list of strings."""
        for data in sequence:
            self.write(data)

    def flush(self):
        """Flush write and read."""
        pass

    def get_log(self):
        """
        Get the read log.
        """
        if not self.log_buffer:
            return

        self.log_buffer.seek(0)
        return self.log_buffer.read()

    def clear_log(self):
        """
        Clear the read log.
        """
        if not self.log_buffer:
            return
        self.log_buffer.seek(0)
        self.log_buffer.truncate()

    def find(self, pattern, timeout=30):
        """Return the matches of pattern within a specific timeout
        in the serial reading stream. If EOF, return value is None.

        If timeout occured, that will raise pexpect.TIMEOUT exception.
        """
        try:
            self.expect(pattern, timeout=timeout)
            return self.before + self.after
        except pexpect.EOF:
            return

    def test_input(self, input_str, expect, timeout=30):
        """Input value to serial, and test the output if match the expectation.

        Arguments:
            input_str {str} -- input string
            expect {str} -- pattern
            timeout {float} -- timeout in seconds

        Returns:
            str -- the output
        """
        self.write(input_str)
        self.expect(expect, timeout=timeout)

        return self.before + self.after
