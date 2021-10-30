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
    'version': '0.1.1',
    'description': 'convert json|dict to python object',
    'long_description': '# Pyon\nconvert json|dict to python object\n\n\n```py\nfrom pyon import pyonize\n\n\ndef example():\n    \n    deneme = pyonize({"id":1,"name":"bilal","job":{"id":1,"title":"CTO"}})\n\n    print(type(deneme))\n    print(deneme.name)\n    print(deneme.job)\n    print(deneme.job.title)\n\nexample()\n```\n\n<br>\n<hr>\n\n# Setup\n\nthis project not available in PyPI now (coming soon). if you want add this library your workspace clone this repo and watch a this steps:\n\n### -**First**\n\nDownload wheel and setuptools libraries\n\n```\npip install wheel setuptools\n```\n\n### -**After** \n\nMake sure you are in the same folder as setup.py\n\n```\npython setup.py bdist_wheel --universal\n```\n\n### -**Finally**\n\nStay in the same directory and copy the name of the .whl file in the dist folder\n\n```\npip install ./dist/copied file name\n```\n\nActually the filename is by default: "pyon-0.1.0-py2.py3-none-any.whl"\n<hr>\n',
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
