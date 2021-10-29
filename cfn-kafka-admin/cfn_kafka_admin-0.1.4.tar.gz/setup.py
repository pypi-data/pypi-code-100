# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfn_kafka_admin',
 'cfn_kafka_admin.cfn_resources_definitions',
 'cfn_kafka_admin.kafka',
 'cfn_kafka_admin.lambda_functions',
 'cfn_kafka_admin.models',
 'cfn_kafka_admin.specs']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'aws-cfn-custom-resource-resolve-parser>=0.2.1,<0.3.0',
 'cfn-resource-provider>=1.0.7,<2.0.0',
 'compose-x-common[aws]>=0.2.2,<0.3.0',
 'datamodel-code-generator[http]>=0.11.14,<0.12.0',
 'importlib-resources>=5.3.0,<6.0.0',
 'jsonschema>=4.1.2,<5.0.0',
 'kafka-python>=2.0.2,<3.0.0',
 'kafka-schema-registry-admin>=0.1,<0.2',
 'troposphere>=3.1.0,<4.0.0']

entry_points = \
{'console_scripts': ['aws-cfn-kafka-admin-provider = cfn_kafka_admin.cli:main']}

setup_kwargs = {
    'name': 'cfn-kafka-admin',
    'version': '0.1.4',
    'description': 'AWS CloudFormation Resources to manage Kafka',
    'long_description': '===============\ncfn-kafka-admin\n===============\n\n------------------------------------------------------------------------------\nCLI Tool and Lambda Functions to CRUD Kafka resources via AWS CloudFormation\n------------------------------------------------------------------------------\n\n\n.. image:: https://img.shields.io/pypi/v/cfn_kafka_admin.svg\n        :target: https://pypi.python.org/pypi/cfn_kafka_admin\n\n\nManage Kafka resources via AWS CFN\n===================================\n\n* Topics\n* ACLs\n* Schemas (non AWS Glue Schema)\n\n\n* Free software: MPL-2.0\n* Documentation: https://cfn-kafka-admin.readthedocs.io.\n',
    'author': 'johnpreston',
    'author_email': 'john@compose-x.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
