# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ethereum_kms_signer', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.5.12,<2.0.0',
 'eth-account>=0.5.6,<0.6.0',
 'eth-utils>=1.10.0,<2.0.0',
 'fire==0.4.0',
 'hexbytes>=0.2.2,<0.3.0',
 'pyasn1>=0.4.8,<0.5.0',
 'pycryptodome>=3.10.1,<4.0.0',
 'toolz>=0.11.1,<0.12.0']

entry_points = \
{'console_scripts': ['ethereum_kms_signer = ethereum_kms_signer.cli:main']}

setup_kwargs = {
    'name': 'ethereum-kms-signer',
    'version': '0.1.5',
    'description': 'Sign ETH transactions with keys stored in AWS KMS.',
    'long_description': '# Ethereum KMS Signer\n\n\n<p align="center">\n<a href="https://pypi.python.org/pypi/ethereum_kms_signer">\n    <img src="https://img.shields.io/pypi/v/ethereum_kms_signer.svg"\n        alt = "Release Status">\n</a>\n\n<a href="https://github.com/meetmangukiya/ethereum_kms_signer/actions">\n    <img src="https://github.com/meetmangukiya/ethereum_kms_signer/actions/workflows/dev.yml/badge.svg?branch=main" alt="CI Status">\n</a>\n\n</p>\n\n\nSign ETH transactions with keys stored in AWS KMS\n\n\n* Free software: MIT\n* Documentation: <https://meetmangukiya.github.io/ethereum-kms-signer>\n\n## Features\n\n* Sign Transactions\n\n## Video Demo\n\n[![Python Ethereum KMS Signer Demo](https://user-images.githubusercontent.com/7620533/135247248-7c3efda3-b8f8-4936-a2b6-363cb05ba513.png)](https://youtu.be/fZ-mtMb2BjY "Python Ethereum KMS Signer Demo")\n\n## Why?\n\nIn the crypto world, all the assets, tokens, crypto you might own is\nprotected by the secrecy of the private key. This leads to a single point\nof failure in cases of leaking of private keys or losing keys because of\nlack of backup or any number of reasons. It becomes even harder when you want\nto share these keys as an organization among many individuals.\n\nUsing something like AWS KMS can help with that and can provide full benefits\nof all the security features it provides. Sigantures can be created without the key\never leaving the AWS\'s infrastructure and could be effectively shared among individuals.\n\nThis library provides a simple and an easy-to-use API for using AWS KMS to sign ethereum\ntransactions and an easy integration with `web3.py` making it practical for using KMS to\nmanage your private keys.\n\n## Quickstart\n\n### Get ethereum address from KMS key\n\n```python\nfrom ethereum_kms_signer import get_eth_address\naddress = get_eth_address(\'THE-AWS-KMS-ID\')\nprint(address)\n```\n\n### Sign a transaction object with KMS key\n\n```python\nfrom ethereum_kms_signer import sign_transaction\n\ndai_txn = dai.functions.transfer(\n    web3.toChecksumAddress(to_address.lower()), amount\n).buildTransaction(\n    {\n        "nonce": nonce,\n    }\n)\n\n# Signing the transaction with KMS key\nsigned_tx = sign_transaction(dai_txn, key_id)\n\n# send transaction\ntx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)\n```\n\n### Provisioning AWS KMS key with terraform\n\nAn `ECC_SECG_P256K1` key can be provisioned using terraform by using the following\nconfiguration along with the aws provider. More details can be found on\n[provider docs]()\n\n```tf\nresource "aws_kms_key" "my_very_secret_eth_account" {\n    description                 = "ETH account #1"\n    key_usage                   = "SIGN_VERIFY"\n    customer_master_key_spec    = "ECC_SECG_P256K1"\n}\n\nresource "aws_kms_alias" "my_very_secret_eth_account" {\n    name            = "eth-account-1"\n    target_key_id   = aws_kms_key.my_very_secret_eth_account.id\n}\n```\n\n## Examples\n\nFew examples can be found [here](https://github.com/meetmangukiya/ethereum-kms-signer/tree/main/examples).\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage) project template.\n\n[This article](https://luhenning.medium.com/the-dark-side-of-the-elliptic-curve-signing-ethereum-transactions-with-aws-kms-in-javascript-83610d9a6f81) has served as a good resource for implementing the functionality\n',
    'author': 'Meet Mangukiya',
    'author_email': 'meet@flamy.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/meetmangukiya/ethereum_kms_signer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
