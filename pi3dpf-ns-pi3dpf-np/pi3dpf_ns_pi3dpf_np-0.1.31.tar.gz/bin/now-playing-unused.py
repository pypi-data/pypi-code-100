#!/usr/bin/env python3

from pi3dpf_ns.pi3dpf_common import pf_common as pfc
import logging
from logging.handlers import RotatingFileHandler
# import traceback
# import pdb
# from icy_tags import IcyTags
from pi3dpf_ns.pi3dpf_np.tunein.icy_tags import IcyTags
import atexit
import bdb
import os
import configparser
# import signal
# import sys
# import shutil
import now_playing
import argparse
import time
parse = argparse.ArgumentParser("start running process to find out what's now playing on various media centers")
parse.add_argument("-a", "--verbose-alexa", default=False, action="store_true", help="show cookies and http headers")
args = parse.parse_args()

this_dir = os.path.dirname(__file__)
this_file = os.path.basename(__file__)
nothing_playing = os.path.join(os.path.dirname(pfc.__file__), 'cfg/icons/1x1-transparent.png')
config_file = [os.path.join(os.path.dirname(pfc.__file__), 'cfg/pf.config')]
cfg = configparser.ConfigParser(inline_comment_prefixes=';', empty_lines_in_values=False,
                                converters={'list': lambda x: [i.strip() for i in x.split(',')]})
if os.path.isfile('/home/pi/.pf/pf.config'):
    config_file.append('/home/pi/.pf/pf.config')
cfg.cfg_fname = config_file
cfg.read(config_file)
LOG_LEVEL = pfc.get_config_param(cfg, 'LOG_LEVEL')
LOG_DIR = pfc.get_config_param(cfg, 'LOG_DIR')
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
LOG_FILE = os.path.join(LOG_DIR, os.path.splitext(os.path.basename(__file__))[0])+'.log'
print("for more information, check log file '{}'.".format(LOG_FILE))
LOG_LEVEL = pfc.get_config_param(cfg, 'LOG_LEVEL')
numeric_level = getattr(logging, LOG_LEVEL.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError("Invalid log level: '{}'}".format(LOG_LEVEL))
# logging.basicConfig(level=numeric_level)

# LOG_DIR = pfc.get_config_param(cfg, 'LOG_DIR')
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
# example for logging initialization: https://stackoverflow.com/a/56369583
rotation_handlers = [RotatingFileHandler(LOG_FILE, maxBytes=3_000_000, backupCount=5)]
logging.basicConfig(level=numeric_level,
                    handlers=rotation_handlers,
                    format='%(asctime)s %(levelname)s: %(module)s - %(message)s')
log = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])

PI3D_ALEXA_ACCOUNT_USERNAME = pfc.get_config_param(cfg, 'PI3D_ALEXA_ACCOUNT_USERNAME')
media_player_active = False
alexa = None
if PI3D_ALEXA_ACCOUNT_USERNAME != 'not-configured':
    alexa = now_playing.alexa(cfg, args.verbose_alexa)
    media_player_active = True

try:
    while media_player_active:
        # todo: check! can this be sped up by using https://towardsdatascience.com/supercharge-pythons-requests-with-async-io-httpx-75b4a5da52d7
        if alexa is not None:
            alexa.now_playing()
        # todo: add Plex
        # todo: add Kodi
        # todo: add ...
        # time.sleep(2)
        log.info("ready for the next loop")
except (KeyboardInterrupt, SystemExit, bdb.BdbQuit):
    log.info("tunein mainloop Keyboard interrupt or system exit")
