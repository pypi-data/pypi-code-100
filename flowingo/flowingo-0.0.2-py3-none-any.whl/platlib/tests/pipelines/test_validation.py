import pathlib

import pytest
import yamale

from flowingo.pipelines.validation import pipeline_schema_path, tasks_schema_path, validate_pipeline, validate_task


class TestTasksValidation:
    def test_schema(self):
        assert tasks_schema_path.exists()

        # Test schema reading OK
        schema = yamale.make_schema(tasks_schema_path.absolute())

    @pytest.mark.parametrize(
        "filename,is_valid",
        [
            ("correct_minimal.yml", True),
            ("correct_simple.yml", True),
            ("correct_complex.yml", True),
            # ("invalid_wrong_task_name.yml", False),
            # ("invalid_wrong_task_name_whitespace.yml", False),
            ("invalid_wrong_parameter_type.yml", False),
        ],
    )
    def test_files(self, tasks_folder: pathlib.Path, filename: str, is_valid: bool):
        path = tasks_folder / filename
        assert path.exists(), f'file {filename} does not exist in folder {tasks_folder.absolute()}'

        assert validate_task(tasks_folder, filename) == is_valid

    def test_file_not_exists(self, tasks_folder: pathlib.Path):
        assert not validate_task(tasks_folder, 'not_existed_file.yml')


class TestPipelinesValidation:
    def test_schema(self):
        assert pipeline_schema_path.exists()

        # Test schema reading OK
        schema = yamale.make_schema(pipeline_schema_path.absolute())

    @pytest.mark.parametrize(
        "filename,is_valid",
        [
            ("correct_minimal.yml", True),
            ("correct_simple.yml", True),
            ("correct_complex.yml", True),
            ("correct_inner.yml", True),
            ("invalid_header_missed.yml", False),
            ("invalid_header_properties.yml", False),
            ("invalid_inner_not_exist.yml", False),
            ("invalid_inner_cycle_simple.yml", False),
            ("invalid_inner_cycle_complex.yml", False),
            ("invalid_task_not_exist.yml", False),
            ("invalid_task_wrong_param.yml", False),
            ("invalid_task_wrong_param_type.yml", False),
        ],
    )
    def test_files(self, pipelines_folder: pathlib.Path, pipelines_tasks_folder: pathlib.Path, filename: str, is_valid: bool):
        path = pipelines_folder / filename
        assert path.exists(), f'file {filename} does not exist in folder {pipelines_folder.absolute()}'

        assert validate_pipeline(pipelines_folder, filename, tasks_folder=pipelines_tasks_folder) == is_valid

    def test_validate_warning_without_tasks_folder(self, pipelines_folder: pathlib.Path):
        filename = 'correct_minimal.yml'
        path = pipelines_folder / filename
        assert path.exists(), f'file {filename} does not exist in folder {pipelines_folder.absolute()}'

        with pytest.warns(UserWarning):
            assert validate_pipeline(pipelines_folder, filename, tasks_folder=None)

    def test_file_not_exists(self, pipelines_folder: pathlib.Path):
        assert not validate_pipeline(pipelines_folder, 'not_existed_file.yml')
