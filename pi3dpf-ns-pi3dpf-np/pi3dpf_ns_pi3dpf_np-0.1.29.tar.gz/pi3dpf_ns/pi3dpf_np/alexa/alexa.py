# hi there
# Interessantes Projekt: https://pypi.org/project/alexa-client/, macht den Login mit einem Token aus der Dev Conlole
# Find broser cookies in DevTools: Application > Storage > Cookies > url

# Es gibt ein node skript was das kann: https://www.npmjs.com/package/login-with-amazon

# da gibt es ein curl project, von welchem man in den Alexa account einloggen kann:
#   https://github.com/thorsten-gehrig/alexa-remote-control
#   ich versuche, das mittels der Library https://requests.readthedocs.io/en/master/ nachzuimplementieren
#
# todo:
#  - add hints how to use curl and alexa_remote_control.sh
#    get inspired by https://github.com/thorsten-gehrig/alexa-remote-control
#       - checking the required function exits in alexa_remote_control.sh
#       - if so, extract the underlying curl command from script
#       - run the curl command, to get more details you can
#            - add -v or --trace (show the form parameters)
#            - replace the url (https://alexa.amazon.com/whatever) in both this script and the curl command with
#              https://httpbin.org/post to compare all details (http headers, cookies, form parameters)
#  - Amazon 2FA
#  - poll for new devices more frequently
#  - detect when echo device is in bluetooth streaming action and treat inactive
#  - add mqtt, plex, emby, jellyfin, kodi

# from requests import codes
import attr
import collections
from collections import Counter
import copy
import json
import logging
import os
from operator import itemgetter
import pdb
import re
import requests
import shutil
import time
import traceback
import threading
from urllib.parse import urlencode, parse_qs, urlsplit, urlunsplit
import urllib3.exceptions

# from ..common import pf_common as pfc
from pi3dpf_ns.pi3dpf_common import pf_common as pfc
from .echo import Devices as devices
from .echo import Device
from .echo import DeviceClass
from .echo import DeviceState
from .echo import QueueInfo
from .visualize import AlexaNowPlayingVisualize
from .muteAdverts import MuteAdverts
from enum import Enum
from ..tunein.tunein import TuneIn
from ..tunein.icy_tags import IcyTags
from ..tunein.icy_tags import Announcement
from ..sonos.sonos import Sonos

_log = logging.getLogger(__name__)


def __dump_headers__(resp):
    dump = ""
    for i in range(0, len(resp)):
        dump += "Header {:03d} HTTP Status: {}\n{}".format(
            i, resp[i].raw.status, json.dumps(dict(resp[i].raw.getheaders()), indent=4))
    return dump if len(resp) > 0 else "no redirections in this response"


def rm_element(dictionary: dict, element):
    if element in dictionary.keys():
        del dictionary[element]


class StationState(Enum):
    idle = 'idle'
    active = 'active'


class StationType(Enum):
    internetRadio = 'internetRadio'
    plex = 'plex'
    kodi = 'kodi'


# From: https://glyph.twistedmatrix.com/2016/08/attrs.html (deprecated)
# From: https://www.attrs.org/en/stable/examples.html#defaults
# Todo: is class Station in use?
@attr.s(auto_attribs=True)
class Station(object):
    station_name: str
    station_id: str
    state: StationState = StationState.idle
    station_type: StationType = None
    now_playing: str = None


# @attr.s(auto_attribs=True)
@attr.s
class StationList(object):
    stations = attr.ib(default=attr.Factory(collections.UserDict))

    # states = attr.ib(default=attr.Factory(collections.UserDict))

    def tune_into_station(self, station_name, station_id, station_url, cv: threading.Event, echo_device: Device):
        try:
            res = self.stations[station_name]
        except KeyError:
            self.stations[station_name] = TuneIn(station_name, station_url, cv)
            res = self.stations[station_name]
        echo_device.untune_callable = self.untune_station
        _log.info("tune_into_station - [{}] radio_station='{}', station_name='{}'".format(
            echo_device.accountName, echo_device.radio_station, station_name))

        # todo: detect when tuning from one station to another. insufficient: echo_device.radio_station != station_name
        # better: check self.stations if given echo_device is listed in other station
        # self.stations.keys()
        # self.stations['SRF 2 Kultur'].tuned_in_echo_devices.keys()
        tis = [s for s in self.stations.keys() if echo_device.accountName in self.stations[s].tuned_in_echo_devices]
        for st in tis:
            _log.info("tune_into_station - [{}] un-tuning station '{}' before tuning into '{}'".format(
                echo_device.accountName, st, station_name))
            self.untune_station(echo_device)
            # pdb.set_trace()
        # if echo_device.radio_station is not None and echo_device.radio_station != station_name:
        #     _log.info("tune_into_station - [{}] calling untune_station, radio_station='{}'".format(
        #         echo_device.accountName, echo_device.radio_station))
        #     self.untune_station(echo_device)
        echo_device.radio_station = station_name
        echo_device.tunein_id = station_id
        echo_device.active_skill = 'TuneIn'
        if len(res.tuned_in_echo_devices) == 0:
            self.stations[station_name].start()
        res.tuned_in_echo_devices[echo_device.accountName] = echo_device
        return res

    def untune_station(self, echo_device: Device):
        accountName, ed_station_name = echo_device.accountName, echo_device.radio_station
        if ed_station_name is None:
            return
        ed_tuned_in = self.stations[ed_station_name].tuned_in_echo_devices
        if accountName not in ed_tuned_in:  # echo_device.active_skill != 'TuneIn' and
            return
        try:
            del (self.stations[ed_station_name].tuned_in_echo_devices[echo_device.accountName])
        except KeyError:
            _log.error("untune_station - [{}] not in self.stations[{}].tuned_in_echo_devices: {}".format(
                accountName, ed_station_name, ed_tuned_in))
        ed_num = len(ed_tuned_in)

        # check if untuning echo_device is the last tuned into this radio station and stop mplayer if so
        if ed_num == 0:
            _log.info("untune_station - [{}] stopping mplayer for '{}'".format(accountName, ed_station_name))
            self.stop_station(ed_station_name)
        else:
            _log.info("untune_station - [{}] {} echo devices tuned in on '{}': {}".format(
                accountName, ed_num, ed_station_name, ", ".join("'{0}'".format(x) for x in ed_tuned_in)))
        echo_device.radio_station = None
        echo_device.tunein_id = None
        echo_device.active_skill = None

    def stop_station(self, station_name):
        _log.info("stop_station stopping station {}".format(station_name))
        self.stations[station_name].icy_tags.stop()


def exit_handler(station_list):
    for st in station_list.keys():
        if isinstance(station_list[st].icy_tags, IcyTags):
            station_list[st].icy_tags.stop()


class ScheduleMode(Enum):
    init = 'init'
    normal = 'normal'
    get_active_elements = 'get_active_elements'


class Alexa:
    def __init__(self, config, verbose):
        self.config = config
        self.verbose = verbose
        self.devices = devices(config)
        self.NP_HOME_DIR = pfc.get_config_param(self.config, 'NP_HOME_DIR')
        Announcement.update_repeater_fname(self.NP_HOME_DIR)
        self.PI3D_ALEXA_ACCOUNT_USERNAME = pfc.get_config_param(self.config, 'PI3D_ALEXA_ACCOUNT_USERNAME')
        self.PI3D_ALEXA_ACCOUNT_PASSWORD = pfc.get_config_param(self.config, 'PI3D_ALEXA_ACCOUNT_PASSWORD')
        self.PI3D_ALEXA_ACCOUNT_BASE_URL = pfc.get_config_param(self.config, 'PI3D_ALEXA_ACCOUNT_BASE_URL')
        self.PI3D_NOW_PLAYING_AD_TITLES = pfc.get_config_param(self.config, 'PI3D_NOW_PLAYING_AD_TITLES')
        self.PI3D_SONOS_ACCOUNT_USERNAME = pfc.get_config_param(self.config, 'PI3D_SONOS_ACCOUNT_USERNAME')
        self.sonos = None
        if self.PI3D_SONOS_ACCOUNT_USERNAME != 'not-configured':
            self.sonos = Sonos(self.config)
            # so.get_album_art_url('Kitchen')
        self.PI3D_NOW_PLAYING_CHECK_IDLE_DEVICES = pfc.get_config_param(
            self.config, 'PI3D_NOW_PLAYING_CHECK_IDLE_DEVICES')
        # self.PI3D_NOW_PLAYING_TOP_DIR = pfc.get_config_param(self.config, 'PI3D_NOW_PLAYING_TOP_DIR')
        self.LOG_DIR = pfc.get_config_param(self.config, 'LOG_DIR')
        self.PI3D_ALEXA_ACCOUNT_LANGUAGE = 'en-US;q=0.7,en;q=0.3'  # todo: add to pf.config? changing en will break code
        self.PI3D_RADIOTIME_LATLON = pfc.get_config_param(self.config, 'PI3D_RADIOTIME_LATLON')
        self.PI3D_RADIOTIME_PARTNER_ID = pfc.get_config_param(self.config, 'PI3D_RADIOTIME_PARTNER_ID')
        self.PI3D_NOW_PLAYING_BM = pfc.get_config_param(self.config, 'PI3D_NOW_PLAYING_BM')
        self.session = requests.Session()
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:1.0) {}/1.0".format(__name__)
        self.session.headers.update(
            {'User-Agent': self.user_agent,
             'Accept-Language': self.PI3D_ALEXA_ACCOUNT_LANGUAGE,
             'DNT': '1',
             'Connection': 'keep-alive',
             'Upgrade-Insecure-Requests': '1'})
        #    'Referer': "{}/spa/index.html".format(self.PI3D_ALEXA_ACCOUNT_BASE_URL)
        # Sometimes you’ll want to omit session-level keys from a dict parameter. To do this, you simply set that
        # key’s value to None in the method-level parameter. It will automatically be omitted.
        self.station_list = StationList()
        self.icy_event = threading.Event()
        self.icy_event.set()
        self.cookie_jar = os.path.join(self.NP_HOME_DIR, 'alexa', '.cookies-alexa')
        self.url_signin = "{}/ap/signin".format(self.PI3D_ALEXA_ACCOUNT_BASE_URL)
        # bootstrap with GUI-Version writes GUI version to cookie returns among other the current authentication state
        self.url_bootstrap = "{}/api/bootstrap".format(self.PI3D_ALEXA_ACCOUNT_BASE_URL)  # todo add ?version=0
        self.url_device = "{}/api/devices-v2/device".format(self.PI3D_ALEXA_ACCOUNT_BASE_URL)
        self.url_player = "{}/api/np/player".format(self.PI3D_ALEXA_ACCOUNT_BASE_URL)
        self.url_allvol = "{}/api/devices/deviceType/dsn/audio/v1/allDeviceVolumes".format(
            self.PI3D_ALEXA_ACCOUNT_BASE_URL)
        self.url_command = "{}/api/np/command".format(self.PI3D_ALEXA_ACCOUNT_BASE_URL)  # not currently in use
        self.url_behaviour = "{}/api/behaviors/preview".format(self.PI3D_ALEXA_ACCOUNT_BASE_URL)
        self.url_queue_info = "{}/api/np/queue".format(self.PI3D_ALEXA_ACCOUNT_BASE_URL)
        self.url_media_state = "{}/api/media/state".format(self.PI3D_ALEXA_ACCOUNT_BASE_URL)
        self.url_tunein_browse = "{}/api/tunein/browse".format(self.PI3D_ALEXA_ACCOUNT_BASE_URL)
        self.customerId = None  # will be set in self.__bootstrap__
        self.muteAdverts = MuteAdverts(self.config, self.devices, self.session, self.customerId)
        self.muteAdverts.fifo_open('write_noblock', '__init__')
        self.muteAdverts.run()
        self.__login__()
        self.__bootstrap__()
        self.playing_list = {}
        self.visualize = AlexaNowPlayingVisualize(self.config)
        self.visualize.fifo_open('write_noblock')
        self.nothing_playing = os.path.join(
            os.path.dirname(__file__), '..', 'cfg', 'icons', '1x1-transparent.png')
        shutil.copyfile(self.nothing_playing, self.PI3D_NOW_PLAYING_BM)
        self.now_playing(init=ScheduleMode.init)
        self.song_changed = False

    def exit_handler(self):
        self.muteAdverts.fifo_write("stop", "non-existing-echo-device", 0.0)
        self.muteAdverts.stop()
        _log.info("exit_handler - copying {} to {}".format(self.nothing_playing, self.PI3D_NOW_PLAYING_BM))
        shutil.copyfile(self.nothing_playing, self.PI3D_NOW_PLAYING_BM)

    def __login__(self):
        _log.info("Alexa - login as '{}' at '{}'".format(
            self.PI3D_ALEXA_ACCOUNT_USERNAME, self.PI3D_ALEXA_ACCOUNT_BASE_URL))
        # Inspired from: alexa_remote_control.sh, https://github.com/thorsten-gehrig/alexa-remote-control.git
        # -1- alexa_remote_control.sh: get first cookie and write redirection target into referer
        # /usr/bin/curl --compressed
        #               --http1.1
        #               --silent
        #               --dump-header /tmp/.alexa.header
        #               --cookie-jar /tmp/.alexa.cookie
        #               --cookie /tmp/.alexa.cookie
        #               --user-agent Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:1.0) bash-script/1.0
        #               --header Accept-Language: de,en-US;q=0.7,en;q=0.3
        #               --header DNT: 1
        #               --header Connection: keep-alive
        #               --header Upgrade-Insecure-Requests: 1
        #               --location
        #               https://alexa.amazon.de
        # -A (--user-agent)
        # -b (--cookie)
        # -c (--cookie-jar)
        # -d (--data)        # Sends the specified data in a POST request to the HTTP server
        # -D (--dump-header) # capture cookies for later use
        # -H (--header)
        # -L (--location)    # If the server reports that the requested page has moved to a different location
        #                    # (indicated with a Location: header and a 3XX response code), this option will make
        #                    # curl redo the request on the new place
        # -s (--silent)
        self.__print__("-1- request headers for url {}:\n{}".format(
            self.PI3D_ALEXA_ACCOUNT_BASE_URL, json.dumps(dict(self.session.headers), indent=4)))
        resp = self.session.get(self.PI3D_ALEXA_ACCOUNT_BASE_URL)
        self.__print__("-1- cookies from response: {}".format(json.dumps(resp.cookies.get_dict(), indent=4)))
        self.__print__("-1- full response header history: {}".format(__dump_headers__(resp.history)))
        self.__print__("-1- resp-headers: {}".format(json.dumps(dict(resp.headers), indent=4)))
        # self.__print__("-1- http response: {}, redirect history: {}".format(resp.status_code, resp.history))

        # At this point, the following cookies are expected:
        # .amazon.de      TRUE    /       TRUE    1643818649      session-id-time 2243002649l
        # .amazon.de      TRUE    /       TRUE    1643818649      session-id      260-5474904-2465521
        self.__print__("-1- session cookies: {}".format(json.dumps(dict(self.session.cookies), indent=4)))
        self.__cookie_checker__(['session-id', 'session-id-time'], resp.text)

        # probably safer to use https://requests.readthedocs.io/projects/requests-html/en/latest/index.html to extract
        # form data, but hey, this saves us from using another library
        post_data = __get_form_data__(resp.text)
        self.__print__("-1- post_data, extracted from <form name=signIn>: {}".format(json.dumps(post_data, indent=4)))

        # -2- alexa_remote_control.sh: login empty to generate session
        # /usr/bin/curl --compressed
        #               --http1.1
        #               --silent
        #               --cookie-jar /tmp/.alexa.cookie
        #               --cookie /tmp/.alexa.cookie
        #               --user-agent Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:1.0) bash-script/1.0
        #               --header Accept-Language: de,en-US;q=0.7,en;q=0.3
        #               --header DNT: 1
        #               --header Connection: keep-alive
        #               --header Upgrade-Insecure-Requests: 1
        #               --location
        #               --header Referer: https://www.amazon.de/ap/signin?showRmrMe=1&openid.return_to=https%3A%2F%2Falexa.amazon.de%2F&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=amzn_dp_project_dee_de&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2
        #               --data @/tmp/.alexa.postdata
        #               https://www.amazon.de/ap/signin
        #
        # das was curl mit Location: -> Referer macht, finde ich in resp.url (und muss es in die Headers einbauen)
        req_headers = {"Referer": resp.url}
        # self.session.headers.update({"Referer": resp.url})
        www_amazon_signin = self.url_signin.replace('https://alexa', 'https://www')
        self.__print_request_headers__("-2- request headers for url ", www_amazon_signin, req_headers)
        resp = self.session.post(www_amazon_signin, data=post_data, headers=req_headers)
        self.__print__("-2- cookies from response: {}".format(json.dumps(resp.cookies.get_dict(), indent=4)))
        # self.__print__("-2- full response header history: {}".format(self.__dump_headers__(resp.history)))
        # self.__print__("-2- http response: {}, redirect history: {}".format(resp.status_code, resp.history))
        post_data_2 = __get_form_data__(resp.text)
        self.__print__("-2- post_data_2, extracted from <form name=signIn>: {}".format(
            json.dumps(post_data_2, indent=4)))
        self.__print__("-2- session cookies: {}".format(json.dumps(dict(self.session.cookies), indent=4)))
        # At this point, the following cookies are expected:
        # .amazon.de      TRUE    /       TRUE    1643802922      ubid-acbde      261-4256818-1121614
        # .amazon.de      TRUE    /       TRUE    1643802922      session-id      262-9658785-0092955
        # .amazon.de      TRUE    /       TRUE    1643802922      session-id-time 2242986922l
        self.__cookie_checker__(['ubid-acbde', 'session-id', 'session-id-time'], resp.text)

        # -3- alexa_remote_control.sh: add OTP if using MFA
        # todo: implement as well
        # OTP=$(${OATHTOOL} -b --totp "${MFA_SECRET}")
        # PASSWORD="${PASSWORD}${OTP}"

        # -4- alexa_remote_control.sh: login with filled out form
        # /usr/bin/curl --compressed
        #               --http1.1
        #               --silent
        #               --dump-header /tmp/.alexa.header2
        #               --cookie-jar /tmp/.alexa.cookie
        #               --cookie /tmp/.alexa.cookie
        #               --user-agent Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:1.0) bash-script/1.0
        #               --header Accept-Language: de,en-US;q=0.7,en;q=0.3
        #               --header DNT: 1
        #               --header Connection: keep-alive
        #               --header Upgrade-Insecure-Requests: 1
        #               --location
        #               --header Referer: https://www.amazon.de/ap/signin/257-0930944-9244821
        #               --data-urlencode email=xyz@abc.com
        #               --data-urlencode password=abcdefghijklmnopqrstuvwxyz
        #               --data @/tmp/.alexa.postdata2
        #               https://www.amazon.de/ap/signin
        referer_url = "{}/{}".format(
            self.url_signin.replace('https://alexa', 'https://www'), resp.cookies.get_dict()['session-id'])
        # self.session.headers.update({"Referer": referer_url})
        req_headers = {"Referer": referer_url}
        post_data_2['email'] = self.PI3D_ALEXA_ACCOUNT_USERNAME
        post_data_2['password'] = self.PI3D_ALEXA_ACCOUNT_PASSWORD
        # self.__print__("-4- request headers for url {}:\n{}".format(
        #     www_amazon_signin, json.dumps(dict(self.session.headers), indent=4)))
        self.__print_request_headers__("-4- request headers for url ", www_amazon_signin, req_headers)

        resp = self.session.post(www_amazon_signin, data=post_data_2, headers=req_headers)
        self.__print__("-4- cookies from response: {}".format(json.dumps(resp.cookies.get_dict(), indent=4)))
        self.__print__("-4- session cookies: {}".format(json.dumps(dict(self.session.cookies), indent=4)))
        self.__print__("-4- full response header history: {}".format(__dump_headers__(resp.history)))
        self.__print__("-4- resp-headers: {}".format(json.dumps(dict(resp.headers), indent=4)))
        # At this point, if you only see below for cookies, login failed :( ('...' indicates shortening for brevity)
        # .amazon.de              TRUE    /       TRUE    1643913072      session-token   w40+Dz22JlgcRK0bwChITez68fa...
        # .amazon.de              TRUE    /       TRUE    1643913072      session-id-time 2243097072l
        # .amazon.de              TRUE    /       TRUE    1643913072      session-id      258-6955739-5827339
        # .amazon.de              TRUE    /       TRUE    1643913072      ubid-acbde      257-6075860-7808122

        # This is how it should look like...
        # #HttpOnly_.amazon.de    TRUE    /       TRUE    1643913652      sst-acbde       Sst1|PQEYJ2_IdARDus...
        # #HttpOnly_.amazon.de    TRUE    /       TRUE    1643913656      sess-at-acbde   "22iuCMPTr+heD3D9Oe...
        # #HttpOnly_.amazon.de    TRUE    /       TRUE    1643913652      at-acbde        Atza|IwEBIIVNE00Whd...
        # .amazon.de              TRUE    /       TRUE    1643913656      x-acbde         "i1RgpI9oTGqXe17cGN...
        # .amazon.de              TRUE    /       TRUE    1643913656      session-token   "BGeCw+abH5q17zC++q...
        # .amazon.de              TRUE    /       TRUE    1643913652      session-id-time 2243097652l
        # .amazon.de              TRUE    /       TRUE    1643913652      session-id      258-6559226-1247140
        # .amazon.de              TRUE    /       TRUE    1643913652      ubid-acbde      259-3931130-3788518
        self.__cookie_checker__(['sst-acbde', 'sess-at-acbde', 'at-acbde', 'x-acbde', 'session-token'], resp.text)
        # todo: scripts checks existence of header Location
        if len(resp.history) > 0 and resp.history[0].raw.getheader('Location'):
            # resp.history[0].raw.getheaders()['Location']
            self.__print__('Login successful! ')
        else:
            self.__print__("login failed")
        # pdb.set_trace()

    def __get_csrf__(self):
        # details see section '# get CSRF' in alexa_remote_control.sh
        # csrf is stored in a cookie:
        # .amazon.de      TRUE    /       FALSE   1927830663      csrf    -433619994
        # if it does not exist, it may be retrieved with:
        # /usr/bin/curl
        #       --compressed
        #       --http1.1
        #       -s
        #       -c /tmp/.alexa.cookie
        #       -b /tmp/.alexa.cookie
        #       -A Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:1.0) bash-script/1.0 -H DNT: 1
        #       -H Connection: keep-alive
        #       -L
        #       -H Referer: https://alexa.amazon.de/spa/index.html
        #       -H Origin: https://alexa.amazon.de
        #       https://alexa.amazon.de/api/language
        # self.session.cookies.clear_expired_cookies()  # todo: implement or delete
        # pdb.set_trace()
        if 'csrf' in self.session.cookies.get_dict().keys():
            return True
        req_headers = {"Origin": self.PI3D_ALEXA_ACCOUNT_BASE_URL}
        req_url = "{}/api/language".format(self.PI3D_ALEXA_ACCOUNT_BASE_URL)
        self.__print_request_headers__("csrf() - request headers for url ", req_url, req_headers)
        resp = self.session.get(req_url, headers=req_headers)
        self.__print__("csrf() - session cookies: {}".format(json.dumps(dict(self.session.cookies), indent=4)))
        if re.search('form name=.signIn. method', resp.text):
            self.__print__("csrf() - Amazon sent login page at this point, you are not signed in")
            exit(1)
        self.__cookie_checker__(['csrf'], resp.text)
        # self.session.headers.update({"csrf": self.session.cookies['csrf']})
        # "csrf": self.session.cookies['csrf']
        # if 'csrf' not in resp.cookies.get_dict():
        #     self.__print__('die')
        return True

    def __bootstrap__(self):
        # _log.info("__bootstrap__ - getting gui version and customerId and also verify login was successful")
        params = {"version": 0}
        resp = self.session.get(self.url_bootstrap, params=params)
        if resp.status_code == 200:
            resp_json = json.loads(resp.text)
            if resp_json['authentication']['authenticated']:
                _log.info("Hi {}, you have successfully logged in at {}".format(
                    resp_json['authentication']['customerName'], self.url_signin))
                self.customerId = resp_json['authentication']['customerId']
                self.muteAdverts.customerId = self.customerId
        else:
            _log.info("__bootstrap__ - login failed, sorry")
            exit(1)

    def __get_device_list__(self):
        #
        # /usr/bin/curl
        #   --compressed
        #   --http1.1
        #   -s
        #   -b /tmp/.alexa.cookie
        #   -A Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:1.0) bash-script/1.0
        #   -H DNT: 1
        #   -H Connection: keep-alive
        #   -L
        #   -H Content-Type: application/json; charset=UTF-8
        #   -H Referer: https://alexa.amazon.de/spa/index.html
        #   -H Origin: https://alexa.amazon.de
        #   -H csrf: -1605331471
        #   https://alexa.amazon.de/api/devices-v2/device?cached=false
        if not self.__get_csrf__():
            _log.info("csrf cookie missing")
            exit(1)
        self.session.headers.update({"csrf": self.session.cookies['csrf']})
        self.__print__(self.url_device)
        lang_header = {'Accept-Language': 'en-US;q=0.7,en;q=0.3'}  # make sure we get name 'This Device'
        resp = self.session.get(self.url_device, headers=lang_header)
        dev_info = json.loads(resp.text)
        self.__print__(json.dumps(dev_info, indent=4))
        names = [dev_info['devices'][i]['accountName'] for i in range(0, len(dev_info['devices']))]
        self.__print__(names)
        self.__print__("__get_device_list__ resp-headers: {}".format(json.dumps(dict(resp.headers), indent=4)))
        self.devices.load_from_response(resp.text)
        self.devices.get_device_names()

    def __get_historical_queue__(self):
        _log.info("not yet implemented")
        # spannend, weil man da die grossen album arts holen kann:
        # https://alexa.amazon.de/api/media/historical-queue?deviceSerialNumber=G091AA0704660XVC&deviceType=A2U21SRK4QGSE1&size=50&offset=-1&_=1612984167266
        # aber leider erst, wenn das stueck fertig ist

    def __get_imageURL__(self, echo_device: Device, is_ad: bool = False):
        req_params = {"deviceSerialNumber": echo_device.serialNumber, "deviceType": echo_device.deviceType,
                      "screenWidth": "1920"}
        imageURL, content_length, np, qi, img_url = None, 0, echo_device.now_playing, echo_device.queue_info, {}
        img_size = {}
        img_url['qi'] = qi.url if qi is not None and qi.url != '' else None
        img_url['np'] = np.mainArt.url if np is not None and np.mainArt is not None and np.mainArt.url != '' else None
        img_url['ms'] = None
        img_url['so'] = None
        m = re.match('Sonos', echo_device.active_skill, re.IGNORECASE) if echo_device.active_skill is not None else None
        if m:
            img_url['so'] = self.sonos.get_album_art_url(echo_device.accountName)
        try:
            resp = self.session.get(self.url_media_state, params=req_params)
            resp_json = json.loads(resp.text)
            img_url['ms'] = resp_json['imageURL'] if 'imageURL' in resp_json.keys() else None
        except (requests.exceptions.ConnectionError, json.decoder.JSONDecodeError):
            _log.warning("__get_imageURL__ - [{}] connection reset. img_url['ms']=None".format(echo_device.accountName))
            return None
        if resp.status_code != requests.codes.ok:
            _log.warning("__get_imageURL__ - [{}] could not get media state. url: {}, resp: {}".format(
                echo_device.accountName, resp.url, resp.text))
        try:
            for k in img_url.keys():
                img_size[k] = None
                if img_url[k] is not None:
                    try:
                        resp = self.session.head(img_url[k])
                        img_size[k] = resp.headers['Content-Length'] if 'Content-Length' in resp.headers.keys() else 0
                    except:
                        _log.warning("__get_imageURL__ - [{}] failed. resp.text={}\nTraceback:\n{}".format(
                            echo_device.accountName, resp.text, traceback.format_exc()))
                _log.debug("__get_imageURL__ - [{}] img_url['{}']='{}' ({} bytes)".format(
                    echo_device.accountName, k, img_url[k], img_size[k] if img_size[k] is not None else 0))
            img_quality = list(dict(sorted({k: img_size[k] for k in img_size.keys() if img_size[k] is not None}.items(),
                                           key=itemgetter(1), reverse=True)).keys())
            if len(img_quality) > 0:
                # found image-urls and size information
                idx = img_quality[0]
                _log.info("__get_imageURL__ - [{}] img_url['{}']='{}' ({} bytes)".format(
                    echo_device.accountName, idx, img_url[idx], img_size[idx]))
                return img_url[idx]
            else:
                _log.info("__get_imageURL__ - [{}] img_url=None (0 bytes)".format(echo_device.accountName))
                return None
        except:
            _log.warning("__get_imageURL__ - [{}] failed. resp={}\nTraceback:\n{}".format(
                echo_device.accountName, resp.text, traceback.format_exc()))
            return None

        # Das bringt das gewuenschte AlbumArt :)

        # https://alexa.amazon.de/api/media/state?deviceSerialNumber=G091AA0704660XVC&deviceType=A2U21SRK4QGSE1&screenWidth=1920&_=1612984167264
        # {
        #    "clientId":"Dee-Domain-Music",
        #    "contentId":"2513700",
        #    "contentType":"TRACKS",
        #    "currentState":"PAUSED",
        #    "imageURL":"https://cdns-images.dzcdn.net/images/cover/22c035481afdd2d9452e6dae98a7f11d/500x500-000000-80-0-0.jpg",
        #    "isDisliked":false,
        #    "isLiked":false,
        #    "looping":false,
        #    "mediaOwnerCustomerId":null,
        #    "muted":false,
        #    "programId":null,
        #    "progressSeconds":273,
        #    "providerId":"MUSIC_SKILL",
        #    "queue":null,
        #    "queueId":null,
        #    "queueSize":0,
        #    "radioStationId":null,
        #    "radioVariety":0,
        #    "referenceId":"0ebab2ba-b57f-42f1-bee4-d7cebbbd2469:13",
        #    "service":"UNKNOWN",
        #    "shuffling":false,
        #    "timeLastShuffled":0,
        #    "volume":30
        # }

    def __get_queue_info(self, echo_device: Device):
        # "https://alexa.amazon.de/api/np/queue?
        #     deviceSerialNumber=39f4fe60c4f944c49cb3ee9625e673a8&
        #     deviceType=A3C9PE6TNYLTCH&
        #     size=25&_=1613164746693"
        req_params = {"deviceSerialNumber": echo_device.serialNumber, "deviceType": echo_device.deviceType}
        try:
            resp = self.session.get(self.url_queue_info, params=req_params)
        except (ConnectionResetError, ConnectionError, urllib3.exceptions.ProtocolError, OSError):
            _log.warning("__get_queue_info - connection error on {}. Traceback:{}\n".format(
                resp.url, traceback.format_exc()))
            return
        if resp.status_code != requests.codes.ok:
            _log.info("__get_queue_info - [{}] could not get queue info. resp: {}".format(
                echo_device.accountName, resp.text))
            return
        echo_device.queue_info = QueueInfo(resp.text, echo_device.accountName)

    def now_playing(self, init: ScheduleMode = ScheduleMode.normal) -> int:
        # change_list, ada, self.playing_list = [], self.devices.all_devices_active, []
        self.song_changed = False
        change_list, ada = [], self.devices.all_devices_active
        adl = [e.accountName for e in ada]
        (ed_list, sleep_duration) = self.alexa_schedule_device_checks(init)
        _log.debug("now_playing - ed_list={}, sleep_duration={:.1f}s, active devices: {}".format(
            [ed.accountName for ed in ed_list], sleep_duration, adl))
        if init == ScheduleMode.normal:
            # tidy playing_list from entries with idle echo devices
            for i in [k for k in self.playing_list.keys() if k not in adl]:
                rm_element(self.playing_list, i)
        sleep_end = time.time() + sleep_duration
        self.icy_event.wait(timeout=sleep_duration)
        is_icy_event = self.icy_event.is_set() and init == ScheduleMode.normal
        _log.debug("now_playing - ed_list={}, sleep_duration<now: {}, is_icy_event='{}'".format(
            [ed.accountName for ed in ed_list], sleep_end < time.time(), is_icy_event))
        if is_icy_event:
            # ICY Tag change detected
            for ed in [e for e in self.devices.all_devices_active]:
                if ed.active_skill == 'TuneIn':
                    # pdb.set_trace()
                    if ed.radio_station is not None:
                        icy = ed.radio_station_icy.icy_tags
                        _log.info("now_playing - [{}]->icy station='{}', icy_tag='{}', last_played'{}'".format(
                            ed.accountName, ed.radio_station, icy.now_playing_song_name, ed.song_title_last_played))
                        if ed.song_title_last_played != icy.now_playing_song_name:
                            _log.info("now_playing - [{}]->icy station='{}' new song: '{}'".format(
                                ed.accountName, ed.radio_station, ed.radio_station_icy.icy_tags.now_playing_song_name))
                            # todo: Some stations need __get_imageURL__, some __radio_time_info__
                            self.playing_list[ed.accountName] = {  # "echo-device": ed.accountName,
                                "skill": "TuneIn", "song": icy.now_playing_song_name, "artist": None,
                                "station": ed.radio_station,
                                "img_url": self.__radio_time_info__('Browse', ed.radio_station_icy.station_id, ed)}
                            change_list.append(ed.accountName)
                            self.song_changed = True
                else:
                    _log.info("now_playing - [{}]->icy station=None (not ready yet)".format(ed.accountName))
        if sleep_end < time.time():
            for ed in ed_list:
                params = self.devices.get_now_playing_payload(ed.serialNumber)
                cont_header = {'Content-Type': 'application/json; charset=UTF-8'}
                try:
                    resp = self.session.get(self.url_player, params=params, headers=cont_header)
                except (ConnectionResetError, requests.exceptions.ConnectionError, urllib3.exceptions.ProtocolError):
                    _log.info("now_playing - [{}] - skipping this device for this round. Traceback:\n{}".format(
                        ed.accountName, traceback.format_exc()))
                    continue
                resp_json = json.loads(resp.text)
                if resp.status_code == 400 and 'message' in resp_json.keys() and resp_json['message'] is None:
                    change_list.append(self.devices.update_device_now_playing(resp.text, ed))
                    rm_element(self.playing_list, ed.accountName)
                    self.station_list.untune_station(ed)
                    ed.active_skill = None
                    ed.deviceState = DeviceState.idle
                    ed.next_check = time.time() + self.PI3D_NOW_PLAYING_CHECK_IDLE_DEVICES
                elif resp.status_code == 400 and 'message' in resp_json.keys():
                    change_list.append(self.devices.update_device_now_playing('{"message":null}', ed))
                    self.station_list.untune_station(ed)
                    ed.deviceState = DeviceState.idle
                    rm_element(self.playing_list, ed.accountName)
                    ed.next_check = time.time() + self.PI3D_NOW_PLAYING_CHECK_IDLE_DEVICES
                    _log.info("now_playing - [{}]->sdl message {}".format(ed.accountName, resp_json['message']))
                elif resp.status_code == requests.codes.ok:
                    try:
                        change_list.append(self.devices.update_device_now_playing(resp.text, ed))
                        # if ed.accountName == 'Kitchen':
                        #     _log.info("[{}] - json_resp={}".format(ed.accountName, json.dumps(resp_json, indent=4)))
                        #     pdb.set_trace()
                        if ed.now_playing is None or ed.now_playing.infoText is None or \
                                ed.now_playing.infoText.title is None:
                            _log.info("now_playing - [{}] - ed.now_playing.infoText is None, no further actions")
                        elif ed.now_playing is not None and ed.song_title_last_played != ed.now_playing.infoText.title:
                            self.song_changed = True
                            if ed.now_playing is not None:
                                img_url = self.__get_imageURL__(ed)
                                radio_station = ed.radio_station
                                if radio_station is None and ed.now_playing.miniArt.altText == 'TuneIn':
                                    radio_station = ed.now_playing.infoText.subText1
                                _log.info("now_playing - [{}]->sdl a) skill: '{}', song: '{}'".format(
                                    ed.accountName, ed.active_skill, ed.now_playing.infoText.title))
                                # pdb.set_trace()
                                self.playing_list[ed.accountName] = {  # "echo-device": ed.accountName,
                                    "skill": ed.active_skill, "song": ed.now_playing.infoText.title,
                                    "artist": ed.now_playing.infoText.subText1,
                                    "station": radio_station, "img_url": img_url}
                    except AttributeError:
                        _log.info("now_playing - [{}]->sdl unexpected error. Traceback:\n{}".format(
                            ed.accountName, traceback.format_exc()))
                else:
                    _log.info(
                        "now_playing - [{}]->sdl unexpected http status {}.\nurl: '{}', json response:\n{}".format(
                            ed.accountName, resp.status_code, resp.url, json.dumps(json.loads(resp.text), indent=4)))
            # adding radio now_playing elements
            current_ed = None
            try:
                for ed in [e for e in self.devices.all_devices_active if e.active_skill == 'TuneIn']:
                    # and e.radio_station_icy.icy_tags is not None]:  # e.radio_station_icy is not None and
                    current_ed = ed.accountName
                    if ed.radio_station_icy is None:
                        _log.warning("now_playing - [{}]->sdl - a) icy subprocess not started".format(ed.accountName))
                    elif ed.radio_station_icy.icy_tags is None:
                        _log.warning("now_playing - [{}]->sdl - b) icy subprocess not started".format(ed.accountName))
                    else:
                        _log.info("now_playing - [{}]->sdl b) skill: '{}', song: '{}'".format(
                            ed.accountName, ed.active_skill, ed.now_playing.infoText.title))
                        icy = ed.radio_station_icy.icy_tags
                        icysu = icy.now_playing_song_url
                        if icysu is None:
                            icysu = self.__get_imageURL__(ed)
                        self.playing_list[ed.accountName] = {"skill": "TuneIn", "song": icy.now_playing_song_name,
                                                             "artist": None, "station": ed.radio_station,
                                                             "img_url": icysu}
            except:
                _log.info("[{}] unexpected exception. Traceback:\n{}".format(current_ed, traceback.format_exc()))
                pdb.set_trace()
                print("abc")

        self.icy_event.clear()
        if len([c for c in change_list if c]) > 0:
            dev_list, _ = self.alexa_schedule_device_checks(ScheduleMode.get_active_elements)
            volume_updated = False
            for e in dev_list:  # self.devices.all_devices_active:
                if e.deviceState == DeviceState.active:
                    self.__get_queue_info(e)  # todo: clever criteria to get queueInfo only when needed
                    qi = e.queue_info
                    if qi is None:
                        pass
                    elif qi.serviceName == 'TUNE_IN':
                        e.active_skill, severity, new_station = 'TuneIn', logging.INFO, qi.infoText.subText1
                        f = "now_playing - [{}] qi.contentId='{}', qi.infoText.subText1='{}', qi.search_term='{}'"
                        _log.info(f.format(e.accountName, qi.contentId, qi.infoText.subText1, qi.search_term))
                        if qi.infoText.subText1 is None and qi.infoText.subText2 is None and \
                                qi.infoText.title is not None and \
                                (e.radio_station is None or e.radio_station != qi.infoText.subText1):
                            new_station = qi.infoText.title
                            f = "a) Extracted new station name '{}' from qi.infoText.title".format(new_station)
                        elif qi.infoText.subText1 is None:
                            severity = logging.WARNING
                            f = "b) Station Name=None, cannot tune into station"
                            f += "\nqi.infoText.title='{}'".format(qi.infoText.title)
                            f += "\n[{}] - qi={}".format(e.accountName, json.dumps(qi.raw, indent=4))
                        elif e.radio_station is None or e.radio_station != qi.infoText.subText1:
                            f = "c) from idle to active '{}'".format(new_station)
                        elif e.tunein_id != qi.contentId:
                            f = "d) from old station '{}' to new station '{}'".format(e.tunein_id, qi.contentId)
                        else:
                            f = "e) no action required"
                        # _log.info("now_playing - [{}] TUNE_IN {}".format(e.accountName, f))
                        _log.log(severity, "now_playing - [{}] TUNE_IN {}".format(e.accountName, f))
                        if f[:1] in ['a', 'c', 'd']:
                            station_url = self.__radio_time_info__('Tune', qi.contentId, e)
                            e.radio_station_icy = self.station_list.tune_into_station(
                                new_station, qi.contentId, station_url, self.icy_event, e)
                        _log.info("now_playing - [{}] received radio_station_icy={}".format(
                            e.accountName, e.radio_station_icy))

                    elif e.now_playing.infoText.subText2 is not None:
                        if qi.contentId is not None:
                            station_url = self.__radio_time_info__('Tune', qi.contentId, e)
                        e.active_skill = e.now_playing.provider.providerName
                    f = "now_playing - [{}] np: subText1='{}',subText2='{}',title='{}',skill: '{}',providerName='{}'"
                    _log.info(f.format(
                        e.accountName, e.now_playing.infoText.subText1, e.now_playing.infoText.subText2,
                        e.now_playing.infoText.title, e.active_skill, e.now_playing.provider.providerName))
                    if qi is not None:
                        f = "now_playing - [{}] qi: serviceName={}, id={}, displayText={}, url='{}'"
                        _log.info(f.format(e.accountName, qi.serviceName, qi.contentId, qi.displayText, qi.url))
                    ad_check = [ad for ad in self.PI3D_NOW_PLAYING_AD_TITLES if ad == e.now_playing.infoText.title]
                    if len(ad_check) > 0:
                        _log.info("[{}] - current song title '{}' is in list PI3D_NOW_PLAYING_AD_TITLES={}".format(
                            e.accountName, e.now_playing.infoText.title, self.PI3D_NOW_PLAYING_AD_TITLES))
                        self.muteAdverts.fifo_write('mute_volume', e.accountName, 'immediate')
                        if not volume_updated:
                            # self.echo_volume('save_volume', e)
                            volume_updated = True
                        # self.echo_volume('mute_volume', e)
                    ad_check = [ad for ad in self.PI3D_NOW_PLAYING_AD_TITLES if ad == e.song_title_last_played]
                    # if e.song_title_last_played in self.PI3D_NOW_PLAYING_AD_TITLES:
                    if len(ad_check) > 0:
                        _log.info("[{}] - last song title '{}' is in list PI3D_NOW_PLAYING_AD_TITLES={}".format(
                            e.accountName, e.now_playing.infoText.title, self.PI3D_NOW_PLAYING_AD_TITLES))
                        self.muteAdverts.fifo_write('unmute_volume', e.accountName, 'immediate')
                        # self.echo_volume('unmute_volume', e)
        if self.song_changed:
            playing_list = self.purge_duplicates()
            self.visualize.fifo_write('alexa', playing_list)
        # return self.purge_duplicates()

    def __cookie_checker__(self, req_cookies, html_response):
        # set([1,2]).issubset(set(f))
        cookie_avlb = list(self.session.cookies.get_dict().keys())
        if set(req_cookies).issubset(set(cookie_avlb)):
            self.__print__("cookie_checker - OK, {} part of session cookies".format(req_cookies))
            return True
        else:
            missing = [req_cookies[e] for e in range(0, len(req_cookies)) if req_cookies[e] not in cookie_avlb]
            _log.error("cookie_checker - NOK, the following required {} missing: {}".format(
                "cookie is" if len(missing) == 1 else str(len(missing)) + " cookies are",
                "'" + "', '".join(missing) + "'"))
            _log.info("session cookies: {}".format(json.dumps(dict(self.session.cookies), indent=4)))
            alexa_response_html = os.path.join(self.LOG_DIR, 'alexa_response.html')
            with open(alexa_response_html, 'w') as f:
                f.write(html_response)
            _log.info('''alexa login failed. If the problem persists, open {} in browser, delete cookies and login 
            (from the page {}), you might need to solve a captcha'''.format(
                alexa_response_html, os.path.basename(alexa_response_html)))
            # pdb.set_trace()
            exit(1)

    def alexa_schedule_device_checks(self, init: ScheduleMode = ScheduleMode.normal) -> ([DeviceClass], float):
        """
        Scheduling algorithm for echo device status probing:
        ====================================================
        [0] when a) init=True or b) init=False periodically: calling __get_device_list__(), which
            a) creates a list of all echo devices in state DeviceState.uninitialized or b) updates the existing list
            self.all_devices in class Devices. Called 'dd'.
            Other device states: DeviceState.idle DeviceState.active. No action on [0] in this method.
        [1] determine echo devices with DeviceClass.hw_device and DeviceState.active. Called 'ad'.
            (DeviceClass values: DeviceClass.hw_device, DeviceClass.multi_room_music_group or DeviceClass.any)
        [2] identify echo devices in DeviceState.active and in DeviceClass.multi_room_music_group. Called 'ag'
        [3] remove members (self.clusterMembers) of DeviceClass.multi_room_music_group with DeviceState.active.
            Called 'td' (temporarily disabled devices) todo: check! td seems not being used anywhere
        [4] todo: rephrase
            new: get devices in DeviceState.idle (disregarding the DeviceClass). Called 'id'
            old: from the 'idle' devices (type=['HW', 'group']), which are not members of active groups 'dl', determine
            the one with the check date furthest back in the past
            identify echo devices in DeviceState.idle, which are not members of active groups 'ia'
        [5] return computed list of devices to scan

        Variable Reference:
        ===================
        dd: (not in use) alias for self.devices.all_devices, list of all echo devices, class: DeviceClass
        mg: Multi-Room Music Groups. E.g.: {'Den': ['Beats Echo Studio', 'Stube']}
        ad: active echo devices (from type: HW and status: active)
        ag: active Multi-Room Music Groups (Alexa is currently playing a song on this group). E.g.: ['Den']
        ae: active elements (='ag' + 'ad' not members of 'ag')
        dm: disabled members, as they are group members of an active 'ag'. E.g. ['Beats Echo Studio', 'Stube']
        dl: dd only with 'last_checked', e.g. {'Beats Echo Studio': 1610982726.9706964, 'Stube': 1610982726.9706964, ...
            excluding 'dm' and 'ag'

        :return: list of DeviceClass echo_devices to check or if list is empty, time when next check
        needs to be conducted
        """

        if init == ScheduleMode.init:
            self.__get_device_list__()  # [0] a)
            return self.devices.all_devices, 0.0
        dd = self.devices.all_devices

        # [1]
        ad = [ed for ed in self.devices.all_devices if ed.deviceState == DeviceState.active and
              ed.deviceClass == DeviceClass.hw_device]
        # [2]
        ag = [ed for ed in self.devices.all_devices if ed.deviceState == DeviceState.active and
              ed.deviceClass == DeviceClass.multi_room_music_group]

        # [3]
        lol = [d.clusterMembers for d in ag]  # lol: list of lists containing member IDs of active mg
        device_ids = [item for sublist in lol for item in sublist]  # flatten list of lists to just a list
        dm = [self.devices.get_device_by_id(ed_id) for ed_id in device_ids]

        # [4]
        ia = [d for d in dd if d.deviceState in [DeviceState.uninitialized, DeviceState.idle]]

        # pdb.set_trace()
        # todo: remove dm from ad and merge with ag to new list of active entities ae
        ae = ag + [e for e in ad if e not in dm]
        self.devices.all_devices_active = ae
        if init == ScheduleMode.get_active_elements:
            return ae, 0
        # devices_to_check_active = [d.next_check for d in ae if d.next_check < time.time()]
        # sleep_time = self.PI3D_NOW_PLAYING_CHECK_IDLE_DEVICES

        # determine minimum wait time for ae
        ready_list = [d for d in ae + ia if d.next_check < time.time()]
        ae_ready_list = [e.next_check for e in ae if e.next_check < time.time()]
        ia_ready_list = [e.next_check for e in ia if e.next_check < time.time()]
        if len(ae_ready_list) + len(ia_ready_list) == 0:
            # no device needs to be checked. determine earliest next_check date
            sleep_time = max(0, min([e.next_check for e in ae + ia]) - time.time())
            # pdb.set_trace()
            _log.info(
                'alexa_schedule_device_checks - a) no device needs checking now. sleeping {:6.1f}s'.format(sleep_time))
        else:  # if len(ae_ready_list) == 0 and len(ia_ready_list) > 0
            # some inactive or active devices need checking
            sleep_time = max(0, min([e.next_check for e in ae + ia if e.next_check < time.time()]) - time.time())
            _log.info("alexa_schedule_device_checks - b) no active device needs checking")

        mled = max([len(n.accountName) for n in ae + ia]) if len(ae + ia) > 0 else 0  # mled: max length echo device
        mlst = max([len(n.deviceState.value) for n in ae + ia]) if len(ae + ia) > 0 else 0  # mlst: len deviceState
        aeia = ae + ia
        for e in [k for k in sorted(aeia, key=lambda x: x.next_check, reverse=True)]:  # ae + ia:
            skill = "{}".format(e.active_skill)
            skill += " ({})".format(e.radio_station) if e.active_skill == 'TuneIn' else ""
            _log.info("alexa_schedule_device_checks - next check at {}, {:6.1f}s from now, Device: {} - {} - {}".format(
                time.strftime('%H:%M:%S', time.localtime(e.next_check)), e.next_check - time.time(),
                "{0:{1}}".format(e.accountName, mled), "{0:{1}}".format(e.deviceState.value, mlst), skill))
            try:
                np = e.now_playing.infoText.title
            except AttributeError:
                np = None
            ls = e.song_title_last_played
            if e.deviceState == DeviceState.active and np is not None and np not in self.PI3D_NOW_PLAYING_AD_TITLES:
                _log.debug("e.now_playing.infoText.title='{}' e.song_title_last_played='{}'".format(np, ls))
                self.muteAdverts.fifo_write('save_volume', e.accountName, e.next_check)  # xxx
        return ready_list, sleep_time  # if sleep_time > 0 else 0

    def __print__(self, string):
        if self.verbose:
            _log.info(string)

    def __print_request_headers__(self, pre, url, specific_headers):
        self.__print__("{} {}:\n{}".format(
            pre, url, json.dumps({**dict(self.session.headers), **specific_headers}, indent=4)))

    def __radio_time_info__(self, operation, station_id, ed: Device):
        if operation not in ['Tune', 'Browse']:
            _log.error("__compile_radiotime_url - unsupported operation '{}'".format(operation))
            exit(1)
        req_params = {"id": station_id, "formats": "aac,mp3", "partnerId": self.PI3D_RADIOTIME_PARTNER_ID,
                      "serial": ed.serialNumber, "locale": "en",
                      "latlon": ",".join(format(x, ".5f") for x in self.PI3D_RADIOTIME_LATLON),
                      'render': "json" if operation == 'Browse' else 'default'}
        req_url = "http://opml.radiotime.com/{}.ashx".format(operation)

        # operation='Tune' is used to retrieve m3u file containing the stream urls for the given station
        # From: https://itman.in/en/how-to-add-parameters-to-the-url-string-in-python/
        if operation == 'Tune':
            scheme, netloc, path, qs, fragment = urlsplit(req_url)
            qs = urlencode(req_params, doseq=True)
            return urlunsplit((scheme, netloc, path, qs, fragment))
        #
        # operation='Browse', which is used to get a album art url. (station must be in favorites)
        # Problem:
        #   serial=AEE3U5473Q5JLHPE4VAD2VZUJWLA is NOT a echo.deviceId
        # But it can be retrieved with this url:
        # https://alexa.amazon.de/api/tunein/browse?
        #    deviceType=A3RBAYBE7VM004&              Device class: (deviceType)
        #    deviceSerialNumber=G2A0XL0701330EE4&    Device class: (serialNumber)
        #    deviceAccountId=A08154182QTWXU4Z592SU&  Device class: (deviceAccountId)
        #    mediaOwnerCustomerId=A1V39U0JZHHL8O&    Device class: (deviceOwnerCustomerId)
        # which returns (when render=json):
        # {
        #     "available": true,
        #     "browseList": null,
        #     "contentType": "link",
        #     "description": null,
        #     "id": null,
        #     "image": null,
        #     "name": "Favorites",
        #     "url": "http://opml.radiotime.com/Browse.ashx?
        #       c=presets&
        #       formats=aac,mp3&
        #       partnerId=!EALLOjB&
        #       serial=AEE3U5473Q5JLHPE4VAD2VZUJWLA&   Here we go!
        #       locale=en&
        #       latlon=47.42394,8.54116"
        # }
        tunein_params = {"deviceType": ed.deviceType, "deviceSerialNumber": ed.serialNumber,
                         "deviceAccountId": ed.deviceAccountId, "mediaOwnerCustomerId": ed.deviceOwnerCustomerId}
        retry, rc = 3, -1
        while retry > 0 and rc != 0:
            try:
                # print("operation='{}' station_id='{}' echo_device='{}'".format(operation, station_id, ed.accountName))
                tunein_resp = self.session.get(self.url_tunein_browse, params=tunein_params)
                rc = 0
            except (ConnectionResetError, requests.exceptions.ConnectionError):
                retry -= 1
                _log.info("__compile_radiotime_url ConnectionResetError/ConnectionError retry={}".format(retry))
                time.sleep(1)
        if rc != 0:
            _log.error("__compile_radiotime_url exhausted ConnectionResetError retries")
            exit(1)

        tunein_json = json.loads(tunein_resp.text)
        try:
            # todo: just happy path is implemented, make this more robust
            if 'browseList' in tunein_json.keys():
                bl = tunein_json['browseList']
                idx = [i for i in range(0, len(bl)) if bl[i]['name'] == 'Favorites']
                idx = idx[0]
                _, _, _, qs, _ = urlsplit(tunein_json['browseList'][idx]['url'])
                qsp = parse_qs(qs)
                req_params['serial'] = qsp['serial'][0]
                req_params['c'] = "presets"
                resp = self.session.get(req_url, params=req_params)
                if resp.status_code != requests.codes.ok:
                    _log.info("__radio_time_info__ - [{}] '{}' failed with http code {}, resp: {}".format(
                        ed.accountName, req_url, resp.status_code, resp.text))
                    return None
                resp_json = json.loads(resp.text)
                body = resp_json['body']
                idx1 = [i for i in range(0, len(body)) if body[i]['guide_id'] == station_id]
                prefix = "__radio_time_info__ - [{}] -".format(ed.accountName)
                comment = ""
                if len(idx1) > 0:
                    idx1 = idx1[0]
                    # body[idx1]['guide_id'] == station_id
                    # body[idx1]['image'] contains the stations logo
                    # body[idx1]['playing_image'] contains album art of current song, not always available!
                    # pdb.set_trace()
                    rv = body[idx1]['playing_image'] if 'playing_image' in body[idx1].keys() else body[idx1]['image']
                else:
                    rv = None
                    comment = " # must add to favorites"
                    _log.warning("{} station '{}' not in favorites".format(prefix, ed.radio_station))
                    _log.info("{} on '{}', go to Music & Books > TuneIn > Favorites and add '{}'.".format(
                        prefix, self.PI3D_ALEXA_ACCOUNT_BASE_URL, ed.radio_station))
                _log.info("__radio_time_info__ - [{}] img_url='{}'{}".format(ed.accountName, rv, comment))
                ed.radio_station_icy.icy_tags.now_playing_song_url = rv
                return rv
        except (KeyError, IndexError) as exc:
            pdb.set_trace()
            _log.info("__radio_time_info__ - [{}] failed. Traceback:\n{}".format(
                ed.accountName, traceback.format_exc()))

    def purge_duplicates(self):
        # identify duplicate song titles and store in 'duplicates':
        playing_list = copy.deepcopy(self.playing_list)
        snp = playing_list  # snp: self-now-playing
        duplicates = [k for k, v in Counter([snp[s]['song'] for s in snp.keys()]).items() if v > 1]
        det, smap, dev_maps = ({}, [], [])
        for s in duplicates:
            anp = playing_list
            ed = [k for k, v in anp.items() if v['song'] == s]  # determine echo_devices with song==s title
            dn = min(ed, key=len)  # determine echo_device with the shortest name
            new_label = "{}+{}".format(dn, len(ed) - 1)  # fake echo name w/ shortest name + # additional devs
            smap.append({"song": s, "dev-map": {k: new_label for k in ed}})

        if smap:
            _log.info("purge_duplicates - detected {} multiple occurrences: smap={}".format(len(smap), smap, indent=4))

        active_list = [ad.accountName for ad in self.devices.all_devices_active]
        for k in self.playing_list.keys():
            _log.info("playing_list['{}']={}".format(k, playing_list[k]))
            if self.playing_list[k]['song'] != '' and self.playing_list[k]['img_url'] != '' and k in active_list:
                _log.debug("purge_duplicates - adding '{}' to now_playing".format(k))
                if self.playing_list[k]['song'] in [e['song'] for e in smap]:
                    anp = playing_list
                    # dev_map = [{'Stube': 'Stube+1', 'Beats Echo Studio': 'Stube+1'}]
                    dev_maps = [i['dev-map'] for i in smap if i['song'] == anp[k]['song']]
                    if len(dev_maps) > 1:
                        _log.error("purge_duplicates - unexpected number of dev_maps: {} {}".format(
                            len, json.dumps(dev_maps, indent=4)))
                        exit(1)
                    elif len(dev_maps) == 1:
                        # dev_maps[0].keys()
                        spl = self.playing_list
                        url_list = set([spl[i]['img_url'] for i in dev_maps[0].keys() if spl[i]['img_url'] is not None])
                        _log.info("url_list={}".format(url_list))
                        playing_list[dev_maps[0][k]] = playing_list[k]
                    else:
                        _log.info("purge_duplicates - this should not happen, please check")
                else:
                    playing_list[k] = playing_list[k]
        if len(dev_maps) > 0:
            for i in [smap[k]['dev-map'] for k in range(0, len(smap))]:
                for l in i:
                    del (playing_list[l])
                    _log.info("purge_duplicates - deleted playing_list[{}]".format(l))
        # delete inactive elements when still in playing list
        all_devices = [ad.accountName for ad in self.devices.all_devices]
        inactive_list = [i for i in all_devices if i not in active_list]
        kill_list = [k for k in playing_list.keys() if k in inactive_list]
        for k in kill_list:
            del (playing_list[k])
        return playing_list


def __get_form_data__(resp_text):
    m = re.search(r'(<form name=.signIn.*?</form>)', resp_text.replace('\n', ''), re.IGNORECASE)
    if m:
        return {i[0]: i[1] for i in re.findall(
            'hidden.\s+name=["\']([^"\']*)["\']\s+value=["\']([^"\']*)["\']\s+', m.group(1))}
    else:
        _log.warning("did not catch <form name='signIn'...</form>. HTML content of response:\n{}".format(
            resp_text
        ))
        return ""
