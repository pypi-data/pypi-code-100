import base64
import hashlib
import random
import string
from typing import Tuple

__version__ = '1.0.0'

VERSION = tuple([int(v) for v in __version__.split('.')])

'''
MIN_SALT_SIZE = 8
minimum salt size recommended by the RFC
'''
MIN_SALT_SIZE = 8

'''
generate_random_salt
will generate random salt with or without seed
'''
def _generate_random_salt(size, seed=None):
        if seed != None:
             random.seed(seed)
        return(''.join(random.choice(string.ascii_letters + string.digits) for i in range(size)))

def _slow_equals(cipher_text: str, new_cipher_text: bytes) -> bool:
    cp_bytes = base64.b64decode(cipher_text)
    diff = len(cp_bytes) ^ len(new_cipher_text)
    for i in range(len(cp_bytes)):
        diff |= cp_bytes[i] ^ new_cipher_text[i]
    
    return diff == 0

'''
PyPBKDF2
'''
class PyPBKDF2:
    def __init__(self, alg='sha256', salt_size=MIN_SALT_SIZE, iterations=100000, key_len=64) -> None:
        self.alg = alg

        if salt_size < 8:
            self.salt_size = MIN_SALT_SIZE
        else:
            self.salt_size = salt_size
            
        self.iterations = iterations
        self.key_len = key_len
    
    def hash_password(self, password: str) -> Tuple:
        salt = _generate_random_salt(self.salt_size)
        dk = hashlib.pbkdf2_hmac(self.alg, bytes(password, encoding='utf-8'), 
            bytes(salt, encoding='utf-8'), self.iterations, self.key_len)
        cipher_text_bytes = base64.b64encode(dk)
        cipher_text = str(cipher_text_bytes, encoding='utf-8')
        return (cipher_text, salt)

    def verify_password(self, password: str, cipher_text: str, salt: str) -> bool:
        salt_bytes = salt.encode(encoding='utf-8')
        dk = hashlib.pbkdf2_hmac(self.alg, bytes(password, encoding='utf-8'), 
            salt_bytes, self.iterations, self.key_len)
        return _slow_equals(cipher_text, dk)
        