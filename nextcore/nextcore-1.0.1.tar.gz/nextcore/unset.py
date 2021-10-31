from typing import Any


class Unset:
    def __eq__(self, other) -> bool:
        return False

    def __bool__(self) -> bool:
        return False


UNSET: Any = Unset()
