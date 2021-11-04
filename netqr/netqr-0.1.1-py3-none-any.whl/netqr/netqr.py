#!usr/bin/env python
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

# https://numpy.org/devdocs/reference/typing.html
# import numpy.typing as npt
from pathlib import Path
from typing import Optional, List, Tuple

# https://stackoverflow.com/questions/3217673/why-use-argparse-rather-than-optparse
import argparse
from confuse import (  # type: ignore
    Configuration,
    NotFoundError,
    ConfigTypeError,
)

# https://namingconvention.org/python/class-naming.html
from pytong import LogClass

# from .util_log import SetLog

# log: logging.Logger = logging.getLogger(__name__)
log: logging.Logger = logging.getLogger(__name__)


# https://www.pythontutorial.net/python-oop/python-class/
#  https://docs.python.org/3/tutorial/classes.html
@LogClass
class QRCode:
    """NetDrones QR Code Generation."""

    # note is you set values here they are class values for *all* instances
    # https://www.toptal.com/python/python-class-attributes-an-overly-thorough-guide
    data: str
    # https://pillow.readthedocs.io/en/stable/handbook/tutorial.html#using-the-image-class
    qr: Image
    basename: Path
    parent: Path
    log: logging.Logger

    def __init__(self, parent: Path = Path.cwd(), data: str = "test") -> None:
        """Initialize QR Code."""
        # self.file = file if not file is not None else Path(file).absolute()
        # https://realpython.com/python-pathlib/
        # need the second Path because .name returns a string
        # log is the module debug output
        log.debug(f"Got {data=}")
        # can this be a decorator?
        # self.log = logging.getLogger(__name__ + '.' type(self).__name__)
        self.parent = parent

        self.data = data
        self.qr = qrcode.make(self.data)
        # self.log is the class logger created by the @LoggingClass decorator
        self.log.debug(f"Made QR {self.qr=}")

    def save(self, basename: Optional[Path] = None) -> QRCode:
        """
        Write QR Code to File.

        parent = directory for saving files
        basename = filename of QR code to be saved
        """
        self.basename = (
            basename
            if basename is not None
            else Path(Path(self.data).name + ".png")
        )
        self.log.debug(
            f"write: {self.data=} into {self.parent=}/{self.basename=}"
        )
        self.qr.save(self.parent / self.basename)
        # allow chaining
        return self


@LogClass
class QRRecognizeVideo:
    """Recognize QR Codes in Videos."""

    file: Path
    recognized: Path
    reader: cv2.VideoCapture
    writer: cv2.VideoWriter
    frame: Tuple[int, int]
    color: bool
    log: logging.Logger  # hint to mypy @LogClass creates this invisibly
    data: List[str]

    # https://stackoverflow.com/questions/47533787/typehinting-tuples-in-python
    def __init__(
        self,
        file: Path,
        fps: float = 24.0,
        frame: Tuple[int, int] = (3840, 2160),
        color: bool = True,
    ):
        """Go through File and Recognize QR Codes."""
        self.file = file
        self.fps = fps
        self.frame = frame
        self.color = color
        self.recognized = file.with_suffix(".recognized" + file.suffix)
        # https://github.com/opencv/opencv-python/issues/299
        self.reader = cv2.VideoCapture(str(self.file))
        self.writer = cv2.VideoWriter(
            filename=str(self.recognized),
            # https://treyhunner.com/2018/10/asterisks-in-python-what-they-are-and-how-to-use-them/
            fourcc=cv2.VideoWriter_fourcc(*"avc1"),
            fps=self.fps,
            frameSize=self.frame,
            isColor=self.color,
        )
        self.data = []

        count: int = 0
        while self.reader.isOpened():
            ret, image = self.reader.read()
            if not ret:
                self.log.debug(f"{self.reader=} ended")
                break
            frame_recognized = QRRecognize(image=image)
            self.log.debug(f"Frame {count=} QR {frame_recognized.found=}")

            if frame_recognized.found:
                self.log.debug(
                    f"{frame_recognized.data=} in {frame_recognized.bbox[0]=}"
                )
                if frame_recognized.data not in self.data:
                    self.log.debug(
                        f"Adding {frame_recognized.data=} to qrcodes"
                    )
                    self.data.append(frame_recognized.data)

            # annotate the current frame with edges and the QRCode
            self.writer.write(
                frame_recognized.annotate().panel(["Status", *self.data]).img
            )
            count += 1

        self.log.info(f"Found {self.data=}")
        self.log.debug(f"Closing {self.writer=} and {self.reader=}")
        self.writer.release()
        self.reader.release()
        cv2.destroyAllWindows()


@LogClass
class QRRecognize:
    """NetDrones Recognize."""

    # note putting things here means they are class variables
    # note instance variables so do not set them here, they should
    # only be set in init
    found: bool
    data: str
    # the raw image
    img: Optional[np.ndarray]
    # recognized: Optional[np.ndarray]
    file: Path
    bbox: np.ndarray
    # rectilinear qr code in recognized image
    straight_qrcode: np.ndarray
    # set by LogClass
    log: logging.Logger

    def __init__(
        self, file: Optional[Path] = None, image: Optional[np.ndarray] = None
    ):
        """Read QR Code from File image."""
        self.img = image
        if file is not None:
            self.file = file
            logging.debug(f"read: searching in {file=}")
            # OpenCV needs a string not a path
            self.img = cv2.imread(str(file))

        # if no image just return
        self.found = False
        # self.recognized = self.img
        if self.img is None:
            return

        detector = cv2.QRCodeDetector()
        # data is the data read from QR code, then the bounding box
        # where we found the qr code and then the rectified QR code
        self.data, self.bbox, self.straight_qrcode = detector.detectAndDecode(
            self.img
        )

        # bbox may not return integers as the bounding box is estimated
        # and convert to an integer
        # https://stackoverflow.com/questions/42889621/converting-numpy-array-values-into-integers

        # if we do not recognize we just exit with recognized equal to original
        # image or if the bbox ckkk
        if self.bbox is None or not self.data:
            logging.debug(f"No bbox {self.found=} or no {self.data=}")
            return
        self.bbox = np.round(self.bbox).astype(int)
        self.found = True
        logging.debug(
            f"read: {self.data=} {type(self.data)=};"
            f" {self.bbox=} {type(self.bbox)=};"
            f" {type(self.straight_qrcode)=}"
        )

    def status(self, lines: List[str]) -> QRRecognize:
        """Draw overall status on the frame."""

    def annotate(self) -> QRRecognize:
        """Add bounding box and QR Data annotations to the image."""
        if not self.found or self.img is None:
            self.log.debug(f"No annotations {self.found=} {self.data=}")
            return self

        # https://www.thepythoncode.com/article/generate-read-qr-code-python
        # note found a bug here really returns a three dimensional box
        # should convert this to a rectangle
        # bbox is three dimensional so each entry is another bounding box
        # bounding boxes may not be four-square
        n_lines = len(self.bbox[0])
        self.log.debug(f"Writing Number of lines {n_lines}")
        self.log.debug(f"Drawing {self.bbox[0]=}")
        self.log.debug(f"annotating with {self.data=}")
        # https://www.geeksforgeeks.org/python-opencv-cv2-polylines-method/
        # Note the bbox should be one level down so you can draw multiple
        cv2.polylines(
            img=self.img,
            pts=self.bbox,
            isClosed=True,
            color=(255, 0, 0),
            thickness=8,
        )
        # for i in range(n_lines):
        #     point1 = tuple(self.bbox[0][i])
        #     point2 = tuple(self.bbox[0][(i + 1) % n_lines])
        #     self.log.debug(f"draw from {point1=} {point2=}")
        #     cv2.line(
        #         self.img, point1, point2, color=(255, 0, 0), thickness=8
        #     )
        self.log.debug(f"{self.img.shape=}")
        # https://pythonexamples.org/python-opencv-write-text-on-image-puttext/
        # position from the top left
        # BGR is format for opencv NOT RGB in Pillow

        # send a list and assume we are in the lower panel 3/4 of the way down
        self.panel(
            data=["QR Data", self.data],
            y=int(self.img.shape[0] * 3 / 4),
        )

        return self

    def panel(
        self,
        data: Optional[List[str]] = None,
        thickness: int = 3,
        font=cv2.FONT_HERSHEY_COMPLEX,
        font_scale: float = 3.0,
        text_size: Optional[List[float]] = None,
        line_height: Optional[int] = None,
        x: Optional[int] = None,
        y: Optional[int] = None,
    ) -> QRRecognize:
        """Add lines of test to the image."""
        # https://www.educba.com/opencv-puttext/
        # https://www.askpython.com/python-modules/opencv-puttext
        # if no lines use the data as a default
        if self.img is None:
            return self
        if data is None:
            if len(self.data) < 1:
                return self
            data = ["QR Data", self.data]

        if x is None:
            x = int(self.img.shape[1] * 1 / 32)
        # Assume this is the upper panel by default
        if y is None:
            y = int(self.img.shape[0] * 1 / 8)

        if text_size is None:
            text_size = cv2.getTextSize(data[0], font, font_scale, thickness)
        if line_height is None:
            line_height = int(text_size[1] * 3)

        for line in data:
            self.log.debug(f"putText {x=} {y=} {line=}")
            cv2.putText(
                img=self.img,
                text=line,
                org=(x, y),
                fontFace=font,
                fontScale=font_scale,
                color=(0, 0, 255),
                thickness=thickness,
                lineType=cv2.LINE_AA,
            )
            y += line_height

        return self

    def write(self, write_file: Optional[Path] = None) -> QRRecognize:
        """Write Recognized, Straight and QR Data."""
        # https://www.tutorialkart.com/opencv/python/opencv-python-save-image-example/
        # opencv needs string not pathlib's Paths

        if self.img is None:
            return self

        if not write_file:
            write_file = self.file
            self.log.debug(
                f"QR code in {write_file=} read and found {self.img.data=}"
            )
        if not write_file:
            return self

        self.log.debug(f"Writing recognized image {self.img.shape=}")
        cv2.imwrite(
            str(write_file.with_suffix(".recognized" + write_file.suffix)),
            self.img,
        )
        cv2.imwrite(
            str(write_file.with_suffix(".straight" + write_file.suffix)),
            self.straight_qrcode,
        )
        # if you want to display it
        # cv2.imshow(img)
        # https://stackoverflow.com/questions/47518669/create-new-folder-with-pathlib-and-write-files-into-it
        # https://realpython.com/python-pathlib/
        write_file.with_suffix(".txt").write_text(self.data + "\n")

        return self


# cannot use a decorator because __name__ in the decorator is
# only the basename and not the fully qualified module location
@LogClass
class QRParameters:
    """Read QR Parameters from Config YAML or Command Line."""

    config: Configuration
    config_file: Path
    test_data: List[str]
    parser: argparse.ArgumentParser
    search_files: List[Path]
    search_videos: List[Path]
    location: Path
    qr_data: List[str]

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
        # done by @LogClass
        # https://stackoverflow.com/questions/20599375/what-is-the-purpose-of-checking-self-class-python?noredirect=1&lq=1
        # self.log: logging.Logger = logging.getLogger(
        # type(self).__module__ + "." + type(self).__name__
        # )
        self.config: Configuration = Configuration(name)
        # set the configuration name + DIR to be the current one
        # overriding the default search in ~/.config
        self.config.set_file(config_file)
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
            "-l",
            "--location",
            help="directory location for qr codes",
            type=str,
        )
        self.parser.add_argument(
            "-v",
            "--videos",
            nargs="+",
            help="List of video files to search",
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

    def read(self) -> Tuple[Path, List[str], List[Path], List[Path]]:
        """
        Read from the qr data and the images to be searched.

        Try to read with confuse and use except to set defaults
        """
        unexpanded_files: List[str]
        try:
            self.qr_data = self.config["data"].as_str_seq()
        # https://stackoverflow.com/questions/6470428/catch-multiple-exceptions-in-one-line-except-block
        except (NotFoundError, ConfigTypeError) as error:
            log.debug(f"confuse {error=}")
            self.qr_data = self.test_data

        try:
            self.location = Path(self.config["location"].as_str())
        except NotFoundError:
            self.location = Path.cwd()

        try:
            # https://github.com/chris1610/pbpython/blob/master/extras/Pathlib-Cheatsheet.pdf
            unexpanded_files = self.config["search"].as_str_seq()
        except NotFoundError:
            unexpanded_files = []
        self.search_files = self.expand(unexpanded_files)

        try:
            self.search_videos = self.expand(self.config["video"].as_str_seq())
        except NotFoundError:
            self.search_videos = []

        return (
            self.location,
            self.qr_data,
            self.search_files,
            self.search_videos,
        )

    def expand(self, files: List[str]) -> List[Path]:
        """Expand strings into full file list."""
        # The search_files can have wildcards and also be directories
        # https://stackoverflow.com/questions/51108256/how-to-take-a-pathname-string-with-wildcards-and-resolve-the-glob-with-pathlib
        # expand the tilde
        expanded = []
        for file in files:
            p = (self.location / file).expanduser()
            parts = p.parts[p.is_absolute() :]  # noqa: E203
            expanded += list(Path(p.root).glob(str(Path(*parts))))
        return expanded
