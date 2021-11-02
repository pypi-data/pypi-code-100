"""Represents a basic datasource or datasink."""

from dataclasses import dataclass
from typing import Protocol


@dataclass
class Connector(Protocol):
    """Basic representation of a data connector."""

    def to_string(self) -> None:
        """Print a string describing the connector."""

    def read(self):
        """Reads data."""

    def write(self):
        """Writes data."""
