# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opendiamond', 'opendiamond.console']

package_data = \
{'': ['*']}

install_requires = \
['M2Crypto>=0.21.1', 'click>=8.0.3,<9.0.0', 'python-dateutil>=1.5']

entry_points = \
{'console_scripts': ['cookiecutter = '
                     'opendiamond.console.scope_generate:generate',
                     'diamond-newscope = '
                     'opendiamond.console.scope_import:import_',
                     'opendiamond-scope = opendiamond.console.scope:cli'],
 'opendiamond.cli_plugins': ['scope = opendiamond.console.scope:cli']}

setup_kwargs = {
    'name': 'opendiamond-scope',
    'version': '10.1.5',
    'description': 'OpenDiamond scope manipulation library and tools',
    'long_description': '# OpenDiamond-scope\n\nLibrary and tools for manipulating OpenDiamond search scopes.\n\n\n# To install the latest release from PyPI\n\n    pipx install opendiamond-scope          # or\n    pip install --user opendiamond-scope\n\n\n# Building from source\n\nThe build depends on SWIG and OpenSSL to build the M2Crypto dependency, the\nfollowing command will install this on a Debian/Ubuntu based system.\n\n    sudo apt install swig libssl-dev\n\nFor development, a consistent development environment is managed with poetry.\nIf you are developing locally it is recommended to set up pre-commit git hooks.\n\n    poetry install\n    poetry run pre-commit install   # optional\n\nThe code can then be run from the managed environment.\n\n    poetry run opendiamond-scope -h\n\nRunning of tests and release tagging is done with nox, which should already be\ninstalled in the development environment at this point.\n\n    # run tests against different installed python interpreters\n    poetry run nox\n\n    # release version tagging (and publishing) are handled by a nox script\n    poetry run nox -s release -- [major/minor/patch]\n',
    'author': 'Carnegie Mellon University',
    'author_email': 'diamond@cs.cmu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://diamond.cs.cmu.edu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
