import click
import os
import yaml
import time
import schedule
import sys
import json
import inp as inp

@click.command()
@click.argument("config_path", default='', required=False)
def main(config_path):

    config = {}
    try:
        print(config_path)
        # if os.path.isfile("config.yaml"):
        with open(config_path) as file:
            config = yaml.load(file)
                # logger.info(config)
        bufferPath = "bufferdata.json"
        if "/" in config_path:
            bufferPath = "/".join(config_path.split("/")[:-1]) + "/bufferdata.json"
        if os.path.exists(bufferPath):
            with open(bufferPath, "r") as f:
                try:
                    prev_data = json.load(f)
                except ValueError:
                    prev_data = {}

            with open(bufferPath, "w") as fl:
                # json.dumps(datalogs , fl)
                json.dump(prev_data, fl)
        else:

            with open(bufferPath, "w") as fl:
                json.dump({},fl)

        inp.work(config, bufferPath)

    except Exception as exception:

        print("error in opening config.yaml", str(exception))

