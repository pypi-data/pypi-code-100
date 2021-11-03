from keywindinstaller import keywindinstaller as ki
import sys, logging
logging.basicConfig(level = logging.DEBUG, format = "%(message)s")
def read_arguments():
    arguments = []
    for index, argument in enumerate(sys.argv):
        if (index):
            arguments.append(argument)
    return arguments
def call_installer(arguments, arg_limit = 1):
    if (len(arguments) > arg_limit):
        logging.debug(f"Error: Expected {arg_limit} argument(s) but received {len(arguments)}\n")
    else:
        ki.Installer(arguments[0])
call_installer(read_arguments())