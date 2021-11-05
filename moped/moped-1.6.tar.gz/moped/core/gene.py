from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Set


@dataclass
class MonomerLink:
    gene: str
    database_links: Dict[str, Set[str]]
