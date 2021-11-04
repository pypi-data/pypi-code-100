# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smqtk_relevancy',
 'smqtk_relevancy.impls',
 'smqtk_relevancy.impls.rank_relevancy',
 'smqtk_relevancy.impls.relevancy_index',
 'smqtk_relevancy.interfaces',
 'smqtk_relevancy.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.5,<2.0.0',
 'pillow>=8.2.0,<9.0.0',
 'smqtk-classifier>=0.19.0',
 'smqtk-core>=0.18.0',
 'smqtk-dataprovider>=0.16.0',
 'smqtk-indexing>=0.17.0']

entry_points = \
{'smqtk_plugins': ['smqtk_relevancy.impls.rank_relevancy.margin_sampling = '
                   'smqtk_relevancy.impls.rank_relevancy.margin_sampling',
                   'smqtk_relevancy.impls.rank_relevancy.wrap_classifier = '
                   'smqtk_relevancy.impls.rank_relevancy.wrap_classifier',
                   'smqtk_relevancy.impls.relevancy_index.classifier_wrapper = '
                   'smqtk_relevancy.impls.relevancy_index.classifier_wrapper',
                   'smqtk_relevancy.impls.relevancy_index.libsvm_hik = '
                   'smqtk_relevancy.impls.relevancy_index.libsvm_hik']}

setup_kwargs = {
    'name': 'smqtk-relevancy',
    'version': '0.16.1',
    'description': 'SMQTK Relevancy',
    'long_description': None,
    'author': 'Kitware, Inc.',
    'author_email': 'smqtk-developers@kitware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
