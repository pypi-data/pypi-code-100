import json
import functools
import dateparser
from typing import Union

from skyfield import api, almanac, eclipselib
from tabulate import tabulate

from astro.geo import Location, IPInfoLocation
from astro.cache import CACHE_PATH

MOON_PHASES_EMOJIS = ["🌑", "🌓", "🌕", "🌗"]

parse_date = functools.partial(
    dateparser.parse, settings={"TO_TIMEZONE": "UTC", "RETURN_AS_TIMEZONE_AWARE": True}
)


class Astro:
    def __init__(
        self,
        location: Union[Location, IPInfoLocation],
        date: str = None,
        format: str = "table",
    ):
        load = api.Loader(CACHE_PATH)
        self.eph = load("de421.bsp")
        self.ts = load.timescale()
        self.date = parse_date(date or "now")
        self.location = location
        self.observer = api.wgs84.latlon(self.location.lat, self.location.lon)
        self.format = format

    @classmethod
    def from_args(cls, **kwargs):
        location = None

        lat = kwargs.get("lat")
        lon = kwargs.get("lon")
        tz = kwargs.get("tz", "UTC")
        force_geoip = kwargs.get("force_geoip")

        if all((lat, lon)):
            location = Location(float(lat), float(lon), tz=tz)
        else:
            location = IPInfoLocation.from_ip(use_cache=not force_geoip)

        return cls(
            location=location,
            date=kwargs.get("date"),
            format=kwargs.get("format")
        )

    def get_twilight_events(self, until="next midnight"):
        t0 = self.ts.utc(self.date)
        t1 = self.ts.utc(parse_date(until))
        times, events = almanac.find_discrete(
            t0, t1, almanac.dark_twilight_day(self.eph, self.observer)
        )

        result = [
            {
                "time": time.astimezone(self.location.tz).ctime(),
                "event": almanac.TWILIGHTS[event],
            }
            for time, event in zip(times, events)
        ]

        return result

    def whereis(self, body: str):
        return (
            (self.eph["earth"] + self.observer)
            .at(self.ts.utc(self.date))
            .observe(self.eph[body])
            .apparent()
            .altaz()
        )

    def get_moon_phases(self, until="in 1 month"):
        t0 = self.ts.utc(self.date)
        t1 = self.ts.utc(parse_date(until))
        times, phases = almanac.find_discrete(t0, t1, almanac.moon_phases(self.eph))

        result = [
            {
                "time": time.astimezone(self.location.tz).ctime(),
                "phase": almanac.MOON_PHASES[phase],
                "emoji": MOON_PHASES_EMOJIS[phase],
            }
            for time, phase in zip(times, phases)
        ]

        return result

    def get_moon_eclipses(self, until="next year"):
        t0 = self.ts.utc(self.date)
        t1 = self.ts.utc(parse_date(until))
        times, eclipse_types, details = eclipselib.lunar_eclipses(t0, t1, self.eph)

        result = [
            {
                "time": time.astimezone(self.location.tz).ctime(),
                "type": eclipselib.LUNAR_ECLIPSES[eclipse_type],
                "detail": detail,
            }
            for time, eclipse_type, detail in zip(times, eclipse_types, details)
        ]

        return result

    def serialize(self, data: dict, **kwargs):
        format = kwargs.get("format", self.format)
        if format == "json":
            return json.dumps(data)
        elif format == "table":
            return tabulate(data, headers="keys")
