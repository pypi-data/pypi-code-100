from dataclasses import dataclass
from pathlib import Path


@dataclass
class File:
    filename: str

    @property
    def path(self):
        return Path(self.filename)

    @classmethod
    def size_str(C, size, suffix='B', decimals=1, sep='\u00a0', k=1000):
        """
        Given the file size in bytes, return a string with the human-readable size.
        """
        SIZE_UNITS = ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
        if size is None:
            return
        size = float(size)
        for unit in SIZE_UNITS:
            if abs(size) < k or unit == SIZE_UNITS[-1]:
                return "{size:.{decimals}f}{sep}{unit}{suffix}".format(
                    size=size,
                    unit=unit,
                    suffix=suffix,
                    sep=sep,
                    decimals=decimals if SIZE_UNITS.index(unit) > 0 else 0,
                )
            size /= k
