import strawberry as graphql  # noqa: F401
import uvicorn as WebServer  # noqa: F401
from fastapi import APIRouter as Router  # noqa: F401
from fastapi import Body  # noqa: F401
from fastapi import FastAPI as WebApp  # noqa: F401
from graphql import ValidationRule  # noqa: F401
from strawberry.asgi import GraphQL as GraphQLApp  # noqa: F401
from strawberry.extensions import AddValidationRules  # noqa: F401
from strawberry.permission import BasePermission  # noqa: F401
from strawberry.types import Info as GraphQLInfo  # noqa: F401

from .value_object import Enum, StrEnum


def graphql_enum(python_enum: Enum):
    return graphql.enum(
        StrEnum(python_enum.__name__, ((e.name, e.value) for e in python_enum))
    )
