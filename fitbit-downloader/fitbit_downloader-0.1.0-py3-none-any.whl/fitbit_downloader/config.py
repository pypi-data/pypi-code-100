import datetime
from enum import Enum
from pathlib import Path
from typing import Final, Optional, List

from pyappconf import BaseConfig, AppConfig, ConfigFormats
from pydantic import BaseModel, Field

APP_NAME: Final = "fitbit-downloader"


class OAuthConfig(BaseModel):
    access_token: str
    refresh_token: str
    expires_at: float

    @property
    def expires_at_time(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.expires_at)


class Dataset(str, Enum):
    STEPS = "steps"
    HEART = "heart"
    ELEVATION = "elevation"
    DISTANCE = "distance"
    FLOORS = "floors"
    SLEEP = "sleep"
    ACTIVITIES = "activities"


class DownloadConfig(BaseModel):
    datasets: List[Dataset] = Field(
        default_factory=lambda: [
            Dataset.STEPS,
            Dataset.HEART,
            Dataset.ELEVATION,
            Dataset.DISTANCE,
            Dataset.FLOORS,
            Dataset.SLEEP,
            Dataset.ACTIVITIES,
        ]
    )
    out_folder: Path = Path(__file__).parent.parent / "Data"


class Config(BaseConfig):
    client_id: str
    client_secret: str
    oauth_config: Optional[OAuthConfig]
    download: DownloadConfig = DownloadConfig()

    _settings = AppConfig(
        app_name=APP_NAME,
        default_format=ConfigFormats.TOML,
        config_name="fitbit-downloader",
    )

    class Config:
        env_file = ".env"
        env_prefix = "FITBIT_DOWNLOADER_"


if __name__ == "__main__":
    print(Config.load_recursive())
