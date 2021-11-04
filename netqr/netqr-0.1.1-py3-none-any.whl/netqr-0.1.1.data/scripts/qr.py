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
from typing import List

# https://stackoverflow.com/questions/3217673/why-use-argparse-rather-than-optparse

# Netdrones internal qr package
from netqr import QRCode, QRRecognize, QRParameters, QRRecognizeVideo
from pytong import LogConfig

log: logging.Logger = LogConfig(__name__).logger


def main() -> None:
    """Start main."""
    log.warning(f"{Path.cwd()}")

    log.debug(f"{__name__=} {log=}")

    qr_codes: List[QRCode] = []
    qr_data: List[str]
    search_files: List[Path]
    qr_location: Path

    params = QRParameters()
    qr_location, qr_data, search_files, search_videos = params.read()

    log.warning(f"Finding QR Codes in {search_files=}")
    for file in search_files:
        img = QRRecognize(file)
        logging.info(f"{file=} {img.found=}")
        if not img.found:
            continue
        img.annotate().write()

    log.warning(f"searching in videos {search_videos=}")
    for video in search_videos:
        video_data: List[str] = QRRecognizeVideo(video).data
        log.debug(f"Found {video_data=} in {video=}")

    log.warning(f"Creating QR Code Images for {qr_data=}")
    for data in qr_data:
        log.debug(f"{data=}")
        # https://www.w3schools.com/python/python_lists_add.asp
        qr_codes.append(qr_code := QRCode(qr_location, data))
        qr_code.save()


if __name__ == "__main__":
    main()
