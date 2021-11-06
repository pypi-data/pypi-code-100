import inspect
from typing import Callable
from datetime import datetime

class Event:
    def __init__(self, name: str, func: Callable):
        self.name = name
        self.func = func

class Command:
    def __init__(self, name: str, func: Callable, _type: int):
        self.name = name
        self.func = func
        self.type = _type

class Component:
    def __init__(self, ucid, func: Callable, parent_context, timeout: float = 0.0):
        self.ucid = ucid
        self.func = func
        self.parent_context = parent_context
        
        if timeout > 0.0:
            self.timeout = datetime.fromtimestamp((datetime.utcnow() - datetime.fromtimestamp(0)).total_seconds() + timeout)
        else:
            self.timeout = None
    
def event(name):
    def predicate(func):
        if not inspect.iscoroutinefunction(func):
            raise TypeError("Event decorator can only be applied to coroutine functions")
        return Event(name, func)
    return predicate

def command(name, _type):
    def predicate(func):
        if not inspect.iscoroutinefunction(func):
            raise TypeError("Command decorator can only be applied to coroutine functions")
        return Command(name, func, _type)
    return predicate