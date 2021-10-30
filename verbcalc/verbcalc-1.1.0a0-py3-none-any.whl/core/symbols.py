"""
   Handles symbol storage.
"""


class Symbols:
    """
    Stores lists with words corresponding to given symbols.
    """

    def __init__(self):
        self._additions = ['plus']
        self._subtractions = ['minus']
        self._multiplications = ['times', 'multiplied by']
        self._divisions = ['divided by']
        self._exponentiations = ['to the power of']
        self.symbol_dictionary = {
            '+': self._additions,
            '-': self._subtractions,
            '*': self._multiplications,
            '/': self._divisions,
            '**': self._exponentiations
        }

    @property
    def additions(self) -> list:
        return self._additions

    @property
    def subtractions(self) -> list:
        return self._subtractions

    @property
    def multiplications(self) -> list:
        return self._multiplications

    @property
    def divisions(self) -> list:
        return self._divisions

    @property
    def exponentiations(self) -> list:
        return self._exponentiations

    @additions.setter
    def additions(self, value) -> None:
        self._additions = value
        self.symbol_dictionary.update({'+': self._additions})

    @subtractions.setter
    def subtractions(self, value) -> None:
        self._subtractions = value
        self.symbol_dictionary.update({'-': self._subtractions})

    @multiplications.setter
    def multiplications(self, value) -> None:
        self._multiplications = value
        self.symbol_dictionary.update({'*': self._multiplications})

    @divisions.setter
    def divisions(self, value) -> None:
        self._divisions = value
        self.symbol_dictionary.update({'/': self._divisions})

    @exponentiations.setter
    def exponentiations(self, value) -> None:
        self._exponentiations = value
        self.symbol_dictionary.update({'**': self._exponentiations})
