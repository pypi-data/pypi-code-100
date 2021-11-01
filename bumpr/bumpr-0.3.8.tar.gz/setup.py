# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bumpr']

package_data = \
{'': ['*']}

extras_require = \
{'doc': ['mkdocs>=1.2.3,<2.0.0',
         'mkdocs-material>=7.3.5,<8.0.0',
         'mkdocstrings>=0.16.2,<0.17.0',
         'mkdocs-include-markdown-plugin>=3.2.3,<4.0.0']}

entry_points = \
{'console_scripts': ['bumpr = bumpr.__main__:main']}

setup_kwargs = {
    'name': 'bumpr',
    'version': '0.3.8',
    'description': 'Version bumper and Python package releaser',
    'long_description': "# Bump'R: Bump and release versions\n\n[![Build Status](https://github.com/noirbizarre/bumpr/actions/workflows/main.yml/badge.svg?tag=0.3.8)](https://github.com/noirbizarre/bumpr/actions/workflows/main.yml)\n[![codecov](https://codecov.io/gh/noirbizarre/bumpr/branch/master/graph/badge.svg?token=G8u0QBT1Sj)](https://codecov.io/gh/noirbizarre/bumpr)\n[![Documentation Status](https://readthedocs.org/projects/bumpr/badge/?version=0.3.8)](https://bumpr.readthedocs.io/en/0.3.8/?badge=latest)\n![PyPI - Last version](https://img.shields.io/pypi/v/bumpr)\n![PyPI - License](https://img.shields.io/pypi/l/bumpr)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bumpr)\n\nBump'R is a version bumper and releaser allowing in a single command:\n\n- Clean-up release artifact\n- Bump version and tag it\n- Build a source distribution and upload on PyPI\n- Update version for a new development cycle\n\nBump'R intend to be customizable with the following features:\n\n- Optionnal test suite run before bump\n- Customizable with a config file\n- Overridable by command line\n- Extensible with hooks\n\n## Compatibility\n\nBump'R requires Python `>=3.7` (and `<4.0`)\n\n## Installation\n\nYou can install Bump'R with pip:\n\n```console\npip install bumpr\n```\n\n## Usage\n\nYou can use directly the command line to setup every parameter:\n\n```console\nbumpr fake/__init__.py README.rst -M -ps dev\n```\n\nBut Bump'R is designed to work with a configuration file (`bumpr.rc` by defaults).\nSome features are only availables with the configuration file like:\n\n- commit message customization\n- hooks configuration\n- multiline test, clean and publish commands\n\nHere's an exemple:\n\n```ini\n[bumpr]\nfile = fake/__init__.py\nvcs = git\ntests = tox\npublish = python setup.py sdist register upload\nclean =\n    python setup.py clean\n    rm -rf *egg-info build dist\nfiles = README.rst\n\n[bump]\nunsuffix = true\nmessage = Bump version {version}\n\n[prepare]\nsuffix = dev\nmessage = Prepare version {version} for next development cycle\n\n[changelog]\nfile = CHANGELOG.rst\nbump = {version} ({date:%Y-%m-%d})\nprepare = In development\n\n[readthedoc]\nid = fake\n```\n\nThis way you only have to specify which part you want to bump on the\ncommand line:\n\n```console\nbumpr -M  # Bump the major\nbumpr     # Bump the default part aka. patch\n```\n\n## Documentation\n\nThe documentation is hosted on Read the Docs:\n\n- [Stable](https://bumpr.readthedocs.io/en/stable/) [![Stable documentation status](https://readthedocs.org/projects/bumpr/badge/?version=stable)](https://bumpr.readthedocs.io/en/stable/?badge=stable)\n- [Development](https://bumpr.readthedocs.io/en/0.3.8/) [![Latest documentation Status](https://readthedocs.org/projects/bumpr/badge/?version=0.3.8)](https://bumpr.readthedocs.io/en/0.3.8/?badge=latest)\n",
    'author': 'Axel H.',
    'author_email': 'noirbizarre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/noirbizarre/bumpr',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
