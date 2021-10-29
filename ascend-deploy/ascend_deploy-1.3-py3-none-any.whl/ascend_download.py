import argparse
import yaml
import os
import configparser
from typing import List

from ascend.sdk.render import download_dataflow
from ascend_deploy.helpers.deploy_functions import *
from ascend_deploy.helpers.config import config_yaml

# Function to copy yaml from package and add credential
def create_yaml(dataflow_id: str, path: str) -> None:

#    current_folder = os.path.dirname(os.path.realpath(__file__))
#    file_location = os.path.join(current_folder, "config.yaml")
    all_tags_mapping: dict = yaml.safe_load(config_yaml)

    config = configparser.ConfigParser()
    config.read(os.path.expanduser("~/.ascend/credentials"))

    all_tags_mapping['credentials'] = {section_name: dict(config[section_name]) for section_name in config.sections()}
    directory = Path(path).joinpath(f"{dataflow_id}/")
    if not os.path.isdir(directory):
        os.mkdir(directory)
        with open(directory.joinpath('config.yaml'), 'w') as file:
            documents = yaml.dump(all_tags_mapping, file)

# Function to download dataflow for a specific data service
def download(dataflow_id: str, data_service_id: str, path: str) -> None:
    """
    Given a data service and dataflows, download the dataflows
    """
    # Splitting the dataflow_id into multiple dataflows
    dataflows: List[str] = dataflow_id.split(",")

    for dataflow in dataflows:

        # Setting up directory. If the directory does not exist, create it
        directory = Path(path).joinpath(f"{dataflow}/")

        if not os.path.isdir(directory):
            print(f"Directory does not exist, creating directory: {directory}")
            os.mkdir(directory)

        # Downloading dataflow
        download_dataflow(
            client,
            data_service_id=data_service_id,
            dataflow_id=dataflow,
            resource_base_path=directory
        )

        print(f"Successfully downloaded dataflow {dataflow}")

def main():

    global client

    parser = argparse.ArgumentParser(
        description="Downloads a full workflow from Ascend Environment"
    )

    parser.add_argument(
        "-c",
        help="The name of the instance which you'd like to download the artifacts from.",
        required=True,
    )

    args, remaining = parser.parse_known_args()

    # Setting up ascend client to connect to ports and creating credentials
    client = client_setup(args.c)

    parser.add_argument(
        "-s",
        help="The name of the dataservice which you'd like to download the dataflow from.",
        choices=[ds.name for ds in client.list_data_services().data],
        required=True,
    )

    args, remaining = parser.parse_known_args()

    parser.add_argument(
        "-f",
        help="The name of the dataflow which you'd like to download.",
        choices=[ds.name for ds in client.list_dataflows(args.s).data],
        required=True,
    )

    parser.add_argument(
        "-p",
        help="The location where you would like to save this dataflow. If none given, will save on this directory.",
        required=False,
        default=".",
    )

    parser.add_argument(
        "-log",
        help="The log level, defaults to INFO.",
        required=False,
        default="INFO",
        type=str.upper,
    )

    args = parser.parse_args()

    build_logging(args.log)

    # create default yaml template for deployment
    create_yaml(args.f, args.p)

    # download(dataflow_id=args.f, data_service_id=args.s, path=args.p)
    download(args.f, args.s, args.p)



# Allowing command line arguments to be applied to the download function
if __name__ == "__main__":
    main()
