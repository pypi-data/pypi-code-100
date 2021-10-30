"""Base block list module."""


class BlockListManager:
    """Block list manager.

    This is an abstract class and should not be instantiated.
    """

    def contains(self, _id: str) -> bool:
        """Return whether a document with a given ID (JWT token) exists or not.

        If the document exists but is expired, it's deleted and `False` is
        returned.

        :param _id: Block list ID (JWD token).
        :return: Whether the block list contains the ID or not.
        """
        raise NotImplementedError()

    def put(self, _id: str, exp: int):
        """Put a block list document.

        :param _id: Block list ID (JWD token).
        :param exp: 10-digit expiration timestamp in seconds.
        """
        raise NotImplementedError()

    def _delete(self, _id: str):
        """Delete a block list document given its ID (JWD token).

        :param _id: Block list ID (JWD token).
        """
        raise NotImplementedError()
