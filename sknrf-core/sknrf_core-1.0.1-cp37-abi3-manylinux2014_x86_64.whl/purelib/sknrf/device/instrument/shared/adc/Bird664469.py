import os
import csv
import time
import logging
import subprocess
import socket

import math as mt
import warnings

import numpy as np
import torch as th
import requests

from sknrf.settings import Settings
from sknrf.device.base import device_logger
from sknrf.utilities.patterns import SingletonType

logger = device_logger(logging.getLogger(__name__))


MEASURE_DELAY = 1.0  # s
ARM_DELAY = 0.4  # s


class Bird664469Controller(object, metaclass=SingletonType):

    def __init__(self, config, id):
        self._config = config
        self.id = id
        self.num_chan = 16
        self.data = 2**15 * th.ones((Settings().t_points, self.num_chan), dtype=th.complex128)

        # Socket Interface
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((self._config["REM_IP"], self._config["REM_SOCKET_PORT"]))
        self.socket = sock

    def get_reg(self, group, group_ind, name):
        cmd_str = 'http://{REM_IP:s}:{REM_PORT:d}/{REM_INTERFACE:s}/{group:s}/{group_ind:d}/{name:s}'.format(
            REM_IP=self._config["REM_IP"], REM_PORT=5000, REM_INTERFACE=self._config["REM_IFACE"],
            group=group, group_ind=group_ind, name=name)
        return requests.get(cmd_str).json()[name]

    def set_reg(self, group, group_ind, name, value):
        cmd_str = 'http://{REM_IP:s}:{REM_PORT:d}/{REM_INTERFACE:s}/{group:s}/{group_ind:d}/'.format(
            REM_IP=self._config["REM_IP"], REM_PORT=self._config["REM_PORT"], REM_INTERFACE=self._config["REM_IFACE"],
            group=group, group_ind=group_ind)
        requests.put(cmd_str, json=dict(((name, value),)))

    def measure(self):

        def scale(x, x_min, x_max, y_min, y_max):
            return (x - x_min) / (x_max - x_min) * (y_max - y_min) + y_min

        loc_db = os.sep.join((Settings().data_root, "testdata", "data.csv"))
        rem_db = os.sep + os.sep.join(("home", "root", "data.csv"))
        rem_cmd = self._config["REM_SCP_DN"].format(FROM=rem_db, TO=loc_db)
        logger.debug(rem_cmd), os.system(rem_cmd + Settings().system_buffers)
        count = self.get_reg("stream_fifo_trigger_control_8", 0, "FIFOReadCount")
        pad = "0"*5
        num_chan = 8
        time.sleep(MEASURE_DELAY)
        with open(loc_db, 'r') as f:
            data_str = f.read()
            data_list = data_str.replace("\n", ", ").split(", ")[0:9*Settings().t_points]
            data_list = ["%s%s" % (pad[:len(pad) - len(i)], i) for i in data_list]
            data_array = np.asarray(data_list, "S5").astype("u2")
            t_points = mt.floor(data_array.shape[0]/9)
            data_array = data_array[0:(num_chan + 1) * t_points].reshape(mt.floor(data_array.shape[0]/9), 9)[:, 1:]
            if len(data_array) == 0:  # No Trigger
                warnings.warn("Bird664469Controller:No Ext trigger")
            elif data_array.shape[0] != Settings().t_points:
                raise AttributeError("Bird664469Controller:Insufficient Time Samples")
            else:
                self.data = th.as_tensor(scale(data_array, 0, (1 << 16) - 1, -0.5, 0.5))


def preset(self):

    ctrl = self.handles["adc"]
    ctrl.socket.sendall(bytes("from {:s} import dac_write\n".format(self._config["FPGA_NAME"]), "utf-8"))
    for i in range(0, 16):
        self.channel = i
        self.adc_offset = 0
    self.channel = 0

    ctrl.set_reg("stream_fifo_trigger_control_8", 0, "trigger_window_size", 4095)  # highest permissible value results in 988 samples
    ctrl.set_reg("{:s}_top_ctrl".format(self._config["FPGA_NAME"]), 0, "ila_testbus_sel", 0)  # Bus Select 0 | 1

    # Clear FIFO
    ctrl.set_reg("stream_fifo_trigger_control_8", 0, "clear_trigger", True)
    ctrl.set_reg("stream_fifo_trigger_control_8", 0, "clear_fifo", 0xffff)
    ctrl.set_reg("stream_fifo_trigger_control_8", 0, "clear_fifo", 0x0000)
    ctrl.set_reg("stream_fifo_trigger_control_8", 0, "clear_trigger", False)

    arm(self)


def arm(self):
    if self.port == 1:
        rem_cmd = "timeout %f %s " % (MEASURE_DELAY, os.sep.join((self._config["REM_ROOT"], "nucleus_adc_dump")))
        loc_cmd = self._config["REM_SSH"].format(REM_CMD=rem_cmd)
        logger.debug(loc_cmd), subprocess.Popen(loc_cmd, shell=True, **Settings().subprocess_buffers)
        time.sleep(ARM_DELAY)


def trigger(self):
    pass


