import os
from functools import lru_cache
from pathlib import Path
from typing import Optional, Union
from typing_extensions import TypedDict

import jinja2


class TemplateData(TypedDict):
    title: str


@lru_cache
def get_environment(local_path: Optional[Union[str, Path]] = None) -> jinja2.Environment:
    path = Path(local_path or os.getcwd())
    local_templates_path = path / "templates"
    local_loader = jinja2.FileSystemLoader(local_templates_path)
    default_loader = jinja2.PackageLoader("plbuilder")
    choice_loader = jinja2.ChoiceLoader([local_loader, default_loader])
    return jinja2.Environment(loader=choice_loader)


def render_template(name: str, data: TemplateData) -> str:
    env = get_environment()
    template = env.get_template(name)
    return template.render(**data)


def output_template(name: str, data: TemplateData, path: Union[str, Path]):
    output = render_template(name, data)
    Path(path).write_text(output)
