import logging
import os
import re
import sys

import datawhys

DATAWHYS_LOG = os.environ.get("DATAWHYS_LOG")

logger = logging.getLogger("datawhys")


def _console_log_level():
    if datawhys.log in ["debug", "info"]:
        return datawhys.log
    elif DATAWHYS_LOG in ["debug", "info"]:
        return DATAWHYS_LOG
    else:
        return None


def log_debug(message, **params):
    msg = logfmt(message, dict(**params))
    if _console_log_level() == "debug":
        print(msg, file=sys.stderr)
    logger.debug(msg)


def log_info(message, **params):
    msg = logfmt(message, dict(**params))
    if _console_log_level() in ["debug", "info"]:
        print(msg, file=sys.stderr)
    logger.info(msg)


def logfmt(message, props: dict):
    def fmt(key: str, val):
        if hasattr(val, "decode"):
            val = val.decode("utf-8")

        if not isinstance(val, str):
            val = str(val)

        if re.search(r"\s", val):
            val = repr(val)

        if re.search(r"\s", key):
            key = repr(key)

        return "{key}={val}".format(key=key, val=val)

    prop_str = " ".join([fmt(key, val) for key, val in sorted(props.items())])

    return "%s %s" % (message, prop_str)
