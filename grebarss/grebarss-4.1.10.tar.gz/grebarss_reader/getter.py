"""Storage module for class GetterXML"""

import requests
import logging

logger = logging.getLogger('app.getter')


class GetterXml:
    """Class for receiving response with xml from the server"""

    def __init__(self):
        self.response = None
        self.url = None

    def get_response(self, url: str):
        """
        Get response and check status.
        :param url: source url for request
        :return: response
        """
        self.url = url

        logger.info(f'Make request to URL - {self.url}')

        try:
            self.response = requests.get(self.url)
            logger.debug(self.response)
        except ConnectionError as err:
            logger.error(err)

        if self.response.ok:
            if GetterXml._is_response_status_200(self.response):
                logger.info(f'Status response is good')
                return self.response
            else:
                logger.warning(f'Current status code response is {self.response.status_code}')
                return self.response

    @staticmethod
    def _is_response_status_200(resp) -> bool:
        """
        Check is status code 200
        :param resp: response object
        :return: bool
        """
        if resp.status_code == 200:
            return True
        return False
