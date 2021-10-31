import re
from typing import List, Optional

import click
from click import Context, Parameter, ParamType
from PyPDF2 import PdfFileReader
from PyPDF2.utils import PdfReadError


class PDFReader(click.File):
    def __init__(
        self,
        errors: Optional[str] = "strict",
        lazy: Optional[bool] = None,
        atomic: bool = False,
    ) -> None:
        super().__init__(
            mode="rb", encoding=None, errors=errors, lazy=lazy, atomic=atomic
        )

    def convert(
        self, value: str, param: Optional[Parameter], ctx: Optional[Context]
    ) -> Optional[PdfFileReader]:
        file = super().convert(value, param, ctx)
        try:
            return PdfFileReader(file)
        except PdfReadError as err:
            self.fail(str(err))


PAGE_NO = re.compile(r"\d+")
PAGE_RANGE = re.compile(r"\d+-\d+")


class PageNoList(ParamType):
    name = "INT | INT-INT"

    def __init__(self, allow_all: bool = False) -> None:
        super().__init__()
        self._allow_all = allow_all

    def convert(
        self, value: str, param: Optional[Parameter], ctx: Optional[Context]
    ) -> List[int]:
        if self._allow_all and value.lower() == "all":
            return []
        if PAGE_RANGE.fullmatch(value):
            start, end = tuple(int(num) for num in value.split("-"))
            if end > start > 0:
                return list(range(start, end + 1))
        elif PAGE_NO.fullmatch(value):
            num = int(value)
            if num > 0:
                return [int(value)]
        self.fail(f"{value} is not valid page number, or range")
