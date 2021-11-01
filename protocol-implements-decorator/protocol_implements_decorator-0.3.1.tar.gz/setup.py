# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['protocol_implements_decorator']

package_data = \
{'': ['*'],
 'protocol_implements_decorator': ['.mypy_cache/*',
                                   '.mypy_cache/3.10/*',
                                   '.mypy_cache/3.10/_typeshed/*',
                                   '.mypy_cache/3.10/collections/*',
                                   '.mypy_cache/3.10/importlib/*',
                                   '.mypy_cache/3.10/os/*',
                                   '.mypy_cache/3.10/protocol_implements_decorator/*']}

setup_kwargs = {
    'name': 'protocol-implements-decorator',
    'version': '0.3.1',
    'description': "Adds '@implements' decorator to aid in explicit use of protocols.",
    'long_description': '# protocol_implements_decorator\n\nAdds the "implements" decorator to make using protocols easier and more explicit\n\n\n## Description\n\nAdds the @implements decorator.\nThis will cause a runtime NotImplementedError if the class does not implement all parts of the protocol.\nAlso adds the get_protocols_implemented method to the class providing a list of all protocols the decorated class adhears to.\n\nUsage:\n---\nTwo example protocols\n\n```python\nclass Printable(Protocol):\n  """A test protocol that requires a to_string method."""\n  \n  def to_string(self) -> str:\n    return ""\n\nclass Otherable(Protocol):\n  """Another example."""\n\n  def other(self) -> str:\n    return "\n```\n\n---\nExample of one protocol\n\n```python\n@implements(Printable)\nclass Example2:\n\n  def to_string(self) -> str:\n    return str(self)\n```\n\nFor multiple protocols you can chain dectorator or include in a list in one dectorator\n```python\n@implements(Printable)\n@implements(Otherable)\nclass Example1:\n  """Test class that uses multiple protocols."""\n\n  def to_string(self) -> str:\n    return str(self)\n\n  def other(self) -> str:\n    return str(self)\n\n\n@implements(Printable, Otherable)\nclass Example2:\n  """Test class that uses multiple protocols."""\n\n  def to_string(self) -> str:\n    return str(self)\n\n  def other(self) -> str:\n    return str(self)\n```\n\nErrors\n---\nThis will cause a runtime error as it doesn\'t implement the Printable protocol\n\n```python\n@implements(Printable, Otherable)\nclass Example2:\n  """Test class that uses multiple protocols."""\n\n  def other(self) -> str:\n    return str(self)\n```\n```text\nNotImplementedError: test.<locals>.Printable requires implentation of [\'to_string\']\n```\n\n\n\n<!-- pyscaffold-notes -->\n\n## Note\n\nThis project has been set up using PyScaffold 4.1.1. For details and usage\ninformation on PyScaffold see https://pyscaffold.org/.\n',
    'author': 'rbroderi',
    'author_email': 'richard@sanguinesoftware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
