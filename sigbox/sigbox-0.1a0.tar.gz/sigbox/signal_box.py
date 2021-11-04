
# Library import
from typing import Optional, List, Callable, Dict
from queue import Queue, Empty

# Project import
from sigbox.signal import _Signal
from sigbox.signal_data import SignalData
from sigbox.global_signal_box import _GSB


class SignalBox:

    def __init__(self, signals: Optional[List[str]] = None):
        """
        Collection of signals, referenced by name.
        :param signals: Dict of signals with string name as key.
        :param new_signals: List of signal names to be created
        """
        self._signals = {}
        self._queue = Queue()
        if signals:
            self._signals.update({sig_name: _Signal(sig_name, self) for sig_name in signals})
        _GSB.register(self)

    @property
    def list(self) -> List:
        """ :return: List of signal names """
        return list(self._signals.keys())

    def add(self, signal_name) -> None:
        """
        Create new signal. Name must be unqiue for this signal box or class, otherwise it will overwrite
        :param signal_name: String name of signal
        """
        self._signals[signal_name] = _Signal(signal_name, self)

    def bind(self, signal: str, func: Callable) -> None:
        """
        Bind given function to the signal name specified
        :param signal: string name of signal
        :param func: function to bind (must conform to signal signature)
        :raises: KeyError if signal name not found
        """
        self._signals[signal].bind(func)

    def unbind(self, signal: str, func: Callable) -> None:
        """
        Unbind given function from signal specified.
        :param signal: string name of signal
        :param func: function to unbind
        :raises: Keyerror if signal name not found, ValueError if function not found.
        """
        self._signals[signal].unbind(func)

    def trigger(self, signal_name: str, data: Optional[Dict] = None, signal_data: Optional['SignalData'] = None) -> None:
        """
        Trigger the given signal, with the args specified
        :param signal_name: string name of the signal
        :param data: Dict of data to pass to bound functions (will be inserted into SignalData instance)
        :param signal_data: Pass SignalData instance in directly
        :raises: KeyError if the signal name is not found, TypeError if the kwargs doesn't match the bound function's
                 signature
        """
        signal_data = signal_data if signal_data else SignalData(signal=self._signals[signal_name], data=data)
        self._queue.put_nowait(signal_data)

    def set(self, name: str) -> None:
        """
        Adds signal with the specified name
        :param name: string name of signal
        """
        self._signals[name] = _Signal(name)

    def get(self, name) -> _Signal:
        """
        Gets the signal instance of the signal with the specified name
        :param name: string name of instance
        :return: Signal instance
        :raises: KeyError if the signal name is not found
        """
        return self._signals[name]

    def pump(self) -> None:
        """
        Process any triggered signals in the queue, calling their bound functions
        """
        while True:
            try:
                self._queue.get_nowait().process()
            except Empty:
                break


class SignalBoxClass:

    def __init__(self, signals: Optional[List[str]] = None):
        """
        Convenience inheriting class, adds a SignalBox instance to self.signals.
        This class must be used if you want to use @SignalDecorator("signal_name") to automatically
        trigger a signal when a function is called.
        :param signals: List of signal names to create
        """
        self.signals = SignalBox(signals=signals)