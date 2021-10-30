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
    'version': '0.1.2',
    'description': 'Editor and Presenter for Manim Generated Content',
    'long_description': '# Manim Editor\n\n## [Working Example](https://manimeditorproject.github.io/manim_editor/tutorial/)\n\nEditor and Presenter for Manim Generated Content\n\nhttps://manim-editor.readthedocs.io/en/latest/\n\nSince the [Section API](https://github.com/ManimCommunity/manim/pull/2152) has been merged, the Manim Web Presenter (https://github.com/christopher-besch/manim_web_presenter) will have to be rewritten.\nThis editor will take that functionality and add some more: It will be something like a "Manim video editor", where you load your scenes and record your lovely voice.\n(Here I\'ll reuse some of the presentation code, which is why these two functions, editing and presenting, will be implemented in the same repo.)\nThen it will sync the voice with the video without any user input required; loops shall be looped, seamless transitions seamlessly transitioned and pauses paused(?)\n\nMy goal is for this repo to eventually become part of the ManimCommunity Organisation.\nWith such a tool, Manim can really rival something like PowerPoint.\n\nIf anyone would like to join forces, I\'m happy to add them to the (hopefully intermediate) ManimEditorProject organisation.\n\n# Build from Source\n\n- clone repo: `git clone https://github.com/ManimEditorProject/manim_editor && cd manim_editor`\n- install poetry dependencies: `poetry install`\n- enter poetry shell: `poetry shell`\n- install npm modules: `npm ci`\n- compile web files: `npm run build_debug` or `npm run build_release`\n- start editor: `manedit`\n',
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
