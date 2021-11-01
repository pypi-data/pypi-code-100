# This file is placed in the Public Domain.


import datetime
import json as js
import os
import pathlib
import uuid


def __dir__():
    return (
        "Object",
        "cdir",
        "gettype",
        "hook",
        "get",
        "keys",
        "items",
        "register",
        "set",
        "update",
        "values",
    )


def cdir(path):
    if os.path.exists(path):
        return
    if path.split(os.sep)[-1].count(":") == 2:
        path = os.path.dirname(path)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

def getwd():
    return Cfg.wd


def setwd(p):
    Cfg.wd = p

class NoPickle(Exception):

    pass


class Object:

    __slots__ = (
        "__dict__",
        "__stp__",
        "__otype__"
    )

    def __init__(self):
        super().__init__()
        self.__otype__ = str(type(self)).split()[-1][1:-2]
        self.__stp__ = os.path.join(
            self.__otype__,
            str(uuid.uuid4()),
            os.sep.join(str(datetime.datetime.now()).split()),
        )

    @staticmethod
    def __default__(o):
        if isinstance(o, Object):
            return vars(o)
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, list):
            return iter(o)
        if isinstance(o, (type(str), type(True), type(False), type(int), type(float))):
            return o
        if "__oqn__" in dir(o):
            return o.__oqn__(o)
        return repr(o)

    def __oqn__(self):
        return "<%s.%s object at %s>" % (
            self.__class__.__module__,
            self.__class__.__name__,
            hex(id(self)),
        )

    def __contains__(self, k):
        if k in keys(self):
            return True
        return False

    def __delitem__(self, k):
        if k in self:
            del self.__dict__[k]

    def __eq__(self, o):
        return len(self) == len(o)

    def __getitem__(self, k):
        return self.__dict__[k]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __le__(self, o):
        return len(self) <= len(o)

    def __lt__(self, o):
        return len(self) < len(o)

    def __ge__(self, o):
        return len(self) >= len(o)

    def __gt__(self, o):
        return len(self) > len(o)

    def __hash__(self):
        return id(self)

    def __hooked__(self, o):
        obj = Object()
        update(obj, o)
        return obj

    def __json__(self):
        s = js.dumps(self.__dict__, default=self.__default__, sort_keys=True)
        s = s.replace("'", '\\"')
        s = s.replace('"', "'")
        return s

    def __reduce__(self):
        raise NoPickle

    def __reduce_ex__(self, k):
        raise NoPickle

    def __setitem__(self, k, v):
        self.__dict__[k] = v

    def __repr__(self):
        return self.__json__()

    def __str__(self):
        return str(self.__dict__)


class Cfg(Object):

    wd  = ""

def get(self, key, default=None):
    return self.__dict__.get(key, default)


def keys(self):
    return self.__dict__.keys()


def items(self):
    try:
        return self.__dict__.items()
    except AttributeError:
        return self.items()


def register(self, k, v):
    self[str(k)] = v


def search(self, s):
    ok = False
    for k, v in items(s):
        vv = getattr(self, k, None)
        if v not in str(vv):
            ok = False
            break
        ok = True
    return ok


def set(self, key, value):
    self.__dict__[key] = value


def update(self, data):
    try:
        self.__dict__.update(vars(data))
    except TypeError:
        self.__dict__.update(data)
    return self


def values(self):
    return self.__dict__.values()


def oqn(self):
    return Object.__oqn__(self)


def register(self, k, v):
    self[str(k)] = v
