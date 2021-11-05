from pathlib import Path
from typing import Literal
from jsonclasses_server.api_class import API
from .kotlin import kotlin
from .swift import swift
from .ts import ts


def package(dest: Path, api: API, lang: Literal['ts', 'swift', 'kotlin']):
    match lang:
        case 'swift':
            swift(dest, api)
        case 'kotlin':
            kotlin(dest, api)
        case 'ts':
            ts(dest, api)
