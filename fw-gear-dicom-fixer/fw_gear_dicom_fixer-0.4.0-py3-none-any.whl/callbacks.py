import functools
import logging
import typing as t
from contextlib import contextmanager

from fw_file.dicom import DICOM, get_config
from fw_file.dicom.fixer import raw_elem_tracker
from pydicom import config as pydicom_config
from pydicom import values
from pydicom.charset import decode_element, default_encoding
from pydicom.datadict import tag_for_keyword
from pydicom.dataelem import DataElement, RawDataElement
from pydicom.dataset import Dataset
from pydicom.tag import BaseTag
from pydicom.uid import ExplicitVRLittleEndian as standard

log = logging.getLogger(__name__)


def is_dcm(dcm: DICOM) -> bool:
    """Look at a potential dicom and see whether it actually is a dicom.

    Args:
        dcm (DICOM): DICOM

    Returns:
        bool: True if it probably is a dicom, False if not
    """
    num_pub_tags = 0
    keys = dcm.dir()
    for key in keys:
        try:
            if BaseTag(tag_for_keyword(key)).group > 2:  # type: ignore
                num_pub_tags += 1
        except (AttributeError, TypeError):
            continue
    # Require two public tags outside the file_meta group.
    if num_pub_tags > 1:
        return True
    else:
        log.debug(f"Removing: {dcm}. Not a DICOM")
        return False


@contextmanager
def setup_callbacks():
    # Important that we get the original callbacks before setting any config values.
    data_elem_bk = pydicom_config.data_element_callback
    data_elem_kwargs_bk = pydicom_config.data_element_callback_kwargs
    config = get_config()
    config.fix_vr_mismatch = True
    # Add incorrect unit callback
    pydicom_config.data_element_callback = functools.partial(
        handle_incorrect_unit,
        data_element_callback=pydicom_config.data_element_callback,
    )
    try:
        yield
    finally:
        pydicom_config.data_element_callback = data_elem_bk
        pydicom_config.data_element_callback_kwargs = data_elem_kwargs_bk


@contextmanager
def empty_pydicom_callback():
    data_elem_bk = pydicom_config.data_element_callback
    data_elem_kwargs_bk = pydicom_config.data_element_callback_kwargs
    pydicom_config.data_element_callback = None
    try:
        yield
    finally:
        pydicom_config.data_element_callback = data_elem_bk
        pydicom_config.data_element_callback_kwargs = data_elem_kwargs_bk


def handle_incorrect_unit(
    raw_elem: RawDataElement,
    data_element_callback: t.Callable[..., RawDataElement] = None,
    **kwargs: t.Dict,
) -> RawDataElement:  # pylint: disable=invalid-name
    """Callback to fix known incorrect units.

    Args:
        raw_elem (RawDataElement): Data element to be corrected.
        data_element_callback (t.Callable[..., RawDataElement], optional): other clalback. Defaults to None.

    Returns:
        RawDataElement: Corrected callback
    """
    if data_element_callback and callable(data_element_callback):
        raw_elem = data_element_callback(raw_elem, **kwargs)
    encodings = kwargs.get("encodings")
    # encodings should be a list, but can be a string
    #   check for string, otherwise assume list GEAR-1770
    if not encodings:
        encodings = [default_encoding]
    elif isinstance(encodings, str):
        encodings = [encodings]
    encoding = encodings[0]
    # Check for incorrect unit on MagneticFieldStrength
    if raw_elem.tag.real == tag_for_keyword("MagneticFieldStrength"):
        try:
            mfs = values.convert_value("DS", raw_elem, encoding)
            mfs = float(mfs)
        except:  # pragma: no cover
            log.error(
                "Uncaught exception, not attempting to change value.", exc_info=True
            )
            return raw_elem
        if mfs:
            if mfs > 30:
                mfs /= 1000
                # DS "decimal string" VR, cast to string.
                raw_elem = raw_elem._replace(value=bytes(str(mfs).encode(encoding)))
    return raw_elem


def decode_dcm(dcm: DICOM) -> None:
    """Decode dicom.

       Mirrors pydicom.dataset.Dataset.decode, except it ignores decoding the
       OriginalAttributesSequence tag.

    Args:
        dcm (DICOM): dicom file.
    """
    dicom_character_set = dcm.dataset.raw._character_set

    def decode(dataset: Dataset, data_element: DataElement) -> None:
        """Callback to decode data element, but ignore OriginalAttributesSequence."""

        if data_element.VR == "SQ":
            if data_element.tag == tag_for_keyword("OriginalAttributesSequence"):
                return
            for dset in data_element.value:
                dset._parent_encoding = dicom_character_set
                dset.decode()
        else:
            decode_element(data_element, dicom_character_set)

    with raw_elem_tracker(dcm.tracker):
        dcm.walk(decode, recursive=False)


def standardize_transfer_syntax(dcm: DICOM):  # pragma: no cover
    """Set TransferSyntaxUID to ExplicitVRLittleEndian."""
    if dcm.dataset.raw.file_meta.TransferSyntaxUID != standard:
        dcm.dataset.raw.is_implicit_VR = False
        dcm.dataset.raw.is_little_endian = True
        dcm.dataset.raw.file_meta.TransferSyntaxUID = standard
