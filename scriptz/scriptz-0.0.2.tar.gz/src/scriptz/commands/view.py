from pathlib import Path
from typing import List

from rich.syntax import Syntax

from scriptz import cli, console, Manager


@cli.command()
def view(files: List[Path]):
    """ View files content with highlighting. """
    output_file(files, force_plain=False)


@cli.command()
def less(files: List[Path]):
    """ Page file content (no highlighting). """
    with console.pager():
        output_file(files, force_plain=True)


def output_file(files: List[Path], force_plain: bool):
    manager = Manager()

    for path in files:
        if path.is_file():
            pygment = None
            if not force_plain:
                handler = manager.config.get_handler(path)
                pygment = handler and handler.pygment
            pygment = pygment or "plain"

            content = path.read_text().strip()
            syntax = Syntax(content, lexer_name=pygment, line_numbers=True)

            console.print(path)
            console.print(syntax)
            console.print()
