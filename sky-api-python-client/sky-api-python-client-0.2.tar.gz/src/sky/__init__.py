"""
"""

__version__ = '0.2.0'


from .sky import Sky

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())