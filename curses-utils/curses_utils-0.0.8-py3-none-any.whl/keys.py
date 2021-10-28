import curses

__keys = {}

def set_key_codes(key_name, key_codes):
    """Sets a key's function by name.

key_name:  The key name to set.
key_codes: A collection of key codes (as returned by stdscr.getkey()) to use.

Make sure to set keys before using them!
Internally, CursesUtils uses the following keys:
* menu_up (for navigating UP through menus)
* menu_down (for navigating DOWN through menus)
* menu_confirm (for CONFIRMING on menus)
* menu_cancel (for QUITTING on menus)"""
    __keys[key_name] = list(key_codes)

def get_key_codes(key_name):
    """Gets a key's codes by name.

key_name: The key name to get the codes of.

Returns the key codes of the given key, or None if it doesn't exist. See set_key_codes for more information."""
    return __keys.get(key_name)

__current_key = None

def get_next_key(stdscr):
    """Gets the next key and saves it.

stdscr: The screen to write to."""
    global __current_key
    __current_key = stdscr.getkey()

def get_current_key():
    """Gets the current pressed key."""
    return __current_key

def get_key_with_timeout(stdscr, timeout):
    """Waits for a timeout, returning immediately on a key. Saves the key, saving None if no key was pressed.

stdscr:  The screen to write to.
timeout: The timeout in milliseconds."""
    global __current_key
    stdscr.timeout(timeout)
    key = stdscr.getch()
    if key == -1:
        __current_key = None
    else:
        curses.ungetch(key)
        get_next_key()
    stdscr.timeout(-1)

def is_pressed(key_name):
    """Checks if the given key is the current pressed key by name.

key_name: The key name to check."""
    return get_current_key() in get_key_codes(key_name)