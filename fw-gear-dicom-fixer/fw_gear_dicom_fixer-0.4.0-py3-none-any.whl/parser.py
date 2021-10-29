"""Parser module to parse gear config.json."""

import typing as t
from pathlib import Path

from flywheel_gear_toolkit import GearToolkitContext


def parse_config(
    gear_context: GearToolkitContext,
) -> Path:
    """Parses gear_context config.json file and returns relevant inputs and
    options."""

    return Path(gear_context.get_input_path("dicom")).resolve()
