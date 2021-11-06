# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flow_py_sdk',
 'flow_py_sdk.cadence',
 'flow_py_sdk.client',
 'flow_py_sdk.frlp',
 'flow_py_sdk.proto',
 'flow_py_sdk.proto.flow',
 'flow_py_sdk.signer']

package_data = \
{'': ['*']}

install_requires = \
['betterproto[compiler]>=1.2.5,<2.0.0',
 'ecdsa==v0.17.0',
 'grpcio-tools>=1.33.2,<2.0.0',
 'grpclib>=0.4.1,<0.5.0',
 'rlp>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['examples = examples.main:run']}

setup_kwargs = {
    'name': 'flow-py-sdk',
    'version': '1.0.0',
    'description': 'A python SKD for the flow blockchain',
    'long_description': 'The Flow Python SDK provides a set of packages for Python developers to build applications that interact with the Flow network.\n\n[![PyPI](https://img.shields.io/pypi/v/flow-py-sdk.svg)](https://pypi.org/project/flow-py-sdk/)\n[![codecov](https://codecov.io/gh/janezpodhostnik/flow-py-sdk/branch/master/graph/badge.svg)](https://codecov.io/gh/codecov/example-go)\n\n\nSee the [guide](https://janezpodhostnik.github.io/flow-py-sdk)!\n\n\nNote: This SDK is also fully compatible with the Flow Emulator and can be used for local development.\n\n## Installing\n\nTo start using the SDK, install Python 3.9 or higher and install package:\n\n```sh\npip install flow-py-sdk\n```\n\nor if using poetry:\n\n```sh\npoetry add flow-py-sdk\n```\n\n## Contributors\n\n<a href="https://github.com/janezpodhostnik/flow-py-sdk/graphs/contributors">\n  <img src="https://contrib.rocks/image?repo=janezpodhostnik/flow-py-sdk" />\n</a>\n\nMade with [contrib.rocks](https://contrib.rocks).',
    'author': 'Janez Podhostnik',
    'author_email': 'janez.podhostnik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/janezpodhostnik/flow-py-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
