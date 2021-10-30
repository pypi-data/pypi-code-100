import numpy as np
import soxr
from scipy.io import wavfile

import pkg_resources

EXAMPLE_AUDIO = "sample/sample.wav"


def example_audio_file() -> str:
    """Get the path to an included audio example file.
    Examples
    """

    return pkg_resources.resource_filename(__name__, EXAMPLE_AUDIO)


def downsample(wav, source, target):
    """wav: np.array or torch.Tensor
    source: int
    target: int"""

    if type(wav).__module__ == np.__name__:
        # return np.float64
        y = soxr.resample(wav, source, target)

    else:
        raise TypeError("wav type is np.array or torch.Tensor")

    return y
