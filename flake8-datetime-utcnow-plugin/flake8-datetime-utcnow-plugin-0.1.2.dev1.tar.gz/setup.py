# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_datetime_utcnow']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3.0.0']

entry_points = \
{'flake8.extension': ['U1 = flake8_datetime_utcnow:DatetimeUtcnowLinter']}

setup_kwargs = {
    'name': 'flake8-datetime-utcnow-plugin',
    'version': '0.1.2.dev1',
    'description': 'Plugin to check that utcnow() is not used in favour of now(UTC)',
    'long_description': "# flake8_datetime_utcnow_plugin\n\n## Rationale\n\nPlugin for `flake8` to warn the developer of the usage of [datetime.utcnow()](https://docs.python.org/3/library/datetime.html#datetime.datetime.utcnow).\n\nThe problem with `datetme.utcnow()` is that indeed returns the current timestamp in the UTC timzone but the object is a naive `datetime`, that is doesn't have the `tzinfo` argument set.\n\nInstead [datetime.now()](https://docs.python.org/3/library/datetime.html#datetime.datetime.utcnow] should be used passing the UTC timezone:\n\n```python\nfrom datetime import datetime, timezone\n\ndatetime.now(timezone.utc)\n```\n\n## Installation\n\nTo install the plugin and `flake8`:\n\n```\npip install flake8_datetime_utcnow_plugin\n```\n",
    'author': 'Daniele Esposti',
    'author_email': 'daniele.esposti@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/expobrain/flake8-datetime-utcnow-plugin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
