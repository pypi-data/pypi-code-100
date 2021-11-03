import json
import pdb
import logging
import traceback
import time
from enum import Enum
from typing import Union
from pi3dpf_ns.pi3dpf_common import pf_common as pfc

_log = logging.getLogger(__name__)

def safe_update(dict_obj: dict, key):
    """
    check if given key exists in dict_obj, returns it's value or None otherwise
    :param dict_obj: arbittrary dict
    :param key: key that might or might not be in dict_obj
    :return: value to key or None
    """
    return dict_obj[key] if key in dict_obj.keys() else None


def print_dict_two_columns(left, right, headers):
    left_str = ["None"] if left is None else ['"{}": "{}"'.format(k, v) for k, v in left.items()
                                              if k not in ['info_text']]
    right_str = ["None"] if right is None else ['"{}": "{}"'.format(k, v) for k, v in right.items()
                                                if k not in ['info_text']]
    try:
        left_max_len = max([0] + [len(i) for i in left_str])
        max_lines = max(len(left_str), len(right_str))
        format_string = "    {{:{}}}    {{}}".format(left_max_len)
        _log.info(format_string.format(headers[0], headers[1]))
        for i in range(0, max_lines):
            _log.info(format_string.format(
                "" if i >= len(left_str) else left_str[i],
                "" if i >= len(right_str) else right_str[i]))
    except ValueError:
        _log.warning("print_dict_two_columns - something went wrong. Traceback:\n{}".format(traceback.format_exc()))
        _log.info("print_dict_two_columns - left={}, right={}".format(left, right))


class DeviceState(Enum):
    idle = 'idle'
    active = 'active'
    uninitialized = 'uninitialized'

    def __repr__(self):
        return "{}.{}".format(self.__class__.__name__, self.value)


class DeviceClass(Enum):
    any = 'any'
    hw_device = 'hw_device'
    multi_room_music_group = 'multi_room_music_group'

    def __repr__(self):
        return "{}.{}".format(self.__class__.__name__, self.value)


class Skill:
    name = None
    logo_url = None


class Device:
    def __init__(self, devices, idx, PI3D_NOW_PLAYING_CHECK_IDLE_DEVICES):
        self.raw = devices[idx]
        # _log.info("init device {}".format(self.raw['accountName']))
        self.PI3D_NOW_PLAYING_CHECK_IDLE_DEVICES = PI3D_NOW_PLAYING_CHECK_IDLE_DEVICES
        self.accountName = self.raw['accountName']
        self.deviceAccountId = self.raw['deviceAccountId']
        self.deviceOwnerCustomerId = self.raw['deviceOwnerCustomerId']
        self.deviceFamily = self.raw['deviceFamily']
        self.serialNumber = self.raw['serialNumber']
        self.clusterMembers = self.raw['clusterMembers']
        self.parentClusters = self.raw['parentClusters']
        self.deviceType = self.raw['deviceType']
        self.deviceClass = DeviceClass.hw_device if len(self.serialNumber) == 16 else DeviceClass.multi_room_music_group
        self.device_volume_raw = None
        self.deviceState = DeviceState.idle
        self.state_volume = None
        self.state_muted = None
        self.untune_callable = None
        self.next_check = 0  # time.time() + self.PI3D_NOW_PLAYING_CHECK_IDLE_DEVICES
        self.now_playing = None
        self.queue_info = None
        self.song_title_last_played = None
        self.active_skill = None
        self.radio_station = None
        self.tunein_id = None
        self.radio_station_icy = None

    def __repr__(self):
        d = {"accountName": self.accountName,
             "deviceFamily": self.deviceFamily,
             "serialNumber": self.serialNumber,
             "clusterMembers": self.clusterMembers,
             "parentClusters": self.parentClusters,
             "deviceType": self.deviceType,
             "deviceClass": "{}".format(self.deviceClass),
             "deviceState": "{}".format(self.deviceState)
             }
        return "{}".format(json.dumps(d, indent=4))


class InfoText:
    def __init__(self, info_text: Union[dict, None]):
        self.info_text = info_text
        if info_text is None:
            return
        self.header = info_text['header']
        self.headerSubtext1 = info_text['headerSubtext1']
        self.multiLineMode = info_text['multiLineMode']
        self.subText1 = info_text['subText1']
        self.subText2 = info_text['subText2']
        self.title = info_text['title']

    def __repr__(self):
        if self.info_text is None:
            return ""
        d = {"header": self.header,
             "headerSubtext1": self.headerSubtext1,
             "multiLineMode": self.multiLineMode,
             "subText1": self.subText1,
             "subText2": self.subText2,
             "title": self.title}
        return "{}".format(json.dumps(d, indent=4))

    def __eq__(self, other):
        if self.info_text is None and other.info_text is None:
            return True
        if self.info_text is None or other.info_text is None:
            return False

        res = True
        if self.header != other.header:
            res = False
        if self.headerSubtext1 != other.headerSubtext1:
            res = False
        if self.multiLineMode != other.multiLineMode:
            res = False
        if self.subText1 != other.subText1:
            res = False
        if self.subText2 != other.subText2:
            res = False
        if self.title != other.title:
            res = False
        return res

    def __ne__(self, other):
        return not self.__eq__(other)


class Art:
    def __init__(self, art_text: dict):
        self.art_text = art_text
        if art_text is None:
            return
        try:
            self.altText = safe_update(art_text, "altText")
            self.artType = safe_update(art_text, "artType")
            self.contentType = safe_update(art_text, "contentType")
            self.url = safe_update(art_text, "url")
            self.iconId = safe_update(art_text, "iconId")
            self.iconStyles = safe_update(art_text, "iconStyles")
        except KeyError as ke:
            _log.info("key missing in art_text: \n{}".format(json.dumps(art_text, indent=4)))
            pdb.set_trace()

    def __repr__(self):
        if self.art_text is None:
            return ""
        d = {"altText": self.altText,
             "artType": self.artType,
             "contentType": self.contentType,
             "url": self.url,
             "iconId": self.iconId,
             "iconStyles": self.iconStyles}
        d = {k: v for k, v in d.items() if v is not None}
        return "{}".format(json.dumps(d, indent=4))


class Progress:
    def __init__(self, progress_text: Union[dict, None]):
        self.progress_text = progress_text
        if progress_text is None:
            self.mediaLength = 0
            self.mediaProgress = 0
            return
        self.allowScrubbing = progress_text["allowScrubbing"]
        self.locationInfo = progress_text["locationInfo"]
        self.mediaLength = progress_text["mediaLength"]
        self.mediaProgress = progress_text["mediaProgress"]
        self.showTiming = progress_text["showTiming"]
        self.visible = progress_text["visible"]

    def __repr__(self):
        if self.progress_text is None:
            return ""
        d = {"allowScrubbing": self.allowScrubbing,
             "locationInfo": self.locationInfo,
             "mediaLength": self.mediaLength,
             "mediaProgress": self.mediaProgress,
             "showTiming": self.showTiming,
             "visible": self.visible}
        return "{}".format(json.dumps(d, indent=4))


class Provider:
    def __init__(self, response_text):
        self.response_text = response_text
        if response_text is None:
            self.providerName = None
            self.providerLogo_url = None
            self.providerDisplayName = None
        else:
            self.providerName = response_text['providerName']
            if self.providerName in ['TuneIn Live Radio', 'TuneIn-Liveradio']:
                self.providerName = 'TuneIn'
            try:
                self.providerLogo_url = response_text['providerLogo']['url']
            except KeyError:
                self.providerLogo_url = None
            try:
                self.providerDisplayName = response_text['providerDisplayName']
            except KeyError:
                self.providerDisplayName = None

    def __repr__(self):
        print(json.dumps(self.response_text, indent=4))


class PlayerInfo:
    def __init__(self, response_text, echo_device: Device = None):
        self.response_text = response_text
        self.echo_device = echo_device
        raw = json.loads(self.response_text)
        if 'playerInfo' not in raw.keys():
            if 'message' in raw.keys():
                _log.info("[{}] received message '{}' instead of playerInfo".format(
                    self.echo_device.accountName, raw['message']))
            else:
                _log.info("playerInfo is not in expected form. Skipping processing")
                pdb.set_trace()
            self.raw = None
            self.progress = Progress(None)
            self.infoText = InfoText(None)
            return
        self.raw = raw['playerInfo']
        self.isPlayingInLemur = self.raw['isPlayingInLemur']
        self.lemurVolume = self.raw['lemurVolume']
        self.mediaId = self.raw['mediaId']
        self.state = self.raw['state']
        self.infoText = InfoText(self.raw['infoText'])
        self.mainArt = Art(self.raw['mainArt'])
        self.miniArt = Art(self.raw['miniArt'])
        self.cover_url_large = None
        self.progress = Progress(self.raw['progress'])
        # if echo_device.accountName == 'Kitchen':
        #     pdb.set_trace()
        self.provider = Provider(self.raw['provider'])


class QueueInfo:
    def __init__(self, response_text, echo_device):
        self.response_text = response_text
        raw = json.loads(self.response_text)
        if 'queueInfo' not in raw.keys():
            _log.info("queueInfo [{}] a) is not in expected form. Skipping processing".format(echo_device))
            self.raw = None
            self.infoText = InfoText(None)
            return
        self.raw = raw['queueInfo']
        media_list = self.raw['media']
        self.contentId = None
        self.displayText = None
        self.serviceName = None
        self.search_term = None
        self.affiliateTag = None
        self.url = None
        if media_list is None:
            _log.info("queueInfo [{}] b) is not in expected form. Skipping processing".format(echo_device))
            return
        action_indexes = [i for i in range(0, len(media_list)) if 'actions' in media_list[i].keys()]
        if action_indexes is None:  # or len(action_indexes) != 1:
            # last element is the newest
            _log.warning("QueueInfo - [{}] please check queueInfo number of elements: {}".format(
                         echo_device, action_indexes))
        else:
            idx = action_indexes[-1]  # could throw index error, but let's see
            _log.info("QueueInfo - [{}] len action_indexes={}, idx={}".format(echo_device, len(action_indexes), idx))
            # if echo_device == 'Kitchen':
            #     pdb.set_trace()
            self.url = media_list[idx]['art']['url'] if 'url' in media_list[idx]['art'].keys() else None
            idx_contentId = [i for i in range(0, len(media_list[idx]['actions'])) if 'contentId' in
                             media_list[idx]['actions'][i].keys()]
            if len(idx_contentId) != 1:
                _log.warning("QueueInfo - [{}] please check queueInfo, expected contentId: 1, actual: {}".format(
                    echo_device, idx_contentId))
            else:
                idx_2 = idx_contentId[0]
                self.contentId = media_list[idx]['actions'][idx_2]['contentId']
                self.displayText = media_list[idx]['actions'][idx_2]['displayText']
                self.serviceName = media_list[idx]['actions'][idx_2]['serviceName']
                try:
                    self.infoText = InfoText(media_list[idx]['infoText'])
                    self.miniArt = Art(media_list[idx]['art'])
                except:
                    pdb.set_trace()
                # self.mainArt = InfoText(media_list[idx]['mainArt'])
                # self.mainArt = Art(self.raw['mainArt'])
                # self.miniArt = Art(self.raw['miniArt'])

            idx_searchTerm = [i for i in range(0, len(media_list[idx]['actions'])) if 'searchTerm' in
                              media_list[idx]['actions'][i].keys()]
            if len(idx_searchTerm) != 1:
                _log.warning("QueueInfo - [{}] please check queueInfo, expected searchTerm: 1, actual: {}".format(
                    echo_device, idx_contentId))
            else:
                idx_3 = idx_searchTerm[0]
                self.search_term = media_list[idx]['actions'][idx_3]['searchTerm']
                self.affiliateTag = media_list[idx]['actions'][idx_3]['affiliateTag']

    # (Pdb) print(json.dumps(resp_json, indent=4))
# {
#     "queueInfo": {
#         "header": {
#             "actions": null,
#             "infoText": null,
#             "primaryAction": null,
#             "queueId": "dac87a97-de81-4e2a-afbd-e7205d887719"
#         },
#         "media": [
#             {
#                 "actions": [
#                     {
#                         "contentId": "s15474",
#                         "displayText": "Favorite station",
#                         "favorited": false,
#                         "mediaOwnerCustomerId": "A1V39U0JZHHL8O",
#                         "serviceName": "TUNE_IN",
#                         "type": "FavoriteContentAction"
#                     },
#                     {
#                         "affiliateTag": "radi0d-20",
#                         "searchTerm": "RTS Couleur 3",
#                         "searchTermType": "track",
#                         "type": "ShopMusicStoreByKeywordAction"
#                     }
#                 ],
#                 "art": {
#                     "altText": "Album Art",
#                     "artType": "UrlArtSource",
#                     "contentType": "image/*",
#                     "url": "https://cdn-radiotime-logos.tunein.com/s15474q.png"
#                 },
#                 "artOverlay": null,
#                 "index": 1,
#                 "infoText": {
#                     "header": null,
#                     "headerSubtext1": null,
#                     "multiLineMode": false,
#                     "subText1": null,
#                     "subText2": null,
#                     "title": "RTS Couleur 3"
#                 },
#                 "mediaId": "dac87a97-de81-4e2a-afbd-e7205d887719:1",
#                 "primaryAction": null
#             }
#         ],
#         "nextPageToken": null,
#         "previousPageToken": null,
#         "queueType": "SINGLETON_QUEUE"
#     }
# }



class Devices:
    def __init__(self, config):
        self.config = config
        self.response_text = None
        self.last_updated = None
        self.all_devices_amazon = []
        self.all_devices = []
        self.all_devices_active = []
        self.PI3D_NOW_PLAYING_CHECK_IDLE_DEVICES = pfc.get_config_param(
            self.config, 'PI3D_NOW_PLAYING_CHECK_IDLE_DEVICES')

    def load_from_response(self, response_text):
        if self.response_text == response_text:
            _log.info("no need to update device info")
        self.last_updated = time.time()
        self.response_text = response_text
        resp_list = json.loads(self.response_text)
        if 'devices' not in resp_list.keys():
            _log.error("device list in unexpected format, key 'devices' missing")
            exit(1)
        self.all_devices_amazon = resp_list['devices']
        for i in range(0, len(self.all_devices_amazon)):
            if self.all_devices_amazon[i]['accountName'] != 'This Device':
                self.all_devices.append(Device(self.all_devices_amazon, i, self.PI3D_NOW_PLAYING_CHECK_IDLE_DEVICES))

    def get_device_names(self, dev_class: DeviceClass = DeviceClass.any) -> [Device]:
        if dev_class == DeviceClass.any:
            return [self.all_devices[i].accountName for i in range(0, len(self.all_devices))]
        else:
            return [self.all_devices[i].accountName for i in range(0, len(self.all_devices))
                    if self.all_devices[i].deviceClass == dev_class]

    def get_device_ids(self, dev_class: DeviceClass = DeviceClass.any) -> [Device]:
        if dev_class == DeviceClass.any:
            return [self.all_devices[i].serialNumber for i in range(0, len(self.all_devices))]
        else:
            return [self.all_devices[i].serialNumber for i in range(0, len(self.all_devices))
                    if self.all_devices[i].deviceClass == dev_class]

    def get_device_details(self, dev_class: DeviceClass = DeviceClass.any) -> [Device]:
        if dev_class == DeviceClass.any:
            return self.all_devices
        else:
            return [self.all_devices[i] for i in range(0, len(self.all_devices))
                    if self.all_devices[i].deviceClass == dev_class]

    def get_device_by_id(self, device_serial_number) -> Device:
        ad = self.all_devices
        dl = [ad[i] for i in range(0, len(ad)) if ad[i].serialNumber == device_serial_number]
        return dl[0] if len(dl) == 1 else None

    def get_multigroup_members(self, mgm_group: Device) -> [Device]:
        dl = []
        for dev_id in mgm_group.clusterMembers:
            dl.append(self.get_device_by_id(dev_id))
        return dl

    def get_now_playing_payload(self, device_serial_number) -> {}:
        """
        Composing required parameter values for alexa request alexa.amazon.com/api/np/player
        :param device_serial_number: a echo device serial number, as string
        :return: returns a dict with required parameters to call alexa.amazon.com/api/np/player
        """
        ed = self.get_device_by_id(device_serial_number)
        params = {"deviceSerialNumber": ed.serialNumber, "deviceType": ed.deviceType}
        if ed.deviceClass != DeviceClass.multi_room_music_group and len(ed.parentClusters) > 0:
            params['lemurId'] = ed.parentClusters[0]
            params['lemurDeviceType'] = self.get_device_by_id(ed.parentClusters[0]).deviceType
        return params

    def update_volume_info(self, volume_details):
        vd = volume_details
        for e in self.all_devices:
            idx_list = [i for i in range(0, len(vd)) if vd[i]['dsn'] == e.serialNumber]
            if len(idx_list) != 1:
                _log.info("unexpected result. idx_list={} (should be list with one element)".format(idx_list))
                return
            i = idx_list[0]
            e.device_volume_raw = volume_details[i]
            try:
                volume_numeric = int(volume_details[i]['speakerVolume'])
            except:
                volume_numeric = 0
                _log.warning("update_volume_info - Exception. Traceback:\n{}".format(traceback.format_exc()))
            if volume_numeric > 0:
                e.state_volume = volume_details[i]['speakerVolume']
            else:
                _log.info("update_volume_info [{}] ignored current volume=0".format(e.accountName))
            e.state_muted = volume_details[i]['speakerMuted']
            _log.info("update_volume_info - speakerVolume={:<3}, speakerMuted={:5}, device=[{}]".format(
                'n/a' if e.state_volume is None else e.state_volume,
                'false' if e.state_muted == 0 else 'true', e.accountName))

    def update_device_now_playing(self, now_playing, echo_device: Device) -> bool:
        """
        Use this method to update the device objects 'now playing' information
        :param now_playing: response string from alexa.amazon.com/api/np/player
        :param echo_device: echo device to be examined
        :return: True when new sound was detected to be playing on given device, False otherwise
        """
        change_detected = False
        np = PlayerInfo(now_playing, echo_device)  # this will probably fail when device falls back to idle
        # todo: set device to idle when np.raw['mediaId'] == "BluetoothMediaId" is detected (device steaming BlueTooth)
        # if echo_device.accountName == 'Küche':
        #     pdb.set_trace()
        if echo_device.now_playing is None:
            _log.info("update_device_now_playing - [{}] - initializing".format(echo_device.accountName))
            change_detected = True
        # todo: handle device when stop playing.
        elif echo_device.now_playing.infoText != np.infoText:
            _log.info("update_device_now_playing - [{}] - change detected".format(
                echo_device.accountName))
            change_detected = True
        else:
            _log.info("update_device_now_playing - [{}] - no change".format(echo_device.accountName))

        if np.raw is not None:
            (co, case) = (change_detected, 'none')
            if np.mediaId == "BluetoothMediaId":  # device is in streaming bluetooth action, set to idle
                case = 'a'
            elif np.isPlayingInLemur and np.state in ['IDLE', 'PAUSED']:
                case = 'b'
            elif not np.isPlayingInLemur and np.state in [None]:
                case = 'c'
            elif not np.isPlayingInLemur and np.state == 'IDLE':
                # TuneIn keeps showing the last played song at times
                case = 'd'
            else:
                case = 'else'
            if case in ['a', 'b', 'c', 'd'] or (case == 'else' and np.state == 'PAUSED'):
                echo_device.deviceState = DeviceState.idle
                if echo_device.untune_callable is not None:
                    echo_device.untune_callable(echo_device)  # tune out if echo device is on TuneIn
                change_detected = False
            change = '' if co == change_detected else "{} -> {}".format(co, change_detected)
            change_txt = '' if change == '' else ", change_detected: {}".format(change)
            _log.info("update_device_now_playing - [{}] - case={}, isPlayingInLemur={}, state={}, mediaId={}{}".format(
                echo_device.accountName, case, np.isPlayingInLemur, np.state, np.mediaId, change_txt))

        # todo: check! this should probably go to Alexa.alexa_schedule_device_checks or better
        #       do in device initialization
        if echo_device.deviceState == DeviceState.idle:
            echo_device.next_check = time.time() + self.PI3D_NOW_PLAYING_CHECK_IDLE_DEVICES

        # echo_device.last_check = time.time()
        if change_detected:
            _log.info("update_device_now_playing - [{}] - change detected. progress_text={}".format(
                echo_device.accountName, np.progress.progress_text))
            #   todo: reset now_playing when device idle, like self.now_playing = None
            if np.progress.progress_text is None:
                echo_device.next_check = time.time() + self.PI3D_NOW_PLAYING_CHECK_IDLE_DEVICES
            elif np.progress.mediaLength == 0:
                echo_device.next_check = time.time() + self.PI3D_NOW_PLAYING_CHECK_IDLE_DEVICES
            else:
                remaining_duration = np.progress.mediaLength - np.progress.mediaProgress
                echo_device.next_check = time.time() + remaining_duration
            old = echo_device.now_playing
            if old is not None and old.infoText is not None and old.raw is not None:
                try:
                    echo_device.song_title_last_played = old.infoText.title
                    _log.info("[{}] - song_title_last_played updated to '{}'".format(
                        echo_device.accountName, old.infoText.title))
                except AttributeError:
                    # device just starts playing. no now playing information was ever stored and infoText is empty
                    pdb.set_trace()
            echo_device.now_playing = np
            echo_device.deviceState = DeviceState.active
            if np.infoText.info_text is not None:
                # self.infoText = InfoText(self.raw['infoText'])
                _log.info("[{}] changing now_playing".format(echo_device.accountName))
                echo_device.now_playing.infoText.subText1 = np.infoText.subText1
                echo_device.now_playing.infoText.subText2 = np.infoText.subText2
                echo_device.now_playing.infoText.title = np.infoText.title
            else:
                _log.info("update_device_now_playing - np.infoText.info_text is None")
            print_dict_two_columns(
                None if old is None else old.infoText.__dict__,
                None if np.infoText is None else np.infoText.__dict__, ["old:", "new:"])
        elif (echo_device.deviceState == DeviceState.active and np.raw is not None and
              np.progress.progress_text is not None and np.progress.mediaLength == 0):
            # TunIn often has mediaLength set to zero. Make sure we aren't in a mess
            next_check_old = echo_device.next_check
            echo_device.next_check = echo_device.next_check = time.time() + self.PI3D_NOW_PLAYING_CHECK_IDLE_DEVICES
            # pdb.set_trace()
            _log.info("update_device_now_playing - [{}] adjusting next_check from {} to {} as mediaLength is 0".format(
                echo_device.accountName, time.strftime('%H:%M:%S', time.localtime(next_check_old)),
                time.strftime('%H:%M:%S', time.localtime(echo_device.next_check))))
        return change_detected
