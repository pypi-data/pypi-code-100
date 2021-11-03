# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mb_excelexport_2csv']

package_data = \
{'': ['*']}

install_requires = \
['PyQt6>=6.2.1,<7.0.0', 'click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['mb_excelexport_2csv = mb_excelexport_2csv.main:main']}

setup_kwargs = {
    'name': 'mb-excelexport-2csv',
    'version': '0.6.0',
    'description': 'Parses an .xls excel file downloaded from ManageBac and converts to comma-deliminated csv. Particularly useful to convert to GSheets without having to use Excel.',
    'long_description': '# mb-excelexport-2csv\n\nThis simple command line tool can be used to take an `.xls` file (that is actually formatted in xml), and output it as a csv. The main use case in mind here is to convert excel files downloaded from ManageBac and upload them to Google Sheets, without having to open Excel.\n\nThis tool provides the exact same output if the xls file was opened in Excel, copied, and then pasted into Google Sheets, but without requiring Excel.\n\n## Getting Started\n\nRequires Python 3.6.1 or above. Install Python 3 at python.org. Installing Python also installs a package manager (called pip) that can install the command `mb_excelexport_2csv` into your command line environment.\n\n`pip3 install mb_excelexport_2csv`\n\nThen, open the mini app using this command:\n\n`mb_excelexport_2csv gui`\n\nFor those who want the command line, use: \n\n`mb_excelexport_2csv cmd`\n\nSee "Command Line" below for more info\n\n### Upgrade\n\nShould you need to update to the latest version, you can do:\n\n`pip install --upgrade mb_excelexport_2csv`\n\n\n## Command Line\n\nAfter pip install worked, it is now installed on your path, and the command mb_excelexport_2csv is now available:\n\n`mb_excelexport_2csv cmd ~/path/to/xml.xls ~/path/to/output.csv`\n\nYou can then import the csv file into Google Sheets. The delimiter used is a comma.\n\nAlternatively, on Mac, you can skip the step of saving the csv file, and just run the following fancy command line, and it\'ll be on your clipboard.\n\n`mb_excelexport_2csv cmd ~/path/to/xml.xls - | pbcopy`\n\nJust paste into "A1" cell of your Google Sheet, Data -> Split Text into Columns.',
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
