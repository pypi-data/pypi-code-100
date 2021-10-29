import datetime
import logging
import sys
from collections import Counter

from fw_file.dicom import DICOM, DICOMCollection
from fw_file.dicom.config import IMPLEMENTATION_CLASS_UID, IMPLEMENTATION_VERSION_NAME
from fw_file.dicom.utils import generate_uid
from pydicom.dataelem import DataElement_from_raw
from pydicom.dataset import Dataset
from pydicom.filebase import DicomBytesIO
from pydicom.filewriter import write_data_element
from pydicom.sequence import Sequence
from tzlocal import get_localzone

from . import pkg_name
from .callbacks import empty_pydicom_callback

log = logging.getLogger(__name__)


def update_modified_dicom_info(dcm: DICOM) -> None:
    """Add OriginalAttributesSequence and Implementation information.

    Args:
        dcm (DICOM): DICOM to update.
    """

    add_implementation(dcm)
    # Modified attributes dataset
    mod_dat = Dataset()
    dcm_buffer = DicomBytesIO()
    dcm_buffer.is_little_endian = True
    dcm_buffer.is_implicit_VR = False
    for element in dcm.tracker.data_elements:
        orig = element.export()["original"]
        try:
            with empty_pydicom_callback():
                elem = DataElement_from_raw(orig)
                write_data_element(dcm_buffer, elem)
        except NotImplementedError:
            log.warning("Cannot write Original Attribute: " + str(orig))
        else:
            mod_dat[orig.tag] = orig
    # Only update if anything changed.
    if mod_dat:
        log.debug(f"Populating OriginalAttributesSequence on {dcm.localpath}")
        time_zone = get_localzone()
        curr_dt = time_zone.localize(datetime.datetime.now())
        curr_dt_str = curr_dt.strftime("%Y%m%d%H%M%S.%f%z")
        # Original attributes dataset
        orig_dat = Dataset()
        # Add Modified attributes dataset as a sequence
        orig_dat.ModifiedAttributesSequence = Sequence([mod_dat])

        orig_dat.ModifyingSystem = pkg_name

        orig_dat.ReasonForTheAttributeModification = "CORRECT"
        orig_dat.AttributeModificationDateTime = curr_dt_str

        raw = dcm.dataset.raw
        if not raw.get("OriginalAttributesSequence", None):
            raw.OriginalAttributesSequence = Sequence()
        raw.OriginalAttributesSequence.append(orig_dat)


def add_implementation(dcm: DICOM) -> None:
    """Sets implementation information to a dicom.

    Args:
        dcm (DICOM): DICOM to update.
    """
    i_class_uid = dcm.dataset.raw.file_meta.get("ImplementationClassUID")
    i_version_name = dcm.dataset.raw.file_meta.get("ImplementationVersionName")

    if not i_class_uid or i_class_uid != IMPLEMENTATION_CLASS_UID:
        log.debug(f"Adding ImplementationClassUID: {IMPLEMENTATION_CLASS_UID}")
        setattr(dcm, "ImplementationClassUID", IMPLEMENTATION_CLASS_UID)

    if not i_version_name or i_version_name != IMPLEMENTATION_VERSION_NAME:
        log.debug(f"Addding ImplementationVersionName: {IMPLEMENTATION_VERSION_NAME}")
        setattr(dcm, "ImplementationVersionName", IMPLEMENTATION_VERSION_NAME)


def add_missing_uid(dcms: DICOMCollection) -> bool:
    """Check for and add missing SeriesInstanceUID.

    Args:
        dcms (DICOMCollection): Dicom to check.

    Returns:
        (bool): Whether or not any modification was made.

    Raises:
        ValueError: When multiple SeriesInstanceUIDs are present across archive.
    """
    mod = False
    series_uid = None
    try:
        series_uid = dcms.get("SeriesInstanceUID")
    except ValueError:
        counts = Counter(dcms.bulk_get("SeriesInstanceUID"))
        log.error(
            f"Multiple SeriesInstanceUIDs detected:\n {counts} \nPlease run splitter gear."
        )
        sys.exit(1)

    sops = dcms.bulk_get("SOPInstanceUID")
    if not all(sops):
        log.info("Populating missing SOPInstanceUIDs.")
        for dcm in dcms:
            if not dcm.get("SOPInstanceUID"):
                setattr(dcm, "SOPInstanceUID", generate_uid())
        mod = True

    if not series_uid:
        log.info("Populating missing SeriesInstanceUID.")
        series_uid = generate_uid()
        dcms.set("SeriesInstanceUID", series_uid)
        mod = True

    return mod
