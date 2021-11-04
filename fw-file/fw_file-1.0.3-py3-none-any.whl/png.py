"""PNG file module."""
import typing as t
import warnings
from pathlib import Path

import png
from fw_utils import AnyFile
from PIL import Image

from .base import FieldsMixin, File

PUBLIC_CHUNK_TYPES = [
    "IHDR",
    "PLTE",
    "IDAT",
    "IEND",
    "bKGD",
    "cHRM",
    "dSIG",
    "eXIf",
    "gAMA",
    "hIST",
    "iCCP",
    "iTXt",
    "pHYs",
    "sBIT",
    "sPLT",
    "sRGB",
    "sTER",
    "tEXt",
    "tIME",
    "tRNS",
    "zTXt",
]

CHUNK_TYPE_MAP = {t.lower(): t for t in PUBLIC_CHUNK_TYPES}

ENCODING_MAP = {
    "iTXt": "utf-8",
    "tEXt": "utf-8",
}


class PNG(FieldsMixin, File):
    """PNG data-file class."""

    def __init__(self, file: AnyFile) -> None:
        """Load and parse PNG files."""
        super().__init__(file)
        img = Image.open(self.file)
        if isinstance(file, (str, Path)):
            reader = png.Reader(filename=file)
        else:
            file.seek(0)
            reader = png.Reader(file=file)
        # NB: The row image is a part of chunk (IDAT)
        chunk_list = list(reader.chunks())
        chunks: dict = {}
        for key, value in chunk_list:
            chunks.setdefault(key.decode(), []).append(value)
        object.__setattr__(self, "fields", chunks)
        object.__setattr__(self, "png", img)

    def save(self, file: t.Optional[AnyFile] = None) -> None:
        """Save (potentially modified) data file."""
        with self.open_dst(file) as wfile:
            chunks = []
            for tag, values in self.fields.items():
                if tag == "IEND":
                    continue
                chunks.extend([(tag.encode(), v) for v in values])
            chunks.append((b"IEND", b""))
            png.write_chunks(wfile, chunks)

    def __getitem__(self, key: str) -> t.Any:
        """Get chunk value by keyword."""
        # TODO: exif, ztxt, time decoding
        key = CHUNK_TYPE_MAP.get(key.lower()) or key
        vals = self.fields.get(key)
        if vals:
            if len(vals) > 1:
                warnings.warn(
                    f"There are multiple values for the given chunk {key}\n."
                    "Use the get_all(<key>) method to get all values."
                )
            return handle_decoding(key, [vals[0]])
        return None

    def getall(self, key: str) -> t.List[bytes]:
        """Get values of a chunk by keyword."""
        result = self.fields.get(key)
        if result:
            return handle_decoding(key, result)
        return []

    def __setitem__(self, key: str, value: t.Any) -> None:
        """Set chunk value."""
        if value and not isinstance(value, bytes):
            if key in ENCODING_MAP:
                value = value.encode(ENCODING_MAP[key])
            else:
                value = value.encode()
        self.fields.setdefault(key, []).append(value)

    def __delitem__(self, key: str) -> None:
        """Delete chunk by key."""
        del self.fields[key]


def handle_decoding(key: str, values: t.List[t.Any]) -> t.Any:
    """Handle de-coding values."""
    results = []
    if key not in ENCODING_MAP:
        results.extend(values)
    else:
        decoded = [v.decode(ENCODING_MAP[key]) for v in values if v is not None]
        results.extend(decoded)
    if results:
        if len(results) > 1:
            return results
        return results[0]
    return None
