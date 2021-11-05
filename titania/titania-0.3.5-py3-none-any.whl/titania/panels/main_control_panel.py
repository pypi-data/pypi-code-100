from PyQt5.QtWidgets import QWidget
from abc import ABC, abstractmethod


class ControlPanelInterface(ABC):

    @abstractmethod
    def get_control_panel(self) -> QWidget:
        pass


class EmptyControlPanel(ControlPanelInterface):
    def __init__(self, data=None, widget=None):
        self.control_panel = None

    def get_control_panel(self):
        return self.control_panel


