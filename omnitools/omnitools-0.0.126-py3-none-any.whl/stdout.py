import sys
from typing import *


__ALL__ = ["p"]


def p(*args, end="\n", **kwargs) -> None:
    print(*args, **kwargs, end=end, flush=True)


