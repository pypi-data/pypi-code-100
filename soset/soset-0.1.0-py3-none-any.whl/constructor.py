import pydantic

import typing

from . import models

class SetsMeta(type):
    def __getitem__(cls, item):
        return pydantic.create_model \
        (
            cls.__name__,
            ** \
            {
                field.name: \
                (
                    typing.Set[field.type_],
                    (
                        ...
                        if field.required
                        else pydantic.Field \
                        (
                            default_factory = set,
                        )
                    ),
                )
                for field in item.__fields__.values()
            },
            __base__ = models.Sets,
        )

class Sets(metaclass = SetsMeta): pass
