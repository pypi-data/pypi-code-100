from __future__ import annotations
from typing import Union
from abc import ABC

import os
from io import BytesIO
import base64

from ..core import Crypt
from ..exception import FileOverwrite


class LoadSaveBase(ABC):
    """
    Responsável pelos métodos de:
        Obtenção, carregamento e salvamento
    """

    def __init__(self):
        self.content_factory: bytes = None
    

    def get(
        self, decode:str=None, b64:bool=True
    ) -> bytes:
        """
        Obtém o conteúdo criptografado
        """

        content_factory = self.content_factory
        
        if (not b64):
            if (Crypt.is_base64(content_factory)):
                content_factory = base64.urlsafe_b64decode(
                    self.content_factory)
        else:
            if (not Crypt.is_base64(content_factory)):
                content_factory = base64.urlsafe_b64encode(
                    self.content_factory)
        
        if (decode):
            return content_factory.decode(decode) 

        return content_factory


    def save(
        self, filename:Union[str, BytesIO], decode:str=None, b64:bool=True,
        replace_file:bool=True
    ) -> bool:
        """
        Salva o conteúdo criptografado em um arquivo
        """

        try:
            self._save_by_filename(
                filename, self.get(decode, b64), replace_file)
            return True
        except:
            return False

    
    def _load_file(
        self, filename:Union[bytes, str, BytesIO]
    ) -> LoadSaveBase:
        """
        @param filename: bytes | str | BytesIO
            bytes: 
                Conteúdo final para ser criptografado
            str:
                - Filename do arquivo com o conteúdo para ser criptografado
                - Caso arquivo não exista, criptografará a string
            BytesIO:
                Caso os dados estejam na memória
        """

        self.content = self._load_by_filename(filename)

        return self


    def _load_by_filename(
        self, filename:Union[str, BytesIO, bytes]
    ) -> bytes:
        """
        Responsável por carregar o conteúdo e retorná-lo em bytes
        """

        content = None

        # Se o dado for do tipo STR
        if (type(filename) is str):
            try:
                with open(filename, "rb") as file:
                    content = file.read()
            except:
                content = filename.encode()
        
        # Se o dado for do tipo BYTES
        if (type(filename) is bytes):
            content = filename

        # Se o dado for do tipo BytesIO
        if (type(filename) is BytesIO):
            try:
                filename.seek(0)
                content = filename.read()
            except Exception as e:
                content = None

        return content

    
    def _save_by_filename(
        self, filename:Union[str, BytesIO], content:bytes, replace_file:bool
    ) -> None:
        """
        Responsável salvar o conteúdo no arquivo

        Raises:
            FileOverwrite
        """

        if (type(filename) is str):
            if (replace_file or not os.path.exists(filename)):
                with open(filename, "wb") as file:
                    file.write(content)
            else:
                raise FileOverwrite(f"'{filename}' cannot be overwritten")
        else:
            filename.write(content)
