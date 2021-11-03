import base64
import bdb
import copy
import errno
import inspect
import json
import logging
import numpy as np
import os
import paho.mqtt.client as mqtt
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
import pdb
import posix
import re
from reportlab.graphics import renderPM
import requests
import shutil
import socket
import string
from svglib.svglib import svg2rlg
import threading
import time
import traceback
import urllib.error
from urllib.request import urlopen

# from ..common import pf_common as pfc
from pi3dpf_ns.pi3dpf_common import pf_common as pfc
_log = logging.getLogger(os.path.basename(__file__))


def add_transparency(pil_img: Image, rgb_code: list):
    # From: https://stackoverflow.com/a/54705555
    # Ensure pil_img it is 3-channel RGB and not 1-channel greyscale, not 4-channel RGBA, not 1-channel palette
    pil_img = pil_img.convert('RGB')
    if pil_img.size == (0, 0):
        _log.warning("image size 0x0 is not going to work")
    # Make into Numpy array of RGB and get dimensions
    rgb = np.array(pil_img)
    h, w = rgb.shape[:2]
    # Add an alpha channel, fully opaque (255)
    rgba = np.dstack((rgb, np.zeros((h, w), dtype=np.uint8)+255))
    # Make mask of black pixels - mask is True where image is black
    # mBlack = (RGBA[:, :, 0:3] == [0, 0, 0]).all(2)
    m_black = (rgba[:, :, 0:3] == rgb_code).all(2)
    # Make all pixels matched by mask into transparent ones
    rgba[m_black] = rgb_code + [0]  # results in 4 elements array
    # Convert Numpy array back to PIL Image and save
    return Image.fromarray(rgba)


class AlexaNowPlayingVisualize:

    def __init__(self, config):
        self.config = config
        self.NP_FT_FONT = pfc.get_config_param(self.config, 'NP_FT_FONT')
        self.PI3D_NOW_PLAYING_ALBUM_ART_SIZE = pfc.get_config_param(self.config, 'PI3D_NOW_PLAYING_ALBUM_ART_SIZE')
        self.PI3D_NOW_PLAYING_ALIGN = pfc.get_config_param(self.config, 'PI3D_NOW_PLAYING_ALIGN')
        self.PI3D_NOW_PLAYING_COLOR = pfc.get_config_param(self.config, 'PI3D_NOW_PLAYING_COLOR')
        self.PI3D_NOW_PLAYING_COLOR_BG = pfc.get_config_param(self.config, 'PI3D_NOW_PLAYING_COLOR_BG')
        self.PI3D_NOW_PLAYING_FONT_SIZE_PX = pfc.get_config_param(self.config, 'PI3D_NOW_PLAYING_FONT_SIZE_PX')
        self.PI3D_NOW_PLAYING_SKILL_DEFS = pfc.get_config_param(self.config, 'PI3D_NOW_PLAYING_SKILL_DEFS')
        self.PI3D_NOW_PLAYING_AD_TITLES = pfc.get_config_param(self.config, 'PI3D_NOW_PLAYING_AD_TITLES')
        self.PI3D_NOW_PLAYING_TOP_DIR = pfc.get_config_param(self.config, 'PI3D_NOW_PLAYING_TOP_DIR')
        # self.NP_FONT_COLOR = pfc.get_config_param(self.config, 'NP_FONT_COLOR')
        self.PI3D_NOW_PLAYING_BM = pfc.get_config_param(self.config, 'PI3D_NOW_PLAYING_BM')
        self.PI3D_NOW_PLAYING_MODE = pfc.get_config_param(self.config, 'PI3D_NOW_PLAYING_MODE')
        self.now_playing_file_name_tmp = os.path.join(os.path.splitext(self.PI3D_NOW_PLAYING_BM)[0]+'-tmp.png')
        self.nothing_playing = os.path.join(os.path.dirname(__file__), '..', 'common', 'cfg', 'icons',
                                            '1x1-transparent.png')
        self.last_height = os.path.join(os.path.dirname(__file__), 'cfg/icons/Pause_-_The_Noun_Project-white.png')
        self.img_txt_list = []
        self.img_pic_list = []
        self.img_dev_list = []
        self.songs = []
        self.font = ImageFont.truetype(self.NP_FT_FONT, round(self.PI3D_NOW_PLAYING_FONT_SIZE_PX * 72 / 96))
        self.font_3 = ImageFont.truetype(self.NP_FT_FONT, round(self.PI3D_NOW_PLAYING_FONT_SIZE_PX * 72 / 96 * 3))
        # self.pi3d_now_playing_color_bg = self.PI3D_NOW_PLAYING_COLOR_BG
        self.image_1px = Image.new("RGB", (1, 1), tuple(self.PI3D_NOW_PLAYING_COLOR_BG))
        self.draw = ImageDraw.Draw(self.image_1px)
        # self.PI3D_NOW_PLAYING_ALBUM_ART_SIZE = 170
        # self.PI3D_NOW_PLAYING_COLOR = 'white'
        self.font_col = (0, 0, 0) if self.PI3D_NOW_PLAYING_COLOR == 'black' else (255, 255, 255)
        self.endorsed_widths_pi3d = [4, 8, 16, 32, 48, 64, 72, 96, 128, 144, 192, 256, 288, 384, 512, 576, 640, 720,
                                     768, 800, 960, 1024, 1080, 1920]
        self.dim_3 = {'width_max': 0, 'height_max': 0, 'height_min': 10000, 'height_total': 0}
        self.dim_1 = {'width_max': 0, 'height_max': 0, 'height_min': 10000, 'height_total': 0}
        self.texts = []
        self.y_offsets_3 = []
        self.txt_widths = []  # used only when align='right'
        self.alexa_skill_configs = []
        self.alexa_skill_props = []
        self.formats = {}
        self.skills_to_profiles = {}
        self.skill_properties = {}
        self.get_skill_defs()
        self.np_viz_thread = None
        self.stop_event = threading.Event()
        self.album_thumb_path_broken = os.path.join(os.path.dirname(__file__), '..', 'common', 'cfg', 'icons',
                                             'Broken-image-389560-{}.png'.format(self.PI3D_NOW_PLAYING_COLOR))
        self.np_viz_fifo_name = "/var/tmp/fifo-now-playing-visualize"
        if os.path.exists(self.np_viz_fifo_name):
            _log.warning("fifo {} already exists".format(self.np_viz_fifo_name))
        else:
            os.mkfifo(self.np_viz_fifo_name)
        self.np_viz_fifo_fhandle = None
        self.playing_lists_now = {'alexa': {}, 'plex': {}, 'kodi': {}}
        self.playing_lists_old = {'alexa': {'x': 'bogus'}, 'plex': {'x': 'bogus'}, 'kodi': {'x': 'bogus'}}
        if self.PI3D_NOW_PLAYING_MODE in ['mqtt_distributor', 'mqtt_receiver']:
            self.MQTT_SERVER_NAME = pfc.get_config_param(self.config, 'MQTT_SERVER_NAME')
            self.MQTT_SERVER_PORT = pfc.get_config_param(self.config, 'MQTT_SERVER_PORT')
            self.MQTT_CLIENT_USERNAME = pfc.get_config_param(self.config, 'MQTT_CLIENT_USERNAME')
            self.MQTT_CLIENT_PASSWORD = pfc.get_config_param(self.config, 'MQTT_CLIENT_PASSWORD')
            if self.PI3D_NOW_PLAYING_MODE == 'mqtt_receiver':
                self.PI3D_NOW_PLAYING_RECEIVER_TOPIC = pfc.get_config_param(self.config, 'PI3D_NOW_PLAYING_RECEIVER_TOPIC')
                self.PI3D_NOW_PLAYING_RECEIVER_TOPIC += "_np/now_playing"
                self.np_topic = self.PI3D_NOW_PLAYING_RECEIVER_TOPIC
                if self.PI3D_NOW_PLAYING_MODE == 'not-configured':
                    _log.error("PI3D_NOW_PLAYING_RECEIVER_TOPIC not configured while in mqtt_receiver action")
                    exit(1)
            else:
                self.MQTT_TOPLEVEL_TOPIC = pfc.get_config_param(self.config, 'MQTT_TOPLEVEL_TOPIC')
                self.MQTT_TOPLEVEL_TOPIC += "_np"
                self.np_topic = "{}/now_playing".format(self.MQTT_TOPLEVEL_TOPIC)
            _log.info("__init__() - mqtt topic for 'now playing' info: '{}'".format(self.np_topic))
            self.client = mqtt.Client()
            self.client.username_pw_set(username=self.MQTT_CLIENT_USERNAME, password=self.MQTT_CLIENT_PASSWORD)
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.enable_logger()
            # prevent MQTT connect errors on system startup when network services (such as DNS) are not fully up and
            # running by attempting to connect to given IP:port socket and only continue when succeeding.
            connect_retry_count = 10
            while True:
                if isOpen(self.MQTT_SERVER_NAME, self.MQTT_SERVER_PORT):
                    break
                else:
                    _log.info("Alexa - Sleeping 5 seconds for '{}:{}' connection. {} retries left.".format(
                        self.MQTT_SERVER_NAME, self.MQTT_SERVER_PORT, connect_retry_count))
                    time.sleep(5)
                connect_retry_count -= 1
                if connect_retry_count <= 0:
                    _log.error("Alexa - failed to establish network connection to mqtt server at {}:{}".format(
                        self.MQTT_SERVER_NAME, self.MQTT_SERVER_PORT))
                    exit(1)
            self.client.connect(self.MQTT_SERVER_NAME, self.MQTT_SERVER_PORT, 60)
            # success message also in on_connect
            # _log.info("Alexa - successfully connected to mqtt server {}:{}".format(
            #     self.MQTT_SERVER_NAME, self.MQTT_SERVER_PORT))
            if self.PI3D_NOW_PLAYING_MODE == 'mqtt_distributor':
                _log.info("Alexa - calling (MQTT/paho) client.loop_start()")
                self.client.loop_start()


    def text_to_image(self, now_playing, align):
        # formats = self.formats
        self.img_txt_list = []
        self.img_pic_list = []
        self.img_dev_list = []
        self.songs = []
        for echo_device in now_playing.keys():
            _log.debug("text_to_image - echo device: '{}', skill: '{}'".format(
                echo_device, now_playing[echo_device]['skill']))
            # +------------------+-----------------------------+-----------------------------+
            # |                  |                             | Layout for Spotify, Deezer  |
            # | Layout for Plex: | Layout for TuneIn:          | and unknown Stations        |
            # +------------------+-----------------------------+-----------------------------+
            # | Song             | Artist - Song               | Song                        |
            # | Album            | Radio Station               | Artist                      |
            # | Artist | Plex    | echo device | Skill         | echo device | Skill         |
            # +------------------+-----------------------------+-----------------------------+
            recs = []
            sk, fm, sk2prof, ed = (None, None, "*", echo_device)
            try:
                sk, s2p = now_playing[echo_device]['skill'], self.skills_to_profiles
                idx = sk if sk in s2p.keys() else "*"
                sk2prof = s2p[idx]
                _log.debug("text_to_image - [{}] skill='{}', skills-to-profiles['{}']->'{}' formats['{}']->{}".format(
                    ed, sk, idx, sk2prof, sk2prof, self.formats[sk2prof]))
                fm = self.formats[sk2prof]
                for element in fm:
                    templ = string.Template(element)
                    recs.append(templ.safe_substitute(
                        {**now_playing[echo_device], **{"echo_device": echo_device, "hostname": os.uname()[1]}}))
                self.calc_dims(recs)
            except KeyError:
                f = "text_to_image - [{}] skill='{}', sk2prof='{}', fm: format='{}', KeyError. Traceback:\n{}"
                _log.warning(f.format(ed, sk, sk2prof, fm, traceback.format_exc()))
                return

            img_txt = Image.new('RGB', (self.dim_3['width_max'], self.dim_3['height_total']),
                                tuple(self.PI3D_NOW_PLAYING_COLOR_BG))
            draw = ImageDraw.Draw(img_txt)
            for i in range(0, len(self.texts)):
                pos_txt = (0, self.y_offsets_3[i]) if align == 'left' else \
                    (self.dim_3['width_max'] - self.txt_widths[i], self.y_offsets_3[i])
                draw.text(pos_txt, self.texts[i], self.font_col, font=self.font_3)
            img_txt = add_transparency(img_txt, self.PI3D_NOW_PLAYING_COLOR_BG)
            img_txt = img_txt.resize((self.dim_1['width_max'], self.dim_1['height_total']), Image.ANTIALIAS)
            if self.texts is not None:
                _log.debug("text_to_image - size for text '{}': {}px".format(
                    "\\n".join(self.texts), "x".join([str(s) for s in img_txt.size])))

            try_svg = False
            try:
                is_svg = re.search('.svg$', now_playing[echo_device]['img_url'], re.IGNORECASE)
                if is_svg and now_playing[echo_device]['img_url'][:4] == 'http':
                    fname_svg = "/var/tmp/{}".format(re.sub('[:/]+', '_', now_playing[echo_device]['img_url']))
                    fname_png = fname_svg.replace('.svg', '.png')
                    if not os.path.exists(fname_svg):
                        resp = requests.get(now_playing[echo_device]['img_url'])
                        with open(fname_svg, 'w') as f:
                            f.write(resp.text)
                    if not os.path.exists(fname_png):
                        # From: https://stackoverflow.com/a/59505217 - convert svg to png
                        drawing = svg2rlg(fname_svg)
                        img_pic = renderPM.drawToPILP(drawing)
                        img_pic.save(fname_png)
                    else:
                        img_pic = Image.open(fname_png)
                elif now_playing[echo_device]['img_url'][:4] == 'http':
                    img_pic = Image.open(urlopen(now_playing[echo_device]['img_url']))
                else:
                    img_pic = Image.open(now_playing[echo_device]['img_url'])
            except (FileNotFoundError, TypeError, urllib.error.HTTPError):
                # pdb.set_trace()
                _log.warning("text_to_image - '{}' not found".format(now_playing[echo_device]['img_url']))
                # album_thumb_path = os.path.join(os.path.dirname(__file__), '..', 'common', 'cfg', 'icons',
                #                                 'Broken-image-389560-{}.png'.format(self.PI3D_NOW_PLAYING_COLOR))
                _log.info("text_to_image - using '{}'".format(self.album_thumb_path_broken))
                img_pic = Image.open(self.album_thumb_path_broken)
            except UnidentifiedImageError:
                _log.warning("text_to_image - '{}' unable to process".format(now_playing[echo_device]['img_url']))

            # Ensure pil_img it is 3-channel RGB or 4-channel RGBA, but not 1-channel greyscale, not 1-channel palette
            img_pic = img_pic if img_pic.mode == 'RGBA' else img_pic.convert('RGB')
            img_pic = img_pic.resize((self.PI3D_NOW_PLAYING_ALBUM_ART_SIZE, self.PI3D_NOW_PLAYING_ALBUM_ART_SIZE))
            _log.debug("text_to_image - size for pict fragment: {}px".format("x".join([str(s) for s in img_pic.size])))

            self.img_txt_list.append(img_txt)
            self.img_pic_list.append(img_pic)
            self.img_dev_list.append(echo_device)
        self.generate_now_playing_bm(align)

    def generate_now_playing_bm(self, align):
        # now we need to compose the generated elements. For that, we need to know the maximal dimensions
        max_img_txt_width = 0
        img_txt_height = 0
        last_height = 0
        idx = 0
        y_pic_offsets = []
        y_txt_offsets = []
        x_txt_offsets = []  # used only when align='right'

        if len(self.img_txt_list) == 0:
            _log.info("generate_now_playing_bm - no songs playing. Getting {}".format(
                os.path.basename(self.nothing_playing)))
            shutil.copyfile(self.nothing_playing, self.PI3D_NOW_PLAYING_BM)
            return
        # _log.info("generate_now_playing_bm - concatenating {} elements".format(len(self.img_txt_list)))
        for i in self.img_txt_list:
            y_pic_offsets.append(last_height if len(y_pic_offsets) == 0 else y_pic_offsets[-1]+last_height)
            in_cell_offset = 0 if self.img_txt_list[idx].height >= self.PI3D_NOW_PLAYING_ALBUM_ART_SIZE else \
                self.PI3D_NOW_PLAYING_ALBUM_ART_SIZE - self.img_txt_list[idx].height
            y_txt_offsets.append(in_cell_offset if idx == 0 else
                                 in_cell_offset + idx * self.PI3D_NOW_PLAYING_ALBUM_ART_SIZE)
            max_img_txt_width = max(max_img_txt_width, i.size[0])
            if i.height <= self.PI3D_NOW_PLAYING_ALBUM_ART_SIZE:
                last_height = self.PI3D_NOW_PLAYING_ALBUM_ART_SIZE
                img_txt_height += self.PI3D_NOW_PLAYING_ALBUM_ART_SIZE
            else:
                f = "generate_now_playing_bm - height={}px in [{}] exceeds PI3D_NOW_PLAYING_ALBUM_ART_SIZE={}px."
                _log.info(f.format(i.height, idx, self.PI3D_NOW_PLAYING_ALBUM_ART_SIZE))
                last_height = i.height
                img_txt_height += i.height
            idx += 1

        # find the next image width known to work as pi3d Texture (without distortion)
        img_width = max_img_txt_width + self.PI3D_NOW_PLAYING_ALBUM_ART_SIZE
        endorsed_width = self.endorsed_widths_pi3d[-1]  # set to max size
        for s in self.endorsed_widths_pi3d:
            if s >= img_width:
                endorsed_width = s
                break

        for i in self.img_txt_list:
            x_txt_offsets.append(endorsed_width - self.PI3D_NOW_PLAYING_ALBUM_ART_SIZE - i.width)

        f = "generate_now_playing_bm - image size required: {}x{}px ({} rows)"
        _log.debug(f.format(endorsed_width, img_txt_height, len(self.img_txt_list)))
        image = Image.new('RGB', (endorsed_width, img_txt_height), tuple(self.PI3D_NOW_PLAYING_COLOR_BG))
        image = add_transparency(image, self.PI3D_NOW_PLAYING_COLOR_BG)
        for i in range(0, len(self.img_txt_list)):
            if align == 'left':
                pos_pic = (0, y_pic_offsets[i])
                pos_txt = (self.PI3D_NOW_PLAYING_ALBUM_ART_SIZE, y_txt_offsets[i])
            else:
                pos_pic = (endorsed_width - self.PI3D_NOW_PLAYING_ALBUM_ART_SIZE, y_pic_offsets[i])
                pos_txt = (x_txt_offsets[i], y_txt_offsets[i])
            image.paste(self.img_pic_list[i], pos_pic)
            image.paste(self.img_txt_list[i], pos_txt)
            _log.debug("generate_now_playing_bm - [{}]: size for thumbnail: {}x{}px".format(
                self.img_dev_list[i], self.img_pic_list[i].width, self.img_pic_list[i].height))

        image.save(self.now_playing_file_name_tmp)
        os.rename(self.now_playing_file_name_tmp, self.PI3D_NOW_PLAYING_BM)

    def calc_dims(self, args):
        self.dim_3 = {'width_max': 0, 'height_max': 0, 'height_min': 10000, 'height_total': 0}
        self.dim_1 = {'width_max': 0, 'height_max': 0, 'height_min': 10000, 'height_total': 0}
        self.texts = []
        self.y_offsets_3 = []
        self.txt_widths = []  # used only when align='right'
        k = 0
        for text in args:
            self.texts.append(text)
            if len(self.y_offsets_3) == 0:
                self.last_height = 0
            dim = [self.dim_3, self.dim_1]
            i = 0
            for font in self.font_3, self.font:
                size = self.draw.textsize(text, font)
                const_txt = "ABC" if k < len(args)-1 else "JgABC"
                width = self.draw.textsize(text, font)[0]
                height = self.draw.textsize(const_txt, font)[1]
                dim[i]['width_max'] = max(dim[i]['width_max'], width)  # size[0]
                dim[i]['height_max'] = max(dim[i]['height_max'], height)  # size[1]
                dim[i]['height_min'] = min(dim[i]['height_min'], height)  # size[1]
                dim[i]['height_total'] += height  # size[1]
                if font == self.font_3:
                    # _log.info("[{}]: {}x{}px".format(len(self.y_offsets_3), size[0], size[1]))
                    self.y_offsets_3.append(0 if len(self.y_offsets_3) == 0 else self.y_offsets_3[-1]+self.last_height)
                    self.last_height = height  # size[1]
                    self.txt_widths.append(width)  # size[0]
                i += 1
            k += 1

    def get_skill_defs(self):
        fnames, i, must_reload = (self.alexa_skill_configs, 0, False)
        # todo: extract file names from PI3D_NOW_PLAYING_SKILL_DEFS
        for f in self.PI3D_NOW_PLAYING_SKILL_DEFS:
        # for f in [os.path.join(os.path.dirname(__file__), '..', 'common', 'cfg', 'now-playing-skills.config'),
        #           '/home/pi/.pf/alexa/now-playing-skills.config']:
            if not os.path.exists(f):
                continue
            mdate, must_reload = (os.path.getmtime(f), False)
            if not [v['fname'] for v in fnames if v['fname'] == f]:
                # fnames[xx]['fname'] with filename 'f' does not exist. Always reload config files (for initialization)
                must_reload = True
                fnames.append({"fname": f, "mdate": mdate, "cfg_txt": "", "cfg": {}})
            elif mdate > fnames[i]['mdate']:
                # fname element exists but meanwhile the file was updated (according to mdate)
                must_reload = True
                fnames[i]['mdate'] = mdate
            if must_reload:
                _log.info("Alexa - get_skill_defs - mdate of '{}' causing config reload".format(f))
                try:
                    with open(fnames[i]['fname']) as af:
                        fnames[i]['cfg_txt'] = ""
                        for line in af:
                            fnames[i]['cfg_txt'] += line.partition('#')[0].rstrip()
                    fnames[i]['cfg'] = json.loads(fnames[i]['cfg_txt'])
                except json.decoder.JSONDecodeError as jsex:
                    _log.warning("Alexa - get_skill_defs - could not load definitions from '{}'. Traceback:\n{}".format(
                        f, traceback.format_exc()))
                    _log.info("exception 'JSONDecodeError' caused by offending config: {}".format(fnames[i]['cfg_txt']))
                    m = re.search('\(char (\d+)\)', jsex.args[0])
                    if m:
                        _log.info("Error '{}' caused by (offending char '{}' first):\n{}".format(
                            jsex.args[0], m.group(1), fnames[i]['cfg_txt'][int(m.group(1)):]))
                    pass
        if must_reload:  # merge 'cfg' part to one dict
            if len(fnames) == 1:
                if fnames[0]['cfg'] == {}:
                    _log.error("invalid Skill config in {}".format(fnames[0]['fname']))
                    exit(1)
                sp = fnames[0]['cfg']
            else:
                sp = {**fnames[0]['cfg'], **fnames[1]['cfg']}

            self.formats = sp['formats']
            self.skills_to_profiles = sp['skills-to-profiles']
            self.skill_properties = sp['skill-properties']
            _log.info("get_skill_defs - formats:\n{}".format(json.dumps(sp['formats'], indent=4)))
            _log.info("get_skill_defs - skills-to-profiles:\n{}".format(json.dumps(sp['skills-to-profiles'], indent=4)))
            _log.info("get_skill_defs - skill-properties:\n{}".format(json.dumps(sp['skill-properties'], indent=4)))

    def start(self):
        self.fifo_open('read_block')
        while not self.stop_event.is_set():
            self.fifo_read()
            time.sleep(1)
        _log.info("start - winding down {}".format(self.__class__.__name__))
        if os.path.exists(self.np_viz_fifo_name):
            os.remove(self.np_viz_fifo_name)

    def stop(self):
        self.stop_event.set()

    def stopped(self):
        return self.stop_event.is_set()

    def run(self):
        self.np_viz_thread = threading.Thread(target=self.start, daemon=True)
        # stopping thread: https://stackoverflow.com/a/2564161
        # and nice description on how to do that properly: https://stackoverflow.com/a/325528
        self.np_viz_thread.start()

    def fifo_open(self, mode):
        # From: https://stackoverflow.com/a/34754523, non-blocking named pipe for writing and reading
        rv = False
        posix_mode = None
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
            self.np_viz_fifo_fhandle = posix.open(self.np_viz_fifo_name, posix_mode)
            rv = True
        except OSError as ex:
            # if ex.errno == errno.ENXIO:
            pass
        return rv

    def fifo_write(self, sender, new_songs):
        try:
            posix.write(self.np_viz_fifo_fhandle, "From: {}, Data: {}\n".format(
                sender, json.dumps(new_songs)).encode('utf-8'))
        except OSError as ex:
            if ex.errno == errno.ENXIO:
                _log.info("fifo_write - unable writing to named pipe '{}'".format(self.np_viz_fifo_name))

    def fifo_read(self):
        try:
            resp = posix.read(self.np_viz_fifo_fhandle, 10000).decode('utf-8')
            for line in resp.strip().split('\n'):
                m = re.match("From: (.*), Data: (.*)", line)
                if not m:
                    _log.warning("fifo_read - line '{}' does not match expected pattern. Skipping.")
                    continue
                sender, now_playing_serial = m.group(1), m.group(2)
                self.playing_lists_now[sender] = json.loads(now_playing_serial)
                np = self.playing_lists_now[sender]
                _log.debug("fifo_read - From: '{}' - now_playing={}".format(sender, np))

            if self.playing_lists_old != self.playing_lists_now:
                np = {**self.playing_lists_now['alexa'], **self.playing_lists_now['plex']}
                for e in np.keys():
                    if np[e]['skill'] in self.skill_properties.keys():
                        reason, new_url = "z) other", self.skill_properties[np[e]['skill']]['logo_url']
                        if np[e]['song'] in self.PI3D_NOW_PLAYING_AD_TITLES:
                            # Advert, replace broken image with skill specific logo
                            reason = "a) Advertisement"
                        elif np[e]['img_url'] is None or np[e]['img_url'] == 'None':
                            # skill logo configured and no album art, so use the configured one
                            reason = "b) img_url=None"
                        if reason[:1] in ['a', 'b']:
                            f = "fifo_read - [{}] changing img_url from '{}' to '{}'. Reason: {}"
                            _log.info(f.format(e, np[e]['img_url'], new_url, reason))
                            np[e]['img_url'] = new_url
                    else:
                        _log.debug("fifo_read - skill '{}' (from np['{}]={}) not in {}".format(
                            np[e]['skill'], e, np[e], list(self.skill_properties.keys())))

                if self.PI3D_NOW_PLAYING_MODE == 'mqtt_distributor':
                    pl = self.playing_lists_now
                    now_playing = {**pl['alexa'], **pl['plex'], **pl['kodi']}
                    # convert Plex Album Art Thumb Nail to base64 and transmit to mqtt_receiver
                    for k in dict(filter(lambda key: key[0].startswith('Plex'), now_playing.items())).keys():
                        img_broken, img_check = self.album_thumb_path_broken, now_playing[k]['img_url']
                        img_ok = img_check if img_check is not None and os.path.exists(img_check) else img_broken
                        # if now_playing[k]['img_url'] is not None and os.path.exists(now_playing[k]['img_url']):
                        with open(img_ok, "rb") as f:
                            i, n = base64.b64encode(f.read()), os.path.basename(img_ok)
                            pay_load = json.dumps({"Plex-thumb": {"filename": n, "content": i.decode("utf-8")}})
                            self.client.publish(self.np_topic, pay_load)
                    _log.debug("fifo_read - publishing to {}: {}".format(
                        self.np_topic, json.dumps({"now_playing": now_playing})))
                    self.client.publish(self.np_topic, json.dumps({"now_playing": now_playing}))

                self.text_to_image(np, self.PI3D_NOW_PLAYING_ALIGN)
                self.playing_lists_old = copy.deepcopy(self.playing_lists_now)
        except bdb.BdbQuit:
            _log.info("stopping")
        except:
            _log.info("exception! Traceback:\n{}".format(traceback.format_exc()))

    def on_connect(self, client, userdata, flags, rc):
        while rc != 0:
            # meanings of rc in rc_to_text_on_connect
            _log.error("Connection failed with rc = {}. Reason: '{}'".format(rc, rc_to_text_on_connect(rc)))
            client.connect(self.MQTT_SERVER_NAME, self.MQTT_SERVER_PORT, 60)

        _log.info("Connection to MQTT broker '{}:{}' as user '{}' successful".format(
            self.MQTT_SERVER_NAME, self.MQTT_SERVER_PORT, self.MQTT_CLIENT_USERNAME))

        # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions
        # will be renewed.
        if self.PI3D_NOW_PLAYING_MODE == 'mqtt_receiver':
            client.subscribe(self.PI3D_NOW_PLAYING_RECEIVER_TOPIC)
            _log.info("Subscribing to '{}'. (Governed by PI3D_NOW_PLAYING_RECEIVER_TOPIC)".format(
                self.PI3D_NOW_PLAYING_RECEIVER_TOPIC))

    def on_message(self, client, userdata, msg):
        msg.payload = msg.payload.decode('UTF-8')
        payload = json.loads(msg.payload)
        if 'now_playing' in payload.keys():
            _log.info("on_message - processing MQTT now_playing message")
            _log.info("payload['now_playing']={}".format(json.dumps(payload['now_playing'], indent=4)))
            self.text_to_image(
                payload['now_playing'], self.PI3D_NOW_PLAYING_ALIGN)
        elif 'Plex-thumb' in payload.keys():
            filename = os.path.join(self.PI3D_NOW_PLAYING_TOP_DIR, 'plex-thumbs', payload['Plex-thumb']['filename'])
            _log.info("on_message - processing MQTT Plex-thumb message for file {}".format(filename))
            if not os.path.exists(filename):
                with open(filename, 'wb') as of:
                    of.write(base64.b64decode(payload['Plex-thumb']['content']))
        else:
            _log.info("on_message - ignoring MQTT message of type {}".format(payload.keys()))


def isOpen(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except Exception as e:
        _log.error(traceback.format_exc())
        return False


def rc_to_text_on_connect(rc):
    # Connection Return Codes:
    # 0: Connection successful
    # 1: Connection refused - incorrect protocol version
    # 2: Connection refused - invalid client identifier
    # 3: Connection refused - server unavailable
    # 4: Connection refused - bad username or password
    # 5: Connection refused - not authorised
    # 6-255: Currently unused.
    rc_texts = ['Connection successful',                           # rc = 0
                'Connection refused - incorrect protocol version', # rc = 1
                'Connection refused - invalid client identifier',  # rc = 2
                'Connection refused - server unavailable',         # rc = 3
                'Connection refused - bad username or password',   # rc = 4
                'Connection refused - not authorised']             # rc = 5
    rc_text = 'server return code rc={} is currently unused'.format(rc)
    if rc < len(rc_texts):
        rc_text = rc_texts[rc]

    return rc_text
