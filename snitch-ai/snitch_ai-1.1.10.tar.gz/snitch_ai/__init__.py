import os

__version__ = "1.1.10"

cloud_endpoint = "https://api.snit.ch/"
endpoint_address = os.getenv("SNITCH_ENDPOINT_ADDRESS", cloud_endpoint)
access_token = os.getenv("SNITCH_ACCESS_TOKEN")

from snitch_ai.internal.project import create_project, get_project, select_project
