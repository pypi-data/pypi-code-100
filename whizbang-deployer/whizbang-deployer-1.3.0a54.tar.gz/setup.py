# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whizbang',
 'whizbang.config',
 'whizbang.container',
 'whizbang.core',
 'whizbang.data',
 'whizbang.data.databricks',
 'whizbang.data.pyodbc',
 'whizbang.domain.commandline',
 'whizbang.domain.handler',
 'whizbang.domain.manager',
 'whizbang.domain.manager.az',
 'whizbang.domain.manager.bicep',
 'whizbang.domain.manager.databricks',
 'whizbang.domain.manager.pyodbc',
 'whizbang.domain.menu',
 'whizbang.domain.models',
 'whizbang.domain.models.active_directory',
 'whizbang.domain.models.commandline',
 'whizbang.domain.models.databricks',
 'whizbang.domain.models.keyvault',
 'whizbang.domain.models.menu',
 'whizbang.domain.models.sql',
 'whizbang.domain.models.storage',
 'whizbang.domain.repository',
 'whizbang.domain.repository.az',
 'whizbang.domain.repository.databricks',
 'whizbang.domain.repository.sql_server',
 'whizbang.domain.shared_types',
 'whizbang.domain.solution',
 'whizbang.domain.workflow',
 'whizbang.domain.workflow.bicep',
 'whizbang.domain.workflow.databricks',
 'whizbang.domain.workflow.datalake',
 'whizbang.notes',
 'whizbang.util']

package_data = \
{'': ['*'], 'whizbang': ['reference/*']}

install_requires = \
['az.cli>=0.5,<0.6',
 'databricks-cli==0.16.2',
 'dependency-injector>=4.35.2,<5.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'pyodbc>=4.0.32,<5.0.0',
 'pytest>=6.2.4,<7.0.0',
 'sqlparse>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['whizbang = whizbang.__main__:main']}

setup_kwargs = {
    'name': 'whizbang-deployer',
    'version': '1.3.0a54',
    'description': 'Whizbang Deployer - An all-in-one Azure deployment solution',
    'long_description': 'whizbang-deployer readme placeholder\n\n\nTo run pytests\ndocker-compose -f docker_builds/docker-compose.yml up --build pyenv\n\nTo run pytests with watch\ndocker-compose -f docker_builds/docker-compose.yml up --build pyenv-watch',
    'author': 'Brian Aiken',
    'author_email': 'baiken@hitachisolutions.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hitachisolutionsamerica/whizbang-deployer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
