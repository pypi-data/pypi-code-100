from typing import Any


class Point:
    def time_difference(self, _: Any) -> float:
        raise NotImplementedError()

    def distance_2d(self, _: Any) -> float:  # noqa: WPS114
        raise NotImplementedError()

    def speed_between(self, _: Any) -> float:
        raise NotImplementedError()
