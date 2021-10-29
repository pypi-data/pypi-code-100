from typing import Iterator

from gpx_parser.parser.gpx_track_interval import GPXInterval
from gpx_renderer.renderers.stdout import STDOUTRenderer
from gpx_renderer.terminal_colors import TerminalColors


class STDOUTTimeRenderer(STDOUTRenderer):
    def __init__(self, running: float, walking: float, destination: str):
        super().__init__(running=running, walking=walking, destination=destination)

    def _generate_points(self, intervals: Iterator[GPXInterval]) -> Iterator[str]:
        for interval in intervals:
            number_of_seconds_active = range(int(interval.duration_s) + 1)
            for _ in number_of_seconds_active:
                color = self._color_from_pace(interval.speed_kmtime)
                yield f"{color}█{TerminalColors.ENDC}"
