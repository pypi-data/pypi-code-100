# From: https://stackoverflow.com/a/62377243
import threading
import subprocess
import re
import os
import time
import logging
import json
# from logging.handlers import RotatingFileHandler
# from logging import Formatter
import traceback
import codecs
import pdb
# from ..alexa.echo import Device
# from ..alexa.echo import DeviceState
# from ..common import pf_common as pfc
from pi3dpf_ns.pi3dpf_np.alexa.echo import Device
from pi3dpf_ns.pi3dpf_np.alexa.echo import DeviceState
from pi3dpf_ns.pi3dpf_common import pf_common as pfc

# from pi3dpf_ns.pi3dpf_np.echo import Device


# todo:
#  - add __del__ method to tidy up on object destruction
#  - add logging
#  - filter out repeating messages
#  - compute streaming url from TuneIn information
#  - done replace non utf-8 characters with rectangle (0xE2 0x96 0xAF)
#  - handle mplayer failure properly
#  - redirect stderr to log file
#    Warning: Use communicate() rather than .stdin.write, .stdout.read or .stderr.read to avoid deadlocks due to any
#    of the other OS pipe buffers filling up and blocking the child process.
#  - make sure python option -u or PYTHONUNBUFFERED=?

_log = logging.getLogger(__name__)


class Announcement:

    repeater_fname = None

    @classmethod
    def update_repeater_fname(cls, np_home_dir):
        cls.repeater_fname = os.path.join(np_home_dir, 'alexa', 'icy-tags-repeaters.txt')

    def __init__(self, title, max_lifespan):
        self.title = title
        self.observed = 0
        self.expiry_date = time.time() + max_lifespan
        self.first_seen = time.time()
        self.last_seen = time.time()

    def update(self):
        self.last_seen = time.time()
        self.observed += 1


class LogWrapper:
    def __init__(self, station_name, station_id=None):
        self.station_name = station_name
        self.station_id = "{}:".format(station_id) if station_id is not None else ""
        self.log_prefix = " " + os.path.basename(__name__)
        self.log = logging.getLogger(__name__)

    def info(self, message, log_prefix=""):
        self.log.info("[{}{}]{} {}".format(self.station_id, self.station_name, log_prefix, message))

    def warning(self, message, log_prefix=""):
        self.log.warning("[{}{}] {} {}".format(self.station_id, self.station_name, log_prefix, message))

    def error(self, message, log_prefix=""):
        self.log.error("[{}{}] {} {}".format(self.station_id, self.station_name, log_prefix, message))


def tofu_king(exc):
    # print("hi there {}".format(reason))
    # Examples: https://stackoverflow.com/q/28423351 and
    #           https://www.programcreek.com/python/example/3643/codecs.register_error#169557
    # exc is an exception
    # exc.reason: description of error, e.g. 'invalid continuation byte'
    # exc.start: index to last good character. (start+1 is the offending one)
    # exc.end: index to the next good character
    #    -> exc.object[exc.start:exc.end] shows the offending character
    # exc.object: holds the failed string
    #
    tofu = u"\u25AF"
    new_char = tofu
    try:
        new_char = bytes(exc.object[exc.start:exc.end]).decode('latin-1')
        _log.info("tofu_king - successfully converted characters")
    except:
        _log.warning("tofu_king - decode('latin-1') was not successful. Traceback:\n{}".format(traceback.format_exc()))
        pass
    # pdb.set_trace()
    return new_char, int(exc.end)


codecs.register_error('tofu_king', tofu_king)


class IcyTags:
    # radio = None
    stream_text = None

    # plex_thread = None

    def __init__(self, station_name, station_url_list, cv: threading.Event, station_id=None):
        # logging.basicConfig(format='%(asctime)s %(levelname)s: [{}] %(message)s'.format(station_name))
        # formatter = Formatter(fmt='%(asctime)s %(levelname)s [{}]: %(message)s'.format(station_name))
        self.max_lifespan = 30 * 60  # entry should have a max life of 30 minutes
        self.next_housekeeping = time.time() + self.max_lifespan
        self.mlog = LogWrapper(station_name, station_id)
        self.now_playing_song_name = None
        self.now_playing_song_url = None
        self.station_name = station_name
        self.station_id = station_id
        self.station_url_list = station_url_list
        self.next_station_url_index = 0
        self.repeater_limit = 10
        self.icy_thread = None
        self.cv = cv
        self.stop_event = threading.Event()
        self.mplayer_phandle = None
        self.bitrate_detected = False
        self.mplayer_fifo_fname = "/var/tmp/fifo-{}-{}-{}".format(
            __name__, station_name.replace(" ", "."), os.getpid())
        if os.path.exists(self.mplayer_fifo_fname):
            self.mlog.info("fifo {} already exists".format(self.mplayer_fifo_fname))
        else:
            os.mkfifo(self.mplayer_fifo_fname)
        self.associated_echo_devices = {}
        self.announcements = {}  # Announcement()
        self.announcements_repeaters = {}
        self.bitrates = {k: [-1, 'kbit/s'] for k in station_url_list}  # initialize bitrates mplayer not always provides
        # From: https://stackoverflow.com/a/30546366
        # running mplayer without stdbuf causes delay in displaying new ICY messages of ~15s
        # make sure python is started with the '-u' option or PYTHONUNBUFFERED='x' (any non-empty value)
        #
        # slave action hints: http://www.mplayerhq.hu/DOCS/tech/slave.txt
        self.mplayer_opts = ['stdbuf', '-oL', '-eL', 'mplayer', '-slave', '-noidle', '-quiet', '-novideo', '-nolirc',
                             '-ao', 'null', '-prefer-ipv4', '-input', 'file={}'.format(self.mplayer_fifo_fname)]
        self.mlog.info("new mplayer instance started to monitor radio station '{}'".format(station_name))

    def repeater_tags_read(self):
        try:
            with open(Announcement.repeater_fname, 'r') as fh:
                for line in fh:
                    station_id, title = line.rstrip().split(':', 1)
                    if station_id == self.station_id and title not in self.announcements.keys():
                        self.announcements[title] = Announcement(title, self.max_lifespan)
                        self.announcements[title].first_seen = 0
                        self.announcements[title].observed = self.repeater_limit * 2
                        _log.info("repeater_tags_read - [{}:{}] restored icy_tag '{}'".format(
                            self.station_id, self.station_name, title))
        except FileNotFoundError:
            _log.info("repeater_tags_read - [{}:{}] file '{}' does not exist".format(
                self.station_id, self.station_name, Announcement.repeater_fname))

    def repeater_tags_write(self):
        with open(Announcement.repeater_fname, "a") as fh:
            rep, sid, sn = self.announcements_repeaters, self.station_id, self.station_name
            for k in rep.keys():
                # Announcement attributes: title, observed, expiry_date, first_seen, last_seen
                if rep[k].first_seen > 0 and rep[k].observed > self.repeater_limit:
                    _log.info("repeater_tags_write - [{}:{}] writing new repeater '{}'".format(sid, sn, rep[k].title))
                    fh.write("{}:{}\n".format(sid, rep[k].title))

    def write_fifo(self, message):
        if self.mplayer_phandle.poll() is None:
            mplayer_fifo_stream = open(self.mplayer_fifo_fname, mode='w')
            mplayer_fifo_stream.write(message)
            mplayer_fifo_stream.close()
        else:
            self.mlog.info("mplayer has already stopped. write would hang.")

    def must_publish(self, title):
        return_value = False
        if title not in self.announcements.keys():
            # first time we encounter given title
            self.mlog.info("New ICY tag '{}' detected".format(title))
            self.announcements[title] = Announcement(title, self.max_lifespan)
            self.now_playing_song_name = title
            try:
                self.cv.set()  # threading
            except:
                self.mlog.error("thread operation failed. Traceback:\n".format(traceback.format_exc()))
            return_value = True

        an = self.announcements
        an[title].observed += 1
        if an[title].observed == 1:
            self.mlog.info("all_titles:\n{}".format(self.print_announcements(an)))

            self.announcements_repeaters = {k: an[k] for k in an.keys() if an[k].title != title and
                   an[k].observed > self.repeater_limit}
            rep = self.announcements_repeaters
            self.mlog.info("repeater:{}".format("\n" + self.print_announcements(rep) if len(rep) > 0 else None))
            if self.next_housekeeping < time.time():
                self.mlog.info("sorted_by_first_seen:\n{}".format("\n".join(self.announcements)))
                # goner = [k for k in an.keys() if k not in rep.keys() and an[k].expiry_date < time.time()]
                goner = {k: an[k] for k in an.keys() if k not in rep.keys() and an[k].expiry_date < time.time()}
                for del_key in goner.keys():
                    del self.announcements[del_key]
                self.mlog.info("goner:{}".format("\n"+self.print_announcements(goner, 'goner') if len(goner) > 0 else None))
                self.next_housekeeping = self.max_lifespan + time.time()
        return return_value

    def print_announcements(self, announcements_dict, display_type='all-elements'):
        # try:
        an = announcements_dict
        s_ok, s_del = ("   ", "del") if display_type == 'goner' else ("", "")
        sorted_by_first_seen = \
            ["> {} {} {:3d} {}".format(s_del if an[k].expiry_date < time.time() else s_ok,
                                 time.strftime('%H:%M:%S', time.localtime(an[k].first_seen)), an[k].observed, k)
             for k in sorted(an, key=lambda e: an[e].first_seen)]
        return "\n".join(sorted_by_first_seen)
        # except:
        #     pdb.set_trace()
        #     _log.info("must investigate")

    def get_text(self):
        if self.stream_text:
            return self.stream_text
        return ""

    def stop(self):
        self.stop_event.set()
        self.write_fifo("quit\n")
        retries_left, stopped = 5, False
        while self.mplayer_phandle.poll() is None and retries_left > 0:
            self.mlog.info("waiting for mplayer to stop. retries_left: {}".format(retries_left))
            time.sleep(1)
            retries_left -= 1
        if self.mplayer_phandle.poll() is None:
            self.mlog.info("killing mplayer")
            self.mplayer_phandle.kill()
        if os.path.exists(self.mplayer_fifo_fname):
            os.remove(self.mplayer_fifo_fname)
        self.repeater_tags_write()

    def stopped(self):
        return self.stop_event.is_set()

    # def tunein_station_for_echo_device(self, station, action, echo_device: Device):
    #     permitted_actions = ['activate', 'deactivate']
    #     if action not in permitted_actions:
    #         _log.error("tunein_station_for_echo_device - invalid action '{}', must be one of {}".format(
    #             action, permitted_actions))
    #         exit(1)
    #     if echo_device.active_skill != 'TuneIn' and action == 'deactivate':
    #         return
    #     if action == 'deactivate':
    #         # todo: check if this echo device is the last one tuned into this radio station and only stop if so
    #         # todo: move icy_tags object from echo_device to alexa (more than one device can tune in to a radio station)
    #         echo_device.radio_station_icy.stop()
    #         echo_device.radio_station = None
    #         echo_device.active_skill = None
    #         echo_device.deviceState = DeviceState.idle
    #         if echo_device.accountName in self.associated_echo_devices.keys():
    #             del(self.associated_echo_devices[echo_device.accountName])
    #     else:
    #         self.associated_echo_devices[echo_device.accountName] = echo_device
    #         _log.info("tunein_station_for_echo_device - not yet implemented")

    def run(self):
        self.icy_thread = threading.Thread(target=self.start, daemon=True)
        # stopping thread: https://stackoverflow.com/a/2564161
        # and nice description on how to do that properly: https://stackoverflow.com/a/325528
        self.icy_thread.start()

    def mplayer_start(self) -> subprocess.Popen:
        mplayer_opts, selected_station_url, idx_info = self.mplayer_opts.copy(), None, ""
        known_br = [k for k in self.bitrates.keys() if int(self.bitrates[k][0]) > -1]
        if len(self.station_url_list) == len(known_br) and len(known_br) > 0:
            # bitrate for all urls are now known, we can select the one with the lowest bitrate to save bandwith
            min_rate = min([self.bitrates[i][0] for i in self.bitrates.keys()])
            url_list = [url for url in self.bitrates.keys() if self.bitrates[url][0] == min_rate]
            if len(url_list) > 1:
                self.mlog.info("mplayer - {} urls found with bandwidth {}, choosing 1st ({}) from {}".format(
                    len(url_list), min_rate, url_list[0], url_list))
            else:
                self.mlog.info("mplayer - choosing single url {} found with bandwidth {}".format(url_list[0], min_rate))
            selected_station_url = url_list[0]
        else:
            # we have not yet tried all provided urls. Keep looping and record bit rate so once we tried all urls,
            # we can choose the one with the lowest bandwidth
            idx = self.next_station_url_index
            idx_info = " # url idx: [{}]".format(idx)
            selected_station_url = self.station_url_list[idx]
            idx = idx + 1 if idx < len(self.station_url_list) - 1 else 0
            self.next_station_url_index = idx
        mplayer_opts.append(selected_station_url)
        self.mlog.info("starting subprocess using command '{}'{}".format(" ".join(mplayer_opts), idx_info))

        handle = subprocess.Popen(
            mplayer_opts, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0,
            universal_newlines=True, errors='tofu_king')
        if handle.poll() is not None:
            msg = handle.communicate()
            _log.error("mplayer failed with message '{}'".format(msg[0]))
            self.stop()
        return handle

    def start(self):
        try:
            self.bitrate_detected = False
            self.mplayer_phandle = self.mplayer_start()
            mplayer_start_time = time.time()
            while not self.stop_event.is_set() and self.mplayer_phandle.poll() is None:
                for line in self.mplayer_phandle.stdout:
                    if line.encode('utf-8').startswith(b'ICY Info:'):
                        info = line.split(':', 1)[1].strip()
                        attrs = dict(re.findall("(\w+)=['\"](.*)['\"]", info))
                        self.stream_text = attrs.get('StreamTitle', '(none)')
                        self.stream_text.strip()
                        if self.must_publish(self.stream_text):
                            self.mlog.info("looks like we have a new title: '{}'".format(self.stream_text))
                        if not self.bitrate_detected and mplayer_start_time + 4 < time.time():
                            self.write_fifo("get_audio_bitrate\n")
                    elif line.startswith("ANS_AUDIO_BITRATE="):
                        # ANS_AUDIO_BITRATE='128 kbps'
                        m = re.match("^ANS_AUDIO_BITRATE='(\d+) (.*?)'", line)
                        if m:
                            self.bitrates[self.mplayer_opts[-1]] = [m.group(1), m.group(2)]
                            self.bitrate_detected = True
                    elif line.startswith("Bitrate: "):  # re.match("^Bitrate: (\d+)(.*)", line):
                        # Bitrate: 96kbit/s
                        m = re.match("^Bitrate: (\d+)(.*)", line)
                        if m:
                            self.bitrates[self.mplayer_opts[-1]] = [m.group(1), m.group(2)]
                            self.bitrate_detected = True
                    self.mlog.info("mplayer: {}".format(line.strip()))
                self.mlog.info("mplayer - subprocess ended")
                if self.stop_event.is_set():
                    # shutdown requested, bail out
                    self.mlog.info("detected stop event, killing mplayer")
                    self.mplayer_phandle.kill()
                    break
                else:
                    # mplayer stopped, restart using different url
                    self.mlog.info("restarting mplayer")
                    self.mplayer_phandle = self.mplayer_start()
            self.mlog.info("mplayer - Stopping Thread")
        except:
            self.mlog.error("thread ended unexpectedly. Traceback:\n{}".format(traceback.format_exc()))
            # todo: handle termination
