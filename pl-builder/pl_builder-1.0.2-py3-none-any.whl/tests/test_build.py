import os

import pytest

from plbuilder.builder import (
    build_all,
)
from plbuilder.creator import create_template
from tests.config import (
    GENERATED_PROJECT_FOLDER,
    INPUT_DOCUMENTS_FOLDER,
    GENERATED_DOCUMENTS_FOLDER,
    INPUT_SLIDES_FOLDER,
    GENERATED_SLIDES_FOLDER,
    GENERATED_HANDOUTS_FOLDER,
    INPUT_HANDOUTS_FOLDER,
)
from tests.fileutils import are_files_equal
from tests.projutils import regenerate_generated_init_project


@pytest.fixture(autouse=True)
def before_each():
    regenerate_generated_init_project()
    os.chdir(GENERATED_PROJECT_FOLDER)
    create_template("presentation", "My Presentation")
    create_template("document", "My Document")
    yield


def test_build():
    build_all()
    assert are_files_equal(
        INPUT_DOCUMENTS_FOLDER / "My Document.tex", GENERATED_DOCUMENTS_FOLDER / "My Document.tex"
    )
    assert are_files_equal(
        INPUT_SLIDES_FOLDER / "My Presentation.tex", GENERATED_SLIDES_FOLDER / "My Presentation.tex"
    )
    assert are_files_equal(
        INPUT_HANDOUTS_FOLDER / "My Presentation.tex", GENERATED_HANDOUTS_FOLDER / "My Presentation.tex"
    )
