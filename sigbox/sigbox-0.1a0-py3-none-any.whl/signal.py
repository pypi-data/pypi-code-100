
# Library import
from typing import TYPE_CHECKING, Callable, Optional

# Project import
if TYPE_CHECKING:
    from sigbox.signal_box import SignalBox
    from sigbox.signal_data import SignalData


class _Signal:

    def __init__(self, name: str, signal_box: 'SignalBox'):
        """
        Signal/slot pattern.
        :param name: Name/identifier for signal
        """
        self._name = name
        self._signal_box = signal_box
        self._bound_functions = []

    @property
    def name(self) -> str:
        """ :return: string name of signal """
        return self._name

    @property
    def signal_box(self) -> 'SignalBox':
        """ :return: Parent SignalBox instance """
        return self._signal_box

    def bind(self, function: Callable):
        """
        Bind given function, which must accept a SignalData object as an argument
        Return values will be ignored
        :param function:
        """
        self._bound_functions.append(function)

    def unbind(self, function: Callable):
        """
        Unbind given function
        :param function:
        """
        self._bound_functions.remove(function)

    def trigger(self, signal_data: 'SignalData') -> None:
        """
        Trigger the signal, calling every bound function with data provided.
        :param signal_data: SignalData instance to be passed down to bound function
        :raises: TypeError if the kwargs provided don't match the bound function's signature
        """
        for func in self._bound_functions:
            func(signal_data)