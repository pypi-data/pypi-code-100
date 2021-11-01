"""DynamoDB notes module."""

from typing import Optional, Any

from boto3.dynamodb.conditions import Key, Attr

from notelist.db.base.notes import NoteManager


class DynamoDbNoteManager(NoteManager):
    """DynamoDB note manager."""

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
                        "AttributeName": "notebook_id",
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
                        "IndexName": "notebook_id_index",
                        "KeySchema": [
                            {
                                "AttributeName": "notebook_id",
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

    def _select_note(self, n: dict, tags: list[str], no_tags: bool) -> bool:
        """Return whether a note document is selected or not based on its tags.

        :param n: Note document.
        :param tags: Tags filter.
        :param no_tags: No Tags filter.
        :return: `True` if `n` is selected or `False` otherwise.
        """
        k = "tags"
        note_tags = n[k] if k in n else []

        return (
            (len(note_tags) == 0 and no_tags) or
            any(map(lambda t: t in note_tags, tags)))

    def get_by_filter(
        self, notebook_id: str, archived: Optional[bool] = None,
        tags: Optional[list[str]] = None, no_tags: bool = False,
        last_mod: bool = False, asc: bool = True
    ) -> list[dict]:
        """Return all the note documents of a given notebook by a filter.

        :param notebook_id: Notebook ID.
        :param archived: State filter (include archived notes or not archived
        notes).
        :param tags: Tags filter (include notes that has any of these tags).
        This list contains tag names.
        :param no_tags: Notes with No Tags filter (include notes with no tags).
        This filter is only applicable if a tag filter has been provided, i.e.
        `tags` is not None).
        :param last_mod: `True` if notes should be sorted by their Last
        Modified timestamp. `False` if notes should be sorted by their Created
        timestamp (default).
        :param asc: Whether the notes order should be ascending (default) or
        not.
        :return: Note documents.
        """
        notes = []
        done = False
        lek = None  # Last Evaluated Key

        while not done:
            args = {
                "IndexName": "notebook_id_index",
                "KeyConditionExpression": Key("notebook_id").eq(notebook_id)
            }

            if archived in (True, False):
                args["FilterExpression"] = Attr("archived").eq(archived)

            if lek is not None:
                args["ExclusiveStartKey"] = lek

            r = self._table.query(**args)
            notes.extend(r.get("Items", []))
            lek = r.get("LastEvaluatedKey")
            done = lek is None

        # Tags and Not Tags filters
        if tags is not None:
            notes = filter(
                lambda n: self._select_note(n, tags, no_tags), notes)

        # Sort notes
        k = "last_modified" if last_mod else "created"
        r = not asc

        return sorted(notes, key=lambda n: n[k], reverse=r)

    def get_by_id(self, _id: str) -> Optional[dict]:
        """Return a note document given its ID.

        :param _id: Note ID.
        :return: Note document.
        """
        r = self._table.get_item(Key={"id": _id})
        return r.get("Item")

    def put(self, note: dict):
        """Put a note document.

        If an existing document has the same ID as `note`, the existing
        document is replaced with `note`.

        :param note: Note document.
        """
        self._table.put_item(Item=note)

    def delete(self, _id: str):
        """Delete a note document given its ID.

        :param _id: Note ID.
        """
        self._table.delete_item(Key={"id": _id})
