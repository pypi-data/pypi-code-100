import sys
import string
from .sos import IS_WIN32


class _KEYS:
    A = b"A"
    B = b"B"
    C = b"C"
    D = b"D"
    E = b"E"
    F = b"F"
    G = b"G"
    H = b"H"
    I = b"I"
    J = b"J"
    K = b"K"
    L = b"L"
    M = b"M"
    N = b"N"
    O = b"O"
    P = b"P"
    Q = b"Q"
    R = b"R"
    S = b"S"
    T = b"T"
    U = b"U"
    V = b"V"
    W = b"W"
    Y = b"Y"
    X = b"X"
    Z = b"Z"
    a = b"a"
    b = b"b"
    c = b"c"
    d = b"d"
    e = b"e"
    f = b"f"
    g = b"g"
    h = b"h"
    i = b"i"
    j = b"j"
    k = b"k"
    l = b"l"
    m = b"m"
    n = b"n"
    o = b"o"
    p = b"p"
    q = b"q"
    r = b"r"
    s = b"s"
    t = b"t"
    u = b"u"
    v = b"v"
    w = b"w"
    y = b"y"
    x = b"x"
    z = b"z"


if IS_WIN32:
    import msvcrt


    class KEYS(_KEYS):
        F1 = b"F1"
        F2 = b"F2"
        F3 = b"F3"
        F4 = b"F4"
        F5 = b"F5"
        F6 = b"F6"
        F7 = b"F7"
        F8 = b"F8"
        F9 = b"F9"
        F10 = b"F10"
        F11 = b"F11"
        CTRL_2 = b"CTRL_2"
        CTRL_A = b"CTRL_A"
        CTRL_B = b"CTRL_B"
        CTRL_C = b"CTRL_C"
        CTRL_D = b"CTRL_D"
        CTRL_E = b"CTRL_E"
        CTRL_F = b"CTRL_F"
        CTRL_G = b"CTRL_G"
        CTRL_K = b"CTRL_K"
        CTRL_L = b"CTRL_L"
        CTRL_N = b"CTRL_N"
        CTRL_O = b"CTRL_O"
        CTRL_P = b"CTRL_P"
        CTRL_Q = b"CTRL_Q"
        CTRL_R = b"CTRL_R"
        CTRL_S = b"CTRL_S"
        CTRL_T = b"CTRL_T"
        CTRL_U = b"CTRL_U"
        CTRL_V = b"CTRL_V"
        CTRL_W = b"CTRL_W"
        CTRL_Y = b"CTRL_Y"
        CTRL_X = b"CTRL_X"
        CTRL_Z = b"CTRL_Z"
        CTRL_F1 = b"CTRL_F1"
        CTRL_F2 = b"CTRL_F2"
        CTRL_F3 = b"CTRL_F3"
        CTRL_F4 = b"CTRL_F4"
        CTRL_F5 = b"CTRL_F5"
        CTRL_F6 = b"CTRL_F6"
        CTRL_F7 = b"CTRL_F7"
        CTRL_F8 = b"CTRL_F8"
        CTRL_F9 = b"CTRL_F9"
        CTRL_F10 = b"CTRL_F10"
        CTRL_F11 = b"CTRL_F11"
        CTRL_F12 = b"CTRL_F12"
        CTRL_NUMDOT = b"CTRL_NUMDOT"
        CTRL_SHIFT_TAB = b"CTRL_SHIFT_TAB"
        CTRL_NUM1 = b"CTRL_NUM1"
        CTRL_NUM2 = b"CTRL_NUM2"
        CTRL_NUM3 = b"CTRL_NUM3"
        CTRL_NUM4 = b"CTRL_NUM4"
        CTRL_NUM6 = b"CTRL_NUM6"
        CTRL_NUM7 = b"CTRL_NUM7"
        CTRL_NUM8 = b"CTRL_NUM8"
        CTRL_NUM9 = b"CTRL_NUM9"
        CTRL_NUMDIV = b"CTRL_NUMDIV"
        UP = b"UP"
        DOWN = b"DOWN"
        LEFT = b"LEFT"
        RIGHT = b"RIGHT"
        INS = b"INS"
        DEL = b"DEL"
        HOME = b"HOME"
        END = b"END"
        PGUP = b"PGUP"
        PGDN = b"PGDN"
        CTRL_INS = b"CTRL_INS"
        CTRL_DEL = b"CTRL_DEL"
        CTRL_HOME = b"CTRL_HOME"
        CTRL_END = b"CTRL_END"
        CTRL_PGUP = b"CTRL_PGUP"
        CTRL_PGDN = b"CTRL_PGDN"
        CTRL_UP = b"CTRL_UP"
        CTRL_DOWN = b"CTRL_DOWN"
        CTRL_LEFT = b"CTRL_LEFT"
        CTRL_RIGHT = b"CTRL_RIGHT"
        TAB = b"TAB"
        ENTER = b"ENTER"
        CTRL_ENTER = b"CTRL_ENTER"
        ESC = b"ESC"
        BACKSPACE = b"BACKSPACE"
        CTRL_BACKSPACE = b"CTRL_BACKSPACE"
        FILE_SEP = b"FILE_SEP"
        GRP_SEP = b"GRP_SEP"
        RCD_SEP = b"RCD_SEP"
        UNIT_SEP = b"UNIT_SEP"


    map_x00 = {
        b";": KEYS.F1,
        b"<": KEYS.F2,
        b"=": KEYS.F3,
        b">": KEYS.F4,
        b"?": KEYS.F5,
        b"@": KEYS.F6,
        b"A": KEYS.F7,
        b"B": KEYS.F8,
        b"C": KEYS.F9,
        b"D": KEYS.F10,
        b"^": KEYS.CTRL_F1,
        b"_": KEYS.CTRL_F2,
        b"`": KEYS.CTRL_F3,
        b"a": KEYS.CTRL_F4,
        b"b": KEYS.CTRL_F5,
        b"c": KEYS.CTRL_F6,
        b"d": KEYS.CTRL_F7,
        b"e": KEYS.CTRL_F8,
        b"f": KEYS.CTRL_F9,
        b"g": KEYS.CTRL_F10,
        b"\x03": KEYS.CTRL_2,
        b"\x93": KEYS.CTRL_NUMDOT,
        b"\x94": KEYS.CTRL_SHIFT_TAB,
        b"u": KEYS.CTRL_NUM1,
        b"\x91": KEYS.CTRL_NUM2,
        b"v": KEYS.CTRL_NUM3,
        b"s": KEYS.CTRL_NUM4,
        b"t": KEYS.CTRL_NUM6,
        b"w": KEYS.CTRL_NUM7,
        b"\x8d": KEYS.CTRL_NUM8,
        b"\x84": KEYS.CTRL_NUM9,
        b"\x95": KEYS.CTRL_NUMDIV,
    }
    map_xe0 = {
        b"H": KEYS.UP,
        b"P": KEYS.DOWN,
        b"K": KEYS.LEFT,
        b"M": KEYS.RIGHT,
        b"R": KEYS.INS,
        b"S": KEYS.DEL,
        b"G": KEYS.HOME,
        b"O": KEYS.END,
        b"I": KEYS.PGUP,
        b"Q": KEYS.PGDN,
        b"\x85": KEYS.F11,
        b"\x89": KEYS.CTRL_F11,
        b"\x8a": KEYS.CTRL_F12,
        b"\x92": KEYS.CTRL_INS,
        b"\x93": KEYS.CTRL_DEL,
        b"w": KEYS.CTRL_HOME,
        b"u": KEYS.CTRL_END,
        b"\x86": KEYS.CTRL_PGUP,
        b"v": KEYS.CTRL_PGDN,
        b"\x8d": KEYS.CTRL_UP,
        b"\x91": KEYS.CTRL_DOWN,
        b"s": KEYS.CTRL_LEFT,
        b"t": KEYS.CTRL_RIGHT,
    }
    map = {
        b"\t": KEYS.TAB,
        b"\r": KEYS.ENTER,
        b"\n": KEYS.CTRL_ENTER,
        b"\x1b": KEYS.ESC,
        b"\x08": KEYS.BACKSPACE,
        b"\x7f": KEYS.CTRL_BACKSPACE,
        b"\x1c": KEYS.FILE_SEP,
        b"\x1d": KEYS.GRP_SEP,
        b"\x1E": KEYS.RCD_SEP,
        b"\x1F": KEYS.UNIT_SEP,
    }


    def getch():
        char = msvcrt.getch()
        if char == b"\xe0":
            char2 = msvcrt.getch()
            try:
                return map_xe0[char2]
            except:
                return char+char2
        if char == b"\x00":
            char2 = msvcrt.getch()
            try:
                return map_x00[char2]
            except:
                return char+char2
        if char in map:
            return map[char]
        if char[0] in range(1, 26+1):
            return b"CTRL_"+bytes([65-1+char[0]])
        return char
else:
    import tty
    import termios


    class KEYS(_KEYS):
        ...


    map_x1b = {
        b"O": {
            b"P": KEYS.F1,
            b"Q": KEYS.F2,
            b"R": KEYS.F3,
            b"S": KEYS.F4,
        },
        b"[1": KEYS.F5,
        b"[2": KEYS.F9,
        b"^": KEYS.CTRL_F1,
        b"_": KEYS.CTRL_F2,
        b"`": KEYS.CTRL_F3,
        b"a": KEYS.CTRL_F4,
        b"b": KEYS.CTRL_F5,
        b"c": KEYS.CTRL_F6,
        b"d": KEYS.CTRL_F7,
        b"e": KEYS.CTRL_F8,
        b"f": KEYS.CTRL_F9,
        b"g": KEYS.CTRL_F10,
        b"\x03": KEYS.CTRL_2,
        b"\x93": KEYS.CTRL_NUMDOT,
        b"\x94": KEYS.CTRL_SHIFT_TAB,
        b"u": KEYS.CTRL_NUM1,
        b"\x91": KEYS.CTRL_NUM2,
        b"v": KEYS.CTRL_NUM3,
        b"s": KEYS.CTRL_NUM4,
        b"t": KEYS.CTRL_NUM6,
        b"w": KEYS.CTRL_NUM7,
        b"\x8d": KEYS.CTRL_NUM8,
        b"\x84": KEYS.CTRL_NUM9,
        b"\x95": KEYS.CTRL_NUMDIV,
    }


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
            if isinstance(char, str):
                return char.encode()
            else:
                return char


    def getch():
        char = _getch()
        if char == b"\x1b":
            char2 = _getch()
            if char2 == b"O":
                char3 = _getch()
                try:
                    return map_x1b[char2][char3]
                except:
                    return char+char2
            elif char2 == b"[":
                char3 = _getch()
                if char3 == b"1":
                    char4 = _getch()
        return char


def getpw(prompt: str = "Enter password: "):
    print(prompt, end="", flush=True)
    pw = []
    while True:
        char = getch()
        if char == KEYS.CTRL_C:
            return
        elif char == KEYS.BACKSPACE and pw:
            pw.pop()
            continue
        elif char == KEYS.ENTER:
            return "".join(pw)
        if len(char) == 1 and char.decode() in string.printable:
            pw.append(char.decode())


