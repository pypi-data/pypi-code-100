import os
import abc
import logging
import paramiko
import shutil

from sknrf.settings import Settings

__author__ = 'dtbespal'
logger = logging.getLogger(__name__)


class SimulatorError(Exception):
    pass


class AbstractSimulator(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, netlist_filename, dataset_filename,
                 remote_host="", remote_user="", remote_password="", remote_key_filename="", remote_port=22):
        self._netlist_filename, self._dataset_filename = "", ""
        self._remote_netlist_filename, self._remote_dataset_filename = "", ""
        self._remote_ssh = None
        self.remote_host = remote_host
        self.remote_user = remote_user
        self.remote_password = remote_password
        self.remote_key_filename = remote_key_filename
        self._connect_remote(remote_host, remote_user, remote_password, remote_key_filename, remote_port)
        self.set_netlist_filename(netlist_filename)
        self.set_dataset_filename(dataset_filename)

    def __del__(self):
        if self.is_remote():
            try:
                self._remote_ssh.close()
            except Exception:
                logger.error("Remote Connection did not close correctly", exc_info=True)
                raise

    def _set_filename(self, filename, mode="rt"):
        if self.is_remote():
            original_local_filename = self._get_remote_file(filename)
            filename_, ext = os.path.splitext(original_local_filename)
            local_filename = filename_ + "_sknrf" + ext
            original_remote_filename = filename
            filename_, ext = os.path.splitext(original_remote_filename)
            remote_filename = filename_ + "_sknrf" + ext
            if not self._is_remote_file(remote_filename):
                shutil.copyfile(original_local_filename, local_filename)
                self._put_remote_file(remote_filename)
        else:
            original_local_filename = filename
            filename_, ext = os.path.splitext(original_local_filename)
            local_filename = filename_ + "_sknrf" + ext
            remote_filename = ""
            if not os.path.isfile(local_filename):
                shutil.copyfile(original_local_filename, local_filename)
        try:
            file = open(local_filename, mode)
        except IOError:
            logger.error("Unable to open: " + local_filename, exc_info=True)
            raise
        else:
            file.close()
            return local_filename, remote_filename

    def set_netlist_filename(self, netlist_filename):
        self._netlist_filename, self._remote_netlist_filename = self._set_filename(netlist_filename, "at")

    def set_dataset_filename(self, dataset_filename):
        self._dataset_filename, self._remote_dataset_filename = self._set_filename(dataset_filename, "rt")

    def is_remote(self):
        return self._remote_ssh

    def _connect_remote(self, host, user, password="", key="", port=22):
        if not host or not user:
            self._remote_ssh = None
            return
        try:
            self._remote_ssh = paramiko.SSHClient()
            self._remote_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if password:
                self._remote_ssh.connect(host, username=user, password=password, port=port)
            else:
                mykey = paramiko.RSAKey.from_private_key_file(key)
                self._remote_ssh.connect(host, username=user, pkey=mykey, port=port)
        except paramiko.ssh_exception.PasswordRequiredException:
            logger.error("Remote system required password authentication, please configure RSA key", exc_info=True)
            raise
        except paramiko.ssh_exception.SSHException:
            logger.error("Unable to open remote connection", exc_info=True)
            raise

    def _is_remote_file(self, remote_filename):
        filepath, filename = os.path.split(remote_filename)
        sftp = self._remote_ssh.open_sftp()
        return filename in sftp.listdir(filepath)

    def _get_remote_file(self, remote_filename):
        _, filename = os.path.split(remote_filename)
        local_filename = os.sep.join((Settings().data_root, "simulation", filename))
        sftp = self._remote_ssh.open_sftp()
        try:
            sftp.get(remote_filename, local_filename)
        except IOError:
            logger.error("Could not get: " + remote_filename, exc_info=True)
            raise
        else:
            return local_filename

    def _put_remote_file(self, remote_filename):
        _, filename = os.path.split(remote_filename)
        local_filename = os.sep.join([Settings().data_root, "simulation", filename])
        sftp = self._remote_ssh.open_sftp()
        try:
            sftp.put(local_filename, remote_filename)
        except IOError:
            logger.error("Could not put: " + remote_filename, exc_info=True)
            raise

    def preset(self):
        """ Preset the simulation netlist
        :return:
        """
        filename, ext = os.path.splitext(self._netlist_filename)
        shutil.copyfile(filename[:-6] + ext, filename + ext)
        filename, ext = os.path.splitext(self._dataset_filename)
        shutil.copyfile(filename[:-6] + ext, filename + ext)

    @abc.abstractmethod
    def add(self, name, value):
        """ Adds variable name to the end of the netlist with value
        :param name: added variable name
        :param value: added variable value
        """
        pass

    @abc.abstractmethod
    def add_block(self, block):
        """ Adds general purpose code-block to the netlist file
        :param block: A netlist code block
        """
        pass

    @abc.abstractmethod
    def read_netlist(self, name):
        """ Reads the value of a netlist variable "name". Sub-component variables are specified with "group.name" notation
        :param name: name of the netlist variable
        :return value: value of the netlist variable
        """
        pass

    @abc.abstractmethod
    def write(self, name, value, add_string_quotes=True):
        """ Writes the "value" of netlist variable "name". Sub-component variables are specified with "group.name" notation
        :param name: name of the netlist variable
        :param value: value of the netlist variable
        :param add_string_quotes: optional flag to wrap string values with double quotes, default=True
        """
        pass

    @abc.abstractmethod
    def measure(self, shell_options="", timeout=None):
        """ Run the simulation in the command line
        :param shell_options: shell option string
        :param timeout: simulation time-out in seconds
        :return (result, log): simulator exit status (0 = success), shell stdout string
        """
        pass

    @abc.abstractmethod
    def read(self, name, sweep_idx=slice(None), freq_idx=slice(None), time_idx=slice(None)):
        """ Reads the value of a dataset variable "name"[sweep_idx, freq_idx, time_idx]
        :param name: name of dataset variable
        :param sweep_idx: parameter sweep index
        :param freq_idx: frequency sweep index
        :param time_idx: time sweep index
        :return value: 3D array (sweep_idx.size, freq_idx.size, time_idx.size) of dataset value
        """
        pass
