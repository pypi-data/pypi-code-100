from typing import List
from click import *

import hodgepodge.click


def str_to_strs(data: str) -> List[str]:
    return hodgepodge.click.str_to_strs(data)


def str_to_ints(data: str) -> List[int]:
    return hodgepodge.click.str_to_ints(data)
