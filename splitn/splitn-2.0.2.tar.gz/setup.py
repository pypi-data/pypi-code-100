# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splitn']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0',
 'rstr>=3.0.0,<4.0.0',
 'sequences',
 'split',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['splitn = splitn.main:app']}

setup_kwargs = {
    'name': 'splitn',
    'version': '2.0.2',
    'description': '',
    'long_description': '`splitn` is a CLI app that generates combinations of chars being a result of splitting strings provided *explicite* or randomly generated from regex patterns. It is made mainly for testing NLU applications, e.g. voicebots, chatbots or tools for extracting structural data from text like [duckling](https://github.com/facebook/duckling).\n\n# Installation\n```\npipx install splitn\n```\n\nor\n\n```\npip install splitn\n```\n\n# Examples\n## Basic usage\n```bash\nsplitn 486\n\n# result\n486\n48 6\n4 86\n4 8 6\n```\n',
    'author': 'Michał Warzocha',
    'author_email': 'warzocha.michal@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
