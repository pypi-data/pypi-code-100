# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sp110e']

package_data = \
{'': ['*']}

install_requires = \
['bleak==0.13.0', 'syncer==1.3.0']

setup_kwargs = {
    'name': 'sp110e',
    'version': '0.1.0',
    'description': 'Control SP110E BLE RGB LED device from computer',
    'long_description': None,
    'author': 'Pavel Roslovets',
    'author_email': 'p.v.roslovets@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
