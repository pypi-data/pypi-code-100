__version__ = '0.1.0rc1'
git_version = 'a65cd2069a3871e89981e555b3d3b659bec5d879'
from torchvision.extension import _check_cuda_version
if _check_cuda_version() > 0:
    cuda = _check_cuda_version()
