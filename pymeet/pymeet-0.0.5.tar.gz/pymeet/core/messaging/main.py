from typing import Dict
from abc import ABC, abstractmethod


class MessageServer(ABC):
    @abstractmethod
    def send(self, client_id: str, message: Dict):
        pass

    @abstractmethod
    def accept_connection(self, client_id: str):
        pass

    @abstractmethod
    def decline_connection(self, client_id: str):
        pass


class MessageClient(ABC):
    @abstractmethod
    def send(self, message: Dict):
        pass
