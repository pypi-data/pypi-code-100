import tkinter as tk

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .abs_class import ThemedWidget


colors = {
    'main_bg':     ("#DDD", "#222"),
    'light_bg':    ("#CCC", "#333"),
    'dark_bg':     ("#EEE", "#111"),
    'main_text':   ("#222", "#DDD"),
    'light_text':  ("#333", "#CCC"),
    'dark_text':   ("#111", "#EEE"),
    'primary':     ("#6666EE", "#6666EE"),
    'white':       ("#DDD", "#DDD"),
    'black':       ("#222", "#222"),
    'red':         ("#E81123", "#E81123"),
    'green':       ("#06B025", "#06B025"),
    'blue':        ("#429CE3", "#429CE3"),
    'cyan':        ("#6FDAE6", "#6FDAE6"),
    'yellow':      ("#FFE78F", "#FFE78F"),
    'magenta':     ("#E62EC0", "#E62EC0")
}

tk_instances = set()


def add_tk_instance(instance: tk.Tk):
    tk_instances.add(instance)


def get_color(name: str, widget: 'ThemedWidget' = None):
    name = name.lower()
    tk_instance = None
    if widget is not None:
        tk_instance = widget.winfo_toplevel()
    elif len(tk_instances) == 1:
        tk_instance = next(iter(tk_instances))

    if tk_instance is None:
        return colors[name][0]
    else:
        return colors[name][1 if tk_instance.theme == "dark" else 0]
