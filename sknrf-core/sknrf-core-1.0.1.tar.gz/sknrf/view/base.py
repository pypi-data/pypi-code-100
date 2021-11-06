import abc
import sys
import os
import webbrowser

from PySide2.QtCore import Qt

from sknrf.settings import Settings, InstrumentFlag
from sknrf.utilities.patterns import AbstractType
__author__ = 'dtbespal'


class AbstractView(object, metaclass=AbstractType):

    _port_nums = [0, 1, 2]
    _instruments = [InstrumentFlag.ALL, InstrumentFlag.ALL, InstrumentFlag.ALL]

    def __init__(self, parent=None):
        super(AbstractView, self).__init__()
        self.__key = 0
        self._model = None

    def connect_submenu(self, sub_menu):
        sub_menu.setAttribute(Qt.WA_DeleteOnClose)
        sub_menu.destroyed.connect(self.window().update)

    @abc.abstractmethod
    def model(self):
        return self._model

    @abc.abstractmethod
    def set_model(self, model):
        self._model = model

    @abc.abstractmethod
    def connect_signals(self):
        pass

    @abc.abstractmethod
    def disconnect_signals(self):
        pass

    def clicked_doc(self):
        name = self.__module__
        if name == '__main__':
            filename = sys.modules[self.__module__].__file__
            name = filename[len(Settings().root)::].replace(".py", "").replace(os.sep, ".")
        url = "/".join((Settings().url_root, Settings().url_api, name + ".html"))
        webbrowser.open(url, new=2, autoraise=True)

    @abc.abstractmethod
    def update(self):
        pass
