# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clidantic']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'clidantic',
    'version': '0.0.1',
    'description': 'Elegant CLI applications using Click and Pydantic',
    'long_description': '# clidantic\nElegant CLIs merging Click and Pydantic\n> WARNING: Library in early alpha stage\n\n## Install\nYou can install this package via pip, getting the latest features through GitHub:\n```\npip install git+https://github.com/edornd/clidantic.git\n```\nOr installing the latest release:\n```\npip install clidantic\n```\n\n# Quickstart\nHere\'s a quick example:\n```python\nfrom typing import Optional\nfrom pydantic import BaseModel\n\nfrom clidantic import Parser\n\n\nclass Arguments(BaseModel):\n    field_a: str\n    field_b: int\n    field_c: Optional[bool] = False\n\n\ncli = Parser()\n\n\n@cli.command()\ndef main(args: Arguments):\n    print(args)\n\n\nif __name__ == "__main__":\n    cli()\n```\n\n\n## Contributing\nWe are not quite there yet :)\n',
    'author': 'Edoardo Arnaudo',
    'author_email': 'edoardo.arn@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/edornd/clidantic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
