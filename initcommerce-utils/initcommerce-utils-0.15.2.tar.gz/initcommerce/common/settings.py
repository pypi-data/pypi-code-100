from pydantic import BaseSettings as PydanticSettings
from pydantic import validator  # noqa: F401


class BaseSettings(PydanticSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
