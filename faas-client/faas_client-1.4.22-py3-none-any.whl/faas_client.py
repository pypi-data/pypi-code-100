import os.path
import re
from io import StringIO

import sh


def build_env_options(env):
    return [f'-e {key}={value}' for (key, value) in env.items()]


class FaasClient:
    def __init__(self, gateway_url, gateway_port, username, password):
        self.__cli = sh.Command('faas-cli')
        self.endpoint = f'{gateway_url}:{gateway_port}'
        self.__username = username
        self.__password = password

    def login(self):
        result = self.__cli('login',
                            '-g', self.endpoint,
                            '--username', self.__username,
                            '--password', self.__password)
        return result.exit_code

    def build(self, path_to_faas_configuration, function_name):
        configuration_filename = os.path.basename(path_to_faas_configuration)
        result = self.__cli(
            'build',
            '-f', configuration_filename,
            '--filter', function_name,
            _cwd=os.path.dirname(path_to_faas_configuration))
        return result.exit_code

    def push(self, path_to_faas_configuration, function_name):
        configuration_filename = os.path.basename(path_to_faas_configuration)
        result = self.__cli(
            'push',
            '-f', configuration_filename,
            '--filter', function_name,
            _cwd=os.path.dirname(path_to_faas_configuration))
        return result.exit_code

    def deploy(self, path_to_faas_configuration, function_name, env={}):
        env_options = build_env_options(env)
        result = self.__cli(
            'deploy',
            '-f', path_to_faas_configuration,
            '--filter', function_name,
            '-g', self.endpoint,
            ' '.join(env_options))
        return result.exit_code

    def is_ready(self, function_name):
        output_buffer = StringIO()
        result = self.__cli(
            'describe', function_name,
            '-g', self.endpoint,
            _out=output_buffer
        )
        assert result.exit_code == 0
        description = output_buffer.getvalue()
        m = re.search(r'Status:\s*(.*)\n', description)
        return m.group(1) == 'Ready' if m else False


class FaasClientFactory:
    def __init__(self, gateway_port):
        self.__gateway_port = gateway_port

    def create(self, gateway_url, username, password):
        return FaasClient(
            gateway_url,
            self.__gateway_port,
            username,
            password)
