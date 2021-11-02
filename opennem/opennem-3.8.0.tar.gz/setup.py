# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opennem',
 'opennem.core',
 'opennem.schema',
 'opennem.settings',
 'opennem.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'click>=7.1.2,<8.0.0',
 'pydantic>=1.5.1,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'requests>=2.25.1,<3.0.0',
 'requests_cache>=0.5.2,<0.6.0',
 'tomlkit>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['opennem = opennem.cli:main']}

setup_kwargs = {
    'name': 'opennem',
    'version': '3.8.0',
    'description': 'OpenNEM Australian Energy Data Python Client',
    'long_description': "# OpenNEM Energy Market Data Access\n\n![PyPI](https://img.shields.io/pypi/v/opennem) ![Tests](https://github.com/opennem/opennempy/workflows/Tests/badge.svg) ![PyPI - License](https://img.shields.io/pypi/l/opennem)\n\nThe OpenNEM project aims to make the wealth of public National Electricity Market (NEM) data more accessible to a wider audience.\n\nThis client library for Python enables accessing the Opennem API and data sets.\n\nProject homepage at https://opennem.org.au\n\nDeveloper documentation at https://developers.opennem.org.au/\n\nCurrently supporting the following energy networks:\n\n- Australia NEM: https://www.nemweb.com.au/\n- Australia WEM (West Australia): http://data.wa.aemo.com.au/\n- APVI rooftop solar data for Australia\n\n## 1. Requirements\n\n- Python 3.8+ (see `.python-version` with `pyenv`)\n- Docker and `docker-compose` if you want to run the local dev stack\n\n## 2. Quickstart\n\n```sh\n$ pip install opennem\n```\n\n```\n>>> import opennem\n```\n\n## 3. Development\n\n### 3.1 Auto setup and install\n\nFor contributions and development of this repository you need to install all the requirements. There\nare some helper scripts in the `scripts/` folder.\n\n```sh\n$ ./scripts/init.sh\n```\n\nBy default the venv is installed in the user local cache folder and not in the project path. To link the venv\nso that it can be found automatically by the shell or editors run the helper script\n\n```sh\n$ ./scripts/link_venv.sh\nCreated .venv\n```\n\n### 3.2 Manual Setup\n\n#### 3.2.1 Prerequisites\n\nFor MacOS and Linux require `pyenv` and `poetry`\n\n * [pyenv homepage](https://github.com/pyenv/pyenv#installation) - simple install with `brew install pyenv`\n * [poetry install](https://python-poetry.org/docs/) (don't install poetry with brew - see [this issue](https://github.com/python-poetry/poetry/issues/36))\n\n#### 3.2.2 Initialize python\n\nWe use `pyenv` for python versioning as it allows a system to run multiple version of python. The version for this project is specified in the `.python-version` file in the root of the repository.\n\nTo install the locally required python version\n\n```sh\n$ pyenv install `cat .python-version`\n```\n\nTo initialize and use the local python version\n\n```sh\n$ pyenv version local\n3.9.6 (set by /Users/user/Projects/Opennem/opennempy/.python-version)\n```\n\nTo test the install is correct\n\n```sh\n❯ python -V\nPython 3.9.6\n❯ which python\n/Users/n/.pyenv/shims/python\n```\n\n#### 3.2.3 Install with poetry\n\nTo manually setup the local development environment, simply create the virtual environment, link it and setup\nthe PYTHONPATH\n\n```sh\n$ poetry install\n$ ln -s `poetry env info -p` .venv\n$ source .venv/bin/activate\n$ pwd > .venv/lib/python3.9/site-packages/local.pth\n```\n\nAlternatively to actiavate the virtual environment `poetry` has a shell command:\n\n```sh\n$ poetry shell\nSpawning shell within /Users/n/Library/Caches/pypoetry/virtualenvs/opennem-pFt2SfpM-py3.9\n$ which python\n/Users/n/Library/Caches/pypoetry/virtualenvs/opennem-pFt2SfpM-py3.9/bin/python\n```\n\n#### 3.2.4 Install with venv\n\nAlternatively if you do not wish to use `poetry` you can setup a simple venv in the local folder and activate it.\n\n```sh\n$ python -m venv .venv\n$ source .venv/bin/activate\n$ pip install -r requirements.txt\n```\n\n### 3.3 Test Install\n\nYou should be able to run a Python REPL (like `iPython`) and import the `opennem` module\n\n```sh\n$ ipython\nPython 3.9.6 (default, Jun 28 2021, 19:24:41)\nType 'copyright', 'credits' or 'license' for more information\nIPython 7.23.0 -- An enhanced Interactive Python. Type '?' for help.\n\nIn [1]: import opennem\n\nIn [2]:\n```\n",
    'author': 'Nik Cubrilovic',
    'author_email': 'nik@infotorch.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://developers.opennem.org.au',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
