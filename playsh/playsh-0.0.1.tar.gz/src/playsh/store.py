from typing import Union


class Store:
    def __init__(self) -> None:
        ItemType = Union[float, int]
        self._storage: dict[str, ItemType] = dict()

    def __getitem__(self, key: str):
        if type(key) is not str:
            raise TypeError
        return self._storage[key]

    def __setitem__(self, key: str, value):
        if type(key) is not str:
            raise TypeError
        self._storage[key] = value

    def __iter__(self):
        return iter(self._storage.items())

    def __len__(self):
        return len(self._storage)
