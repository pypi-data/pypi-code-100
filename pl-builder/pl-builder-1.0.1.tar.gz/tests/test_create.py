import os

import pytest

from plbuilder.creator import create_template
from tests.config import (
    GENERATED_PROJECT_FOLDER,
    INPUT_PRESENTATION_SOURCES_FOLDER,
    GENERATED_PRESENTATION_SOURCES_FOLDER,
    INPUT_DOCUMENT_SOURCES_FOLDER,
    GENERATED_DOCUMENT_SOURCES_FOLDER, GENERATED_TEMPLATES_PATH,
)
from tests.dirutils import assert_dir_trees_are_equal
from tests.projutils import regenerate_generated_init_project


@pytest.fixture(autouse=True)
def before_each():
    regenerate_generated_init_project()
    os.chdir(GENERATED_PROJECT_FOLDER)
    yield


def _replace_local_template(name: str, content: str):
    template_path = GENERATED_TEMPLATES_PATH / f"{name}.j2"
    template_path.write_text(content)



def test_create_presentation():
    create_template("presentation", "My Presentation")
    assert_dir_trees_are_equal(
        INPUT_PRESENTATION_SOURCES_FOLDER, GENERATED_PRESENTATION_SOURCES_FOLDER
    )


def test_create_document():
    create_template("document", "My Document")
    assert_dir_trees_are_equal(
        INPUT_DOCUMENT_SOURCES_FOLDER, GENERATED_DOCUMENT_SOURCES_FOLDER
    )

# TODO: add tests for overriding templates, custom templates

# def test_override_template():
#     # expect_content = "some content"
#     # _replace_local_template("document", expect_content)
#     create_template("document", "My Document")
#     breakpoint()
#
# def test_custom_template():
#     expect_content = "some content"
#     _replace_local_template("mycustom", expect_content)
#     create_template("mycustom", "My Custom")

