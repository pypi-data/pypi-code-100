import json
import logging
import subprocess
import typing
from dataclasses import dataclass
from subprocess import CalledProcessError


@dataclass
class Host(object):
    name: str
    mac_address: str
    broadcast_ip: str = '255.255.255.255'


@dataclass
class BluetoothThermostat(object):
    name: str
    mac_address: str
    temperature: typing.Optional[float] = None
    status: typing.Optional[dict] = None

    def eq3_cmd(self, cmd):
        return f'eq3.exp {self.mac_address} {cmd}'

    def execute_eq3_cmd(self, cmd, tries: int = 2):
        whole_command = f'{self.eq3_cmd(cmd)}'.split(' ')
        for x in range(tries):
            try:
                return subprocess.check_output(whole_command).decode('utf-8')
            except CalledProcessError as e:
                logging.error(f'Could not execute command: {whole_command}. Retrying', exc_info=e)
        logging.error(f'Could not execute command: {whole_command}')
        raise Exception(f'Command "{whole_command}" exited with non-zero code after {tries} tries')

    def get_temperature(self):
        if not self.status:
            self.sync()
        self.temperature = self.status.get('temperature')
        return self.temperature

    def sync(self):
        self.status = json.loads(self.execute_eq3_cmd('json'))
        return self.status


@dataclass
class Config(object):
    hosts: typing.List[Host]
    thermostats: typing.List[BluetoothThermostat]

    def get_host_by_name(self, name: str) -> typing.Optional[Host]:
        return self._get_by('hosts', name)

    def get_thermostat_by_name(self, name: str) -> typing.Optional[BluetoothThermostat]:
        return self._get_by('thermostats', name)

    def _get_by(self, attr: str, name: str):
        for el in getattr(self, attr):
            if el.name == name:
                return el
        return None
