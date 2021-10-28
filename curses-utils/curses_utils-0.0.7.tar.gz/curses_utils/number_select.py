from .keys import get_next_key, is_pressed

def number_select(stdscr, title, num_range, start = None):
    """Pulls up a number selection menu.

stdscr:    The screen to write to.
title:     The title of the selection.
num_range: A range object for valid numbers.
start:     The starting selected number. Defaults to num_range's min value.

Returns the number selected, or None if the user chooses to quit."""
    if not isinstance(num_range, range):
        num_range = range(*num_range)
    selected = start or num_range.start
    stdscr.clear()
    while True:
        stdscr.addstr(0, 0, title)
        stdscr.addstr(1, 0, "^")
        stdscr.addstr(3, 0, "v")
        stdscr.addstr(2, 0, str(selected))
        get_next_key(stdscr)
        stdscr.clear()
        if is_pressed("menu_confirm"):
            return selected
        elif is_pressed("menu_cancel"):
            return
        elif is_pressed("menu_up") and \
          selected < (num_range.stop - 1):
            selected += 1
        elif is_pressed("menu_down") and \
          selected > num_range.start:
            selected -= 1