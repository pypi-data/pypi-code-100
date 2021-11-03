"""Acquisition

Acquisition is an abstraction methodology used in traversal scenarios, by
which descendents can enquire up the ancestor chain for an object. For example
if an object wanted a database session it can acquire it from a parent through
``self.acquisition.db_session`` which could be ``self.parent.db_session`` or
``self.parent.parent.db_session`` depending where it is first found.

Item acquisition e.g. ``self.acquisition['foo']`` is specifically not
implemented since that opens the possibility of injection attacks from
content sources.
"""

from .traversal import traverse_up
from inspect import currentframe

_MISSING_ATTRIBUTE = object()  # an object representing no returned attribute


class AcquisitionProxy(object):
    """A proxy object which searches for attributes or items from ancestors
    of the current domain object
    """

    def __init__(self, subject: object = None):
        """Initialize acquisition proxy

        Args:
            subject: The current object to start the search
        """
        if subject is None:
            try:
                frame = currentframe().f_back
            except AttributeError as err:
                raise Exception("Unknown subject") from err
            if frame is None:
                raise Exception("Unknown subject")
            try:
                subject = frame.f_locals["self"]
            except KeyError as err:
                raise Exception("Unknown subject") from err
        self._ctq_subject = subject

    def __getattr__(self, name: str):
        for current in traverse_up(self._ctq_subject):
            value = getattr(current, name, _MISSING_ATTRIBUTE)
            if value is not _MISSING_ATTRIBUTE:
                setattr(self, name, value)
                return value

        # Nothing found
        raise AttributeError(name)


acquire = AcquisitionProxy
