# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vktoken', 'vktoken.cli']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['vktoken = vktoken.__main__:main']}

setup_kwargs = {
    'name': 'vktoken',
    'version': '2.1.0',
    'description': 'Tool for getting VK access token',
    'long_description': '# vktoken\nTool for getting VK access token.\n[![preview](https://asciinema.org/a/nnP04X2a4jlKzCBIKHaN0HDVY.svg)](https://asciinema.org/a/nnP04X2a4jlKzCBIKHaN0HDVY)\n\n## Installation\n`pip install --user vktoken`\n\n## Usage\n`vktoken [--help] [--version] [--app] [--client-id] [--client-secret] login [password]`\n\n## Examples\n* `vktoken +79652331167`  \n* `vktoken --app iphone +79523311167 mypassword`\n* `vktoken --client-id 3140623 --client-secret VeWdmVclDCtn6ihuP1nt +79523311167`\n\n## Features\n* You can choose builtin VK app credentials from the list: `android`, `iphone`, `ipad` and `windows-phone`.\n',
    'author': 'jieggii',
    'author_email': 'jieggii.contact@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jieggii/vktoken',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
