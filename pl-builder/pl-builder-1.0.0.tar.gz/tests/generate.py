import os

from plbuilder.builder import build_all
from plbuilder.creator import create_template
from tests.config import INIT_PROJECT_INPUT_FOLDER, SOURCES_PROJECT_INPUT_FOLDER
from tests.projutils import regenerate_project


def _generate_init_project():
    regenerate_project(INIT_PROJECT_INPUT_FOLDER)


def _generate_project_with_sources():
    regenerate_project(SOURCES_PROJECT_INPUT_FOLDER)
    os.chdir(SOURCES_PROJECT_INPUT_FOLDER)
    _generate_presentation()
    _generate_document()
    _build()


def _generate_presentation():
    create_template("presentation", "My Presentation")


def _generate_document():
    create_template("document", "My Document")


def _build():
    build_all()


if __name__ == "__main__":
    _generate_init_project()
    _generate_project_with_sources()
