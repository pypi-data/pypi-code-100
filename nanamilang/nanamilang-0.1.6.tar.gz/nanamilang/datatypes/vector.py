"""NanamiLang Vector Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from .base import Base


class Vector(Base):
    """NanamiLang Vector Data Type Class"""

    name: str = 'Vector'
    _expected_type = list
    _python_reference: list = None

    def __init__(self, reference: list) -> None:
        """NanamiLang Vector, initialize new instance"""

        super(Vector, self).__init__(reference=reference)

    def format(self) -> str:
        """NanamiLang Vector, format() method implementation"""

        return '[' + f'{" ".join([i.format() for i in self.reference()])}' + ']'
