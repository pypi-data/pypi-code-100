# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyonize']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['realpython = pyonize.__main__:main']}

setup_kwargs = {
    'name': 'pyonize',
    'version': '0.1.2.1',
    'description': 'convert json|dict to python object',
    'long_description': '# Pyonize\n\nconvert json|dict to python object\n\n## Setup\n\n```\npip install pyonize\n```\n\n## Example\n```py\nfrom pyonize import pyonize\n\n\ndef example():\n    \n    deneme = pyonize({"id":1,"name":"bilal","job":{"id":1,"title":"CTO"}})\n\n    print(type(deneme))\n    print(deneme.name)\n    print(deneme.job)\n    print(deneme.job.title)\n\nexample()\n```\n\n<br>\n<hr>\n\n',
    'author': 'Bilal Alpaslan',
    'author_email': 'm.bilal.alpaslan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BilalAlpaslan/Pyonize',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
