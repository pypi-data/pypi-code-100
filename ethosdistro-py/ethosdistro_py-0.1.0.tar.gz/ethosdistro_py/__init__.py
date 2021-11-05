import os
from dotenv import load_dotenv
import pkg_resources

load_dotenv()

__version__ = pkg_resources.get_distribution("ethosdistro_py").version
__author__ = "Cory Krol"

PANEL_ID = os.environ.get("ETHOS_PANEL_ID", None)

from .ethosdistroapi import EthosAPI
