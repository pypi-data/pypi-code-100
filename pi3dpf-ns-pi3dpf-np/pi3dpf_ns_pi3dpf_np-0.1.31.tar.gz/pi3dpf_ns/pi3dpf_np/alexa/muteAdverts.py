import bdb
from collections import OrderedDict
import errno
import json
import logging
import os
import pdb
import posix
import re
import requests
import select
import threading
import time
import traceback
import typing

# from ..common import pf_common as pfc
from pi3dpf_ns.pi3dpf_common import pf_common as pfc
from .echo import DeviceClass
from .echo import Device
from .echo import Devices

_log = logging.getLogger(os.path.basename(__file__))


class MuteAdverts:
    def __init__(self, config, devices: Devices, session, customer_id):
        self.config = config
        self.devices = devices
        self.session = session
        self.customerId = customer_id
        self.PI3D_ALEXA_ACCOUNT_BASE_URL = pfc.get_config_param(self.config, 'PI3D_ALEXA_ACCOUNT_BASE_URL')
        self.PI3D_NOW_PLAYING_AD_LOOK_AHEAD = pfc.get_config_param(self.config, 'PI3D_NOW_PLAYING_AD_LOOK_AHEAD')
        self.fifo_action_list = ['save_volume', 'unmute_volume', 'mute_volume', 'stop']
        self.mute_ad_fifo_open_for_write = False
        self.mute_ad_fifo_name = "/var/tmp/fifo-mute-advertisements"
        self.mute_ad_fifo_handle_w = None
        self.mute_ad_fifo_handle_r = None
        # self.look_ahead_seconds = 10  # seconds to save time before song ends
        if os.path.exists(self.mute_ad_fifo_name):
            _log.warning("fifo {} already exists".format(self.mute_ad_fifo_name))
        else:
            os.mkfifo(self.mute_ad_fifo_name)
        self.actions = OrderedDict()
        self.mute_ad_thread = None
        self.stop_event = threading.Event()
        self.url_allvol = "{}/api/devices/deviceType/dsn/audio/v1/allDeviceVolumes".format(
            self.PI3D_ALEXA_ACCOUNT_BASE_URL)
        self.url_behaviour = "{}/api/behaviors/preview".format(self.PI3D_ALEXA_ACCOUNT_BASE_URL)

    def run(self):
        self.mute_ad_thread = threading.Thread(target=self.start, daemon=True)
        # stopping thread: https://stackoverflow.com/a/2564161
        # and nice description on how to do that properly: https://stackoverflow.com/a/325528
        self.mute_ad_thread.start()

    def start(self):
        _log.info("start - starting thread {}".format(self.__class__.__name__))
        self.fifo_open('read_block', 'start (thread)')
        while not self.stop_event.is_set():
            self.fifo_read()
            # _log.info("start - read message")
        _log.info("winding down {}".format(self.__class__.__name__))
        if os.path.exists(self.mute_ad_fifo_name):
            os.remove(self.mute_ad_fifo_name)

    def stop(self):
        self.stop_event.set()

    def echo_volume(self, action, echo_device: Device):
        _log.info("echo_volume [{}] action='{}'".format(echo_device.accountName, action))
        mrm = echo_device.deviceClass == DeviceClass.multi_room_music_group
        dl = self.devices.get_multigroup_members(echo_device) if mrm else [echo_device]
        if action == 'save_volume':
            cont_header = {'Content-Type': 'application/json; charset=UTF-8'}
            # _log.info("[{}] echo_volume - getting page '{}'".format(echo_device.accountName, self.url_allvol))
            resp = self.session.get(self.url_allvol, headers=cont_header)
            # Expected response:
            # [
            #       {
            #          "alertVolume":null,
            #          "deviceType":"A3C9PE6TNYLTCH",
            #          "dsn":"39f4fe60c4f944c49cb3ee9625e673a8",
            #          "error":null,
            #          "speakerMuted":false,
            #          "speakerVolume":16
            #       }
            # ]  # dsn has also form 'G0911W0793151RAG'
            volume_info = json.loads(resp.text)
            self.devices.update_volume_info(volume_info['volumes'])
            # _log.info("volume resp:\n{}".format(json.dumps(volume_info, indent=4)))
        elif action == 'unmute_volume':
            for e in dl:
                # _log.info("[{}] echo_volume - getting volume information".format(e.accountName))
                self.__set_volume__(e, e.state_volume)
        elif action == 'mute_volume':
            for e in dl:
                # _log.info("[{}] echo_volume - mute device".format(e.accountName))
                self.__set_volume__(e, 1) # if set to zero, my echo studio device sometimes goes to full volume instead
        else:
            _log.info("[{}] echo_volume - unexpected action '{}'".format(echo_device.accountName, action))

    def __set_volume__(self, echo_device, volume):
        if not isinstance(volume, int):
            _log.warning("__set_volume__ - [{}] ignoring volume='{}', need integer".format(
                echo_device.accountName, volume))
            return
        req_headers = {"Origin": self.PI3D_ALEXA_ACCOUNT_BASE_URL,
                       "Referer": "{}/spa/index.html".format(self.PI3D_ALEXA_ACCOUNT_BASE_URL),
                       "Content-Type": "application/json; charset=UTF-8"}
        #                "csrf": self.session.cookies['csrf']}  # moved to __csrf__
        json_struct = {"@type": "com.amazon.alexa.behaviors.model.Sequence",
                       "startNode": {"@type": "com.amazon.alexa.behaviors.model.OpaquePayloadOperationNode",
                                     "type": "Alexa.DeviceControls.Volume",
                                     "operationPayload": {"deviceType": echo_device.deviceType,
                                                          "deviceSerialNumber": echo_device.serialNumber,
                                                          "customerId": self.customerId,
                                                          "locale": "en-US",
                                                          "value": "{}".format(volume)}
                                     }
                       }
        if self.customerId is None:
            _log.warning("__set_volume__ - self.customerId must not be none for the next call to work")
        req_data = {"behaviorId": "PREVIEW", "sequenceJson": json.dumps(json_struct), "status": "ENABLED"}
        try:
            resp = self.session.post(self.url_behaviour, data=json.dumps(req_data), headers=req_headers)
        except ConnectionResetError:
            _log.warning("__set_volume__ - connection was reset")
            return
        tries, max_retry = 1, 3
        if resp.status_code != requests.codes.ok:
            _log.info("[{}] a) set_volume volume={} failed. http status {}. Message: '{}'. url:'{}'".format(
                echo_device.accountName, volume, resp.status_code, resp.text, resp.url))
            while tries <= max_retry and resp.status_code == 429:
                time.sleep(1 * tries)
                resp = self.session.post(self.url_behaviour, data=json.dumps(req_data), headers=req_headers)
                tries, ok = tries + 1, resp.status_code == requests.codes.ok
                txt = "succeeded" if ok else "failed. http status={}, Message: '{}'".format(resp.status_code, resp.text)
                _log.info("[{}] b) set_volume volume={} {}".format(echo_device.accountName, volume, txt))
        _log.info("[{}] set_volume - volume='{}' tries: {}, final status: {}".format(
            echo_device.accountName, volume, tries, resp.status_code))

    def fifo_open(self, mode, caller):
        # From: https://stackoverflow.com/a/34754523, non-blocking named pipe for writing and reading
        posix_mode, file_handle = None, None
        if mode == 'read_noblock':
            posix_mode = posix.O_RDONLY | posix.O_NONBLOCK
        elif mode == 'read_block':
            posix_mode = posix.O_RDONLY
        elif mode == 'write_noblock':
            posix_mode = posix.O_WRONLY | posix.O_NONBLOCK
        else:
            _log.error("fifo_open - action {} is not implemented".format(mode))
            exit(1)
        try:
            # self.mute_ad_fifo_handle_w = posix.open(self.mute_ad_fifo_name, posix_mode)
            file_handle = posix.open(self.mute_ad_fifo_name, posix_mode)
            if mode == 'write_noblock':
                self.mute_ad_fifo_open_for_write = True
                self.mute_ad_fifo_handle_w = file_handle
            else:
                self.mute_ad_fifo_handle_r = file_handle
        except OSError as ex:
            if ex.errno == errno.ENXIO:
                if caller == '__init__':
                    return None
            _log.error("fifo_open - caller='{}' - unable to open {}. Traceback:\n{}".format(
                caller, self.mute_ad_fifo_name, traceback.format_exc()))
            exit(1)
        return file_handle

    def fifo_write(self, action, ed_account_name, time_for_action):
        try:
            if not self.mute_ad_fifo_open_for_write:
                self.mute_ad_fifo_handle_w = self.fifo_open('write_noblock', 'fifo_write')
            if action not in self.fifo_action_list:
                _log.error("fifo_write - unexpected action '{}'. Use one of {}.".format(action, self.fifo_action_list))
                exit(1)
            msg = "Action: {} Echo-Device: {} Time-for-Action: {}\n".format(action, ed_account_name, time_for_action)
            posix.write(self.mute_ad_fifo_handle_w, msg.encode('utf-8'))
            # _log.info("fifo_write - sent message '{}'".format(msg))
        except OSError as ex:
            if ex.errno == errno.ENXIO:
                _log.info("fifo_write - unable writing to named pipe '{}'".format(self.mute_ad_fifo_name))

    def fifo_read(self):
        try:
            ak, timeout, to_silence, volume_save_time, echo_device = list(self.actions.keys()), 0, "", 0, None
            if len(ak) > 0:
                volume_save_time = ak[0] - self.PI3D_NOW_PLAYING_AD_LOOK_AHEAD
                timeout = volume_save_time - int(time.time())
                to_silence = self.actions[ak[0]]
            timeout = 0 if timeout < 0 else timeout
            # From: https://stackoverflow.com/a/21429655
            if timeout > 0:
                # _log.info("fifo_read - timeout={}s (until: {})".format(
                #     timeout, time.strftime('%H:%M:%S', time.localtime(time.time()+timeout))))
                rlist, _, _ = select.select([self.mute_ad_fifo_handle_r], [], [], timeout)
            else:
                # _log.info("fifo_read - waiting until next read")
                rlist, _, _ = select.select([self.mute_ad_fifo_handle_r], [], [])
            if self.mute_ad_fifo_handle_r in rlist:
                # we have something to read, so just do that
                resp = posix.read(self.mute_ad_fifo_handle_r, 10000)
            else:
                # read timed out, get scheduled action from self.actions and save all echo devices loudspeaker volumes
                if len(ak) > 0:
                    ml = max(len(e) for e in to_silence['ed'].keys())
                    _log.info("fifo_read - to_silence:\n{}".format(
                        "\n".join(["{1:{0}} - {2}".format(ml, k, to_silence['ed'][k]) for k in to_silence['ed'].keys()])))
                    echo_device = self.get_echo_device_from_account_name(list(to_silence['ed'].keys())[0])
                    f = "fifo_read - call: a) echo_volume(action='save_volume',echo_device={}) # executing now"
                    # _log.info(f.format(echo_device.accountName))
                    self.echo_volume('save_volume', echo_device)
                else:
                    _log.info("fifo_read - unsure of condition")
                return

            for line in resp.strip().decode('utf-8').split('\n'):
                # line = resp.decode('utf-8').strip()
                m = re.match("^Action: (.*) Echo-Device: (.*) Time-for-Action: (\d+\.\d+|immediate)", line)
                if not m:
                    _log.warning("fifo_read - lines format not as expected: '{}'. Input ignored".format(line))
                    return
                action, echo_device_account_name, time_for_action = m.group(1), m.group(2), m.group(3)
                time_for_action_str = time_for_action
                echo_device = self.get_echo_device_from_account_name(echo_device_account_name)
                if echo_device is None:
                    _log.warning("fifo_read - unable to find echo device '{}'. stopping".format(echo_device_account_name))
                    return
                ed = echo_device
                if time_for_action != 'immediate':
                    time_for_action = float(time_for_action)
                    time_for_action_str = time.strftime('%H:%M:%S', time.localtime(int(time_for_action)))
                _log.debug("fifo_read - Action: '{}' Echo-Device='{}' Time-for-Action: {}".format(
                    action, echo_device_account_name, time_for_action_str))
                if action == 'stop':
                    # give read above the chance to get out of infinite wait so thread can complete
                    return
                elif action in ['unmute_volume', 'mute_volume']:
                    _log.debug("fifo_read - call: x) echo_volume(action='{}',echo_device={})".format(action, ed.accountName))
                    self.echo_volume(action, echo_device)
                elif action == 'save_volume':
                    # not actually calling echo_volume(), just (re-)scheduling
                    self.schedule(echo_device, time_for_action)
                    if time.time() > volume_save_time + 2:
                        # _log.info("fifo_read - call: d) volume_save_time={} time.time()={}".format(
                        #     time.strftime('%H:%M:%S', time.localtime(int(volume_save_time))),
                        #     time.strftime('%H:%M:%S', time.localtime(time.time()))))
                        return  # no use processing save_volume requests from the past
                    f = "fifo_read - call: b) echo_volume(action='save_volume',echo_device={}) # queued to run at: {}"
                    # _log.info(f.format(ed.accountName, time.strftime('%H:%M:%S', time.localtime(int(volume_save_time)))))
                else:
                    _log.warning("fifo_read - call: unexpected action '{}'".format(action))
                    return
        except bdb.BdbQuit:
            _log.info("fifo_read - stopping")
        except:
            _log.info("fifo_read - exception! Traceback:\n{}".format(traceback.format_exc()))

    def schedule(self, echo_device: Device, time_for_action):
        k, al = int(time_for_action), self.actions
        if k in al.keys():
            al[k]['ed'][echo_device.accountName] = echo_device.active_skill
        else:
            al[k] = {"ed": {echo_device.accountName: echo_device.active_skill}, "state": "save-volume"}
        now, f = int(time.time()), "vol> song end: {} retrieve volume: {} Echo Devices: {}"
        for i in [i for i in al.keys() if i < now]:
            del(al[i])
        s = "\n".join(["vol> song end: {} retrieve volume: {} Echo Devices: {}".format(
            time.strftime('%H:%M:%S', time.localtime(i)),
            time.strftime('%H:%M:%S', time.localtime(i - self.PI3D_NOW_PLAYING_AD_LOOK_AHEAD)), al[i]['ed']) for i in al.keys()])
        _log.debug("schedule - next runs for loudspeaker volume saving:\n{}".format(s))

    def get_echo_device_from_account_name(self, echo_device_account_name):
        devices = [d for d in self.devices.all_devices if d.accountName == echo_device_account_name]
        if len(devices) > 1:
            _log.warning("fifo_read - found {} echo devices {} instead of one with accountName='{}'.".format(
                len(devices), devices, echo_device_account_name))
            _log.info("using first one")
            echo_device = devices[0]
        elif len(devices) == 0:
            _log.warning("fifo_read - found no echo devices with name '{}'.".format(echo_device_account_name))
            return None
        else:
            echo_device = devices[0]
        return echo_device