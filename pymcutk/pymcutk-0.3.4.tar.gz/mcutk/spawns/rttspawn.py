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
import logging
import platform
import time
import pylink
from pylink import library
from mcutk.spawns.base import MCUTKSpawn

LOGGER = logging.getLogger(__name__)

class RTTSpawn(MCUTKSpawn):
    """Segger RTT spawn.

    To get more about Segger RTT, you can visit https://wiki.segger.com/RTT

    This is a JLink RTT viewer and built on pexpect.SpawnBase.
    With this class you can use pexect functions to interact with target device
    via RTT channels.
    """
    _attrs = ["device_name", "search_range", "serial_number", "interface", "jlink_home", "open"]
    def __init__(self, *args, **kwargs):
        """
        Keyword Arguments:
            device_name: {str}, set jlink device name
            serial_number: jlink serial number
            search_range: {str},  set RTT search ranges, like: 0x20003000 0x5000;0x60004000 0x2000
            interface: {str}, device interface, SWD or JTAG
            jlink_home: {str}, jlink home direcotry
        """
        self.up_channel = None
        self.down_channel = None

        self.search_range = kwargs.get("search_range")
        self.device_name = kwargs.get("device_name")
        self.serial_number = kwargs.get("serial_number")
        self.interface = kwargs.get("interface", "SWD")
        jlink_home = kwargs.get("jlink_home")
        auto_open = kwargs.get("open", True)
        # clear kwagrs
        for attr in RTTSpawn._attrs:
            if attr in kwargs:
                kwargs.pop(attr)

        lib = None
        if jlink_home and platform.system() == "Windows":
            dll_name = library.Library.get_appropriate_windows_sdk_name()
            dll_path = jlink_home + "/%s.dll" % dll_name
            lib = library.Library(dll_path)

        super(RTTSpawn, self).__init__(*args, **kwargs)
        self.jlink = pylink.JLink(serial_no=self.serial_number, lib=lib)
        if auto_open:
            self.open()

    def open(self):
        """Open and connect to device."""
        self.jlink.open(self.serial_number)
        LOGGER.info("connecting to %s...", self.device_name)
        interface = getattr(pylink.enums.JLinkInterfaces, self.interface, None)
        self.jlink.set_tif(interface)
        self.jlink.connect(self.device_name)
        LOGGER.info("connected, starting RTT...")

        if self.search_range:
            self.jlink.exec_command("SetRTTSearchRanges %s" % self.search_range)
        self.jlink.rtt_start(None)

        while True:
            try:
                num_up = self.jlink.rtt_get_num_up_buffers()
                num_down = self.jlink.rtt_get_num_down_buffers()
                LOGGER.info("RTT started, %d up bufs, %d down bufs.", num_up, num_down)
                break
            except pylink.errors.JLinkRTTException as error:
                LOGGER.warning(error)
                time.sleep(0.1)

        LOGGER.info("up channels:")
        for buf_index in range(self.jlink.rtt_get_num_up_buffers()):
            buf = self.jlink.rtt_get_buf_descriptor(buf_index, True)
            LOGGER.info("%d: name = %r, size = %d bytes, flags = %d",
                        buf.BufferIndex, buf.name, buf.SizeOfBuffer, buf.Flags)
            if buf.SizeOfBuffer > 0:
                self.up_channel = buf

        LOGGER.info("down channels:")
        for buf_index in range(self.jlink.rtt_get_num_down_buffers()):
            buf = self.jlink.rtt_get_buf_descriptor(buf_index, False)
            LOGGER.info("%d: name = %r, size = %d bytes, flags = %d",
                        buf.BufferIndex, buf.name, buf.SizeOfBuffer, buf.Flags)
            if buf.SizeOfBuffer > 0:
                self.down_channel = buf

        return self

    def __str__(self):
        return "JLinkRTTSpawn({}, SN={})".format(self.device_name, self.serial_number)

    def read_nonblocking(self, size=1, timeout=None):
        """Fake read none blocking for pexpect spawn."""
        data = self.jlink.rtt_read(self.up_channel.BufferIndex, self.up_channel.SizeOfBuffer)
        str_data = self._decoder.decode(bytes(data), final=False)
        self._log_read_data(str_data)
        return str_data

    def chunks(self, lst, num):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), num):
            yield lst[i:i + num]

    def write(self, data):
        """Write str to JLink RTT channel."""
        if not isinstance(data, bytearray):
            LOGGER.info("%s write: %s", self, repr(data))

        bytes_data = list(bytearray(data, "utf-8"))
        for chunk in self.chunks(bytes_data, self.down_channel.SizeOfBuffer-1):
            self.jlink.rtt_write(0, chunk)

    @property
    def is_open(self):
        return self.jlink.opened()

    def close(self):
        """Disconnect JLink"""
        if self.jlink.opened():
            self.jlink.close()
