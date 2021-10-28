from __future__ import annotations
from typing import Union

from io import BytesIO
import rsa
from rsa import PublicKey, PrivateKey

from ..base import LoadSaveBase
from ..exception import InvalidKey


class KeyFile(LoadSaveBase):
    """
    Carrega uma chave RSA (Pública ou Privada)
    """

    def __init__(self, file:Union[bytes, str]):
        self.content: bytes = None
        self.key: Union[PublicKey, PrivateKey] = None
        self._load_file(file)


    def get(self):
        return self.key


    def _load_file(
        self, filename:Union[bytes, str, BytesIO]
    ) -> Union[PublicKey, PrivateKey]:
        """
        @param filename: bytes | str | BytesIO
            bytes: 
                Conteúdo final para ser criptografado
            str:
                - Filename do arquivo com o conteúdo para ser criptografado
                - Caso arquivo não exista, criptografará a string
            BytesIO:
                Caso os dados estejam na memória
        
        Raises:
            InvalidKey
        """

        self.content = self._load_by_filename(filename)

        try:
            self.key = rsa.PublicKey.load_pkcs1(self.content)
        except:
            try:
                self.key = rsa.PrivateKey.load_pkcs1(self.content)
            except:
                raise InvalidKey(f"Invalid '{filename}' key")
        
        return self.key
