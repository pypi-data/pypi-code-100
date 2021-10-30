import hashlib

from fedeproxy.interfaces import dvcs


class DVCS(dvcs.DVCS):
    def url_hashed(self, url):
        return "B" + hashlib.sha256(url.encode("ascii")).hexdigest()
