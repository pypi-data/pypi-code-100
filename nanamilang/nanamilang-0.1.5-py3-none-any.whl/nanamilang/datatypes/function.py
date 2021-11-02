"""NanamiLan Function Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from .base import Base


class Function(Base):
    """NanamiLang Function Data Type Class"""

    name: str = 'Function'
    _expected_type = dict
    _python_reference: dict = None

    def __init__(self, reference: dict) -> None:
        """NanamiLang Function, initialize new instance"""

        super(Function, self).__init__(reference=reference)

    def reference(self):
        """NanamiLang Function, reference() implementation"""

        return self._python_reference.get('function_reference')

    def format(self) -> str:
        """NanamiLang Function, format() method implementation"""

        return self._python_reference.get('function_name')
