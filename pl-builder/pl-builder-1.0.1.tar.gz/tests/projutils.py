import shutil
from pathlib import Path

from plbuilder.init import initialize_project
from tests.config import GENERATED_PROJECT_FOLDER


def reset_generated_init_project():
    reset_project(GENERATED_PROJECT_FOLDER)


def regenerate_generated_init_project():
    regenerate_project(GENERATED_PROJECT_FOLDER)


def reset_project(directory: Path):
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir(parents=True)


def regenerate_project(directory: Path):
    reset_project(directory)
    initialize_project(directory)
