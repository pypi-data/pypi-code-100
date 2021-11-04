import os
import shutil
from pathlib import Path
from typing import Union, Final

from plbuilder.config import CREATED_DIRECTORY

COPY_TEMPLATES: Final = ["author", "organization"]


def initialize_project(in_directory: Union[str, Path] = None):
    in_directory = Path(in_directory or os.getcwd())
    new_directory = in_directory / CREATED_DIRECTORY

    if os.path.exists(new_directory):
        raise ProjectExistsException(f"{new_directory}")

    os.makedirs(new_directory)

    pl_builder_source_path = os.path.dirname(os.path.abspath(__file__))

    templates_source = os.path.join(pl_builder_source_path, "templates")
    templates_out_path = os.path.join(new_directory, "templates")
    os.makedirs(templates_out_path)
    for copy_template_name in COPY_TEMPLATES:
        this_template_path = Path(templates_source) / f"{copy_template_name}.j2"
        shutil.copy(this_template_path, templates_out_path)

    sources_path = os.path.join(new_directory, "sources")
    presentation_sources_path = os.path.join(sources_path, "presentation")
    document_sources_path = os.path.join(sources_path, "document")
    os.makedirs(presentation_sources_path)
    os.makedirs(document_sources_path)

    assets_path = os.path.join(new_directory, "assets")
    images_path = os.path.join(assets_path, "images")
    os.makedirs(images_path)


class ProjectExistsException(Exception):
    pass
