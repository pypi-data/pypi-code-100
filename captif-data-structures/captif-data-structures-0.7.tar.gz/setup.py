# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['captif_data_structures', 'captif_data_structures.structure']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.3,<2.0.0',
 'parse>=1.19.0,<2.0.0',
 'psutil>=5.8.0,<6.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'unsync>=1.4.0,<2.0.0']

setup_kwargs = {
    'name': 'captif-data-structures',
    'version': '0.7',
    'description': '',
    'long_description': '# captif-data-structures\n\nPython package to keep track of the various data files and file versions used by CAPTIF Road Research. The package includes reader classes for general data types.\n\nThe following data types are currently supported.\n\nCAPTIF facility:\n- lap count\n\nInstruments:\n - deflection beam\n - stationary laser profilometer (SLP)\n\nExamples of the data structures currently supported can be found in `./tests/data`.',
    'author': 'John Bull',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/captif-nz/captif-data-structures',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
