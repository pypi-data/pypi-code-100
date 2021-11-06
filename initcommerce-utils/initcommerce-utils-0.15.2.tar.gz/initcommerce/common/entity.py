import abc
from typing import Optional

from pydantic import BaseConfig, BaseModel, Field, validator  # noqa: F401


class BaseEntity(BaseModel, metaclass=abc.ABCMeta):
    id: Optional[int]

    class Config(BaseConfig):
        orm_mode = True
