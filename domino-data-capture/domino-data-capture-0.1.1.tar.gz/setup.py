# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['domino_data_capture']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.1.0,<22.0.0',
 'httpx>=0.15.4,<0.19.0',
 'python-dateutil>=2.8.0,<3.0.0']

setup_kwargs = {
    'name': 'domino-data-capture',
    'version': '0.1.1',
    'description': 'Domino Prediction Client to log prediction data',
    'long_description': '# Domino Data Capture\nDomino Data capture repository which captures user provided prediction data\n\n# How to install\nThis python package is hosted in `pypi`. Use command `pip install domino-data-capture` to install.\n\n\n# How to use\nPlease refer to `library_usage.py` for a complete usage example\n\n## 🛡 License\n\n[![License](https://img.shields.io/github/license/cerebrotech/data-access-sdk)](https://github.com/cerebrotech/dmm-data-ingest-client/blob/master/LICENSE.txt)\n\nThis project is licensed under the terms of the `Apache Software License 2.0` license. See [LICENSE](https://github.com/cerebrotech/dmm-data-ingest-client/blob/master/LICENSE.txt) for more details.\n\n# Important make rules\nHere are the available make rules that will help you in easing your development work\n```shell\n\nmake install-poetry      -> Installs poetry\nmake poetry-remove       -> Uninstalls poetry\nmake install             -> Installs poetry dependencies\nmake pre-commit-install  -> Install pre commit hooks\nmake codestyle           -> Runs codestyle check with black and isort\nmake formatting          -> Runs codestyle\nmake test                -> Runs tests\nmake check-codestyle     -> Checks codestyle\nmake check-safety        -> Checks safety and generates full report\nmake lint                -> Runs linting check with black\nmake build               -> Builds python artifacts\nmake publish             -> Publishes atrifacts to pypi\n``` \n\n# Build and Release process\n\nBuild and Release happens through poetry. Refer to the below commands.\n\n```shell\npoetry build            -> Builds artefacts\npoetry publish          -> Publishes artefacts to pypi\n```\n\n# Support policy\n  * For support policy please refer to the [readme.txt](readme.txt) present in this repo.',
    'author': 'Sayan Nayak',
    'author_email': 'sayan.nayak@dominodatalab.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cerebrotech/dmm-data-ingest-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
