# -*- coding: utf-8 -*-
# Created by restran on 2017/7/30
from __future__ import unicode_literals, absolute_import

import binascii
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import zipfile
from optparse import OptionParser

from PIL import Image
from mountains import force_text, text_type
from mountains import logging
from mountains.file import write_bytes_file
from mountains.logging import ColorStreamHandler, FileHandler

from .what_format import WhatFormat
from ..utils import find_ctf_flag, file_strings
from ..utils.converter import partial_base64_decode, hex2str, bin2str

parser = OptionParser()
parser.add_option("-f", "--file_name", dest="file_name", type="string",
                  help="read from file")
parser.add_option("-s", "--find_flag_strict_mode", dest="find_flag_strict_mode", default=False,
                  action="store_true", help="find ctf flag with strict mode")
parser.add_option("-p", "--enable_img_prepare", dest="enable_img_prepare", default=False,
                  action="store_true", help="enable image prepare, e.g. 去除PNG边缘重复像素")

"""
依赖 pngcheck、zsteg、stegdetect

自动检测文件可能的隐写，需要在Linux下使用 Python3 运行
一些依赖还需要手动安装
TODO:
FFD9 后的文件内容显示出来
"""

logging.init_log(ColorStreamHandler(logging.INFO, '%(message)s'),
                 FileHandler(level=logging.INFO))

logger = logging.getLogger(__name__)


class WhatSteg(object):
    def __init__(self, file_path, find_flag_strict_mode=True, enable_img_prepare=False):
        self.file_path = file_path
        self.enable_img_prepare = enable_img_prepare
        self.current_path = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        # 文件的扩展名
        self.file_ext = (os.path.splitext(base_name)[1]).lower()

        # 文件类型
        self.file_type = ''

        self.output_path = os.path.join(self.current_path, 'output_%s' % base_name)
        self.find_flag_strict_mode = find_flag_strict_mode
        # 需要强调输出的结果内容
        self.result_list = []

        self.extract_file_md5_dict = {}
        self.log_file_name = 'log.txt'
        self.file_img_size = None
        # 是否要跳过 zsteg 的处理，当bmp的图片高度被修改过，zsteg会卡住
        self.skip_zsteg = False

        # 删除旧的数据
        self.remove_dir(self.output_path)
        # 创建输出路径
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

        logging.init_log(ColorStreamHandler(logging.INFO, '%(message)s'),
                         FileHandler(filename=os.path.join(self.output_path, self.log_file_name),
                                     format='%(message)s', level=logging.DEBUG))

    def run_shell_cmd(self, cmd, log_line=False, log_max_line=20):
        try:
            (stdout, stderr) = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE, shell=True,
                                                universal_newlines=False).communicate()
            if stdout is None:
                stdout = b''
            if stderr is None:
                stderr = b''
            output = b'%s%s' % (stdout, stderr)
            output = force_text(output)
            output = text_type(output)
            if log_line is True:
                for line in output.splitlines()[:log_max_line]:
                    try:
                        logger.info(line)
                    except:
                        pass
            return output
        except Exception as e:
            logger.error(e)
            logger.error(cmd)
            logger.exception(e)
            return ''

    def strings(self):
        logger.info('\n--------------------')
        logger.info('run strings')
        out_file = os.path.join(self.output_path, 'strings_1.txt')
        cmd = 'strings %s > %s' % (self.file_path, out_file)
        self.run_shell_cmd(cmd)
        out_file = os.path.join(self.output_path, 'strings_2.txt')
        file_strings.file_2_printable_strings(self.file_path, out_file)

    def check_strings(self):
        file_path = os.path.join(self.output_path, 'strings_1.txt')
        with open(file_path, 'r') as f:
            string_data = f.read()

        if 'Adobe Fireworks' in string_data and self.file_type == 'png':
            self.result_list.append('[*] 很可能是 Fireworks 文件，请用 Fireworks 打开')
        if 'Adobe Photoshop' in string_data:
            self.result_list.append('[*] 可能存在 Photoshop 的 psd 文件，请检查是否有分离出 psd 文件')

    @classmethod
    def extract_file(cls, file_name, export_file_name, begin_hex_str, offset=0, end_hex_str=None):
        with open(file_name, 'rb') as f:
            data = f.read()
            hex_data = force_text(binascii.hexlify(data))

        begin_hex_str = begin_hex_str.replace(' ', '').strip()
        size = len(hex_data)
        begin_index = hex_data.index(begin_hex_str)
        end_index = size
        if end_hex_str is not None:
            end_index = hex_data.index(end_hex_str)

        if end_index < 0:
            end_index = size

        if begin_index < 0:
            return False
        else:
            try:
                begin_index += offset
                file_data = WhatFormat.extract_data(hex_data, begin_index, end_index)
                with open(export_file_name, 'wb') as f:
                    f.write(file_data)
                return True
            except Exception as e:
                logger.error(e)
                return False

    def check_png(self):
        if self.file_type == 'png':
            logger.info('\n--------------------')
            logger.info('run pngcheck')
            cmd = 'pngcheck -vv %s' % self.file_path
            stdout = self.run_shell_cmd(cmd)
            logger.info(stdout)
            if 'CRC error' in stdout:
                self.result_list.append('[*] PNG 文件 CRC 错误，请检查图片的大小是否有被修改')
                pattern = r'\(computed\s([0-9a-zA-Z]{8})\,\sexpected\s([0-9a-zA-Z]{8})\)'
                keywords = ['flag', 'synt']
                for line in stdout.splitlines():
                    r = re.search(pattern, line)
                    if not r:
                        continue

                    for t in r.groups():
                        try:
                            x = hex2str(t)
                            if x.lower() in keywords:
                                logger.warning('检测到 flag 特征数据，{} -> {}'.format(t, x))
                        except:
                            pass

            if 'additional data after IEND chunk' in stdout:
                png_end_hex_str = '00 00 00 00 49 45 4e 44 ae 42 60 82'
                logger.warning('[*] !!!注意!!! 文件末尾附加了数据，请检查PNG文件尾 {} 之后的数据'.format(png_end_hex_str))
                out_file_name = os.path.join(self.output_path, 'additional_data')
                png_end_hex_str = png_end_hex_str.replace(' ', '')
                result = self.extract_file(self.file_path, out_file_name, png_end_hex_str, offset=len(png_end_hex_str))
                if result is True:
                    logger.warning('提取文件末尾的数据成功 --> additional_data')
                else:
                    logger.error('提取文件末尾的数据失败')

            out_list = stdout.split('\n')
            last_length = None
            for t in out_list:
                t = t.strip()
                t = force_text(t)
                if t.startswith('chunk IDAT'):
                    try:
                        length = int(t.split(' ')[-1])
                        if last_length is not None and last_length < length:
                            self.result_list.append('[*] PNG 文件尾部可能附加了数据')
                            break
                        else:
                            last_length = length
                    except:
                        pass

    def check_gif(self):
        if self.file_type != 'gif':
            return

        logger.info('--------------------')
        logger.info('run check_gif')
        cmd = 'identify -format "%s %T \\n" {}'.format(self.file_path)
        try:
            output = self.run_shell_cmd(cmd)
            logger.info('GIF 帧时间输出结果')
            logger.info(output)
            self.save_special_text(output)
            lines = output.splitlines()
            lines = [t.split(' ')[1] for t in lines]
            set_lines = set(lines)
            if 2 <= len(set_lines) <= 100:
                logger.warning('GIF 帧时间可能存在隐写')
                logger.warning(' '.join(lines))
                # 猜测可能是01的布尔型数据
                if len(set_lines) == 3:
                    for i, t in enumerate(lines):
                        if t != lines[0]:
                            new_lines = ['0' if x == t else '1' for x in lines[i:]]
                            result = bin2str(''.join(new_lines))
                            logger.warning(result)
                            self.save_special_text(result)
                            break
                elif len(set_lines) == 2:
                    new_lines = ['0' if x == lines[0] else '1' for x in lines]
                    result = bin2str(''.join(new_lines))
                    logger.warning(result)
                    self.save_special_text(result)

        except:
            pass

    def check_img_height(self):
        """
        检测文件高度被修改过
        如果是修改宽度，会导致图片偏移而显示混乱
        windows忽略crc32检验码，png 可以直接修改任意高度，linux 会校验crc32，导致无法打开
        bmp 修改太高会导致文件打不开
        :return:
        """
        if self.file_type not in ('png', 'bmp', 'jpg'):
            return

        with open(self.file_path, 'rb') as f:
            data = f.read()

        w, h = self.file_img_size

        if self.file_type == 'png':
            bytes_data = data[12:33]
            crc32 = bytes_data[-4:]
            crc32 = struct.unpack('>i', crc32)[0]

            new_h = h * 2
            if binascii.crc32(bytes_data[:-4]) & 0xffffffff != crc32:
                logger.warning('[*] PNG图片宽高CRC32校验失败，文件宽高被修改过，或者文件末尾附加了数据')
                logger.warning('[*] 尝试爆破图片高度')
                new_h = h * 2
                for i in range(1, 65535):
                    height = struct.pack('>i', i)
                    check_data = bytes_data[:8] + height + bytes_data[-9:-4]
                    crc32_result = binascii.crc32(check_data) & 0xffffffff
                    if crc32_result == crc32:
                        logger.warning('[*] 找到正确的图片高度: %s' % i)
                        new_h = i
                        break
                else:
                    # linux 下，如果 png 图片高度改得太大，会无法打开，windows 下可以打开
                    logger.warning('[*] 未找到正确的图片高度，自动修改为2倍，请在Windows下打开')

            for x in range(4):
                height = struct.pack('>i', new_h)
                data = bytearray(data)
                data[20 + x] = height[x]
                data = bytes(data)

            logger.warning('[*] 保存修正高度后的文件: fix_height.png')
            out_path = os.path.join(self.output_path, 'fix_height.png')
            write_bytes_file(out_path, data)

        elif self.file_type == 'jpg':
            # im = Image.open(self.file_path)
            # # 获得图像尺寸:
            # w, h = im.size
            # print(w, h)
            x_img = struct.pack('>h', w)
            y_img = struct.pack('>h', h)
            begin = 0
            while True:
                x = data.find(y_img + x_img, begin)
                if x <= 0:
                    break

                bytes_data = data[x - 5:x + 5]
                sz_section = struct.unpack('>h', bytes_data[2:4])[0]
                nr_comp = struct.unpack('>b', bytes_data[-1:])[0]
                if sz_section - 8 != nr_comp * 3:
                    begin = x
                else:
                    # jpg可以任意增加高度，不会影响显示，至少让图片高度为1000以上
                    if h < 1000:
                        new_h = 1000
                    else:
                        new_h = new_h + 1000
                    new_height = struct.pack('>h', int(new_h))
                    for y_i in range(2):
                        data = bytearray(data)
                        data[x + y_i] = new_height[y_i]
                        data = bytes(data)

                    logger.warning('[*] 保存扩展高度后的文件: enlarge_height.jpg')
                    out_path = os.path.join(self.output_path, 'enlarge_height.jpg')
                    write_bytes_file(out_path, data)
                    break
        elif self.file_type == 'bmp':
            file_size = os.path.getsize(self.file_path)
            bit_count = data[28:30]
            # 1个像素占用多少字节，这个值一般是24或者32，bmp 图片使用小端序
            bit_count = struct.unpack('<h', bit_count)[0]
            if bit_count not in (24, 32):
                logger.warning('[*] 异常的 bmp bit count %s' % bit_count)
            real_height = int((file_size - 54) / (bit_count / 8) / w)

            if h != real_height:
                logger.warning('[*] 图片高度不正确，或者图片末尾附加了数据')
                logger.warning('[*] 正确的高度为: %s' % real_height)
                # bmp 图片使用小端序
                y_img = struct.pack('<i', real_height)
                for x in range(4):
                    data = bytearray(data)
                    data[22 + x] = y_img[x]
                    data = bytes(data)

                logger.warning('[*] 保存修正高度后的文件: fix_height.bmp')
                out_path = os.path.join(self.output_path, 'fix_height.bmp')
                logger.warning('[*] bmp的高度被修改，运行zsteg可能会耗时很久，已跳过')
                self.skip_zsteg = True
                write_bytes_file(out_path, data)

    def check_file(self):
        """
        检查文件真实类型
        :return:
        """
        logger.info('--------------------')
        logger.info('run file')
        cmd = 'file %s' % self.file_path
        stdout = self.run_shell_cmd(cmd)
        if 'PNG image data' in stdout:
            self.file_type = 'png'
        elif 'JPEG image data' in stdout:
            self.file_type = 'jpg'
        elif 'bitmap' in stdout:
            self.file_type = 'bmp'
        else:
            self.file_type = os.path.splitext(self.file_path)[1].lstrip('.')

        self.file_type = self.file_type.lower()

        if self.file_type in ('png', 'jpg', 'bmp'):
            try:
                im = Image.open(self.file_path)
                # 获得图像尺寸
                # w, h
                self.file_img_size = im.size
            except:
                self.file_img_size = None

        stdout = stdout.replace(self.file_path, '').strip()
        stdout = stdout[2:]
        self.result_list.append('[*] 文件类型: %s' % self.file_type)
        self.result_list.append('[*] 文件类型: %s' % stdout)

        file_size = os.path.getsize(self.file_path) / 1024.0
        self.result_list.append('[*] 文件大小: %.3fKB' % file_size)

    def parse_zsteg_output(slef, zsteg_output_file_name):
        """
        解析 zsteg 输出的结果，zsteg.txt进行解析，拆分成列表，每项是解析结果数据
        :param zsteg_output_file_name:
        :return:
        """
        steg_list = []
        with open(zsteg_output_file_name, 'r') as f:
            current = []
            line_count = 0
            for line in f:
                line_count += 1
                line = line.strip()
                if line == '':
                    steg_list.append({
                        'line_begin': line_count - len(current),
                        'data': current
                    })
                    current = []
                else:
                    current.append(line)

        new_steg_list = []
        for item in steg_list:
            line_data = item['data']
            line_begin = item['line_begin']
            for i, line in enumerate(line_data):
                if line.startswith('00000000: '):
                    if i >= 1:
                        begin_index = i - 1
                        line_begin = line_begin + begin_index
                        break
            else:
                begin_index = len(line_data) - 1
                line_begin = line_begin + begin_index

            if len(line_data) <= 0:
                continue
            line_data = line_data[begin_index:]
            new_steg_list.append({
                'line_begin': line_begin,
                'data': line_data
            })

        steg_list = []
        for item in new_steg_list:
            line_data = item['data']
            line_begin = item['line_begin']
            if '.. ' not in line_data[0]:
                continue

            try:
                steg_payload, file_type = line_data[0].split('.. ', 1)
                steg_payload = steg_payload.strip()
                file_type = file_type.strip()
            except Exception as e:
                print(e)
                continue

            new_item = {
                'steg_payload': steg_payload,
                'file_type': file_type,
                'line_begin': line_begin,
                'hex_data': []
            }

            for line in line_data[1:]:
                if line == '*':
                    new_item['hex_data'].append('*')
                elif line[8:10] == ': ':
                    hex_line = line[10:58]
                    hex_line = hex_line.split(' ')
                    hex_data = [t for t in hex_line if t != '']
                    new_item['hex_data'].extend(hex_data)
            new_item['hex_data'] = ''.join(new_item['hex_data'])
            if len(new_item['hex_data']) > 0 or file_type != '':
                steg_list.append(new_item)

        return steg_list

    def zsteg(self):
        """
        检测 png 和 bmp 的隐写
        :return:
        """
        if self.file_type not in ['bmp', 'png']:
            return

        if self.skip_zsteg:
            return

        logger.info('\n--------------------')
        logger.info('run zsteg')
        out_file = os.path.join(self.output_path, 'zsteg.txt')
        cmd = 'zsteg -a -v %s > %s' % (self.file_path, out_file)
        self.run_shell_cmd(cmd)

        file_list = [
            ['PC bitmap, Windows', 'bmp'],
            ['PNG image data', 'png'],
            ['JPEG image data', 'jpg'],
            ['GIF image data', 'gif'],
            ['Zip archive data', 'zip'],
            ['RAR archive data', 'rar'],
            ['gzip compressed data', 'gz'],
            ['7-zip archive data', '7z'],
            ['PDF document', 'pdf'],
            ['Python script', 'py'],
            ['python ', 'pyc'],
            ['tcpdump capture file', 'pcap'],
            ['pcap-ng capture file', 'pcapng'],
            ['PE32 executable ', 'exe'],
            ['PE64 executable ', 'exe'],
            ['ELF ', 'elf'],
        ]

        file_magic_hex_list = [
            ['ffd8ff', 'jpg']
        ]

        # 自动检测 zsteg 隐写是否有检测到隐藏文件
        out_path = os.path.join(self.output_path, 'zsteg')
        if not os.path.exists(out_path):
            os.makedirs(out_path)

        zsteg_text_list = []

        # 对于 zsteg 解析出来，识别成 text 的，需要根据16进制数据，找文件头特征，如果没有识别出文件的话
        def _check_file_magic(_steg_item):
            # 检测16进制数据，避免zsteg无法识别的情况
            for _file_magic in file_magic_hex_list:
                if _file_magic[0] in _steg_item['hex_data']:
                    _help_text = '{} 的特征数据{}，请查看文件的16进制数据'.format(_file_magic[1], _file_magic[0])
                    return True, _file_magic, _help_text

            return False, None, ''

        steg_list = self.parse_zsteg_output(out_file)
        for i, steg_item in enumerate(steg_list):
            steg_file_type = steg_item.get('file_type', '')
            steg_payload = steg_item.get('steg_payload', '')
            line_begin = steg_item['line_begin']

            should_extract = False
            extract_file_ext = None
            extract_help_text = ''
            # 记录所有的 text 数据
            if steg_file_type.startswith('text: '):
                # 凭经验设置的一个大概的值，zsteg 日志没有将所有的文本输出
                # 如果输出的内容比较长的情况下，就要考虑将文本文件提取出来
                if len(steg_file_type) <= 100:
                    result, file_magic, extract_help_text = _check_file_magic(steg_item)
                    if result is True:
                        should_extract = True
                        extract_file_ext = file_magic[1]
                    else:
                        continue
                else:
                    should_extract = True
                    extract_file_ext = 'txt'
                    zsteg_text_list.append('{} .. {}'.format(steg_payload, steg_file_type))
                    extract_help_text = steg_file_type
            else:
                for _, t in enumerate(file_list):
                    if ('file: ' + t[0]) not in steg_file_type:
                        continue
                    else:
                        should_extract = True
                        extract_file_ext = t[1]
                        extract_help_text = steg_file_type
                        break
                else:
                    result, file_magic, extract_help_text = _check_file_magic(steg_item)
                    if result is True:
                        should_extract = True
                        extract_file_ext = file_magic[1]

            # 检测到文件后，自动导出文件
            if should_extract and len(steg_payload.split(',')) > 0:
                f_name = '{}_{}.{}'.format(line_begin, i, extract_file_ext)
                out_file_path = os.path.join(out_path, f_name)
                cmd = "zsteg %s -E '%s' > %s" % (
                    self.file_path, steg_payload, out_file_path)

                logger.warning('[*] zsteg 检测到文件: {}'.format(extract_help_text))
                self.run_shell_cmd(cmd)

                msg = '[*] zsteg 日志第%d行检测到文件: %s' % (
                    line_begin, extract_help_text)
                self.result_list.append(msg)

        text_out_file = os.path.join(self.output_path, 'zsteg_text.txt')
        zsteg_parsed_json = os.path.join(self.output_path, 'zsteg.json')
        with open(zsteg_parsed_json, 'w') as f:
            f.write(json.dumps(steg_list, indent=2))

        with open(text_out_file, 'w') as f:
            for line in zsteg_text_list:
                f.write(line)
                f.write('\n')

                # 自动解码 base64 文本
                text = line[line.index('.. text: "') + len('.. text: "'):-1]
                b64rex = re.compile('^[A-Za-z0-9+/=]{4,}$')
                if b64rex.match(text):
                    text = file_strings.bytes_2_printable_strings(partial_base64_decode(text))
                    if len(text) > 5:
                        f.write('[base64_decode]: {}\n'.format(text))

    def stegdetect(self):
        """
        用于检测 jpg 的隐写
        :return:
        """
        if self.file_type == 'jpg':
            logger.info('\n--------------------')
            logger.info('run stegdetect')
            # -s 表示敏感度，太低了会检测不出来，太大了会误报
            cmd = 'stegdetect -n -s 5 %s' % self.file_path
            stdout = self.run_shell_cmd(cmd)
            logger.info(stdout)
            stdout = stdout.lower()
            if 'negative' not in stdout.lower():
                self.result_list.append('\n')

            if 'appended' in stdout:
                text = '[*] !!!注意!!! 图片后面可能附加了文件，文件类型为'
                self.result_list.append(text)
                begin_i = stdout.index('appended')
                self.result_list.append(stdout[begin_i:].strip())
                text = '请用 010Editor 打开，搜索 FFD9 并观察后面的数据'
                self.result_list.append(text)
                text = '若没有自动分离出文件，需要手动修复文件头'
                self.result_list.append(text)
            if 'jphide' in stdout:
                text = '[*] 使用了 jphide 隐写，如果没有提供密码，可以先用 Jphswin.exe 试一下空密码，再用 stegbreak 用弱口令爆破'
                self.result_list.append(text)
                text = '[*] 也有可能是 steghide 隐写，如果没有提供密码，可以用 steg_hide_break 用弱口令爆破'
                self.result_list.append(text)
                text = '[*] 也有可能是 outguess 隐写，outguess -r in.jpg out.txt'
                self.result_list.append(text)
                text = '    注意，jphide 的检测很可能会出现误报，可以尝试'
                self.result_list.append(text)
            if 'outguess' in stdout:
                text = '[*] 使用了 outguess 隐写'
                self.result_list.append(text)
            if 'f5' in stdout:
                text = '[*] 使用了 F5 隐写'
                self.result_list.append(text)
            if 'jsteg' in stdout:
                text = '[*] 使用了 jsteg  隐写'
                self.result_list.append(text)
            if 'invisible secrets' in stdout:
                text = '[*] 使用了 invisible secrets 隐写'
                self.result_list.append(text)

    @classmethod
    def check_file_md5(cls, file_path):
        with open(file_path, 'rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()
            return md5

    def unzip(self, file_path, destination_path):
        tmp_file_path = file_path.replace(self.current_path, '')
        try:
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                try:
                    zip_ref.extractall(destination_path)
                    return True
                except Exception as e:
                    if 'password required' in e:
                        logger.info('压缩包 %s 需要密码' % tmp_file_path)
                    else:
                        logger.info('压缩包 %s 解压失败' % tmp_file_path)
                    return False
        except Exception as e:
            logger.info('压缩包 %s 解压失败' % tmp_file_path)
            return False

    def unzip_archive(self):
        for root, dirs, files in os.walk(self.output_path):
            for f_name in files:
                path = os.path.join(root, f_name)
                if path.endswith('.zip'):
                    zip_path = path + '_unzip'
                    self.unzip(path, zip_path)

    def check_extracted_file(self):
        # 排除这些文件
        exclude_file_list = [
            'foremost/audit.txt',
            'strings_1.txt',
            'strings_2.txt',
            'zsteg.txt',
            'zsteg.json',
            'zsteg_text.txt',
            'log.txt',
            'special_text.txt',
            'prepared_img.{}'.format(self.file_type),
            'enlarge_height.{}'.format(self.file_type),
            'fix_height.{}'.format(self.file_type),
            'additional_data'
        ]
        exclude_file_list = [
            os.path.join(self.output_path, t)
            for t in exclude_file_list
        ]
        self.extract_file_md5_dict = {}
        file_type_dict = {}

        # 解压出压缩包
        self.unzip_archive()

        for root, dirs, files in os.walk(self.output_path):
            for f_name in files:
                path = os.path.join(root, f_name)
                if path in exclude_file_list:
                    continue

                # 删除大小为空的文件
                file_size = os.path.getsize(path)
                if file_size <= 0:
                    os.remove(path)
                    continue

                md5 = self.check_file_md5(path)
                file_ext = os.path.splitext(path)[1].lower()
                if file_ext != '':
                    # 去掉前面的.
                    file_ext = file_ext[1:]

                if md5 in self.extract_file_md5_dict:
                    old_file = self.extract_file_md5_dict[md5]
                    # 如果是有扩展名的，则替换没有扩展名的
                    if file_ext == '' or old_file['ext'] != '':
                        continue

                self.extract_file_md5_dict[md5] = {
                    'path': path,
                    'ext': file_ext
                }

        for k, v in self.extract_file_md5_dict.items():
            if v['ext'] in file_type_dict:
                item = file_type_dict[v['ext']]
                item.append(v['path'])
            else:
                file_type_dict[v['ext']] = [v['path']]

        total_num = len(self.extract_file_md5_dict.keys())
        self.result_list.append('\n')
        self.result_list.append('[+] 分离出的文件数: %s' % total_num)
        has_zip = False
        # 把所有不重复的文件，按文件类型重新存储
        for file_type, v in file_type_dict.items():
            if file_type == '':
                file_type = 'unknown'

            path = os.path.join(self.output_path, file_type)
            if not os.path.exists(path):
                os.mkdir(path)

            self.result_list.append('[+] %s: %s' % (file_type, len(v)))
            file_name_dict = {}
            for i, f_p in enumerate(v):
                # 默认使用分离文件时的文件名，如果出现冲突，再用数字
                base_name = os.path.basename(f_p)
                if base_name not in file_name_dict:
                    f_name = base_name
                    file_name_dict[f_name] = None
                else:
                    if file_type != 'unknown':
                        f_name = '%s.%s' % (i, file_type)
                    else:
                        f_name = '%s' % i

                p = os.path.join(path, f_name)
                try:
                    # 移动文件
                    shutil.move(f_p, p)
                except Exception as e:
                    logger.error(e)
                file_size = os.path.getsize(p) / 1024.0
                self.result_list.append('    %s: %.3fKB' % (i, file_size))

            if file_type == 'zip':
                has_zip = True

        # 自动删除这些文件夹
        path = os.path.join(self.output_path, 'foremost')
        self.remove_dir(path)
        path = os.path.join(self.output_path, 'what_format')
        self.remove_dir(path)
        path = os.path.join(self.output_path, 'binwalk')
        self.remove_dir(path)
        path = os.path.join(self.output_path, 'zsteg')
        self.remove_dir(path)

        if has_zip:
            self.result_list.append('[!] 如果 zip 文件打开后有很多 xml，很可能是 docx')

    @classmethod
    def remove_dir(cls, dir_path):
        try:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path, ignore_errors=True)
        except:
            pass

    def binwalk(self):
        logger.info('\n--------------------')
        logger.info('run binwalk')
        out_path = os.path.join(self.output_path, 'binwalk')
        self.remove_dir(out_path)
        # binwalk 会自动对 zlib 文件解压缩，可以进一步对解压缩后的文件类型进行识别
        cmd = 'binwalk -v -M -e -C %s %s' % (out_path, self.file_path)
        stdout = self.run_shell_cmd(cmd)
        # 不要输出那么多
        logger.info('\n'.join(stdout.splitlines()[:20]))
        self.process_binwalk_unknown(out_path)

    def process_binwalk_unknown(self, binwalk_path):
        logger.info('\n--------------------')
        logger.info('process binwalk unknown files')
        for root, dirs, files in os.walk(binwalk_path):
            for f_name in files:
                path = os.path.join(root, f_name)
                file_ext = os.path.splitext(path)[1].lower()
                if file_ext == '':
                    out_path = os.path.join(root, 'out_' + f_name)
                    cmd = 'what_format -f %s -o %s -e bmp -e gif -e pdf' % (path, out_path)
                    self.run_shell_cmd(cmd, log_line=True)
                    logger.info(out_path)

    def foremost(self):
        logger.info('\n--------------------')
        logger.info('run foremost')
        out_path = os.path.join(self.output_path, 'foremost')
        self.remove_dir(out_path)
        cmd = 'foremost -o %s %s' % (out_path, self.file_path)
        self.run_shell_cmd(cmd, log_line=True)

    def what_format(self):
        logger.info('\n--------------------')
        logger.info('run what_format')
        out_path = os.path.join(self.output_path, 'what_format')
        self.remove_dir(out_path)
        cmd = 'what_format -f %s -o %s -e bmp -e gif -e pdf' % (self.file_path, out_path)
        self.run_shell_cmd(cmd, log_line=True)

    def run_exif_tool(self):
        if self.file_type not in ['bmp', 'png', 'jpg', 'jpeg', 'gif']:
            return

        logger.info('\n--------------------')
        logger.info('run exiftool')
        # -j 将结果输出为json格式
        cmd = 'exiftool -j %s' % self.file_path
        stdout = self.run_shell_cmd(cmd)

        try:
            json_data = json.loads(stdout)
            if len(json_data) > 0:
                json_data = json_data[0]

            keywords = {
                'Description', 'Title', 'Subject', 'LastKeywordXMP',
                'XPSubject', 'XPKeywords', 'XPComment', 'XPTitle', 'ImageDescription'
            }
            # 检测 exif 中是否有隐藏数据
            exif_not_empty = False
            for key, value in json_data.items():
                if key in keywords and value not in (None, ''):
                    logger.warning('{}: {}'.format(key, value))
                    exif_not_empty = True
                else:
                    logger.info('{}: {}'.format(key, value))

            if exif_not_empty:
                logger.warning('[*] Exif 信息存在数据，请在 Windows 下查看图片的 Exif 信息')

            if self.file_img_size is None:
                self.file_img_size = (json_data['ImageWidth'], json_data['ImageHeight'])
        except:
            logger.info(stdout)

    def image_prepare(self):
        """
        对图片做一些预处理操作，例如PNG图片的颜色(RGBA)有大片都是一样的，可以去除
        :return:
        """
        if not self.enable_img_prepare:
            return

        logger.info('--------------------')
        logger.info('run image_prepare')

        if self.file_type == 'png':
            try:
                im = Image.open(self.file_path)
                im = im.convert('RGBA')
                w, h = im.size
                if w <= 20 or h <= 20:
                    return

                last_rgba = im.getpixel((0, 0))
                begin_i = 0
                for i in range(w):
                    for j in range(h):
                        pix = (i, j)
                        r, g, b, a = im.getpixel(pix)
                        if last_rgba != (r, g, b, a):
                            break
                    else:
                        begin_i = i
                        continue

                    break

                last_rgba = im.getpixel((w - 1, 0))
                end_i = w - 1
                for i in range(w - 1, -1, -1):
                    for j in range(h):
                        pix = (i, j)
                        r, g, b, a = im.getpixel(pix)
                        if last_rgba != (r, g, b, a):
                            break
                    else:
                        end_i = i
                        continue

                    break

                if begin_i > end_i:
                    # error
                    return

                begin_i += 1
                begin_j = 0
                last_rgba = im.getpixel((begin_i, 0))

                for j in range(h):
                    for i in range(begin_i, end_i + 1):
                        pix = (i, j)
                        r, g, b, a = im.getpixel(pix)
                        if last_rgba != (r, g, b, a):
                            break
                    else:
                        begin_j = j
                        continue

                    break

                end_j = h - 1
                last_rgba = im.getpixel((begin_i, h - 1))
                for j in range(h - 1, -1, -1):
                    for i in range(begin_i, end_i + 1):
                        pix = (i, j)
                        r, g, b, a = im.getpixel(pix)
                        if last_rgba != (r, g, b, a):
                            break
                    else:
                        end_j = j
                        continue

                    break

                if begin_j > end_j:
                    # error
                    return

                begin_j += 1
                logger.info('去除PNG重复像素')
                logger.info('w: {}->{}'.format(begin_i, end_i))
                logger.info('h: {}->{}'.format(begin_j, end_j))
                croped_im = im.crop((begin_i, begin_j, end_i, end_j))
                new_file_path = os.path.join(self.output_path, 'prepared_img.{}'.format(self.file_type))
                croped_im.save(new_file_path)
                logger.info('后续处理文件更新为: prepared_img.{}'.format(self.file_type))
                self.file_path = new_file_path
            except:
                return

    def check_abnormal_file_magic(self):
        """
        检查一些异常的文件头，例如将 Rar! 改成 raR!
        :return:
        """
        logger.info('\n--------------------')
        file_path = os.path.join(self.output_path, 'strings_1.txt')
        with open(file_path, 'r') as f:
            data = f.read()

        magic_dict = {
            'RAR!': 'rar',
            'PK': 'zip',
            'PNG': 'png',
            'JFIF': 'jpg'
        }

        re_list = [
            (r'({})'.format('|'.join(magic_dict)), re.I),
        ]

        result_dict = {}
        for r, option in re_list:
            if option is not None:
                pattern = re.compile(r, option)
            else:
                pattern = re.compile(r)

            ret = pattern.findall(data)
            if len(ret) > 0:
                ret = set([t.upper() for t in ret])
                for t in ret:
                    t = magic_dict.get(t, t)
                    if t not in result_dict:
                        result_dict[t] = None

        file_list = [t.lower() for t in result_dict.keys() if t.lower() != self.file_type]
        if len(file_list) > 0:
            logger.warning('[*] 文件中可能存在（误报率较高，仅参考）： {}'.format(', '.join(file_list)))
            logger.warning('[*] 请检查文件尾是否有附加数据')

    def save_special_text(self, text):
        special_text_file = os.path.join(self.output_path, 'special_text.txt')
        with open(special_text_file, 'a+') as f:
            if isinstance(text, list):
                text = [str(t) for t in text]
                text = '\n'.join(text)
            f.write(text + '\n')

    def find_flag(self):
        """
        自动查找可能的 flag
        :return:
        """
        logger.info('\n--------------------')
        logger.info('尝试从文件文本中提取 flag')
        find_flag_result_dict = {}
        # zsteg 日志文件，因为有16进制数据，如果不用严格模式，会有很多误报的数据
        zsteg_file = os.path.join(self.output_path, 'zsteg.txt')
        find_ctf_flag.get_flag_from_file(zsteg_file, True, find_flag_result_dict)
        strings_file = os.path.join(self.output_path, 'strings_1.txt')
        find_ctf_flag.get_flag_from_file(strings_file, self.find_flag_strict_mode, find_flag_result_dict)
        strings_file = os.path.join(self.output_path, 'strings_2.txt')
        find_ctf_flag.get_flag_from_file(strings_file, self.find_flag_strict_mode, find_flag_result_dict)
        strings_file = os.path.join(self.output_path, 'zsteg_text.txt')
        find_ctf_flag.get_flag_from_file(strings_file, self.find_flag_strict_mode, find_flag_result_dict)
        special_text_file = os.path.join(self.output_path, 'special_text.txt')
        if os.path.exists(special_text_file):
            find_ctf_flag.get_flag_from_file(special_text_file, self.find_flag_strict_mode, find_flag_result_dict)

        # 自动从分离出的 txt 文件中查找可能的 flag
        txt_dir = os.path.join(self.output_path, 'txt')
        if os.path.exists(txt_dir):
            for root, dirs, files in os.walk(txt_dir):
                for f in files:
                    txt_file_path = os.path.join(root, f)
                    find_ctf_flag.get_flag_from_file(
                        txt_file_path, self.find_flag_strict_mode, find_flag_result_dict)

        result_list = find_ctf_flag.clean_find_ctf_flag_result(find_flag_result_dict.keys())
        max_line = 20
        if len(result_list) > max_line:
            logger.info('匹配的内容较多，只显示前%s条，更多数据在日志文件中查看' % max_line)

        find_ctf_flag.color_print_result(result_list[:max_line])

    def run(self):
        self.check_file()
        self.strings()
        self.run_exif_tool()
        self.check_img_height()
        self.image_prepare()
        self.zsteg()
        self.binwalk()
        self.foremost()
        self.what_format()
        self.check_png()
        self.check_gif()
        self.stegdetect()
        self.check_strings()
        self.check_extracted_file()
        self.check_abnormal_file_magic()

        logger.info('\n--------------------')
        for t in self.result_list:
            logger.warning(t)

        self.find_flag()

        logger.info('=======================')


def main():
    (options, args) = parser.parse_args()

    if options.file_name is not None:
        file_name = options.file_name
    elif len(args) > 0:
        file_name = args[0]
    else:
        parser.print_help()
        return

    file_path = os.path.join(os.getcwd(), file_name)
    WhatSteg(file_path, options.find_flag_strict_mode, options.enable_img_prepare).run()


if __name__ == '__main__':
    main()
