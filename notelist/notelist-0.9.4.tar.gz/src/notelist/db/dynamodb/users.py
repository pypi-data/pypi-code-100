"""DynamoDB users module."""

from typing import Optional, Any

from boto3.dynamodb.conditions import Key

from notelist.db.base.users import UserManager


class DynamoDbUserManager(UserManager):
    """DynamoDB user manager."""

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
        if self._table_name not in self._root_dm.get_tables():
            self._client.create_table(
                TableName=self._table_name,
                AttributeDefinitions=[
                    {
                        "AttributeName": "id",
                        "AttributeType": "S"
                    },
                    {
                        "AttributeName": "username",
                        "AttributeType": "S"
                    }
                ],
                KeySchema=[
                    {
                        "AttributeName": "id",
                        "KeyType": "HASH"
                    }
                ],
                GlobalSecondaryIndexes=[
                    {
                        "IndexName": "username_index",
                        "KeySchema": [
                            {
                                "AttributeName": "username",
                                "KeyType": "HASH"
                            }
                        ],
                        "Projection": {
                            "ProjectionType": "ALL"
                        }
                    }
                ],
                BillingMode="PAY_PER_REQUEST"
            )

    def delete_table(self):
        """Delete the table."""
        if self._table_name in self._root_dm.get_tables():
            self._client.delete_table(TableName=self._table_name)

    def get_all(self) -> list[dict]:
        """Return all the user documents.

        :return: User documents.
        """
        users = []
        done = False
        lek = None  # Last Evaluated Key

        while not done:
            args = {}

            if lek is not None:
                args["ExclusiveStartKey"] = lek

            r = self._table.scan(**args)
            users.extend(r.get("Items", []))
            lek = r.get("LastEvaluatedKey")
            done = lek is None

        return sorted(users, key=lambda u: u["username"])

    def get_by_id(self, _id: str) -> Optional[dict]:
        """Return a user document given its ID.

        :param _id: User ID.
        :return: User document if it exists or None otherwise.
        """
        r = self._table.get_item(Key={"id": _id})
        return r.get("Item")

    def get_by_username(self, username: str) -> Optional[dict]:
        """Return a user document given its username.

        :param username: Username.
        :return: User document if it exists or None otherwise.
        """
        users = []
        done = False
        lek = None  # Last Evaluated Key

        while not done:
            args = {
                "IndexName": "username_index",
                "KeyConditionExpression": Key("username").eq(username)}

            if lek is not None:
                args["ExclusiveStartKey"] = lek

            r = self._table.query(**args)
            users.extend(r.get("Items", []))
            lek = r.get("LastEvaluatedKey")
            done = len(users) > 0 or lek is None

        return users[0] if len(users) > 0 else None

    def put(self, user: dict):
        """Put a user document.

        If an existing document has the same ID as `user`, the existing
        document is replaced with `user`.

        :param user: User document.
        """
        self._table.put_item(Item=user)

    def delete(self, _id: str):
        """Delete a user document given its ID.

        :param _id: User ID.
        """
        self._table.delete_item(Key={"id": _id})
