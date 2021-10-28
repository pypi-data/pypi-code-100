from __future__ import annotations
from typing import Union

from io import BytesIO
import base64

import rsa

from ..core import Crypt
from ..base import LoadSaveBase
from ..support import KeyFile
from ..exception import InvalidContent


class DencryptBase(LoadSaveBase):
    """
    Classe base para Encrypt e Decrypt
    Responsável pela encriptação e decriptação RSA

    Adequada para dados pequenos
    """

    def __init__(
        self, content:Union[bytes, str], key:Union[bytes, str], encrypt:bool
    ) -> None:
        self.content: bytes = None
        self.content_factory: bytes = None
        self.key = KeyFile(key).get()

        self._load_file(content)
        self._factory(encrypt)

    
    def get(
        self, decode:str=None, b64:bool=False
    ) -> bytes:
        """
        Sobrescreve o padrão da codificação base64 para False
        """

        return super().get(decode, b64)
    

    def save(
        self, filename:Union[str, BytesIO], decode:str=None, b64:bool=False,
        replace_file:bool=True
    ) -> bool:
        """
        Sobrescreve o padrão da codificação base64 para False
        """

        return super().save(filename, decode, b64, replace_file)


    def _factory(self, encrypt:bool) -> bytes:
        """
        Realiza a encriptação ou decriptação RSA
        
        @param encrypt: bool 
            True gera a encriptação do conteúdo
            False gera a decriptação do conteúdo

        Raises:
            InvalidContent
        """

        content = self.content

        if (content is None):
            raise InvalidContent(f"Invalid Content '{content}'")
        
        if (encrypt):
            self.content_factory = rsa.encrypt(content, self.key)
        else:
            if (Crypt.is_base64(content)):
                content = base64.urlsafe_b64decode(content)

            self.content_factory = rsa.decrypt(content, self.key)

        return self.content_factory
