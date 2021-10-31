from abc import ABC, abstractmethod
from typing import List


class CorpusOperations(ABC):
    """Interface shared across all corpus types
    to offer operations:

     - Knowing whether the corpus can be indexed or not.
     - Knowing whether the corpus can be annotated or not.
     - Get the corpus events as a List of strings: this can be useful for
        training third party models that receives text as a list of string.
    """
    @property
    @abstractmethod
    def indexable(self) -> bool:
        pass

    @property
    @abstractmethod
    def annotable(self) -> bool:
        pass

    @property
    @abstractmethod
    def get_events_as_strings(self) -> List[str]:
        """
        Todo: As the Curriculum development takes shape, this method should be
            deprecated and removed. Models will eventually require a structured
            data input that will be implemented in corpus that are compliant with
            the incorporated models.
        :return:
        """
        pass
