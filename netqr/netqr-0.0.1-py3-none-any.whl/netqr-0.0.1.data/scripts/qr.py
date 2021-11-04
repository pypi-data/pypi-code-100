#!python
"""Create QR Code."""

# the command line entry point for netqr
#
# https://www.thepythoncode.com/article/generate-read-qr-code-python
# https://stackoverflow.com/questions/61544854/from-future-import-annotations
# not needed with Python 3.10 and later allows :w

from __future__ import annotations

import logging
from pathlib import Path
import cv2  # type:ignore
from typing import List

# https://stackoverflow.com/questions/3217673/why-use-argparse-rather-than-optparse

# Netdrones internal qr package
from netqr import QRCode, QRRecognize, QRParameters, log

log = logging.getLogger(__name__)


def main() -> None:
    """Start main."""
    log_config()

    log.debug(f"{__name__=} {log=}")

    qr_codes: List[QRCode]
    qr_data: List[str]
    search_files: List[Path]

    params = QRParameters()
    qr_data, subject_images = params.read()

    for data in qr_data:
        log.debug(f"{data=}")
        # https://www.w3schools.com/python/python_lists_add.asp
        qr_codes.append(qr_code := QRCode(data))
        qr_code.save()

    for file in search_files:
        img = QRRecognize(file)
        if not img.found:
            logging.info(f"{file=} no QR code found")
            continue
        # https://www.tutorialkart.com/opencv/python/opencv-python-save-image-example/
        cv2.imwrite(file.with_suffix(".recognized" + file.suffix), img.img)
        cv2.imwrite(
            file.with_suffix(".straight" + file.suffix), img.straight_qrcode
        )
        # cv2.imshow(img)


if __name__ == "__main__":
    main()
