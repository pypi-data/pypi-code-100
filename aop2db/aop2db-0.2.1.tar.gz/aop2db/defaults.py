"""Default paths and variables."""

import logging
import os
from pathlib import Path

from aop2db.constants import AOP_XML_DOWNLOAD

logger = logging.getLogger(__name__)

# Paths
HOME = str(Path.home())
PROJECT_NAME = "aop2db"
BASE_DIR = os.path.join(HOME, f'.{PROJECT_NAME}')

AOP_DIR = os.path.join(BASE_DIR, 'aop')
LOG_DIR = os.path.join(BASE_DIR, 'logs')
DB_PATH = os.path.join(BASE_DIR, f"{PROJECT_NAME}.db")

AOP_XML_FILE = os.path.join(AOP_DIR, os.path.basename(AOP_XML_DOWNLOAD))
TAXONOMY_CACHE = os.path.join(AOP_DIR, "taxonomy_ids.json")

# Make the folders
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(AOP_DIR, exist_ok=True)

# Config file
CONFIG = os.path.join(BASE_DIR, 'config.ini')

# Logging Configuration
LOG_FILE_PATH = os.path.join(LOG_DIR, "aop2db.log")
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
)

# SQL Connection

CONN_STRING = f"sqlite:///{DB_PATH}"
