from typing import Union
import functools
import dateparser
from skyfield import api, almanac, eclipselib

from astro.geo import Location, IPInfoLocation
from astro.cache import cache_path

MOON_PHASES_EMOJIS = ["🌑", "🌓", "🌕", "🌗"]

parse_date = functools.partial(
    dateparser.parse, settings={"TO_TIMEZONE": "UTC", "RETURN_AS_TIMEZONE_AWARE": True}
)


class Astro:
    def __init__(self, location: Union[Location, IPInfoLocation], date: str = None):
        load = api.Loader(cache_path)
        self.eph = load("de421.bsp")
        self.ts = load.timescale()
        self.date = parse_date(date or "now")
        self.location = location
        self.observer = api.wgs84.latlon(self.location.lat, self.location.lon)

    @classmethod
    def from_args(cls, **kwargs):
        location = None

        lat = kwargs.get("lat")
        lon = kwargs.get("lon")
        force_geoip = kwargs.get("force_geoip")

        if all((lat, lon)):
            location = Location(lat, lon)
        else:
            location = IPInfoLocation.from_ip(use_cache=not force_geoip)

        return cls(
            location=location,
            date=kwargs.get("date"),
        )

    def get_twilight_events(self, until="next midnight"):
        t0 = self.ts.utc(self.date)
        t1 = self.ts.utc(parse_date(until))
        times, events = almanac.find_discrete(
            t0, t1, almanac.dark_twilight_day(self.eph, self.observer)
        )

        result = [
            {"time": time.utc_iso(), "event": almanac.TWILIGHTS[event]}
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
                "time": time.utc_iso(),
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
                "time": time.utc_iso(),
                "type": eclipselib.LUNAR_ECLIPSES[eclipse_type],
                "detail": detail,
            }
            for time, eclipse_type, detail in zip(times, eclipse_types, details)
        ]

        return result
