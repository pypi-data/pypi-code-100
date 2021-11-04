import os.path
from pathlib import Path

from plbuilder.paths import source_path
from plbuilder.templater import output_template, TemplateData


def create_template(template_name: str, title: str):
    template_folder = source_path(template_name)
    if not os.path.exists(template_folder):
        os.makedirs(template_folder)

    base_file_name = _get_file_name_from_display_name(title)
    out_path = Path(template_folder) / f"{base_file_name}.py"

    output_template(f"{template_name}.j2", TemplateData(title=title), out_path)


def _get_file_name_from_display_name(name: str) -> str:
    """
    Converts name to snake case and lower case for use in file name

    :param name: display name, can have spaces and capitalization
    :return:
    """
    return name.replace(" ", "_").lower()
