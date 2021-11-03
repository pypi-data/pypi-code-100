# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mbexcelexport2csv']

package_data = \
{'': ['*']}

install_requires = \
['PyQt6>=6.2.1,<7.0.0', 'click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['mbExcelExport2csv = mbExcelExport2csv.main:main']}

setup_kwargs = {
    'name': 'mbexcelexport2csv',
    'version': '0.3.0',
    'description': 'Parses an .xls excel file downloaded from ManageBac and converts to comma-deliminated csv. Particularly useful to convert to GSheets without having to use Excel.',
    'long_description': '# excel2csv\n\nThis simple command line tool can be used to take an `.xls` file (that is actually formatted in xml), and output it as a csv. The main use case in mind here is to convert excel files downloaded from ManageBac and upload them to Google Sheets, without having to open Excel.\n\nThis tool provides the exact same output if the xls file was opened in Excel, copied, and then pasted into Google Sheets, but without requiring Excel.\n\n## Getting Started\n\nRequires Python 3.9 or above. Install Python at python.org. Installing Python also installs a package manager (called pip) that can install the command asc2mb into your command line enviornment.\n\n`pip install excel2csv`\n\nIf for some reason the pip command doesn\'t work, you can manually install it by following the relevant instructions for your system.\n\n### Upgrade\n\nShould you need to update to the latest version, you can do:\n\n`pip install --upgrade excel2csv`\n\n\n## Use\n\nAfter pip install worked, it is now installed on your path, and the command excel2csv is now available:\n\n`excel2csv ~/path/to/xml.xls ~/path/to/output.csv`\n\nYou can then import the csv file into Google Sheets. The delimiter used is a tab.\n\nAlternatively, on Mac, you can skip the step of saving the csv file, and just run the following fancy command line, and it\'ll be on your clipboard.\n\n`excel2csv ~/path/to/xml.xls - | pbcopy`\n\nJust paste into "A1" cell of your Google Sheet.',
    'author': 'Adam Morris',
    'author_email': 'classroomtechtools.ctt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
