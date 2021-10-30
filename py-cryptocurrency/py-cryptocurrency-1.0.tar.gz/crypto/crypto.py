from requests import get
from base64 import b64decode as decode

class crypto():
 def __init__(self):
     self.key = decode("NzAyOWRmODNjOGRkNDFlNjFmYWE2ZDYxZDg4NDZkMDU=".encode())
 def get_price(self, ids="btc", currency="usd"):
     r = get("http://api.coinlayer.com/live", params={"access_key": self.key}).json()
     return r
     
