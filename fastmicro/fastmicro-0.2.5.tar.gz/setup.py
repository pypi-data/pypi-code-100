# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastmicro', 'fastmicro.messaging', 'fastmicro.serializer']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0', 'uvloop>=0.15.3,<0.16.0']

extras_require = \
{'kafka': ['aiokafka>=0.7.2,<0.8.0'],
 'msgpack': ['msgpack>=1.0.2,<2.0.0'],
 'redis': ['aioredis>=2.0.0,<3.0.0']}

setup_kwargs = {
    'name': 'fastmicro',
    'version': '0.2.5',
    'description': 'Fast, simple microservice framework',
    'long_description': '# FastMicro\n\n<p align="center">\n    <em>Fast, simple microservice framework</em>\n</p>\n<p align="center">\n<a href="https://github.com/larmoreg/fastmicro/actions/workflows/main.yml" target="_blank">\n    <img src="https://github.com/larmoreg/fastmicro/actions/workflows/main.yml/badge.svg" alt="Test">\n</a>\n<a href="https://codecov.io/gh/larmoreg/fastmicro" target="_blank">\n    <img src="https://codecov.io/gh/larmoreg/fastmicro/branch/master/graph/badge.svg?token=YRMGejrLMC" alt="Coverage">\n</a>\n<a href="https://pypi.org/project/fastmicro" target="_blank">\n    <img src="https://img.shields.io/pypi/v/fastmicro?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n</p>\n\n---\n\nFastMicro is a modern, fast (high-performance) framework for building microservices with Python 3.7+ based on asyncio.\n\n## Install\n\nTo install FastMicro run the following:\n\n<div class="termy">\n\n```console\n$ pip install fastmicro[redis]\n```\n\n</div>\n\n## Example\n\nThis example shows how to use the default in-memory backend for evaluation and testing.\n\n**Note**:\n\nThe in-memory backend cannot be used for inter-process communication.\n\n### Create it\n\n* Create a file `hello.py` with:\n\n```Python\n#!/usr/bin/env python3\n\nimport asyncio\nfrom pydantic import BaseModel\n\nfrom fastmicro.messaging.memory import Messaging, Topic\nfrom fastmicro.service import Service\n\n\nclass User(BaseModel):\n    name: str\n\n\nclass Greeting(BaseModel):\n    name: str\n    greeting: str\n\n\nmessaging: Messaging = Messaging()\nservice = Service("test", messaging)\nuser_topic = Topic("user", messaging, User)\ngreeting_topic = Topic("greeting", messaging, Greeting)\n\n\n@service.entrypoint(user_topic, greeting_topic)\nasync def greet(user: User) -> Greeting:\n    greeting = Greeting(name=user.name, greeting=f"Hello, {user.name}!")\n    return greeting\n\n\nasync def main() -> None:\n    await service.start()\n\n    user = User(name="Greg")\n    print(user)\n    greeting = await greet.call(user)\n    print(greeting)\n\n    await service.stop()\n\n\nif __name__ == "__main__":\n    loop = asyncio.get_event_loop()\n    loop.run_until_complete(main())\n```\n\n### Run it\n\n```console\n$ python hello.py\n{\'name\': \'Greg\'}\n{\'name\': \'Greg\', \'greeting\': \'Hello, Greg!\'}\n```\n\n## Backends\n\nFastMicro supports the following backends:\n\n* <a href="https://pypi.org/project/aiokafka/" class="external-link" target="_blank">Kafka</a>\n* <a href="https://pypi.org/project/aioredis/" class="external-link" target="_blank">Redis</a>\n\nTo install FastMicro with one of these backends run one of the following:\n\n<div class="termy">\n\n```console\n$ pip install fastmicro[kafka]\n$ pip install fastmicro[redis]\n```\n\n## Another Example\n\nThis example shows how to use the Redis backend for inter-process communication.\n\n### Create it\n\n* Create a file `example.py` with:\n\n```Python\n#!/usr/bin/env python3\n\nfrom pydantic import BaseModel\n\nfrom fastmicro.messaging.redis import Messaging, Topic\nfrom fastmicro.service import Service\n\n\nclass User(BaseModel):\n    name: str\n\n\nclass Greeting(BaseModel):\n    name: str\n    greeting: str\n\n\nmessaging: Messaging = Messaging()\nservice = Service("test", messaging)\nuser_topic = Topic("user", messaging, User)\ngreeting_topic = Topic("greeting", messaging, Greeting)\n\n\n@service.entrypoint(user_topic, greeting_topic)\nasync def greet(user: User) -> Greeting:\n    print(user)\n    greeting = Greeting(name=user.name, greeting=f"Hello, {user.name}!")\n    print(greeting)\n    return greeting\n\n\nif __name__ == "__main__":\n    service.run()\n```\n\n* Create a file `test.py` with:\n\n```python\n#!/usr/bin/env python3\n\nimport asyncio\nfrom pydantic import BaseModel\n\nfrom fastmicro.messaging.redis import Messaging, Topic\nfrom fastmicro.service import Service\n\n\nclass User(BaseModel):\n    name: str\n\n\nclass Greeting(BaseModel):\n    name: str\n    greeting: str\n\n\nmessaging: Messaging = Messaging()\nservice = Service("test", messaging)\nuser_topic = Topic("user", messaging, User)\ngreeting_topic = Topic("greeting", messaging, Greeting)\n\n\n@service.entrypoint(user_topic, greeting_topic)\nasync def greet(user: User) -> Greeting:\n    ...\n\n\nasync def main() -> None:\n    async with messaging:\n        user = User(name="Greg")\n        print(user)\n        greeting = await greet.call(user)\n        print(greeting)\n\n\nif __name__ == "__main__":\n    loop = asyncio.get_event_loop()\n    loop.run_until_complete(main())\n```\n\n### Run it\n\n* In a terminal run:\n\n<div class="termy">\n\n```console\n$ python example.py\n{\'name\': \'Greg\'}\n{\'name\': \'Greg\', \'greeting\': \'Hello, Greg!\'}\n^C\n```\n\n* In another terminal run:\n\n<div class="termy">\n\n```console\n$ python test.py\n{\'name\': \'Greg\'}\n{\'name\': \'Greg\', \'greeting\': \'Hello, Greg!\'}\n```\n\n</div>\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'larmoreg',
    'author_email': 'larmoreg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/larmoreg/fastmicro',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
