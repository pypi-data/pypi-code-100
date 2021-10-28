from __future__ import annotations
from typing import Union, Tuple

import os.path
import base64
from io import BufferedWriter
import hashlib

import rsa
from rsa import PublicKey, PrivateKey
from cryptography.fernet import Fernet

from ..exception import UnknownKey, ExistingKey


class Crypt:
    """
    Responsável por gerar chaves RSA e Fernet
    e por conter métodos de validação
    """

    def __init__(self) -> None:
        self.keys: Tuple[PublicKey, PrivateKey] = (None, None)
        self._pubkey: PublicKey = None
        self._privkey: PrivateKey = None
        self._symmetrickey: bytes = None


    @property
    def pubkey(self) -> bytes:
        try:
            return self._pubkey.save_pkcs1("PEM")
        except:
            return None


    @property
    def privkey(self) -> bytes:
        try:
            return self._privkey.save_pkcs1("PEM")
        except:
            return None

    
    @property
    def symmetrickey(self) -> bytes:
        return self._symmetrickey


    @staticmethod
    def is_base64(content:bytes, urlsafe:bool=True) -> bool:
        """
        Verifica se o 'content' tem uma codificação base64 válida
        """

        if (urlsafe):
            ENCODE = base64.urlsafe_b64encode
            DECODE = base64.urlsafe_b64decode
        else:
            ENCODE = base64.b64encode
            DECODE = base64.b64decode
        
        try:
            return ENCODE(DECODE(content)) == content
        except Exception as e:
            return False


    @staticmethod
    def to_base64(content:bytes, urlsafe:bool=True) -> bool:
        """
        Converte 'content' para uma codificação base64 válida
        """

        if (urlsafe):
            ENCODE = base64.urlsafe_b64encode
        else:
            ENCODE = base64.b64encode
        
        return ENCODE(content)


    @staticmethod
    def md5(content:Union[bytes, str]) -> str:
        """
        Retorna o md5 hexadecimal do conteúdo
        """

        if (type(content) is str):
            return hashlib.md5(
                content.encode("UTF-8")).hexdigest()
        
        return hashlib.md5(
            content).hexdigest()


    def generate_all_keys(self, size:int=2048) -> Crypt:
        """
        Gera as chaves RSA (Pública e Privada) 
        e a chave Fernet
        """

        self.generate_keys(size)
        self.generate_symkey()

        return self


    def generate_keys(
        self, size:int=2048
    ) -> Tuple[PublicKey, PrivateKey]:
        """
        Gera as chaves RSA (Pública e Privada) 
        """

        self._pubkey, self._privkey = rsa.newkeys(size)
        self.keys = (self._pubkey, self._privkey)

        return self.keys


    def generate_symkey(self) -> bytes:
        """
        Gera a chave Fernet
        """

        self._symmetrickey = Fernet.generate_key()

        return self._symmetrickey


    def save_all_keys(
        self, prefix="", sufix="", ext=".key", 
        force_creation=True, replace_file=True, location=""
    ) -> Crypt:
        """
        Realiza o salvamento das chaves RSA (Pública e Privada)
        e o salvamento da chave Fernet

        Raises:
            UnknownKey
            ExistingKey
        """

        self.save_keys(
            prefix, sufix, ext, force_creation, replace_file, location)
        
        self.save_symkey(
            prefix, sufix, ext, force_creation, replace_file, location)

        return self


    def save_keys(
        self, prefix="", sufix="", ext=".key", 
        force_creation=True, replace_file=True, location=""
    ) -> Crypt:
        """
        Realiza o salvamento das chaves RSA (Pública e Privada)

        Raises:
            UnknownKey
            ExistingKey
        """
        
        FILENAME_PUBKEY = os.path.join(
            location, f"{prefix}publickey{sufix}{ext}")
        FILENAME_PRIVKEY = os.path.join(
            location, f"{prefix}privatekey{sufix}{ext}")

        # Public Key
        with self._save(
            self._pubkey, FILENAME_PUBKEY,
            self.generate_keys, force_creation, replace_file
        ) as file:
            file.write(
                self._pubkey.save_pkcs1("PEM"))

        # Private Key
        with self._save(
            self._privkey, FILENAME_PRIVKEY,
            self.generate_keys, force_creation, replace_file
        ) as file:
            file.write(
                self._privkey.save_pkcs1("PEM"))

        return self


    def save_symkey(
        self, prefix="", sufix="", ext=".key", 
        force_creation=True, replace_file=True, location=""
    ) -> Crypt:
        """
        Realiza o salvamento da chave Fernet

        Raises:
            UnknownKey
            ExistingKey
        """

        FILENAME_SYMKEY = os.path.join(
            location, f"{prefix}symmetrickey{sufix}{ext}")

        with self._save(
            self._symmetrickey, FILENAME_SYMKEY,
            self.generate_symkey, force_creation, replace_file
        ) as file:
            file.write(self._symmetrickey)

        return self

    
    def _save(
        self, key:Union[bytes, PublicKey, PrivateKey], filename:str,
        generate:callable, force_creation:bool, replace_file:bool
    ) -> BufferedWriter:
        """
        Suporte para "save_keys" e "save_symkey" 

        Raises:
            UnknownKey
            ExistingKey
        """
        
        # 1.
        if (key is None):
            if (force_creation):
                generate()
            else:
                raise UnknownKey("Key unavailable to save")

        # 2.
        KEY_FILENAME = filename

        # 2.1.
        if (not replace_file):
            EXISTS_KEY = os.path.isfile(KEY_FILENAME)

            if (EXISTS_KEY):
                raise ExistingKey(
                    f"'{KEY_FILENAME}' key already exists")
        
        # 2.2.
        return open(KEY_FILENAME, "wb")
