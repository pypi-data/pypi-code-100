import json
import base64
import os
import urllib.request

from astro.cache import cache


class Location:
    def __init__(self, lat: float, lon: float, name: str = None, tz: str = None):
        self.lat = lat
        self.lon = lon
        self.name = name
        self.tz = None

    @classmethod
    def from_ip(cls):
        raise NotImplementedError

    def __str__(self):
        if self.name:
            return self.name
        return self.coords_display

    @property
    def coords_display(self):
        lat = f"{abs(self.lat):.2f}°{'N' if self.lat > 0 else 'S'}"
        lon = f"{abs(self.lon):.2f}°{'E' if self.lon > 0 else 'W'}"
        return f"{lat} {lon}"


class IPInfoLocation(Location):
    TOKEN = os.getenv("ASTRO_IPINFO_TOKEN", "d0aff427aae8d9")
    CACHE_TIMEOUT = os.getenv("ASTRO_IPINFO_CACHE_TIMEOUT", 60 * 60 * 24)  # 1 day

    @classmethod
    def from_ip(cls, token=TOKEN, use_cache=True):
        if use_cache and (response := cache.get("ipinfo")):
            return cls._from_response(response)

        req = urllib.request.Request("https://ipinfo.io")

        auth = f"{token}:".encode("ascii")
        req.add_header("Authorization", f"Basic {base64.b64encode(auth)}")

        response = urllib.request.urlopen(req).read()
        cache.set("ipinfo", response, expire=cls.CACHE_TIMEOUT)

        return cls._from_response(response)

    @classmethod
    def _from_response(cls, response):
        data = json.loads(response)
        lat, lon = data["loc"].split(",")
        name = f"{data['city']}, {data['region']}, {data['country']} ({data['ip']})"
        tz = data["timezone"]
        return cls(float(lat), float(lon), name, tz)
