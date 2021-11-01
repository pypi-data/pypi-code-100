import ctypes
from typing import Final

# _STD_INPUT_HANDLE: Final = -10
_STD_OUTPUT_HANDLE: Final = -11
# _STD_ERROR_HANDLE: Final = -12

# 字体颜色定义 ,关键在于颜色编码，由2位十六进制组成，分别取0~f，前一位指的是背景色，后一位指的是字体色
# 由于该函数的限制，应该是只有这16种，可以前景色与背景色组合。也可以几种颜色通过或运算组合，组合后还是在这16种颜色中

# Windows CMD命令行 字体颜色定义 text colors
FOREGROUND_BLACK: Final = 0x00
FOREGROUND_DARKBLUE: Final = 0x01
FOREGROUND_DARKGREEN: Final = 0x02
FOREGROUND_DARKSKYBLUE: Final = 0x03
FOREGROUND_DARKRED: Final = 0x04
FOREGROUND_DARKPINK: Final = 0x05
FOREGROUND_DARKYELLOW: Final = 0x06
FOREGROUND_DARKWHITE: Final = 0x07
FOREGROUND_DARKGRAY: Final = 0x08
FOREGROUND_BLUE: Final = 0x09
FOREGROUND_GREEN: Final = 0x0A
FOREGROUND_SKYBLUE: Final = 0x0B
FOREGROUND_RED: Final = 0x0C
FOREGROUND_PINK: Final = 0x0D
FOREGROUND_YELLOW: Final = 0x0E
FOREGROUND_WHITE: Final = 0x0F

# Windows CMD命令行 背景颜色定义 background colors
BACKGROUND_BLACK: Final = 0x10
BACKGROUND_DARKGREEN: Final = 0x20
BACKGROUND_DARKSKYBLUE: Final = 0x30
BACKGROUND_DARKRED: Final = 0x40
BACKGROUND_DARKPINK: Final = 0x50
BACKGROUND_DARKYELLOW: Final = 0x60
BACKGROUND_DARKWHITE: Final = 0x70
BACKGROUND_DARKGRAY: Final = 0x80
BACKGROUND_BLUE: Final = 0x90
BACKGROUND_GREEN: Final = 0xA0
BACKGROUND_SKYBLUE: Final = 0xB0
BACKGROUND_RED: Final = 0xC0
BACKGROUND_PINK: Final = 0xD0
BACKGROUND_YELLOW: Final = 0xE0
BACKGROUND_WHITE: Final = 0xF0

# get handle
_stdOutHandle = ctypes.windll.kernel32.GetStdHandle(_STD_OUTPUT_HANDLE)


def setPrintColor(color: int, handle: int = _stdOutHandle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool


# reset white
def resetPrintColor():
    setPrintColor(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)
