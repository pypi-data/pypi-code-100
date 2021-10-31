import pathlib
from typing import Any, List

import pytest
from click.testing import CliRunner
from pytest_mock import MockerFixture

from flowingo.__main__ import main
from flowingo.cli.manager_command import manager
from flowingo.configuration import conf


class TestCliManager:
    class _TestWorker:
        def __init__(self, *args, **kwargs):
            pass

        def start(self):
            pass

    def test_start_worker(self, cli_runner: CliRunner, class_mocker: MockerFixture) -> None:
        patch = class_mocker.patch('flowingo.cli.manager_command.app.Worker', self._TestWorker)

        result = cli_runner.invoke(manager, [])
        assert result.exit_code == 0

        # patch.assert_called_once_with()

        # Call from main
        result = cli_runner.invoke(main, ['manager'])
        assert result.exit_code == 0

    @pytest.mark.parametrize(
        'cli_flag_parameter,conf_parameter',
        [
            ('--demonize', 'manager_demonize'),
        ]
    )
    def test_conf_flags_as_parameters(self, cli_runner: CliRunner, class_mocker: MockerFixture, cli_flag_parameter: str, conf_parameter: str):
        patch = class_mocker.patch('flowingo.cli.manager_command.app.Worker', self._TestWorker)

        result = cli_runner.invoke(manager, [cli_flag_parameter])
        assert result.exit_code == 0
        assert conf.__getattribute__(conf_parameter)

        result = cli_runner.invoke(manager, [])
        assert result.exit_code == 0
        assert not conf.__getattribute__(conf_parameter)

    @pytest.mark.parametrize(
        'cli_option_parameter,conf_parameter,values',
        [
            ('--pipelines', 'pipelines_folder', ['.', 'pipelines', './pipelines']),
            ('--tasks', 'tasks_folder', ['.', 'tasks', './tasks']),
        ]
    )
    def test_conf_folders_as_parameters(self, cli_runner: CliRunner, class_mocker: MockerFixture, cli_option_parameter: str, conf_parameter: str, values: List[str]):
        patch = class_mocker.patch('flowingo.cli.manager_command.app.Worker', self._TestWorker)

        for value in values:
            with cli_runner.isolated_filesystem():
                pathlib.Path(value).mkdir(exist_ok=True)

                result = cli_runner.invoke(manager, [cli_option_parameter, value])
                assert result.exit_code == 0

                assert conf.__getattribute__(conf_parameter) == value

    def test_not_existed_folders_as_parameters(self, cli_runner: CliRunner):
        result = cli_runner.invoke(manager, ['--pipelines', 'not_existed_folder'])
        assert result.exit_code == 2
        result = cli_runner.invoke(manager, ['--tasks', 'not_existed_folder'])
        assert result.exit_code == 2
