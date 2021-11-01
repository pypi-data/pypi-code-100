import requests
import json
from .exceptions import InvalidPlayerNameError

MOJANG_API = "https://api.mojang.com"

def get_uuid(name):
	response = requests.get(f"{MOJANG_API}/users/profiles/minecraft/{name}")
	json = response.json()
	try:
		return json["id"]
	except json.decoder.JSONDecodeError:
		raise InvalidPlayerNameError
		