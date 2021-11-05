# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xleapp_ios',
 'xleapp_ios.helpers.parsers',
 'xleapp_ios.helpers.parsers.ccl',
 'xleapp_ios.helpers.parsers.ktx',
 'xleapp_ios.plugins',
 'xleapp_ios.plugins.old']

package_data = \
{'': ['*']}

install_requires = \
['astc-decomp>=1.0.3,<2.0.0',
 'astc_decomp>=1.0.3,<2.0.0',
 'blackboxprotobuf>=1.0.1,<2.0.0',
 'bplist>=1.1,<2.0',
 'bs4>=0.0.1,<0.0.2',
 'nska-deserialize>=1.3.1',
 'pandas>=1.3.3,<2.0.0',
 'pillow>=8.3.2,<9.0.0',
 'pyliblzfse>=0.4.1,<0.5.0']

entry_points = \
{'xleapp.plugins': ['ios = xleapp_ios.plugins:IosPlugin']}

setup_kwargs = {
    'name': 'xleapp-ios',
    'version': '0.1.1a0',
    'description': 'iOS Artifacts for xLEAPP (free)',
    'long_description': '# xLEAPP iOS Artifacts \n\nProvides iOS artifacts supported under [MIT license ](https://opensource.org/licenses/MIT).\n\nThis is not a standalone package. xLEAPP is required to be installed. See xLEAPP project documentation for information on using this plugins.',
    'author': 'Jesse Spangenberger',
    'author_email': 'azuleonyx@digitalforensics.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
