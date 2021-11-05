# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['adacord', 'adacord.cli']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['adacord = adacord.cli.main:app']}

setup_kwargs = {
    'name': 'adacord',
    'version': '0.1.9',
    'description': 'The cli and sdk for adacord.com',
    'long_description': '# Adacord CLI\n\n\n## Installation\n\n```bash\npip install adacord\n```\n\n## Usage\n\n### Create a new user\n\n```bash\nadacord user create\n```\n\n### Login\n\n```bash\nadacord user login --email me@my-email.com --password your-password\n```\n\n### Create endpoint\n\n```bash\nadacord bucket create --description "A fancy bucket"\n```\n\n### List endpoints\n\n```bash\nadacord bucket list\n```\n\n### Query endpoint\n\n```bash\nadacord bucket query my-bucket --query \'select * from my-bucket\'\n```\n\n# Contributing\n\n```bash\npoetry install\n```\n',
    'author': 'Christian Barra',
    'author_email': 'me@christianbarra.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.adacord.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
