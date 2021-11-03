import lzma
import codecs
import base64

from .exception import *
from .objtype import *

class ob:
    def strobfuscate(self, str_):
        """Minorly obfuscates a string. While it is unreadable,
        don't expect this to stand up to anyone with a bit
        of python knowledge"""
        try:
            return lzma.compress(base64.a85encode(codecs.encode(str(str_)[::-1], "rot-13").encode("utf-8"))).decode("iso-8859-1")[::-1]
        
        except UnicodeDecodeError:
            return lzma.compress(base64.a85encode(codecs.encode(str(str_)[::-1], "rot-13").encode("iso-8859-1"))).decode("iso-8859-1")[::-1]
        
    def strunobfuscate(self, str_):
        """Unobfuscates a string obfuscated by beetroot.strobfuscate()"""
        try:
            return codecs.encode(base64.a85decode(lzma.decompress(str_[::-1].encode("iso-8859-1"))).decode("utf-8"), "rot-13")[::-1]
        
        except UnicodeDecodeError:
            return codecs.encode(base64.a85decode(lzma.decompress(str_[::-1].encode("iso-8859-1"))).decode("iso-8859-1"), "rot-13")[::-1]
        
    def byteobfuscate(self, b):
        """Minorly obfuscates a bytestring. While it is unreadable,
        don't expect this to stand up to anyone with a bit
        of python knowledge"""
        if objtype(b) != "bytes":
            raise InvalidTypeError("Argument \"b\" can only be bytestring")
            
        return lzma.compress(base64.a85encode(codecs.encode(str(b.decode("iso-8859-1"))[::-1], "rot-13").encode("iso-8859-1"))).decode("iso-8859-1")[::-1].encode("iso-8859-1")
        
    def byteunobfuscate(self, b):
        """Unobfuscates a string obfuscated by beetroot.strobfuscate()"""
        if objtype(b) != "bytes":
            raise InvalidTypeError("Argument \"b\" can only be bytestring")
        
        return codecs.encode(base64.a85decode(lzma.decompress(b.decode("iso-8859-1")[::-1].encode("iso-8859-1"))).decode("iso-8859-1"), "rot-13")[::-1].encode("iso-8859-1")

obf = ob()
del ob