import binascii

from xscanner.modules import Data

class AnyData(Data):

    def __init__(self):
        super(AnyData, self).__init__()

    def from_path(self, path):
        self.path = path
        with open(path, "rb") as f:
            self.from_bytes(f.read())

    def from_bytes(self, _bytes):
        self.text = _bytes.decode("utf-8", errors="ignore")
        self.hex = binascii.hexlify(_bytes).decode("ascii")

    @property
    def type(self):
        return super().type

    @property
    def path(self):
        return super().path

    @path.setter
    def path(self, path):
        super(AnyData, AnyData).path.__set__(self, path)

    def match(self, s):
        return s in self.text

    def match_hex(self, h):
        return h in self.hex
    

# TODO 匹配方式
"""
匹配字符串 "" '' 表示字符串
1. 精准匹配字符串
2. 通配字符串
3. 

匹配16进制 [11223344551122]表示16进制
1. 精准匹配
2. 通配符（后台转正则）
3. 正则

@ / at语法
在什么位置，存在什么东西
a = "http://"
a @ 1000
"""
