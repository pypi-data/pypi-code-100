from __future__ import annotations
from typing import Union

from io import BytesIO
import base64

from cryptography.fernet import Fernet

from ..base import LoadSaveBase
from ..core import Crypt
from ..exception import InvalidContent


class DencryptFileBase(LoadSaveBase):
    """
    Classe base para EncryptFile e DecryptFile
    Responsável pela encriptação e decriptação Fernet

    Adequada para dados grandes
    """

    def __init__(
        self, content:Union[bytes, str], key:Union[bytes, str], encrypt:bool
    ) -> None:
        self.content: bytes = None
        self.content_factory: bytes = None
        self.key: bytes = None

        self._load_file(content)
        self._load_key(key)
        self._factory(encrypt)

    
    def _load_key(
        self, filename:Union[bytes, str, BytesIO]
    ) -> DencryptFileBase:
        """
        Realiza o carregamento da chave
        """
        
        self.key = self._load_by_filename(filename)

        return self


    def _factory(self, encrypt:bool) -> bytes:
        """
        Realiza a encriptação ou decriptação Fernet
        
        @param encrypt: bool 
            True gera a encriptação do conteúdo
            False gera a decriptação do conteúdo

        Raises:
            InvalidContent
        """

        content = self.content

        if (content is None):
            raise InvalidContent(f"Invalid Content '{content}'")

        if (not Crypt.is_base64(self.key)):
            self.key = Crypt.to_base64(self.key)

        fer = Fernet(self.key)
        
        if (encrypt):
            self.content_factory = fer.encrypt(content)
        else:
            if (not Crypt.is_base64(content)):
                content = base64.urlsafe_b64encode(content)

            self.content_factory = fer.decrypt(content)

        return self.content_factory
