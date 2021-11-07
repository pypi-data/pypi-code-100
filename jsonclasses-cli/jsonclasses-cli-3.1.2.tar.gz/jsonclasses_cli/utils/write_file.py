from os import getcwd
from pathlib import Path
from rich import print

def write_file(path: Path, content: str) -> None:
    if not path.parent.exists():
        path.parent.mkdir()
    with open(path, 'w') as file:
        print(f"[bold green]CREATE[/bold green] {path.relative_to(getcwd())}")
        file.write(content)
