from typing import Optional

import pydantic


class RegisterUserInput(pydantic.BaseModel):
    size: pydantic.PositiveInt
    name: Optional[str] = None
    is_signed: bool = False
    fraction_places: pydantic.conint(ge=0) = 0

    class Config:
        extra = "forbid"
