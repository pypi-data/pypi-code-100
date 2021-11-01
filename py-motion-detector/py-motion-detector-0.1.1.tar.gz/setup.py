# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_motion_detector']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.3,<2.0.0', 'picamera>=1.13,<2.0']

entry_points = \
{'console_scripts': ['py-motion-detector = py_motion_detector.cli:init']}

setup_kwargs = {
    'name': 'py-motion-detector',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'ambauma',
    'author_email': 'andrew_5a+github@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
