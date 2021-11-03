from typing import Optional, List, Union, Any
from pydantic import BaseModel

from gtn_tools.schemas.constants import Status
from gtn_tools.schemas.base_schemas import FileBase


class TranslationInputFile(FileBase):
    input_list: Optional[List[str]]


class TranslationInputDocx(TranslationInputFile):
    docx_document: Optional[Any]


class TranslationOutputFile(FileBase):
    def save(self, path):
        with open(path, 'w') as f:
            f.write(self.file.read())


class Translation(BaseModel):
    input: Union[TranslationInputDocx,
                 TranslationInputFile,
                 List[str]]
    output: Optional[Union[TranslationOutputFile, List[str]]]

    source_lang: str
    target_lang: str
    num_chars: Optional[int]
    status: Status


class TranslationProject(BaseModel):
    translations: List[Translation]
    memsource_project_id: str
