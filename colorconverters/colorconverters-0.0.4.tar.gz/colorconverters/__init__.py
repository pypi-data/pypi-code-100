colors_to_hex = {
    "bright_red": "#FF0000",
    "bright_blue": "#0000FF",
    "bright_green": "#00FF00"
}

hex_to_colors = {
    "#FF0000": "bright_red",
    "#0000FF": "bright_blue",
    "#00FF00": "bright_green"
}

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