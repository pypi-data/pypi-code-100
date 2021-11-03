import json
import os
import stat

import click


class Config:
    @staticmethod
    def create_file():
        config_file = open("config.json", "w+")
        os.chmod("config.json", stat.S_IRWXO)
        return config_file

    @staticmethod
    def get_ssh_credentials():
        if not os.path.exists("config.json"):
            click.echo("Config file does not exist.")
            return
        with open("config.json", "r") as config_file:
            content = json.load(config_file)
        return content["ip"], content["name"], content["password"]
