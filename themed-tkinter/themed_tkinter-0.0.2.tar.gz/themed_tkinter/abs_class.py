import tkinter as tk
import darkdetect

from abc import ABC, abstractmethod
from typing import Dict, Union

from .color import colors


class ThemedWidget(ABC, tk.Widget):

    tk_color_opt = {
        "background", "bg",
        "activebackground",
        "highlightbackground",
        "selectbackground",

        "foreground", "fg",
        "activeforeground",
        "disabledforeground",
        "selectforeground",

        "highlightcolor"
    }

    def __init__(self, master, widget_name: str = None):
        if widget_name is None:
            widget_name = self.__class__.__name__.lower()
        tk.Widget.__init__(self, master, widget_name)
        self.__updated_kwargs = {}

    def update_color_in_kwargs(self, kw_in: Dict[str, Union[str, int]]) -> Dict[str, Union[str, int]]:
        kw_out = dict(kw_in)
        for key in ThemedWidget.tk_color_opt.intersection(set(kw_in.keys())):
            if kw_in[key] in colors.keys():
                self.__updated_kwargs[key] = kw_in[key]
                kw_out[key] = self.get_color(kw_in[key])
        return kw_out

    @property
    def top_level(self):
        return self.winfo_toplevel()

    def get_color(self, name):
        return colors[name][0 if self.top_level.theme == "light" else 1]

    def get_updated_color(self, key, name):
        if key in self.__updated_kwargs:
            return self.get_color(self.__updated_kwargs[key])
        else:
            return self.get_color(name)

    @abstractmethod
    def update_theme(self):
        pass

    def pack(self, padx=5, pady=5, **kwargs):
        super().pack(padx=padx, pady=pady, **kwargs)
