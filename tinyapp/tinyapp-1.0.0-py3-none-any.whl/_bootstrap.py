#!/usr/bin/env python
# -*- coding: utf-8 -*-


def init():
    from ._logger import init as init_logger
    init_logger()


def run(
        callback,
        *args, **kwargs
):
    init()

    from ._logger import app_logger as logger
    logger.info("Application startup")
    try:
        exitcode = callback(*args, **kwargs)
    except:
        logger.fatal("An exception occurs", exc_info=True)
        exitcode = -1
    finally:
        logger.info("Application shutdown")

    import sys
    sys.exit(0 if exitcode is None else exitcode)
