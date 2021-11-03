# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pollencli', 'pollencli.pyline_removal']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['rm-pyline = pollencli.pyline_removal.cli:main']}

setup_kwargs = {
    'name': 'pollencli-pyline-removal',
    'version': '0.0.4b0',
    'description': 'Remove lines from python file',
    'long_description': '# pollencli-pyline-removal\n\n`rm-pyline <name_id> <src_filepath>` command\n\n```bash\nrm-pyline\n```\n',
    'author': 'pollenjp',
    'author_email': 'polleninjp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pollenjp/pollencli-pyline-removal',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
