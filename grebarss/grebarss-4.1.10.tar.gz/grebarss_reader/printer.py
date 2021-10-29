"""Storage module for classes Printer"""

import json
import logging

logger = logging.getLogger('app.printer')


class Printer:
    """Class for printing info"""

    @staticmethod
    def print_info(data_to_print: dict):
        """
        Print info in stdout
        :param data_to_print: data for printing
        """

        for item in data_to_print['item']:
            print('\n', "- " * 20, '\n')
            print(f'Title: {item.get("title")}\nData: {item.get("pubDate")}\nLink: {item.get("link")}\n'
                  f'Image: {item.get("image")}')
            if item.get('source'):
                print(f'Source: {item.get("source")}')

    @staticmethod
    def print_info_json(data_to_print: dict):
        """
        Print info in json format
        :param data_to_print: data for printing
        """

        for item in data_to_print['item']:
            item_in_json = json.dumps(item, ensure_ascii=False).encode('utf8')
            print('\n', "- " * 20, '\n')
            print(item_in_json.decode())
