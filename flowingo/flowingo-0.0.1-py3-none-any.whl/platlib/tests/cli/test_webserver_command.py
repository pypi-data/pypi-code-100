from typing import List

import pytest
from click.testing import CliRunner
from pytest_mock import MockerFixture

from flowingo.__main__ import main
from flowingo.cli.webserver_command import webserver
from flowingo.configuration import conf


class TestCliWebserver:
    def test_init(self, cli_runner: CliRunner, mocker: MockerFixture) -> None:
        patch = mocker.patch('flowingo.cli.webserver_command.uvicorn.run')

        result = cli_runner.invoke(webserver, [])
        assert result.exit_code == 0

        patch.assert_called_once()

        # Call from main
        result = cli_runner.invoke(main, ['webserver'])
        assert result.exit_code == 0

    @pytest.mark.parametrize(
        'cli_flag_parameter,conf_parameter',
        [
            ('--debug', 'webserver_debug'),
            ('--demonize', 'webserver_demonize'),
        ]
    )
    def test_conf_flags_as_parameters(self, cli_runner: CliRunner, mocker: MockerFixture, cli_flag_parameter: str, conf_parameter: str):
        patch = mocker.patch('flowingo.cli.webserver_command.uvicorn.run')

        result = cli_runner.invoke(webserver, [cli_flag_parameter])
        assert result.exit_code == 0
        assert conf.__getattribute__(conf_parameter)

        result = cli_runner.invoke(webserver, [])
        assert result.exit_code == 0
        assert not conf.__getattribute__(conf_parameter)

    @pytest.mark.parametrize(
        'cli_option_parameter,conf_parameter,values',
        [
            ('--port', 'webserver_port', [8080, 5923, 3000]),
        ]
    )
    def test_conf_parameters(self, cli_runner: CliRunner, mocker: MockerFixture, cli_option_parameter: str, conf_parameter: str, values: List[str]):
        patch = mocker.patch('flowingo.cli.webserver_command.uvicorn.run')

        for value in values:
            result = cli_runner.invoke(webserver, [cli_option_parameter, value])
            assert result.exit_code == 0

            assert conf.__getattribute__(conf_parameter) == value
