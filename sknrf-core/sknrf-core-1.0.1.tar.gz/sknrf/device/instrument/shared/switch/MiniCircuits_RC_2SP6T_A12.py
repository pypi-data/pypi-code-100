"""
This program is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

The GNU General Public License can be found at <http://www.gnu.org/licenses/>.
"""

"""
Linux interface to Mini-Circuits matrix switch RC-2SP6T-A12.
Written by: Tim Dunker
E-mail: tdu [at] justervesenet [dot] no
OpenPGP key: 0x4FDBC497

This programme is based on the script 'Minimalist Linux interface to Mini Circuits USB power meter', copyright (C) 2017, Rigetti & Co. Inc., distributed with a GPL licence.


Basic usage:
  from MiniCircuits_RC_2SP6T_A12 import MiniCircuits_Switch
  sw = MiniCircuits_Switch()
  # Switch to channel 6 on switch A:  
  sw.switch(1,6)
  # Switch to channel 3 on switch B:
  sw.switch(2,3)
  # De-energize switch A:
  sw.switch(1,0)
"""

import string
import sys
import threading
import time
import numpy as np
import libusb1
import usb1
import requests

################################################################################
#
# Class to operate a Mini-Circuits RC-2SP6T-A12 switch.
#
################################################################################

class MiniCircuits_Switch():
    """
    Operate a Mini Circuits matrix switch RC-2SP6T-A12.
    """
    # Vendor ID of Mini Circuits:
    _VENDOR_ID = 0x20CE
    # Product ID of the RF switch box:
    _PRODUCT_ID = 0x0022
    # Length of a message in bytes:
    _MSG_LEN = 64

    _GET_DEVICE_MODEL_NAME = 40
    _GET_DEVICE_SERIAL_NUMBER = 41
    _GET_FIRMWARE = 99
    _SET_SP6T_SWITCH = 12
    _GET_SP6T_SWITCH = 13

    _RESET_ETHERNET = 101
    _SET_ETHERNET_CONFIGURATION = 250
    _GET_ETHERNET_CONFIGURATION = 251
    _STATIC_IP_ADDRESS = 201
    _STATIC_SUBNET_MASK = 202
    _STATIC_NETWORK_GATEWAY = 203
    _HTTP_PORT = 204
    _USE_PASSWORD = 205
    _PASSWORD = 206
    _DHCP_STATUS = 207

    switch_map = {
        1: "A",
        2: "B"
    }
    ip_address = ""

    def __init__(self, address="USB::0x20CE::0x0022", ip_address=""):
        """
        Connect to the USB RF matrix switch.
        """
        if len(MiniCircuits_Switch.ip_address) == 0:
            print("Initializing MiniCircuits Switch")
            # Configure threading
            self.lock = threading.Lock()
            # Configure the USB target:
            self.context = usb1.USBContext()
            _, vendor_id, product_id = address.split("::")
            self.handle = self.context.openByVendorIDAndProductID(int(vendor_id, 16), int(product_id, 16))
            if self.handle is None:
                raise RuntimeError('No USB RF matrix switch found.')
            self.preset()
            if len(ip_address):
                res = self.get_dhcp_status()
                res = self.set_dhcp_status(False)
                res = self.get_dhcp_status()
                res = self.get_static_ip_address()
                res = self.set_static_ip_address(ip_address)
                res = self.get_static_ip_address()
                res = self.get_static_subnet_mask()
                res = self.set_static_subnet_mask("255.255.0.0")
                res = self.get_static_subnet_mask()
                res = self.get_static_network_gateway()
                res = self.set_static_network_gateway("0.0.0.0")
                res = self.get_static_network_gateway()
                res = self.get_http_port()
                res = self.set_http_port(80)
                res = self.get_http_port()
                res = self.get_use_password()
                res = self.set_use_password(False)
                res = self.get_use_password()
                MiniCircuits_Switch.ip_address = ip_address
                del self.handle

    @property
    def id(self):
        return "Mini-Circuits USB::0x20CE::0x0022"

    def preset(self):
        if hasattr(self, "handle"):
            if self.handle.kernelDriverActive(0):
                self.handle.detachKernelDriver(0)
            self.handle.resetDevice()
            self.handle.claimInterface(0)
            # with self.handle.claimInterface(0):
            #     pass

    def _query(self, cmd):
        """
        Issue the provided command, get and validate the response, and return the rest of the
        response.
        """
        self.cmd = bytearray([0] * MiniCircuits_Switch._MSG_LEN)
        self.cmd[:len(cmd)] = cmd
        self.lock.acquire()
        threading.Thread(target=self._write).start()
        while self.lock.locked():
            time.sleep(1e-6)
        if self.nsent != len(self.cmd):
            sys.exit(1)
        self.lock.acquire()
        threading.Thread(target=self._read).start()
        while self.lock.locked():
            time.sleep(10e-6)
        if len(self.response) != MiniCircuits_Switch._MSG_LEN:
            sys.exit(1)
        return self.response

    def _query_string(self, cmd, response_length=None):
        """
        Issue the provided command and return the string response from the device.
        If the response length is not provided, use a terminating null character to extract the
        string.
        """
        resp = self._query(cmd)
        if response_length is None:
            try:
                response_length = resp.index(bytearray([0]))
            except:
                raise RuntimeError('No terminating null character in response: %s' % resp)
        resp = resp[1:response_length - 1]
        return resp

    def _read(self):
        """
        Interrupt task required to read from the USB device.
        """
        self.response = ''
        try:
            self.response = self.handle.interruptRead(endpoint=1, length=MiniCircuits_Switch._MSG_LEN, timeout=1000)
        finally:
            self.lock.release()

    def _write(self):
        """
        Interrupt task required to write to the USB device.
        """
        self.nsent = -1
        try:
            self.nsent = self.handle.interruptWrite(endpoint=1, data=self.cmd, timeout=50)
        finally:
            self.lock.release()

    def get_device_model_name(self):
        """
        Read the device model name of the RF matrix switch.
        """
        resp = self._query_string([MiniCircuits_Switch._GET_DEVICE_MODEL_NAME, ])
        try:
            return resp.decode()
        except:
            raise RuntimeError('Device model name readout not valid: "%s"' % resp)

    def get_device_serial_number(self):
        """
        Read the serial number of the RF matrix switch.
        """
        resp = self._query_string([MiniCircuits_Switch._GET_DEVICE_SERIAL_NUMBER, ])
        try:
            return resp.decode()
        except:
            raise RuntimeError('Serial number readout not valid: "%s"' % resp)

    def get_firmware(self):
        """
        Read the firmware of the RF matrix switch.
        """
        resp = self._query([MiniCircuits_Switch._GET_FIRMWARE, ])[5:7]
        try:
            return resp.decode()
        except:
            raise RuntimeError('Firmware readout not valid: "%s"' % resp)

    def get_dhcp_status(self):
        """
        Get the dhcp status
        """
        resp = self._query_string([MiniCircuits_Switch._GET_ETHERNET_CONFIGURATION,
                                   MiniCircuits_Switch._DHCP_STATUS, ])
        try:
            return resp[0] if len(resp) > 0 else 0
        except:
            raise RuntimeError('DHCP status readout not valid: "%s"' % resp)

    def set_dhcp_status(self, dhcp_status):
        """
        Set the dhcp status
        """
        resp = self._query_string([MiniCircuits_Switch._SET_ETHERNET_CONFIGURATION,
                                   MiniCircuits_Switch._DHCP_STATUS, dhcp_status])
        try:
            return resp[0] if len(resp) > 0 else 0
        except:
            raise RuntimeError('DHCP status readout not valid: "%s"' % resp)

    def get_static_ip_address(self):
        """
        Get the static ip address
        """
        resp = self._query([MiniCircuits_Switch._GET_ETHERNET_CONFIGURATION,
                                   MiniCircuits_Switch._STATIC_IP_ADDRESS, ])
        try:
            return resp[0] if len(resp) == 1 else ".".join(map(str, resp[1:5:]))
        except:
            raise RuntimeError('Static IP Address readout not valid: "%s"' % resp)

    def set_static_ip_address(self, ip_address):
        """
        Set the static ip address
        """
        byte_address = bytearray(list(map(int, ip_address.split("."))))
        resp = self._query_string([MiniCircuits_Switch._SET_ETHERNET_CONFIGURATION,
                                   MiniCircuits_Switch._STATIC_IP_ADDRESS, *byte_address])
        try:
            return resp[0] if len(resp) > 0 else 0
        except:
            raise RuntimeError('Static IP Address readout not valid: "%s"' % resp)

    def get_static_subnet_mask(self):
        """
        Get the static subnet mask
        """
        resp = self._query([MiniCircuits_Switch._GET_ETHERNET_CONFIGURATION,
                            MiniCircuits_Switch._STATIC_SUBNET_MASK, ])
        try:
            return resp[0] if len(resp) == 1 else ".".join(map(str, resp[1:5:]))
        except:
            raise RuntimeError('Static Subnet Address readout not valid: "%s"' % resp)

    def set_static_subnet_mask(self, subnet_mask):
        """
        Set the static subnet mask
        """
        byte_address = bytearray(list(map(int, subnet_mask.split("."))))
        resp = self._query_string([MiniCircuits_Switch._SET_ETHERNET_CONFIGURATION,
                                   MiniCircuits_Switch._STATIC_SUBNET_MASK, *byte_address])
        try:
            return resp[0] if len(resp) > 0 else 0
        except:
            raise RuntimeError('Static Subnet Address readout not valid: "%s"' % resp)

    def get_static_network_gateway(self):
        """
        Get the static network gateway
        """
        resp = self._query([MiniCircuits_Switch._GET_ETHERNET_CONFIGURATION,
                            MiniCircuits_Switch._STATIC_NETWORK_GATEWAY, ])
        try:
            return resp[0] if len(resp) == 1 else ".".join(map(str, resp[1:5:]))
        except:
            raise RuntimeError('Static Network Gateway Address readout not valid: "%s"' % resp)

    def set_static_network_gateway(self, network_gateway):
        """
        Set the static network gateway
        """
        byte_address = bytearray(list(map(int, network_gateway.split("."))))
        resp = self._query_string([MiniCircuits_Switch._SET_ETHERNET_CONFIGURATION,
                                   MiniCircuits_Switch._STATIC_NETWORK_GATEWAY, *byte_address])
        try:
            return resp[0] if len(resp) > 0 else 0
        except:
            raise RuntimeError('Static Network Gateway Address readout not valid: "%s"' % resp)

    def get_http_port(self):
        """
        Get the static http port
        """
        resp = self._query([MiniCircuits_Switch._GET_ETHERNET_CONFIGURATION, MiniCircuits_Switch._HTTP_PORT, ])
        try:
            return resp[0] if len(resp) == 1 else (resp[1] * 256) + resp[2]
        except:
            raise RuntimeError('HTTP Port readout not valid: "%s"' % resp)

    def set_http_port(self, port):
        """
        Set the static http port
        """
        byte2 = int(port / 256)
        byte3 = int(port - byte2 * 256)
        resp = self._query_string([MiniCircuits_Switch._SET_ETHERNET_CONFIGURATION, MiniCircuits_Switch._HTTP_PORT, byte2, byte3])
        try:
            return resp[0] if len(resp) > 0 else 0
        except:
            raise RuntimeError('HTTP Port readout not valid: "%s"' % resp)

    def get_use_password(self):
        """
        Get the use_password
        """
        resp = self._query([MiniCircuits_Switch._GET_ETHERNET_CONFIGURATION,
                            MiniCircuits_Switch._USE_PASSWORD, ])
        try:
            return resp[0] if len(resp) == 1 else resp[1] > 0
        except:
            raise RuntimeError('Use Password readout not valid: "%s"' % resp)

    def set_use_password(self, password):
        """
        Set the use_password
        """
        resp = self._query_string([MiniCircuits_Switch._SET_ETHERNET_CONFIGURATION,
                                   MiniCircuits_Switch._USE_PASSWORD, password])
        try:
            return resp[0] if len(resp) > 0 else 0
        except:
            raise RuntimeError('Use Password readout not valid: "%s"' % resp)

    def switch(self, switch):
        """
        Set the switch "sw" to channel "state".
        """
        if len(self.ip_address):
            resp = requests.put("http://%s/SP6T%s:STATE?:" % (self.ip_address, MiniCircuits_Switch.switch_map[switch]))
            if len(resp.text) == 1:
                return resp.json()
            else:
                raise RuntimeError('Switch state readout not valid: "%s"' % resp)
        else:
            resp = self._query_string([MiniCircuits_Switch._GET_SP6T_SWITCH, switch, ])
            try:
                return resp[0] if len(resp) > 0 else 0
            except:
                raise RuntimeError('Switch state readout not valid: "%s"' % resp)

    def set_switch(self, switch, state):
        """
        Set the switch "sw" to channel "state".
        """
        if len(self.ip_address):
            resp = requests.put("http://%s/SP6T%s:STATE:%d" % (self.ip_address, MiniCircuits_Switch.switch_map[switch], state))
            time.sleep(0.1)
            if len(resp.text) == 1:
                return resp.json()
            else:
                raise RuntimeError('Switch state readout not valid: "%s"' % resp)
        else:
            resp = self._query_string([MiniCircuits_Switch._SET_SP6T_SWITCH, switch, state, ])
            time.sleep(0.1)
            try:
                return resp.decode()
            except:
                raise RuntimeError('Switch state readout not valid: "%s"' % resp)


if __name__ == "__main__":
    sw = MiniCircuits_Switch(address="USB::0x20CE::0x0022", ip_address="172.16.0.70")
    del sw
    sw = MiniCircuits_Switch(address="USB::0x20CE::0x0022", ip_address="172.16.0.70")
    # Switch to channel 6 on switch A:
    sw.set_switch(1, 6)
    print("1: %d" % (sw.switch(1)))
    sw.set_switch(2, 3)
    print("2: %d" % (sw.switch(2)))
    # De-energize switch A:
    print("1: %d" % (sw.switch(1)))
    sw.set_switch(1, 0)
    print("1: %d" % (sw.switch(1)))

