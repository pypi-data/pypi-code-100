#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    Wisteria Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of Wisteria.
#    Wisteria is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Wisteria is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Wisteria.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    Wisteria project : wisteria/msg.py

    Fonctions used to print & log all projects' messages.

    msgreport() is reserved to checkup, report messages and mymachine().
    msgreporttitle() is reserved to title's report messages.

    Caveat!
    In this project, the choice of a msgxxx() method has nothing to do with
    priority (cf DEBUG, INFO, ERROR) but with message appearance (confer
    special symbols like '@', '>' or '!'). Priority is managed at each call
    of msgxxx() by a test of type
         if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
             msgdebug(...)
    ___________________________________________________________________________

    o  _message(obj)
    o  msgcritical(obj="")
    o  msgdebug(obj="")
    o  msgerror(obj="")
    o  msginfo(obj="")
    o  msgreport(obj="")
    o  msgreporttitle(obj="")
    o  msgwarning(obj="")
"""
from rich import print as rprint

from wisteria.reprfmt import fmt_title, fmt_error
import wisteria.globs


def _message(obj):
    """
        _message()

        Internal function: displays and/or writes <obj> in the log file.

        _______________________________________________________________________

        ARGUMENT: <obj>, the object to be displayed/written in the log file
    """
    if wisteria.globs.OUTPUT[0]:
        rprint(obj)
    if wisteria.globs.OUTPUT[1]:
        wisteria.globs.FILECONSOLE.print(obj)


def msgcritical(obj=""):
    """
        msgcritical()

        Display and/or write <obj> in the log file; to be used like log.critical() .

        _______________________________________________________________________

        ARGUMENT: <obj>, the object to be displayed/written in the log file.
    """
    _message("!!! "+str(obj))


def msgdebug(obj=""):
    """
        msgcritical()

        Display and/or write <obj> in the log file; to be used like log.debug() .

        _______________________________________________________________________

        ARGUMENT: <obj>, the object to be displayed/written in the log file.
    """
    _message("@ "+str(obj))


def msgerror(obj=""):
    """
        msgerror()

        Display and/or write <obj> in the log file; to be used like log.error() .

        _______________________________________________________________________

        ARGUMENT: <obj>, the object to be displayed/written in the log file.
    """
    if isinstance(obj, str):
        obj = fmt_error(obj)
    _message(obj)


def msginfo(obj=""):
    """
        msginfo()

        Display and/or write <obj> in the log file; to be used like log.info() .

        _______________________________________________________________________

        ARGUMENT: <obj>, the object to be displayed/written in the log file.
    """
    _message("> "+str(obj))


def msgreport(obj=""):
    """
        msgreport()

        Display and/or write <obj> in the log file; to be used like log.info() .

        _______________________________________________________________________

        ARGUMENT: <obj>, the object to be displayed/written in the log file.
    """
    _message(obj)


def msgreporttitle(obj=""):
    """
        msgreporttitle()

        Display and/or write <obj> in the log file; to be used like log.info() .

        _______________________________________________________________________

        ARGUMENT: <obj>, the object to be displayed/written in the log file.
    """
    _message(fmt_title(obj))


def warning(obj=""):
    """
        msgwarning()

        Display and/or write <obj> in the log file; to be used like log.warning() .

        _______________________________________________________________________

        ARGUMENT: <obj>, the object to be displayed/written in the log file.
    """
    _message("! "+str(obj))
