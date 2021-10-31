#!/usr/bin/env python
""" what - identify SCCS keyword strings in files
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

# Version string used by the what(1) and ident(1) commands:
ID = "@(#) $Id: what - identify SCCS keyword strings in files v1.0.0 (October 31, 2021) by Hubert Tournier $"

# Default parameters. Can be overcome by environment variables, then command line options
parameters = {
    "Stdin unused": False,
    "First match only": False,
    "No formatting": False,
    "Command flavour": "PNU",
}

SCCS_ID = "@(#)"


################################################################################
def _initialize_debugging(program_name):
    """Debugging set up"""
    console_log_format = program_name + ": %(levelname)s: %(message)s"
    logging.basicConfig(format=console_log_format, level=logging.DEBUG)
    logging.disable(logging.INFO)


################################################################################
def _display_help():
    """Displays usage and help"""
    if parameters["Command flavour"] in ("posix", "linux"):
        print("usage: what [--debug] [--help|-?] [--version]", file=sys.stderr)
        print("       [-s] [--] file [...]", file=sys.stderr)
        print(
            "  ---------  ------------------------------------------",
            file=sys.stderr
        )
        print("  -s         Quit after finding the first occurrence", file=sys.stderr)
        print("             of the pattern in each file", file=sys.stderr)
        print("  --debug    Enable debug mode", file=sys.stderr)
        print("  --help|-?  Print usage and this help message and exit", file=sys.stderr)
        print("  --version  Print version and exit", file=sys.stderr)
        print("  --         Options processing terminator", file=sys.stderr)
    else: # if parameters["Command flavour"] in ("PNU", "bsd", "bsd:freebsd"):
        print("usage: what [--debug] [--help|-?] [--version]", file=sys.stderr)
        print("       [-qs] [--] [file ...]", file=sys.stderr)
        print(
            "  ---------  -----------------------------------------------------",
            file=sys.stderr
        )
        print("  -q         Only output the match text, rather than formatting it", file=sys.stderr)
        print("  -s         Stop searching each file after the first match", file=sys.stderr)
        print("  --debug    Enable debug mode", file=sys.stderr)
        print("  --help|-?  Print usage and this help message and exit", file=sys.stderr)
        print("  --version  Print version and exit", file=sys.stderr)
        print("  --         Options processing terminator", file=sys.stderr)
    print(file=sys.stderr)


################################################################################
def _handle_interrupts(signal_number, current_stack_frame):
    """Prevent SIGINT signals from displaying an ugly stack trace"""
    print(" Interrupted!\n", file=sys.stderr)
    _display_help()
    sys.exit(1) # no match


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

    if "WHAT_DEBUG" in os.environ:
        logging.disable(logging.NOTSET)

    if "FLAVOUR" in os.environ:
        parameters["Command flavour"] = os.environ["FLAVOUR"].lower()
    if "WHAT_FLAVOUR" in os.environ:
        parameters["Command flavour"] = os.environ["WHAT_FLAVOUR"].lower()

    # From "man environ":
    # POSIXLY_CORRECT
    # When set to any value, this environment variable
    # modifies the behaviour of certain commands to (mostly)
    # execute in a strictly POSIX-compliant manner.
    if "POSIXLY_CORRECT" in os.environ:
        parameters["Command flavour"] = "posix"

    # Command variants supported:
    if parameters["Command flavour"] in ("posix", "linux"):
        parameters["Stdin unused"] = True
    elif parameters["Command flavour"] in ("PNU", "bsd", "bsd:freebsd"):
        pass
    else:
        logging.critical("Unimplemented command FLAVOUR: %s", parameters["Command flavour"])
        sys.exit(1) # no match

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
    if parameters["Command flavour"] in ("posix", "linux"):
        character_options = "s?"
    else: # if parameters["Command flavour"] in ("PNU", "bsd", "bsd:freebsd"):
        character_options = "qs?"
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
        sys.exit(1) # no match

    for option, _ in options:

        if option == "--debug":
            logging.disable(logging.NOTSET)

        elif option in ("--help", "-?"):
            _display_help()
            sys.exit(1) # no match

        elif option == "-q":
            parameters["No formatting"] = True

        elif option == "-s":
            parameters["First match only"] = True

        elif option == "--version":
            print(ID.replace("@(" + "#)" + " $" + "Id" + ": ", "").replace(" $", ""))
            sys.exit(1) # no match

    logging.debug("_process_command_line(): parameters:")
    logging.debug(parameters)
    logging.debug("_process_command_line(): remaining_arguments:")
    logging.debug(remaining_arguments)

    return remaining_arguments


################################################################################
def what_in_string(printable_string):
    """If an SCCS identifier, print the string and return True"""
    if SCCS_ID in printable_string:
        content = re.sub(r"^.*" + re.escape(SCCS_ID), "", printable_string)
        content = re.sub(r'("|>|\n|\\).*', "", content)
        if parameters["No formatting"]:
            print(content)
        else:
            print("\t" + content)

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

    exit_status = 1 # no match
    if arguments:
        for filename in arguments:
            if os.path.isfile(filename):
                if not parameters["No formatting"]:
                    print(filename + ":")
                for _, printable_string in strings.strings(filename):
                    if what_in_string(printable_string):
                        exit_status = 0 # match found
                        if  parameters["First match only"]:
                            break
            else:
                logging.error('"%s": No such file or directory', filename)
    elif parameters["Stdin unused"]:
        logging.critical("At least one filename expected")
    else:
        for _, printable_string in strings.strings():
            if what_in_string(printable_string):
                exit_status = 0 # match found
                if  parameters["First match only"]:
                    break

    sys.exit(exit_status)


if __name__ == "__main__":
    main()
