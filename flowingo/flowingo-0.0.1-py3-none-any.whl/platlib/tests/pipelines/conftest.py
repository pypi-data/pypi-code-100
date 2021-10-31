import pathlib

import pytest

PIPELINES_FOLDER = pathlib.Path(__file__).parent / 'data' / 'pipelines'
PIPELINES_TASKS_FOLDER = pathlib.Path(__file__).parent / 'data' / 'pipelines_tasks'
TASKS_FOLDER = pathlib.Path(__file__).parent / 'data' / 'tasks'


@pytest.fixture(scope='session')
def pipelines_folder() -> pathlib.Path:
    return PIPELINES_FOLDER


@pytest.fixture(scope='session')
def pipelines_tasks_folder() -> pathlib.Path:
    return PIPELINES_TASKS_FOLDER


@pytest.fixture(scope='session')
def tasks_folder() -> pathlib.Path:
    return TASKS_FOLDER
