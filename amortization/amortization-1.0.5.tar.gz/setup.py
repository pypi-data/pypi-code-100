# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amortization']

package_data = \
{'': ['*']}

install_requires = \
['tabulate>=0.8.6,<0.9.0']

entry_points = \
{'console_scripts': ['amortize = amortization.amortize:main']}

setup_kwargs = {
    'name': 'amortization',
    'version': '1.0.5',
    'description': 'Python library for calculating amortizations and generating amortization schedules',
    'long_description': '# amortization\n\nPython library for calculating amortizations and generating amortization schedules\n<table>\n    <tr>\n        <td>License</td>\n        <td><img src=\'https://img.shields.io/pypi/l/amortization.svg\' alt="License"></td>\n        <td>Version</td>\n        <td><img src=\'https://img.shields.io/pypi/v/amortization.svg\' alt="Version"></td>\n    </tr>\n    <tr>\n        <td>Github Actions</td>\n        <td><img src=\'https://github.com/roniemartinez/amortization/actions/workflows/python.yml/badge.svg\' alt="Github Actions"></td>\n        <td>Coverage</td>\n        <td><img src=\'https://codecov.io/gh/roniemartinez/amortization/branch/master/graph/badge.svg\'></td>\n    </tr>\n    <tr>\n        <td>Supported versions</td>\n        <td><img src=\'https://img.shields.io/pypi/pyversions/amortization.svg\' alt="Python Versions"></td>\n        <td>Wheel</td>\n        <td><img src=\'https://img.shields.io/pypi/wheel/amortization.svg\' alt="Wheel"></td>\n    </tr>\n    <tr>\n        <td>Status</td>\n        <td><img src=\'https://img.shields.io/pypi/status/amortization.svg\' alt="Status"></td>\n        <td>Downloads</td>\n        <td><img src=\'https://img.shields.io/pypi/dm/amortization.svg\' alt="Downloads"></td>\n    </tr>\n</table>\n\n## Support\nIf you like `amortization` or if it is useful to you, show your support by buying me a coffee.\n\n<a href="https://www.buymeacoffee.com/roniemartinez" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>\n\n## Installation\n\n```bash\npip install amortization\n```\n\n## Usage\n\n### Python\n\n#### Amortization Amount\n\n```python\nfrom amortization.amount import calculate_amortization_amount\n\namount = calculate_amortization_amount(150000, 0.1, 36)\n```\n\n### Amortization Schedule\n\n```python\nfrom amortization.schedule import amortization_schedule\n\nfor number, amount, interest, principal, balance in amortization_schedule(150000, 0.1, 36):\n    print(number, amount, interest, principal, balance)\n```\n\n### Amortization Schedule (using tabulate)\n\n```python\nfrom amortization.schedule import amortization_schedule\nfrom tabulate import tabulate\n\ntable = (x for x in amortization_schedule(150000, 0.1, 36))\nprint(\n    tabulate(\n        table,\n        headers=["Number", "Amount", "Interest", "Principal", "Balance"],\n        floatfmt=",.2f",\n        numalign="right"\n    )\n)\n```\n\n### Command line\n\n```bash\namortize -h\nusage: amortize [-h] -P PRINCIPAL -n PERIOD -r INTEREST_RATE [-s]\n\nPython library for calculating amortizations and generating amortization\nschedules\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -s, --schedule        Generate amortization schedule\n\nrequired arguments:\n  -P PRINCIPAL, --principal PRINCIPAL\n                        Principal amount\n  -n PERIOD, --period PERIOD\n                        Total number of periods\n  -r INTEREST_RATE, --interest-rate INTEREST_RATE\n                        Interest rate per period\n```\n\n```bash\namortize -P 150000 -n 36 -r 0.1 -s\n```\n\n## Dependencies\n\n[tabulate](https://bitbucket.org/astanin/python-tabulate)\n\n## Author\n\n[Ronie Martinez](mailto:ronmarti18@gmail.com)\n\n## References\n\n- [Packaging and distributing projects](https://packaging.python.org/guides/distributing-packages-using-setuptools/)\n- [Using TestPyPI](https://packaging.python.org/guides/using-testpypi/)\n',
    'author': 'Ronie Martinez',
    'author_email': 'ronmarti18@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/roniemartinez/amortization',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4',
}


setup(**setup_kwargs)
