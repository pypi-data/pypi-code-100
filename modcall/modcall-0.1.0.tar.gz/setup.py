# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['modcall']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'modcall',
    'version': '0.1.0',
    'description': 'Create callable modules',
    'long_description': "# modcall\nCreate callable modules\n\n## Usage\n**lib.py**\n```python\nimport modcall\n\ndef hello(name: str) -> None:\n    print(f'Hello, {name}!')\n\nmodcall(__name__, hello)\n```\n\n**app.py**\n```python\nimport lib\n\nlib('World')\n```\n",
    'author': 'Tom Bulled',
    'author_email': '26026015+tombulled@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tombulled/modcall',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
