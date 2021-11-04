
# Library import
from typing import Optional, Any

# Project import
from sigbox.signal import _Signal


class SignalData:

    def __init__(self, signal: _Signal, data: Optional[dict]):
        """
        Simple data container class, passed to bound functions when called
        :param signal: Signal instance that triggered the bound function
        :param data: Dict of data that will be accessed directly from the this instance (avoid keywords)
        """
        self._signal = signal
        self._data = data if data else {}

    @property
    def signal(self):
        return self._signal

    def process(self):
        self._signal.trigger(signal_data=self)

    def __getattr__(self, item):
        return self._data[item]



class DecoratedSignalData(SignalData):

    def __init__(self, signal: _Signal, data: dict, decorated_method: str, decorated_return: Any):
        super().__init__(signal=signal, data=data)
        self._decorated_method = decorated_method
        self._decorated_return = decorated_return

    @property
    def decorated_method(self) -> str:
        return self._decorated_method

    @property
    def decorated_return(self) -> Any:
        return self._decorated_return