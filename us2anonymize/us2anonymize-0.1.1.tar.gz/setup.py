# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['us2anonymize']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.3,<2.0.0',
 'opencv-python<4.5.4',
 'pydicom>=2.2.2,<3.0.0',
 'python-gdcm>=3.0.10,<4.0.0',
 'watchdog>=2.1.6,<3.0.0']

entry_points = \
{'console_scripts': ['anonymize = us2anonymize.anonymize:main']}

setup_kwargs = {
    'name': 'us2anonymize',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'mathias',
    'author_email': 'mathias@us2.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.5,<3.11',
}


setup(**setup_kwargs)
