"""This is the bob.io.stream package

This package provides a way to define efficient processing pipelines, based on the concept of "streams", to load and 
process video data stored in hdf5 files. The interface with the hdf5 files is implemented in 
:class:`~bob.io.stream.StreamFile`. Users can define loading and processing pipeline through the 
:class:`~bob.io.stream.Stream` class.

The stream implementation is designed to allow the extension of the class by implementing filters using the  
:class:`~bob.io.stream.StreamFilter` class and decorating them with :func:`~bob.io.stream.stream_filter`. The decorator
adds the filter to the :class:`~bob.io.stream.Stream`, so it can be used as a stream's member.
"""

# To expose the general classes at the package level: eg: bob.io.stream.Stream and not bob.io.stream.stream.Stream
from bob.io.stream.stream_file import StreamFile
from bob.io.stream.stream import Stream, stream_filter, StreamFilter


# Filters are decorated to be integrated in the stream class, which happens when the module implementing them is
# imported. We import them here to make sure the they are available.

# import filters defined in stream.py
from bob.io.stream.stream import StreamView, StreamSave, StreamAsType, StreamAdjust

# import filters defined in stream_image_filters
from bob.io.stream.stream_image_filters import (
    StreamSelect,
    StreamColorMap,
    StreamNormalize,
    StreamClean,
    StreamStacked,
    StreamSubtract,
)

# Import it so it can be linked against in documentation
from .utils import StreamArray

# Since elements are made available at the package level, we need to update this otherwise sphinx can not find them.
Stream.__module__ = "bob.io.stream"
StreamFile.__module__ = "bob.io.stream"
StreamFilter.__module__ = "bob.io.stream"
stream_filter.__module__ = "bob.io.stream"


def get_config():
    """Returns a string containing the configuration information.
    """

    import bob.extension

    return bob.extension.get_config(__name__)


# gets sphinx autodoc done right - don't remove it
__all__ = [_ for _ in dir() if not _.startswith("_")]
