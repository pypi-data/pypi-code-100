from abc import ABC, abstractmethod
from typing import List


class TokenGenerator(ABC):
    """Abstract class to model a List of tokens generator.

    Tokens are instances of a word in a text.
    A token can be:
        - a Lemma
        - inflected forms of a lemma
        - functional words
        - semantic primes

    """

    @abstractmethod
    def get_tokens(self, pos: str = "", regional_settings: str = "es") -> List:
        """ Get a list of tokens given the implementation.

        Args:
            regional_settings(str): regional settings of tokens retrieved.
            pos(str): POS tag if required.
        """
        pass
