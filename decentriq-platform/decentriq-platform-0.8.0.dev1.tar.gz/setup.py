# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['decentriq_platform', 'decentriq_platform.proto']

package_data = \
{'': ['*']}

install_requires = \
['argon2-cffi>=20.1.0,<21.0.0',
 'asn1crypto>=1.2.0,<2.0.0',
 'certvalidator>=0.11.1,<0.12.0',
 'chily>=0.5.3,<0.6.0',
 'cryptography>=3.4.6,<4.0.0',
 'protobuf>=3.15.0,<4.0.0',
 'requests>=2.25.0,<3.0.0',
 'sgx-ias-structs>=0.1.7,<0.2.0',
 'sqloxide==0.1.12',
 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'decentriq-platform',
    'version': '0.8.0.dev1',
    'description': 'Python client library for the Decentriq platform',
    'long_description': '# decentriq-platform-client\n\nPython client library for the Decentriq platform.\n\n## Installation\n\nAfter cloning the repository you can install the library using pip:\n\n### Virtual environment(optional)\n\nBefore installing the library you may want to working inside a virtual environment:\n\n```\npython -m venv env\nsource env/bin/activate\n```\n\n### Pip\n\nTo install with pip just run:\n\n```\npip install .\n```\n\n## Usage:\n\nTo have an idea of how to use this library, you can check the demo in the `example`\n directory.\n\n## Testing\n\nTo start the testing process install `nox` with `pip install nox` and the run it\nin the project directory. *N.B. make sure you have an available avato-backend*\n\n**nox**\n```\nnox\n```\n',
    'author': 'decentriq',
    'author_email': 'opensource@decentriq.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/decentriq/decentriq-platform',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
