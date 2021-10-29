import argparse
import yaml
import os

from ascend_deploy.helpers.deployment_class import *
from ascend_deploy.helpers.deploy_functions import *

# Setting up ascend client to connect to ports and creating credentials
#client = client_setup()

def deploy(dataflow_id: str, data_service_id: str, environment: str, path: str) -> None:
    """
    Deploys dataflow to the specified data service
    """

    logging.info(
        f"Deploying dataflow: {dataflow_id} to data service: {data_service_id} on environemnt {environment}"
    )

    # Reading in the dataflow file as a string. This is a file that, when run, deploys
    # the dataflow
    file_location = Path(path).joinpath(f"/{dataflow_id}/{dataflow_id}.py")
    file_string = read_file_as_string(file_location)

    # Updating the file_string by applying the config for the specified data service.
    # The config will alter certain arguments to allow the deployment to push to the
    # specified data service, rather than the one it comes from
    updated_file_string = apply_config_to_string(
        file_string, environment, data_service_id
    )

    # Adding on additional code that runs the deployment function
    updated_file_string += (
        f'\napply_dataflow(client, "{data_service_id}", dataflow_{dataflow_id})'
    )

    # Creating a local variable "transform_folder" which points to the location where the
    # transform files are located. The local variable "client" is also created
    transform_folder = os.path.join(os.getcwd(), dataflow_id)
    exec(updated_file_string, locals())

    print(f"Successfully deployed dataflow: {dataflow_id}")

def main():

    parser = argparse.ArgumentParser(
        description="Downloads a full workflow from Ascend Environment"
    )

    parser.add_argument(
        "-c",
        help="The name of the dataservice which you'd like to download the dataflow from.",
        required=True,
    )

    parser.add_argument(
        "-e",
        help="Environment which you will be running this.",
        required=False,
    )

    parser.add_argument(
        "-s",
        help="The name of the dataservice which you'd like to download the dataflow from.",
        required=True,
    )

    args, remaining = parser.parse_known_args()

    parser.add_argument(
        "-f",
        help="The name of the dataflow which you'd like to download.",
        required=True,
    )

    parser.add_argument(
        "-p",
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

    #build_logging(args.log)

    #deploy(dataflow_id=args.f, data_service_id=args.s, environment=args.e)


    #client = Client(hostname="poal-pilot.ascend.io")

    current_config = Path(os.getcwd()).joinpath(f"{args.f}/config.yaml")
    all_tags_mapping: dict = yaml.safe_load(open(current_config).read())

    dd = dataflow_deployment(args.e, args.c, args.s, args.f, args.p, all_tags_mapping)
    dd.get_dataflow_class()
    dd.apply_functions_on_tags()
    #print(dd.previous_data_service_id)
    dd.create_dataflow()


# Allowing command line arguments to be applied to the download function
if __name__ == "__main__":
    main()
