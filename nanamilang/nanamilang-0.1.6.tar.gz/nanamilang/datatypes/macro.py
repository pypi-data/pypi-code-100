"""NanamiLan Macro Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from .base import Base


class Macro(Base):
    """NanamiLang Macro Data Type Class"""

    name: str = 'Macro'
    _expected_type = dict
    _python_reference: dict = None

    def __init__(self, reference: dict) -> None:
        """NanamiLang Macro, initialize new instance"""

        super(Macro, self).__init__(reference=reference)

    def reference(self):
        """NanamiLang Macro, reference() implementation"""

        return self._python_reference.get('macro_reference')

    def format(self) -> str:
        """NanamiLang Macro, format() method implementation"""

        return self._python_reference.get('macro_name')
