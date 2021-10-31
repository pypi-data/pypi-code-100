from click.testing import CliRunner
from pytest_mock import MockerFixture

from flowingo.__main__ import main
from flowingo.cli.db_command import db


class TestCliDb:
    def test_init(self, cli_runner: CliRunner, mocker: MockerFixture) -> None:
        patch = mocker.patch('flowingo.cli.db_command.init_db')

        result = cli_runner.invoke(db, ['init'])
        assert result.exit_code == 0

        patch.assert_called_once()

        # Call from main
        result = cli_runner.invoke(main, ['db', 'init'])
        assert result.exit_code == 0

