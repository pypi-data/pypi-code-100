# This file is placed in the Public Domain.

"list of listeners"


from .obj import Object


class BusError(Exception):

    """
        no matching listener found

        the origin of requester doesn't match the origin of any 
        registered listeners.

    """


class Bus(Object):

    """
        A Bus is a collection of listeners.
        
        The listener on this bus get's added onto a list when it's registered
        and starts receiving text messages post on the bus. Every listener is
        identifiable by a origin that is matched, making specific sending to a
        specifi listener possible. An announce on the bus will broadcast the
        text to all listeners.
        
        A Bus.say(orig, channel, txt) will display txt in the channel found
        on listener with the corresponding orig. If the orig is not known as 
        a listener the a BusError will be raised.

        Methods to select listeners based on orig, type and fd (filedescriptor)
        are available and iteration over the Bus with a iterator is also
        possible.
        
        Bus itself is stateless, it is not instantiated but accessed on class
        level e.g. the class itself holds state.
        
    """

    objs = []

    def __iter__(self):
        return iter(Bus.objs)

    @staticmethod
    def add(obj):
        if obj not in Bus.objs:
            Bus.objs.append(obj)

    @staticmethod
    def announce(txt):
        for h in Bus.objs:
            if "announce" in dir(h):
                h.announce(txt)

    @staticmethod
    def byorig(orig):
        for o in Bus.objs:
            if o.__oqn__() == orig:
                return o
        raise BusError(orig)

    @staticmethod
    def byfd(fd):
        for o in Bus.objs:
            if o.fd and o.fd == fd:
                return o
        return None

    @staticmethod
    def bytype(typ):
        for o in Bus.objs:
            if isinstance(o, typ):
                return o
        return None

    @staticmethod
    def first(otype=None):
        if Bus.objs:
            if not otype:
                return Bus.objs[0]
            for o in Bus.objs:
                if otype in str(type(o)):
                    return o
        return None

    @staticmethod
    def say(orig, channel, txt):
        for o in Bus.objs:
            if o.__oqn__() == orig:
                o.say(channel, txt)
