"""Simple class with custom methods and auto-close"""

import os

NEW_LINE = os.linesep


class FileWriter:
    """Simple helpers for code writing"""

    def __init__(self, file_path):
        """
        :param file_path: path to result file.
         Will be created if exists otherwise overwritten
        """
        self.file_path = file_path
        self.file = open(file_path, 'w+')

    def add_empty_lines(self, count=1):
        """
        :param count: Count of empty lines to add
        """
        self.file.write(NEW_LINE * count)

    def __del__(self):
        """Close file during object removing"""
        self.file.close()
