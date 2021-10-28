import time
from threading import Thread

import pandas as pd
from scipy.io import savemat
import serial
import socket
from streamz import Stream
import numpy as np
from wisdom.utils import *
from pyedflib import highlevel
from wisdom.preprocessing.filter_utils import apply_filters
import h5py

file_exts = {'npy', 'csv', 'edf', 'txt', 'mat'}


class EEGStream:
    def __init__(self, device):
        self.ip_addr, self.port_num = device.ip_addr, device.port_num
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.bind((self.ip_addr, self.port_num))
        self.sock.settimeout(2)
        self.samples_per_packet = 5
        self.sample_size = 54
        self.socket_buffer_size = 1024
        self.sampling_rate = 976.5625
        self.sample_len = 21
        self.server_on = False
        self.ser = None
        self.subscription_key = device.subscription_key
        self.deviceID = device.deviceID
        self.server_thread = None
        self.raw_stream = Stream()
        self.parsed_stream = Stream()
        self.aux_stream = Stream()
        self.eeg_stream = Stream()
        self.filters_object = None

    def __start_server_thread(self):
        while self.server_on:
            data, addr = self.sock.recvfrom(self.socket_buffer_size)
            hex_data = data.hex()
            s = 0
            for i in range(self.samples_per_packet):
                self.raw_stream.emit(hex_data[s:s + 108])
                s += 108

    def start_server(self):
        params = {'deviceid': self.deviceID}
        res = call_api('startStreamingData', self.subscription_key, api_type='POST', handle_res=True, params=params)

        self.server_on = True
        self.parsed_stream = self.raw_stream.map(parse_sample)
        self.eeg_stream = self.parsed_stream.map(stream_eeg_only)
        self.server_thread = Thread(target=self.__start_server_thread)
        self.server_thread.start()

        return res

    def stop_server(self):
        self.server_on = False
        self.server_thread.join()

        params = {'deviceid': self.deviceID}
        res = call_api('stopStreamingData', api_type='POST', key=self.subscription_key, handle_res=True, params=params)

        return res

    def establish_serial(self, com_port):
        self.ser = serial.Serial()
        self.ser.baudrate = 2000000
        self.ser.com_port = com_port
        try:
            self.ser.close()
            time.sleep(2)
            self.ser.open()
        except serial.SerialException:
            raise SerialConnectionError

    def data_vis(self, s_name=None, **kwargs):
        return pd.DataFrame(s_name.current_value[:, :16], columns=column_names[:16], index=s_name.current_value[:, 16])

    def send_marker(self, marker):
        try:
            assert 1
        except AssertionError:
            raise ValidationError(
                "The marker is not in valid format. Refer to documentation for the correct marker format.")

        try:
            self.ser.write(marker)
        except serial.SerialException:
            raise SerialConnectionError

    def applyfiltering(self, filters, buf_size=1000):
        return self.eeg_stream.partition(buf_size).map(apply_filters, filters)

    @staticmethod
    def store_stream(stream_name):
        lst = stream_name.sink_to_list()
        return lst

    @staticmethod
    def export_stream(store, file_name, file_ext='txt'):
        lst = np.array(store)
        dims = len(lst.shape)
        if dims == 3:
            lst = lst.reshape(lst.shape[0]*lst.shape[1], lst.shape[2])

        cols = lst.shape[1]

        if file_ext not in file_exts:
            print("Not a valid file extension, using default value.")
            file_ext = 'txt'
        if file_ext == 'npy':
            np.save(f"{file_name}.npy", lst)
        elif file_ext == 'csv':
            df = pd.DataFrame(data=lst, index=None, columns=column_names[:cols])
            df.to_csv(f"{file_name}.csv", index=False)
            del df
        elif file_ext == 'edf':
            signal_headers = highlevel.make_signal_headers(column_names[:cols], sample_rate=SAMPLING_FREQUENCY,
                                                           physical_min=-80000, physical_max=80000,
                                                           digital_min=-1875000, digital_max=1875000)
            highlevel.write_edf(f'{file_name}.edf', lst.T, signal_headers)
        elif file_ext == 'mat':
            data = {"data": lst, "cols": column_names[:cols]}
            savemat(f"{file_name}", mdict=data)
            del data
        else:
            np.savetxt(f"{file_name}.txt", lst)

