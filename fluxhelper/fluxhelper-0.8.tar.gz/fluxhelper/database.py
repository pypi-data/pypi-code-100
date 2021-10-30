from montydb import MontyClient, set_storage
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import motor.motor_asyncio


class ConnectionError(Exception):
    pass


class Database:

    """
    Initialize a database. All this class really does is decide whether to use MontyClient or MongoClient or AsyncIOMotorClient.
    """

    def __init__(self, dbName: str, **kwargs):

        # Parameters
        self.connectionString = kwargs.get("connectionString")
        self.useMotor = kwargs.get("useMotor", False)
        self.dbPath = kwargs.get("dbPath", "./db")
        self.logging = kwargs.get("logging")
        self.cacheModified = kwargs.get("cacheModified", 5)
        self.dbName = dbName

        self.client = None
        self.db = None
        self.type = "tinydb"

        if self.connectionString:
            try:
                if not self.useMotor:
                    self.client = MongoClient(
                        self.connectionString, serverSelectionTimeoutMS=2000
                    )
                else:
                    self.client = motor.motor_asyncio.AsyncIOMotorClient(
                        self.connectionString, serverSelectionTimeoutMS=2000
                    )

                self.db = self.client[self.dbName]

                if not self.useMotor:
                    self.client.server_info()

                self.type = "mongo"

                if self.logging:
                    self.logging.success("Successfully connected to mongodb.")
            except ServerSelectionTimeoutError:
                if self.logging:
                    self.logging.warning(
                        "Failed to connect to mongodb, falling back to tinydb."
                    )

        if self.type == "tinydb":
            try:
                set_storage(self.dbPath, cache_modified=self.cacheModified)
                self.client = MontyClient(self.dbPath)
                self.db = self.client[self.dbName]

                if self.logging:
                    self.logging.success("Successfully connected to tinydb.")
            except Exception as e:
                raise ConnectionError(f"Failed to connect to tinydb. ({e})")
