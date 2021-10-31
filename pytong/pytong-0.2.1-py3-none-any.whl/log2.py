#!/usr/bin/env/python
"""
Log v2 within a package.

This takes a logging.yaml configuration file that can either be just
for this package or for all libraries that are compliant.
"""
import logging
import logging.config
from pathlib import Path
import yaml  # type: ignore

# https://www.geeksforgeeks.org/python-functools-wraps-function/
# we only wrap classes though
# from functools import update_wrapper

log: logging.Logger = logging.getLogger(__name__)


def config_log(config: Path = Path("logging.yaml")):
    """Read Logging Config YAML file."""
    log.warning(f"{Path.cwd()=}")
    with open(config, "r") as stream:
        try:
            logging_config = yaml.safe_load(stream)
        except yaml.YAMLError:
            # no config so take defaults
            pass
    logging.config.dictConfig(logging_config)


# https://pencilprogrammer.com/decorate-python-class/
# the above was a function that you call that is setting the logging
# configuration
# This example decorate a class so that each class
# create a self.log where the logger name is __name__ + '.' + type(object)
# That is the each class in a module/file will get it's own logger name
# making the logging out put nice and clear


# https://towardsdatascience.com/using-class-decorators-in-python-2807ef52d273
class SetLog:
    """
    Wrap a class with logging info.

    Automatically create a specific logger and set the which is in
    global called log.
    """

    # https://stackoverflow.com/questions/10814452/how-can-i-access-global-variable-inside-class-in-python
    def __init__(self, class_to_wrap: object, name: str = None):
        """Set logger with a name based on current module and class."""
        # no easy way to set a breakpoint from pdb into a class so do this
        # breakpoint()
        global log
        self.wrapped_class: object = class_to_wrap
        # https://www.geeksforgeeks.org/python-functools-update_wrapper/
        # update wrapper only works for functions
        # update_wrapper(self, class_to_wrap)

        if name is None:
            # __class__.__name__ is actually just type
            # https://stackoverflow.com/questions/20599375/what-is-the-purpose-of-checking-self-class-python?noredirect=1&lq=1
            # type(self).__name__ is preferred
            # __name__ is not quite right either at decorator time
            # it is not fully qualified
            name = (
                self.wrapped_class.__module__
                + "."
                # not clear if __name__ exists so use getattr
                # + self.wrapped_class.__name__
                + getattr(self.wrapped_class, "__name__")
            )

        # this generates a mypy error since log is potentially not defined
        # use setattr instead
        # self.wrapped_class.log = logging.getLogger(name)
        # use the setattr to get around mypy bug
        setattr(self.wrapped_class, "log", logging.getLogger(name))
        log.debug(f"set {self.wrapped_class=} log")

    def __call__(self, *args, **kwargs):
        """
        Accept the __init__ call from the wrapped class.

        And pass it on since we just set the log but this could be used
        to log all entries.
        """
        # https://www.geeksforgeeks.org/__call__-in-python/
        # this fakes out a class call, so
        # normally x = new_class(a, b, c) will call new_class.__init__()
        # but when wrapped, the logging class gets the init and then
        # new_class.__call__() is run
        log.debug(f"run __init__ for {self.wrapped_class=}")
        return self.wrapped_class(*args, **kwargs)
