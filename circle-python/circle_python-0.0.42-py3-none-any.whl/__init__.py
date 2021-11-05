__version__ = "0.0.42"  # Do not update directly, use bumpversion

api_key = None
default_http_client = None
proxy_url = None
api_base = (
    "https://api-sandbox.circle.com"  # override with "https://api.circle.com in prod
)

max_network_retries = 0

from circle.resources import *
