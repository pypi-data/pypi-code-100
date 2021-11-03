#!/usr/bin/env python3
# Note: -u option in 'python3 -u' will make sure icy_tags reports new song title w/o any delay
import argparse
import atexit
import bdb
import configparser
import io
import json
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import signal
import sys
import time
import traceback

from pi3dpf_ns.pi3dpf_common import pf_common as pfc
from pi3dpf_ns.pi3dpf_np.tunein.icy_tags import IcyTags
import pi3dpf_ns.pi3dpf_np.alexa.alexa as alexa
import pi3dpf_ns.pi3dpf_np.plex.plex as plex
from pi3dpf_ns.pi3dpf_np.alexa.visualize import AlexaNowPlayingVisualize

def signal_handler(signal, frame):
    print("\n{} - signal_handler: received exit signal".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
    log.info("signal_handler() - signal {} received, terminating.".format(signal))
    exit(0)
    # exit_handler(ax.station_list.stations)


def exit_handler(station_list):
    print("{} - exit_handler: please stand by, winding down threads".format(
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
    if PI3D_NOW_PLAYING_MODE == 'mqtt_distributor':
        # sending empty now_playing
        log.info("exit_handler - publishing empty now playing information for mqtt_receiver to '{}'".format(np_topic))
        axv.client.publish(np_topic, json.dumps({"now_playing": {}}))
    if station_list is not None:
        for st in station_list.keys():
            if isinstance(station_list[st].icy_tags, IcyTags):
                station_list[st].icy_tags.stop()
    if ax is not None:
        ax.exit_handler()
    axv.stop()


# From: https://adamj.eu/tech/2020/06/26/how-to-check-if-pythons-output-buffering-is-enabled/
def output_buffering_enabled():
    return isinstance(sys.__stdout__.buffer, io.BufferedWriter)


parse = argparse.ArgumentParser("start running process to find out what's now playing on various media centers")
parse.add_argument("-a", "--verbose-alexa", default=False, action="store_true", help="show cookies and http headers")
args = parse.parse_args()
this_dir = os.path.dirname(__file__)
this_file = os.path.basename(__file__)
nothing_playing = os.path.join(Path(alexa.__file__).parents[1], 'common/cfg/icons/1x1-transparent.png')
config_file = [os.path.join(Path(alexa.__file__).parents[1], 'cfg', 'np.config')]
cfg = configparser.ConfigParser(inline_comment_prefixes=';', empty_lines_in_values=False,
                                converters={'list': lambda x: [i.strip() for i in x.split(',')]})

if output_buffering_enabled():
    print("ERROR - output buffering must be disabled. (run python -u or set PYTHONUNBUFFERED=x")
    exit(1)
if os.path.isfile('/home/pi/.pf/pf.config'):
    config_file.append('/home/pi/.pf/pf.config')
cfg.cfg_fname = config_file
cfg.read(config_file)
LOG_LEVEL = pfc.get_config_param(cfg, 'LOG_LEVEL')
LOG_DIR = pfc.get_config_param(cfg, 'LOG_DIR')
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
LOG_FILE = os.path.join(LOG_DIR, os.path.splitext(os.path.basename(__file__))[0])+'.log'
print("{} - {}: starting up, for more information, check log file '{}'.".format(
    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), this_file, LOG_FILE))

LOG_LEVEL = pfc.get_config_param(cfg, 'LOG_LEVEL')
numeric_level = getattr(logging, LOG_LEVEL.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError("Invalid log level: '{}'}".format(LOG_LEVEL))

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
# example for logging initialization: https://stackoverflow.com/a/56369583
rotation_handlers = [RotatingFileHandler(LOG_FILE, maxBytes=3_000_000, backupCount=5)]
logging.basicConfig(level=numeric_level,
                    handlers=rotation_handlers,
                    format='%(asctime)s %(levelname)s: %(module)s - %(message)s')
log = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGHUP, signal_handler)
signal.signal(signal.SIGQUIT, signal_handler)
signal.signal(signal.SIGTRAP, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

try:
    media_player_active, ax, px, so, init, song_changed = False, None, None, None, True, False
    playing_lists_now = {'alexa': {}, 'plex': {}, 'kodi': {}}
    playing_lists_old = {'alexa': {'x': 'bogus'}, 'plex': {'x': 'bogus'}, 'kodi': {'x': 'bogus'}}
    log.info("{} starting".format(os.path.basename(__file__)))

    PI3D_NOW_PLAYING_MODE = pfc.get_config_param(cfg, 'PI3D_NOW_PLAYING_MODE')
    MQTT_TOPLEVEL_TOPIC = pfc.get_config_param(cfg, 'MQTT_TOPLEVEL_TOPIC')
    if PI3D_NOW_PLAYING_MODE == 'mqtt_distributor':
        np_topic = "{}_np/now_playing".format(MQTT_TOPLEVEL_TOPIC)

    PI3D_ALEXA_ACCOUNT_USERNAME = pfc.get_config_param(cfg, 'PI3D_ALEXA_ACCOUNT_USERNAME')
    axv = AlexaNowPlayingVisualize(cfg)
    axv.run()
    if PI3D_ALEXA_ACCOUNT_USERNAME != 'not-configured':
        ax = alexa.Alexa(cfg, args.verbose_alexa)
        media_player_active = True
        atexit.register(exit_handler, ax.station_list.stations)
    else:
        log.warning("PI3D_ALEXA_ACCOUNT_USERNAME set to {}, process will not start".format(PI3D_ALEXA_ACCOUNT_USERNAME))

    if PI3D_NOW_PLAYING_MODE == 'mqtt_receiver':
        media_player_active = True
        callable = None if ax is None or ax.station_list is None else ax.station_list.stations
        atexit.register(exit_handler, callable)

    PI3D_PLEX_ACCOUNT_USERNAME = pfc.get_config_param(cfg, 'PI3D_PLEX_ACCOUNT_USERNAME')
    if PI3D_PLEX_ACCOUNT_USERNAME != 'not-configured':
        px = plex.Plex(cfg)
        media_player_active = True
        px.run()

    while media_player_active:
        if PI3D_NOW_PLAYING_MODE == 'mqtt_receiver':
            axv.client.loop_forever()

        if ax is not None:
            _ = ax.now_playing()
            song_changed = True
            init = False

        # todo: add Kodi
        # todo: add emby
        # todo: add jellyfin
        log.debug("ready for the next loop")
except (KeyboardInterrupt, SystemExit, bdb.BdbQuit):
    log.info("mainloop Keyboard interrupt or system exit")
    exit(0)
except:
    log.error("unexpected error. Traceback:\n{}".format(traceback.format_exc()))
    log.info("exiting program")
    exit(1)
