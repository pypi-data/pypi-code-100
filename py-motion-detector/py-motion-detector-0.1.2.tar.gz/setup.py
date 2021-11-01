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
    'version': '0.1.2',
    'description': 'A python based motion detection application for the raspberry pi.',
    'long_description': '==================\npy-motion-detector\n==================\n\nA python based motion detection application for the raspberry pi.  Current version must be ran on a raspberry pi since it relies on the ``picamera`` software.\n\nUsage\n-----\n\nTo start the application::\n\n    py-motion-detector\n\nHit Ctrl-C to exit or use ``kill <pid>``.\n',
    'author': 'ambauma',
    'author_email': 'ambauma@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ambauma/pi-motion-detector/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
