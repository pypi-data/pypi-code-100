# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['datalakebundle',
 'datalakebundle.delta',
 'datalakebundle.notebook.decorator',
 'datalakebundle.notebook.decorator.tests',
 'datalakebundle.notebook.lineage',
 'datalakebundle.notebook.lineage.argument',
 'datalakebundle.table',
 'datalakebundle.table.class_',
 'datalakebundle.table.create',
 'datalakebundle.table.delete',
 'datalakebundle.table.identifier',
 'datalakebundle.table.name',
 'datalakebundle.table.optimize',
 'datalakebundle.table.parameters',
 'datalakebundle.table.read',
 'datalakebundle.table.schema',
 'datalakebundle.table.schema.tests',
 'datalakebundle.table.upsert',
 'datalakebundle.table.write',
 'datalakebundle.table.write.tests',
 'datalakebundle.test']

package_data = \
{'': ['*'], 'datalakebundle': ['_config/*']}

install_requires = \
['console-bundle>=0.5,<0.6',
 'daipe-core==1.2.0dev1',
 'deepdiff>=5,<6',
 'injecta>=0.10.0,<0.11.0',
 'pyfony-bundles>=0.4.0,<0.5.0',
 'pyspark-bundle==1.2.0dev1',
 'simpleeval>=0.9.10,<1.0.0']

entry_points = \
{'pyfony.bundle': ['create = datalakebundle.DataLakeBundle:DataLakeBundle']}

setup_kwargs = {
    'name': 'datalake-bundle',
    'version': '1.2.0.dev3',
    'description': 'DataLake tables management bundle for the Daipe Framework',
    'long_description': '# Datalake bundle\n\nThis bundle allows you to easily create and manage datalake(house) based on the [Daipe Framework](https://www.daipe.ai).  \n\n## Resources\n\n* [Documentation](https://docs.daipe.ai/data-pipelines-workflow/managing-datalake/)\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/daipe-ai/datalake-bundle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
