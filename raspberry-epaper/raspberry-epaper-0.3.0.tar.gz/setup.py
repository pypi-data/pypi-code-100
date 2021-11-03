# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['raspberry_epaper']

package_data = \
{'': ['*'], 'raspberry_epaper': ['font/*']}

install_requires = \
['Pillow>=8.4.0,<9.0.0',
 'python-box>=5.4.1,<6.0.0',
 'qrcode>=7.3.1,<8.0.0',
 'typer>=0.4.0,<0.5.0',
 'waveshare-epaper>=1.0.3,<2.0.0']

entry_points = \
{'console_scripts': ['epaper = raspberry_epaper.cli:main']}

setup_kwargs = {
    'name': 'raspberry-epaper',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'yskoht',
    'author_email': 'ysk.oht@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
