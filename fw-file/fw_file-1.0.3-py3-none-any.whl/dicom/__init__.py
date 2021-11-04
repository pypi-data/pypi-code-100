"""dicom module."""
from .config import get_config
from .dcmdict import load_dcmdict, load_private_dictionaries
from .dicom import DICOM, TagType
from .series import DICOMCollection, DICOMSeries, build_dicom_tree
from .utils import generate_uid

__all__ = [
    "DICOM",
    "DICOMCollection",
    "DICOMSeries",
    "TagType",
    "build_dicom_tree",
    "generate_uid",
    "get_config",
    "load_dcmdict",
]


# init config (also pre-configures pydicom dataelem callbacks)
get_config()

# extend pydicom private dict (with shipped extras and DCMDICTPATH if set)
load_private_dictionaries()
