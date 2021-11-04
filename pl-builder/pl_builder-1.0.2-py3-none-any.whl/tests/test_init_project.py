import pytest

from plbuilder.init import initialize_project, ProjectExistsException
from tests.config import GENERATED_PROJECT_FOLDER, INIT_PROJECT_INPUT_FOLDER
from tests.dirutils import assert_dir_trees_are_equal
from tests.projutils import reset_generated_init_project


@pytest.fixture(autouse=True)
def before_each():
    reset_generated_init_project()
    yield


def test_init_project_when_empty():
    initialize_project(GENERATED_PROJECT_FOLDER)
    assert_dir_trees_are_equal(GENERATED_PROJECT_FOLDER, INIT_PROJECT_INPUT_FOLDER)


def test_init_project_when_exists():
    initialize_project(GENERATED_PROJECT_FOLDER)
    with pytest.raises(ProjectExistsException):
        initialize_project(GENERATED_PROJECT_FOLDER)
