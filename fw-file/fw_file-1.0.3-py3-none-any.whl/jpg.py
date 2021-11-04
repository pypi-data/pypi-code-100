"""JPG file module."""
import typing as t

import piexif
from fw_utils import AnyFile
from piexif import TAGS
from PIL import Image

from .base import FieldsMixin, File

IFDS = ["0th", "Exif", "GPS", "Interop", "1st"]
IFD_MAP = {ifd.lower(): ifd for ifd in IFDS}
KEYWORD_MAP: dict = {}
for ifd_ in IFDS:
    for tag_, desc in TAGS[ifd_].items():
        KEYWORD_MAP.setdefault(desc["name"].lower(), {"tag": tag_, "ifds": []})
        KEYWORD_MAP[desc["name"].lower()]["ifds"].append(ifd_)


class JPG(FieldsMixin, File):
    """JPG data-file class."""

    def __init__(self, file: AnyFile) -> None:
        """Load and parse JPG files."""
        super().__init__(file)
        img = Image.open(self.file)
        exif = piexif.load(img.info["exif"]) if "exif" in img.info else {}
        object.__setattr__(self, "fields", exif)
        object.__setattr__(self, "jpg", img)

    def save(self, file: t.Optional[AnyFile] = None) -> None:
        """Save (potentially modified) data file."""
        with self.open_dst(file) as wfile:
            exif_bytes = piexif.dump(self.fields)
            self.jpg.save(wfile, exif=exif_bytes, format="JPEG")

    def __getitem__(self, key: t.Union[t.Tuple[str, str], str]) -> t.Any:
        """Get EXIF value by tag/keyword."""
        ifds, tag = get_exif_tag(key)
        # If IFD not provided in key return the first find
        for ifd in ifds:
            value = self.fields.get(ifd, {}).get(tag)
            if value:
                return value
        return None

    def __setitem__(self, key: t.Union[t.Tuple[str, str], str], value: t.Any) -> None:
        """Set EXIF tag's value."""
        ifds, tag = get_exif_tag(key)
        for ifd in ifds:
            self.fields[ifd][tag] = value

    def __delitem__(self, key: t.Union[t.Tuple[str, str], str]) -> None:
        """Delete EXIF tag."""
        ifds, tag = get_exif_tag(key)
        for ifd in ifds:
            del self.fields[ifd][tag]


def get_exif_tag(key: t.Union[t.Tuple[str, str], str]) -> t.Tuple[t.List[str], int]:
    """Get EXIF tag and IFDs from keyword."""
    ifd = None
    if not isinstance(key, str):
        ifd, key = key
    result = KEYWORD_MAP[key.lower()]
    return result["ifds"] if not ifd else [IFD_MAP[ifd.lower()]], result["tag"]
