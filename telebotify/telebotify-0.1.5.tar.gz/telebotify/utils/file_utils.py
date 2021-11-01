import importlib.resources as pkg_resources
from os import PathLike
from types import ModuleType
from typing import Union


def get_resource_path(package: Union[str, ModuleType], resource: Union[str, PathLike]) -> str:
    with pkg_resources.path(package, resource) as p:
        return p.__str__()
