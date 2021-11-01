# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['strigiform',
 'strigiform.alerts',
 'strigiform.app',
 'strigiform.core',
 'strigiform.core.commands',
 'strigiform.data.analyze',
 'strigiform.data.fetch',
 'strigiform.data.import',
 'strigiform.data.load',
 'strigiform.data.storage',
 'strigiform.data.storage.postgres',
 'strigiform.secrets',
 'strigiform.util']

package_data = \
{'': ['*'], 'strigiform.data.storage': ['maria/*', 'redis/*']}

install_requires = \
['SQLAlchemy==1.4.23',
 'botocore>=1.21.29,<2.0.0',
 'click',
 'click-help-colors>=0.9.1,<0.10.0',
 'configparser>=5.0.2,<6.0.0',
 'hvac>=0.11.2,<0.12.0',
 'importlib-metadata<4.9.0',
 'mock>=4.0.3,<5.0.0',
 'nox-poetry>=0.8.6,<0.9.0',
 'pandas-stubs>=1.2.0,<2.0.0',
 'pandas>=1.2.5,<2.0.0',
 'parameterized>=0.8.1,<0.9.0',
 'psycopg2>=2.9.1,<3.0.0',
 'pytest-responsemock[dev]>=1.0.1,<2.0.0',
 'requests-mock',
 'requests==2.26.0',
 'sql>=0.4.0,<0.5.0',
 'streamlit>=1.0.0,<2.0.0',
 'types-requests>=2.25.0,<3.0.0']

entry_points = \
{'console_scripts': ['strigiform = strigiform.core.cli:main']}

setup_kwargs = {
    'name': 'strigiform',
    'version': '0.0.4',
    'description': 'strigiform',
    'long_description': "===============================\nstrigiform\n===============================\n\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/strigiform.svg\n   :target: https://pypi.org/project/strigiform/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/strigiform\n   :target: https://pypi.org/project/strigiform\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/strigiform\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/strigiform/latest.svg?label=Read%20the%20Docs\n   :target: https://strigiform.readthedocs.io/\n   :alt: Read the documentation at https://strigiform.readthedocs.io/\n.. |Tests| image:: https://github.com/X-McKay/strigiform/workflows/Tests/badge.svg\n   :target: https://github.com/X-McKay/strigiform/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/X-McKay/strigiform/branch/develop/graph/badge.svg\n   :target: https://codecov.io/gh/X-McKay/strigiform\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nstrigiform is a Python mono-repo that provides tools for Birders and Researchers to:\n\n* Explore and visualize information for Birders\n* Easily interact with eBird APIs.\n\n\nProject Maturity and readiness\n------------------------------\n\nstrigiform is under active development; many key workflows and best practices are still being worked out.\nMore seamless interaction with eBird products is in development, as well as\ngeneral improvement the overall user experience.\n\n\nA current major focus is visualization of user life-lists across various levels\nof taxonomy and relevant categories.\n\n\nFeatures\n--------\n\n* Retrieval of hotspots (eBird) via CLI and/or python\n* Extracting the latest version of the eBird Taxonomy (species list for data entry and listing purposes across the world)\n\n\n\nRequirements\n------------\n\n`ASDF`_ for managing multiple runtime verisions.\n\n`eBird API Key`_ to dyanamically use and access eBird data.\n\n* Once an API Key has been obtained, store it in an Environment variable named **EBIRD_KEY**\n\n\nInstallation\n------------\n\nYou can install *strigiform* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install strigiform\n\n\nUsage\n-----\n\n* IN PROGRESS\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*strigiform* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\n* Cornell University\n\n* Cornell Lab of Ornithology\n\n* This project was originally based on `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n* Credit to Tim Rodriguez for indirect influence of S&BP.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/X-McKay/strigiform/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://strigiform.readthedocs.io/en/latest/usage.html\n.. _ASDF: http://asdf-vm.com/\n.. _eBird API Key: https://ebird.org/data/download\n",
    'author': 'Alex McKay',
    'author_email': 'aldmckay@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/X-McKay/strigiform',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.9,<4.0.0',
}


setup(**setup_kwargs)
