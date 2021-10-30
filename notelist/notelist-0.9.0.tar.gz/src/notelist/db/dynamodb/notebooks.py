"""DynamoDB notebooks module."""

from typing import Optional, Any

from boto3.dynamodb.conditions import Key

from notelist.db.base.notebooks import NotebookManager


class DynamoDbNotebookManager(NotebookManager):
    """DynamoDB notebook manager."""

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
                },
                {
                    "AttributeName": "user_id",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "name",
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
                    "IndexName": "user_id_index",
                    "KeySchema": [
                        {
                            "AttributeName": "user_id",
                            "KeyType": "HASH"
                        }
                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    }
                },
                {
                    "IndexName": "user_id_name_index",
                    "KeySchema": [
                        {
                            "AttributeName": "user_id",
                            "KeyType": "HASH"
                        },
                        {
                            "AttributeName": "name",
                            "KeyType": "RANGE"
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
        self._client.delete_table(TableName=self._table_name)

    def get_by_user(self, user_id: str) -> list[dict]:
        """Return all the notebook documents of a given user.

        :param user_id: User ID.
        :return: Notebook documents.
        """
        notebooks = []
        done = False
        lek = None  # Last Evaluated Key

        while not done:
            args = {
                "IndexName": "user_id_index",
                "KeyConditionExpression": Key("user_id").eq(user_id)}

            if lek is not None:
                args["ExclusiveStartKey"] = lek

            r = self._table.query(**args)
            notebooks.extend(r.get("Items", []))
            lek = r.get("LastEvaluatedKey")
            done = lek is None

        return sorted(notebooks, key=lambda u: u["name"])

    def get_by_id(self, _id: str) -> Optional[dict]:
        """Return a notebook document given its ID.

        :param _id: Notebook ID.
        :return: Notebook document if it exists or None otherwise.
        """
        r = self._table.get_item(Key={"id": _id})
        return r.get("Item")

    def get_by_name(self, user_id: str, name: str) -> Optional[dict]:
        """Return a notebook document given its user and name.

        :param user_id: Notebook user ID.
        :param name: Notebook name.
        :return: Notebook document if it exists or None otherwise.
        """
        notebooks = []
        done = False
        lek = None  # Last Evaluated Key

        while not done:
            args = {
                "IndexName": "user_id_name_index",
                "KeyConditionExpression":
                    Key("user_id").eq(user_id) & Key("name").eq(name)}

            if lek is not None:
                args["ExclusiveStartKey"] = lek

            r = self._table.query(**args)
            notebooks.extend(r.get("Items", []))
            lek = r.get("LastEvaluatedKey")
            done = len(notebooks) > 0 or lek is None

        return notebooks[0] if len(notebooks) > 0 else None

    def put(self, notebook: dict):
        """Put a notebook document.

        If an existing document has the same ID as `notebook`, the existing
        document is replaced with `notebook`.

        :param notebook: Notebook document.
        """
        self._table.put_item(Item=notebook)

    def delete(self, _id: str):
        """Delete a notebook document given its ID.

        :param _id: Notebook ID.
        """
        self._table.delete_item(Key={"id": _id})
