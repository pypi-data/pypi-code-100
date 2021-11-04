# Copyright 2021 drewCo Software, All Rights Reserved

from drewcopytools.filetools import get_sequential_file_path
import logging
from pathlib import Path

# ----------------------------------------------------------------------------------------------------------------------------
# REUSE
def init_logging(logName:str = "./log.runlog"):

    LOG_NAME = logName
    LOG_FORMAT = "%(asctime)s %(name)s:%(levelname)s:%(message)s"

    fileHandler = logging.FileHandler(filename=LOG_NAME, encoding='utf-8', mode='a+')

    # also this:
    # https://pythonhowtoprogram.com/logging-in-python-3-how-to-output-logs-to-file-and-console/
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamformat = logging.Formatter("%(message)s")
    streamHandler.setFormatter(streamformat)

    # Thanks!  Since the docs give exmaples that dont work:
    # https://stackoverflow.com/questions/10706547/add-encoding-parameter-to-logging-basicconfig
    logging.basicConfig(handlers=[fileHandler, streamHandler],
                        format=LOG_FORMAT, 
                        datefmt="%F %A %T", 
                        level=logging.INFO)


# ----------------------------------------------------------------------------------------------------------------------------
# REUSE
def log_exception(ex):
    logging.critical("")
    logging.critical("Unhandled exception was encountered in __main__!")
    
    # Save the exception...
    exDataPath = get_sequential_file_path(Path("./.exception"), "exception", ".txt")
    logging.critical("Exception detail will be saved to: " + str(exDataPath))

    # tex = traceback.TracebackException.from_exception(ex, limit=10, lookup_lines=False, capture_locals=True)
    # sum = tex.stack
    import traceback
    fex = traceback.format_exception(ex.__class__, value=ex, tb=ex.__traceback__, limit=15)

    stackTrace = ''.join(fex)
    logging.critical(stackTrace)

    LINE = "-------------------------------------\n"
    content = LINE
    content += 'EXCEPTION LOG:\n'
    content += LINE + "\n"
    content += "Stack Trace:\n" + LINE
    content += stackTrace
    exDataPath.write_text(content)
