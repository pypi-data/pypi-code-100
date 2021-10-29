# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rtmilk']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1', 'requests>=2.23.0']

extras_require = \
{':python_version >= "3.10" and python_version < "4"': ['urllib3>=1.26']}

setup_kwargs = {
    'name': 'rtmilk',
    'version': '0.0.7',
    'description': 'RTM API wrapper',
    'long_description': 'Python wrapper for "Remember the Milk" [API](https://www.rememberthemilk.com/services/api/)\n\n# Usage\n```python\nfrom rtmmilk import API, RTMError\n\napi = API(API_KEY, SHARED_SECRET, TOKEN)\n\ntimeline = api.TasksCreateTimeline().timeline\ntry:\n    api.TasksAdd(timeline, \'task name\')\nexcept RTMError as e:\n    print(e)\n```\n\n# Authorization\n```python\nfrom rtmmilk import AuthorizationSession\n\nauthenticationSession = AuthorizationSession(API_KEY, SHARED_SECRET, \'delete\')\ninput(f"Go to {authenticationSession.url} and authorize. Then Press ENTER")\ntoken = authenticationSession.Done()\nprint(f\'Authorization token is {token}\')\n```\n',
    'author': 'Rehan Khwaja',
    'author_email': 'rehan@khwaja.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rkhwaja/rtmilk',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
