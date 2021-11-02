"""NanamiLang Base Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

import nanamilang.shortcuts


class Base:
    """NanamiLang Base Data Type Class"""

    name: str
    _expected_type = None
    _python_reference = None

    def __init__(self, reference) -> None:
        """NanamiLang Base Data Type, initialize new instance"""

        nanamilang.shortcuts.ASSERT_TYPE_OF_A(reference,
                                              self._expected_type)

        self._python_reference = reference

    def reference(self):
        """NanamiLang Base Data Type, self._python_reference getter"""

        return self._python_reference

    def format(self) -> str:
        """NanamiLang Base Data Type, format() default implementation"""
        return f'{self._python_reference}'  # we need to cast it to str

    def __str__(self) -> str:
        """NanamiLang Base Data Type, __str__() method implementation"""

        return f'<{self.name}>: {self.format()}'

    def __repr__(self) -> str:
        """NanamiLang Base Data Type, __repr__() method implementation"""

        return self.__str__()
