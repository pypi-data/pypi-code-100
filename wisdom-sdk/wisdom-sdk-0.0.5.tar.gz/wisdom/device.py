from __future__ import print_function, unicode_literals

import sys
import os
import socket
import re
from wisdom.errors import *
from wisdom.utils import call_api
from wisdom.wifiprovision import esp_prov

esp_prov.config_throw_except = True


class Device:
    """
    Summary - Device Class

    Provides methods to authenticate, initialize and setup the device. 

    Attributes
    ----------
    key : string
        Your subscription key, that you got from the NexStem Developer Portal.

    Methods
    -------
    connect(device_id=None, ip_addr=None, port_num=None)
        Initialize and Authenticate you Device
    disconnect()
        Disconnect the device from the SDK (Clear all configurations.)
    get_working_device()
        Get Device ID for the active working device.
    get_streaming_server()
        Get Server Configuration for data streaming.
    get_telemetry()
        Get Active Device telemetry.
    get_user_information()
        Retrieve user information - name, userid, and registered devices(if any).
    choose_device()
        Choose Active Working Device.

    """

    def __init__(self, key):
        self.deviceID = 0
        self.user_details = User()
        self.subscription_key = key
        self.ip_addr = "NA"
        self.port_num = 6565

    @staticmethod
    def get_default_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except socket.error:
            IP = 'NA'
        finally:
            s.close()
        return IP

    def get_working_device(self):
        """
        Summary - Get Device ID for the active working device.

        Returns
        -------
        deviceID : string
            Device ID of the active device.

        """
        return self.deviceID

    def get_streaming_server(self):
        """
        Summary - Get Server Configuration for data streaming.

        Returns
        -------
        server : string
            IP Address and Port Number of the data socket.
        """
        return {"IP": self.ip_addr, "Port": self.port_num}

    def choose_device(self):
        """
        Summary - Choose Active Working Device

        Choose active device from the list of registered devices.

        Returns
        -------
        deviceID : string
            chosen device

        Raises
        ------
        Exception DeviceInitError
        """

        device_count = len(self.user_details.device_list)
        if device_count < 1:
            raise DeviceInitError("Provision your headset. Use the provision() method.")
        print("-----------------------------")
        for i in range(device_count):
            print(f'{i + 1}) {self.user_details.device_list[i]}')
        print("-----------------------------")
        choice = input("Choose the device you want to use: ")

        return self.user_details.device_list[int(choice) - 1]

    def provision(self, ssid, password):
        oid = self.user_details.oid
        print('Starting Provisioning')
        verbose = False
        protover = 'v1.1'
        secver = 0
        provmode = 'softap'
        ap_ssid = ssid
        ap_password = password

        print('Getting security')
        security = esp_prov.get_security()
        if security is None:
            raise ProvisionError('Failed to get security')
        devname = None
        print('Getting transport')
        transport = esp_prov.get_transport()
        if transport is None:
            raise ProvisionError('Failed to get transport')

        print('Verifying protocol version')
        if not esp_prov.version_match(transport):
            raise ProvisionError('Mismatch in protocol version')

        print('Verifying scan list capability')
        if not esp_prov.has_capability(transport):
            raise ProvisionError('Capability not present')

        print('Starting Session')
        if not esp_prov.establish_session(transport, security):
            raise ProvisionError('Failed to start session')

        # print('Sending Custom Data')
        # if not esp_prov.custom_data(transport, security, oid):
        #     raise ProvisionError('Failed to send custom data')

        print('Sending Wifi credential to DUT')
        if not esp_prov.send_wifi_config(transport, security, ap_ssid, ap_password):
            raise ProvisionError('Failed to send Wi-Fi config')

        print('Applying config')
        if not esp_prov.apply_wifi_config(transport, security):
            raise ProvisionError('Failed to send apply config')

        if not esp_prov.wait_wifi_connected(transport, security):
            raise ProvisionError('Provisioning failed')

    def get_user_information(self, ignore_device_info=False):
        """
        Summary - Retrieve user information - name, userid, and registered devices(if any).

        The get_user_information method plays a critical role in authenticating a user. The userid in combination
        with the subscription key, are used to authenticate and validate a user.

        Parameters
        ----------
        ignore_device_info

        Raises
        ------
        Exception DeviceInitError
        Exception AuthFailedError
        """

        res = call_api('getUserDetails', self.subscription_key, api_type='GET', handle_res=False)
        if res.status_code != 401:
            name = res.json().get('name')
            oid = res.json().get('oid')
            if res.status_code != 202:
                devices = res.json().get('devices')
                device_count = self.user_details.populate_info(name, oid, devices)
            elif ignore_device_info:
                return name, oid
            else:
                raise DeviceInitError(res.text)
        else:
            raise AuthFailedError(res.text)

    def connect(self, device_id=None, ip_addr=None, port_num=None):
        """
        Summary - Initialize and Authenticate you Device

        The connect method allows one to connect with their device. In case of multiple devices are registered to a
        user, you can select which device you want to connect with.

        Parameters ---------- device_id : string, optional The device ID for the device which you want to initialize
        and configure to start streaming data. In case None is passed, you will be given a list of devices registered
        to you, to choose from. ip_addr : string, optional IP Address for the socket which receives the incoming data
        from the device. In case None is passed, local IP address of the workstation will be used. Default - Local IP
        Address of the workstation port_num : int, optional Port Number for the socket which receives the incoming
        data from the device. In case None is passed, port number 6565 of the workstation will be used.

        Returns
        -------
        status_code : int
            200, if the execution was successful, else the function will throw an exception.

        Raises
        ------
        Exception ValidationError
        Exception AuthFailedError
        Exception RequestError
        Exception UnexpectedError
        """
        self.get_user_information(ignore_device_info=False)

        # check for validity of deviceID
        if device_id is None:
            print("Choose the device you want to configure from the list of registered device/s below.")
            self.deviceID = self.choose_device()
        elif device_id not in self.user_details.device_list:
            print("Invalid Device ID entered. Choose the device you want to configure from the list of registered "
                  "device/s below.")
            self.deviceID = self.choose_device()
        else:
            self.deviceID = device_id

        # Check for valid IP and Port number and allocate accordingly
        if ip_addr is None and port_num is None:
            self.ip_addr = self.get_default_ip()
            self.port_num = 6565
            print(f"Streaming on {self.get_streaming_server()}")
        elif ip_addr is None:
            try:
                assert 0 < int(port_num) < 65535
            except AssertionError:
                raise ValidationError("Invalid port number f{port_num}.")
            self.ip_addr = self.get_default_ip()
            self.port_num = port_num
        elif port_num is None:
            ok = re.match('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip_addr)
            if not ok:
                raise ValidationError("Enter a valid IP Address.")
            self.ip_addr = ip_addr
            self.port_num = 6565
        else:
            ok = re.match('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip_addr)
            if not ok:
                raise ValidationError("Enter a valid IP Address.")
            try:
                assert 0 < int(port_num) < 65535
            except AssertionError:
                raise ValidationError("Enter a valid port number (0-65534).")

            self.ip_addr = ip_addr
            self.port_num = port_num

        params = {'deviceid': self.deviceID,
                  'ipaddr': self.ip_addr,
                  'portnum': self.port_num}
        res = call_api('setServerDetails', self.subscription_key, api_type='POST', handle_res=True, params=params)

        return 200

    def disconnect(self):
        """
        Summary - Disconnect the device from the SDK (Clear all configurations.)

        The disconnect method allows one to disconnect their active device and clear the server details from the device. 

        Returns
        -------
        status_code : int
            200, if the execution was successful, else the function will throw an exception.

        Raises
        ------
        Exception AuthFailedError
        Exception RequestError
        Exception UnexpectedError
        """
        params = {'deviceid': self.deviceID}
        res = call_api('removeServerDetails', self.subscription_key, api_type='POST', handle_res=True, params=params)

        return 200

    def get_telemetry(self):
        """
        Summary - Get Active Device telemetry.

        The get_telemetry method, allows one to get the device twin for the active working device.

        Returns
        -------
        status_code : int
            telemetry, a dictionary of the device telemetry

        Raises
        ------
        Exception AuthFailedError
        Exception RequestError
        Exception UnexpectedError
        """
        params = {'deviceid': self.deviceID}
        res = call_api('getDeviceTelemetry', self.subscription_key, api_type='GET', handle_res=True, params=params)

        return res.json()


class User:
    # USER Class - Stores user information
    def __init__(self):
        self.oid = 0
        self.name = ""
        self.device_list = []

    def set_oid(self, oid):
        self.oid = oid

    def set_name(self, name):
        self.name = name

    def list_devices(self):
        return self.device_list

    def populate_info(self, name, oid, devices):
        self.device_list = devices
        self.name = name
        self.oid = oid

        if len(self.device_list) < 1:
            raise DeviceInitError
        else:
            return len(self.device_list)
