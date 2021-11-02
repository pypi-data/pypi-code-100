import hashlib
import sys

from .exception import *
from .objtype import *

class has:
    def strhash(self, str_, **kwargs):
        """Hash Function that uses MD5 or SHA512."""
        
        secure = kwargs.get(
            "secure",
            True
        )
        
        if objtype(secure) != "bool":
            raise InvalidHashSecurityValue("Argument \"secure\" can only be boolean")
        
        if secure:
            return hashlib.sha512(str(str_).encode("iso-8859-1")).hexdigest()
        
        elif not secure:
            return hashlib.md5(str(str_).encode("iso-8859-1")).hexdigest()
            
        else:
            raise UnknownError("¯\_(ツ)_/¯")
        
    def bytehash(self, b, **kwargs):
        """Hash Function that uses MD5 or SHA512."""
        
        secure = kwargs.get(
            "secure",
            True
        )
        
        if objtype(secure) != "bool":
            raise InvalidHashSecurityValue("Argument \"secure\" can only be boolean")
        
        if objtype(b) != "bytes":
            raise InvalidHashTypeError("Argument \"b\" can only be bytestring")
        
        if secure:
            return hashlib.sha512(b).hexdigest()
        
        elif not secure:
            return hashlib.md5(b).hexdigest()
            
        else:
            raise UnknownError("¯\_(ツ)_/¯")
        
    def dehash(self, hashobj):
        sys.stderr.write("You can't dehash hashes, dumb dumb. Unless it's an MD5/SHA1, which I'm too lazy to check for.")
        sys.exit()

hashl = has()
del has