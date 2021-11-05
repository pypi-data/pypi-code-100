from rich import print
from os import system


def run(cmd: str) -> None:
    print(f"[bold green]RUN[/bold green] {cmd}")
    system(cmd)
