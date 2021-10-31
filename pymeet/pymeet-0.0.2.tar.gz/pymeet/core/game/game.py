from typing import Callable, Any
from abc import ABC, abstractmethod


class Game(ABC):
    @abstractmethod
    def push_joining_notification(
            self,
            requester_name: str,
            ip_address: str,
            on_accepted: Callable[[str], Any],
            on_declined: Callable[[str], Any],
    ):
        pass
