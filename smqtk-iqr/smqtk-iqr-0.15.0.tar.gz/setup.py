# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smqtk_iqr',
 'smqtk_iqr.iqr',
 'smqtk_iqr.utils',
 'smqtk_iqr.web',
 'smqtk_iqr.web.iqr_service',
 'smqtk_iqr.web.search_app',
 'smqtk_iqr.web.search_app.modules',
 'smqtk_iqr.web.search_app.modules.file_upload',
 'smqtk_iqr.web.search_app.modules.iqr',
 'smqtk_iqr.web.search_app.modules.login']

package_data = \
{'': ['*'],
 'smqtk_iqr.web.search_app': ['sample_configs/*',
                              'static/css/*',
                              'static/css/images/*',
                              'static/img/*',
                              'static/js/*',
                              'templates/*'],
 'smqtk_iqr.web.search_app.modules.file_upload': ['static/css/*',
                                                  'static/js/*'],
 'smqtk_iqr.web.search_app.modules.iqr': ['static/css/*',
                                          'static/img/*',
                                          'static/js/*',
                                          'templates/*'],
 'smqtk_iqr.web.search_app.modules.login': ['templates/*']}

install_requires = \
['Flask-BasicAuth>=0.2.0,<0.3.0',
 'Flask-Cors>=3.0.10,<4.0.0',
 'Flask>=2.0.1,<3.0.0',
 'Pillow>=8.3.2,<9.0.0',
 'imageio>=2.9.0,<3.0.0',
 'pymongo>=3.12.0,<4.0.0',
 'smqtk-classifier>=0.18.0',
 'smqtk-core>=0.18.0,<0.19.0',
 'smqtk-dataprovider>=0.16.0,<0.17.0',
 'smqtk-descriptors>=0.16.0,<0.17.0',
 'smqtk-indexing>=0.16.0,<0.17.0',
 'smqtk-relevancy>=0.15.0,<0.16.0']

entry_points = \
{'console_scripts': ['iqrTrainClassifier = '
                     'smqtk_iqr.utils.iqrTrainClassifier:main',
                     'iqr_app_model_generation = '
                     'smqtk_iqr.utils.iqr_app_model_generation:main',
                     'runApplication = smqtk_iqr.utils.runApplication:main'],
 'smqtk_plugins': ['smqtk_iqr.web.iqr_service.iqr_server = '
                   'smqtk_iqr.web.iqr_service.iqr_server',
                   'smqtk_iqr.web.search_app = '
                   'smqtk_iqr.web.search_app.__init__']}

setup_kwargs = {
    'name': 'smqtk-iqr',
    'version': '0.15.0',
    'description': 'IQR datastructures and web interface',
    'long_description': "# SMQTK - IQR\n\n## Intent\nThis package provides the tools and web interface for using SMQTK's IQR\nplatform.\n\n## Documentation\nYou can build the Sphinx documentation locally for the most up-tp-date\nreference:\n\n```bash\n# Install dependencies\npoetry install\n# Navigate to the documentation root.\ncd docs\n# Build the docs.\npoetry run make html\n# Open in your favorite browser!\nfirefox _build/html/index.html\n```\n",
    'author': 'Kitware, Inc.',
    'author_email': 'smqtk-developers@kitware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kitware/SMQTK-IQR',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
