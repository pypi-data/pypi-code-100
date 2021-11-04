from __future__ import print_function
import ctypes, sys


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def need_admin(filename):
    def func_de(func):
        if is_admin():
            def func_wrap(*args, **kwargs):
                func(*args,**kwargs);
            return func_wrap;
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, filename, None, 1);
    return func_de;









    