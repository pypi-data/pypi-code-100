"""A simple plugin loader."""
import importlib
import os
from typing import List


class ModuleInterface:
    """Represents a plugin interface. A plugin has a single register function."""

    @staticmethod
    def register() -> None:
        """Register the necessary items in the connector factory."""


def import_module(name: str) -> ModuleInterface:
    """Imports a module given a name."""
    return importlib.import_module(name, package=__name__)  # type: ignore


def load_plugins(plugins: List[str]) -> None:
    """Loads the plugins defined in the plugins list."""
    for plugin_file in plugins:
        plugin = import_module(f"...plugins.{plugin_file}")
        plugin.register()
