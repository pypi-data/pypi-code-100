# -*- coding: utf-8 -*-

import obspython as obs
import asyncio
import websockets
import threading
import logging, logging.handlers
from time import sleep

PORT_DEFAULT = 5678
HOSTNAME_DEFAULT = "localhost"

hotkey_id_first = None
hotkey_id_prev = None
hotkey_id_next = None
hotkey_id_last = None
hotkey_id_black = None
hotkey_id_white = None

HOTKEY_NAME_FIRST = 'powerpoint_slides.first'
HOTKEY_NAME_PREV = 'powerpoint_slides.previous'
HOTKEY_NAME_NEXT = 'powerpoint_slides.next'
HOTKEY_NAME_LAST = 'powerpoint_slides.last'
HOTKEY_NAME_BLACK = 'powerpoint_slides.black'
HOTKEY_NAME_WHITE = 'powerpoint_slides.white'

HOTKEY_DESC_FIRST = 'First PowerPoint slide'
HOTKEY_DESC_PREV = 'Previous PowerPoint slide'
HOTKEY_DESC_NEXT = 'Next PowerPoint slide'
HOTKEY_DESC_LAST = 'Last PowerPoint slide'
HOTKEY_DESC_BLACK = 'Black PowerPoint slide'
HOTKEY_DESC_WHITE = 'White PowerPoint slide'

LOG_LEVEL = logging.WARNING

cmd = ""
hostname = HOSTNAME_DEFAULT
port = PORT_DEFAULT
attempts = 0
logger = None
slideshow = ""

logging.basicConfig()

async def communicate():
    async with websockets.connect("ws://%s:%s" % (hostname, port), ping_interval=None) as websocket:
        global cmd
        global attempts 
        while True:
            if cmd:
                try:
                    cmd_temp = cmd
                    cmd = ""
                    await websocket.send('{"presentation": "", "action": "%s"}' % cmd_temp)
                except websockets.ConnectionClosed as exc:
                    logger.info("Failed to send command {}: {}".format(cmd_temp, str(exc)))
                    cmd = cmd_temp
                    attempts += 1
                    if attempts == 4:
                        logger.info("Failed to send command {} after {} attempts - aborting connection".format(cmd_temp, attempts))
                        attempts = 0
                        cmd = ""
                        break
            await asyncio.sleep(0.05 + 0.5*attempts**2)

def run_ws():
    while True:
        logger.debug("Attempting to connect")
        try:
            asyncio.set_event_loop(asyncio.new_event_loop())
            asyncio.get_event_loop().run_until_complete(communicate())
        except (OSError, websockets.exceptions.ConnectionClosedError) as e:
            # No server available - just keep trying
            pass
        except Exception as e:
            logger.warning("Failed to connect to websocket: {} - {}".format(type(e), e))
        finally:
            sleep(1)

#------------------------------------------------------------
# global functions for script plugins

def script_load(settings):
    global hotkey_id_first
    global hotkey_id_prev
    global hotkey_id_next
    global hotkey_id_last
    global hotkey_id_black
    global hotkey_id_white
    global logger

    hotkey_id_first = register_and_load_hotkey(settings, HOTKEY_NAME_FIRST, HOTKEY_DESC_FIRST, first_slide)
    hotkey_id_prev = register_and_load_hotkey(settings, HOTKEY_NAME_PREV, HOTKEY_DESC_PREV, prev_slide)
    hotkey_id_next = register_and_load_hotkey(settings, HOTKEY_NAME_NEXT, HOTKEY_DESC_NEXT, next_slide)
    hotkey_id_last = register_and_load_hotkey(settings, HOTKEY_NAME_LAST, HOTKEY_DESC_LAST, last_slide)
    hotkey_id_black = register_and_load_hotkey(settings, HOTKEY_NAME_BLACK, HOTKEY_DESC_BLACK, black)
    hotkey_id_white = register_and_load_hotkey(settings, HOTKEY_NAME_WHITE, HOTKEY_DESC_WHITE, white)

    # Set up logging
    log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-7.7s]  %(message)s")
    logger = logging.getLogger("ppt_control_obs")
    logger.setLevel(LOG_LEVEL)
    logger.propagate = False
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(LOG_LEVEL)
    logger.addHandler(console_handler)

    ws_daemon = threading.Thread(name="ws_daemon", target=run_ws)
    ws_daemon.setDaemon(True)
    ws_daemon.start()
    logger.info("Started websocket client")

def script_unload():
    obs.obs_hotkey_unregister(first_slide)
    obs.obs_hotkey_unregister(prev_slide)
    obs.obs_hotkey_unregister(next_slide)
    obs.obs_hotkey_unregister(last_slide)
    obs.obs_hotkey_unregister(black)
    obs.obs_hotkey_unregister(white)

def script_save(settings):
    save_hotkey(settings, HOTKEY_NAME_FIRST, hotkey_id_first)
    save_hotkey(settings, HOTKEY_NAME_PREV, hotkey_id_prev)
    save_hotkey(settings, HOTKEY_NAME_NEXT, hotkey_id_next)
    save_hotkey(settings, HOTKEY_NAME_LAST, hotkey_id_last)
    save_hotkey(settings, HOTKEY_NAME_BLACK, hotkey_id_black)
    save_hotkey(settings, HOTKEY_NAME_WHITE, hotkey_id_white)

def script_description():
    return """ppt-control client

    Provides hotkeys for controlling PowerPoint slides using websockets.
    Go to OBS settings -> Hotkeys to change hotkeys (none set by default)."""

def script_defaults(settings):
    obs.obs_data_set_default_string(settings, 'hostname', HOSTNAME_DEFAULT)
    obs.obs_data_set_default_int(settings, 'port', PORT_DEFAULT)

def script_properties():
    props = obs.obs_properties_create()

    obs.obs_properties_add_text(props, "hostname", "Hostname: ", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_int(props, "port", "Port: ", 0, 9999, 1)
    return props

def script_update(settings):
    global port
    port = obs.obs_data_get_int(settings, "port")
    hostname = obs.obs_data_get_string(settings, "hostname")

def register_and_load_hotkey(settings, name, description, callback):
    hotkey_id = obs.obs_hotkey_register_frontend(name, description, callback)
    hotkey_save_array = obs.obs_data_get_array(settings, name)
    obs.obs_hotkey_load(hotkey_id, hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)

    return hotkey_id

def save_hotkey(settings, name, hotkey_id):
    hotkey_save_array = obs.obs_hotkey_save(hotkey_id)
    obs.obs_data_set_array(settings, name, hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)

#-------------------------------------

def first_slide(pressed):
    if pressed:
        global cmd
        cmd = "first"

def prev_slide(pressed):
    if pressed:
        global cmd
        cmd = "prev"

def next_slide(pressed):
    if pressed:
        global cmd
        cmd = "next"

def last_slide(pressed):
    if pressed:
        global cmd
        cmd = "last"

def black(pressed):
    if pressed:
        global cmd
        cmd = "black"

def white(pressed):
    if pressed:
        global cmd
        cmd = "white"
