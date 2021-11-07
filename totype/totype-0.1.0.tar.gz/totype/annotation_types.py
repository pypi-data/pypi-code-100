import datetime as dt
from typing import Any, Union, Literal, AnyStr

OldValueT = Any
NewValueT = Any
RowNum = int
RowT = Union[list, tuple, dict]
ErrorPolicyLiteralT = Literal["default", "raise", "ignore"]
OldStringT = AnyStr
NewStringT = AnyStr
StrOrDatetime = Union[str, dt.datetime, dt.date]
