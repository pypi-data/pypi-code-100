# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['tsmock']
setup_kwargs = {
    'name': 'tsmock',
    'version': '0.1.2',
    'description': 'Thread safe wrapper around unittest.mock',
    'long_description': '# tsmock\n\n### Thread safe pything mocking wrapper around unittest.mock\n\nEither monkey patch all mock classes:\n\n```\nfrom tsmock import thread_safe_mocks\nthread_safe_mocks()\n```\n\nOr use a single mock class as needed:\n\n```\nfrom tsmock import MagicMock\n```\n',
    'author': 'Erik Aronesty',
    'author_email': 'erik@atakama.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AtakamaLLC/tsmock',
    'py_modules': modules,
    'python_requires': '>=3.6.8',
}


setup(**setup_kwargs)
