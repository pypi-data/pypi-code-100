from typing import Iterable, NamedTuple, Generator

import rich
from colour import Color


__all__ = ("Color", "print_with_gradient", "make_gradient")
__author__ = "Wasi Master"
__version__ = "0.1.0"


def print_with_gradient(text: str, color1: Color, color2: Color) -> None:
    lines = text.splitlines()
    for c, l in zip(color1.range_to(color2, len(lines)), lines):
        rich.print(f"[{c.hex_l}]{l}[/]")
