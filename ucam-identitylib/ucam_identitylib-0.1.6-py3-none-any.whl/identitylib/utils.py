from typing import Iterable, Any


def chunks(list: Iterable[Any], chunk_size: int):
    for i in range(0, len(list), chunk_size):
        yield list[i:i + chunk_size]
