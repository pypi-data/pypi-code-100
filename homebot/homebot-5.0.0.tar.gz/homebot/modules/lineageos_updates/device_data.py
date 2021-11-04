import requests
import yaml

DEVICES_DATA_URL = "https://raw.githubusercontent.com/LineageOS/lineage_wiki/master/_data/devices/{device}.yml"
OTA_API_URL = "https://download.lineageos.org/api/v1/{device}/nightly/1"

def get_device_data(device: str):
	yaml_url = DEVICES_DATA_URL.format(device=device)
	response = requests.get(url=yaml_url).text
	return yaml.safe_load(response)

def get_device_updates(device: str):
	api_url = OTA_API_URL.format(device=device)
	return requests.get(url=api_url).json()["response"]
