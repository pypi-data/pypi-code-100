#Beetroot, a general purpose library for all sorts of uses.

#Imports
import sys

from .exception import *

if not str(sys.version).startswith("3"):
    #HOW DARE YOU USE PYTHON2 IDIOT. or python4, if that ever exists
    #well I mean, if it's like a massive database or smth and you don't wanna migrate 1k+ lines of code then I understand, BUT STILL.
    #And if you're using Python1, then the following emoji is for you. 😲
    raise VersionError("Python version is not supported.")

#More imports
import platform
import getpass
import socket
import uuid
import hashlib
import webbrowser
import datetime
import os
    
try:
    import PIL
    
except (ModuleNotFoundError, ImportError):
    pass

try:
    import pyautogui
    
except (ModuleNotFoundError, ImportError):
    pass

try:
    import psutil
    
except (ModuleNotFoundError, ImportError):
    pass

from pathlib import Path as p

from .metadata import *
from .random import *
from .stopwatch import *
from .file import *
from .tts import *
from .objtype import *
from .obf import *
from .mem import *
from .yt import *
from .hashl import *
from .text import *

#Constants
gen = mrandom.SystemRandom()
sys.setrecursionlimit(32767)
        
def test():
    """Test"""
    print("Hello, world!")
    return 0

def remove(str_, ting):
    """Removes all occurences of "ting" in str_"""
    return str_.replace(str(ting), "")

def siteize(str_):
    """Turns the string into a malformed url so you can talk
    in a weird way. For example, "Hello, world!", gets
    turned into "www.HelloWorld.com"."""
    a = list(str_)
    b = []
    
    for item in a:
        if item.isalnum() or item == " ":
            b.append(item)
            
    b = remove("".join(b).title(), " ")
    return "".join(["www.", b, ".com"])
    
def taskkill(tasque):
    """Kills a task by name with psutil."""
    try:
        for proc in psutil.process_iter():
            if proc.name() == tasque:
                proc.kill()
                
    except NameError:
        raise ModuleError("psutil must be installed to use beetroot.taskkill(). Use pip install psutil or pip install beetroot[ram].")
    
def crash():
    """This causes python to cra- cra- cra- cras- cra- crash."""
    try:
        taskkill(os.path.basename(sys.executable))
                
    except NameError:
        raise ModuleError("psutil must be installed to use beetroot.crash(). Use pip install psutil or pip install beetroot[ram].")
    
def quicksort(array):
    """Quicksort algorithm"""

    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0]
        
        for x in array:
            if x < pivot:
                less.append(x)
                
            elif x == pivot:
                equal.append(x)
                
            elif x > pivot:
                greater.append(x)
                
        return quicksort(less) + equal + quicksort(greater)
    
    else:
        return array

def lsep(str_, sep=" "):
    """Seperates string str_ by seperator sep whilst avoiding all strings containing whitespace"""
    a = str_.split(sep)
    
    out = []
    for i in range(0, len(a)):
        if (not a[i].isspace()) and a[i] != "":
            out.append(a[i])
            
    return out

def execfile(file):
    """Executes a python .py script"""
    with open(p(file), "r", encoding="iso-8859-1") as f:
        exec(f.read())
        f.close()
        
    return 0

def systemstats():
    """Returns info about system and hardware"""
    return [getpass.getuser(), platform.system(), platform.version(), platform.machine(), platform.node(), socket.gethostbyname(socket.gethostname()), ':'.join(("%012X" % uuid.getnode())[i:i+2] for i in range(0, 12, 2)).lower()]

def unline(str_):
    """Makes multi-line strings single-line"""
    return str(str_).replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r").replace("\a", "\\a").replace("\b", "\\b")

def reline(str_):
    """Reverses beetroot.unline()"""
    return str(str_).replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r").replace("\\a", "\a").replace("\\b", "\b")

def pixelgrab(i_x, i_y):
    try:
        import PIL.ImageGrab
        return PIL.ImageGrab.grab().load()[int(i_x), int(i_y)]
    
    except (ModuleNotFoundError, ImportError):
        raise ModuleError("PIL most be installed to use beetroot.pixelgrab(). Try pip install pillow.")
    
    except ValueError:
        raise InvalidTypeError("Arguement \"i_x\" and \"i_y\" must be ints or floats")
    
def mousepixelgrab():
    try:
        import PIL.ImageGrab
        import pyautogui
        
        pos = pyautogui.position()
        return PIL.ImageGrab.grab().load()[pos.x, pos.y]

    except (ModuleNotFoundError, ImportError):
        raise ModuleError("PIL and pyautogui most be installed to use beetroot.mousepixelgrab(). Try pip install pillow pyautogui.")
    
def beetroot():
    """BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT-"""
    while True:
        get_beetrolled = True
        print("""

██████╗░███████╗███████╗████████╗██████╗░░█████╗░░█████╗░████████╗
██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝
██████╦╝█████╗░░█████╗░░░░░██║░░░██████╔╝██║░░██║██║░░██║░░░██║░░░
██╔══██╗██╔══╝░░██╔══╝░░░░░██║░░░██╔══██╗██║░░██║██║░░██║░░░██║░░░
██████╦╝███████╗███████╗░░░██║░░░██║░░██║╚█████╔╝╚█████╔╝░░░██║░░░
╚═════╝░╚══════╝╚══════╝░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░░╚════╝░░░░╚═╝░░░""", end="", flush=True)
        time.sleep(0.5)
        
    return 69420

def totally_not_a_rickroll():
    for i in range(0, 100):
        rickrolled = True
        
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ", new=0)
    return "".join(["U JUST GOT RICKROLLED IN ", str(datetime.datetime.now().year)])