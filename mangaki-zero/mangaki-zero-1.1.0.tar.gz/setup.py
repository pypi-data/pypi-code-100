# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zero', 'zero.tests']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20,<2.0',
 'pandas>=1.3,<1.3.4',
 'scikit-learn>=1.0,<2.0',
 'scipy>=1.4,<2.0']

extras_require = \
{'deep': ['tensorflow'], 'external': ['surprise'], 'fm': ['fastFM', 'pywFM']}

setup_kwargs = {
    'name': 'mangaki-zero',
    'version': '1.1.0',
    'description': "Mangaki's recommandation algorithms",
    'long_description': "# Zero\n\n[![Mangaki Zero's CI status](https://github.com/mangaki/zero/workflows/CI/badge.svg)](https://github.com/mangaki/zero/actions)\n[![Mangaki Zero's code coverage](https://codecov.io/gh/mangaki/zero/branch/master/graph/badge.svg)](https://codecov.io/gh/mangaki/zero)\n\nMangaki's recommendation algorithms.\n\nThey are tested on Python 3.6, 3.7, 3.8 over OpenBLAS LP64 & MKL.\n\n## Install\n\n    python -m venv venv\n\tsource venv/bin/activate\n\tpip install -r requirements.txt\n\n## Usage\n\nTo run cross-validation:\n\n1. Download a dataset like [Movielens 100k](http://files.grouplens.org/datasets/movielens/ml-latest-small.zip).\n2. Ensure the columns are named `user,item,rating`:\n\nuser | item | rating\n--- | --- | ---\n3 | 5 | 4.5\n\nFor example, here, user 3 gave 4.5 stars to item 5.\n\n3. Then run:\n\n    python compare.py <path/to/dataset>\n\nYou can tweak the `experiments/default.json` file to compare other models.\n\n## Custom usage\n\nMost models have the following routines:\n\n    from zero.als import MangakiALS\n    model = MangakiALS(nb_components=10)\n    model.fit(X, y)\n    model.predict(X)\n\nwhere:\n\n- *X* is a numpy array of size `nb_samples` x 2\n(first column: user ID, second column: item ID)\n- and *y* is the column of ratings.\n\nThere are a couple of other methods that can be used for online fit, say `model.predict_single_user(work_ids, user_parameters)`.\n\nSee [zero.py](zero/zero.py) as an example of dumb baseline (only predicts zeroes) to start from.\n\n## Results\n\n### Mangaki data\n\n![Comparing on Mangaki](results/mangaki.png)\n\n### Movielens data\n\n![Comparing on Movielens](results/movielens.png)\n\nFeel free to use. Under MIT license.\n",
    'author': 'Jill-Jênn Vie',
    'author_email': 'vie@jill-jenn.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://research.mangaki.fr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1',
}


setup(**setup_kwargs)
