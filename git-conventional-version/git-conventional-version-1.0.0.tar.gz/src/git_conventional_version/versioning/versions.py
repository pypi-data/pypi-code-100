import re


class Version:
    """Represents specific type of version.

    Each Version implementation should have defined:
    - pattern,
    - str_format,
    - default value for numbers attribute that is consistent with above.

    Version classes are used by analogical Release classes.
    """
    pattern: str
    str_format: str

    def __init__(
        self,
        numbers: list = None
    ) -> None:
        self.numbers = numbers

    @classmethod
    def _validate_tag(cls, tag: str) -> None:
        if not re.search(cls.pattern, tag):
            raise Exception(f"Tag {tag} does not match pattern {cls.pattern}.")

    @classmethod
    def _extract_version(cls, tag: str) -> "Version":
        groups = re.search(cls.pattern, tag).groups()
        return cls([int(group) for group in groups])

    @classmethod
    def from_tag(cls, tag: str) -> "Version":
        cls._validate_tag(tag)
        return cls._extract_version(tag)

    def __str__(self):
        return self.str_format % tuple(self.numbers)


class FinalVersion(Version):
    """Represents final version.
    """
    pattern: str = r"^(\d+)\.(\d+)\.(\d+)$"
    str_format: str = "%d.%d.%d"
    def __init__(self, numbers: list = None) -> None:
        super().__init__(numbers=numbers)
        if not numbers:
            self.numbers = [0, 0, 0]


class PreReleaseVersion(Version):
    """Represents pre-release types of version.

    Needs subclassing.
    """
    def __init__(self, numbers: list = None) -> None:
        super().__init__(numbers=numbers)
        if not numbers:
            self.numbers = [0, 0, 0, 0]


class ReleaseCandidateVersion(PreReleaseVersion):
    """Represents release candidate version.
    """
    pattern: str = r"^(\d+)\.(\d+)\.(\d+)rc(\d+)$"
    str_format: str = "%d.%d.%drc%d"


class DevelopmentalVersion(PreReleaseVersion):
    """Represents developmental version.
    """
    pattern: str = r"^(\d+)\.(\d+)\.(\d+)dev(\d+)$"
    str_format: str = "%d.%d.%ddev%d"


class AlphaVersion(PreReleaseVersion):
    """Represents alpha version.
    """
    pattern: str = r"^(\d+)\.(\d+)\.(\d+)a(\d+)$"
    str_format: str = "%d.%d.%da%d"


class BetaVersion(PreReleaseVersion):
    """Represents beta version.
    """
    pattern: str = r"^(\d+)\.(\d+)\.(\d+)b(\d+)$"
    str_format: str = "%d.%d.%db%d"
