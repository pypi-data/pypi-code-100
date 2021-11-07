from __future__ import annotations

import io
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterator, Optional, Union, Generator

import requests

DEFAULT_CHUNK_SIZE = 64 * 1024  # 64 kb


class InputFile(ABC):
    """
    This object represents the contents of a file to be uploaded. Must be posted using multipart/form-data
    in the usual way that files are uploaded via the browser.

    Source: https://core.telegram.org/bots/api#inputfile
    """

    def __init__(self, filename: Optional[str] = None, chunk_size: int = DEFAULT_CHUNK_SIZE):
        """
        Base class for input files. Should not be used directly.
        Look at :class:`BufferedInputFile`, :class:`FSInputFile` :class:`URLInputFile`

        :param filename: name of the given file
        :param chunk_size: reader chunks size
        """
        self.filename = filename
        self.chunk_size = chunk_size

    @classmethod
    def __get_validators__(cls) -> Iterator[None]:
        yield None

    @abstractmethod
    def read(self, chunk_size: int) -> Generator[bytes, None]:  # pragma: no cover
        yield b""

    def __iter__(self) -> Iterator[bytes]:
        for chunk in self.read(self.chunk_size):
            yield chunk


class BufferedInputFile(InputFile):
    def __init__(self, file: bytes, filename: str, chunk_size: int = DEFAULT_CHUNK_SIZE):
        """
        Represents object for uploading files from filesystem

        :param file: Bytes
        :param filename: Filename to be propagated to telegram.
        :param chunk_size: Uploading chunk size
        """
        super().__init__(filename=filename, chunk_size=chunk_size)

        self.data = file

    @classmethod
    def from_file(
            cls,
            path: Union[str, Path],
            filename: Optional[str] = None,
            chunk_size: int = DEFAULT_CHUNK_SIZE,
    ) -> BufferedInputFile:
        """
        Create buffer from file

        :param path: Path to file
        :param filename: Filename to be propagated to telegram.
            By default will be parsed from path
        :param chunk_size: Uploading chunk size
        :return: instance of :obj:`BufferedInputFile`
        """
        if filename is None:
            filename = os.path.basename(path)
        with open(path, "rb") as f:
            data = f.read()
        return cls(data, filename=filename, chunk_size=chunk_size)

    def read(self, chunk_size: int) -> Generator[bytes, None]:
        buffer = io.BytesIO(self.data)
        chunk = buffer.read(chunk_size)
        while chunk:
            yield chunk
            chunk = buffer.read(chunk_size)


class FSInputFile(InputFile):
    def __init__(
            self,
            path: Union[str, Path],
            filename: Optional[str] = None,
            chunk_size: int = DEFAULT_CHUNK_SIZE,
    ):
        """
        Represents object for uploading files from filesystem

        :param path: Path to file
        :param filename: Filename to be propagated to telegram.
            By default will be parsed from path
        :param chunk_size: Uploading chunk size
        """
        if filename is None:
            filename = os.path.basename(path)
        super().__init__(filename=filename, chunk_size=chunk_size)

        self.path = path

    def read(self, chunk_size: int) -> Generator[bytes, None]:
        with open(self.path, "rb") as f:
            chunk = f.read(chunk_size)
            while chunk:
                yield chunk
                chunk = f.read(chunk_size)


class URLInputFile(InputFile):  # noqa
    def __init__(
            self,
            url: str,
            filename: Optional[str] = None,
            chunk_size: int = DEFAULT_CHUNK_SIZE,
            timeout: int = 30,
    ):
        """
        Represents object for streaming files from internet

        :param url: URL in internet
        :param filename: Filename to be propagated to telegram.
        :param chunk_size: Uploading chunk size
        """
        super().__init__(filename=filename, chunk_size=chunk_size)

        self.url = url
        self.timeout = timeout

    def read(self, chunk_size: int) -> Generator[bytes, None]:
        stream = requests.get(url=self.url, timeout=self.timeout, stream=True)
        for chunk in stream.iter_content(chunk_size=self.chunk_size):
            yield chunk
