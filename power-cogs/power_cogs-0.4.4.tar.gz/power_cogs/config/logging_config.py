from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class LoggingConfig:
    checkpoint_path: str = "checkpoints"
    tensorboard_log_path: Optional[str] = None
    checkpoint_interval: int = 100
