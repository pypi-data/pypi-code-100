"""
"""
# Future Imports (Python < 3.10)
from __future__ import annotations

# Typing
from typing import TextIO

# Standard Library
import sys
import os
import threading as th
import multiprocessing as mp
from functools import wraps
from contextlib import contextmanager

# Third-Party
import colorama

__version__ = "1.0.3"


class CStream(object):
    """"""

    # File Descriptors
    STDIN_FD = 0
    STDOUT_FD = 1
    STDERR_FD = 2

    RESET = colorama.Style.RESET_ALL

    COLORS = {
        "BLACK",
        "RED",
        "GREEN",
        "YELLOW",
        "BLUE",
        "MAGENTA",
        "CYAN",
        "WHITE",
        None,
    }

    # pylint: disable=no-self-argument,not-callable
    def __echo(callback):
        @wraps(callback)
        def echo_callback(self, *args, **kwargs):
            if self:
                return callback(self, *args, **kwargs)

        return echo_callback

    STYLES = {"DIM", "NORMAL", "BRIGHT", None}

    __slots__ = ("__bg", "_bg", "__fg", "_fg", "__sty", "_sty", "__end", "__file", "__level", "__flush")
    __level__ = None
    __echo__: bool = True
    __lock__: th.Lock | mp.Lock | None = None

    T_LOCK = 1  # Thread lock
    P_LOCK = 2  # Process Lock

    def __init__(
        self,
        *,
        bg: str | None = None,
        fg: str | None = None,
        sty: str | None = None,
        end: str | None = None,
        file=None,
        level: int | None = None,
        flush: bool = False,
    ):
        """"""
        # -*- Type Checking -*-
        if bg is not None and not isinstance(bg, str):
            raise ValueError(f"'bg' must be of type 'str' or 'None', not '{type(bg)}'")
        if fg is not None and not isinstance(fg, str):
            raise ValueError(f"'fg' must be of type 'str' or 'None', not '{type(fg)}'")
        if sty is not None and not isinstance(sty, str):
            raise ValueError(
                f"'sty' must be of type 'str' or 'None', not '{type(sty)}'"
            )
        if end is not None and not isinstance(end, str):
            raise ValueError(
                f"'end' must be of type 'str' or 'None', not '{type(end)}'"
            )
        if level is not None and not isinstance(level, int):
            raise ValueError(
                f"'level' must be of type 'int' or 'None', not '{type(level)}'"
            )
        if not isinstance(flush, bool):
            raise TypeError(f"'flush' must be of type 'bool', not '{type(flush)}'")

        # -*- Value Checking -*-
        if bg not in self.COLORS:
            raise ValueError(f"Color {bg!r} not available. Options are {self.COLORS}")
        else:
            self._bg = bg
        if fg not in self.COLORS:
            raise ValueError(f"Color {fg!r} not available. Options are {self.COLORS}")
        else:
            self._fg = fg
        if sty not in self.STYLES:
            raise ValueError(f"Style {sty!r} not available. Options: are {self.STYLES}")
        else:
            self._sty = sty

        if file is None:
            self.__file = sys.stdout
        else:
            self.__file = file

        self.__level = level
        self.__flush = flush

        if self._bg is None:
            self.__bg = ""
        else:
            self.__bg = getattr(colorama.Back, self._bg)

        if self._fg is None:
            self.__fg = ""
        else:
            self.__fg = getattr(colorama.Fore, self._fg)

        if self._sty is None:
            self.__sty = ""
        else:
            self.__sty = getattr(colorama.Style, self._sty)

        if end is None:
            self.__end = ""
        else:
            self.__end = end

    @classmethod
    @contextmanager
    def lock(cls):
        """"""
        if cls.__lock__ is None:
            yield
            return

        cls.__lock__.acquire()

        try:
            yield
        finally:
            cls.__lock__.release()

    @classmethod
    def config(cls, *, level: int | None = ..., lock_type: int | None = ...):

        if level == ...:
            pass
        elif isinstance(level, int):
            cls.__level__ = level
        elif level is None:
            cls.__level__ = level
        else:
            raise TypeError(
                f"'level' must be of type 'int' or 'None, not '{type(level)}'"
            )

        if lock_type == ...:
            pass
        elif lock_type == cls.T_LOCK:
            cls.__lock__ = th.Lock()
        elif lock_type == cls.P_LOCK:
            cls.__lock__ = mp.Lock()
        elif lock_type == None:
            cls.__lock__ = None
        else:
            raise ValueError("Invalid value for 'lock_type'")

    def __getitem__(self, level: int | None):
        return CStream(
            bg=self._bg,
            fg=self._fg,
            sty=self._sty,
            end=self.__end,
            file=self.__file,
            level=level,
        )

    def __bool__(self):
        return self.__echo__ and (
            (self.__level is None)
            or (self.__level__ is None)
            or (self.__level >= self.__level__)
        )

    @classmethod
    def echo_on(cls):
        """"""
        cls.__echo__ = True

    @classmethod
    def echo_off(cls):
        """"""
        cls.__echo__ = False

    # -*- <stdio.h> -*-
    @__echo
    def printf(self, s: str, *args) -> None:
        """"""
        with self.lock():
            print(self.sprintf(s, *args), end="", file=self.file, flush=self.flush)

    def sprintf(self, s: str, *args) -> str:
        """"""
        if args:
            if self.__bg or self.__fg or self.__sty:
                return f"{self.__bg}{self.__fg}{self.__sty}{s}{self.RESET}" % args
            else:
                return s % args
        elif self.__bg or self.__fg or self.__sty:
            return f"{self.__bg}{self.__fg}{self.__sty}{s}{self.RESET}"
        else:
            return s

    @__echo
    def __lshift__(self, s: str | object):
        with self.lock():
            print(self.sprintf(str(s)), end=self.end, file=self.file, flush=self.flush)
        return self

    # -*- File interface -*-
    def write(self, s: str):
        return self.file.write(s)

    @property
    def flush(self) -> bool:
        return self.__flush or (self.__lock__ is not None)

    @property
    def file(self) -> TextIO:
        return self.__file

    @property
    def end(self) -> str:
        return self.__end

    @classmethod
    def init(cls):
        colorama.init()
        os.system("")

class NullStream(CStream):

    __ref__ = None

    __slots__ = CStream.__slots__ + ("__sys_stdout", "__sys_stderr")

    def __new__(cls, *__args, **__kwargs):
        if cls.__ref__ is None:
            cls.__ref__ = CStream.__new__(cls)
        return cls.__ref__

    @wraps(CStream.__init__)
    def __init__(self, **__kwargs):
        CStream.__init__(self, **__kwargs)
        self.__sys_stdout = None
        self.__sys_stderr = None

    def __enter__(self):
        self.__sys_stdout = sys.stdout
        self.__sys_stderr = sys.stderr
        sys.stdout = sys.stderr = self

    def __exit__(self, *args, **kwargs):
        sys.stdout = self.__sys_stdout
        sys.stderr = self.__sys_stderr
        self.__sys_stdout = None
        self.__sys_stderr = None

    def write(self, __s: str):
        pass

    def read(self) -> str:
        raise IOError("Can't read from NullStream")

__all__ = ["CStream", "NullStream"]