import requests
from blackduck_c_cpp.util.hub_api import HubAPI
from google.cloud import storage
import os
from google.oauth2 import service_account
import hashlib
import time
print("here1")
hub_api = HubAPI(bd_url="https://prd-kb-dev-match02.dc2.lan",api_token="OGJlNWU1ZTktNjQ2MC00NDYzLTkxNWUtZDAwOWRhYjhhNzE4OmJlOWU5OGMwLWI2ZjQtNGYwZi1iYTA1LTA2ZDM4NTc2NDRkMQ==",insecure=True)
print("here2")
hub_api.authenticate()
print("here3")

hub = hub_api.hub
headers = hub.get_headers()
response = requests.post('{}/api/tool-token'.format("https://prd-kb-dev-match02.dc2.lan"),
                         headers=headers,
                         verify=False)
resp = response.json()
print(resp)
print(resp['jsonWebToken'])
print(resp)
pkg_mgr = 'macos'
str_output= resp['checksum'][pkg_mgr]
checksum,path = str_output.split(",")
print(checksum)
print(path)
list_gc = path.split("/")
file_name = list_gc[-1]
bucket_name = list_gc[-2]
print(file_name)
print(bucket_name)

sha1_res = hashlib.sha256(open('/Users/kakarlas/Desktop/cov-latest.zip','rb').read()).hexdigest()
print(sha1_res)

if checksum == sha1_res:
    print("yayy")
else:
    print("Something went wrong")
    time.sleep(10)
    storage_credentials = service_account.Credentials.from_service_account_info(resp['jsonWebToken'])
    client = storage.Client(credentials=storage_credentials)
    bucket = client.bucket("blackduck-tools")
    blob = bucket.blob("cov-bd-capture-macosx-2021.9.1.zip")
    blob.download_to_filename("/Users/kakarlas/Desktop/cov-latest.zip")
    print("downloaded")
