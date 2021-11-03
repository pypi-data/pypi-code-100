"""Video streams file reader/writer.

This module implements the :class:`bob.io.stream.StreamFile` class to read and write data and meta-data inside hdf5 
files containing recordings of video. The class is designed to load into memory only the requested frames of data to 
minimize disk access. Using configuration dictionaries, the data can be processed into an expected format, and 
information such timestamps can be retrivied for the streams of data in the files.
"""


import json
import numpy as np

from bob.io.base import HDF5File

from .config import load_data_config


class StreamFile:
    """File class to read and write from HDF5 files.

    Exposes methods to read a stream's data and meta-data. The format of the data in the hdf5 file is defined through a 
    configuration dictionary.
    
    The class can also be used to write a HDF5 file, through the :meth:`~bob.io.stream.StreamFile.put_frame` method. 
    This operates by appending, one frame at a time, data to a file.

    Attributes
    ----------
    hdf5_file : :py:class:`bob.io.base.HDF5File`
        HDF5 file containing the streams data.
    data_format_config : str
        Path to configuration json with the streams data meta-data (names, shape, etc...)
    """

    def __init__(self, hdf5_file=None, data_format_config_file_path=None, mode="r"):
        """Open the HDF5 and register the data configuration via :meth:`bob.io.stream.StreamFile.set_source`.
        """
        self.hdf5_file = None
        self.data_format_config = None
        self.set_source(hdf5_file, data_format_config_file_path, mode)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(self.hdf5_file, HDF5File):
            self.hdf5_file.close()

    def set_source(self, hdf5_file=None, data_format_config_file_path=None, mode="r"):
        """Open the HDF5 file and load data config.

        Parameters
        ----------
        hdf5_file : :obj:`bob.io.base.HDF5File` or str or None
            File handle or path to the streams HDF5 File, by default None.
        data_format_config_file_path : str or None
            Path to the data config file, by default None.
        mode : str
            File opening mode, by default "r".
        """
        if isinstance(hdf5_file, str):  # case string: it is a path, use bob.io.base.HDF5File
            self.hdf5_file = HDF5File(hdf5_file, mode)
        elif hdf5_file is not None:  # otherwise expect an opened file object (bob.io.base.HDF5File, h5py.File, etc...)
            self.hdf5_file = hdf5_file
        else:
            self.hdf5_file = None
        if data_format_config_file_path is not None:
            self.data_format_config = load_data_config(data_format_config_file_path)
        else:
            self.data_format_config = None

    def get_available_streams(self):
        """:obj:`list` of :obj:`str`: Get the names of the streams in the HDF5 File."""

        if self.data_format_config is not None:
            return list(self.data_format_config.keys())
        else:
            # TODO list available datasets if no config present
            return None

    def get_stream_config(self, stream_name):
        """Get the `stream_name` configuration: stream name, data format, etc...

        Parameters
        ----------
        stream_name : str
            Name of the stream in the HDF5 File which meta-data is requested.

        Returns
        -------
        dict
            Stream meta-data. If the configuration is not available, return a default config contaning only the stream 
            name.
        """
        if self.data_format_config is not None:
            data_config = self.data_format_config[stream_name]
        else:
            # return a generic config if no config is present
            data_config = {"path": stream_name}
        return data_config

    def get_stream_shape(self, stream_name):
        """Get the shape of the data in in `stream_name`.

        Parameters
        ----------
        stream_name : str
            Name of the stream which shape is requested.

        Returns
        -------
        :obj:`tuple` of :obj:`int`
            Shape of the `stream_name`'s data.
        """
        data_config = self.get_stream_config(stream_name)
        data_path = data_config["path"]
        descriptor = self.hdf5_file.describe(data_path)
        # @TODO check fo other arrays types..
        shape = descriptor[1][0][1]
        return shape

    def get_stream_timestamps(self, stream_name):
        """Return the timestamps of each frame in `stream_name`.

        Parameters
        ----------
        stream_name : str
            Name of the stream which timestamps are requested.

        Returns
        -------
        :obj:`numpy.ndarray`
            Timestamps of each frame in `stream_name`
        """
        data_config = self.get_stream_config(stream_name)
        data_path = data_config["path"]
        if not self.hdf5_file.has_attribute("timestamps", data_path):
            return None
        timestamps = self.hdf5_file.get_attribute("timestamps", data_path)
        if isinstance(timestamps, np.ndarray) and len(timestamps) == 1 and isinstance(timestamps[0], np.bytes_):
            timestamps = timestamps[0]
        if isinstance(timestamps, bytes):
            timestamps = timestamps.decode("utf-8")
        if isinstance(timestamps, str):
            timestamps = np.array(json.loads("[" + timestamps.strip().strip("[").strip("]") + "]"))

        return timestamps

    def load_stream_data(self, stream_name, index):
        """Load the `index` frame(s) of data from `stream_name`.

        Loads only the requested indices from the file.
        If the stream's data configuration requests it, some axis in the loaded data are flipped.

        Parameters
        ----------
        stream_name : str
            Name of the stream which data should to be loaded
        index : int or :obj:`list` of :obj:`int`
            Index of the frame(s) to load.

        Returns
        -------
        :obj:`numpy.ndarray`
            Stream's data at frames index.

        Raises
        ------
        ValueError
            If `index` has not a valid type.
        """
        data_config = self.get_stream_config(stream_name)
        data_path = data_config["path"]
        if "use_config_from" in data_config:
            data_config = self.get_stream_config(data_config["use_config_from"])

        # load only relevant data using lread.
        if isinstance(index, int):
            data = np.stack([self.hdf5_file.lread(data_path, index)])
        elif isinstance(index, list):
            data = np.stack([self.hdf5_file.lread(data_path, i) for i in index])
        else:
            raise ValueError("index can only be int or list")

        # flip if requested
        array_flip = None
        if "array_format" in data_config:
            array_format = data_config["array_format"]
            if "flip" in array_format:
                array_flip = array_format["flip"]

        def flip_axes(data, axes):
            if axes is not None:
                for axis_name in axes:
                    data = np.flip(data, axis=int(array_format[axis_name]))
            return data

        data = flip_axes(data, array_flip)

        # TODO rotate if requested
        return data

    def put_frame(self, name, data, timestamp=None):
        """Appends `data` (a frame of a stream) to the hdf5 file.

        Parameters
        ----------
        name : str
            Path to the dataset to append to.
        data : obj:`numpy.ndarray`
            Data frame to append.
        """
        self.hdf5_file.append(name, data)
        if timestamp is not None:
            try:
                previous_timestamps = self.hdf5_file.get_attribute("timestamps", name)
            except RuntimeError:  # No previous timestamps
                previous_timestamps = []
            self.hdf5_file.set_attribute("timestamps", np.append(previous_timestamps, timestamp), name)
