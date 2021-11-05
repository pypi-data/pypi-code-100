import logging

import coloredlogs

_format = "%(asctime)s %(pathname)s (%(lineno)d) [%(levelname)s]: %(message)s"
_field_styles = dict(
    asctime=dict(color="green"),
    hostname=dict(color="magenta"),
    levelname=dict(color="yellow", bold=True),
    pathname=dict(color="magenta"),
    name=dict(color="blue"),
    programname=dict(color="cyan"),
    username=dict(color="yellow"),
)
_level_styles = dict(
    spam=dict(color="green", faint=True),
    debug=dict(color="green"),
    verbose=dict(color="blue"),
    info=dict(color="cyan"),
    notice=dict(color="magenta"),
    warning=dict(color="yellow"),
    success=dict(color="green", bold=True),
    error=dict(color="red"),
    critical=dict(color="red", bold=True),
)


def get_logger(name=None, level=logging.INFO):
    logger = logging.getLogger(name)
    logging.root.setLevel(level)
    coloredlogs.install(
        level=level,
        datefmt="%Y-%m-%dT%H:%M:%S",
        fmt=_format,
        logger=logger,
        field_styles=_field_styles,
        level_styles=_level_styles,
    )
    return logger
