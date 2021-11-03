from .stereo import stereo_match, reproject_image
from .camera import load_camera_config, Camera, CameraPair
from .parameters import StereoParameters
from .stereo_stream_filters import add_stream_camera, StreamWarp, StreamStereo, StreamReproject

# Modify bob.io.stream.Stream and bob.io.stream.StreamFile classes to add camera configs.
add_stream_camera()

# gets sphinx autodoc done right - don't remove it
def __appropriate__(*args):
    """Says object was actually declared here, and not in the import module.
    
    Fixing sphinx warnings of not being able to find classes, when path is
    shortened.
    Resolves `Sphinx referencing issues
    <https://github.com/sphinx-doc/sphinx/issues/3048>`

    Parameters
    ----------
    *args
        An iterable of objects to modify.
    """

    for obj in args:
        obj.__module__ = __name__


__appropriate__(
    stereo_match,
    reproject_image,
    load_camera_config,
    Camera,
    CameraPair,
    StereoParameters,
    StreamWarp,
    StreamStereo,
    StreamReproject,
)


def get_config():
    """Returns a string containing the configuration information.
    """

    import bob.extension

    return bob.extension.get_config(__name__)


__all__ = [_ for _ in dir() if not _.startswith("_")]

