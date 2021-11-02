import logging
import os
import re
import time
import pdb
from logging import Logger
from .icy_tags import IcyTags
import threading
from enum import Enum
import attr
import collections
import typing
import requests
from urllib.parse import urlparse, parse_qs, urlunparse

_log: Logger = logging.getLogger(__name__)


# there are several main pages: Tune.ashx Index.aspx Browse.ashx Search.ashx
# If you browser in Chrome or Edge to the page https://alexa.amazon.de/spa/index.html#music/TUNE_IN, and then
# continue to Favorites, the link will extend to something like this:
# https://alexa.amazon.de/spa/index.html#music/TUNE_IN/link/aHR0cDovL29wbWwucmFkaW90aW1lLmNvbS9Ccm93c2UuYXNoeD9jPXByZXNldHMmZm9ybWF0cz1hYWMsbXAzJnBhcnRuZXJJZD0hRUFMTE9qQiZzZXJpYWw9QUVFM1U1NDczUTVKTEhQRTRWQUQyVlpVSldMQSZsb2NhbGU9ZW4mbGF0bG9uPTQ3LjQyMzk0LDguNTQxMTY%3D
# which is base64 encoded. Using 'base64 -d', the data-url provides:
# http://opml.radiotime.com/Browse.ashx?c=presets&formats=aac,mp3&partnerId=!EALLOjB&serial=AEE3U5473Q5JLHPE4VAD2VZUJWLA&locale=en&latlon=47.42394,8.54116
# Remarks: adding &render=json to the url will return JSON.
# snippet:
#  <outline
#    type="audio"
#    text="94.5 | ROCK ANTENNE (Rock Music)"
#    URL="http://opml.radiotime.com/Tune.ashx?id=s25217&formats=aac,mp3&partnerId=!EALLOjB&serial=AEE3U5473Q5JLHPE4VAD2VZUJWLA&locale=en&latlon=47.42394,8.54116"
#    bitrate="128"
#    reliability="99"
#    guide_id="s25217"
#    subtext="Oasis - Wonderwall"
#    genre_id="g19"
#    formats="mp3,aac"
#    playing="Oasis - Wonderwall"
#    playing_image="http://cdn-albums.tunein.com/gn/XTRGN001M0d.jpg"
#    item="station"
#    image="http://cdn-profiles.tunein.com/s25217/images/logoq.jpg?t=152942"
#    now_playing_id="s25217"
#    preset_number="5"
#    preset_id="s25217"
#    is_preset="true"
#  />
#
# among other things, there is the attribute 'guide_id="s25217"', which can also be found in now playing
# information (part of url):
# "mainArt": {
#     "altText": "Album Art",
#     "artType": "UrlArtSource",
#     "contentType": "image/jpeg",
#     "url": "https://cdn-profiles.tunein.com/s25217/images/logoq.jpg?t=152942"
# },
#
# http://opml.radiotime.com/Search.ashx?partnerId=!EALLOjB&serial=AEE3U5473Q5JLHPE4VAD2VZUJWLA&locale=en&query=s25217

class StationState(Enum):
    idle = 'idle'
    active = 'active'


class StationType(Enum):
    internetRadio = 'internetRadio'
    plex = 'plex'
    kodi = 'kodi'


# From: https://glyph.twistedmatrix.com/2016/08/attrs.html (deprecated)
# From: https://www.attrs.org/en/stable/examples.html#defaults
# @attr.s(auto_attribs=True)
# class Station(object):
#     station_name: str
#     station_id: str
#     state: StationState = StationState.idle
#     station_type: StationType = None
#     now_playing: str = None
#
#
# # @attr.s(auto_attribs=True)
# @attr.s
# class StationList(object):
#     stations = attr.ib(default=attr.Factory(collections.UserDict))
#     # states = attr.ib(default=attr.Factory(collections.UserDict))
#
#     def tune_into_station(self, station_name, station_url, cv: threading.Event):
#         try:
#             return self.stations[station_name]
#         except KeyError:
#             self.stations[station_name] = tunein.TuneIn(station_name, station_url, cv)
#         return self.stations[station_name]
#
#     def stop_station(self, station_name):
#         self.stations[station_name].icy_tags.stop()
#
#
# def exit_handler(station_list):
#     for st in station_list.keys():
#         if isinstance(station_list[st].icy_tags, IcyTags):
#             station_list[st].icy_tags.stop()


class TuneIn:
    def __init__(self, station_name, station_url, cv: threading.Event):
        self.station_name = station_name
        self.station_url = station_url
        self.stream_dict = {}
        self.stream_list = []
        self.session = requests.session()
        self.icy_tags = None
        self.station_id = None
        self.cv = cv
        self.tuned_in_echo_devices = {}

    def start(self) -> bool:
        parsed_url = urlparse(self.station_url)
        parsed_qry = parse_qs(parsed_url.query)
        obfuscated = {}
        station_id = parsed_qry['id'][0] if 'id' in parsed_qry.keys() else None
        for param in parsed_qry.keys():
            if param in ['partnerId', 'serial']:
                obfuscated[param] = [re.sub('', 'x', str(parsed_qry[param][0]))]
            elif param == 'latlon':
                obfuscated[param] = [re.sub('\d', 'x', str(parsed_qry[param][0]))]
            else:
                obfuscated[param] = parsed_qry[param]

        query = "&".join(["{}={}".format(k, v[0]) for k, v, in obfuscated.items()])
        ob = parsed_url._replace(query=query)
        obfuscated = urlunparse(ob)

        # self.station_id = parse.urlparse()
        self.station_id = parsed_qry['id'][0]
        _log.info("getting station playlist for '{}' (id={})".format(self.station_name, self.station_id))
        rc = self._resolve_m3u(self.station_url, obfuscated)
        self.stream_list = [i for i in self.stream_dict.keys()]
        _log.info("Found stream urls {} for Station {}".format(self.stream_list, self.station_name))
        if rc:
            _log.info("starting mplayer")
            self.icy_tags = IcyTags(self.station_name, self.stream_list, self.cv, station_id)
            self.icy_tags.run()
            self.icy_tags.repeater_tags_read()
        return rc

    def _resolve_m3u(self, web_url, obfuscated_url=None) -> bool:
        _log.info("getting url {}".format(obfuscated_url if obfuscated_url is not None else web_url))
        response = self.session.get(web_url)
        if not response.status_code == requests.codes.ok:
            _log.error("_resolve_m3u - failed to download {}. Response: {}".format(web_url, response.text))
            return False
        _log.info("{} seems ok".format(obfuscated_url if obfuscated_url is not None else web_url))
        return_value = True
        for stream_url in response.text.split():
            # print("checking {}".format(stream_url))
            parsed_url = urlparse(stream_url)
            m = re.search("\.m3u$", stream_url, flags=re.IGNORECASE)
            if m:
                rc = self._resolve_m3u(stream_url)
                return_value = return_value and rc
            else:
                self.stream_dict[stream_url] = True
        return return_value

    # def get_radiotime_now_playing_from_favorite_stations(self):
    #     pdb.set_trace()
    #     url = "http://opml.radiotime.com/Browse.ashx?c=presets&formats=aac,mp3&partnerId=!EALLOjB&serial=AEE3U5473Q5JLHPE4VAD2VZUJWLA&locale=en&latlon=47.42394,8.54116"
    #     resp = self.session.get()

