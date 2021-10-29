from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Manager, Folder


class Script:
    def __init__(self, manager: Manager, path: Path, folder: Folder = None):
        self.manager = manager
        self.path = path
        self.folder = folder or self.manager.get_folder(path.parent)
        self.handler = manager.config.get_handler(path)

    def __str__(self):
        return f"{self.full_name} [{self.handler}]"

    @property
    def name(self):
        return self.path.name

    @property
    def full_name(self):
        return f"{self.folder.name}/{self.name}"
