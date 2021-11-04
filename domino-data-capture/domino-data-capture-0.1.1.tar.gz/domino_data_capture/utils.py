import logging
import os

from domino_data_capture.exception import RecordInvalidException


def get_model_version():
    host_name = os.getenv("HOSTNAME")
    return host_name.split("-")[1] if host_name is not None and host_name.startswith("model") else None


def handle_error(is_dev_mode, message):
    if is_dev_mode:
        raise RecordInvalidException(message)
    else:
        logging.error(message)


def get_scrape_location():
    host_name = os.getenv("HOSTNAME")
    scrape_directory = os.getenv("PREDICTION_DATA_DIRECTORY")

    if host_name and scrape_directory:
        if scrape_directory.endswith('/'):
            scrape_directory = scrape_directory[:-1]
        return scrape_directory + "/" + host_name + ".log"
    else:
        return "/tmp/dummy.log"
