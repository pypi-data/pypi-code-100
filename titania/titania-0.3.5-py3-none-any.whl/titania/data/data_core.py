from abc import ABC, abstractmethod


class TitaniaDataInterface(ABC):

    @abstractmethod
    def fetch(self):
        pass


class EmptyTitaniaData(TitaniaDataInterface):

    def fetch(self):
        return []