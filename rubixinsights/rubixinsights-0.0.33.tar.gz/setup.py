# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rubixinsights', 'rubixinsights.adverity']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.0,<3.0.0',
 'PyYAML==5.3.1',
 'SQLAlchemy==1.3.23',
 'boto3==1.17.29',
 'google-api-core==1.26.0',
 'google-api-python-client==1.12.8',
 'google-auth-httplib2==0.0.4',
 'google-auth-oauthlib==0.4.2',
 'googleapis-common-protos==1.52.0',
 'loguru>=0.5.3,<0.6.0',
 'pandas==1.2.0',
 'psycopg2-binary==2.8.6',
 'requests==2.25.1']

setup_kwargs = {
    'name': 'rubixinsights',
    'version': '0.0.33',
    'description': 'rubixin-sights',
    'long_description': '# insights-helper-functions\nHelper and Utility Functions\n',
    'author': 'rubix',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4',
}


setup(**setup_kwargs)
