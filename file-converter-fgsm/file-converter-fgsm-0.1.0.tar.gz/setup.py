# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['file_converter']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['file_converter = '
                     'file_converter.file_converter:file_converter']}

setup_kwargs = {
    'name': 'file-converter-fgsm',
    'version': '0.1.0',
    'description': 'Class project to convert files from CSV to JSON and vice-versa',
    'long_description': None,
    'author': 'Fillipe Goulart',
    'author_email': 'fillipe.gsm@tutanota.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fillipe-gsm/file-converter-puc-ia',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
