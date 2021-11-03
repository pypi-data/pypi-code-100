# -*- coding: utf-8 -*-
"""Processing pipeline implementation.

This module implements the base class :class:`~bob.io.stream.Stream` which allows to build processing pipeline for data
stored in hdf5 files. The :class:`~bob.io.stream.Stream` implements a numpy-like interface to load or write and buffer 
data from file through the :class:`~bob.io.stream.StreamFile` class. 

Through the :func:`~bob.io.stream.stream_filter` decorator, the :class:`~bob.io.stream.Stream` class can be enriched 
with filters functions that implements data processing, which allows the easy definition of a processing pipeline by 
cascading filters. Some core functionalities of the :class:`~bob.io.stream.Stream` such as slicing 
(:class:`~bob.io.stream.StreamView`) class are also implemented using filters.

In order to implement new functionalities, one can either use the :class:`~bob.io.stream.StreamFilter` filter and 
provide a "process_frame" function, or use the :func:`~bob.io.stream.stream_filter` decorator. In order to have the the 
new filter accessible when using "import bob.io.stream", it is necessary to import the newly defined filter in the 
`__init__.py`.

Example
-------
Image processing using stream filters: 

    >>> from bob.io.stream import StreamFile, Stream
    >>> # Open a Streamfile to a hdf5 file.
    >>> f = StreamFile("input_example.h5", idiap_face_streams_config.json")
    >>> # Define streams
    >>> color = Stream("color", f)
    >>> swir_dark = Stream("swir", f)
    >>> swir_940 = Stream("swir_940nm", f)
    >>> # Define pipelines using filters
    >>> swir_dark = swir_dark.adjust(color)
    >>> swir_940 = swir_940.adjust(color).subtract(swir_dark).clean()
    >>> swir_940.load(0)  # Loads data and apply processing for the first frame.
"""


from builtins import str

import numpy as np
from scipy.spatial import cKDTree

from .utils import StreamArray, get_index_list, get_axis_size
from .stream_file import StreamFile


class Stream:
    """Base class implementing methods to load/write, process and use data from hdf5 file with a "numpy-like" api.

    This class is designed to provide the following functionalities:

    - Easily define chain of processing and loading data. When accessing data through a stream, it will recursively call
      its `parent` :meth:`~bob.io.stream.Stream.load` function before its own. For instance if a stream's parent is a 
      StreamFile, loading data through the stream will first load the data (from the dataset specified by the stream's 
      `name`) from the hdf5 through the StreamFile before applying its own processing.  
    - Provide an easy syntax to implement this chain processing. This is achieved through the 
      :func:`~bob.io.stream.stream_filter` filter decorator which adds to the Stream class filters members, allowing them to 
      be used in the following fashion::

        example_stream = Stream("cam1").normalize().stack(Stream("cam2").normalize())

      The data loaded through example_stream will thus load data from "cam1" and normalize it, then load data from 
      "cam2" and normalize it, and finally stack the two together.

    - In a similar fashion to the chain processing, this class allows to apply processing in the reverse order to write
      data in a hdf5 file. This is implemented in the :meth:`~bob.io.stream.Stream.put` method and uses the `child`
      attribute.

    The api is designed to be similar to numpy arrays:

    - Data access (processing and loading) is done using [].
    - Taking a slice in a stream returns a new stream with the sliced data. (This is implemented with the 
      :class:`~bob.io.stream.StreamView` filter).

    To reduce disk access, the result of loading or processing is buffered. 
    
    The class was initially designed to work with video streams, therefore :class:`~bob.io.stream.StreamArray` members 
    are available to provide an easy way to use bounding boxes or landmarks for each frame in the stream.
    Additionally, the :obj:`~bob.io.stream.Stream.timestamps` member are the timestamps of each frame in the stream.

    Attributes
    ----------
    name : str
        Name of the stream. If `parent` is a :class:`~bob.io.stream.StreamFile`, it will be used to know from which 
        dataset in the hdf5 file the data should be taken. Otherwise it is an identifier of the Stream (or 
        StreamFilter) functionality (eg "adjust", "normalize", ...).
    parent : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFile`
        The element before this instance in the chain of processing for *loading* data. The parent's "load" function will 
        recursively be used before this instance's one.
    child : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFile`
        The element after this instance in the chain of processing for *writing* data. When 
        :meth:`~bob.io.stream.Stream.put` is called, it will perform its function then recursively call its `child`'s.
    _loaded : :obj:`list` of int
        Indices of the data that is currently buffered.
    _data : :obj:`numpy.ndarray`
        Buffered data.
    _shape : :obj:`tuple` of int
        Shape of the stream's data. This member is mostly used when writing data, while when reading the 
        :obj:`~bob.io.stream.Stream.shape` property is used.
    """

    filters = []

    def __init__(self, name=None, parent=None):
        self.name = name
        self.parent = parent
        self.child = None
        if isinstance(parent, Stream):  # Sets Parent's child as this instance if needed.
            parent.child = self
        self.reset()

    def reset(self):
        """Deletes buffered data and meta-data."""
        self._loaded = None
        self._data = None
        self._shape = None
        self.__bounding_box = StreamArray(self)
        self.__image_points = StreamArray(self)

    @property
    def source(self):
        """Source file of the Stream's data.

        While `parent` points to the previous stream in the chain of processing, `source` points directly to the data 
        file.

        Returns
        -------
        :obj:`~bob.io.stream.StreamFile`
            File containing the stream's data, before processing.
        """
        if isinstance(self.parent, StreamFile) or self.parent is None:
            return self.parent
        else:
            return self.parent.source

    @source.setter
    def source(self, src):
        self.set_source(src)

    def set_source(self, src):
        """Recursively set `source` of self and `parent`.

        Parameters
        ----------
        src : :obj:`~bob.io.stream.StreamFile`
            The file containing the raw data of this stream and parents.
        """
        if isinstance(self.parent, StreamFile) or self.parent is None:
            self.parent = src
        else:
            self.parent.set_source(src)
        self.reset()

    @property
    def config(self):
        """Configuration dictionary to access the data in the hdf5 file.

        Returns
        -------
        :obj:`dict`
            Config.
        """
        if isinstance(self.parent, StreamFile):
            return self.parent.get_stream_config(self.name)
        else:
            return self.parent.config

    @config.setter
    def config(self, value):
        raise NotImplementedError

    @property
    def shape(self):
        """Shape of the stream's data.

        When reading data, the shape of the stream is typically defined by the shape of the data in `source`, therefore
        the shape is recursively set to `parent` as well.
        However, when writing data, the shape is defined by the user, and the stream's parent might not be set. In this
        case, we store the shape in `_shape`.

        Raises
        ------
        Exception
            If trying to set the shape when it is already defined (by a parent StreamFile).
        ValueError
            If setting the shape with an invalid type.

        Returns
        -------
        :obj:`tuple` of int
            Shape.
        """
        # if parent is file return dataset shape
        if isinstance(self.parent, StreamFile):
            return self.parent.get_stream_shape(self.name)
        # if has parent return parent shape
        elif self.parent is not None:
            return self.parent.shape
        # if parent is None return internal _shape
        # This case typically happen when writing data: in this case the shape is not defined by the data in the source.
        else:
            return self._shape

    @shape.setter
    def shape(self, value):
        # can only set shape if undefined
        if self.shape is not None:
            raise Exception("shape is already set")
        # set dataset dimension (should this be allowed?)
        if isinstance(self.parent, StreamFile):
            self.parent.set_dataset_shape(name=self.name, shape=value)
        # set recursively
        elif self.parent is not None:
            self.parent.shape = value
        else:
            if isinstance(value, tuple):
                self._shape = value
            else:
                raise ValueError("shape must be a tuple of int or None")

    @property
    def ndim(self):
        """Number of dimension in the stream's data.

        Returns
        -------
        int
            Number of dimension.
        """
        return len(self.shape)

    @property
    def timestamps(self):
        """Timestamp of each frame in the stream's data.

        Returns
        -------
        :obj:`numpy.ndarray`
            Timestamps.
        """
        if isinstance(self.parent, StreamFile):
            return self.parent.get_stream_timestamps(self.name)
        else:
            return self.parent.timestamps

    @timestamps.setter
    def timestamps(self, value):
        raise NotImplementedError

    @property
    def bounding_box(self):
        """Bounding box at each frame in the stream.

        A StreamArray member is provided to allow the user easily store their bounding boxes with the stream's data.

        Returns
        -------
        :obj:`~bob.io.stream.StreamArray`
            Bounding boxes.
        """
        if isinstance(self.parent, StreamFile):
            return self.__bounding_box
        else:
            return self.parent.bounding_box

    @property
    def image_points(self):
        """Landmarks at each frame in the stream.

        A StreamArray member is provided to allow the user easily store their landmark points with the stream's data.

        Returns
        -------
        :obj:`~bob.io.stream.StreamArray`
            Landmarks.
        """
        if isinstance(self.parent, StreamFile):
            return self.__image_points
        else:
            return self.parent.image_points

    def __getitem__(self, index):
        """Data access: returns either a frame (if index is int) or a StreamView (if index is a slice or a tuple).

        Implementation is similar to numpy's: when only 1 frame is requested (`index` is an int), return the frame 
        - not a Stream containing only 1 frame ; when several frames are requested, return a Stream containing the 
        requested frames. This last case is implemented using the :class:`~bob.io.stream.Stream.StreamView".

        Parameters
        ----------
        index : int or :obj:`slice` or :obj:`tuple` of int
            Indices of the data to load.

        Returns
        -------
        :obj:`numpy.ndarray` or :obj:`~bob.io.stream.Stream`
            A frame if only one was requested. If a slice was requested, return a :obj:`~bob.io.stream.StreamView`.

        Raises
        ------
        ValueError
            If indices in `index` are of the wrong type.
        ValueError
            If index does not have a supported type.
        """
        # case 1: index is int: load and return a frame.
        if isinstance(index, int):
            data = self.load(index)
            return data[0]
        # case 2: index is slice: it acts on first dimension only so pack it in a tuple
        elif isinstance(index, slice):
            view_indices = (index,)
        # case 3: index is tuple: validate each index
        elif isinstance(index, tuple):
            # we do not check dimensionality here, because it can be varying if the pipeline has no source
            for i in index:
                if isinstance(i, int):
                    pass
                elif isinstance(i, slice):
                    pass
                else:
                    raise ValueError(
                        "Got index "
                        + str(i)
                        + " of type "
                        + str(type(i))
                        + " in "
                        + str(index)
                        + ", but only support int or slice."
                    )
            view_indices = index
        else:
            raise ValueError(
                "index can only be int, slice or tuple, but got " + str(index) + " of type " + str(type(index))
            )
        # case 2 & 3: return stream_view
        return self.view(view_indices=view_indices)

    def __setitem__(self, index, data):
        raise NotImplementedError

    def load(self, index=None):
        """Load data directly.

        Unlike accessing stream data through brackets [], this method always returns the data, not a Stream.
        This method is overloaded in :class:`~bob.io.stream.StreamFilter`, in order to call `parent` load method first
        and apply processing on the result.

        The loaded data is buffered to reduce disk access.

        Parameters
        ----------
        index : int or :obj:`list`
            Indices of the frames to load, by default None.

        Returns
        -------
        :obj:`numpy.ndarray`
            Data at `index`.
        """
        indices = get_index_list(index, self.shape[0])
        # return buffered data OR load from file
        if self._loaded == indices and self._data is not None:
            pass
        else:
            self._data = self.parent.load_stream_data(self.name, indices)
        # buffer loaded indices
        self._loaded = indices
        return self._data

    # TODO define behaviour across all states
    def put(self, data, timestamp=None):
        """Recursivelly pass `data` down to `child` to write in hdf5File.

        :class:`~bob.io.stream.StreamFilter` overloads this method to process `data` with the filter function before 
        passing down to child.

        Parameters
        ----------
        data : :obj:`numpy.ndarray`
            data to write to file.
        timestamp : int or float
            Timestamp of `data`, by default None.

        Raises
        ------
        ValueError
            If `data`'s shape does not match with previous frames' shape or with stream's shape..
        """
        # set _shape to keep track of size of frames
        if self._shape is None:
            self._shape = tuple([None, *data.shape])
        # check if same shape
        elif data.shape != self._shape[1:]:
            raise ValueError(
                "Expected data with shape "
                + str(data.shape)
                + " to have same shape "
                + str(self._shape[1:])
                + ' as previous frames. Use "reset"'
                " to reset the stream's shape."
            )
        # pass down the chain for writing.
        if self.child is not None:
            self.child.put(data, timestamp)

    def get_available_filters(self):
        """Get a list of the available filters to use with :class:`~bob.io.stream.Stream` class.

        Note: Stream.filters is filled in with the name of the filters by the :func:`~bob.io.stream.stream_filter` 
        decorator, each time a class is decorated.

        Returns
        -------
        :obj:`list` of str
            List of available filters in the :class:`~bob.io.stream.Stream` class. The filters can be used as 
            "stream.filter()"
        """
        return Stream.filters

    def get_parent(self):
        """Return this stream's parent (None if `parent` is not set)

        Returns
        -------
        :obj:`~bob.io.stream.Stream`
            This stream's parent.
        """
        return self.parent


##################################################################
# Decorator to add Filters to the Stream class
def stream_filter(name):
    """Adds the filter with `name` to the :class:`~bob.io.stream.Stream` class.

    This decorator function is meant to be used on a filter class that inherits the :class:`~bob.io.stream.Stream` 
    class. It adds this filter to the :class:`~bob.io.stream.Stream` class so it can be used directly as a member. It 
    also adds it to the :obj:`~bob.io.stream.Stream.filters` list.

    For example, see the :class:`~bob.io.stream.StreamView` filter.
    
    Parameters
    ----------
    name : str
        Name of the filter
    """

    def wrapper(Filter):
        def filter(self, *args, **kwargs):
            return Filter(name=name, parent=self, *args, **kwargs)

        # add the filter to the Stream class.
        setattr(Stream, name, filter)
        # Append it to the filtes list.
        Stream.filters.append(name)
        return Filter

    return wrapper


##################################################################
# StreamFilter class: base class for filters.
@stream_filter("filter")
class StreamFilter(Stream):
    """Base filter class: overloads the :meth:`bob.io.stream.Stream.load` and :meth:`bob.io.stream.Stream.put` methods 
    to insert the filter processing.

    This class implements the :meth:`~bob.io.stream.StreamFilter.process` and 
    :meth:`bob.io.stream.StreamFilter.process_frame`  methods, which define the processing operated by the filter. A 
    "process_frame" method can be receive in argument, in which case it will be applied to each frame of data in 
    :meth:`~bob.io.stream.StreamFilter.process_frame`. If not provided, this filter doesn't perform any processing, 
    however it provides the definition of the processing methods which can be overloaded in inheriting classes. See for
    example :class:`~bob.io.stream.StreamView` filter.


    The :meth:`bob.io.stream.Stream.load` is overloaded to first perform the filter's `parent` processing (or loading 
    if `parent` is not a filter)
    The :meth:`bob.io.stream.Stream.put` methods is overloaded to first perform the processing of the filter, then pass
    the data down to `child` to further process or write on disk.

    Attributes
    ----------
    filter_name : str
        The name of this filter. `name` (from class :class:`bob.io.stream.Stream`) is kept separate because it is used 
        to know from which dataset to load data in the hdf5.
    """

    def __init__(self, name, parent, process_frame=None):
        """Register `process_frame` if provided, and intialize super. 

        Parameters
        ----------
        name : str
            "filter": identifier name to use this filter from the :obj:`~bob.io.stream.Stream` class.
        parent : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
            Parent Stream(Filter).
        process_frame : :obj:`Callable`
            Process_frame function, by default None.
        """
        self.__process_frame = process_frame
        self.filter_name = name
        super().__init__(name=parent.name, parent=parent)

    def process(self, data, indices):
        """Apply the filter on each frame of data, and stack the results back in one array.

        Parameters
        ----------
        data : :obj:`numpy.ndarray`
            Data to process.
        indices : :obj:`list` of int
            Indices of `data` in the stream. Unused here, but usefull for instance for filters that combine two streams
            together.

        Returns
        -------
        :obj:`numpy.ndarray`
            Processed data.

        Raises
        ------
        ValueError
            If indices is not a list.
        """
        if not isinstance(indices, list):
            raise ValueError("Indices should be a list, but got " + str(type(indices)))
        return np.stack([self.process_frame(data[i], i, indices[i]) for i in range(data.shape[0])])

    def process_frame(self, data, data_index, stream_index):
        """Apply `self.__process_frame` if possible, otherwise simply return data.

        Parameters
        ----------
        data : :obj:`numpy.ndarray`
            Data (one frame) to process.
        data_index : int
            Not used. Index of `data` in the stream.
        stream_index : int
            Not used. Index of the stream from which `data` comes, to be used by filters that combine several streams.

        Returns
        -------
        :obj:`numpy.ndarray`
            Processed frame.
        """
        if self.__process_frame is not None:
            return self.__process_frame(data)
        else:
            return data

    # load one or several frames
    def load(self, index=None):
        """Overload :meth:`bob.io.stream.Stream.load` to apply the filter processing what `parent` loaded.

        Parameters
        ----------
        index : int or :obj:`list` of int
            Indices of the frames to load, by default None.

        Returns
        -------
        :obj:`numpy.ndarray`
            The processed data.
        """
        indices = get_index_list(index, self.shape[0])
        # return buffered data OR process parent's data.
        if self._loaded == indices and self._data is not None:
            # print('loaded', self.name)
            pass
        else:
            self._data = self.process(self.parent.load(indices), indices)

        # buffer loaded indices.
        self._loaded = indices
        return self._data

    # TODO define behaviour across all states
    def put(self, data, timestamp=None):
        """Apply filter's processsing, then pass down `data` to child for further processing or save on disk.

        Parameters
        ----------
        data : :obj:`numpy.ndarray`
            Data (one frame) to process.
        timestamp : int or float
            Timestamp of `data` in the stream, by default None.
        """
        # set _shape to keep track of size of frames
        if self._shape is None:
            self._shape = tuple([None, *data.shape])
        # check if same shape
        elif data.shape != self._shape[1:]:
            raise ValueError(
                "Expected data with shape "
                + str(data.shape)
                + " to have same shape "
                + str(self._shape[1:])
                + " as previous frames."
            )
        indices = [-1]  # data is appended to the previous frames, so index can be -1: implies frame is the latest.
        data = np.stack([data])  # create a set of frames (with 1 frame) to match what `process` is expecting.
        data = self.process(data, indices)
        data = data[0]  # go back to manipulating only 1 frame.
        # buffer processed index and data.
        self._loaded = indices
        self._data = data
        # pass down to children until writing to disk.
        if self.child is not None:
            self.child.put(data, timestamp)


################################################################################
# Filters implementing important functionalities of the Stream class


@stream_filter("view")
class StreamView(StreamFilter):
    """Filter to implement "slicing" functionality for the :class:`bob.io.stream.Stream` class.

    Similarly to numpy's "view", this filter allows to take a slice in a stream without creating a copy of the data.

    Attributes
    ----------
    frame_view : :obj:`slice` or None
        Slice value in the first dimension of the stream (along the frame's axis). None means no slicing: take the 
        whole array.
    bulk_view : :obj:`tuple` of int or :obj:`slice` or None
        Slice value along the other axis in the stream.
    """

    def __init__(self, name, parent, view_indices=None):
        """Initializes the stream and checks that the requested slice is properly defined.

        Parameters
        ----------
        name : str
            "view": identifier name to use this filter from the :obj:`~bob.io.stream.Stream` class.
        parent : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
            Parent Stream(Filter).
        view_indices : :obj:`tuple` of int or :obj:`slice`
            Indices defining the slice, by default None (meaning no slicing: take the whole array).

        Raises
        ------
        ValueError
            If indices type are not supported.
        ValueError
            If `view_indices` type is not supported.
        ValueError
            If the slice would result in an empty stream.
        ValueError
            If the requested slice has more dimension than are available in the stream.
        """
        super().__init__(name=name, parent=parent)
        self.frame_view = None
        self.bulk_view = None
        if isinstance(view_indices, tuple):
            # separate frame (axis = 0) and bulk (axis > 0) views
            self.frame_view = view_indices[0]
            # TODO should case with int on frame index be allowed?
            if isinstance(self.frame_view, int):
                raise ValueError(
                    "Can not slice into a single frame. To perform this operation, select first the frame and apply "
                    "slicing on the numpy array."
                )
            # bulk views
            if len(view_indices) > 1:
                self.bulk_view = view_indices[1:]
                for e in self.bulk_view:
                    if isinstance(e, int) or isinstance(e, slice) or e is None:
                        pass
                    else:
                        raise ValueError(
                            "Incorrect type of index: received "
                            + str(type(e))
                            + " in "
                            + str(view_indices)
                            + ". Indices should be a tuple of int/slice or None."
                        )
        elif view_indices is None:
            pass
        else:
            raise ValueError(
                "Indices should be a tuple of int/slice or None, but got "
                + str(view_indices)
                + " of type "
                + str(type(view_indices))
                + "."
            )

        if not all(self.shape):  # true if a dimension in shape is 0: resulting stream has no data.
            if not all(self.shape):
                raise ValueError(
                    str(view_indices)
                    + " in stream with shape "
                    + str(parent.shape)
                    + " results in empty stream. (shape "
                    + str(self.shape)
                    + ")"
                )

        # If slice operates on more dimension than available.
        if self.bulk_view is not None and self.parent.ndim <= len(self.bulk_view):
            raise ValueError(
                "Got "
                + str(len(self.bulk_view) + 1)
                + " indices for stream with shape "
                + str(self.parent.shape)
                + ". Too many indices !"
            )

    # shape property
    @property
    def shape(self):
        """Shape of the stream's data.

        The shape is computed with respect to the parent's shape, because `source` might not be set so we can not know 
        the shape of the data. If the requested slice has a integer index along one axis, this dimension is dropped. 
        However, taking an integer along the first axis is not allowed (Exception raised in __init__).

        Returns
        -------
        :obj:`tuple` of int
            Shape of the stream's data.
        """
        # first dimension ...
        __shape = [get_axis_size(self.parent.shape, 0, self.frame_view)]
        # ... and others
        for d in range(1, self.parent.ndim):
            if self.bulk_view is not None and d - 1 < len(self.bulk_view):
                __view_index = self.bulk_view[d - 1]
                # don't add axis to shape if integer index
                if isinstance(__view_index, int):
                    pass
                else:
                    __shape.append(get_axis_size(self.parent.shape, d, __view_index))
            else:
                __shape.append(get_axis_size(self.parent.shape, d))
        return tuple(__shape)

    @property
    def ndim(self):
        """Number of dimension of the stream's data.

        If the requested slice has an integer along an axis, this dimension is collapsed, otherwise the number of 
        dimension is the same as `parent`'s.

        Returns
        -------
        int
            Number of dimension.
        """
        __ndim = self.parent.ndim
        if self.frame_view is not None and isinstance(self.frame_view, int):
            __ndim -= 1
        if self.bulk_view is not None:
            for a in self.bulk_view:
                if isinstance(a, int):
                    __ndim -= 1
        return __ndim

    def load(self, index=None):
        """Load stream's data at the corresponding indices.

        Maps `index` to indices in `parent` and delegate loading.

        Parameters
        ----------
        index : int or :obj:`list` of int or :obj:`slice`
            Indices of the data to load.

        Returns
        -------
        :obj:`numpy.ndarray`
            Data at `index` in the stream.
        """
        parent_indices = get_index_list(self.frame_view, self.parent.shape[0])
        view_indices = get_index_list(index, self.shape[0])
        indices = [parent_indices[i] for i in view_indices]
        return super().load(indices)

    def process(self, data, indices):
        """Apply slicing on each frame of `data`.

        The slicing of the frame's axis is performed in :meth:`bob.io.stream.StreamView.load`, so that `data` only
        contains frames that are requested. It remains to apply the slicing along the other axis in `data`, which is 
        delegarted to :meth:`~bob.io.stream.StreamView.process_frame` (by slicing into the numpy arrays). Here we only 
        store the requested slice in full format (value along all axis).

        Parameters
        ----------
        data : :obj:`numpy.ndarray`
            Data to slice. Slicing on the first axis is already performed.
        indices : int or :obj:`list` of int
            Indices of `data` in the stream.

        Returns
        -------
        :obj:`numpy.ndarray`
            Sliced data.
        """
        # generate full bulk view
        __bulk_view_full = [slice(None, None, None) for d in range(self.parent.ndim - 1)]
        if self.bulk_view is not None:
            for d in range(self.ndim - 1):
                if d < len(self.bulk_view):
                    if self.bulk_view[d] is not None:
                        # should be int or slice
                        __bulk_view_full[d] = self.bulk_view[d]
        self.__bulk_view_full = tuple(__bulk_view_full)
        return super().process(data, indices)  # super stacks the result of process_frame.

    def process_frame(self, data, data_index, stream_index):
        """Apply the slicing on a frame of data.

        Apply the frame slicing computed in :meth:`~bob.io.stream.StreamView.process` on a frame.

        Parameters
        ----------
        data : :obj:`numpy.ndarray`
            Frame of data.
        data_index : int
            Not used. Present for compatibility with other filters.
        stream_index : int
            Not used. Present for compatibility with other filters.

        Returns
        -------
        :obj:`numpy.ndarray`
            Sliced data.
        """
        return data[self.__bulk_view_full]


@stream_filter("save")
class StreamSave(StreamFilter):
    """Filter to save frames of data to a :class:`~bob.io.stream.StreamFile`.

    Saving is performed by appending to the streamfile.

    Attributes
    ----------
    file : :obj:`~bob.io.stream.StreamFile`
        StreamFile into which the data will be appended.
    """

    def __init__(self, file, name, parent):
        """Initializes stream and register the output :obj:`~bob.io.stream.StreamFile`.

        Parameters
        ----------
        file : :obj:`~bob.io.stream.StreamFile`
            Output file.
        name : str
            "save": identifier name to use this filter from the :obj:`~bob.io.stream.Stream` class.
        parent : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
            Parent Stream(Filter).
        """
        super().__init__(name=name, parent=parent)
        self.file = file
        if not isinstance(self.file, StreamFile):
            raise ValueError("Output file is not a valid StreamFile.")

    def put(self, data, timestamp=None):
        """Pass data and timestamp to the :obj:`~bob.io.stream.StreamFile` to write to disk.

        Parameters
        ----------
        data : :obj:`numpy.ndarray`
            data to write to file.
        timestamp : int or float
            Timestamp of `data`, by default None.
        """
        self.file.put_frame(self.name, data, timestamp)


################################################################################
# General use filters


@stream_filter("astype")
class StreamAsType(StreamFilter):
    """Filter to cast the data to a different numpy dtype.

    Attributes
    ----------
    dtype : :obj:`numpy.dtype`
        The dtype to which to cast the data.
    """

    def __init__(self, name, parent, dtype):
        """Set `dtype` and initializes super().

        Parameters
        ----------
        name : str
            "astyype": identifier name to use this filter from the :obj:`~bob.io.stream.Stream` class.
        parent : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
            Parent Stream(Filter).
        dtype : :obj:`numpy.dtype`
            dtype to cast to.
        """
        super().__init__(name=name, parent=parent)
        self.dtype = dtype

    def process(self, data, indices):
        """Cast `data` to `dtype`.

        Parameters
        ----------
        data : :obj:`numpy.ndarray`
            Data to cast.
        indices : int or :obj:`list` of int
            Not used. Present for compatibility with other filters.

        Returns
        -------
        :obj:`numpy.ndarray`
            `data` casted to `dtype`.
        """
        return data.astype(self.dtype)


@stream_filter("adjust")
class StreamAdjust(StreamFilter):
    """Filter that allows to use 2 streams with different timestamps seamlessly by taking the closest time neighbors.

    Streams frames are not necessarily simultaneous: some streams may be delayed, some might have less frames... However 
    the timestamps of each frames are available. Given the timestamps of the `parent` stream, this filter implements a 
    nearest neighbor search in the timestamps of the `adjust_to` stream to load the closest frame.

    This stream emulates the `adjust_to` number of frames and timestamps to facilitate operations on streams.

    Attributes
    ----------
    adjust_to : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
        Stream relatively to which the timestamps will be adjusted.
    """

    def __init__(self, adjust_to, name, parent):
        """Set super and register `adjust_to`.

        Parameters
        ----------
        adjust_to : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
            Stream to which `parent` is adjusted.
        name : str
            "adjust": identifier name to use this filter from the :obj:`~bob.io.stream.Stream` class.
        parent : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
            Parent Stream(Filter).
        """
        super().__init__(name=name, parent=parent)
        self.adjust_to = adjust_to

    def set_source(self, src):
        """Set `self` and `adjust_to` sources to `src`.

        Parameters
        ----------
        src : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFile`
            Source Stream or StreamFile.
        """
        super().set_source(src)
        self.adjust_to.set_source(src)

    @property
    def shape(self):
        """Stream's data shape. The number of frames is equal to `adjust_to`.

        Returns
        -------
        :obj:`tuple` of int
            Shape of the Stream's data.
        """
        return (self.adjust_to.shape[0], self.parent.shape[1], self.parent.shape[2], self.parent.shape[3])

    @property
    def timestamps(self):
        """Stream's timestamps, equal to `adjust_to` after adjustment.

        Returns
        -------
        :obj:`numpy.ndarray`
            Timestamps of the frames in the stream.
        """
        return self.adjust_to.timestamps

    def load(self, index):
        """Load frame(s) at index.

        `index` is the index of a frame in `adjust_to`. The closest frame in `self` is found using nearest neighbor 
        search, then the data is loaded.

        Parameters
        ----------
        index : int or :obj:`list` of int or slice
            Indices of the frames to load.

        Returns
        -------
        :obj:`numpy.ndarray`
            Stream's data at `index`.
        """
        # original stream indices
        old_indices = get_index_list(index, self.shape[0])
        selected_timestamps = [self.adjust_to.timestamps[i] for i in old_indices]
        kdtree = cKDTree(self.parent.timestamps[:, np.newaxis])

        def get_index(val, kdtree):
            _, i = kdtree.query(val, k=1)
            return i

        new_indices = [get_index(ts[np.newaxis], kdtree) for ts in selected_timestamps]

        return super().load(new_indices)
