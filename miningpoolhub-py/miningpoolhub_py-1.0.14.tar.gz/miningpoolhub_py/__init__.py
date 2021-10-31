import os
from dotenv import load_dotenv
import pkg_resources

load_dotenv()

__version__ = pkg_resources.get_distribution("miningpoolhub_py").version
__author__ = "Cory Krol"

API_KEY = os.environ.get("MPH_API_KEY", None)

from .miningpoolhubapi import MiningPoolHubAPI
