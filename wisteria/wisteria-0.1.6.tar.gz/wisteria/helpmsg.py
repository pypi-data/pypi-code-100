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
    Wisteria project : wisteria/helpmsg.py

    Some help messages

    ___________________________________________________________________________

    o  help_graphsfilenames()
"""
import sys

from wisteria.globs import GRAPHS_FILENAME, LOGFILE_NAME
from wisteria.utils import normpath, get_missing_required_modules


def help_helpcommandlineargument():
    """
        help_helpcommandlineargument()

        Complete the --help message. If all required packages are installed,
        give some advice; if all required packages ARE NOT installed,
        give the list of the missing packages.
    """
    missing_modules = get_missing_required_modules()

    if not missing_modules:
        return 'Try $ wisteria --checkup then $ wisteria --cmp="pickle against marshal". ' \
            'The results appear in the console and ' \
            f'are also written in a file, \'{LOGFILE_NAME}\' ({normpath(LOGFILE_NAME)}), ' \
            'and - if matplotlib is installed - graphs are written in files named ' \
            f'{help_graphsfilenames()}.'

    return "\n\nERROR !\nBEWARE, MISSING REQUIRED PACKAGAGES ! " \
        "THE PROGRAM CAN'T BE EXECUTED WITHOUT THE FOLLOWING PACKAGE(S): " \
        f"{tuple(missing_modules)}; " \
        f"current Python version: {sys.version.replace(chr(0x0A), '- ')}"


def help_graphsfilenames():
    """
        help_graphsfilenames()

        Return a message describing where graphs files would be written
        on disk.

        _______________________________________________________________________

        RETURNED VALUE: (str)an help message
    """
    return f"'{GRAPHS_FILENAME.replace('__SUFFIX__', '1')}' " \
        f"({normpath(GRAPHS_FILENAME.replace('__SUFFIX__', '1'))}), " \
        f"'{GRAPHS_FILENAME.replace('__SUFFIX__', '2')}' " \
        f"({normpath(GRAPHS_FILENAME.replace('__SUFFIX__', '2'))}), " \
        "and so on"
