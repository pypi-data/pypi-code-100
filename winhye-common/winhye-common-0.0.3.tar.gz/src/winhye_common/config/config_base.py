import json
import os

__all__ = ["config"]


class Config:
    def __init__(self):
        idc = os.environ.get('IDC')
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        with open(config_path, "r") as f:
            config_all = json.loads(f.read())
        if idc:
            self.config = config_all[idc]
        else:
            self.config = config_all["test"]

    def get_pg_config(self):
        return self.config["pg_config"]

    def get_oss_config(self):
        return self.config["oss_config"]

    def get_mqtt_config(self):
        return self.config["mqtt_config"]

    def get_app_config(self):
        return self.config["app"]

    def get_websocket_config(self):
        return self.config["websocket_config"]

    def get_auth_video_config(self):
        return self.config["auth_video_config"]

    def get_invite_code_overdue_time(self):
        return self.config["invite_code_overdue_time"]

    def get_province_abbreviation(self):
        return self.config["province_abbreviation"]


config = Config()
