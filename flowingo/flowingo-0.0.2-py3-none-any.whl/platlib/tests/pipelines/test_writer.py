import pathlib
import shutil
import sys
from uuid import uuid1

import pytest

from flowingo.pipelines.reader import read_pipeline, read_yml
from flowingo.pipelines.writer import write_pipeline, write_yml


class TestYamlWriter:
    @pytest.mark.parametrize(
        "content",
        [
            {}, [], {'title': 'tt', 'tasks': []}, {'t': 12}, {'t': [], 'te': [{'tt': 'tt'}, 12]}
        ],
    )
    def test_different_types(self, tmp_folder: pathlib.Path, content):
        path = tmp_folder / f'{uuid1()}.yml'

        # Writing ok
        write_yml(path, content)

        # Reading ok
        read_yml(path)


class TestPipelinesWriter:
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
    def test_files(self, pipelines_folder: pathlib.Path, pipelines_tasks_folder: pathlib.Path, tmp_folder: pathlib.Path, filename, is_valid):
        read_path = pipelines_folder / filename
        assert read_path.exists(), f'file {filename} does not exist in folder {pipelines_folder.absolute()}'

        if sys.version_info >= (3, 8):
            shutil.copytree(pipelines_folder, tmp_folder, dirs_exist_ok=True)
        else:
            shutil.copytree(pipelines_folder, tmp_folder)

        # Reading ok
        content = read_pipeline(pipelines_folder, filename)

        # Writing ok
        if is_valid:
            write_pipeline(tmp_folder, filename, content, tasks_folder=pipelines_tasks_folder)
        else:
            with pytest.raises(Exception):
                write_pipeline(tmp_folder, filename, content, tasks_folder=pipelines_tasks_folder)
