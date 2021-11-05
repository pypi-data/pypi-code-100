"""Holds all the bars"""
from libqtile.widget import (
        Battery,
        CPUGraph,
        CapsNumLockIndicator,
        Clock,
        CurrentLayout,
        GroupBox,
        HDDGraph,
        MemoryGraph,
        Net,
        Prompt,
        QuickExit,
        Spacer,
        Systray,
        WindowName,
        )

from libqtile.bar import Bar, STRETCH

# TODO: Modularize and create a constructor function
current_layout = CurrentLayout()
group_box = GroupBox()
prompt_widget = Prompt()
window_name = WindowName()
clock_widget = Clock(format='%Y-%m-%d %a %I:%M %p')
system_tray = Systray()
quick_exit = QuickExit()
capslock_numlock_indicator = CapsNumLockIndicator()
cpu_indicator = CPUGraph()
memory_indicator = MemoryGraph()
hdd_indicator = HDDGraph()

# TODO: Only add this if this is a laptop, control through config.
battery_indicator = Battery()
network_indicator = Net()
spacer = Spacer(length=STRETCH)

default_size = 24
default_top_bar = Bar([
    current_layout,
    prompt_widget,
    spacer,
    cpu_indicator,
    memory_indicator,
    hdd_indicator,
    system_tray,
    network_indicator,
    capslock_numlock_indicator,

    ], default_size)
default_bottom_bar = Bar([
    group_box,
    window_name,
    clock_widget,
    battery_indicator,
    quick_exit,
    ], default_size)
