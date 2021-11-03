from itertools import chain, repeat
from typing import Iterable, List, Mapping, Optional, Union

Value = Union[int, float]


class Vector(List[Value]):
    def __init__(self, values: Iterable[Value], padding_value: Optional[Value]) -> None:
        super().__init__(values)
        self.padding_value = padding_value if padding_value is not None else 0

    def padded(self, size: int) -> "Vector":
        if size < len(self):
            raise RuntimeError(f"Trying pad a Vector to lesser size: from {len(self)} to {size} elements.")
        return Vector(chain(self, repeat(self.padding_value, size - len(self))), self.padding_value)


FeatureVectors = Mapping[str, Vector]
InstanceFeatureVectors = Mapping[str, FeatureVectors]
