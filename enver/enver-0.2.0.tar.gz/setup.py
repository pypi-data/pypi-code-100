# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['enver']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'enver',
    'version': '0.2.0',
    'description': 'Organize your config and environment variables',
    'long_description': '# enver\n\nEnver is a simple config / environment helper.\n\n[![Test And Lint](https://github.com/danhje/enver/actions/workflows/python-test.yml/badge.svg)](https://github.com/danhje/enver/actions/workflows/python-test.yml)\n[![codecov](https://codecov.io/gh/danhje/enver/branch/master/graph/badge.svg)](https://codecov.io/gh/danhje/enver)\n![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/danhje/enver?include_prereleases)\n![PyPI](https://img.shields.io/pypi/v/enver)\n\nCollect all your config values and environment variables in a single location, so new contributors knows what variables must be\n  set, and don\'t have to go searching for `os.environ` or `os.getenv` scattered throughout the code.\n\nFeatures:\n- Automatic validation of environment variables.\n- Automatic casting to desired data type using Pydantic.\n- Optional default values.\n- Fails fast if a variable has no value (either default or override).\n- Allows lookup using dot notation, e.g. `env.DB_PASSWORD`, as well as subscript (`env[\'DB_PASSWORD\']`) or the `get()` method `env.get(\'DB_PASSWORD\')`.\n\n## Installation\n\n```\npip install enver\n```\n\n## Usage\n\nCreate a class that inherits from Enver, with config variables as class attributes. Putting this class in a separate config.py file might be a good idea, but is not necessary.\n\n\n```python\n# config.py\n\nfrom enver import Enver\nfrom typing import Optional, List, Dict\n\nclass Config(Enver):\n    MY_DB_HOST: str = "127.0.0.1"\n    MY_DB_USER: str = "user"\n    MY_DB_PASSWORD: str  # No default value, will be supplied as environment value.\n    THIS_VAL_MIGHT_NOT_EXIST_IN_ENV: Optional[str]\n    PI: float  # Read from env and converted to float, if possible.\n    ENABLE_LOGGING: bool = True\n    LOCATIONS: List[str] = ["/opt", "/etc"]\n    MAPPING: Dict[str, float]\n```\n\nIf environment values with the same name as any of the attributes exist, those will be used, overriding any defaults. Values will be converted to the specified type. If conversion is not possible, an exception is thrown.\n\nHere\'s how to use the values:\n\n```python\n# service.py\n\nfrom .config import Config\n\nenv = Config()\n\nuser = env.MY_DB_USER\npassword = env.MY_DB_PASSWORD\n\nif env.exists(\'FEATURE_1\'):\n  feature_1()\n\nall_values = env.all()\n```\n\nThe `Enver` class and any derived classes are singletons, meaning they always return the same instance:\n\n```python\nenv1 = Config()\nenv2 = Config()\nassert env1 is env2\n```\n\nWhich means this is fine:\n\n````python\nuser = Config().MY_DB_USER\npassword = Config().MY_DB_PASSWORD\n````\n\n## Development\n\nDependencies for the project are managed with poetry.\nTo install all dependencies run:\n\n```shell\npoetry install\n```\n\nTo install pre-commit and set up its git hooks:\n```\npip install pre-commit\npre-commit install\n```\nNow pre-commit will run automatically on every commit.\n',
    'author': 'Daniel Hjertholm',
    'author_email': 'daniel.hjertholm@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
