# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neuroio',
 'neuroio.auth',
 'neuroio.billing',
 'neuroio.entries',
 'neuroio.groups',
 'neuroio.licenses',
 'neuroio.licenses.sources',
 'neuroio.lists',
 'neuroio.lists.spaces',
 'neuroio.notifications',
 'neuroio.persons',
 'neuroio.settings',
 'neuroio.sources',
 'neuroio.spaces',
 'neuroio.streams',
 'neuroio.streams.tokens',
 'neuroio.tokens',
 'neuroio.utility',
 'neuroio.whoami']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'neuroio',
    'version': '0.0.9',
    'description': 'A Python package for interacting with NeuroIO API',
    'long_description': '# Python API client for NeuroIO\n\n\n[![PyPI version](https://badge.fury.io/py/neuroio.svg)](http://badge.fury.io/py/neuroio)\n[![codecov](https://codecov.io/gh/neuroio/neuroio-python/branch/master/graph/badge.svg)](https://codecov.io/gh/neuroio/neuroio-python)\n[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/neuroio/)\n[![Downloads](https://pepy.tech/badge/neuroio)](https://pepy.tech/project/neuroio)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)\n\n_________________\n\n[Read Latest Documentation](https://neuroio.github.io/neuroio-python/) - [Browse GitHub Code Repository](https://github.com/neuroio/neuroio-python/)\n_________________\n\nThis library strives to be a complete mirror of official NeuroIO API in terms of methods and interfaces.\n\nOfficial latest API documentation can be found [here](https://kb.neuroio.com/).\n\nFor your convenience, you can make API calls using sync or async (asyncio) interface.\n\n## Installation\n\n```sh\npip install neuroio\n```\n\nNote that it is always recommended pinning version of your installed packages.\n\n## Usage example (sync)\n\nAn example of how to create a source:\n\n```python\nfrom neuroio import Client\n\n\nif __name__ == \'__main__\':\n    # api_token is just str with your API token from NeuroIO\n    api_token = "abcd012345"\n    # Now create instance of Client. There should be only one per process.\n    client = Client(api_token=api_token)\n    # Issue API request to create source\n    client.sources.create(name="test_name")\n\n```\n\nNow that we have our source created, we can create person inside that source:\n\n```python\nfrom neuroio import Client\n\n\ndef create_persons_example(client: Client):\n    source_name = "test_name"\n    with open("image.png", "rb") as f:\n        response = client.persons.create(\n            image=f,\n            source=source_name,\n            facesize=1000,\n            create_on_ha=True,\n            create_on_junk=True,\n            identify_asm=True\n        )\n    print("Persons Create Response:\\n", response.json(), flush=True)\n\n\nif __name__ == \'__main__\':\n    # api_token is just str with your API token from NeuroIO\n    api_token = "abcd012345"\n    # Now create instance of Client. There should be only one per process.\n    client = Client(api_token=api_token)\n    # Issue API request to create a person\n    create_persons_example(client)\n\n```\n\nNow that we have our source & person created, we can search for persons:\n\n```python\nfrom neuroio import Client\n\n\ndef search_persons_example(client: Client):\n    with open("image.png", "rb") as f:\n        response = client.persons.search(\n            image=f,\n            identify_asm=True\n        )\n    print("Persons Search Response:\\n", response.json(), flush=True)\n\n\nif __name__ == \'__main__\':\n    # api_token is just str with your API token from NeuroIO\n    api_token = "abcd012345"\n    # Now create instance of Client. There should be only one per process.\n    client = Client(api_token=api_token)\n    # Issue API request to search persons\n    search_persons_example(client)\n\n```\n\n_For more examples and usage, please refer to the [docs](https://neuroio.github.io/neuroio-python/)._\n\n## Development setup\n\nTo install all the development requirements:\n\n```sh\npip install --upgrade pip\npip install poetry\npoetry install --no-root\n```\n\nTo run linters & test suite:\n\n```sh\n./scripts/test.sh\n```\n\n## Release History\n* 0.0.9\n    * Fixes to the sources API in terms of required fields\n* 0.0.8\n    * Updated library to latest API version (at the time of this release - 1.3.1)\n    * Updated README & docs\n* 0.0.7\n    * Updated library to latest API version (at the time of this release - 1.3.0)\n    * Updated requirements\n    * Updated README & docs\n* 0.0.6\n    * Updated library to latest API version (at the time of this release - 1.2.1)\n    * Updated README & docs\n* 0.0.5\n    * Fixed persistent connection problems\n    * Updated requirements\n    * Codebase cleanup\n* 0.0.4\n    * Changed the way how we treat httpx connection - now we don\'t close it after every request (which was supposedly right way in httpx docs)\n* 0.0.3\n    * Updated httpx version, disabled cruft check since it just messes up project files\n\n## License\n\nDistributed under the MIT license. See ``LICENSE`` for more information.\n\n## Contributing\n\n1. Fork it (<https://github.com/yourname/yourproject/fork>)\n2. Create your feature branch (`git checkout -b feature/fooBar`)\n3. Commit your changes (`git commit -am \'Add some fooBar\'`)\n4. Push to the branch (`git push origin feature/fooBar`)\n5. Create a new Pull Request\n',
    'author': 'Lev Rubel',
    'author_email': 'l@datacorp.ee',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
