import requests
from .error import *

class cb0t:
    def __init__(self, url:str):
        self.r = requests.post("https://cb0t.cc/api/create", data = {"url": url})
        if self.r.status_code == 400:
            raise Invalidurl("Invalid url specified.")
        elif self.r.status_code == 406:
            raise Invalidurl("Sorry but the specified domain is on our blacklist.")

    @property
    def url(self):
        return self.r.json()["url"]
