import json
import logging
import os
from json.decoder import JSONDecodeError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def set_env():
    env_local = os.environ.get("SECRETS_PATH", None)
    if env_local:
        if os.path.isdir(env_local):
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
                        logger.info(f"Could not set env variable from file {filename}")
                        continue
                else:
                    try:
                        with open(f"{env_local}/{filename}") as file:
                            try:
                                content = file.read()
                                var = json.loads(content)
                                if isinstance(var, dict):
                                    os.environ[filename] = json.dumps(var)
                                else:
                                    file.seek(0)
                                    for line in file:
                                        if line.startswith("#") or not line.strip():
                                            continue
                                        os.environ[filename] = line.strip()
                            except:
                                logger.info(
                                    f"Could not set env variable from file {filename}"
                                )
                    except:
                        logger.info(f"Could not open env {filename}")
                        continue

        else:
            logger.info(f"{env_local} is not directory")
    else:
        logger.info(f"Env variable 'SECRETS_PATH' not set")
