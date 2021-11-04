# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_csv_json_converter']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'pandas>=1.3.4,<2.0.0']

entry_points = \
{'console_scripts': ['csv_converter = '
                     'python_csv_json_converter.converter:converter']}

setup_kwargs = {
    'name': 'python-csv-json-converter',
    'version': '0.1.4',
    'description': 'Convert csv to Json. For learning purposes',
    'long_description': '**CSV TO JSON in Python\n\nProject is written in Python to read a CSV file and export a JSON file. All options to conversion are passed by prompt commands options.\nThis project makes part of the course Artificial Intelligence, specifically the discipline "Python for data science"\n',
    'author': 'Felipe França',
    'author_email': 'felipejonataoliveira@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
