# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['staticbackend']

package_data = \
{'': ['*']}

install_requires = \
['asgiref>=3.4.1,<4.0.0',
 'email-validator>=1.1.3,<2.0.0',
 'httpx>=0.19.0,<0.20.0',
 'mkdocs-material>=7.3.6,<8.0.0',
 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'staticbackend',
    'version': '0.1.1',
    'description': 'StaticBackend Python client',
    'long_description': '# backend-python\n\n[StaticBackend](https://staticbackend.com/) Python 3 client.\n\n## Requirements\n\nCPython 3.6.2+\n\n## Installatin\n\n```\npip install staticbackend\n```\n\n## Usage\n\n```python\nfrom staticbackend import Config, StaticBackend\n\nconfig = Config(\n    api_token=os.environ["PUBLICKEY"],\n    root_token=os.environ["ROOTKEY"],\n    endpoint=os.environ["ENDPOINT"],\n)\nbackend = StaticBackend(config)\nstate = backend.user.login("foo@bar.com", "zot")\ndocs = state.database.list_documents(db)\nprint(docs)\n```\n\n## Features\n\n- [x] User Management\n    - [x] Register\n    - [x] Login\n    - [x] Reset Password\n- [x] Database\n    - [x] Create a document\n    - [x] List documents\n    - [x] Get a document\n    - [x] Query for documents\n    - [x] Update a document\n    - [x] Delete documents\n- [x] Storage\n    - [x] Upload files\n- [ ] Forms\n    - [ ] Submit HTML forms\n- [ ] Websocket\n\n## License\n\nMIT\n\n## Contributing\n\nTBD.\n\n## CHANGELOG\n\nSee [CHANGELOG.md](https://github.com/staticbackendhq/backend-python/blob/main/CHANGELOG.md)\n',
    'author': 'ipfans',
    'author_email': '363344+ipfans@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://staticbackend.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
