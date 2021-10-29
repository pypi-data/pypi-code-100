import os
from typing import Iterator, Optional

import gpxpy
from gpxpy.gpx import GPXTrackSegment

from gpx_parser.geometry.point import Point
from gpx_parser.io.file.file import File
from gpx_parser.parser.gpx_format_not_supported_error import GPXFormatNotSupportedError
from gpx_parser.parser.gpx_track_interval import GPXInterval
from gpx_parser.parser.parser import Parser


class GPXFileParser(Parser):
    def __init__(self, filename: str):
        self._filename: str = filename

    def parse(self) -> Iterator[GPXInterval]:
        with File(self._filename, os.R_OK) as gpx_file:
            return self.parse_xml(gpx_file.read())

    def parse_xml(self, xml: str) -> Iterator[GPXInterval]:
        gpx: gpxpy.mod_gpx.GPX = gpxpy.parse(xml)
        self._verify_gpx_integrity(gpx)
        yield from self._intervals_in_gpx(gpx)

    def _verify_gpx_integrity(self, gpx: gpxpy.mod_gpx.GPX) -> None:
        if len(gpx.tracks) != 1:
            raise GPXFormatNotSupportedError("Multi-track GPX files not supported.")

    def _intervals_in_gpx(self, gpx: gpxpy.mod_gpx.GPX) -> Iterator[GPXInterval]:
        for track in gpx.tracks:
            for segment in track.segments:
                yield from self._intervals_in_segment(segment)

    def _intervals_in_segment(self, segment: GPXTrackSegment) -> Iterator[GPXInterval]:
        previous_point: Optional[Point] = None
        current_point: Point

        for current_point in segment.points:
            if previous_point is None:
                previous_point = current_point
                continue
            yield GPXInterval.from_point_pair(current_point, previous_point)
            previous_point = current_point
