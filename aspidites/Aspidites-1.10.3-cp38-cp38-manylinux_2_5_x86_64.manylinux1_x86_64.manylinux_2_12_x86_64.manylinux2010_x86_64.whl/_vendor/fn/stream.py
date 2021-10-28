#cython: language_level=3, annotation_typing=True, c_string_encoding=utf-8, boundscheck=False, wraparound=False, initializedcheck=False
from itertools import chain
from sys import maxsize as maxint


class Stream(object):

    __slots__ = ("_last", "_collection", "_origin")

    class _StreamIterator(object):

        __slots__ = ("_stream", "_position")

        def __init__(self, stream):
            self._stream = stream
            self._position = - 1  # not started yet

        def __next__(self):
            # check if elements are available for next position
            # return next element or raise StopIteration
            self._position += 1

            col_pos = len(self._stream._collection) > self._position
            if col_pos or self._stream._fill_to(self._position):
                return self._stream._collection[self._position]

            raise StopIteration()

    def __init__(self, *origin):
        self._collection = []
        self._last = - 1  # not started yet
        self._origin = iter(origin) if origin else []

    def __lshift__(self, rvalue):
        iterator = rvalue() if callable(rvalue) else rvalue
        self._origin = chain(self._origin, iterator)
        return self

    def cursor(self):
        """Return position of next evaluated element"""
        return self._last + 1

    def _fill_to(self, index):
        if self._last >= index:
            return True

        while self._last < index:
            try:
                n = next(self._origin)
            except StopIteration:
                return False

            self._last += 1
            self._collection.append(n)

        return True

    def __iter__(self):
        return self._StreamIterator(self)

    def __getitem__(self, index):
        if isinstance(index, int):
            if index < 0:
                raise TypeError("Invalid argument type")
            self._fill_to(index)
        elif isinstance(index, slice):
            low, high, step = index.indices(maxint)
            if step == 0:
                raise ValueError("Step must not be 0")
            return self.__class__() << map(
                self.__getitem__, range(low, high, step or 1)
            )
        else:
            raise TypeError("Invalid argument type")

        return self._collection.__getitem__(index)
