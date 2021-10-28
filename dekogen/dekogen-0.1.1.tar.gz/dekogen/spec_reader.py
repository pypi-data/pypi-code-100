"""Specs related code"""
import urllib.request
import yaml


class SpecReader:
    """Provides ability to read and convert specs"""

    @staticmethod
    def read_yaml(file_path=None, link=None):
        """
        Represent YAML file as python dict
        :param file_path: Local file path
        :param link: Link to spec.yaml data
         Note: Change value of class member 'spec_data'
        """
        if (not file_path and not link) or (file_path and link):
            raise ValueError('Please provide file_path OR link')
        if link:
            response = urllib.request.urlopen(link)
            yaml_data = response.read()
        if file_path:
            with open(file_path, 'r') as spec:
                yaml_data = spec.read()
        return yaml.safe_load(yaml_data)
