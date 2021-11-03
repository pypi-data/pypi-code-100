"""This file contains the code implementing stereo operations as :class:`bob.io.stream.StreamFilter`

In order to use stereo operations, we need information about the relative position of the camera associated with each
stream of data. This is done by modifying the :clas:`bob.io.stream.Stream` class, in the 
:func:`~bob.ip.stereo.add_stream_camera` function, which adds methods to register the camera configuration file and 
return the camera of a stream.  
The :func:`~bob.ip.stereo.add_stream_camera` function is executed in __init__.py so that the modifications are operated
when bob.ip.stereo is imported.

3 filters are implemented:
- StreamWarp - to wrap images from a stream to the shape (x,y size) of another stream.
- StreamStereo - to build a 3d map
- StreamReproject - to reproject a stream onto another, using a 3d map.
"""

from .camera import load_camera_config

import bob.io.stream

from skimage import transform


def add_stream_camera():

    #################################################
    # Modify StreamFile class to get camera configs.

    # Add method to set camera_file_path to StreamFile
    def set_camera_configs(self, camera_config_file_path):
        self.camera_config = load_camera_config(camera_config_file_path)

    setattr(bob.io.stream.StreamFile, "set_camera_configs", set_camera_configs)

    # Add get_camera method to StreamFile (a StreamFile must be parent of all Streams instance, so this method will be
    # found by a stream looking for its camera)
    def get_stream_camera(self, stream_name):
        data_config = self.get_stream_config(stream_name)
        if "use_config_from" in data_config:
            data_config = self.get_stream_config(data_config["use_config_from"])
        if "camera" in data_config:
            camera_name = data_config["camera"]
            if camera_name in self.camera_config:
                return self.camera_config[camera_name]
            else:
                raise ValueError("invalid camera name")
        else:
            return None

    setattr(bob.io.stream.StreamFile, "get_stream_camera", get_stream_camera)

    #################################################
    # Modify Stream class to add camera property

    # Add camera property to Stream class
    @property
    def camera(self):
        """Camera object corresponding to this stream's data.

        Returns
        -------
        :obj:`bob.ip.stereo.Camera`
            Camera.
        """

        if isinstance(self.parent, bob.io.stream.StreamFile):
            return self.parent.get_stream_camera(self.name)
        else:
            return self.parent.camera

    @camera.setter
    def camera(self, value):
        raise NotImplementedError

    setattr(bob.io.stream.Stream, "camera", camera)


########################################################################################################################
# stereo filters
########################################################################################################################


from .parameters import StereoParameters
from .stereo import stereo_match, reproject_image
from .camera import CameraPair

from bob.io.stream import StreamArray, Stream, StreamFilter, stream_filter

import numpy as np


@bob.io.stream.stream_filter("warp")
class StreamWarp(bob.io.stream.StreamFilter):
    """Filter to warp a stream images to the dimension of another stream.

    Attributes
    ----------
    warp_to : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
        The data in `parent` will be warped to the dimension of `warp_to`.
    """

    def __init__(self, warp_to, name, parent):
        """Set super() and register `warp_to`.

        Parameters
        ----------
        warp_to : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
            The dimension of this stream will be used to warp.
        name : str
            "warp": identifier name to use this filter from the :obj:`~bob.io.stream.Stream` class.
        parent : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
            Parent Stream(Filter).
        """
        super().__init__(name=name, parent=parent)
        self.warp_to = warp_to

    def set_source(self, src):
        """Set `self` and `warp_to` source to `src`.

        Parameters
        ----------
        src : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFile`
            Source Stream or StreamFile.
        """
        super().set_source(src)
        self.warp_to.set_source(src)

    @property
    def shape(self):
        """Shape of the stream's data. The image width and height are those of `warp_to` after warping.

        Returns
        -------
        :obj:`tuple` of int
            Shape of the stream's data.
        """
        return (self.parent.shape[0], self.parent.shape[1], self.warp_to.shape[2], self.warp_to.shape[3])

    def process(self, data, indices):
        """Warp `data` at `indices` to the output shape of `warp_to`.

        This function sets the warp transform, the computation is done in 
        :meth:`~bob.ip.stereo.StreamWarp.process_frame`.

        Parameters
        ----------
        data : :obj:`numpy.ndarray`
            The stream's data, to be warped.
        indices : int or :obj:`list` of int
            Indices of `data`.

        Returns
        -------
        :obj:`numpy.ndarray`
            `data` warped to `warp_to` image shape.
        """
        if self.warp_to.camera.markers is None or self.camera.markers is None:
            raise ValueError("Camera markers are not defined ! Did you run linear calibration of your cameras ?")
        self.markers = (self.warp_to.camera.markers, self.camera.markers)  # camera added to Stream by add_stream_camera
        self.warp_transform = transform.ProjectiveTransform()
        self.warp_transform.estimate(*self.markers)
        self.output_shape = (self.warp_to.shape[2], self.warp_to.shape[3])

        return super().process(data, indices)

    def process_frame(self, data, data_index, stream_index):
        """Warp `data` to `warp_to` image width and height.

        Parameters
        ----------
        data : :obj:`numpy.ndarray`
            `parent` frame at `data_index`.
        data_index : int
            Not used. Present for compatibility with other filters.
        stream_index : int
            Not used. Present for compatibility with other filters.

        Returns
        -------
        :obj:`numpy.ndarray`
            Warped `data`.
        """
        output = []
        num_chan = data.shape[0]
        for c in range(num_chan):
            output.append(
                transform.warp(
                    data[c], self.warp_transform, output_shape=self.output_shape, preserve_range=True
                ).astype(data.dtype)
            )
        output = np.stack(output)

        return output


@bob.io.stream.stream_filter("stereo")
class StreamStereo(bob.io.stream.StreamFilter):
    """Filter to compute a 3d map given images from `parent` and `match_with_stream`.

    Attributes
    ----------
    match_with_stream : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
        `parent` and `match_with_stream` are used in stereo to build the 3d maps.
    """

    def __init__(self, match_with_stream, name, parent, stereo_parameters=StereoParameters()):
        """Set super and register `match_with_stream`.

        Parameters
        ----------
        match_with_stream : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
            Stream used with `parent` to build 3d map.
        name : str
            "stereo": identifier name to use this filter from the :obj:`~bob.io.stream.Stream` class.
        parent : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
            Parent Stream(Filter).
        stereo_parameters : :obj:`bob.ip.stereo.StereoParameters`
            Parameters of stereo algorithms, by default StereoParameters().
        """
        super().__init__(name=name, parent=parent)
        self.match_with_stream = match_with_stream
        self.stereo_parameters = stereo_parameters

    def set_source(self, src):
        """Set `self` and `match_with_stream` sources to `src`.

        Parameters
        ----------
        src : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFile`
            Source stream or stream file.
        """
        super().set_source(src)
        self.match_with_stream.set_source(src)

    def process(self, data, indices):
        """Compute 3d map at `indices` from `data` and `match_with_stream`'s data.

        This function loads `match_with_stream`'s data and set the camera pair for the stereo algorithm. The actual 
        computation is performed in :meth:`bob.ip.stereo.StreamStereo.process_frame`.

        Parameters
        ----------
        data : :obj:`numpy.ndarray`
            `data` at `indices`.
        indices : int or :obj:`list` or int
            Indices of `data`.

        Returns
        -------
        :obj:`numpy.ndarray`
            3d map at `indices`.
        """
        self.camera_pair = CameraPair(self.camera, self.match_with_stream.camera)
        self.right_data = self.match_with_stream.load(indices)
        return super().process(data, indices)

    def process_frame(self, data, data_index, stream_index):
        """Computes 3d map using `data` from `parent` and `self.right_data` from `match_with_stream`.

        Parameters
        ----------
        data : :obj:`numpy.ndarray`
            Data at `data_index` from parent stream.
        data_index : int
            Index of the frame (`data`) that is processed.
        stream_index : int
            Not used. Present for compatibility with other filters.

        Returns
        -------
        :obj:`numpy.ndarray`
            3d map.
        """
        return stereo_match(
            data, self.right_data[data_index], self.camera_pair, stereo_parameters=self.stereo_parameters
        )


@bob.io.stream.stream_filter("reproject")
class StreamReproject(bob.io.stream.StreamFilter):
    """Filter to project an image onto `left_stream` camera, using `map_3d` build from `left_stream` and `right_stream`.

    Attributes
    ----------
    left_stream : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
        Stream onto which the data will be projected.
    right_stream : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
        Stream used to build `map_3d` using stereo algorithms.
    map_3d : :obj:`~bob.ip.stereo.StreamStereo`
        3d map filter.
    """

    def __init__(self, left_stream, right_stream, map_3d, name, parent):
        """Set super and register `left_stream`, `right_stream` and `map_3d`.

        Parameters
        ----------
        left_stream : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
            Stream onto which the data will be projected.
        right_stream : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
            Stream used to build `map_3d`.
        map_3d : :obj:`~bob.ip.stereo.StreamStereo`
            3d map filter.
        name : str
            "reproject": identifier name to use this filter from the :obj:`~bob.io.stream.Stream` class.
        parent : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFilter`
            Parent Stream(Filter).
        """
        super().__init__(name=name, parent=parent)
        self.left_stream = left_stream
        self.right_stream = right_stream
        self.map_3d = map_3d
        self.__bounding_box = StreamArray(self)
        self.__image_points = StreamArray(self)

    def set_source(self, src):
        """Set `self`, `left_stream`, `right_stream` and `map_3d` sources to `src`.

        Parameters
        ----------
        src : :obj:`~bob.io.stream.Stream` or :obj:`~bob.io.stream.StreamFile`
            Source Stream or StreamFile.
        """
        super().set_source(src)
        self.left_stream.set_source(src)
        self.right_stream.set_source(src)
        self.map_3d.set_source(src)

    @property
    def shape(self):
        """:obj:`tuple` of int: Shape of the stream's data. The projected image has the width and height of the 3d map."""
        return (self.parent.shape[0], self.parent.shape[1], self.map_3d.shape[2], self.map_3d.shape[3])

    @property
    def bounding_box(self):
        """:obj:`~bob.io.stream.StreamArray`: Bounding box at each frame of the stream."""
        return self.__bounding_box

    @property
    def image_points(self):
        """:obj:`~bob.io.stream.StreamArray`: Landmarks at each frame of the stream."""
        return self.__image_points

    def process(self, data, indices):
        """Project `data` onto `left_stream`'s camera.

        The method loads `map_3d`'s data and sets the `CameraPair` from `stream_left` and `stream_right`. The actual 
        projection is performed frame per frame in :meth:`bob.ip.stereo.StreamReproject.process_frame`.

        Parameters
        ----------
        data : :obj:`numpy.ndarray`.
            Image(s) from `parent` at `indices` to project.
        indices : int or :obj:`list` of int
            Indices of `data`.

        Returns
        -------
        :obj:`numpy.ndarray`
            `data` projected onto `left_stream` camera.
        """
        self.map_3d_data = self.map_3d.load(indices)
        self.camera_pair = CameraPair(self.left_stream.camera, self.right_stream.camera)
        return super().process(data, indices)

    def process_frame(self, data, data_index, stream_index):
        """Projects `data` image onto `left_stream` camera.

        Parameters
        ----------
        data : :obj:`numpy.ndarray`
            `parent` frame at `data_index`.
        data_index : int
            Not used. Present for compatibility with other streams.
        stream_index : int
            Not used. Present for compatibility with other streams.

        Returns
        -------
        :obj:`numpy.ndarray`
            Projected `data`.
        """
        # copy parent's bounding box
        bounding_box = self.parent.bounding_box[stream_index]
        if bounding_box is not None:
            # TODO do type checking in StreamArray
            assert isinstance(bounding_box, np.ndarray)
            assert bounding_box.shape[0] == 2
            assert bounding_box.shape[1] == 2
            bounding_box = np.copy(bounding_box)
            self.__bounding_box[stream_index] = bounding_box
        # copy parent's image points
        image_points = self.parent.image_points[stream_index]
        if image_points is not None:
            assert isinstance(image_points, np.ndarray)
            assert image_points.shape[1] == 2
            image_points = np.copy(image_points)
            self.__image_points[stream_index] = image_points
        # reproject
        return reproject_image(
            data,
            self.map_3d_data[data_index],
            self.camera,
            self.camera_pair,
            bounding_box=bounding_box,
            image_points=image_points,
        )
