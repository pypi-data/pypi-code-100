from __future__ import absolute_import

import binascii
import io
import zipfile

import pyftype
from xscanner.modules import Data


class ZipData(Data):
    def __init__(self):
        self._type = "zip"
        self._mime = "application/zip"

    def from_bytes(self, _bytes):
        super(ZipData, self).from_bytes(_bytes)

        self.zfile = zipfile.ZipFile(io.BytesIO(_bytes), "r")
        self._init_zipfiles()

    def _init_zipfiles(self):
        self.datas = []
        self.strings = {}
        self.hexs = {}
        for name in self.zfile.namelist():
            bs = self.zfile.read(name)
            d = Data()
            d.from_bytes(bs)
            d.path = name
            self.datas.append(d)
            self.strings[name] = bs.decode("utf-8", errors="ignore")
            self.hexs[name] = binascii.hexlify(bs).decode("ascii")
        self.zfile.close()

    def match_file(self, name, s):
        for k, v in self.strings.items():
            if name not in k:
                continue
            if s in v:
                return True
        return False

    def match_file_hex(self, name, h):
        for k, v in self.hexs.items():
            if name not in k:
                continue
            if h in v:
                return True
        return False

    # 把所有的文件都当作普通文件？
    def get_datas(self):
        return self.datas
