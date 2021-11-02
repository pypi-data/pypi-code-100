"""NanamiLan HashMap Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from .base import Base


class HashMap(Base):
    """NanamiLang Function Data Type Class"""

    name: str = 'HashMap'
    _expected_type = dict
    _python_reference: dict = None

    def __init__(self, reference: dict) -> None:
        """NanamiLang Function, initialize new instance"""

        super(HashMap, self).__init__(reference=reference)

    def format(self) -> str:
        """NanamiLang Vector, format() method implementation"""

        return '{' + f'{" ".join([f"{k.format()} {v.format()}" for k, v in self.reference().items()])}' + '}'
