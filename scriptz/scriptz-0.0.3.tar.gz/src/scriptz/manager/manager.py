from typing import List, Iterator
from pathlib import Path
import sys

from scriptz import console
from . import Config, Folder, Script


class Manager:
    def __init__(self, root_dir: Path = None):
        self.root_dir = root_dir or Path.cwd()
        self.config = Config(root_dir=self.root_dir)

    @property
    def ini_path(self) -> Path:
        return self.config.ini_path

    def get_folder(self, path=None) -> Folder:
        if path is None:
            path = self.root_dir
        elif isinstance(path, str):
            path = Path(self.root_dir / path)
        return Folder(manager=self, path=path)

    def get_script(self, path: Path) -> Script:
        return Script(manager=self, path=path)

    def iterate_scripts(self, paths: List[Path]) -> Iterator[Script]:
        for path in paths:
            path = path.absolute()
            if path.is_dir():
                folder = self.get_folder(path=path)
                yield from folder.iterate_scripts()
            else:
                yield Script(manager=self, path=path)

    @classmethod
    def check(
        cls,
        check_value,
        error_msg: str,
        error_code: int = 1,
        ok_msg: str = None,
    ):
        if not check_value:
            cls.exit(error_msg=error_msg, error_code=error_code)

        elif ok_msg:
            console.print(f"[green]{ok_msg}[/green]")

    @classmethod
    def exit(cls, error_msg: str = None, error_code: int = 1):
        if error_msg:
            console.print(f"[red]{error_msg}[/red]")
        sys.exit(error_code)
