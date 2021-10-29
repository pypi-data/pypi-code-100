#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import math
import subprocess
import logging
import re
import hashlib
import time
import json
from ffmpy import FFmpeg


# 时长转换：mode=1 => 100.201 转换为 00:01:40.201
def time_convert(duration, mode=1):
    M, H = 60, 60 ** 2
    if mode == 1:
        hour = math.floor(duration / H)
        mine = math.floor(duration % H / M)
        second = math.floor(duration % H % M)
        tim_srt = "%02d:%02d:%02d.%d" % (hour, mine, second, round(math.modf(duration)[0] * 1000))
        return tim_srt
    else:
        match = re.search(r'(\d+):(\d+):(\d+)(\.?\d*?)$', duration)
        # print(match.group())
        h = int(match.group(1))
        m = int(match.group(2))
        s = int(match.group(3))
        ms = round(float(match.group(4)), 3) if match.group(4) else 0
        t = (h * H + m * M + s) + ms
        # print(t)
        return t


def concatenate_videoclips():
    pass


class VideoFileClip(object):
    def __init__(self, path):
        setattr(__class__, 'clip', VideoClip(path))

    def __getattr__(self, attr):
        if not hasattr(__class__, attr):
            return getattr(self.clip, attr)
        else:
            return getattr(__class__, attr)

    def subclip(self, start=None, duration=None, save=None):
        clip = self.clip
        src = clip.path
        if type(start) == int or type(start) == float:
            start = time_convert(start)
        if not save:
            m = hashlib.md5()
            strs = "%s%s%s" % (start, duration, time.time())
            m.update(strs.encode("utf8"))
            filename = m.hexdigest() + '.mp4'
            save = os.path.join(os.path.dirname(src), filename)
        inputs = '-ss %s -t %s' % (start, duration) if duration else '-ss %s' % start
        ff = FFmpeg(inputs={src: inputs}
                    , outputs={save: "-c:v libx264 -c:a aac -strict experimental -b:a 98k -y "})
        logging.getLogger(__name__).debug(ff.cmd)
        ff.run()
        return VideoClip(save)


class VideoClip(object):
    def __init__(self, path):
        self.size = None
        self.w = None
        self.h = None
        self.bitrate = None
        self.fps = None
        self.duration = None
        self.rotate = None
        self.path = path
        self.__input_video()

    def __input_video(self):
        u"""
        获取视频信息
        """
        cmd = ['ffprobe', '-select_streams', 'v', '-show_streams', '-v', 'quiet', '-of', 'csv="p=0"', '-of', 'json',
               self.path]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode == 0:
            data = json.loads(out)
            # print(json.dumps(data))
            video = data['streams'][0]
            self.duration = float(video['duration'])
            # self.bitrate=video['bitrate']
            self.rotate = int(video['tags']['rotate']) if 'rotate' in video['tags'] else 0
            self.w = int(video['width'])
            self.h = int(video['height'])
            self.fps = int(video['r_frame_rate'].split('/')[0])
            self.size = (self.w, self.h)
            # print(self.__dict__)
        else:
            raise VideoException('ffprobe', err)


class VideoException(Exception):
    pass
