from typing import Any

from gpx_parser.geometry.point import Point
from gpx_parser.parser.gpx_parse_error import GPXParseError

MS_PER_KMH = 3.6


class GPXInterval:  # noqa: WPS214
    def __init__(self, duration: float, speed: float, distance: float):
        self._duration: float = duration
        self._speed: float = speed
        self._distance: float = distance

    @classmethod
    def from_point_pair(cls, point_a: Point, point_b: Point) -> Any:
        try:  # noqa: WPS229
            duration = float(point_a.time_difference(point_b))
            distance = float(point_a.distance_2d(point_b))
            speed = float(point_a.speed_between(point_b))
        except ValueError:
            raise GPXParseError(f"Invalid point pair {point_a} {point_b}")
        except TypeError:
            raise GPXParseError(f"Invalid point pair {point_a} {point_b}")
        return cls(duration, speed, distance)

    @property
    def speed_ms(self) -> float:
        return self._speed

    @property
    def speed_kmh(self) -> float:
        return self.speed_ms * MS_PER_KMH

    @property
    def speed_kmtime(self) -> float:
        return 60 / self.speed_kmh

    @property
    def duration_s(self) -> float:
        return self._duration

    @property
    def distance_m(self) -> float:
        return self._distance

    @property
    def distance_km(self) -> float:
        return self.distance_m * 1000.0

    def __repr__(self) -> str:  # noqa: D105
        return f"{self.__class__.__name__}<{self.duration_s}s @ {self.speed_kmh}km/h covering {self.distance_m}m>"  # noqa: E501, WPS221, WPS237
