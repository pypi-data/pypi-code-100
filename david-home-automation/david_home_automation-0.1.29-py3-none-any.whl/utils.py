import logging
import os
import sys
import typing
from david_home_automation.config import Config, BluetoothThermostat, Host

import yaml

ENV_CONFIG_VARIABLE_NAME = 'HOME_AUTOMATION_CONFIG'
DEFAULT_CONFIG = os.path.expanduser('~/.config/david-home-automation.yaml')


def get_config(config_file: typing.Optional[str] = None):
    if not config_file:
        config_file = os.environ.get(ENV_CONFIG_VARIABLE_NAME, DEFAULT_CONFIG)
    try:
        config_file = os.path.expanduser(config_file)
        with open(config_file) as f:
            config = yaml.load(f, Loader=yaml.Loader)
        # ToDo: this should be done automatically by PyYaml
        out = Config(thermostats=[], hosts=[])
        for host in config.get('hosts', []):
            out.hosts.append(Host(**host))
        for thermostat in config.get('thermostats', []):
            out.thermostats.append(BluetoothThermostat(**thermostat))
        return out
    except Exception as e:
        logging.error(f"Could not parse config {config_file}")
        raise e
