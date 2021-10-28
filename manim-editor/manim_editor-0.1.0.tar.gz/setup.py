# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['manim_editor',
 'manim_editor.app',
 'manim_editor.app.error',
 'manim_editor.app.main',
 'manim_editor.editor']

package_data = \
{'': ['*'],
 'manim_editor.app': ['static/img/*', 'templates/*'],
 'manim_editor.app.error': ['templates/*'],
 'manim_editor.app.main': ['templates/*']}

install_requires = \
['Flask>=2.0.2,<3.0.0',
 'click>=8.0.3,<9.0.0',
 'jsonschema>=4.1.2,<5.0.0',
 'waitress>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['manedit = manim_editor.__main__:main']}

setup_kwargs = {
    'name': 'manim-editor',
    'version': '0.1.0',
    'description': 'Editor and Presenter for Manim Generated Content',
    'long_description': None,
    'author': 'christopher-besch',
    'author_email': 'christopher.besch@gmx.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
