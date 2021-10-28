from .invalid_content import InvalidContent
from .invalid_key import InvalidKey
from .unknown_key import UnknownKey
from .existing_key import ExistingKey
from .file_overwrite import FileOverwrite


class InvalidContent(InvalidContent): ...


class InvalidKey(InvalidKey): ...


class UnknownKey(UnknownKey): ...


class ExistingKey(ExistingKey): ...


class FileOverwrite(FileOverwrite): ...
