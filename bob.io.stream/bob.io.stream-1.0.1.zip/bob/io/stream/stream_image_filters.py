# -*- coding: utf-8 -*-
"""Image manipulation filters.

This module implements several StreamFilters for image processing. The following functionalities are available:

- selection of a channel in a color video stream: :class:`~bob.io.stream.StreamSelect`
- map a 1 channel image (eg depth map) to a color image for visualization: :class:`~bob.io.stream.StreamColorMap`
- normalize stream's value to image format: :class:`~bob.io.stream.StreamNormalize`
- clean dead pixels in stream's data: :class:`~bob.io.stream.StreamClean`
- stack 2 streams along the channel dimension: :class:`~bob.io.stream.StreamStacked`
- Subtract a stream from another (to remove background noise): :class:`~bob.io.stream.StreamSubtract`
"""


import numpy as np
import cv2 as cv

from bob.io.image.utils import opencvbgr_to_bob

from .utils import StreamArray
from .stream import stream_filter, StreamFilter


@stream_filter("select")
class StreamSelect(StreamFilter):
    """Filter to select a channel in a color stream (in bob's format).

    This could also be performed by slicing the channel in the parent.

    Attributes
    ----------
    channel : int
        Index of the channel to keep.
    """

    def __init__(self, name, parent, channel):
        """Set `channel` and initializes super() name and parent.

        Parameters
        ----------
        name : str
            "select": identifier name to use this filter from the :obj:`~bob.io.stream.Stream` class.
        parent : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
            Parent Stream(Filter).
        channel : int
            The channel to select in the color stream.
        """
        super().__init__(name=name, parent=parent)
        self.channel = channel

    @property
    def shape(self):
        """Shape of the stream's data.

        Because 1 channel is selected, the dimension is 1 on the channel axis.

        Returns
        -------
        :obj:`tuple` of int
            Shape of the stream's data.
        """
        return (self.parent.shape[0], 1, self.parent.shape[2], self.parent.shape[3])

    def process(self, data, indices):
        """Select the required channel in `data`.

        Parameters
        ----------
        data : :obj:`numpy.ndarray`
            Color data, from which a channel is selected.
        indices : int
            Not used. Present for compatibility with other filters.

        Returns
        -------
        :obj:`numpy.ndarray`
            Selected channel in `data`.
        """
        return np.expand_dims(data[:, self.channel, :, :], axis=1)


@stream_filter("colormap")
class StreamColorMap(StreamFilter):
    """Filter to map a 1 channel images to RGB images, usefull for visualization, eg of depth maps.

    Attributes
    ----------
    colormap : str
        The colormap used to represent the data. Can be "gray" for grayscale, or an openCV colormap.
    """

    def __init__(self, name, parent, colormap="gray"):
        """Set the StreamFilter (super) name and parent, and the requested colormap.

        Parameters
        ----------
        name : str
            "colormap": identifier name to use this filter from the :obj:`~bob.io.stream.Stream` class.
        parent : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
            Parent Stream(Filter).
        colormap : str
            Colormap to use, by default "gray"
        """
        super().__init__(name=name, parent=parent)
        self.colormap = colormap

    @property
    def shape(self):
        """Shape of the stream's data. The stream parent must have 1 channel, and this stream has mapped it to 3 (RGB).

        Returns
        -------
        :obj:`tuple` of int
            Shape of the stream's data.
        """
        return (self.parent.shape[0], 3, self.parent.shape[2], self.parent.shape[3])

    def process_frame(self, data, data_index, stream_index):
        """Maps a 1 channel frame to a RGB frame using the filter's colormap.

        Parameters
        ----------
        data : :obj:`numpy.ndarray`
            Parent stream's data. Must have only 1 channel
        data_index : int
            Not used. Present for compatibility with other streams.
        stream_index : int
            Not used. Present for compatibility with other filters.

        Returns
        -------
        :obj:`numpy.ndarray`
            Stream's data, mapped to RGB using the filter's colormap.

        Raises
        ------
        ValueError
            If the parent's stream does not have only 1 channel: this stream maps 1 channel images to RGB.
        """
        if data.shape[0] == 1:
            # normalise
            tmin = np.amin(data)
            tmax = np.amax(data)
            data = data[0, :, :]
            data = (data - tmin).astype("float")
            data = (data * 255.0 / float(tmax - tmin)).astype("uint8")
            if self.colormap == "gray":
                data = (np.stack([data, data, data])).astype("uint8")
                return data
            else:
                # TODO: add all colormaps
                maps = {
                    "jet": cv.COLORMAP_JET,
                    "bone": cv.COLORMAP_BONE,
                    "hsv": cv.COLORMAP_HSV,
                }
                data = cv.applyColorMap(data, maps[self.colormap])
                data = opencvbgr_to_bob(data)
                return data
        else:
            raise ValueError("Can not convert multi-channel streams. Parent number of channels: " + str(data.shape[0]))


@stream_filter("normalize")
class StreamNormalize(StreamFilter):
    """Filter to normalize images data range.

    Attributes
    ----------
    tmin : :obj:`numpy.generic`
        minimal threshold: values below `tmin` will be clipped to 0.
    tmax : :obj:`numpy.generic`
        maximum threshold: values over `tmax` will be clipped to the maximum value allowed by the `dtype`
    dtype : str or :obj:`numpy.dtype`
        Data type of the images.
    """

    def __init__(self, name, parent, tmin=None, tmax=None, dtype="uint8"):
        """Set super() arguments and optionally set min/max threshold and output dtype.

        Parameters
        ----------
        name : str
            "normalize": identifier name to use this filter from the :obj:`~bob.io.stream.Stream` class.
        parent : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
            Parent Stream(Filter).
        tmin : :obj:`numpy.generic`
            Minimum threshold for clipping, by default None. If None, the minimum of the retrieved data will be used.
        tmax : :obj:`numpy.generic`
            Maximum threshold for clipping, by default None. If None, the maximum of the retrieved data will be used.
        dtype : str or :obj:`numpy.dtype`
            Data type of the output, by default "uint8".
        """
        self.tmin = tmin
        self.tmax = tmax
        self.dtype = dtype
        super().__init__(name=name, parent=parent)

    def process(self, data, indices):
        """Normalize `data`.

        Parameters
        ----------
        data : :obj:`numpy.ndarray`
            The parent stream's data, to be normalized.
        indices : int or :obj:`list` of int
            Not used. Present for compatibility with other filters. The indices of `data` in the stream.

        Returns
        -------
        :obj:`numpy.ndarray`
            The normalized data.
        """
        tmin = np.amin(data) if self.tmin is None else self.tmin
        tmax = np.amax(data) if self.tmax is None else self.tmax
        data = (data - tmin).astype("float64")
        data = data / float(tmax - tmin)
        data = np.clip(data, a_min=0.0, a_max=1.0)
        if self.dtype == "uint8":
            data = (data * 255.0).astype("uint8")
        elif self.dtype == "uint16":
            data = (data * 65535.0).astype("uint16")
        return data


@stream_filter("clean")
class StreamClean(StreamFilter):
    """Filter to fill in dead pixels through inpainting, then blurring."""

    def __init__(self, name, parent):
        """Set super().

        Parameters
        ----------
        name : str
            "clean": identifier name to use this filter from the :obj:`~bob.io.stream.Stream` class.
        parent : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
            Parent Stream(Filter).
        """
        super().__init__(name=name, parent=parent)

    def process_frame(self, data, data_index, stream_index):
        """Fill in dead pixels in `data`.

        Parameters
        ----------
        data : :obj:`numpy.ndarray`
            Parent stream's data to clean.
        data_index : int or :obj:`list` of int
            Not used. Present for compatibility with other filters.
        stream_index : int or :obj:`list` of int
            Not used. Present for compatibility with other filters.

        Returns
        -------
        :obj:`numpy.ndarray`
            Cleaned `data`.
        """
        data = data[0]
        dtype = data.dtype
        data = data.astype(np.float32)
        mask = np.where(data == 0, 1, 0).astype(np.uint8)
        data = cv.inpaint(data, mask, 3, cv.INPAINT_NS)
        data = cv.medianBlur(data, 3)
        data = np.stack([data]).astype(dtype)
        return data


@stream_filter("stack")
class StreamStacked(StreamFilter):
    """Filter to stack streams along the channel dimension.

    The stream stacks his parent Stream with its `stack_stream`.

    Attributes
    ----------
    stack_stream : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
        The stream to stack with `parent`.
    """

    def __init__(self, stack_stream, name, parent):
        """Set super() and `stack_stream`

        Parameters
        ----------
        stack_stream : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
            The stream to stack with `parent`.
        name : str
            "stack": identifier name to use this filter from the :obj:`~bob.io.stream.Stream` class.
        parent : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
            Parent Stream(Filter).
        """
        super().__init__(name=name, parent=parent)
        self.stack_stream = stack_stream

    def set_source(self, src):
        """Set `self` and `stack_stream` source to `src`.

        Parameters
        ----------
        src : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFile`
            Source Stream or StreamFile.
        """
        super().set_source(src)
        self.stack_stream.set_source(src)

    @property
    def shape(self):
        """Shape of the stream's data. The number of channels is the sum of the parent's and the stacked stream.

        Returns
        -------
        :obj:`tuple` of int
            Shape of the stream's data.
        """
        return (
            self.parent.shape[0],
            self.parent.shape[1] + self.stack_stream.shape[1],
            self.parent.shape[2],
            self.parent.shape[3],
        )

    def process(self, data, indices):
        """Stacks data from `stack_stream` with `data` (which comes from parent).

        `data` comes from `parent` with shape (n, c1, ...), this method loads the data of `stack_stream` at the same 
        indices, which has shape (n, c2, ...), then stacks them to output an array of shape (n, c1 + c2, ...)

        `parent` and `stack_stream` must have the same dimensions, except in the channel axis.

        Parameters
        ----------
        data : :obj:`numpy.ndarray`
            Parent stream's data at `indices`
        indices : int or :obj:`list` of int
            Indices of `data`

        Returns
        -------
        :obj:`numpy.ndarray`
            `data` from parent stacked with data at `indices` from `stacked_stream` along the channel dimension.
        """
        # Load data from `stack_stream` at `indices` once.
        self.data2 = self.stack_stream.load(indices)
        # stack at the frame level: super().process stacks the output of `process_frame`
        return super().process(data, indices)

    def process_frame(self, data, data_index, stream_index):
        """Concatenate frame from `parent` and `stack_stream` along channel axis.

        Parameters
        ----------
        data : :obj:`numpy.ndarray`
            `parent` frame at `data_index`.
        data_index : int
            Index of the frames to stack in the streams.
        stream_index : int
            Not used. Present for compatibility with other filters.

        Returns
        -------
        :obj:`numpy.ndarray`
            Concatenated frames from `parent` and `stack_stream` streams.
        """
        return np.concatenate((data, self.data2[data_index]), axis=0)


@stream_filter("subtract")
class StreamSubtract(StreamFilter):
    """Filter to subtract `subtrahend` from `parent`, clipping results values to be positive or zero.

    Attributes
    ----------
    subtrahend : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
        The stream's which data will be subtracted.
    """

    def __init__(self, subtrahend, name, parent):
        """Set super and register `subtrahend`.

        Parameters
        ----------
        subtrahend : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
            The stream's which data will be subtracted.
        name : str
            "subtract": identifier name to use this filter from the :obj:`~bob.io.stream.Stream` class.
        parent : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFile`
            Parent Stream(Filter).
        """
        self.subtrahend = subtrahend
        super().__init__(name=name, parent=parent)

    def set_source(self, src):
        """Set `self` and `subtrahend` sources to `src`.

        Parameters
        ----------
        src : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFile`
            Source stream or stream file.
        """
        super().set_source(src)
        self.subtrahend.set_source(src)

    def process(self, data, indices):
        """Subtract `subtrahend`'s data from `data`.

        Parameters
        ----------
        data : :obj:`numpy.ndarray`
            `parent` data at `indices`.
        indices : int
            Indices of `data`.

        Returns
        -------
        :obj:`numpy.ndarray`
            `data` minus `subtrahend`'s data.
        """
        subtrahend_data = self.subtrahend.load(indices)
        assert data.shape == subtrahend_data.shape
        # if data > subtrahend_data: return data - subtrahend_data, else return 0 (clipping subtraction to 0)
        return np.where(data > subtrahend_data, data - subtrahend_data, 0)
