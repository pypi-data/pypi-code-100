# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ethosdistro_py']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'python-dotenv>=0.19.1,<0.20.0', 'yarl>=1.6.3,<2.0.0']

extras_require = \
{'docs': ['Sphinx>=4.2.0,<5.0.0',
          'sphinx-rtd-theme>=1.0.0,<2.0.0',
          'sphinxcontrib-napoleon>=0.7,<0.8']}

setup_kwargs = {
    'name': 'ethosdistro-py',
    'version': '0.1.0',
    'description': 'An async Python wrapper for the ethosOS API',
    'long_description': '\nminingpoolhub_py\n----------------\n.. image:: https://github.com/CoryKrol/ethosdistro_py/workflows/CI/badge.svg?branch=master\n     :target: https://github.com/CoryKrol/ethosdistro_py/actions?workflow=CI\n     :alt: CI Status\n\nA Python wrapper for the EthOS REST API\n\nInstallation\n------------\nInstall with pip:\n\n.. code-block:: bash\n\n   pip install ethosdistro_py\n\nUsage\n------------\n\n.. code-block:: python\n\n   from ethos_py import EthosAPI\n\n   session = aiohttp.ClientSession()\n   ethosapi = EthosAPI(session=session)\n\n\nConfiguration\n-------------------\n\nEnvironment File\n--------------------------------\n.. code-block::\n\n   ETHOS_PANEL_ID=<api_key>\n\n\nReferences\n------------\n\nContribute\n----------\n\n- `Issue Tracker <https://github.com/CoryKrol/ethosdistro_py/issues>`_\n- `Source Code <https://github.com/CoryKrol/ethosdistro_py>`_\n\nSupport\n-------\n\n`Open an issue <https://github.com/CoryKrol/ethosdistro_py/issues/new>`_\n\nLicense\n-------\n\nThe project is licensed under the Apache 2 license',
    'author': 'CoryKrol',
    'author_email': '16892390+CoryKrol@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CoryKrol/ethosdistro_py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
