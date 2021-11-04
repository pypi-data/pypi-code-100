import os
import sys
from pathlib import Path
from typing import List, Tuple

from rope.base import libutils
from rope.base.codeanalyze import SourceLinesAdapter
from rope.base.project import Project
from rope.base.resources import Resource
from rope.refactor.extract import ExtractMethod, ExtractVariable
from rope.refactor.importutils import FromImport, NormalImport
from rope.refactor.importutils.module_imports import ModuleImports
from rope.refactor.inline import create_inline


def guess_project_path(source_path: Path) -> Path:
    """Find the root of the project given a full path inside it"""
    abs_path = source_path.resolve()
    res = abs_path.parent
    while True:
        if res.parent == res:
            # No top-level indicator found, default to the parent of the source path
            return abs_path.parent
        for root in ["setup.py", "setup.cfg", "pyproject.toml", ".git", ".hg"]:
            if (res / root).exists():
                return res
        res = res.parent


class KakouneHandler:
    def __init__(self, project: Project, resource: Resource) -> None:
        self.project = project
        self.resource = resource
        self.code = resource.read()
        self.adapter = SourceLinesAdapter(self.code)

    def get_main_selection(self) -> str:
        return os.environ["kak_selection"]

    def get_selection_offsets(self) -> Tuple[int, int]:
        selection_desc = os.environ["kak_selection_desc"]
        start_cursor, end_cursor = selection_desc.split(",")
        start_line, start_column = [int(x) for x in start_cursor.split(".")]
        end_line, end_column = [int(x) for x in end_cursor.split(".")]
        # kakoune columns start at 1, so we need -1 for the start, and nothing for the end
        start_offset: int = self.adapter.get_line_start(start_line) + start_column - 1
        end_offset: int = self.adapter.get_line_start(end_line) + end_column
        # kakoune selection maybe backwards, so start_offset maybe greater than stop_offset
        if start_offset > end_offset:
            return (end_offset, start_offset)
        else:
            return (start_offset, end_offset)

    def get_cursor_offset(self) -> int:
        line = int(os.environ["kak_cursor_line"])
        column = int(os.environ["kak_cursor_column"])
        res: int = self.adapter.get_line_start(line) + column - 1
        return res

    def add_import(self, args: List[str]) -> None:
        pymodule = self.project.get_pymodule(self.resource)
        selection = self.get_main_selection()

        if len(args) == 0:
            # Reminder: in kakoune, there's *always* a selection
            if len(selection) <= 1:
                sys.exit("add-import: no name given and selection too short")
            name = selection
            parent = None
        elif len(args) == 1:
            name = args[0]
            parent = None
        elif len(args) == 2:
            parent, name = args
        else:
            sys.exit("Could not parse add-import args")

        # Note: I almost never use 'as', so aliases are always None
        if not parent:
            import_info = NormalImport([(name, None)])
        else:
            import_info = FromImport(parent, 0, [(name, None)])

        module_imports = ModuleImports(self.project, pymodule)
        module_imports.add_import(import_info)
        changed_source = module_imports.get_changed_source()
        self.resource.write(changed_source)

    def extract(self, kind: str, new_name: str) -> None:
        (start_offset, end_offset) = self.get_selection_offsets()
        if kind == "variable":
            extractor = ExtractVariable(
                self.project, self.resource, start_offset, end_offset
            )
        else:
            extractor = ExtractMethod(
                self.project, self.resource, start_offset, end_offset
            )
        changes = extractor.get_changes(new_name)
        self.project.do(changes)

    def inline(self) -> None:
        offset = self.get_cursor_offset()
        inline = create_inline(self.project, self.resource, offset)
        changes = inline.get_changes()
        self.project.do(changes)


def main() -> None:
    buffile = os.environ["kak_buffile"]
    source_path = Path(buffile)
    project_path = guess_project_path(source_path)
    project = Project(project_path)
    resource = libutils.path_to_resource(project, source_path)
    handler = KakouneHandler(project, resource)

    _, action, *args = sys.argv
    if action == "add-import":
        handler.add_import(args)
    elif action == "extract-variable":
        (new_name,) = args
        handler.extract("variable", new_name)
    elif action == "extract-method":
        (new_name,) = args
        handler.extract("method", new_name)
    elif action == "inline":
        handler.inline()
    else:
        sys.exit(f"Unknown action {action}")
