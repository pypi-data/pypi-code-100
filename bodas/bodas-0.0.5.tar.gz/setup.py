# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bodas']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.3,<4.0.0', 'numpy>=1.19.5,<2.0.0', 'sympy>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'bodas',
    'version': '0.0.5',
    'description': 'Asymptotic Bode Plots in Python',
    'long_description': "# bodas\n[![Downloads](https://pepy.tech/badge/bodas)](https://pepy.tech/project/bodas)\n\nAsymptotic Bode plots in Python.\n\n![](https://github.com/urbanij/bodas/blob/main/docs/example2.png?raw=true)\n\n### Installation\n`pip install bodas`\n\n\n### Simple usage example\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/urbanij/bodas/HEAD?labpath=examples%2Fbasic.ipynb)\n\n```python\nIn [1]: import bodas \n\nIn [2]: import sympy                # import [SymPy](https://www.sympy.org) the Python \n                                    # library for symbolic mathematics\n\nIn [3]: s = sympy.Symbol('s')       # define `s` as symbol\n\nIn [4]: H = (1+s/23)/(1+s/123)**2   # assign to `H` the function you want to plot\n\nIn [5]: sympy.pretty_print(H)\n  s\n  ── + 1\n  23\n──────────\n         2\n⎛ s     ⎞\n⎜─── + 1⎟\n⎝123    ⎠\n\n\nIn [6]: bodas.plot(H)               # call the `plot` function defined in the bodas library\n```\n\n\n\n<!-- ### Todo\nSee [TODO.md](https://github.com/urbanij/bodas/blob/main/TODO.md) -->\n",
    'author': 'Francesco Urbani',
    'author_email': 'francescourbanidue@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/urbanij/bodas',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
