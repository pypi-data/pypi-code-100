# This file is placed in the Public Domain.


import inspect


from .obj import Object


class Table(Object):

    classes = Object()
    modnames = Object()
    names = Object()

    @staticmethod
    def add(func):
        n = func.__name__
        Table.modnames[n] = func.__module__

    @staticmethod
    def addcls(clz):
        Table.classes[clz.__name__] = clz
        name = clz.__name__.lower()
        if name not in Table.names:
            Table.names[name] = []
        Table.names[name].append("%s.%s" % (clz.__module__, clz.__name__))

    @staticmethod
    def addmod(mod):
        Table.introspect(mod)

    @staticmethod
    def introspect(mod):
        for _k, o in inspect.getmembers(mod, inspect.isfunction):
            if o.__code__.co_argcount == 1 and "event" in o.__code__.co_varnames:
                Table.add(o)
        for _k, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, Object):
                Table.addcls(o)
