from .keys import get_next_key, is_pressed

def menu(stdscr, title, options):
    """Pulls up a select menu.

stdscr:  The screen to write to.
title:   The title of the menu.
options: A collection of strings to choose from.

Returns the index of the selected item, or None if the user chooses to quit."""
    selected = 0
    stdscr.clear()
    while True:
        stdscr.addstr(0, 0, title)
        for i, option in enumerate(options):
            stdscr.addstr(i+1, 2, option)
        stdscr.addstr(selected + 1, 0, ">")
        get_next_key(stdscr)
        stdscr.clear()
        if is_pressed("menu_confirm"):
            return selected
        elif is_pressed("menu_cancel"):
            return
        elif is_pressed("menu_up"):
            selected -= 1
        elif is_pressed("menu_down"):
            selected += 1
        selected %= len(options)