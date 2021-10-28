from alfa_sdk.common.base import BaseClient


class CacheClient(BaseClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.session.set_default({
            "service": "core",
            "prefix": "/api/caches",
        })

    def store_value(self, key, value, ttl=3600):
        body = {"key": key, "value": value, "ttl": ttl}
        return self.session.request("post", path="/{}".format(key), json=body)

    def fetch_value(self, key):
        return self.session.request("get", path="/{}".format(key))
