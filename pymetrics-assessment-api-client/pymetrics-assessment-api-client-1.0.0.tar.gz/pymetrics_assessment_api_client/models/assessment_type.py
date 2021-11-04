from enum import Enum


class AssessmentType(str, Enum):
    GAMES = "games"
    VIDEO_INTERVIEW = "video_interview"
    NLR = "nlr"

    def __str__(self) -> str:
        return str(self.value)
