"""Local Storage block list module."""

from datetime import datetime

from notelist.db.base.blocklist import BlockListManager


class LocalStBlockListManager(BlockListManager):
    """Local Storage block list manager."""

    def __init__(self, root_dm: "LocalStorageManager"):
        """Initialize instance.

        :param root_dm: Root database manager.
        """
        self._root_dm = root_dm

    def contains(self, _id: str) -> bool:
        """Return whether a document with a given ID (JWT token) exists or not.

        If the document exists but is expired, it's deleted and `False` is
        returned.

        :param _id: Block list ID (JWD token).
        :return: Whether the block list contains the ID or not.
        """
        # Get document
        bl = self._root_dm.get_data()["notebooks"].get(_id)

        # Check if the document exists
        if bl is None:
            return False

        # Check if the document is expired
        exp = bl["expiration"]
        now = int(datetime.now().timestamp())

        if now > exp:
            self._delete(_id)
            return False

        return True

    def put(self, _id: str, exp: int):
        """Put a block list document.

        :param _id: Block list ID (JWD token).
        :param exp: 10-digit expiration timestamp in seconds.
        """
        data = self._root_dm.get_data()
        data["blocklist"][_id] = {"expiration": exp}

        self._root_dm.save_data(data)

    def _delete(self, _id: str):
        """Delete a block list document given its ID (JWD token).

        :param _id: Block list ID (JWD token).
        """
        k = "blocklist"
        data = self._root_dm.get_data()

        if _id in data[k]:
            data[k].pop(_id)
            self._root_dm.save_data(data)
