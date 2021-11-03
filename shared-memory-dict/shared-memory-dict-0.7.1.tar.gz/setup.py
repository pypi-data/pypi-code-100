# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shared_memory_dict', 'shared_memory_dict.caches']

package_data = \
{'': ['*']}

extras_require = \
{'aiocache': ['aiocache>=0.11.1,<0.12.0'],
 'all': ['django>=3.0.8,<4.0.0', 'aiocache>=0.11.1,<0.12.0'],
 'django': ['django>=3.0.8,<4.0.0']}

setup_kwargs = {
    'name': 'shared-memory-dict',
    'version': '0.7.1',
    'description': 'A very simple shared memory dict implementation',
    'long_description': '# Shared Memory Dict\nA very simple [shared memory](https://docs.python.org/3/library/multiprocessing.shared_memory.html) dict implementation.\n\n**Requires**: Python >= 3.8\n\n```python\n>>> # In the first Python interactive shell\n>> from shared_memory_dict import SharedMemoryDict\n>> smd = SharedMemoryDict(name=\'tokens\', size=1024)\n>> smd[\'some-key\'] = \'some-value-with-any-type\'\n>> smd[\'some-key\']\n\'some-value-with-any-type\'\n\n>>> # In either the same shell or a new Python shell on the same machine\n>> existing_smd = SharedMemoryDict(name=\'tokens\', size=1024)\n>>> existing_smd[\'some-key\']\n\'some-value-with-any-type\'\n>>> existing_smd[\'new-key\'] = \'some-value-with-any-type\'\n\n\n>>> # Back in the first Python interactive shell, smd reflects this change\n>> smd[\'new-key\']\n\'some-value-with-any-type\'\n\n>>> # Clean up from within the second Python shell\n>>> existing_smd.shm.close()  # or "del existing_smd"\n\n>>> # Clean up from within the first Python shell\n>>> smd.shm.close()\n>>> smd.shm.unlink()  # Free and release the shared memory block at the very end\n>>> del smd  # use of smd after call unlink() is unsupported\n```\n\n> The arg `name` defines the location of the memory block, so if you want to share the memory between process use the same name\n\n## Installation\nUsing `pip`:\n```shell\npip install shared-memory-dict\n```\n\n## Locks\nTo use [multiprocessing.Lock](https://docs.python.org/3.8/library/multiprocessing.html#multiprocessing.Lock) on write operations of shared memory dict set environment variable `SHARED_MEMORY_USE_LOCK=1`.\n\n## Serialization\n\nWe use [pickle](https://docs.python.org/3/library/pickle.html) as default to read and write the data into the shared memory block.\n\nYou can create a custom serializer by implementing the `dumps` and `loads` methods.\n\n```python\nNULL_BYTE: Final = b"\\x00"\n\n\nclass JSONSerializer:\n    def dumps(self, obj: dict) -> bytes:\n        return json.dumps(obj).encode() + NULL_BYTE\n\n    def loads(self, data: bytes) -> dict:\n        data = data.split(NULL_BYTE, 1)[0]\n        return json.loads(data)\n\n```\n\nNote: A null byte is used to separate the dictionary contents from the bytes that are in memory.\n\nTo use the custom serializer you must set it when creating a new shared memory dict instance:\n \n```python\n>>> smd = SharedMemoryDict(name=\'tokens\', size=1024, serializer=JSONSerializer())\n```\n\n### Caveat\n\nThe pickle module is not secure. Only unpickle data you trust.\n\nSee more [here](https://docs.python.org/3/library/pickle.html).\n\n\n## Django Cache Implementation\nThere\'s a [Django Cache Implementation](https://docs.djangoproject.com/en/3.0/topics/cache/) with Shared Memory Dict:\n\n```python\n# settings/base.py\nCACHES = {\n    \'default\': {\n        \'BACKEND\': \'shared_memory_dict.caches.django.SharedMemoryCache\',\n        \'LOCATION\': \'memory\',\n        \'OPTIONS\': {\'MEMORY_BLOCK_SIZE\': 1024}\n    }\n}\n```\n\n**Install with**: `pip install "shared-memory-dict[django]"`\n\n### Caveat\nWith Django cache implementation the keys only expire when they\'re read. Be careful with memory usage\n\n\n## AioCache Backend\nThere\'s also a [AioCache Backend Implementation](https://aiocache.readthedocs.io/en/latest/caches.html) with Shared Memory Dict:\n\n```python\nFrom aiocache import caches\n\ncaches.set_config({\n    \'default\': {\n        \'cache\': \'shared_memory_dict.caches.aiocache.SharedMemoryCache\',\n        \'size\': 1024,\n    },\n})\n```\n\n> This implementation is very based on aiocache [SimpleMemoryCache](https://aiocache.readthedocs.io/en/latest/caches.html#simplememorycache)\n\n**Install with**: `pip install "shared-memory-dict[aiocache]"`\n',
    'author': 'Arquitetura LuizaLabs',
    'author_email': 'arquitetura@luizalabs.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/luizalabs/shared-memory-dict',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
