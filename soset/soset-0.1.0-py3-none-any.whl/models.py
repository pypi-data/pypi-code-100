import pydantic

import operator
import typing

class BaseModel(pydantic.BaseModel): pass

class Sets(BaseModel):
    @classmethod
    def __operate__(cls, operator, lhs, rhs):
        return cls.parse_obj \
        (
            {
                field: operator \
                (
                    getattr(lhs, field),
                    getattr(rhs, field),
                )
                for field in cls.__fields__.keys()
            }
        )

    def __or__(self, rhs):
        return self.__operate__(operator.__or__, self, rhs)

    def __and__(self, rhs):
        return self.__operate__(operator.__and__, self, rhs)

    def __bool__(self):
        return self.all()

    @classmethod
    def from_model(cls, model):
        return cls.parse_obj \
        (
            {
                key: {value} if value is not None else set()
                for key, value in model
            }
        )

    def keys(self):
        return self.dict().keys()

    def values(self):
        return self.dict().values()

    def all(self):
        return all(self.values())

    def any(self):
        return any(self.values())
