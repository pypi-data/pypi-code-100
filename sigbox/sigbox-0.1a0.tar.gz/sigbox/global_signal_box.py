
# Library import
from typing import TYPE_CHECKING

# Project import
if TYPE_CHECKING:
    from sigbox.signal_box import SignalBox


class _GlobalSignalBox:

    def __init__(self):
        self._signal_boxes = []

    def register(self, signal_box: 'SignalBox'):
        self._signal_boxes.append(signal_box)

    def pump(self):
        for signal_box in self._signal_boxes:
            signal_box.pump()


_GSB = _GlobalSignalBox()