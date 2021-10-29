from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Optional, Iterator

from . import Script

if TYPE_CHECKING:
    from . import Manager


class Folder:
    def __init__(self, manager: Manager, path: Path):
        self.manager = manager
        self.path = path

    def __str__(self):
        return self.name

    @property
    def relative_path(self):
        return self.path.relative_to(self.manager.root_dir)

    @property
    def name(self):
        return str(self.relative_path)

    @property
    def exists(self):
        return self.path.is_dir()

    @property
    def step_paths(self):
        return sorted(p for p in self.path.glob("[0-9]*_*"))

    @property
    def step_names(self):
        return [p.name for p in self.step_paths]

    @property
    def last_step_name(self) -> Optional[str]:
        last_step_name = self.step_names[-1:]
        if last_step_name:
            return last_step_name[0]

    @property
    def last_prefix(self) -> str:
        return (self.last_step_name or "_").split("_", maxsplit=1)[0]

    def get_next_prefix(self) -> str:
        next_prefix = int(self.last_prefix or -1) + 1
        return self.manager.config.zfill(next_prefix)

    def create_script(self, file_name: str, suffix: str):
        next_prefix = self.get_next_prefix()
        hold = self.path / f"{next_prefix}.hold"
        hold.touch(exist_ok=False)  # todo: real lock

        path = self.path / f"{next_prefix}_{file_name}{suffix}"
        self.manager.check(not path.exists(), f"Script {path} already exists.")
        path.touch(exist_ok=False)
        script = Script(manager=self.manager, path=path, folder=self)

        hold.unlink(missing_ok=False)  # todo: real lock

        return script

    def iterate_scripts(self) -> Iterator[Script]:
        for path in self.step_paths:
            if path.is_dir():
                folder = self.manager.get_folder(path=path)
                yield from folder.iterate_scripts()
            else:
                yield Script(manager=self.manager, path=path, folder=self)
