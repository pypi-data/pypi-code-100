"""NanamiLang NException Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from nanamilang.shortcuts import ASSERT_LIST_LENGTH_IS
from .base import Base


class NException(Base):
    """NanamiLang String Data Type Class"""

    name: str = 'NException'
    _expected_type = list
    _python_reference: list = None

    def __init__(self, reference: list) -> None:
        """NanamiLang NException, initialize new instance"""

        ASSERT_LIST_LENGTH_IS(reference, 2)

        super(NException, self).__init__(reference=reference)

    def format(self) -> str:
        """NanamiLang NException, format() method implementation"""

        exception_class, message = self.reference()

        return f'{exception_class} has been occurred, details: {message}'
