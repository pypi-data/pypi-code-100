import os
import re
import time
import subprocess
import logging

import numpy as np
from scipy.io import loadmat

from sknrf.device.simulator.base import AbstractSimulator, SimulatorError
from sknrf.settings import Settings

__author__ = 'dtbespal'
logger = logging.getLogger(__name__)


class ADSSimulator(AbstractSimulator):
    """ Remote Control over Keysight ADS Simulator using read/write of ADS netlist file and read of .mat dataset file
        Used to write input conditions to an existing ADS netlist file, performs the simulation, and then collect
        simulation results from a .mat dataset file
    """

    def __init__(self, netlist_filename, dataset_filename, simulator_type, simulator_name, config_filename="",
                 remote_host="", remote_user="", remote_password="", remote_key_filename="", remote_port=22):
        super(ADSSimulator, self).__init__(netlist_filename, dataset_filename,
                                           remote_host=remote_host, remote_user=remote_user,
                                           remote_password=remote_password, remote_key_filename=remote_key_filename,
                                           remote_port=remote_port)

        self._simulator_type = ""
        self._simulator_name = ""
        self._config_filename, self._remote_config_filename = "", ""
        # self.set_config_filename(config_filename)

        # Set the Simulator ID
        self.order = 5
        self.simulator_type = simulator_type
        self.simulator_name = simulator_name

        # Todo Copy the Workspace config file to the local folder
        # Todo check to see that pc environment is configured for running ADS from the command line

    def set_config_filename(self, config_filename):
        self._config_filename, self._remote_config_filename = self._set_filename(config_filename, "rt")

    @property
    def simulator_type(self):
        """ ADS Simulator Type get method.
        :return: simulator_name eg("HB")
        """
        return self._simulator_type

    @simulator_type.setter
    def simulator_type(self, simulator_type):
        """ ADS Simulator Type set method.
        :param: simulator_type eg("HB")
        """
        self._simulator_type = simulator_type

    @property
    def simulator_name(self):
        """ ADS Simulator Name get method.
        :return: simulator_name eg("HB1")
        """
        return self._simulator_name

    @simulator_name.setter
    def simulator_name(self, simulator_name):
        """ ADS Simulator Name set method.
        :param simulator_name: simulator_name eg("HB1")
        :return:
        """
        self._simulator_name = simulator_name

    @property
    def simulator_id(self):
        """ ADS Simulator ID get method.
        :return simulator_id: simulator_name.simulator_type
        """
        return self.simulator_name + "." + self.simulator_type

    def preset(self):
        super(ADSSimulator, self).preset()
        # filename, ext = os.path.splitext(self._config_filename)
        # shutil.copyfile(filename[:-7] + ext, filename + ext)

        # Pre-Format Netlist File for easier parsing:
        # Convert mutli-line blocks to single line for easier parsing
        with open(self._netlist_filename, "rt") as file:
            file_str = file.read()
            file_str = re.sub(r"\s+\\\s*\n", " ", file_str)

        with open(self._netlist_filename, "wt") as file:
            print(file_str, file=file, sep="", end="", flush=True)

        # Write the Dataset filename to the netlist
        if self.is_remote():
            self.write(r'MatlabOutput.Argument\[0\]', self._remote_dataset_filename)
        else:
            self.write(r'MatlabOutput.Argument\[0\]', self._dataset_filename)

        try:
            self.write(self.simulator_name + ".Stop", Settings().t_stop)
            self.write(self.simulator_name + ".Step", Settings().t_step)
            self.write("_fund_1", Settings().f0)
            if int(self.read_netlist(self.simulator_name + ".Order\[1\]").real) < Settings().num_harmonics:
                raise ValueError("Number of harmonics: " + str(Settings().num_harmonics) + "exceeds maximum harmonics: 5")
        except AttributeError:
            logger.warning("Could not preset simulator controller")

        # Initialize the IQ files to CW values
        for port_index in range(1, 3):
            np.savetxt(os.sep.join((Settings().data_root,"simulation", "V%d%d_I.txt" % (port_index, 0))),
                           np.ones(Settings().t_points, dtype=np.float64).reshape((1, -1)))
            np.savetxt(os.sep.join((Settings().data_root,"simulation", "V%d%d_Q.txt" % (port_index, 0))),
                           np.zeros(Settings().t_points, dtype=np.float64).reshape((1, -1)))
            np.savetxt(os.sep.join((Settings().data_root,"simulation", "Z%d%d_I.txt" % (port_index, 0))),
                           np.ones(Settings().t_points, dtype=np.float64).reshape((1, -1)))
            np.savetxt(os.sep.join((Settings().data_root,"simulation", "Z%d%d_Q.txt" % (port_index, 0))),
                           np.zeros(Settings().t_points, dtype=np.float64).reshape((1, -1)))
            for harm_idx in range(1, 6):
                np.savetxt(os.sep.join((Settings().data_root,"simulation", "A%d%d_I.txt" % (port_index, harm_idx))),
                           np.ones(Settings().t_points, dtype=np.float64).reshape((1, -1)))
                np.savetxt(os.sep.join((Settings().data_root,"simulation", "A%d%d_Q.txt" % (port_index, harm_idx))),
                           np.zeros(Settings().t_points, dtype=np.float64).reshape((1, -1)))
                np.savetxt(os.sep.join((Settings().data_root,"simulation", "Z%d%d_I.txt" % (port_index, harm_idx))),
                           np.ones(Settings().t_points, dtype=np.float64).reshape((1, -1)))
                np.savetxt(os.sep.join((Settings().data_root,"simulation", "Z%d%d_Q.txt" % (port_index, harm_idx))),
                           np.zeros(Settings().t_points, dtype=np.float64).reshape((1, -1)))

    def add(self, name, value):
        if isinstance(value, (int, float, complex)):
            formatted_value = str(value)
        elif isinstance(value, str):
            formatted_value = '"' + value + '"'
        else:
            formatted_value = ""

        with open(self._netlist_filename, "at") as file:
            file.write("%s=%s\n" % (name, formatted_value))

    def add_block(self, block):
        block = re.sub(r"\s+\\\s*\n", " ", block)
        # block = re.sub(r"\\", r"\\\\", block)
        with open(self._netlist_filename, "at") as file:
            file.write("%s\n" % block)

    def read_netlist(self, name):
        try:
            group, name = re.split(r"\.", name)
        except ValueError:
            group = ""
        with open(self._netlist_filename, "rt") as file:
            file_str = file.read()
        try:
            value = re.search(group + r".*" + name + r"\s*=\s*(\S*).*", file_str).group(1)
        except AttributeError:
            logger.error("Unknown Netlist Variable: %s" % name, exc_info=True)
            raise
        if value[0] == '"' and value[-1] == '"':
            return value[1:-1:1]
        else:
            value = value.replace("*j", "j").replace("j*", "1j*").replace("list", "").replace(")", ",)")
            array_value = np.array(eval(value), dtype=np.complex128)
            return array_value

    def write(self, name, value, add_string_quotes=True):
        try:
            group, name = re.split(r"\.", name)
        except ValueError:
            group = ""
        if isinstance(value, (np.ndarray, list, tuple)):
            formatted_value = str(np.array(value).ravel())[1:-1].strip().replace("j", "*j,")
            formatted_value = re.sub(r"\s+", r"", formatted_value)
            formatted_value = "list(" + formatted_value[0:-1] + ")"
        elif isinstance(value, (complex, int, float)):
            formatted_value = str(value).replace("(", "").replace(")", "").replace("j", "*j")
        elif isinstance(value, str):
            formatted_value = re.sub(r"\\", r"\\\\", value)
            if add_string_quotes:
                formatted_value = '"' + formatted_value + '"'
        else:
            raise ValueError("Unsupported Netlist Variable Type: " + str(type(value)))

        formatted_group = re.sub(r"\\", r"", group)
        formatted_name = re.sub(r"\\", r"", name)
        with open(self._netlist_filename, "rt") as file:
            file_str = file.read()
        (file_str, num_subs) = re.subn(group + r"(.*)" + name + r"\s*=\s*(\S*)(.*)",
                                       r"%s\1%s=%s\3" % (formatted_group, formatted_name, formatted_value), file_str)
        if num_subs < 1:
            raise AttributeError("Unknown Netlist Variable: %s" % name)
        if num_subs > 1:
            raise AttributeError("Duplicate Netlist Variable: %s" % name)

        with open(self._netlist_filename, "wt") as file:
            print(file_str, file=file, sep="", end="", flush=True)

    def import_iq(self, shell_options="", timeout=20):
        if self.is_remote():
            path, _ = os.path.split(self._remote_netlist_filename)
            remote_netlist_filename = path + "load_iq.txt"
            self._put_remote_file(remote_netlist_filename)
            cmd = "hpeesofsim " + remote_netlist_filename + " " + shell_options
            stdin_file, stdout_file, stderr_file = self._remote_ssh.exec_command(cmd, timeout=timeout)
            time.sleep(3) # Wait for dataset file to be written
            # Todo remove dataset generation delay
            self._get_remote_file(self._remote_dataset_filename)
            log = stdout_file.read()
            result = -1 if stderr_file.read() else 0
        else:
            netlist_filename = self._netlist_filename
            cmd = "hpeesofsim " + netlist_filename + " " + shell_options
            log = subprocess.call(cmd, shell=True, timeout=timeout)
            result = 0
        if result < 0:
            raise SimulatorError(log)
        return result, log

    def measure(self, shell_options="", timeout=50):
        if self.is_remote():
            self._put_remote_file(self._remote_netlist_filename)
            cmd = "hpeesofsim " + self._remote_netlist_filename + " " + shell_options
            stdin_file, stdout_file, stderr_file = self._remote_ssh.exec_command(cmd, timeout=timeout)
            time.sleep(3) # Wait for dataset file to be written
            # Todo remove dataset generation delay
            self._get_remote_file(self._remote_dataset_filename)
            log = stdout_file.read()
            result = -1 if stderr_file.read() else 0
        else:
            cmd = "hpeesofsim " + self._netlist_filename + " " + shell_options
            log = subprocess.call(cmd, shell=True, timeout=timeout)
            result = 0
        if result < 0:
            raise SimulatorError(log)
        return result, log

    def read(self, name, sweep_idx=slice(None), freq_idx=slice(None), time_idx=slice(None)):

        # Assume the first dataset
        dataset_container = loadmat(self._dataset_filename)
        datasets = (k for k in dataset_container.keys() if k[0] is not '_')
        dataset = dataset_container[datasets.__next__()][0, 0]

        # Find the data_blocks for the selected simulator_id
        block = None
        dep_idx = None
        data_blocks = np.reshape(dataset['dataBlocks'], dataset['dataBlocks'].size)
        data_blocks_gen = (db for db in data_blocks if self.simulator_id in db['name'][0])
        for data_block in data_blocks_gen:
            for dep_var_idx, dep_var in enumerate(data_block['dependents'][0, :]):
                if name == dep_var[0]:
                    block = data_block
                    dep_idx = dep_var_idx
                    break

        if block is None:
            raise KeyError("Simulator ID: " + self.simulator_id + " not found in dataset")
        if dep_idx is None:
            raise KeyError("Measurement Variable: " + name + " not found in " + self.simulator_id)

        # Extract the Measurment Data Based on the Simulation Type
        if block['type'][0] == 'DC':
            var_length, freq_length = np.shape(block['data'][0]['dependents'][0])
            sweep_length = block['data'][0]['sweep'].size
            time_length = 1
        else:  # Assume block['type'][0] == 'HarmonicBalance':
            var_length, freq_length = np.shape(block['data'][0]['dependents'][0])
            if block['sweeps'].size and block['sweeps'][0, -1][0] == 'time':
                sweep_length = block['data'][0]['sweep'][0].size
                time_length = int(block['data'][0]['sweep'].size/sweep_length)
            else:
                sweep_length = block['data'][0]['sweep'].size
                time_length = 1
        # else:
        #     raise AttributeError("Simulator ID: " + self.simulator_id + " could not be found in dataset")
        sweep_idx = np.arange(sweep_length)[sweep_idx].reshape(-1, 1, 1, 1)
        freq_idx = np.arange(freq_length)[freq_idx].reshape(1, 1, -1, 1)
        time_idx = np.arange(time_length)[time_idx].reshape(1, 1, 1, -1)
        sweep_data = np.concatenate(block['data'][0]['dependents'])
        sweep_data = sweep_data.reshape((sweep_length, time_length, var_length, freq_length))
        sweep_data = sweep_data.swapaxes(1, 3)
        sweep_data = sweep_data.swapaxes(1, 2)

        # Todo Integrate preceding code into measure or batch_measure methods
        return sweep_data[sweep_idx, dep_idx, freq_idx, time_idx].reshape(sweep_idx.size, freq_idx.size, time_idx.size)


if __name__ == "__main__":
    ads = ADSSimulator("ads_unit_test_netlist.txt", "ads_unit_test_dataset.mat",
                       "DC", "DC1",
                       remote_host=Settings().remote_host, remote_user=Settings().remote_user,
                       remote_key_filename=Settings().remote_key_file)
    var1 = ads.read_netlist("NumericVar1")
    ads.write("NumericVar1", 12)
    var1_ = ads.read_netlist("NumericVar1")
    result_, log_ = ads.measure()
    meas1 = ads.read("Meas1")
