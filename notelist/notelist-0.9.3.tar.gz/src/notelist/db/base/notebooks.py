"""Base notebooks module."""

from typing import Optional


class NotebookManager:
    """Notebook manager.

    This is an abstract class and should not be instantiated.
    """

    def get_by_user(self, user_id: str) -> list[dict]:
        """Return all the notebook documents of a given user.

        :param user_id: User ID.
        :return: Notebook documents.
        """
        raise NotImplementedError()

    def get_by_id(self, _id: str) -> Optional[dict]:
        """Return a notebook document given its ID.

        :param _id: Notebook ID.
        :return: Notebook document if it exists or None otherwise.
        """
        raise NotImplementedError()

    def get_by_name(self, user_id: str, name: str) -> Optional[dict]:
        """Return a notebook document given its user and name.

        :param user_id: Notebook user ID.
        :param name: Notebook name.
        :return: Notebook document if it exists or None otherwise.
        """
        raise NotImplementedError()

    def put(self, notebook: dict):
        """Put a notebook document.

        If an existing document has the same ID as `notebook`, the existing
        document is replaced with `notebook`.

        :param notebook: Notebook document.
        """
        raise NotImplementedError()

    def delete(self, _id: str):
        """Delete a notebook document given its ID.

        :param _id: Notebook ID.
        """
        raise NotImplementedError()
