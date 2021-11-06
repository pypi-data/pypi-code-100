import tkinter as tk

from abc import ABC, abstractmethod
from typing import Dict, Union

from .color import colors, get_color


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

    def get_color(self, name):
        return get_color(name, self.winfo_toplevel())

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


class ThemedWindow(ThemedWidget, tk.Wm):

    def __init__(self):
        self.__theme_updated_id = None
        self.bind('<Configure>', self.on_configure)
        self.after(10, self.update_theme)

    def center(self):
        self.after(10, self.__move_to_center_of_screen)

    def __move_to_center_of_screen(self):
        self.update_idletasks()
        # We use double slash '//' to make a integer division
        x = self.winfo_screenwidth() // 2 - self.width // 2
        y = self.winfo_screenheight() // 2 - self.height // 2
        self.geometry(f"{self.winfo_width()}x{self.winfo_height()}+{x}+{y}")

    def on_configure(self, event):
        if event.widget == self:
            if self.__theme_updated_id is not None:
                self.after_cancel(self.__theme_updated_id)
            self.__theme_updated_id = self.after(500, self.update_theme)

    def update_theme(self):
        self.config(bg=self.get_color('main_bg'))
        for child in self.children.values():
            if isinstance(child, ThemedWidget):
                child.update_theme()
        self.__theme_updated_id = None

    @property
    def frame_size(self):
        return self.winfo_rootx() - self.winfo_x()

    @property
    def titlebar_height(self):
        return self.winfo_rooty() - self.winfo_y()

    @property
    def width(self):
        return self.winfo_width() + 2 * self.frame_size

    @property
    def height(self):
        return self.winfo_height() + self.titlebar_height + self.frame_size
