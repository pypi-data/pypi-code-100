from typing import Iterator

from gpx_parser.parser.gpx_track_interval import GPXInterval
from gpx_renderer.renderers.stdout import STDOUTRenderer
from gpx_renderer.terminal_colors import TerminalColors


class STDOUTDistanceRenderer(STDOUTRenderer):
    def __init__(self, running: float, walking: float, destination: str):
        super().__init__(running=running, walking=walking, destination=destination)

    def _generate_points(self, intervals: Iterator[GPXInterval]) -> Iterator[str]:
        for interval in intervals:
            interval_distance_m = range(int(interval.distance_m) + 1)
            for _ in interval_distance_m:
                color = self._color_from_pace(interval.speed_kmtime)
                yield f"{color}█{TerminalColors.ENDC}"
