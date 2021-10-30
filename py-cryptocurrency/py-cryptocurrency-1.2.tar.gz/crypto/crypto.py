from requests import get
from base64 import b64decode as decode

class crypto():
 def __init__(self):
     self.key = decode("NzAyOWRmODNjOGRkNDFlNjFmYWE2ZDYxZDg4NDZkMDU=".encode())
     print("v1.2")
 def get_price(self, ids=None, currency="usd"):
     r = get("http://api.coinlayer.com/live", params={"access_key": self.key}).json()
     if ids.upper() == "BTC":
        print("v3")
        return r["rates"]["BTC"]
     if ids and r["rates"].get(ids.upper()):
        return {ids.upper(): r["rates"].get(ids.upper())}
     return r
     
