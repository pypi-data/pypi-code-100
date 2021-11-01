# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['safex']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'safex',
    'version': '0.4.0',
    'description': 'Simple and safe expression evaluator',
    'long_description': '# safex\n\nSafe and simple python expression evaluator.\n\n## Installation\n\n```\npip install safex\n```\n\n## Usage\n\n```\nfrom safex import eval_expression\n\n\nassert eval_expression("1 + 2 * 12 / 3") == 9\nassert eval_expression("a + b", {"a": 1, "b": 2}) == 3\n\nassert eval_expression("not True") == False\nassert eval_expression("not False") == True\n\nassert eval_expression("1 < 2 < 3") == True\n\nassert eval_expression("a", {"a": 1}) == 1\nassert eval_expression("inc(x)", {"inc": lambda x: x + 1, "x": 1}) == 2\n\n\nassert eval_expression("[0, 1, 2, 3, 4, 5][0]") == 0\nassert eval_expression("{\'a\': 1, \'b\': 2}[\'a\']") == 1\n\nevent = {\n    \'type\': \'user_added\',\n    \'payload\': {\n        \'name\': \'test\',\n        \'age\': 17,\n        \'emails\': [\n            {\'type\': \'primary\', \'email\': \'test@test.com\'},\n            {\'type\': \'secondary\', \'email\': \'test2@test.com\'}\n        ]\n    }\n}\nassert eval_expression(\n    "event[\'type\'] == \'user_added\' and event[\'payload\'][\'age\'] < 18", {"event": event}) == True\nassert eval_expression(\n    "event[\'payload\'][\'emails\'][0][\'email\']", {"event": event}) == \'test@test.com\'\n```',
    'author': 'Rahul Kumar',
    'author_email': 'r@thoughtnirvana.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rahulkmr/safex',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
