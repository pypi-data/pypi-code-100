"""DynamoDB block list module."""

from datetime import datetime
from typing import Any

from notelist.db.base.blocklist import BlockListManager


class DynamoDbBlockListManager(BlockListManager):
    """DynamoDB block list manager."""

    def __init__(
        self, root_dm: "DynamoDbManager", client: Any, resource: Any,
        table: str
    ):
        """Initialize instance.

        :param root_dm: Root database manager.
        :param client: DynamoDB client.
        :param resource: DynamoDB resource.
        :param table: DynamoDB table name.
        """
        self._root_dm = root_dm
        self._client = client
        self._table_name = table
        self._table = resource.Table(table)

    def create_table(self):
        """Create the table."""
        self._client.create_table(
            TableName=self._table_name,
            AttributeDefinitions=[
                {
                    "AttributeName": "id",
                    "AttributeType": "S"
                }
            ],
            KeySchema=[
                {
                    "AttributeName": "id",
                    "KeyType": "HASH"
                }
            ],
            BillingMode="PAY_PER_REQUEST"
        )

    def delete_table(self):
        """Delete the table."""
        self._client.delete_table(TableName=self._table_name)

    def contains(self, _id: str) -> bool:
        """Return whether a document with a given ID (JWT token) exists or not.

        If the document exists but is expired, it's deleted and `False` is
        returned.

        :param _id: Block list ID (JWD token).
        :return: Whether the block list contains the ID or not.
        """
        # Get document
        bl = self._table.get_item(Key={"id": _id}).get("Item")

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
        self._table.put_item(Item={"id": _id, "expiration": exp})

    def _delete(self, _id: str):
        """Delete a block list document given its ID (JWD token).

        :param _id: Block list ID (JWD token).
        """
        self._table.delete_item(Key={"id": _id})
