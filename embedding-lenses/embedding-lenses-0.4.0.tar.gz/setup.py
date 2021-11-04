# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['embedding_lenses']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.10b0,<22.0',
 'bokeh==2.2.2',
 'datasets==1.14.0',
 'flake8>=4.0.1,<5.0.0',
 'huggingface-hub==0.0.19',
 'numba>=0.54.1,<0.55.0',
 'numpy==1.20.0',
 'scikit-learn==0.24.2',
 'sentence-transformers==2.0.0',
 'streamlit==1.1.0',
 'transformers==4.11.3',
 'umap-learn>=0.5.2,<0.6.0',
 'watchdog==2.1.3']

setup_kwargs = {
    'name': 'embedding-lenses',
    'version': '0.4.0',
    'description': '',
    'long_description': None,
    'author': 'edugp',
    'author_email': 'edugp91@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.9,<3.10',
}


setup(**setup_kwargs)
