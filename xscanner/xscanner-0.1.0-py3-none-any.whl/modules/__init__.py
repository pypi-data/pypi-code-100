import abc
import binascii
# metaclass=abc.ABCMeta
class Data(object):

    def __init__(self):
        self.__type = 'any'

    def from_path(self, path):
        raise NotImplementedError
        # self.__path = path
        # with open(path, "rb") as f:
            # self.from_bytes(f.read())

    def from_bytes(self, _bytes):
        raise NotImplementedError
        # self.text = _bytes.decode("utf-8", errors="ignore")
        # self.hex = binascii.hexlify(_bytes).decode("ascii")

    @property
    def type(self):
        return self.__type

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, value):
        self.__path = value

    def match(self, regex): # 匹配字符串
        raise NotImplementedError

    def match_hex(self, regex): # 匹配16进制
        raise NotImplementedError
