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
    Wisteria project : wisteria/cmdline_output.py

    Just the parsing of the --output argument. No msgxxx() method here since
    at this stage of the program no msgxxx() methods have not yet be
    initialized.

    ___________________________________________________________________________

    o  parse_output_argument(output_string)
"""
from rich import print as rprint

from wisteria.globs import LOGFILE_NAME


def parse_output_argument(output_string):
    """
        parse_output_argument()

        Parse the --output string <output_string>.

        _______________________________________________________________________

        ARGUMENT: (str)output_string, the --output string

        RETURNED VALUE:(
                        (bool)success, True if the --output string had been successfully parsed
                        (bool)output to the console ?,
                        (bool)output to the logfile ?,
                        (str)logfile open mode = 'a' or 'w',
                        (str)logfile name,
                       )
    """
    success = False
    bool_console = False
    bool_logfile = False
    opening_mode = "w"
    logfile_name = LOGFILE_NAME

    # ---- console part -------------------------------------------------------
    if "console;" in output_string:
        bool_console = True
        output_string = output_string.replace("console;", "")
    elif "console" in output_string:
        bool_console = True
        output_string = output_string.replace("console", "")

    # ---- logfile part -------------------------------------------------------
    if "logfile" in output_string:
        bool_logfile = True
        if "logfile/a" in output_string:
            opening_mode = "a"
            output_string = output_string.replace("logfile/a", "")
        elif "logfile/w" in output_string:
            opening_mode = "w"
            output_string = output_string.replace("logfile/w", "")
        else:
            output_string = output_string.replace("logfile", "")

        output_string = output_string.replace(";", "")

        if "=" in output_string:
            logfile_name = output_string[output_string.index('=')+1:]
            output_string = output_string.replace("=", "")
            output_string = output_string.replace(logfile_name, "")
            if not logfile_name:
                rprint("(ERRORID014) Ill-formed --output string: empty logfile name.")
                return False, None, None, None, None

    # ---- what else ? --------------------------------------------------------
    if output_string.strip() == "":
        success = True
    else:
        rprint(f"(ERRORID019) Ill-formed --output string: what is '{output_string}' ?.")
        return False, None, None, None, None

    return success, bool_console, bool_logfile, opening_mode, logfile_name
