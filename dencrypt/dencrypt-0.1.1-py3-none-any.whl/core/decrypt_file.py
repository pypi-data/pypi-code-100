from __future__ import annotations
from typing import Union

from io import BytesIO

from ..base import DencryptFileBase


class DecryptFile(DencryptFileBase):
    """
    Gera decriptação Fernet
    """

    def __init__(
        self, content:Union[bytes, str], key:Union[bytes, str]
    ) -> None:
        super().__init__(content, key, encrypt=False)

    
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
