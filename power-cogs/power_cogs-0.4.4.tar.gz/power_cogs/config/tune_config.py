from dataclasses import field
from typing import Any, Dict, List, Optional

from pydantic.dataclasses import dataclass

from power_cogs.config import Config


@dataclass
class MlflowLoggerConfig(Config):
    experiment_name: Optional[str] = None
    save_artifact: bool = False


@dataclass
class WandbLoggerConfig(Config):
    project: Optional[str] = None
    log_config: bool = False
    reinit: bool = False
    wandb_api_key_file: Optional[str] = None


@dataclass
class TuneConfig(Config):
    metric: str = "loss"
    mode: str = "min"
    num_samples: int = 1
    name: Optional[str] = ""
    checkpoint_freq: int = 100
    checkpoint_at_end: bool = True
    callbacks: List[Any] = field(default_factory=lambda: [])
    additional_config: Dict[str, Any] = field(default_factory=lambda: {})


@dataclass
class TuneWrapperConfig(Config):
    tune_config: Any = TuneConfig()
    wandb: Any = WandbLoggerConfig()
    mlflow: Any = MlflowLoggerConfig()
