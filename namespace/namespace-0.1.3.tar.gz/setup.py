# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['namespace']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'namespace',
    'version': '0.1.3',
    'description': 'Simple namespaces',
    'long_description': '# namespace\nSimple namespaces\n\n## Usage\n```python\n>>> import namespace\n>>>\n>>> functions = namespace()\n>>>\n>>> @functions\n>>> def foo(): pass\n>>>\n>>> functions\nNamespace(foo=<function foo at 0x7fd5d249d1f0>)\n>>>\n>>> functions.foo\n<function foo at 0x7fd5d249d1f0>\n```\n',
    'author': 'Tom Bulled',
    'author_email': '26026015+tombulled@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tombulled/namespace',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
