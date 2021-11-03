import os
import platform
import subprocess
import sys
import textwrap
from builtins import input, print
from typing import Any
from typing import Generator, Optional, Type
from dataclasses import dataclass, field

from utils import terminal_size
from config import BORDER, MARGIN, PADDING, BORDER_TYPE

@dataclass
class Screen:
    """Console screen.

    Args:
        height (int): Screen height in rows.
        width (int): Screen width in columns.

    Example:

        >>> from prototools.components import Screen
        >>> screen = Screen()
    """
    _tw: Any = textwrap.TextWrapper()
    height: int = 40
    width: int = field(default_factory=terminal_size)

    @staticmethod
    def clear() -> None:
        """Clear the screen.
        """
        if platform.system() == "Windows":
            subprocess.check_call("cls", shell=True)
        else:
            print(subprocess.check_output("clear").decode())
    
    @staticmethod
    def flush():
        """
        Flush any buffered standard output to screen.
        """
        sys.stdout.flush()

    @staticmethod
    def input(self, prompt=''):
        """
        Prompt the end user for input.

        Args:
            prompt (str): Message to display as the prompt.

        Returns:
            User's input.
        """
        return input(prompt)

    @staticmethod
    def printf(*args):
        """
        Prints the arguments to the screen.

        Args:
            *args: Variable length argument list.
        """
        print(*args, end='')

    @staticmethod
    def println(*args):
        """
        Prints the arguments to the screen, including an appended
        newline character.

        Args:
            *args: Variable length argument list.
        """
        print(*args)


s = Screen()
print(s)