import configparser
import json
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
import pdb
import posix
import re
import requests
import time
from pi3dpf_ns.pi3dpf_common import pf_common as pfc
from pi3dpf_ns.pi3dpf_owm.owm_org import openweathermap as Owm
from pi3dpf_ns.pi3dpf_owm.owm_org import openweathermapToerikflowers_wi as owm_eric
# from pi3dpf_owm_weather.common import pf_common as pfc
# import pi3dpf_owm_weather.owm_org.openweathermap as Owm
# import pi3dpf_owm_weather.owm_org.openweathermapToerikflowers_wi as owm_eric

if "PF_ROOT" not in os.environ.keys() or not os.path.isdir(os.environ["PF_ROOT"]):
    print("ERROR - PF_HOME must point to install directory")
    exit(1)
this_file = os.path.basename(__file__)
this_dir = os.path.dirname(__file__)
config_file = [os.path.join(os.path.dirname(Owm.__file__), 'cfg', 'wm.config')]
cfg = configparser.ConfigParser(inline_comment_prefixes=';', empty_lines_in_values=False,
                                converters={'list': lambda x: [i.strip() for i in x.split(',')]})
# pdb.set_trace()
# if output_buffering_enabled():
#     print("ERROR - output buffering must be disabled. (run python -u or set PYTHONUNBUFFERED=x")
#     exit(1)
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
owm = Owm.OpenWeatherMap(cfg)
owm_pf = owm_eric.owm4pf(cfg, log)  # import pi3dpf_owm_weather.owm_org.openweathermapToerikflowers_wi as owm_eric
OWM_NOW_REFRESH_RATE = pfc.get_config_param(cfg, 'OWM_NOW_REFRESH_RATE')
OWM_DATA_DIR = pfc.get_config_param(cfg, 'OWM_DATA_DIR')
# owm_formatstring
last_5d3h_update = 0
owm_info = owm_pf.update_weather_info()
while True:
    owm.get_5_days()
    if time.time() > last_5d3h_update + 3 * 60 * 60:
        last_5d3h_update = time.time()
        owm_info = owm_pf.update_weather_info()
        for i in range(0, len(owm_info)):
            owm_weather_now_formatstring = os.path.join(OWM_DATA_DIR, 'now', 'owm_formatstring_{}.txt'.format(i))
            if owm_info[i] != "":
                with open(owm_weather_now_formatstring, 'w') as fs_file:
                    fs_file.write(owm_info[i])
                log.info("written file {} with content: '{}'".format(owm_weather_now_formatstring, owm_info[i]))
    time.sleep(OWM_NOW_REFRESH_RATE * 60)
