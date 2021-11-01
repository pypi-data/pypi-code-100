# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anvil_rl',
 'anvil_rl.agents',
 'anvil_rl.buffers',
 'anvil_rl.callbacks',
 'anvil_rl.common',
 'anvil_rl.explorers',
 'anvil_rl.models',
 'anvil_rl.signal_processing',
 'anvil_rl.updaters']

package_data = \
{'': ['*']}

install_requires = \
['gym>=0.19.0,<0.20.0',
 'numpy>=1.20.3,<2.0.0',
 'psutil>=5.8.0,<6.0.0',
 'tensorboard>=2.7.0,<3.0.0',
 'torch>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'anvil-rl',
    'version': '0.1.0',
    'description': 'Adaptable tools to make reinforcement learning algorithms',
    'long_description': None,
    'author': 'Rohan Tangri',
    'author_email': 'rohan.tangri@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
