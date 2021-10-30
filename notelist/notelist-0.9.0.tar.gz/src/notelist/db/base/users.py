"""Base users module."""

from typing import Optional


class UserManager:
    """User manager.

    This is an abstract class and should not be instantiated.
    """

    def get_all(self) -> list[dict]:
        """Return all the user documents.

        :return: User documents.
        """
        raise NotImplementedError()

    def get_by_id(self, _id: str) -> Optional[dict]:
        """Return a user document given its ID.

        :param _id: User ID.
        :return: User document if it exists or None otherwise.
        """
        raise NotImplementedError()

    def get_by_username(self, username: str) -> Optional[dict]:
        """Return a user document given its username.

        :param username: Username.
        :return: User document if it exists or None otherwise.
        """
        raise NotImplementedError()

    def put(self, user: dict):
        """Put a user document.

        If an existing document has the same ID as `user`, the existing
        document is replaced with `user`.

        :param user: User document.
        """
        raise NotImplementedError()

    def delete(self, _id: str):
        """Delete a user document given its ID.

        :param _id: User ID.
        """
        raise NotImplementedError()
