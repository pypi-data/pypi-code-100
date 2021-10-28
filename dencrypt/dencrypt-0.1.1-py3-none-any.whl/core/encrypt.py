from __future__ import annotations
from typing import Union

from ..base import DencryptBase


class Encrypt(DencryptBase):
    """
    Gera encriptação RSA
    """

    def __init__(
        self, content:Union[bytes, str], pubkey:Union[bytes, str]
    ) -> None:
        super().__init__(content, pubkey, encrypt=True)
