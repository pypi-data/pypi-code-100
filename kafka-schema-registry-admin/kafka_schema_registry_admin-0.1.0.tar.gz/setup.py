# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kafka_schema_registry_admin']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'kafka-schema-registry-admin',
    'version': '0.1.0',
    'description': 'Python native library to manage Kafka Schemas in Schema Registry',
    'long_description': '===========================\nKafka schema registry admin\n===========================\n\nPure HTTP client library (using requests) to manipulate schemas and definitions into Schema Registry"\n\nAPI specification is documented `here <https://docs.confluent.io/platform/current/schema-registry/develop/api.html#overview>`__\n\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage\n',
    'author': 'johnpreston',
    'author_email': 'john@compose-x.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
