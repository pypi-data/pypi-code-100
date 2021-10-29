from pathlib import Path
from typing import NamedTuple

from colour import Color


class Settings(NamedTuple):
    """Tools settings"""

    in_file: Path
    """Input file"""

    out_file: Path
    """Output file"""

    lower: int
    """Lower threshold for Candy edge detection"""

    upper: float
    """Upper threshold for Candy edge detection"""

    color: Color
    """Final color of contour"""

    crop: bool
    """Crop transparent pixels after converting"""
