import tkinter as tk

from .typing import ScreenRegion


def color_is_light(color):
    # Remove the heading '#'
    color = color[1:]
    # Get the length of the composite color
    length = int(len(color) / 3)
    # We get the red, green and blue component and recalculate them on the base of 255
    red = int(color[0:length], 16) / ((16 ** length) - 1) * 255
    green = int(color[length: 2 * length], 16) / ((16 ** length) - 1) * 255
    blue = int(color[2 * length: 3 * length], 16) / ((16 ** length) - 1) * 255
    # It exist many way to compute the brightness of a color the one under have good result
    # brightness = ((red * 299) + (green * 587) + (blue * 114)) / 1000
    brightness = 0.2126 * red + 0.7152 * green + 0.0722 * blue
    return brightness > 118


def get_widget_region(widget: tk.Misc) -> ScreenRegion:
    """
    Gets x-coordinate, y-coordinate, width and height of the tkinter test_widget
    :param  widget:

    :return:
    """

    widget.update()

    x = widget.winfo_rootx()
    y = widget.winfo_rooty()
    width = widget.winfo_width()
    height = widget.winfo_height()

    return ScreenRegion(x, y, width, height)


def get_window_region(widget: tk.Misc) -> ScreenRegion:
    """
    Gets x-coordinate, y-coordinate, width and height of the tkinter test_widget
    :param  widget:

    :return:
    """

    widget.update()
    parent = widget.nametowidget(widget.winfo_parent())

    x = parent.winfo_rootx()
    y = parent.winfo_rooty()
    width = parent.winfo_width()
    height = parent.winfo_height()

    return ScreenRegion(x, y, width, height)
