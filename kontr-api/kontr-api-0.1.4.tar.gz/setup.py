# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kontr_api', 'kontr_api.resources']

package_data = \
{'': ['*']}

install_requires = \
['pyjwt', 'requests']

setup_kwargs = {
    'name': 'kontr-api',
    'version': '0.1.4',
    'description': 'Kontr Portal REST Api Client',
    'long_description': "# Kontr Portal REST API Client\n\nKontr Portal REST API Client is the Portal REST API wrapper over the resources in the portal.\nIt supports CRUD operations and simple management over entities.\n\nKontr 2 is the project created on FI MUNI to test and execute students solutions for programming assignments.\n\n## Setup\n\nInstall and update using the pip:\n\n```bash\n$ pip install kontr-api\n```\n\n## Simple examples\n\nSimple examples how to configure and user the API Client.\n\nExample how to manage the users.\n\n```python\nfrom kontr_api import KontrClient\n\nportal_url='https://localhost'\nusername='admin'\npassword='123456'\n\nkontr_client = KontrClient(url=portal_url, username=username, password=password)\n\n# List all users\nkontr_client.users.list()\n\n# Create new user\nkontr_client.users.create(username='xlogin', name='Test user', uco='123456')\n\n# Get user\nuser = kontr_client.users.get('xlogin')\n\n# Update user's name\nuser['name'] = 'new name'\nuser.update() # or use the kontr_client.users.update({ 'name': 'new name' }, 'xlogin')\n\n# Set user's password\nuser.set_password('Password.123')\n\n# Delete the user\nuser.delete() # or use the kontr_client.users.delete('xlogin')\n```\n\n## Contributing\n\nTake a look at the [contribution guide](https://gitlab.fi.muni.cz/grp-kontr2/kontr-documentation/blob/master/contributing/GeneralContributionGuide.adoc).",
    'author': 'Peter Stanko',
    'author_email': 'stanko@mail.muni.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.fi.muni.cz/grp-kontr2/kontr-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
