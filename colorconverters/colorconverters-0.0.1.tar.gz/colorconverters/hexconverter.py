from utilities import *


def color_to_hex(color):
    try:
        if colors_to_hex.get(color) is None:
            return None
        else:
            return colors_to_hex[color]
    except:
        print("Returning hex from color failed!")


def hex_to_color(hex):
    if hex_to_colors.get(hex) is None:
        return None
    else:
        return hex_to_colors[hex]
