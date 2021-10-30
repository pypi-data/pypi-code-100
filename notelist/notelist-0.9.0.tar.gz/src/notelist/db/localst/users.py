"""Local Storage users module."""

from typing import Optional

from notelist.db.base.users import UserManager


class LocalStUserManager(UserManager):
    """Local Storage user manager."""

    def __init__(self, root_dm: "LocalStorageManager"):
        """Initialize instance.

        :param root_dm: Root data manager.
        """
        self._root_dm = root_dm

    def get_all(self) -> list[dict]:
        """Return all the user documents.

        :return: User documents.
        """
        users = self._root_dm.get_data()["users"].items()
        users = [{"id": _id} | u for _id, u in users]

        return sorted(users, key=lambda u: u["username"])

    def get_by_id(self, _id: str) -> Optional[dict]:
        """Return a user document given its ID.

        :param _id: User ID.
        :return: User document if it exists or None otherwise.
        """
        user = self._root_dm.get_data()["users"].get(_id)

        if user is not None:
            user = {"id": _id} | user

        return user

    def get_by_username(self, username: str) -> Optional[dict]:
        """Return a user document given its username.

        :param username: Username.
        :return: User document if it exists or None otherwise.
        """
        user = None

        for _id, u in self._root_dm.get_data()["users"].items():
            if u["username"] == username:
                user = {"id": _id} | u
                break

        return user

    def put(self, user: dict):
        """Put a user document.

        If an existing document has the same ID as `user`, the existing
        document is replaced with `user`.

        :param user: User document.
        """
        user = user.copy()
        _id = user.pop("id")

        data = self._root_dm.get_data()
        data["users"][_id] = user

        self._root_dm.save_data(data)

    def delete(self, _id: str):
        """Delete a user document given its ID.

        :param _id: User ID.
        """
        k = "users"
        data = self._root_dm.get_data()

        if _id in data[k]:
            data[k].pop(_id)
            self._root_dm.save_data(data)
