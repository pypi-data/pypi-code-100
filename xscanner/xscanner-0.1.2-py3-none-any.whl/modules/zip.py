from __future__ import absolute_import

import binascii
import zipfile

from xscanner.modules import Data
import pyftype
from xscanner.modules import anything
import io
class ZipData(Data):

    def from_path(self, path):
        self.path = path
        f =  open(path, 'rb')
        self.from_io(f)
        f.close()

    def from_bytes(self, _bytes):
        self.text = _bytes.decode("utf-8", errors="ignore")
        self.hex = binascii.hexlify(_bytes).decode("ascii")

        self.zfile = zipfile.ZipFile(io.BytesIO(_bytes), 'r')

    def from_io(self, _io):
        # 全部初始化到内存
        self.strings = {}
        self.hexs = {}
        self.zfile = zipfile.ZipFile(_io, 'r')
        self.datas = []
        for name in self.zfile.namelist():
            bs = self.zfile.read(name)
            d = anything.AnyData()
            d.from_bytes(bs)
            d.path = name
            self.datas.append(d)
            self.strings[name] = bs.decode("utf-8", errors="ignore")
            self.hexs[name] = binascii.hexlify(bs).decode("ascii")
        self.zfile.close()
        
    def close(self):
        self.zfile.close()
    
    @property
    def type(self):
        return super().type

    @property
    def path(self):
        return super().path

    @path.setter
    def path(self, path):
        super(ZipData, ZipData).path.__set__(self, path)

    def match(self, s):
        # FIXME 遍历所有的文件，进行匹配
        # 因为已经使用其他方式，全部匹配了一遍，还有必要再匹配么？
        # 这里其实是重复匹配
        for _, v in self.strings.items():
            if s in v:
                return True
        return False

    def match_hex(self, h):
        # 遍历所有的文件进行匹配
        for _, v in self.hexs.items():
            if h in v:
                return True
        return False

    def match_file(self, name, s):
        # 对指定文件进行匹配
        pass

    def match_file_hex(self, name, h):
        pass

    # 把所有的文件都当作普通文件？
    def get_datas(self):
        return self.datas
