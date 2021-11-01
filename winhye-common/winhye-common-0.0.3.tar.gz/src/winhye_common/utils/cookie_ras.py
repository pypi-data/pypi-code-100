import os
import base64

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

__all__ = ["CookieRsa"]


class CookieRsa:
    def __init__(self):
        key_dir = "/data/log/rsa_key"
        if not os.path.exists(key_dir):
            os.makedirs(key_dir)
        self.__config_path = key_dir

    # 初始化公钥私钥
    def __init_key(self):
        # 初始化RSA对象， 伪随机数生成器
        rsa = RSA.generate(1024, Random.new().read)

        # 私钥
        private_key = rsa.exportKey()
        private_key_path = os.path.join(self.__config_path, "private_key.pem")

        # 公钥
        public_key = rsa.publickey().exportKey()
        public_key_path = os.path.join(self.__config_path, "public_key.pem")

        with open(private_key_path, 'w') as f:
            f.write(private_key.decode())

        with open(public_key_path, 'w') as f:
            f.write(public_key.decode())

        return private_key, public_key

    # 获取私钥
    def __get_private_key(self):
        private_key_path = os.path.join(self.__config_path, "private_key.pem")
        if os.path.exists(private_key_path):
            with open(private_key_path, "r") as f:
                private_key = f.read()
        else:
            private_key = self.__init_key()[0]

        return private_key

    # 获取公钥
    def __get_public_key(self):
        public_key_path = os.path.join(self.__config_path, "public_key.pem")
        if os.path.exists(public_key_path):
            with open(public_key_path, "r") as f:
                public_key = f.read()
        else:
            public_key = self.__init_key()[1]
        return public_key

    # 加密
    def rsa_encrypt(self, content: str) -> str:
        public = RSA.importKey(self.__get_public_key())
        cipher = PKCS1_v1_5.new(public)
        return base64.b64encode(cipher.encrypt(content.encode('utf-8'))).decode('utf-8')

    # 解密
    def rsa_decrypt(self, content: str) -> str:
        private = RSA.importKey(self.__get_private_key())
        cipher = PKCS1_v1_5.new(private)
        return cipher.decrypt(base64.b64decode(content), b'error: decrypt fail').decode('utf-8')
