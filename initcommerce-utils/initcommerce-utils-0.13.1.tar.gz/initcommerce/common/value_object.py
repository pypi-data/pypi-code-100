from datetime import datetime
from enum import Enum
from enum import IntEnum as PythonIntEnum

from pydantic import BaseModel, Field, validator  # noqa: F401

from initcommerce.common.uuid import UUID as ID  # noqa: F401


class StrEnum(str, Enum):
    def __str__(self):
        return str(self.value)


class IntEnum(PythonIntEnum):
    def __str__(self):
        return self.name


class CreateTimeStampMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UpdateTimeStampMixin(BaseModel):
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class BaseValueObj(BaseModel):
    """General type for types that are not saved anywhere but are used in app"""
