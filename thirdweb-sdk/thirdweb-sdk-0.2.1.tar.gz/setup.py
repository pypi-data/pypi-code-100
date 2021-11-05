# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nftlabs',
 'nftlabs.abi',
 'nftlabs.abi.coin',
 'nftlabs.abi.erc1155',
 'nftlabs.abi.erc165',
 'nftlabs.abi.erc20',
 'nftlabs.abi.market',
 'nftlabs.abi.nft',
 'nftlabs.abi.nft_collection',
 'nftlabs.abi.pack',
 'nftlabs.errors',
 'nftlabs.modules',
 'nftlabs.options',
 'nftlabs.storage',
 'nftlabs.types',
 'nftlabs.types.collection',
 'nftlabs.types.currency',
 'nftlabs.types.market',
 'nftlabs.types.metadata',
 'nftlabs.types.nft',
 'nftlabs.types.pack']

package_data = \
{'': ['*']}

install_requires = \
['0x-contract-wrappers>=2.0.0,<3.0.0',
 'dataclasses-json>=0.5.6,<0.6.0',
 'requests>=2.26.0,<3.0.0',
 'web3>=5.24.0,<6.0.0']

setup_kwargs = {
    'name': 'thirdweb-sdk',
    'version': '0.2.1',
    'description': 'Official ThirdWeb sdk',
    'long_description': None,
    'author': 'Ibrahim Ahmed',
    'author_email': 'abe@thirdweb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
