import abc
import binascii


class Data(object):
    def __init__(self):
        self._type = "any"

    def from_path(self, path):
        self._path = path
        with open(path, "rb") as f:
            self.from_bytes(f.read())

    def from_io(self, _io):
        self.from_bytes(_io.read())

    def from_bytes(self, _bytes):
        self._text = _bytes.decode("utf-8", errors="ignore")
        self._hex = binascii.hexlify(_bytes).decode("ascii")

    def type(self):
        return self._type

    def get_path(self):
        return self._path

    def set_path(self, value):
        self._path = value

    def match(self, s):
        return s in self._text

    def match_hex(self, h):
        return h in self._hex
