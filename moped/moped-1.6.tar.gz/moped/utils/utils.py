from __future__ import annotations

import sys
from pathlib import Path


def get_temporary_directory(subdirectory: str) -> Path:
    if sys.platform in ["win32", "cygwin"]:
        temp_dir = Path(f"%userprofile%/AppData/Local/Temp/moped/{subdirectory}")
    else:
        temp_dir = Path(f"/tmp/moped/{subdirectory}")
    if not temp_dir.is_dir():
        temp_dir.mkdir(parents=True)
    return temp_dir
