#!/usr/bin/env python
""" ident - identify RCS keyword strings in files
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
"""

import getopt
import logging
import os
import re
import signal
import sys

import strings

# Version string used by the ident(1) and ident(1) commands:
ID = "@(#) $Id: ident - identify RCS keyword strings in files v1.0.0 (October 31, 2021) by Hubert Tournier $"

# Default parameters. Can be overcome by environment variables, then command line options
parameters = {
    "Quiet mode": False,
    "Allow Subversion patterns": False,
    "Require ending space": False,
    "No match is an error": False,
    "Command flavour": "PNU",
}


################################################################################
def _initialize_debugging(program_name):
    """Debugging set up"""
    console_log_format = program_name + ": %(levelname)s: %(message)s"
    logging.basicConfig(format=console_log_format, level=logging.DEBUG)
    logging.disable(logging.INFO)


################################################################################
def _display_help():
    """Displays usage and help"""
    if parameters["Command flavour"] in ("bsd", "bsd:freebsd"):
        print("usage: ident [--debug] [--help|-?] [--version]", file=sys.stderr)
        print("       [-qV] [--] [file ...]", file=sys.stderr)
        print(
            "  ---------  ------------------------------------------",
            file=sys.stderr
        )
        print("  -q         Quiet mode", file=sys.stderr)
        print("  -V         Do nothing and exit", file=sys.stderr)
        print("  --debug    Enable debug mode", file=sys.stderr)
        print("  --help|-?  Print usage and this help message and exit", file=sys.stderr)
        print("  --version  Print version and exit", file=sys.stderr)
        print("  --         Options processing terminator", file=sys.stderr)
    else: # if parameters["Command flavour"] in ("PNU", "gnu", "gnu:linux", "linux"):
        print("usage: ident [--debug] [--help|-?] [-V|--version]", file=sys.stderr)
        print("       [-q] [--] [file ...]", file=sys.stderr)
        print(
            "  ------------  ------------------------------------------",
            file=sys.stderr
        )
        print("  -q            Quiet mode", file=sys.stderr)
        print("  --debug       Enable debug mode", file=sys.stderr)
        print("  --help|-?     Print usage and this help message and exit", file=sys.stderr)
        print("  -V|--version  Print version and exit", file=sys.stderr)
        print("  --            Options processing terminator", file=sys.stderr)
    print(file=sys.stderr)


################################################################################
def _handle_interrupts(signal_number, current_stack_frame):
    """Prevent SIGINT signals from displaying an ugly stack trace"""
    print(" Interrupted!\n", file=sys.stderr)
    _display_help()
    sys.exit(0)


################################################################################
def _handle_signals():
    """Process signals"""
    signal.signal(signal.SIGINT, _handle_interrupts)


################################################################################
def _process_environment_variables():
    """Process environment variables"""
    # pylint: disable=C0103
    global parameters
    # pylint: enable=C0103

    if "IDENT_DEBUG" in os.environ:
        logging.disable(logging.NOTSET)

    if "FLAVOUR" in os.environ:
        parameters["Command flavour"] = os.environ["FLAVOUR"].lower()
    if "IDENT_FLAVOUR" in os.environ:
        parameters["Command flavour"] = os.environ["IDENT_FLAVOUR"].lower()

    # Command variants supported:
    if parameters["Command flavour"] in ("PNU", "gnu", "gnu:linux", "linux"):
        parameters["Allow Subversion patterns"] = True
        parameters["Require ending space"] = True
    elif parameters["Command flavour"] in ("bsd", "bsd:freebsd"):
        parameters["No match is an error"] = True
    else:
        logging.critical("Unimplemented command FLAVOUR: %s", parameters["Command flavour"])
        sys.exit(1)

    logging.debug("_process_environment_variables(): parameters:")
    logging.debug(parameters)


################################################################################
def _process_command_line():
    """Process command line options"""
    # pylint: disable=C0103
    global parameters
    # pylint: enable=C0103

    # option letters followed by : expect an argument
    # same for option strings followed by =
    character_options = "qV?"
    string_options = [
        "debug",
        "help",
        "version",
    ]

    try:
        options, remaining_arguments = getopt.getopt(
            sys.argv[1:], character_options, string_options
        )
    except getopt.GetoptError as error:
        logging.critical("Syntax error: %s", error)
        _display_help()
        sys.exit(1)

    for option, _ in options:

        if option == "--debug":
            logging.disable(logging.NOTSET)

        elif option in ("--help", "-?"):
            _display_help()
            sys.exit(0)

        elif option == "-q":
            parameters["Quiet mode"] = True

        elif option == "-V":
            if parameters["Command flavour"] in ("gnu", "gnu:linux", "linux"):
                print(ID.replace("@(" + "#)" + " $" + "Id" + ": ", "").replace(" $", ""))
            sys.exit(0)

        elif option == "--version":
            print(ID.replace("@(" + "#)" + " $" + "Id" + ": ", "").replace(" $", ""))
            sys.exit(0)

    logging.debug("_process_command_line(): parameters:")
    logging.debug(parameters)
    logging.debug("_process_command_line(): remaining_arguments:")
    logging.debug(remaining_arguments)

    return remaining_arguments


################################################################################
def ident_in_string(printable_string):
    """If an SCCS identifier, print the string and return True"""
    if parameters["Allow Subversion patterns"]:
        if parameters["Require ending space"]:
            pattern = r".*\$[A-Za-z0-9]*::? .* #?\$.*"
        else:
            pattern = r".*\$[A-Za-z0-9]*::? .*#?\$.*"
    else:
        if parameters["Require ending space"]:
            pattern = r".*\$[A-Za-z0-9]*: .* \$.*"
        else:
            pattern = r".*\$[A-Za-z0-9]*: .*\$.*"

    if re.match(pattern, printable_string):
        content = re.sub(r"^[^$]*", "", printable_string)
        content = re.sub(r"[^$]$", "", content)
        print("     " + content)

        return True

    return False


################################################################################
def main():
    """The program's main entry point"""
    program_name = os.path.basename(sys.argv[0])

    _initialize_debugging(program_name)
    _handle_signals()
    _process_environment_variables()
    arguments = _process_command_line()

    exit_status = 0
    if arguments:
        for filename in arguments:
            if os.path.isfile(filename):
                print(filename + ":")
                found = False
                for _, printable_string in strings.strings(filename):
                    if ident_in_string(printable_string):
                        found = True
                if not found:
                    if not parameters["Quiet mode"]:
                        print("ident warning: no id keywords in " + filename, file=sys.stderr)
                    if parameters["No match is an error"]:
                        exit_status = 1
            else:
                logging.error('"%s": No such file or directory', filename)
                exit_status = 1
    else:
        found = False
        for _, printable_string in strings.strings():
            if ident_in_string(printable_string):
                found = True
        if not found:
            if not parameters["Quiet mode"]:
                print("ident warning: no id keywords in standard input", file=sys.stderr)
            if parameters["No match is an error"]:
                exit_status = 1

    sys.exit(exit_status)


if __name__ == "__main__":
    main()
