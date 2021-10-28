from re import findall
from functools import reduce
import requests
from wisdom.errors import *
import pandas as pd

SAMPLING_FREQUENCY = 976.5625

compliment = {'0': '1', '1': '0'}

hex_map = {'0': '0000', '1': '0001', '2': '0010', '3': '0011',
           '4': '0100', '5': '0101', '6': '0110', '7': '0111',
           '8': '1000', '9': '1001', 'a': '1010', 'b': '1011',
           'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111'}

column_names = ['AF3', 'Fz', 'FC3', 'C3', 'CP3', 'C5', 'PO3', 'Cz',
                'AF4', 'CPz', 'FC4', 'C4', 'CP4', 'C6', 'PO4', 'Pz',
                'counter', 'marker', 'button', 'battery', 'parity']


def stream_eeg_only(x):
    return x[:17]


def parse_sample(sample_hex_str):
    sample_data = []

    eeg = sample_hex_str[:96]
    counter = sample_hex_str[96:100]
    marker = sample_hex_str[100:102]
    battery = sample_hex_str[102:106]
    cksum = sample_hex_str[106:]

    sample_data.extend([parse_eeg_str(channel_str) for channel_str in findall('.' * 6, eeg)])
    sample_data.append(int(counter, 16))

    marker_binary = ''.join(hex_map[d] for d in marker)
    sample_data.append(int(marker_binary[:-1], 2))
    sample_data.append(int(marker_binary[-1], 2))

    sample_data.append(int(battery, 16))

    byte_list = [int(byte_str, 16) for byte_str in findall('..', sample_hex_str[:106])]
    cksum_calc = reduce(lambda x, y: x ^ y, byte_list)
    cksum_calc = cksum_calc ^ int('dd', 16)
    sample_data.append(int(cksum_calc == int(cksum, 16)))

    return sample_data


def parse_eeg_str(hex_str):
    if hex_map[hex_str[0]][0] == '0':
        hex_str = '0' * (8 - len(hex_str)) + hex_str
        eeg_value = int(hex_str, 16)
    else:
        hex_str = 'ff' + hex_str
        ones_comp = ''.join([hex_map[d] for d in hex(int(hex_str, 16) - 1)[2:]])
        eeg_value = -1 * int(''.join([compliment[bit] for bit in ones_comp]), 2)

    return (4.5 * 1e6 * eeg_value) / (24 * ((2 ** 23) - 1))


def call_api(method_name, key, api_type='POST', handle_res=True, params=None):
    url = "https://wisdom-sdk-local.azure-api.net/wisdom-sdk-local/" + method_name
    headers = {'Cache-Control': 'no-cache',
               'Ocp-Apim-Subscription-Key': key}

    if api_type == 'POST':
        res = requests.post(url, headers=headers, params=params)
    elif api_type == 'GET':
        res = requests.get(url, headers=headers, params=params)
    else:
        raise RequestError("API type is invalid")

    if handle_res:
        if res.status_code == 401:
            raise AuthFailedError(res.text)
        elif res.status_code == 402:
            raise RequestError(res.text)
        elif res.status_code == 666:
            raise UnexpectedError(res.text)
        elif res.status_code == 200:
            print(res.json())

    return res

