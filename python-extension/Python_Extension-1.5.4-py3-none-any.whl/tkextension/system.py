# -*- coding: utf-8  -*-

from pyextension import *

def opensource(module='tkextension'):
    if module == 'tkextension' or module == '__init__':
        file = open('__init__.py')
        get = file.read()
        file.close()
        return get
    elif module == 'blackboard index' or module == 'blackboard_index':
        file = open('blackboard.py')
        get = file.read()
        file.close()
        return get
    elif module == 'test':
        file = open('test.py')
        get = file.read()
        file.close()
        return get
    elif module == 'timer index' or module == 'timer_index':
        file = open('timer.py')
        get = file.read()
        file.close()
        return get
    elif module == 'tix':
        file = open('tix/__init__.py')
        get = file.read()
        file.close()
        return get
    elif module == 'tix.blackboard' or module == 'blackboard':
        file = open('tix/blackboard.py')
        get = file.read()
        file.close()
        return get
    elif module == 'tix.dialog' or module == 'dialog':
        file = open('tix/dialog.py')
        get = file.read()
        file.close()
        return get
    elif module == 'tix.dialog index' or module == 'dialog index' or module == 'tix.dialog_index' or module == 'dialog_index':
        file = open('tix/dialog.py')
        get = file.read()
        file.close()
        return get
    elif module == 'tix.filedialog' or module == 'filedialog':
        file = open('tix/filedialog.py')
        get = file.read()
        file.close()
        return get
    elif module == 'tix.timer' or module == 'timer':
        file = open('tix/timer.py')
        get = file.read()
        file.close()
        return get
    elif module == 'turtledrawer':
        file = open('turtledrawer.py')
        get = file.read()
        file.close()
        return get
    elif module == 'system':
        file = open('system.py')
        get = file.read()
        file.close()
        return get
    else:
        raise AttributeError('\'opensource\' object has no attribute \'%s\'' % module)
