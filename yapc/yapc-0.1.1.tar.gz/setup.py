# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yapc']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=1.26.0,<2.0.0', 'click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['pdf_tool = yapc.__main__:cli']}

setup_kwargs = {
    'name': 'yapc',
    'version': '0.1.1',
    'description': 'Yet Another PDF CLI',
    'long_description': '# yapc - Yet Anothet PDF CLI\n\nYet another CLI tool for interacting with PDFs files.\n',
    'author': 'Atahan Yorgancı',
    'author_email': 'atahanyorganci@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/atahanyorganci/yapc.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
