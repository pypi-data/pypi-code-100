# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioalfacrm', 'aioalfacrm.core', 'aioalfacrm.objects']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.0,<4.0.0']

setup_kwargs = {
    'name': 'aioalfacrm',
    'version': '0.0.7',
    'description': 'Is an asynchronous implementation for AlfaCRM API',
    'long_description': '# AIOAlfacrm\n\n[![PyPi Package Version](https://img.shields.io/pypi/v/aioalfacrm.svg?style=flat-square)](https://pypi.python.org/pypi/aioalfacrm)\n[![Supported python versions](https://img.shields.io/pypi/pyversions/aioalfacrm.svg?style=flat-square)](https://pypi.python.org/pypi/aioalfacrm)\n[![MIT License](https://img.shields.io/pypi/l/aioalfacrm.svg?style=flat-blue)](https://opensource.org/licenses/MIT)\n[![Downloads](https://img.shields.io/pypi/dm/aioalfacrm.svg?style=flat-square)](https://pypi.python.org/pypi/aioalfacrm)\n\n**aioalfacrm** - is an asynchronous implementation for the [AlfaCRM API](https://alfacrm.pro/rest-api)\n\n## Package is in development\n\n## Installation using pip\n```\n$ pip install aioalfacrm\n```\n\n*Example:*\n\n```python\nimport asyncio\nfrom aioalfacrm import AlfaClient\n\nHOSTNAME = \'demo.s20.online\'\nEMAIL = \'api-email@email.example\'\nAPI_KEY = \'user-api-token\'\nBRANCH_ID = 1\n\n\nasync def main():\n    alfa_client = AlfaClient(\n        hostname=HOSTNAME,\n        email=EMAIL,\n        api_key=API_KEY,\n        branch_id=BRANCH_ID,\n    )\n    try:\n        # Check auth (Optionaly)\n        if not await alfa_client.check_auth():\n            print("Authentification error")\n            return\n        # Get branches\n        branches = await alfa_client.branch.list(page=0, count=20)\n    finally:\n        await alfa_client.close()\n\n\nasyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # For Windows\nasyncio.run(main())\n\n\n```\n\n## Available CRM objects\n\n```python\nalfa_client.branch  # Branch\nalfa_client.customer  # Customer\nalfa_client.location  # Location\nalfa_client.study_status  # StudyStatus\nalfa_client.subject  # Subject\nalfa_client.lead_status  # LeadStatus\nalfa_client.lead_source  # LeadSource\n```\n\n## Available CRM methods\n\n```python\nalfa_client.<object>.list(**filters)  # Get objects list\nalfa_client.<object>.get(id)  # Get one object by id\nalfa_client.<object>.create(fields)  # Create object\nalfa_client.<object>.update(id, fields)  # Update object\n```\n\n## Paginator\n```python\n# Get all objects\nfor page in alfa_client.<object>.get_paginator():\n    objects = page.items\n```',
    'author': 'Stanislav Rush',
    'author_email': '911rush@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stas12312/aioalfacrm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
