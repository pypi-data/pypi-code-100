from yarl import URL


class Urls:
    def __init__(self):
        self.protocol = "http://"
        self.base_url = "ethosdistro.com/"
        self.panel_id = "{panel_id}."
        self.no_pool_base_url = self.protocol + self.base_url

        self.json_query_param = {"json": "yes"}

        # Panel only URLs
        self.get_panel = self.protocol + self.panel_id + self.base_url

    def base_url(self) -> str:
        return self.base_url

    def get_panel_url(self, panel_id: str) -> URL:
        return URL(self.get_panel.format(panel_id=panel_id)) % self.json_query_param
