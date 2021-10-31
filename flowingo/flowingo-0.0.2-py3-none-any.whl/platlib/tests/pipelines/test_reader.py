import pathlib

import pytest

from flowingo.pipelines.reader import read_pipeline, read_related_pipelines, read_task, read_yml


class TestYamlReader:
    @pytest.mark.parametrize(
        "filename",
        [
            "correct_minimal.yml",
            "correct_simple.yml",
            "correct_complex.yml",
        ],
    )
    def test_files(self, pipelines_folder: pathlib.Path, filename):
        path = pipelines_folder / filename
        assert path.exists(), f'file {filename} does not exist in folder {pipelines_folder.absolute()}'

        # Reading ok
        read_yml(path)


class TestTaskReader:
    @pytest.mark.parametrize(
        "filename",
        [
            "correct_minimal.yml",
            "correct_simple.yml",
            "correct_complex.yml",
        ],
    )
    def test_files(self, tasks_folder: pathlib.Path, filename):
        path = tasks_folder / filename
        assert path.exists(), f'file {filename} does not exist in folder {tasks_folder.absolute()}'

        # Reading ok
        read_task(tasks_folder, filename)


class TestPipelinesReader:
    @pytest.mark.parametrize(
        "filename",
        [
            "correct_minimal.yml",
            "correct_simple.yml",
            "correct_complex.yml",
        ],
    )
    def test_single_pipeline(self, pipelines_folder: pathlib.Path, filename):
        path = pipelines_folder / filename
        assert path.exists(), f'file {filename} does not exist in folder {pipelines_folder.absolute()}'

        # Reading ok
        read_pipeline(pipelines_folder, filename)

    @pytest.mark.parametrize(
        "filename,pipelines",
        [
            ("correct_minimal.yml", []),
            ("correct_simple.yml", []),
            ("correct_complex.yml", ['correct_simple.yml', 'correct_minimal.yml']),
            ("correct_inner.yml", ['correct_minimal.yml']),
            ("invalid_header_missed.yml", []),
            ("invalid_header_properties.yml", []),
        ],
    )
    def test_multiple_pipelines(self, pipelines_folder: pathlib.Path, filename, pipelines):
        path = pipelines_folder / filename
        assert path.exists(), f'file {filename} does not exist in folder {pipelines_folder.absolute()}'

        # Reading ok
        related_pipelines = read_related_pipelines(pipelines_folder, filename)
        assert related_pipelines.keys() == {filename, *pipelines}
