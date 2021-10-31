# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['miningpoolhub_py']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'python-dotenv>=0.19.1,<0.20.0', 'yarl>=1.6.3,<2.0.0']

extras_require = \
{'docs': ['Sphinx>=4.2.0,<5.0.0',
          'sphinx-rtd-theme>=1.0.0,<2.0.0',
          'sphinxcontrib-napoleon>=0.7,<0.8']}

setup_kwargs = {
    'name': 'miningpoolhub-py',
    'version': '1.0.14',
    'description': 'An async Python wrapper for the Mining Pool Hub REST API',
    'long_description': "\nminingpoolhub_py\n----------------\n.. image:: https://github.com/CoryKrol/miningpoolhub_py/workflows/CI/badge.svg?branch=master\n     :target: https://github.com/CoryKrol/miningpoolhub_py/actions?workflow=CI\n     :alt: CI Status\n\nA Python wrapper for the Mining Pool Hub REST API\n\nInstallation\n------------\nInstall with pip:\n\n.. code-block:: bash\n\n   pip install miningpoolhub_py\n\nUsage\n------------\n\nUniversal Endpoints\n-------------------\nMining Pool Hub supports auto switching between coins. Obtain statistics for all coins with the following methods\n\n.. code-block:: python\n\n   from miningpoolhub_py import Pool\n\n   pool_instance = Pool('ethereum')\n   pool_instance.get_all_user_balances()\n   pool_instance.get_auto_switching_and_profits_statistics()\n   pool_instance.get_mining_profit_and_statistics()\n\n\nPool Selection\n-------------------\nMining Pool Hub has different base urls for each coin they offer. Create a new pool object for every coin you are\ninterested in mining statistics for\n\n.. code-block:: python\n\n   from miningpoolhub_py import Pool\n   pool_instance = Pool('ethereum')\n   pool_instance.get_dashboard()\n\nAuthentication\n-------------------\n\nEnvironment File\n--------------------------------\n.. code-block::\n\n   MPH_API_KEY=<api_key>\n\nPass API Key to Pool Constructor\n--------------------------------\n.. code-block:: python\n\n   from miningpoolhub_py import Pool\n   pool_instance = Pool('ethereum', '<api_key>')\n\nReferences\n------------\n\nMining Pool Hub\n---------------------------------------------\n- `Mining Pool Hub <https://miningpoolhub.com/>`_\n- `API Reference <https://github.com/miningpoolhub/php-mpos/wiki/API-Reference>`_\n- `Mining Pool Hub API Key <https://miningpoolhub.com/?page=account&action=edit>`_\n\nPython API Wrapper & and CI/CD Pipeline\n---------------------------------------------\n- `Building and Testing an API Wrapper in Python <https://semaphoreci.com/community/tutorials/building-and-testing-an-api-wrapper-in-python>`_\n- `Creating a Python API Wrapper \\(Ally Invest API\\) <https://medium.com/analytics-vidhya/creating-a-python-api-wrapper-ally-invest-api-568934a1411c>`_\n- `Publishing a Package to PyPI with Poetry <https://www.ianwootten.co.uk/2020/10/20/publishing-a-package-to-pypi-with-poetry/>`_\n- `Publishing to PyPI Using GitHub Actions <https://www.ianwootten.co.uk/2020/10/23/publishing-to-pypi-using-github-actions/>`_\n   - `Code Repo <https://github.com/niftydigits/ftrack-s3-accessor/tree/master/.github/workflows>`_\n\nContribute\n----------\n\n- `Issue Tracker <https://github.com/CoryKrol/miningpoolhub_py/issues>`_\n- `Source Code <https://github.com/CoryKrol/miningpoolhub_py>`_\n\nSupport\n-------\n\n`Open an issue <https://github.com/CoryKrol/miningpoolhub_py/issues/new>`_\n\nLicense\n-------\n\nThe project is licensed under the Apache 2 license",
    'author': 'CoryKrol',
    'author_email': '16892390+CoryKrol@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CoryKrol/miningpoolhub_py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
