from __future__ import print_function

import json
import time
from builtins import input as binput
from getpass import getpass

from wisdom.wifiprovision import prov
from wisdom.wifiprovision import security
from wisdom.wifiprovision import transport

from wisdom.errors import ProvisionError

# Set this to true to allow exceptions to be thrown
config_throw_except = True

def on_except(err):
    if config_throw_except:
        raise ProvisionError(err)
    else:
        print(err)


def get_security():
    return security.Security0(False)


def get_transport():
    try:
        tp = None 
        service_name = '192.168.4.1:80'
        tp = transport.Transport_HTTP(service_name)
        return tp
    except RuntimeError as e:
        on_except(e)
        return None


def version_match(tp):
    protover = 'v1.1'
    try:
        response = tp.send_data('proto-ver', protover)

        if response.lower() == protover.lower():
            return True

        try:
            info = json.loads(response)
            if info['prov']['ver'].lower() == protover.lower():
                return True

        except ValueError:
            return False

    except Exception as e:
        on_except(e)
        return None


def has_capability(tp):
    capability='wifi_scan'
    try:
        response = tp.send_data('proto-ver', capability)
        try:
            info = json.loads(response)
            supported_capabilities = info['prov']['cap']
            if capability.lower() == 'none':
                return True
            elif capability in supported_capabilities:
                return True
            return False

        except ValueError:
            return False

    except RuntimeError as e:
        on_except(e)

    return False


def get_version(tp):
    response = None
    try:
        response = tp.send_data('proto-ver', '---')
    except RuntimeError as e:
        on_except(e)
        response = ''
    return response


def establish_session(tp, sec):
    try:
        response = None
        while True:
            request = sec.security_session(response)
            if request is None:
                break
            response = tp.send_data('prov-session', request)
            if (response is None):
                return False
        return True
    except RuntimeError as e:
        on_except(e)
        return None


def custom_data(tp, sec, custom_data):
    try:
        message = prov.custom_data_request(sec, custom_data)
        response = tp.send_data('custom-data', message)
        return (prov.custom_data_response(sec, response) == 0)
    except RuntimeError as e:
        on_except(e)
        return None



def send_wifi_config(tp, sec, ssid, passphrase):
    try:
        message = prov.config_set_config_request(sec, ssid, passphrase)
        response = tp.send_data('prov-config', message)
        return (prov.config_set_config_response(sec, response) == 0)
    except RuntimeError as e:
        on_except(e)
        return None


def apply_wifi_config(tp, sec):
    try:
        message = prov.config_apply_config_request(sec)
        response = tp.send_data('prov-config', message)
        return (prov.config_apply_config_response(sec, response) == 0)
    except RuntimeError as e:
        on_except(e)
        return None


def get_wifi_config(tp, sec):
    try:
        message = prov.config_get_status_request(sec)
        response = tp.send_data('prov-config', message)
        return prov.config_get_status_response(sec, response)
    except RuntimeError as e:
        on_except(e)
        return None


def wait_wifi_connected(tp, sec):
    """
    Wait for provisioning to report Wi-Fi is connected
    Returns True if Wi-Fi connection succeeded, False if connection consistently failed
    """
    TIME_PER_POLL = 5
    retry = 3

    while True:
        time.sleep(TIME_PER_POLL)
        ret = get_wifi_config(tp, sec)
        if ret == 'connecting':
            continue
        elif ret == 'connected':
            return True
        elif retry > 0:
            retry -= 1
        else:
            return False

