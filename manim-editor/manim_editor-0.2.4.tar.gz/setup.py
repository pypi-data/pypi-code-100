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
 'manim_editor.app': ['static/img/*', 'static/webpack/*', 'templates/*'],
 'manim_editor.app.error': ['templates/*'],
 'manim_editor.app.main': ['templates/*']}

install_requires = \
['Flask>=2.0.2,<3.0.0',
 'click>=8.0.3,<9.0.0',
 'jsonschema>=4.1.2,<5.0.0',
 'waitress>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['manedit = manim_editor.__main__:main',
                     'manim_editor = manim_editor.__main__:main']}

setup_kwargs = {
    'name': 'manim-editor',
    'version': '0.2.4',
    'description': 'Editor and Presenter for Manim Generated Content',
    'long_description': '<p align="center">\n    <a href="#"><img src="https://raw.githubusercontent.com/ManimEditorProject/manim_editor/main/banner.png"></a>\n    <br />\n    <br />\n    <a href="https://pypi.org/project/manim-editor/"><img src="https://img.shields.io/pypi/v/manim-editor.svg?style=flat&logo=pypi" alt="PyPI Latest Release"></a>\n    <a href="https://manim-editor.readthedocs.io/en/stable/"><img src=\'https://readthedocs.org/projects/manim-editor/badge/?version=stable\' alt=\'Documentation Status\' /></a>\n    <a href="http://choosealicense.com/licenses/mit/"><img src="https://img.shields.io/badge/license-MIT-red.svg?style=flat" alt="MIT License"></a>\n    <a href="https://github.com/ManimEditorProject/manim_editor/actions/workflows/build_pages.yml"><img src="https://github.com/ManimEditorProject/manim_editor/actions/workflows/build_pages.yml/badge.svg" alt="MIT License"></a>\n    <br />\n    <br />\n    <i>Editor and Presenter for Manim Generated Content.</i>\n</p>\n<hr />\n\nTake a look at the [Working Example](https://manimeditorproject.github.io/manim_editor/).\nMore information can be found on the [documentation](https://manim-editor.readthedocs.io/en/stable/).\n',
    'author': 'christopher-besch',
    'author_email': 'christopher.besch@gmx.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ManimEditorProject/manim_editor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
