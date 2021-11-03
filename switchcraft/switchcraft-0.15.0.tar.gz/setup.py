# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['switchcraft',
 'switchcraft.clients',
 'switchcraft.conversion',
 'switchcraft.conversion.arnparse',
 'switchcraft.data_classes']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.16.3,<2.0.0', 'pydantic>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'switchcraft',
    'version': '0.15.0',
    'description': 'Client wrappers and helpful utilities to solve common coding challenges in AWS',
    'long_description': "# Switchcraft\n\n![logo](./assets/logo/cover-800X600.jpg)\n\n> ⚠️ Warning: this library is under active development and may take time to reach as stable `v1.0` release.\n\nSwitchcraft is a Python library that provides light-weight AWS clients, common patterns, and helper functions that ease development of AWS applications.\n\n## Installation\n\nSwitchcraft is available as a Python package.\n\n```bash\npip install switchcraft\n```\n\n## Examples\n\n### Access ARN elements as objects\n\n```python\nfrom switchcraft.conversion import Arn\n\narn = 'arn:aws:clouddirectory:us-west-2:12345678910:schema/published/cognito/1.0'\narn_elements = Arn(arn)\n\nprint(arn_elements.account_id)\n#> 12345678910\n\nprint(arn_elements.region)\n#> us-west-2\n \n```\n\n### Convert Parameters to Python dictionaries\n\n```python\nfrom switchcraft.conversion import param_list_to_dict\n\nparams = [{'Key': 'hello', 'Value': 'world'}, {'Key': 'hi', 'Value': 'there'}]\nparams_dict = param_list_to_dict(params)\n\nprint(params_dict)\n#> {'hello': 'world', 'hi': 'there'}\n\nhello = params_dict.get('hello')\nprint(hello)\n#> world\n\n```\n\n## Versioning\n\nWe use [SemVer](http://semver.org/) for versioning.\n\n## Author(s)\n\n- **Derek Sudduth (AWS)**\n",
    'author': 'WWPS ProServe',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
