from os.path import join
from tempfile import TemporaryDirectory
from unittest import mock

from click.testing import CliRunner
from pandas import DataFrame

from cesar_puc_csv_converter import main


def test_should_run_converter_to_csv(
    mocker: mock.Mock, example_dataset: DataFrame
) -> None:

    fake_read_csv_file = mocker.patch.object(main, 'read_csv_file')
    fake_save_to_json_files = mocker.patch.object(main, 'save_to_json_files')
    runner = CliRunner()

    with TemporaryDirectory() as tmpdirname:

        path_file = join(tmpdirname, 'example-file.csv')
        example_dataset.to_csv(path_file)

        result = runner.invoke(
            main.converter,
            [
                'csv',
                '--input',
                path_file,
                '--output',
                tmpdirname,
            ],
        )

    fake_read_csv_file.assert_called_once()
    fake_save_to_json_files.assert_called_once()

    assert result.exit_code == 0


def test_should_run_converter_to_json(
    mocker: mock.Mock, example_dataset: DataFrame
) -> None:

    fake_read_json_file = mocker.patch.object(main, 'read_json_file')
    fake_save_to_csv_files = mocker.patch.object(main, 'save_to_csv_files')
    runner = CliRunner()

    with TemporaryDirectory() as tmpdirname:

        path_file = join(tmpdirname, 'example-file.json')
        example_dataset.to_json(path_file)

        result = runner.invoke(
            main.converter,
            [
                'json',
                '--input',
                path_file,
                '--output',
                tmpdirname,
            ],
        )

    fake_read_json_file.assert_called_once()
    fake_save_to_csv_files.assert_called_once()

    assert result.exit_code == 0


def test_should_raise_error_if_not_file_to_converter() -> None:
    runner = CliRunner()
    result = runner.invoke(
        main.converter,
        [
            'csv',
            '--input',
            '/dev/null',
        ],
    )

    assert result.exit_code == 1
    assert str(result.exception) == 'Not a valid path or file name. /dev/null'
