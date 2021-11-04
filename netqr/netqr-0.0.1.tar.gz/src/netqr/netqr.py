#!/usr/bin/env python
"""Create QR Code."""

# https://www.thepythoncode.com/article/generate-read-qr-code-python
# https://stackoverflow.com/questions/61544854/from-future-import-annotations
# not needed with Python 3.10 and later allows :w

from __future__ import annotations


import qrcode  # type:ignore
from PIL import Image  # type: ignore
import logging
import cv2  # type:ignore
import numpy as np
from pathlib import Path
from typing import Optional, List, Tuple

# https://stackoverflow.com/questions/3217673/why-use-argparse-rather-than-optparse
import argparse
from confuse import (  # type: ignore
    Configuration,
    NotFoundError,
    ConfigTypeError,
)


# https://www.pythontutorial.net/python-oop/python-class/
#  https://docs.python.org/3/tutorial/classes.html
class QRCode():
    """NetDrones QR Code Generation."""

    # note is you set values here they are class values for *all* instances
    # https://www.toptal.com/python/python-class-attributes-an-overly-thorough-guide
    data: str
    # https://pillow.readthedocs.io/en/stable/handbook/tutorial.html#using-the-image-class
    qr: Image
    file: Path

    def __init__(self, data: str) -> None:
        """Initialize QR Code."""
        # self.file = file if not file is not None else Path(file).absolute()
        # https://realpython.com/python-pathlib/
        # need the second Path because .name returns a string
        self.data = data
        self.qr = qrcode.make(self.data)

    def save(self, file: Optional[Path] = None) -> QRCode:
        """Write QR Code to File."""
        self.file = file if file is not None else Path(Path(self.data).name)
        logging.debug(f"write: {self.data=} {self.file=}")
        self.qr.save(self.file)
        # allow chaining
        return self


class QRRecognize():
    """NetDrones Recognize."""

    found: bool = False
    read_data: str
    img: np.ndarray
    file: Path
    bbox: np.ndarray
    straight_qrcode: np.ndarray

    def __init__(self, file: Path):
        """Read QR Code from File image."""
        # start the BaseLog

        self.file = file
        logging.debug(f"read: searching in {file=}")
        self.img: np.ndarray = cv2.imread(file)
        detector = cv2.QRCodeDetector()
        # data is the data read from QR code, then the bounding box
        # where we found the qr code and then the rectified QR code
        self.read_data, bbox, self.straight_qrcode = detector.detectAndDecode(
            self.img
        )

        # bbox may not return integers as the bounding box is estimated
        # and convert to an integer
        # https://stackoverflow.com/questions/42889621/converting-numpy-array-values-into-integers

        if bbox is None:
            logging.debug(f"No bbox {self.found=}")
            return

        self.found = True
        logging.debug(f"{bbox=} {type(bbox)=}")
        self.bbox = np.round(bbox).astype(int)
        logging.debug(
            f"read: {self.read_data=} {type(self.read_data)=};"
            f" {bbox=} {type(self.bbox)=};"
            f" {type(self.straight_qrcode)=}"
        )
        print(f"QR Code data found: {self.read_data}")
        # https://www.thepythoncode.com/article/generate-read-qr-code-python
        # note found a bug here really returns a three dimensional box
        # should convert this to a rectangle
        n_lines = len(bbox[0])
        print(f"Number of lines {n_lines}")
        logging.debug("Drawing {type(self.bbox)=}")
        for i in range(n_lines):
            point1 = tuple(self.bbox[0][i])
            point2 = tuple(self.bbox[0][(i + 1) % n_lines])
            logging.debug("draw from {point1=} {point2=}")
            cv2.line(self.img, point1, point2, color=(255, 0, 0), thickness=2)

            logging.debug(f"{self.img=} {type(self.img)=}")


class QRParameters():
    """Read QR Parameters from Config YAML or Command Line."""

    config: Configuration
    config_file: Path
    test_data: List[str]
    parser: argparse.ArgumentParser
    search_files: List[Path]
    qrcode: List[str]

    def __init__(
        self,
        name: str = Path.cwd().name,
        config_file: Path = Path("./config.yaml"),
    ):
        """
        Parse the command line.

        Usage: qr [-f config.yaml ] -d [data1, data2,..] -i [image1, image2...]

        It is better to use a config files, the default is qr.yaml
        The default config file is in the script directory/config.yaml
        """
        # https://confit.readthedocs.io/en/latest/
        # https://stackoverflow.com/questions/56639952/what-does-pathlib-path-cwd-return
        self.config: Configuration = Configuration(name)
        # set the configuration name + DIR to be the current one
        # overriding the default search in ~/.config
        self.config.set_file(self.config_file)
        # https://docs.python.org/3/library/argparse.html
        self.parser = argparse.ArgumentParser(
            description="Read QR data and generate codes"
        )
        # https://stackoverflow.com/questions/15753701/how-can-i-pass-a-list-as-a-command-line-argument-with-argparse
        self.parser.add_argument(
            "-d" "--data",
            nargs="+",
            help="list of data strings to encode into QR",
            type=str,
        )
        self.parser.add_argument(
            "-i",
            "--image",
            nargs="+",
            help="List of image files to search",
            type=str,
        )
        args = self.parser.parse_args()
        self.config.set_args(args)

        self.test_data = [
            "https://netdron.es/survey/234234",
            "https://netdron.es/survey/908098",
            "https://netdron.es/survey/68763",
            "ipfs://QmZSTrVzb4U9jZ1BzvM9PZGu8jmUGXoMDJTZWcFSxPUvy2",
        ]

    def read(self) -> Tuple[List[str], List[Path]]:
        """Read from the qr data and the images to be searched."""
        try:
            self.qr_data: List[str] = self.config["qr_data"].as_str_seq()
            # https://github.com/chris1610/pbpython/blob/master/extras/Pathlib-Cheatsheet.pdf
            unexpanded_files: List[Path] = self.config["search"].as_str_seq()
        # https://stackoverflow.com/questions/6470428/catch-multiple-exceptions-in-one-line-except-block
        except (NotFoundError, ConfigTypeError) as error:
            self.log.debug(f"confuse {error=}")

        if self.qr_data is None:
            self.qr_data = self.test_data

        # The search_files can have wildcards and also be directories
        # https://stackoverflow.com/questions/51108256/how-to-take-a-pathname-string-with-wildcards-and-resolve-the-glob-with-pathlib
        # expand the tilde
        self.search_files = []
        for file in unexpanded_files:
            p = Path(file).expanduser()
            parts = p.parts[p.is_absolute() :]
            self.search_files += list(Path(p.root).glob(str(Path(*parts))))

        return self.qr_data, self.search_files
