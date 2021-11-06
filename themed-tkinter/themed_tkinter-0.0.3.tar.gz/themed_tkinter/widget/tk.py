import tkinter as tk
import darkdetect

from enum import Enum
from typing import Union


from ..abs_class import ThemedWindow
from ..font import build_all_font
from ..color import add_tk_instance


class Theme(Enum):
    AUTO = "auto"
    DARK = "dark"
    LIGHT = "light"


class Tk(tk.Tk, ThemedWindow):
    def __init__(self):
        tk.Tk.__init__(self)
        ThemedWindow.__init__(self)
        self.__theme = None
        self.__theme_forced = Theme.AUTO
        build_all_font(self)
        add_tk_instance(self)

    @property
    def theme(self):
        if self.__theme_forced != Theme.AUTO:
            return self.__theme_forced
        elif self.__theme is None:
            self.__theme = darkdetect.theme().lower()
        return self.__theme

    @theme.setter
    def theme(self, new_theme: Union[Theme, str]):
        if type(new_theme) == Theme:
            new_theme = new_theme.value
        if new_theme.lower() in [e.value for e in Theme]:
            self.__theme_forced = new_theme
        else:
            raise RuntimeError("Wrong theme")

    def on_configure(self, event):
        if self.__theme_forced == Theme.AUTO:
            if self.theme != darkdetect.theme():
                self.__theme = None
                ThemedWindow.on_configure(self, event)

