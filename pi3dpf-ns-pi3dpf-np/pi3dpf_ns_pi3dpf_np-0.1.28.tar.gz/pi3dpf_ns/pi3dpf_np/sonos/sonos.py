import logging
import pdb
import soco
import traceback
import xml.etree.ElementTree as ET
import http.client
import urllib3.exceptions
import requests.exceptions

# from ..common import pf_common as pfc
from pi3dpf_ns.pi3dpf_common import pf_common as pfc

_log = logging.getLogger(__name__)


class Sonos:

    def __init__(self, config):
        self.config = config
        self.PI3D_SONOS_ACCOUNT_USERNAME = pfc.get_config_param(self.config, 'PI3D_SONOS_ACCOUNT_USERNAME')
        self.enabled = True
        if self.PI3D_SONOS_ACCOUNT_USERNAME == 'not-configured':
            _log.info("__init__ - PI3D_SONOS_ACCOUNT_USERNAME='not-configured' - disabling Sonos")
            self.enabled = False
            return
        self.PI3D_SONOS_ACCOUNT_PASSWORD = pfc.get_config_param(self.config, 'PI3D_SONOS_ACCOUNT_PASSWORD')
        self.sonos_zones = {}
        self.soco_sonos_zones = soco.discover()

        if self.soco_sonos_zones is None:
            self.enabled = False
            _log.warning("__init__ - discovery did not yield any sonos zones - disabling Sonos")
            return
        for zone in self.soco_sonos_zones:
            _log.info("__init__ - detected zone '{}' at address {}".format(zone.player_name, zone.ip_address))
            if zone.player_name in self.sonos_zones.keys():
                _log.error("__init__ - {] is not unique".format(zone.player_name))
                continue
            self.sonos_zones[zone.player_name] = zone

    def get_album_art_url(self, player_name):
        if not self.enabled:
            return None
        if player_name not in self.sonos_zones.keys():
            player = self.sonos_zones[player_name]
        else:
            try:
                players, player = [i for i in self.soco_sonos_zones if i.player_name == player_name], None
            except (http.client.RemoteDisconnected, urllib3.exceptions.ProtocolError,
                    requests.exceptions.ConnectionError):
                _log.warning("get_album_art_url - error retrieving images. Traceback:\n{}", traceback.format_exc())
                return None
            if len(players) > 1:
                _log.error("get_album_art_url - ambiguous player name '{}'. Found: {}".format(player_name, players))
                return
            elif len(players) < 1:
                _log.error("get_album_art_url - player '{}' not found".format(player_name))
                return
            else:
                player = players[0]
                self.sonos_zones[player] = player
        np = player.get_current_track_info()
        # np['position']  -
        # np['uri']       -
        # np['metadata']  - holds xml, check for albumArtURI if album_art is empty
        # np['album_art'] - may be empty string
        reason, rv = "c) unable retrieving album_art", None
        try:
            if 'album_art' in np.keys() and np['album_art'] != '':
                reason = "a) album_art as expected"
                rv = np['album_art']
            if 'metadata' in np.keys():
                # data_structures.me
                md = np['metadata']
                _log.info("get_album_art_url - md = '{}'".format(md))
                tree = ET.ElementTree(ET.fromstring(md))
                root = tree.getroot()
                for child in root.iter():
                    if child.tag == '{urn:schemas-upnp-org:metadata-1-0/upnp/}albumArtURI':
                        reason = "b) albumArtURI from metadata"
                        rv = child.text
                        break
        except ET.ParseError:
            reason = "d) xml ParseError. {}".format(traceback.format_exc())

        _log.info("get_album_art_url - album_art='{}' # reason={}".format(rv, reason))
        return rv
