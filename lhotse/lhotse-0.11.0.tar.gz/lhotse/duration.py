from dataclasses import dataclass
from operator import xor
from typing import Optional

SampleCount = int
FrameCount = int


@dataclass(unsafe_hash=True, frozen=True)
class Duration:
    sampling_rate: int
    num_samples: Optional[SampleCount] = None
    num_frames: Optional[FrameCount] = None
    frame_shift: Optional[SampleCount] = None

    def __post_init__(self):
        assert (
            self.sampling_rate is not None
        ), "Sampling rate has to be specified for Duration"
        represents_samples = self.num_samples is not None
        represents_frames = self.represents_frames
        assert xor(
            represents_samples, represents_frames
        ), "Either num_samples or (num_frames and frame_shift), but not both, need to be specified for Duration"
        if represents_frames:
            object.__setattr__(self, "num_samples", self.num_frames * self.frame_shift)

    @property
    def represents_frames(self) -> bool:
        return self.frame_shift is not None and self.num_frames is not None

    @property
    def frame_shift_seconds(self) -> float:
        return self.frame_shift / self.sampling_rate

    @property
    def seconds(self) -> float:
        if self.represents_frames:
            return self.num_frames * self.frame_shift / self.sampling_rate
        return self.num_samples / self.sampling_rate

    @property
    def milliseconds(self) -> float:
        return self.seconds * 1000.0

    def __add__(self, other: "Duration") -> "Duration":
        assert self.sampling_rate == other.sampling_rate
        if self.represents_frames:
            assert self.frame_shift == other.frame_shift
            return Duration(
                num_frames=self.num_frames + other.num_frames,
                frame_shift=self.frame_shift,
                sampling_rate=self.sampling_rate,
            )
        return Duration(
            num_samples=self.num_samples + other.num_samples,
            sampling_rate=self.sampling_rate,
        )

    def __sub__(self, other: "Duration") -> "Duration":
        return self + (-other)

    def __neg__(self) -> "Duration":
        if self.represents_frames:
            return Duration(
                num_frames=-self.num_frames,
                frame_shift=self.frame_shift,
                sampling_rate=self.sampling_rate,
            )
        return Duration(num_samples=-self.num_samples, sampling_rate=self.sampling_rate)

    def __bool__(self) -> bool:
        return bool(self.num_samples)

    # Ordering and equality operators.
    # We assume that Duration's of different sampling_rate or frame_shift
    # can still be meaningfully compared as time quantities, so we cast them to seconds.

    def __eq__(self, other: "Duration") -> bool:
        return self.seconds == other.seconds

    def __lt__(self, other: "Duration") -> bool:
        return self.seconds < other.seconds

    def __gt__(self, other: "Duration") -> bool:
        return other < self

    def __le__(self, other: "Duration") -> bool:
        return not (other > self)

    def __ge__(self, other: "Duration") -> bool:
        return not (self < other)
