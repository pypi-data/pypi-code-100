"""``Core`` provides common functionality.
"""

import os
import re

from mesiqi.core import get_logger

logger = get_logger()


def clean_column_names(s):
    """A BigQuery column name must contain only letters (a-z, A-Z),
    numbers (0-9), or underscores (_), and it must start with a letter or underscore.
    The maximum column name length is 300 characters.
    A column name cannot use any of the following prefixes: _TABLE_, _FILE_, _PARTITION

    Args:
        s (string): original column name

    Returns:
        string: string which can be used as a BigQuery column name
    """
    res = re.sub(
        "[^a-zA-Z0-9]+",
        "_",
        s.lower()
        .strip()
        .replace("ø", "o")
        .replace("æ", "ae")
        .replace("å", "aa")
        .replace("_TABLE_", "table_")
        .replace("_FILE_", "file_")
        .replace("_PARTITION", "partition_"),
    ).strip()

    if res[0].isdigit():
        res = "_" + res

    return res[0:300]


def get_env(t):
    v = os.environ.get(t)
    if type(v) == str:
        # v = v.replace('"','')
        return v
    else:
        logger.info(f"Environment variable {t} not set")
    return t


def set_env():
    env_local = os.environ.get("ENV_LOCAL", None)
    if env_local:  # use local file for local debugging and testing
        logger.info(f"Set env variables from directory: {env_local}")
        for filename in os.listdir(env_local):
            if filename.endswith(".env"):
                try:
                    with open(f"{env_local}/{filename}") as file:
                        for line in file:
                            if line.startswith("#") or not line.strip():
                                continue
                            name, var = line.strip().split("=", 1)
                            os.environ[name] = var
                except:
                    continue
    else:  # try default path for nais vault secrets
        env_local = "/var/run/secrets/nais.io/vault"
        if os.path.isdir(env_local):
            logger.info(f"Set env variables from directory: {env_local}")
            for filename in os.listdir(env_local):
                logger.info(f"Set env variables from file: {filename}")
                if filename.endswith(".env"):
                    try:
                        with open(f"{env_local}/{filename}") as file:
                            for line in file:
                                if line.startswith("#") or not line.strip():
                                    continue
                                name, var = line.strip().split("=", 1)
                                os.environ[name] = var
                    except:
                        logger.info(f"Could not set env variable from file {filename}")
                        continue
                else:
                    try:
                        with open(f"{env_local}/{filename}") as file:
                            try:
                                var = json.load(file)
                                os.environ[filename] = var
                            except:
                                for line in file:
                                    if line.startswith("#") or not line.strip():
                                        continue
                                    os.environ[filename] = line.strip()
                    except:
                        logger.info(f"Could not set env variable from file {filename}")
                        continue

        else:
            logger.info(f"{env_local} is not directory")
