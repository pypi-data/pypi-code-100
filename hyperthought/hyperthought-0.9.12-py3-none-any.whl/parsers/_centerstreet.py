"""
Parser is intended to parse design of experiments and GCode files created by
Center Street from various AM experiments.
"""

import os
import re
import xml.etree.ElementTree as ET

from .base import BaseParser
from ..metadata import MetadataItem


class CenterStreet(BaseParser):
    """
    Parser intended to be applied to all CenterStreet documents.

    Currently parser will handle mpf and dpdx files.
    """

    VALID_EXTENSIONS = {'mpf', 'dxpx'}

    def format_string(self, _input):

        """
        Formats a given input by converting to string and eliminating
        new line characters and starting or trailing whitespaces.

        Parameters
        ----------
        format_input (string): input to be formatted
        """

        new_string = str(_input).replace('\n', ' ').strip()
        new_string = re.sub(r'\s+', ' ', new_string)

        return new_string

    def gcode_parser(self):
        """
        Parser designed to parse out key data items from a GCode file.
        Returns list of metadata items constructed from parsed data.

        Parameters
        ----------
        """
        # Add GCode structure validation
        valid_lines = []
        start_line_index = -1
        end_line_index = -1

        # Items that have units that need to be apart of the value
        skip_units = [
            'Extruder 1 Material used',
            'Extruder 1 Material name',
            'Version of Fusion'
        ]

        metadata_items = []

        metadata_items.append(
            MetadataItem(
                key='File Name',
                value=os.path.splitext(self.file_path.split('\\')[-1])[0]
            )
        )

        with open(self.file_path) as f:
            lines = f.readlines()

        for index, line in enumerate(lines):
            if line[0] == ';' and start_line_index == -1:
                start_line_index = index
                valid_lines.append(line)
                continue
            if line[0] == ';' and end_line_index == -1:
                valid_lines.append(line)

            if line[0] != ';' and end_line_index == -1:
                end_line_index = index
                break

        for line in valid_lines:
            line_elements = line.split(":", 1)

            if len(line_elements) == 1:
                continue

            key = self.format_string(line_elements[0]).strip(';')
            value = self.format_string(line_elements[1])

            # Validate this is what we want to look up
            # Currently works but will need a better solution.
            unit_match = re.search('\d+(in)', value)

            if (unit_match and key not in skip_units):
                value = re.sub('in', '', value)
                unit = unit_match.group(1)
            else:
                unit = ''

            if key and value:
                metadata_items.append(
                    MetadataItem(
                        key=key,
                        value=value,
                        units=unit
                    )
                )

        return metadata_items

    def doe_parser(self):
        """
        Parser designed to parse out key data items from a DOE file.
        Returns list of metadata items constructed from parsed data.

        Parameters
        ----------
        """
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        headers = {}
        header_items = []
        metadata_items = []

        header_items.extend(
            [
                item
                for factor in root.findall('factorInfo')
                for item in factor
            ]
        )

        header_items.extend(
            [
                item
                for response in root.findall('responseInfo')
                for item in response
            ]
        )

        headers = {
            header.attrib['id'] : {
                'name': header.attrib['name'],
                'unit': header.attrib['unit']
            }
            for header in header_items
        }

        for index, item in enumerate(root.findall('run')):
            for child in item:
                metadata_items.append(
                    MetadataItem(
                        key=headers[child.attrib['id']]['name'],
                        value=child.text,
                        units=headers[child.attrib['id']]['unit'],
                        annotation='Run Index: '+str(index)
                    )
                )

        return metadata_items

    def parse(self):
        """
        Parse file based on file extension.
        """
        file_extension = os.path.splitext(self.file_path)[1].lstrip('.').lower()

        if file_extension == 'mpf':
            self.metadata = self.gcode_parser()
        elif file_extension == "dxpx":
            self.metadata = self.doe_parser()
        else:
            # This shouldn't happen.
            raise ValueError(
                f"{self.file_path} does not have a valid extension.  "
                f"Extension must be one of {self.VALID_EXTENSIONS}."
            )
