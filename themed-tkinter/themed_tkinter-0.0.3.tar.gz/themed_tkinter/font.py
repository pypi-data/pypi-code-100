import tkinter as tk

from tkinter.font import Font

__fonts = {}


def build_all_font(root: tk.Tk):
    build_font(root, 'themed_default', 'Courier', 12)


def build_font(root: tk.Tk, name, family, size, weight='normal', slant='roman', underline=0, overstrike=0):
    __fonts[name] = Font(root=root,
                         name=name,
                         family=family,
                         size=size,
                         weight=weight,
                         slant=slant,
                         underline=underline,
                         overstrike=overstrike)
