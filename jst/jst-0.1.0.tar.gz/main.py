import json
import datetime
import typing

from pydantic import BaseModel
import jst


class Foo(BaseModel):
    a: int
    b: str
    c: datetime.datetime
    d: typing.Optional[int]


print(Foo.schema_json())

bq_schema = jst.convert_bq(Foo.schema_json(), "panic")
print(bq_schema)
