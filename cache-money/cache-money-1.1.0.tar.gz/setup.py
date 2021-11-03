# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cache_money']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'cache-money',
    'version': '1.1.0',
    'description': 'Async cache decorator for memoization using aioredis.',
    'long_description': '# Cache Money\n\n[![Build Status](https://dev.azure.com/novisto/novisto/_apis/build/status/novisto.cache-money?branchName=master)](https://dev.azure.com/novisto/novisto/_build/latest?definitionId=30&branchName=master)\n[![codecov](https://codecov.io/gh/novisto/cache-money/branch/master/graph/badge.svg?token=V05Y6MTMU2)](https://codecov.io/gh/novisto/cache-money)\n[![Version](https://img.shields.io/pypi/v/cache-money)](https://pypi.org/project/cache-money/)\n[![Python Version](https://img.shields.io/pypi/pyversions/cache-money)](https://pypi.org/project/cache-money/)\n\nAsync cache library for [memoization](https://en.wikipedia.org/wiki/Memoization) using Redis. Inspired by \n[Walrus](https://github.com/coleifer/walrus) and implemented with [aioredis](https://github.com/aio-libs/aioredis-py).\n\nCache Money is used through a decorator you can add to your function that needs to be cached. When the decorator \ngets executed, Cache Money will make a unique key from the name of the function and the params received and look up in \nredis if there is a result for this key. If there is a result it will be used as the output of the function and the \nexecution of the function will be skipped.\n\nYou can add a timeout in the declaration of the decorator, you can find constants for common timeout duration in \n`cache_money/constants.py`. When the timeout is reached, Redis remove the entry itself.\n\nIt\'s also possible to clear the cache early by using the method bust that gets added to a function decorated by \nCache Money. An example is provided below.\n\nThis library is available on PyPI under the name cache-money. You can install with pip by running `pip install \ncache-money`.\n\n\n# Requirements\n\nYou need a redis instance running to use this library. This library was tested to run on version of Redis >= 4.0.0. \nIf you have docker set up you can create a redis instance like this:\n\n```shell\nmake redis-start\n```\n\n\n# Usage\n\n## Basic usage\n\nFirst thing is initializing Cache Money and decorating a function that you want to cache\n\n```python\nfrom cache_money import cache_money, init_cache_money\nfrom cache_money.constants import CACHE_HOUR, CACHE_WEEK\n\ninit_cache_money(host="localhost")\n\n@cache_money.cached(timeout=CACHE_HOUR)\nasync def addition(x: int, y: int) -> int:\n    return x + y\n\n@cache_money.cached(timeout=CACHE_WEEK)\nasync def multiplication(x: int, y: int) -> int:\n    return x * y\n```\n\nIf you run the following calls to the function `addition` consecutively:\n```doctest\n  >>> await addition(3, 4)\n  7\n  \n  >>> await addition(3, 7)\n  10\n \n  >>> await addition(3, 4)\n  7\n```\n\nThe first and second call would be executed, but the third call would have used the cache in redis instead, as long \nas the third call was done within one hour of when the first call was made, as the function addition is caching results \nfor one hour.\n\nIn Redis you would see two entries like this:\n\n```shell\n# redis-cli \n\n127.0.0.1:6379> KEYS *\n1) "__main__:addition:ea53056bad64a599c84efdfd4f4cbb64"\n2) "__main__:addition:bb6b7afb6a6cf3191f6d7fd35d976d42"\n\n127.0.0.1:6379> TTL addition:ea53056bad64a599c84efdfd4f4cbb64\n(integer) 3403\n```\n\n## Busting cache for a specific function call\n\nYou can force expire (bust) the cache for a specific function call\n\n```doctest\n>> await addition(3, 4)\n>> await addition(3, 7)\n>> await addition.bust(3, 4)\n```\n\nIn Redis you would see one entry as the other one has been busted\n\n```shell\n127.0.0.1:6379> KEYS *\n1) "__main__:addition:bb6b7afb6a6cf3191f6d7fd35d976d42"\n```\n\n\n## Busting cache for all function calls of a specific function\n\nYou can bust the cache for all instance of a function call\n\n```doctest\n>> await addition(3, 4)\n>> await addition(3, 7)\n>> await multiplication(2, 4)\n>> await addition.bust_all()\n```\n\nIn Redis you would see no entries for the function `addition` which has been busted,\nyou would see one entry for `multiplication`\n\n```shell\n127.0.0.1:6379> KEYS *\n1) "__main__:multiplication:bc3b7afc6a7cf3191f6d1fd31d810d55"\n```\n\n\n## Busting cache for all function calls of all functions\n\nYou can bust the cache of all entries made by Cache Money as well\n\n```doctest\n>> await addition(3, 4)\n>> await addition(3, 7)\n>> await multiplication(2, 4)\n>> cache_money.bust()\n```\n\nIn Redis you would see no entries\n\n```shell\n127.0.0.1:6379> KEYS *\n(empty array)\n```\n\n\n## Contributing and getting set up for local development\n\nTo set yourself up for development on Cache Money, make sure you are using\n[poetry](https://poetry.eustace.io/docs/) and simply run the following commands from the root directory:\n\n```shell\nmake sys-deps\nmake install\n```\n',
    'author': 'Alexandre Jutras',
    'author_email': 'alexandre.jutras@novisto.com',
    'maintainer': 'Alexandre Jutras',
    'maintainer_email': 'alexandre.jutras@novisto.com',
    'url': 'https://github.com/novisto/cache-money',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
