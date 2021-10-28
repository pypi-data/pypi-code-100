from alfa_sdk.common.base import BaseClient


class SecretsClient(BaseClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.session.set_default({
            "service": "core",
            "prefix": "/api/secrets"
        })

    def list_names(self):
        params = {"teamId": self.team_id}
        return self.session.request("get", path="/list", params=params)

    def fetch_value(self, name):
        params = {"name": name, "teamId": self.team_id}
        return self.session.request("get", path="/", params=params)

    def fetch_values(self, names):
        body = {"names": names, "teamId": self.team_id}
        return self.session.request("post", path="/batch", json=body)

    def store_value(self, name, value, *, description=None):
        body = {"name": name, "value": value, "description": description, "teamId": self.team_id}
        return self.session.request("post", path="/", json=body)

    def remove_value(self, name):
        body = {"name": name, "teamId": self.team_id}
        return self.session.request("post", path="/remove", json=body)
