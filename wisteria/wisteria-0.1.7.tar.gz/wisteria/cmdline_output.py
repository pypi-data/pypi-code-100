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
import datetime
import time

from rich import print as rprint

from wisteria.globs import DEFAULT_REPORTFILE_NAME


def parse_output_argument(output_string):
    """
        parse_output_argument()

        Parse the --output string <output_string>.

        _______________________________________________________________________

        ARGUMENT: (str)output_string, the --output string

        RETURNED VALUE:(
                        (bool)success, True if the --output string had been successfully parsed
                        (bool)output to the console ?,
                        (bool)output to the reportfile ?,
                        (str)reportfile open mode = 'a' or 'w',
                        (str)reportfile name,
                       )
    """
    success = False
    bool_console = False
    bool_reportfile = False
    opening_mode = "w"
    reportfile_name = DEFAULT_REPORTFILE_NAME

    # ---- console part -------------------------------------------------------
    if "console;" in output_string:
        bool_console = True
        output_string = output_string.replace("console;", "")
    elif "console" in output_string:
        bool_console = True
        output_string = output_string.replace("console", "")

    # ---- reportfile part -------------------------------------------------------
    if "reportfile" in output_string:
        bool_reportfile = True
        if "reportfile/a" in output_string:
            opening_mode = "a"
            output_string = output_string.replace("reportfile/a", "")
        elif "reportfile/w" in output_string:
            opening_mode = "w"
            output_string = output_string.replace("reportfile/w", "")
        else:
            output_string = output_string.replace("reportfile", "")

        output_string = output_string.replace(";", "")

        if "=" in output_string:
            reportfile_name = output_string[output_string.index('=')+1:]
            output_string = output_string.replace("=", "")
            output_string = output_string.replace(reportfile_name, "")
            if not reportfile_name:
                rprint("(ERRORID014) Ill-formed --output string: empty reportfile name.")
                return False, None, None, None, None

            # Should we replace special strings 'TIMESTAMP'/'DATETIME' (in <reportfile_name>)
            # by the expected string ?
            #
            # (pimydoc)report filename format
            # ⋅* either a simple string like 'report.txt'
            # ⋅* either a string containing 'DATETIME'; in this case, 'DATETIME' will
            # ⋅  be replaced by datetime.datetime.now().strftime("%Y-%m-%d.%H.%M.%S");
            # ⋅  e.g. "report_DATETIME.txt" would become something like
            # ⋅       "report_2021-12-31.23.59.59.txt"
            # ⋅* either a string containing 'TIMESTAMP'; in this case, 'TIMESTAMP' will
            # ⋅  be replaced by str(int(time.time()))
            # ⋅    e.g. "report_DATETIME.txt" would become something like
            # ⋅         "report_1635672267.txt"
            if 'DATETIME' in reportfile_name:
                reportfile_name = reportfile_name.replace(
                    'DATETIME',
                    datetime.datetime.now().strftime("%Y-%m-%d.%H.%M.%S"))
            if 'TIMESTAMP' in reportfile_name:
                reportfile_name = reportfile_name.replace(
                    'TIMESTAMP',
                    str(int(time.time())))

    # ---- what else ? --------------------------------------------------------
    if output_string.strip() == "":
        success = True
    else:
        rprint(f"(ERRORID019) Ill-formed --output string: what is '{output_string}' ?.")
        return False, None, None, None, None

    return success, bool_console, bool_reportfile, opening_mode, reportfile_name
