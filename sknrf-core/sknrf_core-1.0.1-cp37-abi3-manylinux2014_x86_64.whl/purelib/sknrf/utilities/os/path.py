import sys
import os
if sys.platform == "win32": import winshell


def realpath(path):
    if sys.platform == "win32":
        shortcut = winshell.Shortcut(path + ".lnk").path
        return shortcut if len(shortcut) else path
    else:
        return os.path.realpath(path)


def islink(path):
    if sys.platform == "win32":
        return bool(winshell.Shortcut(path).path)
    else:
        return os.path.realpath(path)
