from typing import List, Optional
from pydantic import BaseModel

from .base_schemas import Provider, FileBase
from .constants import StatusPostEditing, Status


class TranscriptionInputFile(FileBase):
    frame_rate: Optional[int]
    channels: Optional[int]
    seconds: Optional[float]


class TranscriptionOutputFile(FileBase):
    def save(self, path):
        with open(path, 'w') as f:
            f.write(self.file.read())


class TranscriptionProvider(Provider):
    ...


class Transcription(BaseModel):
    input_file: TranscriptionInputFile
    output_file: Optional[TranscriptionOutputFile]
    text: Optional[List[str]]

    provider: Optional[TranscriptionProvider]
    status: Status


class TranscriptionPostEditing(Transcription):
    status: StatusPostEditing
    memsource_project_id: str
