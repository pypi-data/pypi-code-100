import pathlib

from click.testing import CliRunner
from pytest_mock import MockerFixture

from flowingo.__main__ import main
from flowingo.cli.pipeline_command import pipeline


class TestCliPipeline:
    def test_validation(self, cli_runner: CliRunner, mocker: MockerFixture) -> None:
        patch_validate = mocker.patch('flowingo.cli.pipeline_command.validate_pipeline', return_value=True)

        # Test file not exist
        result = cli_runner.invoke(pipeline, ['validate', '.', 'file_not_exits.yml'])
        assert result.exit_code == 2

        # Test file exist, but wrong extension
        with cli_runner.isolated_filesystem():
            with open('file.yeml', 'w') as f:
                f.write('Hello World!')

            result = cli_runner.invoke(pipeline, ['validate', '.', 'file.yeml'])
            assert result.exit_code == 1
            assert result.output == 'file.yeml has wrong extension .yeml (Can be .yaml or .yml)\n', result.output

        # Test file exist, validate always false
        patch_validate.return_value, patch_validate.call_count = False, 0
        with cli_runner.isolated_filesystem():
            with open('file.yml', 'w') as f:
                f.write('Hello World!')

            result = cli_runner.invoke(pipeline, ['validate', '.', 'file.yml'])
            assert result.exit_code == 1
            assert result.output == 'pipeline file.yml is NOT valid!\n', result.output
        patch_validate.assert_called_once()

        # Test file exist, validate always True
        patch_validate.return_value, patch_validate.call_count = True, 0
        with cli_runner.isolated_filesystem():
            with open('file.yml', 'w') as f:
                f.write('Hello World!')

            result = cli_runner.invoke(pipeline, ['validate', '.', 'file.yml'])
            assert result.exit_code == 0
            assert result.output == 'pipeline file.yml is valid!\n', result.output
            patch_validate.assert_called_once()

            # Call from main
            result = cli_runner.invoke(main, ['pipeline', 'validate', '.', 'file.yml'])
            assert result.exit_code == 0
