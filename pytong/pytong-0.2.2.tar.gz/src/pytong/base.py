"""Base for all Classes.

Base mainly includes the description fields
"""
import logging
from typing import Optional

from .log import Log  # type: ignore


class BaseLog:
    """
    Set a base logging.

    Use this as the base class for all your work. This adds a logging root.
    """

    def __init__(self, log_root: Optional[Log] = None):
        """Set the Root Log."""
        # since we have no log otherwise
        self.log_root = log_root
        self.log = (
            log_root.log_class(self)
            if log_root is not None
            else logging.getLogger(__name__)
        )
        self.log.debug(f"{self=}")
