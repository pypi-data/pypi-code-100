from __future__ import annotations
from typing import Union

from ..base import DencryptBase


class Decrypt(DencryptBase):
    """
    Gera decriptação RSA
    """

    def __init__(
        self, content:Union[bytes, str], privkey:Union[bytes, str]
    ) -> None:
        super().__init__(content, privkey, encrypt=False)
