# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['turdshovel',
 'turdshovel._stubs.Microsoft',
 'turdshovel._stubs.Microsoft.Diagnostics',
 'turdshovel._stubs.Microsoft.Diagnostics.NETCore',
 'turdshovel._stubs.Microsoft.Diagnostics.Runtime',
 'turdshovel._stubs.Microsoft.Diagnostics.Runtime.DataReaders',
 'turdshovel._stubs.System',
 'turdshovel._stubs.System.Buffers',
 'turdshovel._stubs.System.Collections',
 'turdshovel._stubs.System.Reflection',
 'turdshovel._stubs.System.Reflection.Metadata',
 'turdshovel._stubs.System.Runtime',
 'turdshovel._stubs.System.Threading',
 'turdshovel._stubs.System.Threading.Tasks',
 'turdshovel.commands',
 'turdshovel.core']

package_data = \
{'': ['*'], 'turdshovel': ['_dlls/*']}

install_requires = \
['numpy>=1.21.2,<2.0.0',
 'orjson>=3.6.4,<4.0.0',
 'pyparsing==2.4.7',
 'python-nubia>=0.2b5,<0.3',
 'pythonnet>=2.5.2,<3.0.0',
 'rich>=10.12.0,<11.0.0']

entry_points = \
{'console_scripts': ['turdshovel = turdshovel.main:init']}

setup_kwargs = {
    'name': 'turdshovel',
    'version': '0.2',
    'description': 'Looks through memory dumps for secrets',
    'long_description': None,
    'author': 'Leron Gray',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<3.9',
}


setup(**setup_kwargs)
