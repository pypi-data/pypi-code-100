# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rasam', 'rasam.components', 'rasam.importers']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=8.1.4,<9.0.0', 'rasa>=2.6.1,<3.0.0', 'urlextract>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'rasam',
    'version': '0.4.1',
    'description': 'Rasa Improved',
    'long_description': '# rasam\n\nRasa Improved\n\n<table>\n    <tr>\n        <td>License</td>\n        <td><img src=\'https://img.shields.io/pypi/l/rasam.svg\' alt="License"></td>\n        <td>Version</td>\n        <td><img src=\'https://img.shields.io/pypi/v/rasam.svg\' alt="Version"></td>\n    </tr>\n    <tr>\n        <td>Github Actions</td>\n        <td><img src=\'https://github.com/roniemartinez/rasam/actions/workflows/python.yml/badge.svg\' alt="Github Actions"></td>\n        <td>Coverage</td>\n        <td><img src=\'https://codecov.io/gh/roniemartinez/rasam/branch/master/graph/badge.svg\' alt="CodeCov"></td>\n    </tr>\n    <tr>\n        <td>Supported versions</td>\n        <td><img src=\'https://img.shields.io/pypi/pyversions/rasam.svg\' alt="Python Versions"></td>\n        <td>Wheel</td>\n        <td><img src=\'https://img.shields.io/pypi/wheel/rasam.svg\' alt="Wheel"></td>\n    </tr>\n    <tr>\n        <td>Status</td>\n        <td><img src=\'https://img.shields.io/pypi/status/rasam.svg\' alt="Status"></td>\n        <td>Downloads</td>\n        <td><img src=\'https://img.shields.io/pypi/dm/rasam.svg\' alt="Downloads"></td>\n    </tr>\n</table>\n\n## Support\nIf you like `rasam` or if it is useful to you, show your support by buying me a coffee.\n\n<a href="https://www.buymeacoffee.com/roniemartinez" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>\n\n## Usage\n\n### Installation\n\n```bash\npip install rasam\n```\n\n### Rasa `config.yml`\n\n```yaml\nimporters:\n  - name: rasam.PlaceholderImporter\n    fake_data_count: 10  # default value is 1\n\npipeline:\n  - name: rasam.RegexEntityExtractor\n  - name: rasam.URLEntityExtractor\n```\n\n### Rasa `nlu.yml`\n\n#### PlaceholderImporter\n\nThe `PlaceholderImporter` removes the need to write unnecessary information (eg. name, address, numbers, etc.) and helps focus on writing test data.\n\n#### Using `{}` placeholder\n\n```yaml\nnlu:\n- intent: tell_name\n  examples: |\n    - My name is {name}\n    - I am {name} and he is {name}\n```\n\n#### Using `@` placeholder\n\n```yaml\nnlu:\n- intent: tell_address\n  examples: |\n    - I live in @address\n    - I stay at @address and @address\n```\n\n#### Mixing `{}` and `@` placeholders\n\nIt is possible to mix both `{}` and `@` placeholders but it is recommended to use only one style for consistency.\n\n#### Available placeholders\n\n- any (if you need just any data)    \n- integer    \n- decimal    \n- number     \n- name       \n- first_name \n- last_name  \n- text       \n- word       \n- paragraph  \n- uri        \n- url        \n- local_uri  \n- email      \n- date         \n- time         \n- month        \n- day          \n- timezone     \n- company      \n- license_plate\n- address\n- city\n- country\n- user_agent\n- password\n- user_name\n- file_path\n\n### Rasam decorators\n\nRasa relies too heavily on classes to define objects like actions, forms, etc. \nRasam aims to remove these Rasa boilerplates to make writing chatbots easier.\n\n#### @action decorator\n\nThe `@action` decorator converts function into an Action class. \nHere is an example of how we can write custom classes in Rasa:\n\n```python\nclass ActionHelloWorld(Action):\n\n    def name(self) -> Text:\n        return "action_hello_world"\n\n    def run(self, dispatcher: CollectingDispatcher,\n            tracker: Tracker,\n            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:\n\n        dispatcher.utter_message(text="Hello World!")\n\n        return []\n\n```\n\nThe above code can be simplified using Rasam\'s `@action` decorator.\n\n```python\nfrom rasam import action\n\n\n@action\ndef action_hello_world(\n    self: Action, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]\n) -> List[Dict[Text, Any]]:\n    dispatcher.utter_message(text="Hello World!")\n    return []\n```\n\n\n\n## Author\n[Ronie Martinez](ronmarti18@gmail.com) \n',
    'author': 'Ronie Martinez',
    'author_email': 'ronmarti18@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/roniemartinez/rasam',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<3.9',
}


setup(**setup_kwargs)
