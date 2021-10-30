import yaml
import os
import json
from abc import ABC, abstractmethod


class DataStore(ABC):

    @abstractmethod
    def save(self, data: dict) -> None:
        """save the data from the ConfigsDict to the designated target"""

    @abstractmethod
    def load(self) -> dict:
        """load the configs data from the designated target"""

    @abstractmethod
    def is_empty(self) -> bool:
        """whether there is data in the store"""


class RamStore(DataStore):

    def __init__(self):
        self._data: dict = dict()

    def save(self, data: dict) -> None:
        """store the dict in ram"""
        self._data = data

    def load(self) -> dict:
        return self._data

    def is_empty(self):
        return self.load() == {}


class FileStore(DataStore):

    def __init__(self, filename: str):
        self.filename = filename

    def load(self) -> dict:
        return self._load()

    def save(self, data: dict) -> None:
        self._dump(data)

    def is_empty(self) -> bool:
        """return True if the file doesn't exist or no data is stored in the file"""
        if not os.path.exists(self.filename):
            return True
        if self.load() == {}:
            return True
        return False

    def _load(self) -> dict:
        """
        store specific loading of data needs to override this function

        :return: configurations as a dict
        """

    def _dump(self, data: dict) -> None:
        """
        store specific saving of data needs to override this function
        """

    def __repr__(self) -> str:
        return f"FileStore({self.load()})"


class YAMLFileStore(FileStore):

    def _load(self) -> dict:
        if os.path.isfile(self.filename):
            with open(self.filename, 'r') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
            if data:
                return data
        return {}

    def _dump(self, data: dict) -> None:
        with open(self.filename, 'w') as f:
            yaml.safe_dump(data, f)

    def __repr__(self) -> str:
        return f"YAMLFileStore({self.load()})"


class JSONFileStore(FileStore):

    def _load(self) -> dict:
        if os.path.isfile(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                if data:
                    return data
        return {}

    def _dump(self, data: dict) -> None:
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def __repr__(self) -> str:
        return f"YAMLFileStore({self.load()})"


class DataStoreException(Exception):
    pass


class DataStoreNotFound(DataStoreException):
    pass


class DataStoreDetectionFailedException(DataStoreException):
    pass


def get_store(filename: str, store_type: str = "auto") -> DataStore:
    FILESTORE_EXTENSION = {
        "yaml": ["yaml", "yml"],
        "json": ["json"]
    }

    # if store_type is auto, the store type is guessed from file extension
    if store_type == "auto":
        file_ext = filename.split(".")[-1]
    else:
        file_ext = ""

    if store_type.upper() == "RAM" or filename.upper() == "RAM":
        return RamStore()
    elif store_type.lower() in FILESTORE_EXTENSION["yaml"] \
            or file_ext.lower() in FILESTORE_EXTENSION["yaml"]:
        return YAMLFileStore(filename)
    elif store_type.lower() in FILESTORE_EXTENSION["json"] \
            or file_ext.lower() in FILESTORE_EXTENSION["json"]:
        return JSONFileStore(filename)
    else:
        raise DataStoreDetectionFailedException(f"Failed to identify type of FileStore {filename}")
