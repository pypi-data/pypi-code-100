"""DynamoDB package."""

from typing import Optional

import boto3

from notelist.db.base import DbManager
from notelist.db.dynamodb.users import DynamoDbUserManager
from notelist.db.dynamodb.notebooks import DynamoDbNotebookManager
from notelist.db.dynamodb.notes import DynamoDbNoteManager
from notelist.db.dynamodb.blocklist import DynamoDbBlockListManager


class DynamoDbManager(DbManager):
    """DynamoDB manager."""

    def __init__(
        self, ep: Optional[str], reg: Optional[str], aki: Optional[str],
        sak: Optional[str], st: Optional[str], us_tab: str, nb_tab: str,
        no_tab: str, bl_tab: str,
    ):
        """Initialize instance.

        :param ep: AWS endpoint URL.
        :param reg: AWS region name.
        :param aki: AWS Acess Key ID.
        :param sak: AWS Secret Access Key.
        :param st: AWS Session Token.
        :param us_tab: DynamoDB users table name. E.g. "users".
        :param nb_tab: DynamoDB notebooks table name. E.g. "notebook".
        :param no_tab: DynamoDB notes table name. E.g. "notes".
        :param bl_tab: DynamoDB block list table name. E.g. "blocklist".
        """
        options = {}

        if ep is not None:
            options["endpoint_url"] = ep

        if reg is not None:
            options["region_name"] = reg

        if aki is not None:
            options["aws_access_key_id"] = aki

        if sak is not None:
            options["aws_secret_access_key"] = sak

        if st is not None:
            options["aws_session_token"] = st

        # AWS interfaces
        self._client = boto3.client("dynamodb", **options)
        res = boto3.resource("dynamodb", **options)

        # Managers
        self._users = DynamoDbUserManager(self, self._client, res, us_tab)
        self._notebooks = DynamoDbNotebookManager(
            self, self._client, res, nb_tab
        )
        self._notes = DynamoDbNoteManager(self, self._client, res, no_tab)
        self._blocklist = DynamoDbBlockListManager(
            self, self._client, res, bl_tab
        )

    def get_tables(self):
        """Return the table names."""
        tables = []
        done = False
        let = None  # Last Evaluated Table Name

        while not done:
            args = {} if let is None else {"ExclusiveStartTableName": let}
            r = self._client.list_tables(**args)
            tables.extend(r.get("TableNames", []))
            let = r.get("LastEvaluatedTableName")
            done = let is None

        return tables

    def create_db(self):
        """Create the database."""
        self._users.create_table()
        self._notebooks.create_table()
        self._notes.create_table()
        self._blocklist.create_table()

    def delete_db(self):
        """Delete the database."""
        self._users.delete_table()
        self._notebooks.delete_table()
        self._notes.delete_table()
        self._blocklist.delete_table()

    @property
    def users(self) -> DynamoDbUserManager:
        """Return the user data manager.

        :return: `DynamoDbUserManager` instance.
        """
        return self._users

    @property
    def notebooks(self) -> DynamoDbNotebookManager:
        """Return the notebook data manager.

        :return: `DynamoDbNotebookManager` instance.
        """
        return self._notebooks

    @property
    def notes(self) -> DynamoDbNoteManager:
        """Return the note data manager.

        :return: `DynamoDbNoteManager` instance.
        """
        return self._notes

    @property
    def blocklist(self) -> DynamoDbBlockListManager:
        """Return the block list manager.

        :return: `DynamoDbBlockListManager` instance.
        """
        return self._blocklist
