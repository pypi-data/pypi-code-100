import sys
import string
from .os import IS_WIN32


if IS_WIN32:
    import msvcrt
    _x00 = {
        b";": b"F1",
        b"<": b"F2",
        b"=": b"F3",
        b">": b"F4",
        b"?": b"F5",
        b"@": b"F6",
        b"A": b"F7",
        b"B": b"F8",
        b"C": b"F9",
        b"D": b"F10",
        b"^": b"CTRL_F1",
        b"_": b"CTRL_F2",
        b"`": b"CTRL_F3",
        b"a": b"CTRL_F4",
        b"b": b"CTRL_F5",
        b"c": b"CTRL_F6",
        b"d": b"CTRL_F7",
        b"e": b"CTRL_F8",
        b"f": b"CTRL_F9",
        b"g": b"CTRL_F10",
        b"\x03": b"CTRL_2",
        b"\x93": b"CTRL_NUMDOT",
        b"\x94": b"CTRL_SHIFT_TAB",
        b"u": b"CTRL_NUM1",
        b"\x91": b"CTRL_NUM2",
        b"v": b"CTRL_NUM3",
        b"s": b"CTRL_NUM4",
        b"t": b"CTRL_NUM6",
        b"w": b"CTRL_NUM7",
        b"\x8d": b"CTRL_NUM8",
        b"\x84": b"CTRL_NUM9",
        b"\x95": b"CTRL_NUMDIV",
    }
    _xe0 = {
        b"H": b"UP",
        b"P": b"DOWN",
        b"K": b"LEFT",
        b"M": b"RIGHT",
        b"R": b"INS",
        b"S": b"DEL",
        b"G": b"HOME",
        b"O": b"END",
        b"I": b"PGUP",
        b"Q": b"PGDN",
        b"\x85": b"F11",
        b"\x89": b"CTRL_F11",
        b"\x8a": b"CTRL_F12",
        b"\x92": b"CTRL_INS",
        b"\x93": b"CTRL_DEL",
        b"w": b"CTRL_HOME",
        b"u": b"CTRL_END",
        b"\x86": b"CTRL_PGUP",
        b"v": b"CTRL_PGDN",
        b"\x8d": b"CTRL_UP",
        b"\x91": b"CTRL_DOWN",
        b"s": b"CTRL_LEFT",
        b"t": b"CTRL_RIGHT",
    }
    SPECIAL = {
        b"\t": b"TAB",
        b"\r": b"ENTER",
        b"\n": b"CTRL_ENTER",
        b"\x1b": b"ESC",
        b"\x08": b"BACKSPACE",
        b"\x7f": b"CTRL_BACKSPACE",
        b"\x1c": b"FILE_SEP",
        b"\x1d": b"GRP_SEP",
        b"\x1E": b"RCD_SEP",
        b"\x1F": b"UNIT_SEP",
    }


    def getch():
        char = msvcrt.getch()
        if char == b"\xe0":
            char2 = msvcrt.getch()
            try:
                return _xe0[char2]
            except:
                return char+char2
        if char == b"\x00":
            char2 = msvcrt.getch()
            try:
                return _x00[char2]
            except:
                return char+char2
        if char in SPECIAL:
            return SPECIAL[char]
        if char[0] in range(1, 26+1):
            return b"CTRL_"+bytes([65-1+char[0]])
        return char
else:
    import tty
    import termios


    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        char = None
        try:
            tty.setraw(fd)
            char = sys.stdin.read(1)
        except Exception as e:
            raise e
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return char


    def getch():
        char = _getch()

        return char


def getpw(prompt: str = "Enter password: "):
    print(prompt, end="", flush=True)
    pw = []
    while True:
        char = getch()
        if char == b"CTRL_C":
            return
        elif char == b"BACKSPACE" and pw:
            pw.pop()
            continue
        elif char == b"ENTER":
            return "".join(pw)
        if len(char) == 1 and char.decode() in string.printable:
            pw.append(char.decode())


