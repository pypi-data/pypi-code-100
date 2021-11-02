from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class MatchConfig:
    """
    Represents a match configuration that can be used to request matching at a match service.
    """
    match_function: str = "TRIGRAM_DICE"
    selection_strategy: str = "FULL_RESULT"
    threshold: float = 0


@dataclass(frozen=True)
class MatchRequest:
    """
    Represents a request to match the domain bit strings against the range bit strings.
    """
    domain_bit_strings: List[str] = field(default_factory=list)
    range_bit_strings: List[str] = field(default_factory=list)
    match_config: MatchConfig = field(default_factory=MatchConfig)


@dataclass(frozen=True)
class Match:
    """
    Represents a match returned by the match service.
    """
    domain_bit_string: str
    range_bit_string: str
    confidence: float
