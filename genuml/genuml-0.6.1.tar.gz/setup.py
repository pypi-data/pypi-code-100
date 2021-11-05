# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['genuml']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['genuml = genuml.genuml:app']}

setup_kwargs = {
    'name': 'genuml',
    'version': '0.6.1',
    'description': 'Generate PlantUML diagram code from Java class files',
    'long_description': '# GenUML - Generate PlantUML from Java class files\n\n[![PyPI Version](https://badge.fury.io/py/genuml.svg)](https://badge.fury.io/py/genuml)\n[![Build Status](https://github.com/samuller/genuml/workflows/test/badge.svg)](https://github.com/samuller/genuml/actions)\n[![Code Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/samuller/c2a6dcd467afe62785c828a40acc96d8/raw/genuml-badge-coverage.json)](https://github.com/samuller/genuml/actions)\n\nThis tool aids in creating [PlantUML](https://plantuml.com/) class diagrams by generating UML diagrams from Java class files. Diagrams can be generated from single class files, or generated diagrams can be inserted into PlantUML code based on comments containing the correct "pattern".\n\n```console\n$ genuml --help\nUsage: genuml [OPTIONS] COMMAND [ARGS]...\n\n  Generate PlantUML class diagram DSL from Java class files.\n\nOptions:\n  --version\n  --help     Show this message and exit.\n\nCommands:\n  generate  Generate PlantUML for single given Java class file.\n  insert    Insert diagrams into PlantUML containing pattern comments.\n```\n\nSome functionality, as well as the generated diagram style, are based on [ObjectAid UML Explorer](https://marketplace.eclipse.org/content/objectaid-uml-explorer), an Eclipse plug-in which seems to no longer be supported.\n\n## Example usage\n\n```console\ngenuml insert --class-dir "WEB-INF/classes" plantuml-diagram.puml \\\n    | java -jar plantuml.jar -pipe > diagram.png\n```\n\nSome explanation:\n\n- Compiled classes are found in `WEB-INF/classes`.\n- `plantuml-diagram.puml` contains PlantUML code as well as "pattern" comments referencing specific classes contained in the given folders (see [example](tests/data/diagram.puml)).\n  - This file will be processed with the generated diagrams being placed directly after their pattern comments. Transformed output will be printed to stdout (and in this example, piped directly to PlantUML).\n- `plantuml.jar` has been downloaded to the local folder.\n\n### Example PlantUML with pattern comments\n\n```plantuml\n@startuml\nskinparam linetype polyline\n\n\' Pattern comments that will be processed by GenUML:\n\'!gen_java tests.data.ExampleClass\n\'!gen_java tests.data.ExampleAbstract\n\'!gen_java tests.data.ExampleInterface\n\'!gen_java tests.data.ExampleEnum: LOW HIGH\n\nExampleInterface *-- ExampleClass : implements\nExampleClass .> "0..1" ExampleEnum\nExampleClass -> ExampleAbstract\n\n@enduml\n```\n\nwhich could then be used to generate this diagram:\n\n![PlantUML class diagram](https://raw.githubusercontent.com/samuller/genuml/main/tests/data/diagram.png)\n\n## Installation\n\n### Install from PyPI\n\nWith `Python 3` installed on your system, you can run:\n\n```console\npip install genuml\n```\n\nTo test that installation worked, run:\n\n```console\ngenuml --help\n```\n\nand you can uninstall at any time with:\n\n```console\npip uninstall genuml\n```\n\n### Install from Github\n\nTo install the newest code directly from Github:\n\n```console\npip install git+https://github.com/samuller/genuml\n```\n\nAnd uninstall remains the same:\n\n```console\npip uninstall genuml\n```\n',
    'author': 'Simon Muller',
    'author_email': 'samullers@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/samuller/genuml',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
