import unittest
from pathlib import Path

from ruteni import ROOTNS
from ruteni.utils.icon import IcoIcon, PngIcon
from urlobject.path import URLPath

# /usr/bin/identify tests/icons/icons.ico
ICO_FILENAME = Path("tests/icons/icons.ico")
PNG_FILENAME = Path("tests/icons/icon-512x512.png")
ICO_PATH = URLPath("ico")
PNG_PATH = URLPath("png")


class IconTestCase(unittest.TestCase):
    def test_ico(self) -> None:
        ico_icon = IcoIcon(ROOTNS, ICO_PATH, ICO_FILENAME)
        self.assertEqual(
            ico_icon.sizes,
            "72x72 96x96 120x120 128x128 144x144 180x180 192x192 256x256 512x512",
        )

    def test_png(self) -> None:
        png_icon = PngIcon(ROOTNS, PNG_PATH, PNG_FILENAME)
        self.assertEqual(png_icon.sizes, "512x512")
        self.assertEqual(png_icon.src, "/" + PNG_PATH)

    def test_purpose(self) -> None:
        for purpose in ("any", "maskable", "monochrome", "any maskable"):
            self.assertEqual(
                PngIcon(ROOTNS, PNG_PATH, PNG_FILENAME, purpose=purpose).purpose,
                purpose,
            )
        with self.assertRaises(ValueError):
            PngIcon(ROOTNS, PNG_PATH, PNG_FILENAME, purpose="foo")
        with self.assertRaises(ValueError):
            PngIcon(ROOTNS, PNG_PATH, PNG_FILENAME, purpose="any foo")
