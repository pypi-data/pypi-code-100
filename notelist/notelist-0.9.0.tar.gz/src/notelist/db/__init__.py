"""Database package."""

from notelist.config import get_sm
from notelist.db.base import DbManager
from notelist.db.mongodb import MongoDbManager
from notelist.db.dynamodb import DynamoDbManager
from notelist.db.localst import LocalStManager


# Settings
_db_sys_key = "NL_DB_SYS"

_mongodb_keys = (
    "NL_MONGODB_URI", "NL_MONGODB_DB", "NL_MONGODB_US_COL",
    "NL_MONGODB_NB_COL", "NL_MONGODB_NO_COL", "NL_MONGODB_BL_COL"
)

_dynamodb_keys_1 = (
    "NL_DYNAMODB_AWS_ENDPOINT", "NL_DYNAMODB_AWS_REGION",
    "NL_DYNAMODB_AWS_ACCESS_KEY_ID", "NL_DYNAMODB_AWS_SECRET_ACCESS_KEY",
    "NL_DYNAMODB_AWS_SESSION_TOKEN"
)

_dynamodb_keys_2 = (
    "NL_DYNAMODB_US_TAB", "NL_DYNAMODB_NB_TAB", "NL_DYNAMODB_NO_TAB",
    "NL_DYNAMODB_BL_TAB"
)

_localst_path_key = "NL_LOCALST_PATH"


def _get_values(keys: tuple[str, ...], exc: bool = False) -> tuple:
    """Return the values of given settings.

    An exception is raised if any setting is not set (i.e. its value is None)
    and `exc` is `True`.

    :param keys: Setting keys.
    :param exc: Whether an exception should be raised if any setting is not set
    or not.
    :returns: Settings values.
    """
    sm = get_sm()
    values = [sm.get(k) for k in keys]

    if exc:
        not_set = [v is None for v in values]
        not_set = [keys[i] for i, v in enumerate(not_set) if v]

        c = len(not_set)

        if c > 0:
            s = "s" if c > 1 else ""
            not_set = ", ".join(not_set)
            raise Exception(f"'{not_set}' setting{s} not set")

    return values


def get_db() -> DbManager:
    """Return the database manager.

    :returns: Database manager.
    """
    db_sys, = _get_values((_db_sys_key,), True)

    if db_sys == "mongodb":
        values = _get_values(_mongodb_keys, True)
        db = MongoDbManager(*values)
    elif db_sys == "dynamodb":
        values1 = _get_values(_dynamodb_keys_1)        # Optional settings
        values2 = _get_values(_dynamodb_keys_2, True)  # Required settings

        db = DynamoDbManager(*values1, *values2)
    elif db_sys == "localst":
        path, = _get_values((_localst_path_key,), True)  # JSON file path
        db = LocalStManager(path)
    else:
        raise Exception(f"'{_db_sys_key}' setting invalid")

    return db
