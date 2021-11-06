import json

from marshmallow.exceptions import ValidationError
from multipart.multipart import parse_options_header
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from typing import Type
from marshmallow import Schema


async def get_body(request: Request) -> Response:
    content_type_header = request.headers.get("Content-Type")
    content_type, options = parse_options_header(content_type_header)
    if content_type == b"application/json":
        try:
            return await request.json()
        except json.decoder.JSONDecodeError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif (
        content_type == b"multipart/form-data"
        or content_type == b"application/x-www-form-urlencoded"
    ):
        try:
            return await request.form()
        except TypeError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    else:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


async def get_form(request: Request, Schema: Type[Schema]) -> dict:
    body = await get_body(request)
    schema = Schema()
    try:
        return schema.load(body)
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
