"""Main module."""

import functools
import logging
import tempfile
import typing as t
import zipfile
from contextlib import contextmanager
from pathlib import Path

from fw_file.dicom import DICOMCollection
from pydicom import config as pydicom_config
from pydicom.datadict import keyword_for_tag
from pydicom.uid import UncompressedTransferSyntaxes

from .callbacks import decode_dcm, is_dcm, setup_callbacks, standardize_transfer_syntax
from .metadata import add_missing_uid, update_modified_dicom_info

log = logging.getLogger(__name__)


def run(
    dicom_path: Path, out_dir: Path, transfer_syntax: bool
) -> t.List[t.Dict[str, t.List[str]]]:
    """Run dicom fixer.

    Args:
        dicom_path (str): Path to directory containing dicom files.
        out_dir (Path): Path to directory to store outputs.
    """
    events = []
    with setup_callbacks():
        if zipfile.is_zipfile(str(dicom_path)):
            dcms = DICOMCollection.from_zip(
                dicom_path, filter_fn=is_dcm, force=True, track=True
            )
        else:
            dcms = DICOMCollection(dicom_path, filter_fn=is_dcm, force=True, track=True)
        for dcm in dcms:
            decode_dcm(dcm)
            # Attempt to decompress dicom PixelData with GDCM if compressed
            if (
                dcm.dataset.raw.file_meta.TransferSyntaxUID
                not in UncompressedTransferSyntaxes
            ):
                dcm.dataset.raw.decompress(handler_name="gdcm")
            if transfer_syntax:
                standardize_transfer_syntax(dcm)
            dcm.tracker.trim()
            for element in dcm.tracker.data_elements:
                if element.events:
                    tagname = str(element.tag).replace(",", "")
                    kw = keyword_for_tag(element.tag)
                    if kw:
                        tagname = kw
                    events.append({tagname: [str(ev) for ev in element.events]})
            update_modified_dicom_info(dcm)

    added_uid = add_missing_uid(dcms)

    if (len(events) > 0 and all([len(ev) > 0 for ev in events])) or added_uid:
        log.info(f"Writing output to {out_dir / dicom_path.name}")
        if len(dcms) > 1:
            dcms.to_zip(out_dir / dicom_path.name)
        else:
            dcms[0].save(out_dir / dicom_path.name)

    return events
