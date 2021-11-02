import os
from os.path import expanduser
import requests

try:
    if int(os.environ['ONNC_TESTMODE']):
        api_host = 'http://127.0.0.1:8000'
except KeyError:
    api_host = 'https://api.onnc.skymizer.com'

onnc_key_var = 'ONNC_APIKEY'


api_protocol = 'https'
api_url = "api.onnc.skymizer.com"
api_port = 443