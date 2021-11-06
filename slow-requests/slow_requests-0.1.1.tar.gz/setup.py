# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slow_requests']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'slow-requests',
    'version': '0.1.1',
    'description': "Many APIs will throttle and potentially ban users for hitting their endpoints to fast or often. Don't get yourself throttled or banned, slow your requests down.",
    'long_description': None,
    'author': 'Logan',
    'author_email': '10239411+Loag@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
