from typing import Optional, Dict, Any
from pydantic import BaseModel


class Provider(BaseModel):
    identifier: str
    name: str
    url: Optional[str]
    apis: Dict[str, Any]


class FileBase(BaseModel):
    file: Any
    filename: str
    type: str
    lang: str
