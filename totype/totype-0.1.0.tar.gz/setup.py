# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['totype']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'totype',
    'version': '0.1.0',
    'description': 'Data converter',
    'long_description': '# Data converter\n\n\n## Install\n    poetry add totype\n\nor\n\n    pip install totype\n\n## Examples\n\n### Transform value\n\n```python\nfrom totype.fields import Field\n\nvalue = "1"\n\nfield = Field(\n    transform_funcs=[\n        int, \n        lambda x: x * 100,\n        str\n    ]\n)\nvalid, new_value = field(value)\n\nassert valid\nassert new_value == "100"\n```\n\n\n### Transform rows\n```python\nimport datetime as dt\nfrom totype import fields, RowTransform\n\n\ntransform = RowTransform(\n    fields=[\n        fields.TextField(),\n        fields.IntField(),\n        fields.UIntField(),\n        fields.FloatField(),\n        fields.ArrayField(),\n        fields.JSONField(),\n        fields.DateTimeField(),\n        fields.DateField(),\n    ],\n    skip_error_rows=False,\n    store_rows_with_errors=False,\n)\nnewrow = transform(\n    (1, "20", "-100", "500", "[[100]]", \'{"100": 100}\', "2021-01-01", "2021-01-01")\n)\nassert newrow == ("1", 20, 0, 500.0, [[100]], {"100": 100}, dt.datetime(2021,1,1), dt.date(2021,1,1))\n```',
    'author': 'Pavel Maksimov',
    'author_email': 'vur21@ya.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pavelmaksimov/totype',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
