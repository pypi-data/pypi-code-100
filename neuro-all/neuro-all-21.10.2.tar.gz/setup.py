# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neuro_all']

package_data = \
{'': ['*']}

install_requires = \
['neuro-cli==21.10.0', 'neuro-extras==21.9.3', 'neuro-flow==21.10.0']

entry_points = \
{'console_scripts': ['docker-credential-neuro = '
                     'neuro_cli.docker_credential_helper:main',
                     'neuro = neuro_cli.main:main',
                     'neuro-extras = neuro_extras:main',
                     'neuro-flow = neuro_flow.cli:main']}

setup_kwargs = {
    'name': 'neuro-all',
    'version': '21.10.2',
    'description': "Combo package for installing all neu.ro command line tools by 'pipx install neuro-all' command",
    'long_description': '# neuro-all\nCombo package for installing all neu.ro command line tools by `pipx install neuro-all` command\n',
    'author': 'Neu.ro Team',
    'author_email': 'team@neu.ro',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://neu.ro',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
