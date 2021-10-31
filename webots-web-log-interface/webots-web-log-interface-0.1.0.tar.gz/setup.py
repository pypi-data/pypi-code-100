# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webots_web_log_interface']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.3,<4.0.0', 'numpy>=1.21.3,<2.0.0']

setup_kwargs = {
    'name': 'webots-web-log-interface',
    'version': '0.1.0',
    'description': 'A python library used to interact with webots robocup game web logs',
    'long_description': '# Webots Web Log Interface\nA python library used to interact with webots robocup game web logs\n',
    'author': 'Florian Vahl',
    'author_email': 'florian@flova.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bit-bots/webots-web-log-interface',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
