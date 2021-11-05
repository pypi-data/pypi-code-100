from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic.dataclasses import dataclass

# internal
from power_cogs.config import Config


class ClusterType(Enum):
    LOCAL: str = "LOCAL"
    RAY: str = "RAY"

    @classmethod
    def _missing_(cls, value) -> ClusterType:
        print(
            "value {} is not a valid enum value for ClusterType, defaulting to LOCAL".format(
                value
            )
        )
        return ClusterType.LOCAL


@dataclass
class ClusterConfig(Config):
    name: str = ""
    cluster_config_path: Optional[str] = None
    join_cluster: bool = False
    cluster_type: ClusterType = ClusterType.LOCAL


@dataclass
class LocalClusterConfig(ClusterConfig):
    pass


@dataclass
class RayClusterConfig(ClusterConfig):
    cluster_type: ClusterType = ClusterType.RAY
