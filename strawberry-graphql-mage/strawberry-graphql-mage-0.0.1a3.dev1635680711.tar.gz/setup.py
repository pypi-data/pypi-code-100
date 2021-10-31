# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strawberry_mage',
 'strawberry_mage.backends',
 'strawberry_mage.backends.api',
 'strawberry_mage.backends.json',
 'strawberry_mage.backends.python',
 'strawberry_mage.backends.sqlalchemy',
 'strawberry_mage.core']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy-Utils>=0.37.9,<0.38.0',
 'SQLAlchemy[asyncio]>=1.4.25,<2.0.0',
 'aiosqlite>=0.17.0,<0.18.0',
 'frozendict>=2.0.6,<3.0.0',
 'inflection>=0.5.1,<0.6.0',
 'overrides>=6.1.0,<7.0.0',
 'strawberry-graphql>=0.84,<0.86']

setup_kwargs = {
    'name': 'strawberry-graphql-mage',
    'version': '0.0.1a3.dev1635680711',
    'description': 'An automated, modular, backend-agnostic GraphQL schema generator',
    'long_description': '# Strawberry-GraphQL-Mage\n\nAn automated, modular, backend-agnostic GraphQL schema generator.\n\nThe aim of this project is to simplify graphql api creation without being tied to one specific data backend.\n\nPerformance is currently not a major factor - this is mostly a helper library to make creating GraphQL endpoints easier.\n\n## Still under heavy development\n\nFeel free to use it and create issues though.\n\nContributions are welcome as well.\n\n## TO-DO list\n\n- [x] Generating a basic GraphQL schema\n- [x] Queries\n- [x] Mutations\n- [ ] Subscriptions\n- [x] Backend separation + dummy backend\n- [ ] SQLAlchemy backend\n  - [x] Entity models\n  - [x] Implement basic mutations/queries\n  - [x] Add basic tests\n  - [ ] Add more tests\n  - [x] Asyncio\n  - [ ] Implement abstract sqla models\n- [ ] Python backend\n  - [x] Basic SQLAlchemy conversion\n  - [x] Database engine pool\n  - [ ] Native python datatype simple implementation\n  - [x] Queries\n  - [x] Queries with dynamic dataset\n  - [ ] Mutations\n  - [ ] TESTS\n- [ ] JSON (dict) backend\n  - [x] Conversion to python backend\n  - [x] Queries\n  - [x] Queries with dynamic dataset\n  - [ ] Mutations\n  - [ ] TESTS\n- [ ] API backend (REST/GraphQL)\n  - [x] Queries\n  - [x] Queries with dynamic dataset\n  - [x] Mutations\n  - [ ] Helpers for graphql input fields conversion\n  - [ ] Improve the structure\n  - [ ] TESTS\n- [ ] Separate backends into package extras\n- [ ] Add more filters\n- [ ] Add options for custom data-types\n- [ ] Setup CI\n- [ ] Try some authorization / authentication\n- [ ] Write instructions for using the app\n- [ ] Write instructions for creating custom backends\n',
    'author': 'Vojtěch Dohnal',
    'author_email': 'vojdoh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
