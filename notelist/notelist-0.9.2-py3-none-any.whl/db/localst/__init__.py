"""Local Storage package."""

from os import remove
from os.path import exists
from collections import OrderedDict
import json

from notelist.db.base import DbManager
from notelist.db.localst.users import LocalStUserManager
from notelist.db.localst.notebooks import LocalStNotebookManager
from notelist.db.localst.notes import LocalStNoteManager
from notelist.db.localst.blocklist import LocalStBlockListManager


class LocalStManager(DbManager):
    """Local Storage manager."""

    def __init__(self, path: str):
        """Initialize instance.

        :param path: JSON file path.
        """
        self._path = path

        # Managers
        self._users = LocalStUserManager(self)
        self._notebooks = LocalStNotebookManager(self)
        self._notes = LocalStNoteManager(self)
        self._blocklist = LocalStBlockListManager(self)

    def create_db(self):
        """Create the database."""
        pass

    def delete_db(self):
        """Delete the database."""
        if exists(self._path):
            remove(self._path)

    def get_data(self) -> dict:
        """Return data from the JSON file.

        :return: Data.
        """
        if exists(self._path):
            with open(self._path, "r") as f:
                data = OrderedDict(json.load(f))
        else:
            data = OrderedDict(users={}, notebooks={}, notes={}, blocklist={})

        return data

    def save_data(self, data: dict):
        """Save data to the JSON file.

        :param data: Data.
        """
        with open(self._path, "w") as f:
            json.dump(data, f, indent=4)

    @property
    def users(self) -> LocalStUserManager:
        """Return the user manager.

        :return: `LocalStUserManager` instance.
        """
        return self._users

    @property
    def notebooks(self) -> LocalStNotebookManager:
        """Return the notebook manager.

        :return: `LocalStNotebookManager` instance.
        """
        return self._notebooks

    @property
    def notes(self) -> LocalStNoteManager:
        """Return the note manager.

        :return: `LocalStNoteManager` instance.
        """
        return self._notes

    @property
    def blocklist(self) -> LocalStBlockListManager:
        """Return the block list manager.

        :return: `LocalStBlockListManager` instance.
        """
        return self._blocklist
