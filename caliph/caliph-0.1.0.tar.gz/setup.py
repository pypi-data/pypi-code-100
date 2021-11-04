# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['caliph']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.4.0,<0.5.0', 'numpy>=1.21.3,<2.0.0']

entry_points = \
{'console_scripts': ['calibrate = caliph:calib', 'convert = caliph:conv']}

setup_kwargs = {
    'name': 'caliph',
    'version': '0.1.0',
    'description': 'A simple tool to calibrate and convert pH measurements using a two point method.',
    'long_description': None,
    'author': 'Peter Dunne',
    'author_email': 'peter.dunne@applied-magnetism.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
