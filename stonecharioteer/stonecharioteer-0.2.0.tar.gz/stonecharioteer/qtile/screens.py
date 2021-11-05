"""This module configures the monitors depending on how many displays
there are. To properly use it, you need to create a config file in
~/.config/stonecharioteer/monitors.toml, note that that file will
need to list the IDs of your monitors, getting them from `xrandr`
so that this code can properly configure them. Alternatively, you can
overrride the location of the monitors config file using the
`STONECHARIOTEER_MONITORS` environment variable, which should
point to the *absolute* path of a toml file."""

import pathlib
import os
import toml

from libqtile.config import Screen
from stonecharioteer.qtile.panels import default_top_bar, default_bottom_bar

def configure_screens():
    """This function configures the screens based on how many active
    monitors there are currently."""
    if monitors_config := os.environ.get("STONECHARIOTEER_MONITORS"):
        monitors_config = pathlib.Path(monitors_config)
    else:
        monitors_config = pathlib.Path("~/.config/stonecharioteer/monitors.toml")
    if monitors_config.is_file():
        with open(monitors_config) as f:
            monitor_config = toml.load(f)
        # TODO: implement behavior for multi monitor configuration 
    
    default_screen = Screen(
            top = default_top_bar,
            bottom= default_bottom_bar,
            )
    screens = [
        default_screen
    ]
    return screens
