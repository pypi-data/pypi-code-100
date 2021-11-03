# From: https://github.com/mannibis/plex_api

import copy
import logging
import os
import pdb
import requests
import threading
import time
import traceback
import urllib3.exceptions

import xml.etree.ElementTree as ET
# from ..common import pf_common as pfc
# from ..alexa.visualize import AlexaNowPlayingVisualize
from pi3dpf_ns.pi3dpf_common import pf_common as pfc
from pi3dpf_ns.pi3dpf_np.alexa.visualize import AlexaNowPlayingVisualize
_log = logging.getLogger(__name__)


class Plex:
    def __init__(self, config):
        self.config = config
        self.PI3D_PLEX_SIGN_IN = pfc.get_config_param(self.config, 'PI3D_PLEX_SIGN_IN')
        self.PI3D_PLEX_ACCOUNT_BASE_URL = pfc.get_config_param(self.config, 'PI3D_PLEX_ACCOUNT_BASE_URL')
        self.PI3D_PLEX_ACCOUNT_USERNAME = pfc.get_config_param(self.config, 'PI3D_PLEX_ACCOUNT_USERNAME')
        self.PI3D_NOW_PLAYING_TOP_DIR = pfc.get_config_param(self.config, 'PI3D_NOW_PLAYING_TOP_DIR')
        self.enabled = True
        if self.PI3D_PLEX_ACCOUNT_USERNAME == 'not-configured':
            _log.info("__init__ - PI3D_PLEX_ACCOUNT_USERNAME='not-configured' - disabling Plex")
            self.enabled = False
            return
        self.PI3D_PLEX_ACCOUNT_PASSWORD = pfc.get_config_param(self.config, 'PI3D_PLEX_ACCOUNT_PASSWORD')
        self.visualize = AlexaNowPlayingVisualize(self.config)
        self.visualize.fifo_open('write_noblock')
        self.session = requests.Session()
        self.plex_token = self.get_auth_token()
        self.plex_thread = None
        self.stop_event = threading.Event()
        if self.plex_token is None:
            _log.warning("unable to login at {}".format(self.PI3D_PLEX_SIGN_IN))
            self.enabled = False
        self.counter = 0
        self.now_playing = {}
        self.last_song = {}

    def stop(self):
        self.stop_event.set()

    def stopped(self):
        return self.stop_event.is_set()

    def run(self):
        self.plex_thread = threading.Thread(target=self.start, daemon=True)
        # stopping thread: https://stackoverflow.com/a/2564161
        # and nice description on how to do that properly: https://stackoverflow.com/a/325528
        self.plex_thread.start()

    def start(self):
        while not self.stop_event.is_set():
            rv = self.get_session_data()
            sleep_time = 2 if rv else 120
            time.sleep(sleep_time)

    def get_auth_token(self):
        auth_params = {'user[login]': self.PI3D_PLEX_ACCOUNT_USERNAME,
                       'user[password]': self.PI3D_PLEX_ACCOUNT_PASSWORD}
        headers = {'X-Plex-Product': 'Plex API', 'X-Plex-Version': "0.2", 'X-Plex-Client-Identifier': '112286'}
        try:
            _log.info("get_auth_token - loading '{}'".format(self.PI3D_PLEX_SIGN_IN))
            # auth_request = requests.post(self.PI3D_PLEX_SIGN_IN, headers=headers, data=auth_params)
            auth_request = self.session.post(self.PI3D_PLEX_SIGN_IN, headers=headers, data=auth_params)
            auth_response = auth_request.content
            root = ET.fromstring(auth_response)
            try:
                plex_auth_token = root.attrib['authToken']
                return plex_auth_token
            except KeyError:
                _log.warning("get_auth_token - login with username '{}' at {} was not successful".format(
                    self.PI3D_PLEX_ACCOUNT_USERNAME, self.PI3D_PLEX_SIGN_IN))
                _log.info("get_auth_token - disabling Plex")
                self.enabled = False
        except requests.Timeout or requests.ConnectionError or requests.HTTPError:
            self.enabled = False
            return None

    def get_session_data(self):
        plex_url = '{}/status/sessions'.format(self.PI3D_PLEX_ACCOUNT_BASE_URL)
        plex_params = {'X-Plex-Token': self.plex_token}
        # _log.info("get_session_data - loading '{}'".format(plex_url))
        # plex_response = requests.get(plex_url, params=plex_params)
        try:
            plex_response = self.session.get(plex_url, params=plex_params)
        except (requests.exceptions.ConnectionError, ConnectionResetError, urllib3.exceptions.ProtocolError,
                requests.exceptions.ConnectionError, ConnectionRefusedError):
            _log.warning("get_session_data - {} failed. Traceback:\n{}".format(
                plex_url, traceback.format_exc()))
            return None
        plex_content = plex_response.content
        self.counter += 1
        self.parse_session_data(plex_content)
        return True

    def parse_session_data(self, xmlfile):
        display_list = []
        root = ET.fromstring(xmlfile)

        num_videos = root.get('size')
        # pdb.set_trace()
        if num_videos is not None and int(num_videos) > 0:
            display_list.append('PLEX API: There is/are {} video(s) playing'.format(num_videos))
        else:
            display_list.append('PLEX API: There are currently no videos playing')
        for video in root.findall('Video'):
            if video.get('type') == 'episode':
                show_title = video.get('grandparentTitle')
                episode_title = video.get('title')
                _log.info("ignoring detected video '{}|{}' currently playing".format(show_title, episode_title))
            elif video.get('type') == 'movie':
                movie_title = video.get('title')
                movie_year = video.get('year')
                _log.info("ignoring detected Movie '{} ({})' currently playing".format(movie_title, movie_year))
            for user in video.findall('User'):
                user_name = user.get('title')
            for player in video.findall('Player'):
                player_platform = player.get('platform')
                player_state = player.get('state')
        n, np = 1, {}
        for track in root.findall('Track'):
            idx = "Plex-{:03d}".format(n)  # , self.now_playing[idx]
            np[idx] = {'skill': 'Plex', 'station': None, 'song': track.get('title'), 'album': track.get('parentTitle'),
                       'artist': track.get('grandparentTitle')}
            duration = int(track.get('duration'))   # duration
            duration_txt = time.strftime("%H:%M:%S", time.gmtime(duration//1000))
            duration_txt = duration_txt[3:] if duration_txt[:2] else duration_txt
            viewOffset = int(track.get('viewOffset'))
            completion = 100 * viewOffset / duration
            # _log.info("artist='{}', album='{}', song='{}', duration={}, viewOffset={}, completion={:.2f}%".format(
            #     artist, album, title, duration_txt, track.get('viewOffset'), completion))
            for player in track.findall('Player'):
                # pdb.set_trace()
                address = player.get('address')
                machineIdentifier = player.get('machineIdentifier')
                # _log.info("address={}, machineIdentifier={}".format(address, machineIdentifier))
            np[idx]['img_url'] = self.store_album_art(track.get("thumb"), np[idx]['artist'], np[idx]['album'],
                                                      np[idx]['song'])
            n += 1
        if self.now_playing != np:
            self.visualize.fifo_write('plex', np)
            self.now_playing = copy.deepcopy(np)
        return

    def store_album_art(self, thumb_url, artist, album, song):
        try:
            if thumb_url is None or thumb_url == 'None':
                return None
            full_thumb_url = '{}{}'.format(self.PI3D_PLEX_ACCOUNT_BASE_URL, thumb_url)
            album_thumb_path = os.path.join(self.PI3D_NOW_PLAYING_TOP_DIR, 'plex-thumbs', "{}_{}.jpg".format(
                artist.lower().replace(' ', '.'), album.lower().replace(' ', '.')))
            if not os.path.isfile(album_thumb_path):
                _log.info("get_thumb - loading '{}'".format(full_thumb_url))
                plex_params = {'X-Plex-Token': self.plex_token}
                # plex_response = requests.get(full_thumb_url, params=plex_params)
                plex_response = self.session.get(full_thumb_url, params=plex_params)
                with open(album_thumb_path, 'wb') as of:
                    of.write(plex_response.content)
            return album_thumb_path
        except:
            _log.warning("get_thumb - something went wrong. Traceback:\n{}".format(traceback.format_exc()))
            return None
