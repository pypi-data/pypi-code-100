import requests
import wget
import zipfile
import os
import logging

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


class DownloadDriver:
    def __init__(self):
        ...

    @staticmethod
    def chrome(version, path=None):
        """Downloads Chrome Driver Automatically to Project Directory"""
        # get the latest chrome driver version number
        url = f'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{version}'
        response = requests.get(url)
        version_number = response.text

        # build the download url
        download_url = "https://chromedriver.storage.googleapis.com/" + version_number + "/chromedriver_win32.zip"

        # download the zip file using the url built above
        latest_driver_zip = wget.download(download_url, 'chromedriver.zip')

        # extract the zip file
        with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
            zip_ref.extractall(path)  # you can specify the destination folder path here
        # delete the zip file downloaded above
        os.remove(latest_driver_zip)


class Pylog:
    def __init__(self, file_name):
        self.filename = file_name

    def setup_logger(self, level=logging.INFO):
        """To setup as many loggers as you want"""

        self.handler = logging.FileHandler(self.filename)
        self.handler.setFormatter(formatter)
        logger = logging.getLogger(__name__)
        logger.setLevel(level)
        logger.addHandler(self.handler)

        return logger

    def critical(self, bot_process, process_details):
        """Logs Critical Errors"""
        logger = self.setup_logger()
        logger.critical(f'{bot_process} encountered a critical error while running {process_details}',
                        exc_info=True
                        )
        logger.removeHandler(self.handler)

    def handled_error(self, bot_process, process_details):
        """Logs Handled Errors"""
        logger = self.setup_logger()
        logger.error(f'{bot_process} tried handling an error which occured while running {process_details}'

                     )
        logger.removeHandler(self.handler)

    def simple_warning(self, bot_process, process_details):
        """Logs Warning Messages"""
        logger = self.setup_logger()
        logger.warning(f'{bot_process} successfully handled an error which occured while running {process_details}'

                       )
        logger.removeHandler(self.handler)

    def show_info(self, message_info):
        """Logs and Displays Defined Error Messages"""
        logger = self.setup_logger()
        logger.info(f'{message_info}')
        logger.removeHandler(self.handler)

        return f'{message_info}'
