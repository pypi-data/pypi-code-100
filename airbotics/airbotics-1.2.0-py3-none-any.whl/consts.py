from __future__ import annotations
from enum import Enum
from typing import TypedDict

REQUEST_TIMEOUT         = 5 # seconds
SDK_VERSION             = '1.2.0'
BASE_URL                = 'https://api.airbotics.io'
ENV_API_KEY             = 'AIR_API_KEY'
API_KEY_REGEX           = '^air_([a-zA-Z0-9]){42}$'
API_KEY_HEADER_NAME     = 'air-api-key'

class ContentType(str, Enum):
    '''Content-type to send in the request headers.'''
    JSON = 'application/json'
    PGM = 'image/x-portable-graymap'
    PNG = 'image/png'

class HTTPMethod(str, Enum):
    '''HTTP methods supported by the API.'''
    POST = 'POST'
    GET = 'GET'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'

class StatusCode(Enum):
    '''HTTP status codes supported by the API.'''
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    SERVER_ERROR = 500

class PgmCodec(str, Enum):
    '''Supported pgm codecs.'''
    P2 = 'P2'
    P5 = 'P5'

class RequestParams(TypedDict):
    '''Dict containing parameters for each request.'''
    method: HTTPMethod
    path: str
    body: any | None
    req_content_type: ContentType
    res_content_type: ContentType
