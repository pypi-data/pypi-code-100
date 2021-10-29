# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['calibrade']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.3,<4.0.0',
 'numpy>=1.21.3,<2.0.0',
 'opencv-python>=4.5.4,<5.0.0']

setup_kwargs = {
    'name': 'calibrade',
    'version': '0.1.1',
    'description': 'A toolbox for end-to-end camera calibration with minimal pain.',
    'long_description': None,
    'author': 'Aarrushi Shandilya',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
