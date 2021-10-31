"""Base package."""

from notelist.db.base.users import UserManager
from notelist.db.base.notebooks import NotebookManager
from notelist.db.base.notes import NoteManager
from notelist.db.base.blocklist import BlockListManager


class DbManager:
    """Database manager.

    This is an abstract class and should not be instantiated.
    """

    def create_db(self):
        """Create the database."""
        raise NotImplementedError()

    def delete_db(self):
        """Delete the database."""
        raise NotImplementedError()

    @property
    def users(self) -> UserManager:
        """Return the user data manager.

        :return: `UserManager` instance.
        """
        raise NotImplementedError()

    @property
    def notebooks(self) -> NotebookManager:
        """Return the notebook data manager.

        :return: `NotebookManager` instance.
        """
        raise NotImplementedError()

    @property
    def notes(self) -> NoteManager:
        """Return the note data manager.

        :return: `NoteManager` instance.
        """
        raise NotImplementedError()

    @property
    def blocklist(self) -> BlockListManager:
        """Return the block list manager.

        :return: `BlockListManager` instance.
        """
        raise NotImplementedError()
