import tkinter as tk
import darkdetect

from enum import Enum
from typing import Union


from ..abs_class import ThemedWidget
from ..font import build_all_font


class Theme(Enum):
    AUTO = "auto"
    DARK = "dark"
    LIGHT = "light"


class Tk(tk.Tk, ThemedWidget):
    def __init__(self):
        tk.Tk.__init__(self)
        self.__theme = None
        self.__theme_updated_id = None
        self.__theme_forced = Theme.AUTO
        self.bind('<Configure>', self.on_configure)
        self.after(50, self.update_theme)
        build_all_font(self)

    @property
    def theme(self):
        if self.__theme_forced != Theme.AUTO:
            return self.__theme_forced
        elif self.__theme is None:
            self.__theme = darkdetect.theme()
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
        if event.widget == self and self.__theme_forced == Theme.AUTO:
            if self.theme != darkdetect.theme():
                self.__theme = None
                if self.__theme_updated_id is not None:
                    self.after_cancel(self.__theme_updated_id)
                self.__theme_updated_id = self.after(500, self.update_theme)

    def update_theme(self):
        self.config(bg=self.get_color('main_bg'))
        self.configure(background=self.get_color('main_bg'))
        for child in self.children.values():
            if isinstance(child, ThemedWidget):
                child.update_theme()
