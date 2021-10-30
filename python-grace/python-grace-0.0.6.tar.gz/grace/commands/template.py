"""Copying template files."""

import shutil
from pathlib import Path
from typing import Optional, Sequence

from .. import GRACE_ROOT


def copy_template(name: str, destdir: Optional[Path] = None) -> None:
    """Copy a template in.prc."""
    src = GRACE_ROOT / "lib" / "templates" / name / "in.prc"
    if destdir is None:
        destdir = Path.cwd()
    dest = destdir / "in.prc"
    shutil.copy(src, dest)


def list_templates() -> Sequence[str]:
    """List names of templates."""
    template_dir = GRACE_ROOT / "lib" / "templates"
    names = [str(f.relative_to(template_dir)) for f in template_dir.glob("*/*")]
    return tuple(names)
