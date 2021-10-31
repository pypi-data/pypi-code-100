import pathlib

import pytest

from flowingo.configuration import conf

PIPELINES_FOLDER = pathlib.Path(__file__).parent / 'data' / 'pipelines'
TASKS_FOLDER = pathlib.Path(__file__).parent / 'data' / 'tasks'


@pytest.fixture(scope='function')
def config_folders():
    conf.pipelines_folder = PIPELINES_FOLDER
    conf.tasks_folder = TASKS_FOLDER
